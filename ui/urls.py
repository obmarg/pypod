
import re
from views import Index, AddPodcast, RemovePodcast
from baseviews import File, Folder

class Url(object):
    """ Object representing a URL """

    def __init__( self, regexp, view ):
        """ Constructor
            Params:
                regexp - String regular expression to match
                view - View function/class this url presents
        """
        self.regexp = re.compile( regexp )
        self.view = view

    def Matches( self, url ):
        """ Checks if a user is requesting this url """
        return self.regexp.match( url )

Urls = [ 
        Url( r"^/$", Index ),
        Url( r"^/api/addPodcast$", AddPodcast ),
        Url( r"^/api/removePodcast$", RemovePodcast ),
        Url( r"^/style.css$", File( "scripts/style.css" ) ),
        Url( r"^/jquery.js$", File( "scripts/jquery/js/jquery-1.7.1.js" ) ),
        Url( r"^/jquery-ui.js$", File( "scripts/jquery/js/jquery-ui-1.8.16.custom.min.js" ) ),
        Url( r"^/jquery-ui.css$", File( "scripts/jquery/css/blitzer/jquery-ui-1.8.16.custom.css" ) ),
        Url( r"^/images/.*$", Folder( "scripts/jquery/css/blitzer/images/", "/images/" ) ), 
        Url( r"^/jquery.qtip.js", File( "scripts/jquery/js/jquery.qtip.min.js" ) ),
        Url( r"^/jquery.qtip.css", File( "scripts/jquery/css/jquery.qtip.min.css" ) ),
        ]

