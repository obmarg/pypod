
import pickle
import os

historyFilename = os.path.expanduser( "~/.pypodhistory" )

def Load():
    """ Loads the history. If it exists
        Should return an empty dictionary if not
    """
    if os.path.exists( historyFilename ):
        with open( historyFilename, 'r' ) as f:
            return pickle.load( f )
    else:
        return {}

def Save( history ):
    """ Saves the history to a file """
    with open( historyFilename, 'w' ) as f:
        pickle.dump( history, f )
