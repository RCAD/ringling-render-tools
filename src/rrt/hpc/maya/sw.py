"""
Node Prep/Release script entry points for jobs ran with `Render.exe -r sw ...`
"""
import os
from shutil import copyfile
from subprocess import call
from rrt.hpc import env
from rrt.hpc.scripts import LOG
from rrt import SPOOL_UNC
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


def _cleanup_node_project():
    LOG.info("Cleaning up node project: %s" % ENV['NODE_PROJECT'])
    LOG.info("\tCalculating size...")
    LOG.info("\tThis could take a while...")
    size = sum([os.path.getsize(os.path.join(root,f)) for root,dirs,files in os.walk(ENV['NODE_PROJECT']) for f in files])
    LOG.info("\t%0.1f MB" % (size/(1024*1024.0)))
    call('rmdir /S /Q %s' % ENV['NODE_PROJECT'], shell=True)

def _setup_dirmaps():
    dst = os.path.join(ENV['NODE_PROJECT'],'scripts','userSetup.mel')
    LOG.info("Writing Dirmaps to: %s" % dst)
    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    proj = ProjectPath(ENV['PROJECT'])
    root = ProjectPath(SPOOL_UNC)
    map_pairs = (
        (proj.ppath, proj.punc),
        (proj.ppath+'//', proj.punc+'/'), 
        (root.ppath, root.punc),
        (ENV['NODE_PROJECT'].replace('\\','/'), proj.punc)
    )
    maps = ['dirmap -m "%s" "%s";' % pair for pair in map_pairs]
    maps.append('dirmap -en on;')
    with open(dst,'wb') as fh:
        fh.write(os.linesep.join(maps))
    with open(dst, 'rb') as fh:
        LOG.debug(fh.read())


def prep():
    _setup_node_project()
    _setup_dirmaps()


def release():
    _cleanup_node_project()
