"""
These functions serve as script entry points.
They identify the job style based on the environment, then pass the request off
to application specific implementations.
"""

import os, sys
from ringling import RinglingException, get_log
from ringling.hpc import env
LOG = get_log(__name__, stream=True)

class MissingDelegateError(RinglingException):pass

class Delegator(object):
    __delegates__ = {
                     'maya_render_sw': 'ringling.hpc.maya.sw',
                     'maya_render_rman': 'ringling.hpc.maya.rman', 
                     'max': 'ringling.hpc.max'
                     }
    _delegate = None
    
    def __init__(self):
        LOG.debug("Params: %r" % env())
        jobtype = os.getenv('RENDERER', None)
        if jobtype not in self.__delegates__:
            raise MissingDelegateError
        self._delegate = self.__delegates__[jobtype]
        LOG.debug("Got delegate: %s" % self._delegate)
        __import__(self._delegate, globals(), locals())
        LOG.info("Running node prep for %s job #%s" % (jobtype, env()['JOBID']))
        
    def prep(self):
        """ Delegate access to implementation """
        return sys.modules[self._delegate].prep()

    def release(self):
        """ Delegate access to implementation """
        return sys.modules[self._delegate].release()


def prep_delegator():
    return Delegator().prep()

def release_delegator():
    return Delegator().release()