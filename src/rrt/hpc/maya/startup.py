import os
import rrt
LOG = rrt.get_log()
LOG.info("Starting %s" % rrt.get_version())

from rrt.maya.helpers import ProjectPath
from rrt.settings import SPOOL_UNC
from rrt.hpc import env
ENV = env()

from maya import cmds

proj = ProjectPath(ENV['PROJECT'])
root = ProjectPath(SPOOL_UNC)

map_pairs = [
    (proj.ppath, proj.punc),
    (proj.ppath+'//', proj.punc+'/'), 
    (root.ppath, root.punc),
    (ENV['NODE_PROJECT'].replace('\\','/'), proj.punc)
]
for name in os.listdir(proj.punc):
    full = ProjectPath(proj.punc, name)
    if os.path.isdir(full.punc):
        map_pairs.append(('//'+name, full.punc))
        map_pairs.append((ENV['NODE_PROJECT'].replace('\\','/')+'//'+name, full.punc))
LOG.debug("Dirmaps:")
for m in map_pairs:
    LOG.debug(m)
    cmds.dirmap(mapDirectory=m)
cmds.dirmap(enable=True)
