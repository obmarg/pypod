
import pickle
import os

podcastFilename = "~/.pypodcasts"

class Podcast(object):
    def __init__( self, feedUrl, name, downloadAll ):
        self.feedUrl = feedUrl
        self.name = name
        self.downloadAll = downloadAll

class PodcastManager(object):
    def __init__( self ):
        self.podcasts = {}
        self.maxId = 0

    def AddPodcast( self, podcast ):
        self.podcasts[ self.maxId ] = podcast
        self.maxId += 1

    def PostLoad( self ):
        self.maxId = max( self.podcasts.iterkeys ) + 1

    def Save( self ):
        pickle.dump( open( podcastFilename, 'w' ) )

    def GetPodcastList( self ):
        return self.podcasts.itervalues()

def GetPodcastManager():
    if not os.path.exists( podcastFilename ):
        return PodcastManager()
    manager = pickle.load( open( podcastFilename, 'r' ) )
    manager.PostLoad()
    return manager
