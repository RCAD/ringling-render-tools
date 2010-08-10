"""
This package contains script entry points for HPC job setup, cleanup, etc 
"""
import os

def env():
    """Returns a dict of relevant environment variables.""" 
    return {'OWNER': os.getenv('OWNER', None),
            'USER_DIR': r"%s" % os.getenv('USER_DIR', ''),
            'JOBID': os.getenv('CCP_JOBID', None),
            'PROJECT': r"%s" % os.getenv('PROJECT', ''),
            'SCENE': r"%s" % os.getenv('SCENE', ''),
            'NODE_PROJECT': os.path.expandvars(os.getenv('NODE_PROJECT', None)),
            'RENDERER': os.getenv('RENDERER', None)}