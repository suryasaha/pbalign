import unittest
import filecmp
from os import path
from pbalign.pbalignfiles import PBAlignFiles

class Test_PbAlignFiles_Ecoli(unittest.TestCase):
    def setUp(self):
        self.rootDir = path.dirname(path.dirname(path.abspath(__file__)))
        self.inputFileName    = path.join(self.rootDir, "data/ecoli.fasta")
        self.referencePath    = "/mnt/secondary/Smrtanalysis/opt/" + \
                                "smrtanalysis/common/references/ecoli_K12_MG1655/"
        self.targetFileName   = path.join(self.referencePath,
                                          "sequence/ecoli_K12_MG1655.fasta")
        self.sawriterFileName = self.targetFileName + ".sa"
        self.outputFileName   = path.join(self.rootDir, "out/tmp.sam")

    def test_init(self):
        """Test PBAlignFiles.__init__() with a reference repository."""
        # Without region table
        p = PBAlignFiles(self.inputFileName,
                         self.referencePath,
                         self.outputFileName)
        self.assertTrue(filecmp.cmp(p.inputFileName, self.inputFileName))
        self.assertTrue(p.referencePath, path.abspath(path.expanduser(self.referencePath)))
        self.assertTrue(filecmp.cmp(p.targetFileName, self.targetFileName))
        self.assertTrue(filecmp.cmp(p.outputFileName, self.outputFileName))
        self.assertIsNone(p.regionTable)



class Test_PbAlignFiles(unittest.TestCase):
    def setUp(self):
        self.rootDir = path.dirname(path.dirname(path.abspath(__file__)))
        self.inputFileName = path.join(self.rootDir, "data/lambda_bax.fofn")
        self.referenceFile = "/mnt/secondary/Smrtanalysis/opt/" + \
                             "smrtanalysis/common/references/" + \
                             "lambda/sequence/lambda.fasta"
        self.outputFileName = path.join(self.rootDir, "out/tmp.sam")

    def test_init(self):
        """Test PBAlignFiles.__init__()."""
        # Without region table
        p = PBAlignFiles(self.inputFileName,
                         self.referenceFile,
                         self.outputFileName)
        self.assertTrue(filecmp.cmp(p.inputFileName, self.inputFileName))
        self.assertTrue(filecmp.cmp(p.referencePath, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.targetFileName, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.outputFileName, self.outputFileName))
        self.assertIsNone(p.regionTable)

    def test_init_region_table(self):
        """Test PBAlignFiles.__init__() with a region table."""
        # With an artifical region table
        regionTable = path.join(self.rootDir, "data/lambda.rgn.h5")
        p = PBAlignFiles(self.inputFileName,
                         self.referenceFile,
                         self.outputFileName,
                         regionTable)
        self.assertTrue(filecmp.cmp(p.regionTable, regionTable))


    def test_setInOutFiles(self):
        """Test PBAlignFiles.SetInOutFiles()."""
        p = PBAlignFiles()
        self.assertIsNone(p.inputFileName)
        self.assertIsNone(p.outputFileName)
        self.assertIsNone(p.referencePath)

        p.SetInOutFiles(self.inputFileName,
                        self.referenceFile,
                        self.outputFileName,
                        None)
        self.assertTrue(filecmp.cmp(p.inputFileName, self.inputFileName))
        self.assertTrue(filecmp.cmp(p.referencePath, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.targetFileName, self.referenceFile))
        self.assertTrue(filecmp.cmp(p.outputFileName, self.outputFileName))
        self.assertIsNone(p.regionTable)


if __name__ == "__main__":
    unittest.main()

