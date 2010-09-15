import ntpath
from subprocess import Popen, PIPE
def get_share(path):
    """
    Maps windows drive letters to unc paths.
    """
    drive_letter = ntpath.splitdrive(path)[0]
    try:
        p = Popen(' '.join(['net', 'use', drive_letter]), stdout=PIPE, 
                  stderr=PIPE, shell=True)
        out = p.communicate()[0]
        if p.returncode != 0:
            raise RuntimeError("Can't find network share for drive %s" % drive_letter)
        unc = out.splitlines()[1].split()[2].strip()
        return unc
    except Exception, e:
        raise e 