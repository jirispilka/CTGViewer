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
import numpy as np
import Init


class TestReadWrite(unittest.TestCase):

    def setUp(self):
        Init.init()
        self._dataLoader = LoadData()

    def tearDown(self):
        pass

    def test_read_csv(self):

        file1 = os.path.join('unittest_files', '1001.csv')
        adata, dummy = self._dataLoader.read_csv_file(file1)

        timestamp = adata[Enum.timestamp]
        fhr = adata[Enum.fhr]
        uc = adata[Enum.uc]

        self.assertEqual(timestamp[0], 1)
        self.assertEqual(timestamp[1], 2)

        self.assertEqual(fhr[0], 150.5)
        self.assertEqual(fhr[3], 151.25)
        self.assertEqual(fhr[18978], 94.75)

        self.assertEqual(uc[0], 7.0)
        self.assertEqual(uc[1], 8.5)

    def test_write_read_csv(self):

        t1 = np.zeros((2, 1), np.int)
        t2 = np.zeros((2, 1), np.float64)
        t3 = np.zeros((2, 1), np.float64)
        data_all = dict()

        t1[0, 0] = 1
        t1[1, 0] = 2
        t2[0, 0] = 155.5
        t2[1, 0] = 155
        t3[0, 0] = 7.8
        t3[1, 0] = 8

        data_all[Enum.timestamp] = t1
        data_all[Enum.fhr] = t2
        data_all[Enum.uc] = t3

        file1 = os.path.join('unittest_files', 'test_write_read.csv')
        self._dataLoader.write_csv_file(file1, data_all)

        data_read, dummy = self._dataLoader.read_csv_file(file1)

        timestamp = data_read[Enum.timestamp]
        fhr = data_read[Enum.fhr]
        uc = data_read[Enum.uc]

        # print data_read[0,0], self._data_write[0,0]
        self.assertEqual(timestamp[0, 0], t1[0, 0])
        self.assertEqual(timestamp[1, 0], t1[1, 0])

        self.assertEqual(fhr[0], t2[0, 0])
        self.assertEqual(fhr[1], t2[1, 0])

        self.assertEqual(uc[0], t3[0, 0])
        self.assertEqual(uc[1], t3[1, 0])

    def test_read_matlab(self):

        file1 = os.path.join('unittest_files', '1001.mat')
        adata = self._dataLoader.read_matlab_file(file1)

        timestamp = adata[Enum.timestamp]
        fhr = adata[Enum.fhr]
        uc = adata[Enum.uc]
        fs = adata[Enum.fs]

        self.assertEqual(timestamp[0], 1)
        self.assertEqual(timestamp[1], 2)

        self.assertEqual(fhr[0], 150.5)
        self.assertEqual(fhr[3], 151.25)
        self.assertEqual(fhr[18978], 94.75)

        self.assertEqual(uc[0], 7.0)
        self.assertEqual(uc[1], 8.5)

        self.assertEqual(fs, 4)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestMapper.testName']
    unittest.main()