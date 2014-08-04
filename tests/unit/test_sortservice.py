"""Test pbalign.forquiverservice.sort."""
import unittest
from os import path, remove
from shutil import copyfile
from pbalign.forquiverservice.sort import SortService
from tempfile import mkstemp


class Opt(object):
    """Simulate pbalign options."""
    def __init__(self):
        """Option class."""
        self.verbosity = 2

class Test_SortService(unittest.TestCase):
    """Test pbalign.forquiverservice.sort."""
    def setUp(self):
        """Set up tests."""
        self.rootDir = "/mnt/secondary-siv/" + \
                       "testdata/BlasrTestData/pbalign"
        self.inCmpFile = path.join(self.rootDir, "data/testsort.cmp.h5")
        self.outCmpFile = mkstemp(suffix=".cmp.h5")[1]

        copyfile(self.inCmpFile, self.outCmpFile)
        self.options = Opt()
        self.obj = SortService(self.outCmpFile, self.options)

    def tearDown(self):
        remove(self.outCmpFile)

    def test_run(self):
        """Test SortService.__init__()."""
        print self.obj.cmd
        _output, errCode, _errMsg = self.obj.run()
        self.assertEqual(errCode, 0)

if __name__ == "__main__":
    unittest.main()
