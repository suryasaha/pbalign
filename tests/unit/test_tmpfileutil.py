from pbalign.utils.tempfileutil import TempFileManager
import unittest
from os import path

def keep_writing_to_file(fn):
    """Keep writing a to a file."""
    f = open(fn, 'w')
    while True:
        # Keep writing a to a file,
        # note that this function will never end unless
        # being killed by the main process.
       f.write('a')

class Test_TempFileManager(unittest.TestCase):

    def test_init(self):
        """Test TempFileManager all functions."""
        t = TempFileManager()
        t.SetRootDir("/scratch")

        newFN = t.RegisterNewTmpFile()
        self.assertTrue(path.isfile(newFN))

        existingDir = t.RegisterExistingTmpFile("/tmp", isDir=True)
        self.assertTrue(path.isdir(existingDir))

        with self.assertRaises(IOError) as cm:
            t.RegisterExistingTmpFile("filethatdoesnotexist")

        newDN = t.RegisterNewTmpFile(isDir=True)
        self.assertTrue(path.isdir(newDN))
        self.assertTrue(t._isRegistered(newDN))

        newTxt = t.RegisterNewTmpFile(suffix=".txt")
        self.assertTrue(newTxt.endswith(".txt"))

        t.SetRootDir("~/tmp/")

        t.CleanUp()
        self.assertFalse(path.exists(newFN))
        self.assertFalse(path.exists(newDN))
        self.assertEqual(t.fileDB, [])
        self.assertEqual(t.dirDB, [])

#    def test_CleanUp(self):
#        """Create a temp directory and register several tmp files.
#        Then, manually open another file under temp dir without
#        registering it. Finally, call CleanUp to delete temp dirs
#        and files. Note that by doing this, an nfs lock is created
#        manually, CleanUp should exit with a warning instead of an
#        error."""
#        t = TempFileManager()
#        t.SetRootDir("/scratch")
#        newFN = t.RegisterNewTmpFile()
#        with open(newFN, 'w') as writer:
#            writer.write("x")
#
#        newFN2 = t.RegisterNewTmpFile()
#        with open(newFN2, 'w') as writer:
#            writer.write("x")
#
#        # Manually create a temp file under temp dir without register
#        rootDir = t.defaultRootDir
#        extraFN = path.join(t.defaultRootDir, 'extra_file.txt')
#        # Keep the file open while trying to Clean up temp dir.
#        from multiprocessing import Process
#        p = Process(target=keep_writing_to_file, args=(extraFN, ))
#        p.start()
#        self.assertTrue(p.is_alive())
#
#        t.CleanUp()
#
#        self.assertFalse(path.exists(newFN))
#        self.assertFalse(path.exists(newFN2))
#
#        self.assertTrue(p.is_alive())
#        self.assertTrue(path.exists(extraFN))
#        self.assertEqual(t.fileDB, [])
#        self.assertEqual(t.dirDB, [])
#
#        p.terminate()
#
#        import time
#        time.sleep(1)
#        import shutil
#        shutil.rmtree(rootDir)
#

if __name__ == "__main__":
    unittest.main()

