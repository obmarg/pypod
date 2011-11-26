#!/usr/bin/python

import feedparser
import os
import pickle
import logging
from episode import Episode

log = logging.getLogger()

class Feed:
    """ Class representing a single podcast feed """

    def __init__( self, url, destPath, limit=None, postCommand=None ):
        """ Constructor
            Params:
                url - The url of the feed
                destPath - The path to download mp3 files to
                limit - The max files to add to download 
                        list in one shot
                postCommand - A command to be run on finishing
        """
        self.url = url
        self.downloadList = []
        self.episodes = []
        self.destPath = destPath
        self.limit = limit
        self.postCommand = postCommand
        self.histFile = os.path.join( self.destPath, '.pypodhist' )

    def IsNew( self ):
        """ Checks if this feed is new """
        return len( self.episodes ) == 0

    def LoadHistory( self ):
        """ Loads the download history """
        if not os.path.exists( self.destPath ):
            return
        if not os.path.exists( self.histFile ):
            log.debug( "%s does not exist. Skipping loading", self.histFile )
            return
        with open( self.histFile, 'r') as f:
            self.episodes = pickle.load( f )
            log.debug( "Loaded %i episodes", len( self.episodes ) )

    def SaveHistory( self ):
        """ Saves the download history """
        if os.path.exists( self.destPath ):
            with open( self.histFile, 'w' ) as f:
                log.debug( "Saving %i episodes", len( self.episodes ) )
                pickle.dump( self.episodes, f )
        else:
            log.warning( "destPath doesn't exist, so not saving history" )
            log.warning( "%s", self.destPath )

    def RunUpdate( self ):
        """ Runs an update of this feed """
        self.LoadHistory()
        self.FetchFeed()
        self.DownloadFiles()
        self.SaveHistory()

    def HasEpisode( self, name ):
        """ Checks if an episode has already been download
            Params:
                name - The name of the episode to look for
            Returns True or False
        """
        return any( 
            True for e in self.episodes 
            if e.name == name
            ) 

    def FetchFeed( self ):
        """ Fetches from the rss feed """
        result = feedparser.parse( self.url )
        for entry in result.entries:
            if not self.HasEpisode( entry.title ): 
                epUrl = self.GetDownloadUrl( entry )
                if not epUrl:
                    continue
                self.AddToDownloadList( epUrl, entry.title )
        log.debug( 
                "Feed fetched.  %i total, %i new",
                len( result.entries ),
                len( self.downloadList )
                )

    def AddToDownloadList( self, link, reference ):
        """ Adds a link and reference to the download list
            Params:
                link - The link to add
                reference - A unique reference (id/title) 
                            for the download
        """
        self.downloadList.append(
                Episode( 
                    reference,
                    reference,
                    link,
                    os.path.basename( link )
                    ) )

    def GetDownloadUrl( self, entry ):
        """ Gets the mp3 download url from an rss entry
            Params:
                entry - the rss entry
            Returns:
                The url (or None) 
        """
        if entry.link and entry.link[:4] == u'.mp3':
            return entry.link
        elif entry.links:
            for linkData in entry.links:
                if ( 
                    linkData['type'] == u'audio/mpeg' or
                    linkData['href'][:-4] == u'.mp3'
                    ):
                    return linkData.href
        log.info( 
                "No download link found for %s",
                entry.title
                )
        return

    def DownloadFiles( self ):
        """ Downloads each of the files in downloadList """
        if not os.path.exists( self.destPath ):
            os.makedirs( self.destPath )
        limit = self.downloadList
        if self.limit != 0:
            limit = self.limit
        for episode in self.downloadList[limit:]:
            try:
                episode.Download( self.destPath )
                self.episodes.append( episode )
                CallPostCommand( episode )
            except:
                pass
                """ TODO: print traceback """
        else:
            log.debug( "No New Episodes" )

    def CallPostCommand( self, episode ):
        """ Call the post download command
            Params:
                episode - The episode just downloaded
        """
        pass

    def MarkAllAsDownloaded( self ):
        log.info( "Marking all as Downloaded" )
        for episode in self.downloadList:
            self.episodes.append( episode )


