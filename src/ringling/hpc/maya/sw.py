"""
Node Prep/Release script entry points for jobs ran with `Render.exe -r sw ...`
"""
import os
from shutil import copyfile
from subprocess import call
from ringling.hpc import env
from ringling.hpc.scripts import LOG
ENV = env()

def _setup_node_project():
    LOG.info("Setting up node project directory: %s" % ENV['NODE_PROJECT'])
    if not os.path.isdir(ENV['NODE_PROJECT']):
        os.makedirs(ENV['NODE_PROJECT'])
    src = os.path.join(ENV['PROJECT'],'workspace.mel')
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
    with open(dst,'wb') as fh:
        fh.write("""
dirmap -m "S:/" "//desmond/spool/";
dirmap -m "{node_project}" "{project}";
dirmap -m "{project_name}//" "{project}/";
dirmap -en on;
""".format(project_name=os.path.basename(ENV['PROJECT'])[-1],node_project=ENV['NODE_PROJECT'].replace('\\', '/'), 
           project=ENV['PROJECT'].replace('\\', '/')))
    with open(dst) as fh:
        LOG.debug(fh.read())


def prep():
    _setup_node_project()
    _setup_dirmaps()


def release():
    _cleanup_node_project()
