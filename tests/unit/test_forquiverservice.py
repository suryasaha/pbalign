"""Test pbalign.forquiverservice.forquiver."""
import unittest
from os import path, remove
from shutil import copyfile
from pbalign.forquiverservice.forquiver import ForQuiverService
from pbalign.pbalignfiles import PBAlignFiles
from tempfile import mkstemp

class Opt(object):
    """Simulate PBAlign options."""
    def __init__(self):
        """Option class."""
        self.verbosity = 2
        self.metrics = "DeletionQV, InsertionQV"
        self.byread = None


class Test_ForQuiverService(unittest.TestCase):
    """Test pbalign.forquiverservice.forquiver."""
    def setUp(self):
        self.rootDir = "/mnt/secondary-siv/" + \
                       "testdata/BlasrTestData/pbalign"
        self.inCmpFile = path.join(self.rootDir, "data/testforquiver.cmp.h5")
        #self.outCmpFile = path.join(self.rootDir, "out/testforquiver.cmp.h5")
        self.outCmpFile = mkstemp(suffix=".cmp.h5")[1]

        copyfile(self.inCmpFile, self.outCmpFile)
        self.basFile = path.join(self.rootDir, "data/lambda_bax.fofn")

        refpath = "/mnt/secondary/Smrtanalysis/opt/" + \
                  "smrtanalysis/common/references/lambda/"

        self.fileNames = PBAlignFiles()
        self.fileNames.SetInOutFiles(self.basFile, refpath,
                                     self.outCmpFile, None, None)
        self.options = Opt()
        self.obj = ForQuiverService(self.fileNames, self.options)

    def tearDown(self):
        remove(self.outCmpFile)

    def test_run(self):
        """Test ForQuiverService.__init__()."""
        self.obj.run()

if __name__ == "__main__":
    unittest.main()
