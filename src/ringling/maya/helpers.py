import os
from ringling import SPOOL_UNC, SPOOL_LETTER, RinglingException

class InvalidPathError(RinglingException):pass

def _to_posix(path): return path.replace("\\", "/")
def _to_nt(path): return path.replace("/", "\\")

class Path(object):
    _source = None

    def __init__(self, *path):
        
        self._source = os.path.normpath(os.path.abspath(os.path.join(*path)))
        
        path_parts = os.path.splitdrive(self._source)
        if not path_parts[0]:
            path_parts = os.path.splitunc(self._source)
        if path_parts[0].lower() not in [SPOOL_UNC.lower(), SPOOL_LETTER.lower()]:
            raise InvalidPathError, path_parts
        self._tail = path_parts[1] 

    @property
    def raw(self):
        return self._source
    @property
    def _path(self):
        return SPOOL_LETTER+self._tail
    @property
    def _unc(self):
        return SPOOL_UNC+self._tail
    @property
    def path(self):
        return self._path
    @property
    def unc(self):
        return self._unc
    @property
    def ppath(self): 
        return _to_posix(self._path)
    @property
    def punc(self): 
        return _to_posix(self._unc)
    @property
    def name(self): return os.path.splitext(os.path.split(self.path)[-1])[0]
