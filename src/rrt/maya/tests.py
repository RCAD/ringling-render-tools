import unittest, os
from rrt.maya.helpers import Path, InvalidPathError
from rrt import SPOOL_LETTER, SPOOL_UNC
class TestPathHelper(unittest.TestCase):

    def setUp(self):pass

    def test_nt_unc_arg(self):
        src = SPOOL_UNC+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = Path(src)
        self.assertEqual(src, path.unc)
        self.assertEqual(psrc, path.punc)
    
    def test_nt_letter_arg(self):
        src = SPOOL_LETTER+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = Path(src)
        self.assertEqual(src, path.path)
        self.assertEqual(psrc, path.ppath)
        
    def test_posix_unc_arg(self):
        src = SPOOL_UNC+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = Path(psrc)
        self.assertEqual(src, path.unc)
        self.assertEqual(psrc, path.punc)
        self.assertEqual(src, path.unc)
        self.assertEqual(psrc, path.punc)
    
    def test_posix_letter_arg(self):
        src = SPOOL_LETTER+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = Path(psrc)
        self.assertEqual(src, path.path)
        self.assertEqual(psrc, path.ppath)
        self.assertEqual(src, path.path)
        self.assertEqual(psrc, path.ppath)
        
    def test_invalid_path(self):
        self.assertRaises(InvalidPathError, Path, r"D:\my\path")
        self.assertRaises(InvalidPathError, Path, "D:/my/path")
        self.assertRaises(InvalidPathError, Path, r"Z:\my\path")
        self.assertRaises(InvalidPathError, Path, "Z:/my/path")
    
    def test_nt_letter_unc_substitution(self):
        tail = "maya\\foo\\scenes\\bar.mb"
        self.assertEquals(Path(SPOOL_LETTER, tail).path, 
                          Path(SPOOL_UNC, tail).path)
        self.assertEquals(Path(SPOOL_LETTER, tail).unc, 
                          Path(SPOOL_UNC, tail).unc)
        self.assertEquals(Path(SPOOL_LETTER, tail).ppath, 
                          Path(SPOOL_UNC, tail).ppath)
        self.assertEquals(Path(SPOOL_LETTER, tail).punc, 
                          Path(SPOOL_UNC, tail).punc)
    
    def test_posix_letter_unc_substitution(self):
        unc_src = SPOOL_UNC+"\\maya\\foo\\scenes\\bar.mb"
        unc_psrc = unc_src.replace('\\','/')
        letter_src = SPOOL_LETTER+"\\maya\\foo\\scenes\\bar.mb"
        letter_psrc = letter_src.replace('\\','/')
        letter_path = Path(letter_psrc)
        unc_path = Path(unc_psrc)
        self.assertEquals(unc_path.path, letter_path.path)
        self.assertEquals(unc_path.unc, letter_path.unc)
        self.assertEquals(unc_src, letter_path.unc)
        self.assertEquals(letter_src, unc_path.path)
        self.assertEquals(letter_psrc, unc_path.ppath)
        self.assertEquals(unc_psrc, letter_path.punc)

if __name__ == '__main__':
    unittest.main()
