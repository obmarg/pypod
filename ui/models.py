
import pickle
import os

podcastFilename = os.path.expanduser( "~/.pypodcasts" )

class Podcast(object):
    def __init__( self, feedUrl, name, downloadAll ):
        self.feedUrl = feedUrl
        self.name = name
        self.downloadAll = downloadAll

class PodcastManager(object):
    def __init__( self ):
        self.podcasts = {}

    def AddPodcast( self, podcast ):
        if podcast.name in self.podcasts:
            raise Exception( "Podcast by that name already exists" )
        self.podcasts[ podcast.name ] = podcast

    def Save( self ):
        pickle.dump( self, open( podcastFilename, 'w' ) )

    def GetPodcastList( self ):
        print "Podcasts: "
        for p in self.podcasts.itervalues():
            print p.name
        return self.podcasts.itervalues()

def GetPodcastManager():
    if not os.path.exists( podcastFilename ):
        return PodcastManager()
    try:
        manager = pickle.load( open( podcastFilename, 'r' ) )
        return manager
    except Exception as e:
        print "Error loading podcast data: "
        print e
        return PodcastManager()
