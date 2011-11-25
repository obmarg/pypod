#!/usr/bin/python

import feedparser
import urllib
import os
import pickle
from episode import Episode

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

    def LoadHistory( self ):
        """ Loads the download history """
        if os.path.exists( self.destPath ):
            if os.path.exists( self.histFile ):
                try:
                    self.episodes = pickle.load( open( self.histFile, 'r' ) )
                except:
                    pass

    def SaveHistory( self ):
        """ Saves the download history """
        if os.path.exists( self.destPath ):
            pickle.dump( self.episodes, open( self.histFile, 'w' ) )

    def RunUpdate( self ):
        """ Runs an update of this feed """
        self.LoadHistory()
        self.FetchFeed()
        self.DownloadFiles()
        self.SaveHistory()

    def FetchFeed( self ):
        """ Fetches from the rss feed """
        result = feedparser.parse( self.url )
        for entry in result.entries:
            if entry.title not in self.episodes:
                try:
                    self.AddToDownloadList(
                        self.GetDownloadLink( entry ),
                        entry.title
                        )
                except:
                    pass

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

    def GetDownloadLink( self, entry ):
        """ Gets the mp3 download link from an rss entry
            Params:
                entry - the rss entry
            Returns:
                A link if any
            Throws:
                Exception if none found
        """
        if entry.link and entry.link[:4] == u'.mp3':
            return entry.link
        elif entry.links:
            for linkData in entry.links:
                if ( 
                    linkData['type'] == u'audio/mpeg' or
                    linkData['href'][:-4] == u'.mp3'
                    ):
                    print "Found link: " + linkData.href
                    return linkData.href
            raise Exception( "Link Not Found" )

    def DownloadFiles( self ):
        """ Downloads each of the files in downloadList """
        if not os.path.exists( self.destPath ):
            os.makedirs( self.destPath )
        limit = self.downloadList
        if self.limit != 0:
            limit = self.limit
        for episode in self.downloadList[limit:]:
            episode.Download( self.destPath )
            self.episodes.append( episode )
            CallPostCommand( episode )
            
    def CallPostCommand( self, episode ):
        """ Call the post download command
            Params:
                episode - The episode just downloaded
        """
        pass

    def MarkAllAsDownloaded( self ):
        for episode in self.downloadList:
            self.episodes.append( episode )


