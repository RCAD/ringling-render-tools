import logging, os

__LOG_LEVEL__ = logging.DEBUG if os.getenv('RRT_DEBUG',False) else logging.INFO

def get_log(name=__name__, stream=False):
    log = logging.getLogger(name)
    log.setLevel(__LOG_LEVEL__)
    if stream:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(name)s %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
    return log
    

__VERSION__ = (0,0,1)

__version__ = '.'.join([str(n) for n in __VERSION__]) 

def get_version():
    version_string = 'Ringling Render Tools '+__version__
    return version_string

class RinglingException(Exception):pass

# Blessed  file system locations
SPOOL_LETTER = "S:"
SPOOL_UNC = "\\\\chome\\chome"
JOB_LOGS_UNC = "\\\\clogs\\clogs"
JOB_OUTPUT_UNC = "\\\\coutput\\coutput"

if os.getenv('RRT_USE_DESMOND', False):
    SPOOL_UNC = "\\\\desmond\\spool" # note the native \ style separators
    JOB_LOGS_UNC = "\\\\desmond\\spool\\logs"
    JOB_OUTPUT_UNC = "\\\\desmond\\spool\\output"
