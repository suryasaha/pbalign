"""Test pbalign.utils.RgnH5IO.py."""

import unittest
from pbcore.io.BasH5IO import ADAPTER_REGION, INSERT_REGION, HQ_REGION
from pbalign.utils.RgnH5IO import Region, RegionTable, RgnH5Reader, \
    RgnH5Writer, addStrListAttr
from os import path
import h5py


class Test_RgnH5IO(unittest.TestCase):
    """Test RgnH5Reader and RgnH5Writer."""

    def setUp(self):
        """Set up test data."""
        self.rootDir = path.dirname(path.dirname(path.abspath(__file__)))
        self.inRgnFN = "/mnt/secondary-siv/testdata/" + \
            "BlasrTestData/pbalign/data/test_rgnh5io.rgn.h5"
        self.outRgnFN = path.join(self.rootDir, "out/test_rgnh5io_out.rgn.h5")
        self.outTmpFN = path.join(self.rootDir, "out/test_rgnh5io_tmp.h5")
        self.movieName = "m130427_152935_42178_" + \
            "c100518602550000001823079209281316_s1_p0"

    def test_Region(self):
        """Test class Region."""
        rtuple = (0, 2, 2, 3, 4)
        r = Region(list(rtuple))
        self.assertTrue(r.toTuple() == rtuple)
        r.setStartAndEnd(10, 20)
        self.assertTrue(r.toTuple() == (0, 2, 10, 20, 4))
        self.assertTrue(r.isHqRegion)
        self.assertTrue(r.holeNumber == 0)
        self.assertTrue(r.typeIndex == HQ_REGION)
        self.assertTrue(r.start == 10)
        self.assertTrue(r.end == 20)
        self.assertTrue(r.score == 4)

        # Create an instance of Region with type = ADAPTER_REGION.
        self.assertTrue(Region([11, ADAPTER_REGION, 30, 50, -1]).isAdapter)
        # Create an instance of Region with type = INSERT_REGION.
        self.assertTrue(Region([11, INSERT_REGION, 30, 50, -1]).isInsert)

    def test_RegionTable(self):
        """Test class RegionTable."""
        l = [Region([11, 1, 1634, 7207, -1]), Region([11, 2, 1634, 7207, 872])]
        rt = RegionTable(11, l)
        self.assertEqual(rt.numRegions, 2)
        self.assertEqual(rt.toList(), [(11, 1, 1634, 7207, -1),
                                       (11, 2, 1634, 7207, 872)])

    def test_reader(self):
        """Test RgnH5Reader."""
        reader = RgnH5Reader(self.inRgnFN)
        for rt in reader:
            if (rt.holeNumber in [0, 1, 81740]):
                self.assertEqual(
                    rt.toList(),
                    [(rt.holeNumber, 2, 0, 0, 0)])
            elif rt.holeNumber == 11:
                self.assertEqual(
                    rt.toList(),
                    [(11, 1, 1634, 7207, -1), (11, 2, 1634, 7207, 882)])
            elif rt.holeNumber == 30:
                self.assertEqual(
                    rt.toList(),
                    [(30, 1, 14046, 17047, -1),
                     (30, 1, 17092, 19610, -1),
                     (30, 0, 17047, 17092, 955),
                     (30, 2, 14046, 19610, 890)])
                # Reset HQRegion and test.
                rt.setHQRegion(0, 0)
                self.assertEqual(
                    rt.toList(),
                    [(30, 1, 14046, 17047, -1),
                     (30, 1, 17092, 19610, -1),
                     (30, 0, 17047, 17092, 955),
                     (30, 2, 0, 0, 890)])
        self.assertEqual(reader.movieName, self.movieName)
        self.assertEqual(reader.numZMWs, 81741)
        reader.close()

    def test_writer(self):
        """Test RgnH5Writer()."""
        reader = RgnH5Reader(self.inRgnFN)
        writer = RgnH5Writer(self.outRgnFN)
        writer.writeScanDataGroup(reader.scanDataGroup)
        for rt in reader:
            writer.addRegionTable(rt)
            if rt.holeNumber == 1000:
                break
        reader.close()
        writer.close()

        reader1 = RgnH5Reader(self.inRgnFN)
        reader2 = RgnH5Reader(self.outRgnFN)
        self.assertTrue("PulseData" in reader2.file)
        self.assertTrue("ScanData" in reader2.file)
        for (rt1, rt2) in zip(reader1, reader2):
            self.assertEqual(rt1.toList(), rt2.toList())
            if rt1.holeNumber == 1000:
                break

    def test_addStrListAttr(self):
        """Test function addStrListAttr(obj, name, strlist)."""
        f = h5py.File(self.outTmpFN, 'w')
        obj = f.create_group("PulseData")
        addStrListAttr(obj, "addedAttr", ["val1", "val2"])
        f.close()

        f = h5py.File(self.outTmpFN, 'r')
        self.assertTrue("addedAttr" in f["PulseData"].attrs)
        attrList = f["PulseData"].attrs["addedAttr"]
        self.assertEqual(attrList[0], 'val1')
        self.assertEqual(attrList[1], 'val2')
        f.close()


if __name__ == "__main__":
    unittest.main()
