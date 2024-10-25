from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
import webbrowser
import json
import uuid

from backend.libs.psn.appconfig.appconfig import AppConfig

class ServerController(SimpleHTTPRequestHandler):   
    sseClients = dict()
    
    class SSEClient:
        def __init__(self, streamHandler, clientId):
            self.streamHandler = streamHandler
            self.clientId = clientId

    # Helper to organize routes
    def router(self, ctx, mode):    
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
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        # Response - Stub
        responseData = {
            "status": "success",
            "permission": "admin"
        }
        self._writeJsonResponse(ctx, responseData)

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
        # Response - Headers      
        self._setsDefaultResponseHeaders(ctx, 200)
        # Response - Stub
        responseData = {
            "status": "success"
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
