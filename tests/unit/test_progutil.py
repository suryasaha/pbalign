import unittest
from os import path
from pbalign.utils.progutil import *

class Test_progutil(unittest.TestCase):
    def setUp(self):
        self.prog = "blasr"

    def testAvailability(self):
        self.assertTrue(Availability(self.prog))

    def testCheckAvailability(self):
        CheckAvailability(self.prog)

    def testExecute(self):
        Execute("ls", "ls")

if __name__ == "__main__":
    unittest.main()
