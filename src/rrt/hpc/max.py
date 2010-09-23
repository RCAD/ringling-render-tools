"""
Node Prep/Release script entry points for jobs ran with `3dsmaxcmd.exe ...`
In Max jobs, PROJECT is a path to an archive zip file, which we extract to the 
NODE_PROJECT directory.
"""

import os, tempfile, zipfile
from shutil import copyfile
from rrt.hpc import env
from rrt.hpc.scripts import LOG
ENV = env()

def prep():
    with tempfile.NamedTemporaryFile(dir=ENV['NODE_PROJECT'], 
                                     prefix='max', suffix='.zip') as tmp:
        # I'm just using tempfile to generate a name, we don't want to keep 
        # the tempfile
        tmpzip = tmp.name
        tmp.close() # file is deleted when closed
    copyfile(ENV['PROJECT'], tmpzip)
    os.chdir(ENV['NODE_PROJECT'])
    zipfile.ZipFile(tmpzip).extractall()
    os.remove(tmpzip)
    # from here, we will render using %NODE_PROJECT%\\sceneName.max
    
def release():
    pass
