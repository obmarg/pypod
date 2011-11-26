
import os
import logging
import urllib

log = logging.getLogger()

class Episode:
    def __init__( self, ref, name, url, filename ):
        """ Initialiser
            Params:
                ref - Unique reference
                name - Name of episode
                url - Remote url
                filename - Local filename
        """
        self.ref = ref
        self.name = name
        self.url = url
        self.filename = filename

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
        args = ( self.url, destFile )
        try:
            log.debug( "Downloading %s to %s", *args )
            urllib.urlretrieve( *args )
        except:
            log.error( "Failed to download %s to %s", *args )
            raise
