
from baseviews import TemplateView, BaseView, BaseResponse
from models import GetPodcastManager, PodcastManager, Podcast

class Index(TemplateView):
    """ Index view """
    template = "index.tpl"

    destFilenameFormatHelp = """
        %filename% - The Original Download Filename
        %title% - The Title Of The Podcast Episode
        %podcastname% - The Podcast Name
        """
    defaultDestFilenameFormat = "%podcastname%/%filename%"

    def GetData( self ):
        pm = GetPodcastManager()
        return {
                'podcasts' : pm.GetPodcastList(),
                'podcastNames' : [ p.name for p in pm.GetPodcastList() ],
                'destFilenameFormatHelp' : self.destFilenameFormatHelp,
                'defaultDestFilenameFormat' : self.defaultDestFilenameFormat
                }

class AddPodcast(BaseView):
    """ View that handles an add podcast request """
    
    def RunView( self ):
        args = self.handler.GetPostVars([
            "url",
            "name",
            "da",
            "filenameFormat"
            ])
        pm = GetPodcastManager()
        p = Podcast( 
                args["url"][0],
                args["name"][0],
                args["da"][0] == "2",
                args["filenameFormat"][0]
                )
        pm.AddPodcast( p )
        pm.Save()
        self.response.data = "OK!"

class RemovePodcast(BaseView):
    """ View that handles a remove podcast request """

    def RunView( self ):
        args = self.handler.GetPostVars([
            "name"
            ])
        pm = GetPodcastManager()
        pm.RemovePodcast( args["name"][0] )
        pm.Save()
        self.response.data = "OK!"

