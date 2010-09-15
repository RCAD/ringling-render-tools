import os
import rrt
LOG = rrt.get_log()
LOG.info("Starting %s" % rrt.get_version())

from rrt.hpc import env
ENV = env()

from maya import cmds

posix = lambda s: s.replace('\\', '/')

proj = posix(ENV['PROJECT'])
node_proj = posix(ENV['NODE_PROJECT'])

map_pairs = [
    (node_proj, proj),
]

for name in os.listdir(ENV['PROJECT']):
    full = os.path.join(ENV['PROJECT'], name)
    if os.path.isdir(full):
        map_pairs.append(('//'+name, posix(full)))
        map_pairs.append((node_proj+'//'+name, posix(full)))

LOG.debug("Dirmaps:")
for m in map_pairs:
    LOG.debug(m)
    cmds.dirmap(mapDirectory=m)
cmds.dirmap(enable=True)
