"""
This package contains script entry points for HPC job setup, cleanup, etc 
"""
import os

def env():
    """Returns a dict of relevant environment variables.""" 
    return {'OWNER': os.getenv('OWNER', None),
            'PROJECT': os.getenv('PROJECT', None),
            'SCENE': os.getenv('SCENE', None),
            'NODE_PROJECT': os.getenv('NODE_PROJECT', None),
            'RENDERER': os.getenv('RENDERER', None),
            'LOGS': os.getenv('LOGS', None),
            'STATS': os.getenv('STATS', None),
            'OUTPUT': os.getenv('OUTPUT', None)}