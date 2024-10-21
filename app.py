from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
import webbrowser
import json
import uuid

HostName = "localhost"
HostPort = 8080

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
        
        
class ThreadedTCPServer(ThreadingTCPServer):
    allow_reuse_address = True

# Start APP
if __name__ == '__main__':
    with ThreadedTCPServer((HostName, HostPort), ServerController) as server:
        server_address = f"http://{HostName}:{HostPort}"
        print(f"Server started: {server_address}")
        webbrowser.open(server_address)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server.")
            server.shutdown()

    server.server_close()
    print("Server stopped.")