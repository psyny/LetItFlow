from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
import webbrowser
import json
import uuid

from backend.libs.psn.appconfig.appconfig import AppConfig
from backend.controllers.app.app_controller import AppController
from backend.models.player import Player


def BuildResponse(ctx, obj, code: int, status: str, message: str, responseData):
    responseData["status"] = status
    responseData["message"] = message
    obj._setsDefaultResponseHeaders(ctx, code)
    obj._writeJsonResponse(ctx, responseData)

def CanAccess(minAccessLevel: str, viewtype: str, token: str, targetPlayerId: str, allowSelf: bool):
    # Needed Controllers
    player_controller = AppController().playercontroller
    credentials_controller = AppController().credentialsController

    # Spectator Check
    if viewtype == "spectator":
        levelDiff = Player.accessLevelCompare(minAccessLevel, Player.AcessLevel.SPECTATOR.value)
        if levelDiff < 0:
            return False, "not enough access"
        else:
            return True, ""
        
    # Player Check
    tokenPlayerId = credentials_controller.token_validate(token)
    if tokenPlayerId == None:
        return False, "invalid token"

    tokenPlayer = player_controller.get_player_by_id(tokenPlayerId)
    if tokenPlayer == None:
        return False, "invalid player"
    
    if allowSelf:
        if tokenPlayerId == targetPlayerId:
            return True, ""
    
    levelDiff = Player.accessLevelCompare(Player.AcessLevel.DUNGEONMASTER.value, tokenPlayer.accessLevelDefault)
    if levelDiff < 0:
        return False, "not enough access"

class ServerController(SimpleHTTPRequestHandler):   
    sseClients = dict()
    
    class SSEClient:
        def __init__(self, streamHandler, clientId):
            self.streamHandler = streamHandler
            self.clientId = clientId
            
    # Set default GET to our router
    def do_GET(self):
        # Redirect to filelike server
        if self.path.startswith('/web/'):
            return SimpleHTTPRequestHandler.do_GET(self)
        
        # Redirect to event stream
        elif self.path.startswith('/events/'):
            # Get client id
            clientId = self.headers.get('Client-id')
            if clientId == None:
                clientId = str(uuid.uuid4())
            
            # Open SSE stream
            self.send_response(200, "ok")
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()

            # Add client to the list of connected clients
            sseClient = ServerController.SSEClient(self.wfile, clientId)
            ServerController.sseClients[clientId] = sseClient
            
        else:        
            # Redirect to endpoint router
            self.router(self, "GET")            

    # Set default POST to our router        
    def do_POST(self):
        self.router(self, "POST")
   
    # Handshake Options for CORs Setup        
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        
    # Checks if the received POST payload is a JSON type
    def _isPostPayloadJson(self, ctx):
        if ctx.headers.get("Content-Type") != 'application/json':
            ctx.send_response(400)
            ctx.end_headers()
            return False
        
        return True        
        
    # Get the payload in Python data structure (dicts, lists and primitives)
    def _getPayload(self, ctx, opts):
        contentLength = int(ctx.headers['Content-Length'])
        postDataBytes = ctx.rfile.read(contentLength)
        postDataStr = postDataBytes.decode('utf-8')
        payload = json.loads(postDataStr)
        return payload
    
    # Sets a default response to the ctx
    def _setsDefaultResponseHeaders(self, ctx, response = 200, contentType = 'application/json'):
        ctx.send_response(response)
        ctx.send_header("Content-type", contentType)
        ctx.send_header('Access-Control-Allow-Origin', '*')
        ctx.end_headers()   
        return True

    # Writes JSON response to body
    def _writeJsonResponse(self, ctx, jsonObj, encoding = 'utf_8'):
        ctx.wfile.write(json.dumps(jsonObj).encode(encoding=encoding)) 
        return True
    
    # Writes a TEXT response to body
    # The function will attempt to cast each element of outputList as string and write it
    def _writeTextResponse(self, ctx, outputList, encoding = 'utf_8'):
        for outputObj in outputList:
            ctx.wfile.write(bytes(str(outputObj), encoding))
        return True
    
    # Broadcasts a message to all connected SSE clients
    def _sse_broadcast(self, message, clientIds = None):
        # Filter clients to receive the message
        clientsToReceive = list()
        if clientIds == None:
            clientsToReceive = ServerController.sseClients.values()
        else:
            for clientId in clientIds:
                client = ServerController.sseClients.get(clientId)
                if client != None:
                    clientsToReceive.append(client) 
                    
        # Send the message
        messagesSent = 0        
        for client in clientsToReceive:
            try:
                streamHandler = client.streamHandler
                streamHandler.write(f"data: {message}\n\n".encode('utf-8'))
                streamHandler.flush()
                messagesSent += 1
            except (BrokenPipeError, OSError):
                print("Client disconnected.")
                del ServerController.sseClients[client.clientId]
        
  
        return messagesSent

    
    # Fallback for invalid endpoints    
    def invalidEndpoint(self, ctx, opts):
        self._setsDefaultResponseHeaders(ctx, 200, "text/html")
        
        responseBody = [
            "<html><head><title>Page Title</title></head>",
            "<p>Request: %s</p>" % self.path,
            "<body>",
            "<p>Invalid Endpoint.</p>",
            "</body></html>",
        ]
        self._writeTextResponse(ctx, responseBody)
        
    # GET type endpoint with a JSON response        
    def endpointExample_GET(self, ctx, opts):        
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        
        # Response - Data
        responseData = {"response": True}
        self._writeJsonResponse(ctx, responseData)

    # POST type endpoint with a JSON response equals its payload
    def endpointExample_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)

        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200) 
        
        # Response - Data
        self._writeJsonResponse(ctx, payload)   
        
    # POST type endpoint with that broadcasts SSE to all its clients
    def broadcastSseExample_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)
        payloadStr = json.dumps(payload).encode(encoding='utf-8')
        
        # Broadcasts the SSE
        messagesSent = self._sse_broadcast(payloadStr, None)

        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200) 
        
        # Response - Data
        payload["messagesSent"] = str(messagesSent)
        self._writeJsonResponse(ctx, payload)           
        

    # ------------------------------------------------------------------------------------------        
    # ------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------
        
    # Helper to organize routes
    def router(self, ctx, mode):   
        print(f"Received {mode} request at {ctx.path}")

        get_routes = {
                None: self.invalidEndpoint,
                '/getEndpointExample': self.endpointExample_GET,  
            }

        post_routes = {
                None: self.invalidEndpoint,
                '/postEndpointExample': self.endpointExample_POST,
                '/broadcastSseExample': self.broadcastSseExample_POST,
                '/login': self.login_POST,
                '/actions': self.actions_POST,
                '/macro': self.macro_POST,
                '/refreshstate': self.refreshstate_POST,
                '/character': self.character_POST,
                '/player': self.player_POST,
                '/party': self.party_POST,
            }
        
        def getRouteFunc(path, routeDict):
            return routeDict.get(path, routeDict[None])
        
        routes = None
        if mode == "GET":
            routes = get_routes
        elif mode == "POST":
            routes = post_routes
            
        routeFunc = getRouteFunc(ctx.path, routes)        
        routeFunc(ctx,None)     

    # POST: /login
    def login_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)

        username = payload.get("username")
        password = payload.get("password")
        viewtype = payload.get("viewtype")

        if username == None or password == None or viewtype == None:
            BuildResponse(ctx, self, 400, "fail", "missing input", {"token": "---"})
            return

        # Needed Controllers
        player_controller = AppController().playercontroller
        credentials_controller = AppController().credentialsController

        # Admin first login case
        if username == "admin":
            adminExists = credentials_controller.player_exists(username)
            if not adminExists:
                credentials_controller.change_player_key(username, password)
                adminPlayer = Player(username, "admin")
                adminPlayer.accessLevel = Player.AcessLevel.DUNGEONMASTER
                player_controller.save_player(adminPlayer)

        # Check credentials - Spectator
        if viewtype == Player.AcessLevel.SPECTATOR.value:
            BuildResponse(ctx, self, 200, "success", "spectator", {"token": "---"})
            return

        # Check credentials - Player
        valid = credentials_controller.validate_credentials(username, password)
        if valid == False:
            BuildResponse(ctx, self, 401, "fail", "invalid credentials", {"token": "---"})
            return
        
        else:
            token = credentials_controller.token_generate(username)
            BuildResponse(ctx, self, 200, "success", "", {"token": str(token)})
            return

    # POST: /actions
    def actions_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        # Response - Stub
        responseData = {
            "status": "success"
        }
        self._writeJsonResponse(ctx, responseData)

    # POST: /macro
    def macro_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        # Response - Stub
        responseData = {
            "status": "success"
        }
        self._writeJsonResponse(ctx, responseData)

    # POST: /refreshstate
    def refreshstate_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        # Response - Stub
        responseData = {
            "statePoint": 123,
            "gameState": {},
            "actions": []
        }
        self._writeJsonResponse(ctx, responseData)

    # POST: /character
    def character_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        # Response - Stub
        responseData = {
            "status": "success"
        }
        self._writeJsonResponse(ctx, responseData)

    # POST: /player
    def player_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)

        token = payload.get("token")
        viewtype = payload.get("viewtype")
        operation = payload.get("operation")

        if token == None or viewtype == None:
            BuildResponse(ctx, self, 400, "fail", "missing input", {})
            return
        
        # Player Payload
        playerData = payload.get("player")
        if playerData == None:
            BuildResponse(ctx, self, 400, "fail", "missing player data", {})
            return
        
        playerDataId = playerData.get("playerId")
        if playerDataId == None:
            BuildResponse(ctx, self, 400, "fail", "missing player id", {})
            return

        # Access Checks
        can, msg = CanAccess(Player.AcessLevel.DUNGEONMASTER.value, viewtype, token, playerDataId, False)
        if can == False:
            BuildResponse(ctx, self, 401, "fail", msg, {})
            return

        # Needed Controllers
        player_controller = AppController().playercontroller
        credentials_controller = AppController().credentialsController

        # Operation - Get
        if operation == "get":
            # TODO: Finish here
            pass

        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 400)

        # Response - Stub
        responseData = {
            "status": "fail",
            "message": "invalid operation",
        }
        self._writeJsonResponse(ctx, responseData)

    # POST: /party
    def party_POST(self, ctx, opts):
        # Request - Check Datatype
        if not self._isPostPayloadJson(ctx):
            return
        # Request - Get Payload
        payload = self._getPayload(ctx, opts)
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        # Response - Stub
        responseData = {
            "status": "success"
        }
        self._writeJsonResponse(ctx, responseData)

    # Other methods...

class ThreadedTCPServer(ThreadingTCPServer):
    allow_reuse_address = True

# Start APP
if __name__ == '__main__':
    # Load external appconfig
    appConfig = AppConfig()

    # Start server
    with ThreadedTCPServer((appConfig.get("hostname"), appConfig.get("hostport")), ServerController) as server:
        server_address = f"http://{appConfig.get('hostname')}:{appConfig.get('hostport')}"
        print(f"Server started: {server_address}")
        webbrowser.open(server_address)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server.")
            server.shutdown()

    server.server_close()
    print("Server stopped.")
