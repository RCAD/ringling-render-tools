"""
Node Prep/Release script entry points for jobs ran with `Render.exe -r sw ...`
"""
import os
from shutil import copyfile, copytree
from rrt.hpc import env
from rrt.hpc.scripts import LOG
ENV = env()

def _setup_node_project():
    LOG.info("Setting up node project directory: %s" % ENV['NODE_PROJECT'])
    if not os.path.isdir(ENV['NODE_PROJECT']):
        os.makedirs(ENV['NODE_PROJECT'])
    src = os.path.join(ENV['PROJECT'],'workspace.mel')
    dst = os.path.join(ENV['NODE_PROJECT'],'workspace.mel')
    copyfile(src, dst)
    LOG.debug("File copied: %s -> %s" % (src,dst))
    LOG.debug("node local workspace:")
    LOG.debug(open(dst).read())
    
    LOG.info("Copying any fur data...")
    for name in os.listdir(ENV['PROJECT']):
        src = os.path.join(ENV['PROJECT'], name)
        if name.startswith('fur') and os.path.isdir(src):
            dst = os.path.join(ENV['NODE_PROJECT'], name)
            copytree(src, dst)
            LOG.debug("File copied: %s -> %s" % (src,dst))

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
