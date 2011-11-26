
import BaseHTTPServer
import threading
from handler import Handler

class Server:
    def __init__( self, address, port ):
        self.endpoint = ( address, port )
        self.httpd = BaseHTTPServer.HTTPServer( self.endpoint, Handler )

    def RunServer( self ):
        self.httpd.serve_forever()
    
    def ShutdownServer( self ):
        self.httpd.shutdown()
