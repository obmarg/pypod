
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
                filename - Destination filename (including path)
        """
        self.ref = ref
        self.name = name
        self.url = url
        self.destFilename = filename

    def Download( self, force=False ):
        """ Downloads the podcast, if not already done
            Params:
                force - If true, overwrite any existing
                        files
        """
        if os.path.exists( self.destFilename ) and not force:
            return
        args = ( self.url, self.destFilename )
        try:
            log.debug( "Downloading %s to %s", *args )
            urllib.urlretrieve( *args )
        except:
            log.error( "Failed to download %s to %s", *args )
            raise
