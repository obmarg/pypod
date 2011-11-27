
import pickle
import os
import logging

log = logging.getLogger()
podcastFilename = os.path.expanduser( "~/.pypodcasts" )

class Podcast(object):
    """ Class containing config data for a podcast """

    def __init__( self, feedUrl, name, downloadAll, destFilenameFormat ):
        """ Constructor
            Params:
                feedUrl - The url of the rss feed
                name - The name of the podcast
                downloadAll - Should we download all previous podcasts?
                destFilenameFormat - The format of the destination filename
        """
        self.feedUrl = feedUrl
        self.name = name
        self.downloadAll = downloadAll
        self.destFilenameFormat = destFilenameFormat

class PodcastManager(object):
    """ Manager class for podcast configuration objects """

    def __init__( self ):
        self.podcasts = {}

    def AddPodcast( self, podcast ):
        """ Add a podcast to the manager
            Params:
                podcast - The podcast to add
            Throws if podcast with same name already exists
        """
        if podcast.name in self.podcasts:
            raise Exception( "Podcast by that name already exists" )
        self.podcasts[ podcast.name ] = podcast

    def RemovePodcast( self, name ):
        """ Removes a podcast
            Params:
                name - The name of the podcast to remove
            Throws if podcast does not exist
        """
        if name not in self.podcasts:
            raise Exception( "Podcast by that name does not exist" )
        #TODO: Would be good to delete the pypod podcast data files here
        del self.podcasts[ name ]

    def Save( self ):
        """ Save the podcast information to disk """
        pickle.dump( self, open( podcastFilename, 'w' ) )

    def GetPodcastList( self ):
        """ Returns a list of podcasts """
        log.debug( "Podcasts: " )
        for p in self.podcasts.itervalues():
            log.debug( p.name )
        return self.podcasts.itervalues()

def GetPodcastManager():
    """ Function to load a podcast manager from disk
        Returns a PodcastManager
    """
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
