from pbalign.options import *
from argparse import *
from os import path
import filecmp
import unittest

rootDir = path.dirname(path.dirname(path.abspath(__file__)))
configFile = path.join(rootDir, "data/2.config")
configFile3 = path.join(rootDir, "data/3.config")

def writeConfigFile(configFile, configOptions):
    """Write configs to a file."""
    with open (configFile, 'w') as f:
        f.write("\n".join(configOptions))

class Test_Options(unittest.TestCase):

    def test_importConfigOptions(self):
        """Test importConfigOptions()."""
        configOptions = ("--minAccuracy     = 40",
                         "--maxHits         = 20")
        writeConfigFile(configFile, configOptions)
        options = Namespace(configFile=configFile,
                            minAccuracy=10,
                            maxHits=12)

        newOptions, infoMsg = importConfigOptions(options)

        self.assertEqual(int(newOptions.maxHits),     20)
        self.assertEqual(int(newOptions.minAccuracy), 40)

    def test_ConstructOptionParser(self):
        """Test constructOptionParser()."""
        ret = constructOptionParser()
        self.assertEqual(type(ret), argparse.ArgumentParser)

    def test_parseOptions(self):
        """Test parseOptions()."""
        configOptions = (
            "--maxHits       = 20",
            "--minAnchorSize = 15",
            "--minLength     = 100",
            "--algorithmOptions = '-noSplitSubreads " + \
            "-maxMatch 30 -nCandidates 30'",
            "# Some comments",
            "--scoreFunction = blasr",
            "--hitPolicy     = random",
            "--maxDivergence = 40",
            "--debug")
        writeConfigFile(configFile, configOptions)

    def test_parseOptions_with_config(self):
        """Test parseOptions with a config file."""
        # With the above config file
        argumentList = ['--configFile', configFile,
                        '--maxHits', '30',
                        '--minAccuracy', '50',
                        'readfile', 'reffile', 'outfile']
        parser, options, infoMsg = parseOptions(argumentList)

        self.assertTrue(filecmp.cmp(options.configFile, configFile))
        self.assertEqual(int(options.maxHits),       30)
        self.assertEqual(int(options.minAccuracy),   50)

        self.assertEqual("".join(options.algorithmOptions),
                         "-noSplitSubreads -maxMatch 30 -nCandidates 30")
        self.assertEqual(options.scoreFunction,      "blasr")
        self.assertEqual(options.hitPolicy,          "random")
        self.assertEqual(int(options.maxDivergence), 40)

    def test_parseOptions_without_config(self):
        """Test parseOptions without any config file."""
        argumentList = ['--maxHits=30',
                        '--minAccuracy=50',
                        'readfile', 'reffile', 'outfile']
        parser, options,infoMsg = parseOptions(argumentList)

        self.assertIsNone(options.configFile)
        self.assertEqual(int(options.maxHits),       30)
        self.assertEqual(int(options.minAccuracy),   50)
        self.assertIsNone(options.algorithmOptions)
        self.assertIsNone(options.minAnchorSize)

    def test_parseOptions_multi_algorithmOptions(self):
        """Test parseOptions with multiple algorithmOptions."""
        algo1 = " -holeNumbers 1"
        algo2 = " -nCandidate 25"
        algo3 = " ' -bestn 11 '"
        argumentList = ['--algorithmOptions=%s' % algo1,
                        '--algorithmOptions=%s' % algo2,
                        'readfile', 'reffile', 'outfile']

        print argumentList
        parser, options, infoMsg = parseOptions(argumentList)
        # Both algo1 and algo2 should be in algorithmOptions.
        print options.algorithmOptions
        #self.assertTrue(algo1 in options.algorithmOptions)
        #self.assertTrue(algo2 in options.algorithmOptions)

        # Construct a config file.
        configOptions = ("--algorithmOptions = \"%s\"" % algo3)
        writeConfigFile(configFile3, [configOptions])

        argumentList.append("--configFile={0}".format(configFile3))
        print argumentList
        parser, options, infoMsg = parseOptions(argumentList)
        # Make sure algo3 have been overwritten.
        print options.algorithmOptions
        self.assertTrue(algo1 in options.algorithmOptions)
        self.assertTrue(algo2 in options.algorithmOptions)
        self.assertFalse(algo3 in options.algorithmOptions)

    def test_parseOptions_without_some_options(self):
        """Test parseOptions without specifying maxHits and minAccuracy."""
        # Test if maxHits and minAccuracy are not set,
        # whether both options.minAnchorSize and maxHits are None
        argumentList = ["--minAccuracy", "50",
                        'readfile', 'reffile', 'outfile']
        parser, options,infoMsg = parseOptions(argumentList)
        self.assertIsNone(options.minAnchorSize)
        self.assertIsNone(options.maxHits)

    def test_importDefaultOptions(self):
        """Test importDefaultOptions"""
        options = Namespace(configFile=configFile,
                            minAccuracy=10,
                            maxHits=12)
        defaultOptions = {"minAccuracy":30, "maxHits":14}
        newOptions, infoMsg = importDefaultOptions(options, defaultOptions)
        self.assertEqual(newOptions.minAccuracy,     10)
        self.assertEqual(newOptions.maxHits,         12)


if __name__ == "__main__":
    unittest.main()

