import os
from ringling import SPOOL_UNC, SPOOL_LETTER, RinglingException

class InvalidPathError(RinglingException):pass

def _to_posix(path): return path.replace("\\","/")
def _to_nt(path): return path.replace("/", "\\")

class Path(object):
    _source = None
    _clean = None
    def __init__(self,path):
        self._source = path.strip().lower()
        self._clean = _to_nt(os.path.abspath(self._source))
        if not (self._clean.startswith(SPOOL_UNC.lower()) or
                self._clean.startswith(SPOOL_LETTER.lower())):
            raise InvalidPathError, path 
    @property
    def raw(self):
        return self._source
    @property
    def _path(self):
        if self._clean.startswith(SPOOL_LETTER.lower()):
            return self._clean
        return self._clean.replace(SPOOL_UNC.lower(), SPOOL_LETTER.lower())
    @property
    def _unc(self):
        if self._clean.startswith(SPOOL_UNC.lower()):
            return self._clean
        return self._clean.replace(SPOOL_LETTER.lower(), SPOOL_UNC.lower())
    @property
    def path(self):
        return _to_nt(self._path)
    @property
    def unc(self):
        return _to_nt(self._unc)
    @property
    def ppath(self): 
        return _to_posix(self.path)
    @property
    def punc(self): 
        return _to_posix(self.unc)
    @property
    def name(self): return os.path.splitext(os.path.split(self.path)[-1])[0]