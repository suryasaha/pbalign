import unittest
from os import path
from pbalign.pbalignrunner import PBAlignRunner

class Test_PBAlignRunner(unittest.TestCase):
    def setUp(self):
        self.rootDir = path.dirname(path.dirname(path.abspath(__file__)))
        self.queryFile = path.join(self.rootDir, "data/lambda_query.fasta")
        self.referenceFile = "/mnt/secondary/Smrtanalysis/opt/" + \
                             "smrtanalysis/common/references/" + \
                             "lambda/sequence/lambda.fasta"
        self.configFile = path.join(self.rootDir, "data/1.config")
        self.samOut = path.join(self.rootDir, "out/lambda_out.sam")
        self.cmph5Out = path.join(self.rootDir, "out/lambda_out.cmp.h5")

    def test_init(self):
        """Test PBAlignRunner.__init__()."""
        argumentList = ['--minAccuracy', '70', '--maxDivergence', '30',
                        self.queryFile, self.referenceFile,
                        self.samOut]
        pbobj = PBAlignRunner(argumentList = argumentList)
        self.assertEqual(pbobj.start(), 0)

    def test_init_with_algorithmOptions(self):
        """Test PBAlignRunner.__init__() with --algorithmOptions."""
        argumentList = ['--algorithmOptions', '-minMatch 10 -useccsall',
                        self.queryFile, self.referenceFile,
                        self.cmph5Out]
        pbobj = PBAlignRunner(argumentList = argumentList)
        self.assertEqual(pbobj.start(), 0)

    def test_init_with_config_algorithmOptions(self):
        """Test PBAlignRunner.__init__() with a config file and --algorithmOptions."""
        argumentList = ['--algorithmOptions', '-maxMatch 20 -nCandidates 30',
                        '--configFile', self.configFile,
                        self.queryFile, self.referenceFile,
                        self.cmph5Out]

        pbobj = PBAlignRunner(argumentList = argumentList)
        self.assertEqual(pbobj.start(), 0)

    def test_init_expect_conflicting_options(self):
        """Test PBAlignRunner.__init__() with a config file and --algorithmOptions
        and expect a ValueError for conflicting options."""
        argumentList = ['--algorithmOptions', '-minMatch 10 -useccsall',
                        '--configFile', self.configFile,
                        self.queryFile, self.referenceFile,
                        self.cmph5Out]
        pbobj = PBAlignRunner(argumentList = argumentList)
        with self.assertRaises(ValueError) as cm:
            # Expect a ValueError since -minMatch and --minAnchorSize conflicts.
            pbobj.start()


if __name__ == "__main__":
    unittest.main()
