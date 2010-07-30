"""
These functions serve as script entry points.
They identify the job style based on the environment, then pass the request off
to application specific implementations.
"""

import os, sys, platform, datetime
from ringling import RinglingException, get_log
from ringling.hpc import env
LOG = get_log(platform.uname()[1], True)

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
        
    def prep(self):
        """ Delegate access to implementation """
        return sys.modules[self._delegate].prep()

    def release(self):
        """ Delegate access to implementation """
        return sys.modules[self._delegate].release()


def prep_delegator():
    start = datetime.datetime.now()
    LOG.info("Starting node prep. %s" % str(start))
    LOG.info(str(start))
    Delegator().prep()
    end = datetime.datetime.now()
    LOG.info("Elapsed time: %s" % str(end - start))
    LOG.info("Done.")
    sys.exit(0)

def release_delegator():
    start = datetime.datetime.now()
    LOG.info("Starting node release. %s" % str(start))
    Delegator().release()
    end = datetime.datetime.now()
    LOG.info("Elapsed time: %s" % str(end - start))
    LOG.info("Done.")
    sys.exit(0)