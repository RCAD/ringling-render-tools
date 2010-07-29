import logging

__LOG_LEVEL__ = logging.DEBUG

def get_log(name=__name__):
    log = logging.getLogger(name)
    log.setLevel(__LOG_LEVEL__)
    return log
    

__VERSION__ = (0,0,1)
__VERSION_TAG__ = "rc3"

__version__ = '.'.join([str(n) for n in __VERSION__]) 
if __VERSION_TAG__:
    __version__ += __VERSION_TAG__

def get_version():
    version_string = 'Ringling Render Tools '+__version__
    return version_string