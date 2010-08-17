"""
Node Prep/Release script entry points for jobs ran with `Render.exe -r sw ...`
"""
import os
from shutil import copyfile
from rrt.hpc import env
from rrt.hpc.scripts import LOG
from rrt.maya.helpers import ProjectPath
ENV = env()

def _setup_node_project():
    LOG.info("Setting up node project directory: %s" % ENV['NODE_PROJECT'])
    if not os.path.isdir(ENV['NODE_PROJECT']):
        os.makedirs(ENV['NODE_PROJECT'])
    src = ProjectPath(ENV['PROJECT']+r'\workspace.mel').unc
    dst = os.path.join(ENV['NODE_PROJECT'],'workspace.mel')
    copyfile(src,dst)
    LOG.debug("File copied: %s -> %s" % (src,dst))
    LOG.debug("node local workspace:")
    LOG.debug(open(dst).read())


def _create_startup_script():
    dst = os.path.join(ENV['NODE_PROJECT'],'scripts','userSetup.mel')
    LOG.info("Writing %s" % dst)
    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    with open(dst,'wb') as fh:
        fh.write('python("import rrt.hpc.maya.startup");\n')


def prep():
    _setup_node_project()
    _create_startup_script()


def release():pass
