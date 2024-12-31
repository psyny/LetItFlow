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
            
    # Override do_GET to route GET requests
    def do_GET(self):
        print("GET request received")  # Debugging
        self.router(self, "GET")

    # Override do_POST to route POST requests
    def do_POST(self):
        print("POST request received")  # Debugging
        self.router(self, "POST")
        
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
