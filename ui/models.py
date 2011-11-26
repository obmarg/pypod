
import pickle
import os
import logging

log = logging.getLogger()
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
        log.debug( "Podcasts: " )
        for p in self.podcasts.itervalues():
            log.debug( p.name )
        return self.podcasts.itervalues()

def GetPodcastManager():
    if not os.path.exists( podcastFilename ):
        log.info( "%s does not exist.  Creating new PodcastManager", podcastFilename )
        return PodcastManager()
    try:
        log.debug( "Attempting to load manager from %s", podcastFilename )
        manager = pickle.load( open( podcastFilename, 'r' ) )
        log.debug( "Loaded: %r", manager )
        return manager
    except Exception as e:
        log.error( "Error loading podcast data: %s", e )
        return PodcastManager()
