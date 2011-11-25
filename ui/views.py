
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

