"""Test pbalign.forquiverservice.repack."""
import unittest
from os import path, remove
from shutil import copyfile
from pbalign.forquiverservice.repack import RepackService
from tempfile import mkstemp


class Test_RepackService(unittest.TestCase):
    """Test pbalign.forquiverservice.repack."""
    def setUp(self):
        """Set up the tests."""
        self.rootDir = "/mnt/secondary-siv/" + \
                       "testdata/BlasrTestData/pbalign"
        self.inCmpFile = path.join(self.rootDir, "data/testrepack.cmp.h5")
        #self.outCmpFile = path.join(self.rootDir, "out/testrepack.cmp.h5")
        self.outCmpFile = mkstemp(suffix=".cmp.h5")[1]
        self.tmpCmpFile = self.outCmpFile + ".tmp"

        #self.tmpCmpFile = path.join(self.rootDir, "out/testrepack.cmp.h5.tmp")
        copyfile(self.inCmpFile, self.outCmpFile)
        self.options = {}
        self.obj = RepackService(self.outCmpFile, self.tmpCmpFile)

    def tearDown(self):
        remove(self.outCmpFile)

    def test_run(self):
        """Test LoadPulsesService.__init__()."""
        print self.obj.cmd
        _output, errCode, _errMsg = self.obj.run()
        self.assertEqual(errCode, 0)

if __name__ == "__main__":
    unittest.main()
