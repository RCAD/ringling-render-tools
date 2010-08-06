import os, re
from ringling import SPOOL_UNC, SPOOL_LETTER, RinglingException

class InvalidPathError(RinglingException):pass

def _to_posix(path): return path.replace("\\","/")
def _to_nt(path): return path.replace("/", "\\")
def _raw(s): return r"%s"%s

class Path(object):
    # regex patterns (case insensitive since we're on windows)
    letter_re = re.compile('^%s' % re.escape(_to_posix(SPOOL_LETTER)), re.IGNORECASE)
    unc_re = re.compile('^%s' % re.escape(_to_posix(SPOOL_UNC)), re.IGNORECASE)
    
    _source = None
    _clean = None
    def __init__(self,path):
        self._source =  path.strip()
        self._clean = _to_posix(os.path.abspath(self._source))
        if not (self.letter_re.match(self._clean) or
                self.unc_re.match(self._clean)):
            raise InvalidPathError, path 
    @property
    def raw(self):
        return self._source
    @property
    def _path(self):
        return re.sub(self.unc_re, SPOOL_LETTER, self._clean)
    @property
    def _unc(self):
        return re.sub(self.letter_re, SPOOL_UNC, self._clean)
    @property
    def path(self):
        return _to_nt(_raw(self._path))
    @property
    def unc(self):
        return _to_nt(_raw(self._unc))
    @property
    def ppath(self): 
        return _to_posix(self.path)
    @property
    def punc(self): 
        return _to_posix(self.unc)
    @property
    def name(self): return os.path.splitext(os.path.split(self.path)[-1])[0]