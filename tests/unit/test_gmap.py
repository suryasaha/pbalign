"""Test pbalign.alignservices.gmap."""
import unittest
from os import path
from pbalign.alignservice.gmap import GMAPService
from pbalign.pbalignfiles import PBAlignFiles
from pbalign.options import parseOptions
import argparse


class Test_GMAPService(unittest.TestCase):
    """Test pbalign.alignservices.gmap."""
    def setUp(self):
        """Set up test data."""
        self.rootDir = path.dirname(path.dirname(path.abspath(__file__)))
        self.outDir = path.join(self.rootDir, "out/")
        self.outSam = path.join(self.outDir, "test_gmap_01.sam")
        self.dataDir = path.join(self.rootDir, "data/")
        self.queryFofn = path.join(self.dataDir, "ecoli_lp.fofn")
        self.refFa = path.join(self.dataDir, "ecoli.fasta")
        self.repoPath = "/mnt/secondary/Smrtanalysis/opt/smrtanalysis/" + \
                        "common/references/ecoli/"

    def test_gmapCreateDB_case1(self):
        """Test _gmapCreateDB(refFile, isWithinRepository, tempRootDir).
        Condition: the reference is not within a reference repository.
        """
        # Case 1: the reference is not within a reference repository
        files = PBAlignFiles()
        parser = argparse.ArgumentParser()
        argumentList = [self.queryFofn, self.refFa, self.outSam,
                        '--algorithm', 'gmap']
        parser, options, _info = parseOptions(argumentList=argumentList,
                                              parser=parser)
        service = GMAPService(options, files)
        dbRoot, dbName = service._gmapCreateDB(self.refFa, False, self.outDir)
        self.assertTrue(path.exists(dbRoot))
        self.assertTrue(path.exists(path.join(dbRoot, dbName)))

    def test_gmapCreateDB_case2(self):
        """Test _gmapCreateDB(refFile, isWithinRepository, tempRootDir).
        Condition: the reference is within a reference repository.
        """
        # Case 2: the reference is within a reference repository
        files = PBAlignFiles()
        parser = argparse.ArgumentParser()
        argumentList = [self.queryFofn, self.repoPath, self.outSam,
                        '--algorithm', 'gmap']
        parser, options, _info = parseOptions(argumentList=argumentList,
                                              parser=parser)
        service = GMAPService(options, files)
        dbRoot, dbName = service._gmapCreateDB(files.targetFileName, True,
                                               self.outDir)
        self.assertEqual(path.abspath(dbRoot), path.abspath(self.repoPath))
        self.assertEqual(dbName, "gmap_db")
