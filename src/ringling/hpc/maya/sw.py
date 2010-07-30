"""
Node Prep/Release script entry points for jobs ran with `Render.exe -r sw ...`
"""
import os
from shutil import copyfile
from ringling.hpc import env
from ringling import get_log

ENV = env()
LOG = get_log(__name__, True)
def _setup_node_project():
    if not os.path.isdir(ENV['NODE_PROJECT']):
        os.makedirs(ENV['NODE_PROJECT'])
    src = os.path.join(ENV['PROJECT'],'workspace.mel')
    dst = os.path.join(ENV['NODE_PROJECT'],'workspace.mel')
    copyfile(src,dst)
    LOG.debug("File copied: %s -> %s" % (src,dst))
    LOG.debug("node local workspace:")
    LOG.debug(open(dst).read())
def _setup_dirmaps():
    dst = os.path.join(ENV['NODE_PROJECT'],'scripts','userSetup.mel')
    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    with open(dst,'wb') as fh:
        fh.write("""
dirmap -m "S:/" "//desmond/spool/";
dirmap -m "{node_project}" "{project}";
dirmap -en on;
""".format(node_project=ENV['NODE_PROJECT'].replace('\\', '/'), 
           project=ENV['PROJECT'].replace('\\', '/')))

def prep():
    _setup_node_project()
    _setup_dirmaps()
def release():pass