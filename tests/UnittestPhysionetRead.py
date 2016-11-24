# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import unittest
import os

from LoadWriteData import EnumVariableName as Enum
from LoadWriteData import LoadData
import Init


class TestReadWrite(unittest.TestCase):

    def setUp(self):
        Init.init()
        self._dataLoader = LoadData()

    def tearDown(self):
        pass

    def test_read_header(self):

        file1 = os.path.join('unittest_files', '1001.hea')
        lheader, nrsignals, nfs, nrsamples = self._dataLoader.read_physionet_header(file1)

        dict1 = lheader[0]
        dict2 = lheader[1]

        self.assertEqual(nrsignals, 2)
        self.assertEqual(nfs, 4)
        self.assertEqual(nrsamples, 19200)

        self.assertEqual(dict1['format'], 16)
        self.assertEqual(dict2['format'], 16)
        self.assertEqual(dict1['gain'], 100)
        self.assertEqual(dict2['gain'], 100)

        self.assertEqual(dict1['firstvalue'], 15050)
        self.assertEqual(dict2['firstvalue'], 700)

    def test_read_signal(self):

        file1 = os.path.join('unittest_files', '1001.dat')
        adata, dummy = self._dataLoader.read_physionet_signal16(file1)

        fhr = adata[Enum.fhr]
        uc = adata[Enum.uc]

        self.assertEqual(fhr[0], 150.5)
        self.assertEqual(fhr[3], 151.25)
        self.assertEqual(fhr[18978], 94.75)

        self.assertEqual(uc[0], 7.0)
        self.assertEqual(uc[1], 8.5)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMapper.testName']
    unittest.main()
