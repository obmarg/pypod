
import BaseHTTPServer
import cgi
import sys,traceback
#TODO: Uncomment this at some point when finished shit
#from .urls import Urls
import re
from views import Index, File, Folder

Urls = [ 
        ( re.compile(r"^/$"), Index ),
        ( re.compile( r"^/style.css$" ), File( "scripts/style.css" ) ),
        ( re.compile( r"^/jquery.js$" ), File( "scripts/jquery/js/jquery-1.7.1.js" ) ),
        ( re.compile( "^/jquery-ui.js$" ), File(
        "scripts/jquery/js/jquery-ui-1.8.16.custom.min.js" ) ),
        ( re.compile( "^/jquery-ui.css$" ), File(
        "scripts/jquery/css/blitzer/jquery-ui-1.8.16.custom.css" ) ),
        ( re.compile( "^/images/.*$" ), Folder(
        "scripts/jquery/css/blitzer/images/", "/images/" ) ), 
        ]

class Handler( BaseHTTPServer.BaseHTTPRequestHandler ):
    urls = Urls
    debug = True

    def CheckUrl( self, url ):
        """ Checks if a url is registered
            Params:
                url - The url the client has requested
            Return:
                A Url handler function, or None
        """
        print "URL: %s" % url
        for( regexp, view ) in self.urls:
            if regexp.match( self.path ):
                print "matched %r" % regexp
                return view
        return None

    def do_GET( self ):
        """ Handles GET requests from clients """
        view = self.CheckUrl( self.path )
        if view is None:
            self.Send404()
            return
        try:
            v = view( self )
            v.RunView()
            response = v.response
            self.send_response(200)
            self.send_header( 'Content-type', response.mimetype )
            self.end_headers()
            self.wfile.write( response.data )
            return
        except Exception as e:
            self.Send500( str( e ) )
            print "Server Error: "
            traceback.print_exc(file=sys.stdout) 
            return

    def do_POST( self ):
        """ Handles POST requests from clients. """
        pass

    def Send404( self, message=None ):
        """ Sends a 404 Error Back to the client
            Params:
                message - An optional description message to send
        """
        self.SendError( 404, message )


    def Send500( self, message=None ):
        """ Sends a 500 Server Error Back to the client
            Params:
                message - An optional description message to send
        """
        self.SendError( 500, message )
    
    def SendError( self, errNum, message=None ):
        """ Sends an error back to the client
            Params:
                errNum - The error number.  e.g. 404, 500
                message - An optional description message to send
        """
        self.send_response(errNum)
        self.end_headers()
        self.wfile.write(
                "<html><head><title>" + str( errNum ) + " Error</title></head><body>"
                )
        self.wfile.write( str( errNum ) + " Error")
        if message:
            self.wfile.write(": " + message )
        self.wfile.write("</body></html>")


