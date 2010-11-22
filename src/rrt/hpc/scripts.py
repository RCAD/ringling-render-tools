"""
These functions serve as script entry points.
They identify the job style based on the environment, then pass the request off
to application specific implementations.
"""
import os, sys, shutil, platform, datetime, rrt
from subprocess import call
from pkg_resources import Requirement, resource_filename #@UnresolvedImport

from rrt import RinglingException, get_log
from rrt.hpc import env
LOG = get_log(platform.uname()[1], True)

class MissingDelegateError(RinglingException):pass

class Delegator(object):
    _env = env()
    __delegates__ = {
                     'maya_render_sw': 'rrt.hpc.maya.sw',
                     'maya_render_rman': 'rrt.hpc.maya.rman',
                     'max': 'rrt.hpc.max'
                     }
    _delegate = None

    def __init__(self):
        LOG.info("Starting " + rrt.get_version())
        LOG.debug("Params: %r" % env())
        jobtype = os.getenv('RENDERER', None)
        if jobtype not in self.__delegates__:
            raise MissingDelegateError
        self._delegate = self.__delegates__[jobtype]
        LOG.debug("Got delegate: %s" % self._delegate)
        __import__(self._delegate, globals(), locals())

    def prep(self):
        # Generic Prep
        try:
            os.makedirs(self._env['NODE_PROJECT'])
            LOG.info("Setting up node project directory: %s" % self._env['NODE_PROJECT'])
        except Exception, e:
            LOG.debug(e)

        log_dir = os.path.dirname(self._env['LOGS'])
        output_dir = os.path.dirname(self._env['OUTPUT'])

        for d in (log_dir, output_dir):
            try:
                os.makedirs(d)
                LOG.info("Creating directory %s" % d)
            except OSError, e:
                if e.errno == 17:
                    # errno 17 is file already exists... which is good
                    LOG.debug(e)
                else:
                    LOG.exception(e)

        # Delegate access to implementation
        return sys.modules[self._delegate].prep()

    def release(self):
        # Generic release
        LOG.info("Cleaning up node project: %s" % self._env['NODE_PROJECT'])
        LOG.info("\tCalculating size...")
        LOG.info("\tThis could take a while...")
        size = sum([os.path.getsize(os.path.join(root, f)) for root, dirs, files in os.walk(self._env['NODE_PROJECT']) for f in files])
        LOG.info("\t%0.1f MB" % (size / (1024 * 1024.0)))
        call('rmdir /S /Q %s' % self._env['NODE_PROJECT'], shell=True)

        # Delegate access to implementation
        return sys.modules[self._delegate].release()


def prep_delegator():
    start = datetime.datetime.now()
    LOG.info("Starting node prep. %s" % str(start))
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

def deploy_extras():
    DEPLOY_LOCATION = r'C:\Ringling\HPC'
    extras = resource_filename(Requirement.parse("ringling-render-tools"), "rrt/extras")
    if os.path.exists(DEPLOY_LOCATION): shutil.rmtree(DEPLOY_LOCATION)
    shutil.copytree(extras, DEPLOY_LOCATION)
    print "Done."
    sys.exit(0)
