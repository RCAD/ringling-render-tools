import logging, os
from subprocess import Popen, PIPE
from pkg_resources import Requirement, resource_filename, DistributionNotFound
try:
    __VERSION_FILE__ = resource_filename(Requirement.parse("ringling-render-tools"),"rrt/RELEASE-VERSION")
except (KeyError, DistributionNotFound):
    __VERSION_FILE__ = os.path.join(os.path.dirname(__file__),"RELEASE-VERSION")
    
__LOG_LEVEL__ = logging.DEBUG if os.getenv('RRT_DEBUG',False) else logging.INFO

def get_log(name=__name__, stream=False):
    log = logging.getLogger(name)
    log.setLevel(__LOG_LEVEL__)
    if stream:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(name)s %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
    return log

def __call_git_describe(abbrev=4):
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()
    except:
        return None

def __read_release_version():
    try:
        f = open(__VERSION_FILE__, "r")
        try:
            version = f.readlines()[0]
            return version.strip()
        finally:
            f.close()
    except:
        return None


def __write_release_version(version):
    f = open(__VERSION_FILE__, "w")
    f.write("%s\n" % version)
    f.close()


def get_git_version(abbrev=4):
    # Read in the version that's currently in RELEASE-VERSION.
    release_version = __read_release_version()
    # First try to get the current version using git describe.
    version = __call_git_describe(abbrev)
    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.
    if version is None:
        version = release_version
    # If we still don't have anything, that's an error.
    if version is None:
        raise ValueError("Cannot find the version number!")
    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if version != release_version:
        __write_release_version(version)
    # Finally, return the current version.
    return version


__POST_RELEASE_TAG__ = None
__version__ = get_git_version()
if __POST_RELEASE_TAG__: __version__ = '-'.join([__version__,__POST_RELEASE_TAG__])


def get_version():
    version_string = 'Ringling Render Tools '+__version__
    return version_string

class RinglingException(Exception):pass

# Blessed  file system locations
SPOOL_LETTER = "S:"
SPOOL_UNC = "\\\\chome\\chome"
JOB_LOGS_UNC = "\\\\clogs\\clogs"
JOB_OUTPUT_UNC = "\\\\coutput\\coutput"

if os.getenv('RRT_USE_DESMOND', False):
    SPOOL_UNC = "\\\\desmond\\spool" # note the native \ style separators
    JOB_LOGS_UNC = "\\\\desmond\\spool\\logs"
    JOB_OUTPUT_UNC = "\\\\desmond\\spool\\output"
