"""Test pbalign.forquiverservice.loadpulses."""
import unittest
from os import path, remove
from shutil import copyfile
from pbalign.forquiverservice.loadpulses import LoadPulsesService
from argparse import Namespace
from tempfile import mkstemp


class Test_LoadPulsesService(unittest.TestCase):
    """Test pbalign.forquiverservice.loadpulses."""
    def setUp(self):
        """Set up tests."""
        self.rootDir = "/mnt/secondary-siv/" + \
                       "testdata/BlasrTestData/pbalign"
        self.inCmpFile = path.join(self.rootDir, "data/testloadpulses.cmp.h5")
        #self.outCmpFile = path.join(self.rootDir, "out/testloadpulses.cmp.h5")
        self.outCmpFile = mkstemp(suffix=".cmp.h5")[1]

        self.basFile = path.join(self.rootDir, "data/lambda_bax.fofn")
        copyfile(self.inCmpFile, self.outCmpFile)
        self.options = Namespace(metrics="DeletionQV", byread=False)
        self.obj = LoadPulsesService(self.basFile,
                self.outCmpFile, self.options)

    def tearDown(self):
        remove(self.outCmpFile)

    def test_run(self):
        """Test LoadPulsesService.__init__()."""
        _output, errCode, _errMsg = self.obj.run()
        self.assertEqual(errCode, 0)

if __name__ == "__main__":
    unittest.main()
