import unittest
from rrt.maya.helpers import ProjectPath, InvalidPathError
from rrt import SPOOL_LETTER, SPOOL_UNC

class TestPathHelper(unittest.TestCase):

    def test_nt_unc_arg(self):
        src = SPOOL_UNC+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = ProjectPath(src)
        self.assertEqual(src, path.unc)
        self.assertEqual(psrc, path.punc)
    
    def test_nt_letter_arg(self):
        src = SPOOL_LETTER+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = ProjectPath(src)
        self.assertEqual(src, path.path)
        self.assertEqual(psrc, path.ppath)
        
    def test_posix_unc_arg(self):
        src = SPOOL_UNC+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = ProjectPath(psrc)
        self.assertEqual(src, path.unc)
        self.assertEqual(psrc, path.punc)
        self.assertEqual(src, path.unc)
        self.assertEqual(psrc, path.punc)
    
    def test_posix_letter_arg(self):
        src = SPOOL_LETTER+"\\maya\\foo\\scenes\\bar.mb"
        psrc = src.replace('\\','/')
        path = ProjectPath(psrc)
        self.assertEqual(src, path.path)
        self.assertEqual(psrc, path.ppath)
        self.assertEqual(src, path.path)
        self.assertEqual(psrc, path.ppath)
        
    def test_invalid_path(self):
        self.assertRaises(InvalidPathError, ProjectPath, r"D:\my\path")
        self.assertRaises(InvalidPathError, ProjectPath, "D:/my/path")
#        self.assertRaises(InvalidPathError, ProjectPath, r"Z:\my\path")
#        self.assertRaises(InvalidPathError, ProjectPath, "Z:/my/path")
    
    def test_nt_letter_unc_substitution(self):
        tail = "\\maya\\foo\\scenes\\bar.mb"
        self.assertEquals(ProjectPath(SPOOL_LETTER, tail).path, 
                          ProjectPath(SPOOL_UNC, tail).path)
        self.assertEquals(ProjectPath(SPOOL_LETTER, tail).unc, 
                          ProjectPath(SPOOL_UNC, tail).unc)
        self.assertEquals(ProjectPath(SPOOL_LETTER, tail).ppath, 
                          ProjectPath(SPOOL_UNC, tail).ppath)
        self.assertEquals(ProjectPath(SPOOL_LETTER, tail).punc, 
                          ProjectPath(SPOOL_UNC, tail).punc)
    
    def test_posix_letter_unc_substitution(self):
        unc_src = SPOOL_UNC+"\\maya\\foo\\scenes\\bar.mb"
        unc_psrc = unc_src.replace('\\','/')
        letter_src = SPOOL_LETTER+"\\maya\\foo\\scenes\\bar.mb"
        letter_psrc = letter_src.replace('\\','/')
        letter_path = ProjectPath(letter_psrc)
        unc_path = ProjectPath(unc_psrc)
        self.assertEquals(unc_path.path, letter_path.path)
        self.assertEquals(unc_path.unc, letter_path.unc)
        self.assertEquals(unc_src, letter_path.unc)
        self.assertEquals(letter_src, unc_path.path)
        self.assertEquals(letter_psrc, unc_path.ppath)
        self.assertEquals(unc_psrc, letter_path.punc)

if __name__ == '__main__':
    unittest.main()
