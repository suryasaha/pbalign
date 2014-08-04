"""Test pbalign.filterservice."""
from pbalign.filterservice import FilterService
from os import path
import unittest

class Opt(object):
    """The Option class."""
    def __init__(self, maxDivergence, minAccuracy, minLength,
                       seed, scoreCutoff, hitPolicy):
        self.maxDivergence = maxDivergence
        self.minAccuracy   = minAccuracy
        self.minLength     = minLength
        self.seed          = seed
        self.scoreCutoff   = scoreCutoff
        self.hitPolicy     = hitPolicy
        self.filterAdapterOnly = None

class Test_FilterService(unittest.TestCase):
    """Test pbalign.filterservice."""
    def setUp(self):
        self.testDir = path.dirname(path.dirname(path.abspath(__file__)))
        self.alignedSam    = path.join(self.testDir,
                                       "data/lambda.sam")
        self.targetFileName = "/mnt/secondary/Smrtanalysis/opt/" + \
                               "smrtanalysis/common/references/" + \
                               "lambda/sequence/lambda.fasta"
        self.filteredSam   = path.join(self.testDir,
                                       "out/lambda_filtered.sam")

    def test_init(self):
        """Test FilterService.__init__()."""
        options = Opt(30, 70, 50, 1, None, "random")

        obj = FilterService(self.alignedSam, self.targetFileName,
                            self.filteredSam, "BlasrService", -1,
                            options)

        self.assertTrue(obj.availability) # samFilter should be available
        self.assertIn("-minPctSimilarity 70", obj.cmd)
        self.assertIn("-minAccuracy 70", obj.cmd)
        self.assertIn("-scoreSign -1", obj.cmd)

    def test_run(self):
        """Test FilterService.run()."""
        options = Opt(30, 70, 50, 1, None, "random")

        obj = FilterService(self.alignedSam, self.targetFileName,
                            self.filteredSam, "BlasrService", -1,
                            options)

        _output, errCode, _errMsg = obj.run()

        self.assertEqual(errCode, 0)


    def test_run_without_scoreCutoff(self):
        """Test FilterService.run() without score cutoff."""
        options2 = Opt(40, 50, None, None, None, "allbest")
        obj2 = FilterService(self.alignedSam, self.targetFileName,
                             self.filteredSam, "BowtieService", 1,
                             options2)

        self.assertNotIn("-seed", obj2.cmd)
        self.assertNotIn("-scoreCutoff", obj2.cmd)
        self.assertIn("-scoreSign 1", obj2.cmd)

        _output, errCode, _errMsg = obj2.run()

        self.assertEqual(errCode, 0)

if __name__ == "__main__":
    unittest.main()
