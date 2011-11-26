#!/usr/bin/python

import os
import traceback
import sys
import threading
import logging
import argparse
from feed import Feed
from ui.server import Server
from ui.models import GetPodcastManager

log = logging.getLogger()

class PyPod:
    """ Main pypod class """

    fetchInterval = 60 * 60    # Fetch every hour

    def __init__( self, ipAddr, port, destPath ):
        """ Constructor.
            Params:
                ipAddr - The ip address to run the ui on
                port - The port to run the ui on
                destPath - The root folder to download to
        """
        self.server = Server( ipAddr, int( port ) )
        self.destPath = destPath
        self.timer = threading.Timer( self.fetchInterval, self.RunFetch )

    def Run( self ):
        """ Runs the server """
        threading.Thread( target=self.RunFetch ).start()
        self.server.RunServer()

    def Stop( self ):
        """ Stops the server """
        self.server.ShutdownServer()
        if self.timer:
            self.timer.cancel()
        
    def RunFetch( self ):
        """ Runs a fetch of all current podcasts """
        pm = GetPodcastManager()
        log.debug( "Loaded %i podcasts", len( pm.podcasts ) )
        for podcast in pm.GetPodcastList():
            try:
                f = Feed( 
                    podcast.feedUrl,
                    os.path.join( self.destPath, podcast.name )
                    )
                log.info( "Running fetch for %s", podcast.name )
                self.FetchFeed( f, podcast.downloadAll )
            except Exception as e:
                log.error( "Error when fetching %s", podcast.name )
                traceback.print_exc(file=sys.stdout)
        self.ScheduleFetch()

    def FetchFeed( self, feed, downloadAll ):
        """ Fetches a single feed 
            Params:
                feed - The feed to fetch
                downloadAll - True if all history should be downloaded
        """
        feed.LoadHistory()
        markAllRead = feed.IsNew() and not downloadAll
        feed.FetchFeed()
        if markAllRead:
            feed.MarkAllAsDownloaded()
        else:
            feed.DownloadFiles()
        feed.SaveHistory()

    def ScheduleFetch( self ):
        """ Schedules the next fetch """
        self.timer.start()


if __name__ == "__main__":
    logging.basicConfig( level=logging.INFO )
    argParser = argparse.ArgumentParser( 
        description="Basic Python Podcatcher"
        )
    argParser.add_argument(
        'args',
        metavar=( '<ip>', '<port>', '<download path>' ),
        nargs=3
        )
    args = argParser.parse_args()

    p = PyPod( *args.args )
    try:
        p.Run()
    except KeyboardInterrupt:
        print "Interrupted by keyboard"
        p.Stop()

