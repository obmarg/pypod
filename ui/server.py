
import BaseHTTPServer
from handler import Handler

class Server:
    def __init__( self, address, port ):
        self.endpoint = ( address, port )
        self.httpd = BaseHTTPServer.HTTPServer( self.endpoint, Handler )

    def RunServer( self ):
        #TODO: Spawn a thread
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            self.httpd.socket.close()


