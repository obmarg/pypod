
from baseviews import TemplateView, BaseView, BaseResponse
from models import GetPodcastManager, PodcastManager, Podcast

class Index(TemplateView):
    """ Index view """
    template = "index.tpl"

    def GetData( self ):
        pm = GetPodcastManager()
        return {
                'podcasts' : pm.GetPodcastList()
                }

class AddPodcast(BaseView):
    """ View that handles an add podcast request """
    
    def RunView( self ):
        args = self.handler.GetPostVars([
            "url",
            "name",
            "da"
            ])
        pm = GetPodcastManager()
        p = Podcast( 
                args["url"][0],
                args["name"][0],
                args["da"][0] == "2" 
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

