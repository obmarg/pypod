
import os
import mimetypes
from jinja2 import Environment, FileSystemLoader
from models import GetPodcastManager, PodcastManager, Podcast

templatePath = "templates"

class BaseResponse:
    """ Basic http response class """

    def __init__( self ):
        self.mimetype = ""
        self.data = ""

class BaseView(object):
    """ Base class for views
        Class variables:
            mimetype - The mimetype of the view content
    """
    mimetype = "text/html"

    def __init__( self, handler ):
        """ Constructor
            Params:
                handler - The HttpRequestHandler
        """
        self.response = BaseResponse()
        self.response.mimetype = self.mimetype
        self.handler = handler
        
    def RunView( self ):
        """ Runs a views code.  Should be overridden
            to provide content
        """
        return

class FileView(BaseView):
    """ Base class for text file based views """
    
    def __init__( self, filename, *pargs, **kwargs ):
        """ Constructor
            Params:
                filename - filename to serve
        """
        self.mimetype = mimetypes.guess_type( filename )[0]
        super( FileView, self ).__init__( *pargs, **kwargs )
        self.filename = filename

    def RunView( self ):
        """ Reads in a file for data """
        self.response.data = open( self.filename ).read()

def File( filename ):
    """ Factory function for FileView """
    def inner( handler ):
        return FileView( filename, handler )
    return inner

class FolderView(BaseView):
    """ Base class for views of entire folders """

    def __init__( self, path, urlPrefix, *pargs, **kwargs ):
        """ Constructor
            Params:
                path - The path to expose
                urlPrefix - The url prefix
        """
        super( FolderView, self ).__init__( *pargs, **kwargs )
        self.path = path
        self.urlPrefix = urlPrefix

    def RunView( self ):
        """ Runs the view """
        if not self.handler.path.startswith( self.urlPrefix ):
            print "Prefix: %s" % self.urlPrefix
            print "Actual: %s" % self.handler.path
            raise Exception( "Path doesn't match folder path prefix" )
        subPath = self.handler.path[len( self.urlPrefix ):]
        path = os.path.normpath( self.path + subPath )
        if not path.startswith( self.path ):
            raise Exception( "Symbolic links or trickery being used in FolderView")
        self.response.mimetype = mimetypes.guess_type( path )
        self.response.data = open( path, 'r' ).read()

def Folder( path, urlPrefix ):
    """ Factory function for FolderView """
    def inner( handler ):
        return FolderView( path, urlPrefix, handler )
    return inner

class TemplateView(BaseView):
    """ Base class for template based views 
        Class variables:
            template - The name of the template for the view
    """

    def __init__( self, *pargs, **kwargs ):
        super( TemplateView, self ).__init__( *pargs, **kwargs )
        self.env = Environment(
                loader = FileSystemLoader( templatePath ),
                trim_blocks = True
                )

    def RunView( self ):
        """ Runs the code for the view """
        t = self.env.get_template( self.template )
        self.response.data = t.render( self.GetData() )

    def GetData( self ):
        """ Gets a dictionary for the template data
            Should be overriden by child classes
        """
        return {}

class Index(TemplateView):
    """ Index view """
    template = "index.tpl"

    def GetData( self ):
        pm = GetPodcastManager()
        return {
                'podcasts' : pm.GetPodcastList()
                }

