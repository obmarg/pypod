
import os
import logging

log = logging.getLogger()

class Episode:
    def __init__( self, ref, name, url, filename ):
        """ Initialiser
            Params:
                ref - Unique reference
                name - Name of episode
                url - Remote url
                filename filename
        """
        self.ref = ref
        self.name = name
        self.url = url
        self.filename = localPath

    def Download( self, path, force=False ):
        """ Downloads the podcast, if not already done
            Params:
                path - The destination path
                force - If true, overwrite any existing
                        files
        """
        destFile = os.path.join( path, self.filename )
        if os.path.exists( destFile ) and not force:
            return
        try:
            a = ( link, destFile )
            log.debug( "Downloading %s to %s", *a )
            urllib.urlretrieve( *a )
            self.history.append( reference )
            self.CallPostCommand( reference, link )
        except:
            print "Failed to download " + link

