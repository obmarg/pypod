#!/usr/bin/python

import feedparser
import os
import pickle
import logging
from episode import Episode

log = logging.getLogger()

class Feed:
    """ Class representing a single podcast feed """

    def __init__( 
            self,
            name,
            url, 
            destPath,
            episodes,
            limit=0, 
            postCommand=None,
            destFilenameFormat=None
            ):
        """ Constructor
            Params:
                name - The name of the podcast
                url - The url of the feed
                destPath - The path to download mp3 files to
                episodes - A list of already downloaded episodes
                limit - The max files to add to download 
                        list in one shot
                postCommand - A command to be run on finishing
                destFilenameFormat - The format for destination filenames
        """
        self.name = name
        self.url = url
        self.destPath = destPath
        self.episodes = episodes
        self.downloadList = []
        self.limit = limit
        self.postCommand = postCommand
        if destFilenameFormat:
            self.destFilenameFormat = destFilenameFormat.rstrip()
        else:
            self.destFilenameFormat = "%podcastname%/%filename%"

    def IsNew( self ):
        """ Checks if this feed is new """
        return len( self.episodes ) == 0

    def RunUpdate( self ):
        """ Runs an update of this feed """
        self.FetchFeed()
        self.DownloadFiles()

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
                self.AddToDownloadList( 
                        epUrl, 
                        entry.title,
                        self.MakeEpisodeFilename( 
                            entry,
                            epUrl
                            ) )
        log.debug( 
                "Feed fetched.  %i total, %i new",
                len( result.entries ),
                len( self.downloadList )
                )

    def AddToDownloadList( self, link, title, destFilename ):
        """ Adds a link and reference to the download list
            Params:
                link - The link to add
                title - The title of this episode
                destFilename - The destination filename
        """
        self.downloadList.append(
                Episode( 
                    title,
                    title,
                    link,
                    destFilename
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
        limit = len( self.downloadList )
        if self.limit != 0:
            limit = self.limit
        for episode in self.downloadList[:limit]:
            try:
                episode.Download()
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
        """ Marks everything in the downloaded list as downloaded """
        log.info( "Marking all as Downloaded" )
        for episode in self.downloadList:
            self.episodes.append( episode )

    def MakeEpisodeFilename( self, entry, url=None ):
        """ Makes a filename for an episode.
            Params:
                entry - The rss feed entry for this episode 
                url - The url for this episode.
                      Will be calculated if not set
            Returns the destination filename, including full path    
        """
        if url == None:
            url = self.MakeDownloadUrl( entry )

        urlBasename = os.path.basename( url )
        urlBasenameExt = urlBasename.rfind( '.' )
        if urlBasenameExt != -1:
            urlFilename = urlBasename[:urlBasenameExt]
            urlExt = urlBasename[urlBasenameExt:]
        else:
            urlFilename = urlBasename
            urlExt = ""

        destFilenameSubs = [
                ( '%filename%', urlFilename ),
                ( '%title%', entry.title ),
                ( '%podcastname%', self.name ),
                ]

        rv = self.destFilenameFormat
        log.debug( "Initial filename: %s", rv )
        for search, replace in destFilenameSubs:
            rv = rv.replace( search, replace )
            log.debug( "New filename: %s", rv )
        rv = os.path.join( self.destPath, rv + urlExt )
        log.debug( "Returning %s", rv )
        return rv
