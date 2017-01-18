# -*- coding: utf-8 -*-
#
# Created on Jan 18, 2017
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import unittest
import os
import sys
import tempfile
import numpy as np
from PyQt4 import Qt

sys.path.append('../')

try:
    from Common import *
except:
    raise ImportError('Import error')


class TestCommon(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ensure_dir(self):

        sdir = 'test_ensure_dir'
        ensure_dir(sdir)
        self.assertTrue(os.path.exists(sdir))
        os.removedirs(sdir)

    def test_remove_nans_at_begin_and_end(self):

        x = np.array([0, 0, 10, 20, 30, 40, 50, 0, 0, 0])
        x_out, gap_at_begin, gap_at_end, ifrom, ito = remove_nans_at_begin_and_end(x)

        self.assertTrue(np.alltrue(x_out == np.array([10, 20, 30, 40, 50])))
        self.assertTrue(np.alltrue(gap_at_begin == np.arange(0, 2)))
        self.assertTrue(np.alltrue(gap_at_end == np.arange(7, 10)))

        self.assertEqual(ifrom, 2)
        self.assertEqual(ito, 7)

        x = np.array([np.nan, np.nan, 10, 20, 30, 40, 50, np.nan, np.nan, np.nan])
        x_out, gap_at_begin, gap_at_end, ifrom, ito = remove_nans_at_begin_and_end(x)

        self.assertTrue(np.alltrue(x_out == np.array([10, 20, 30, 40, 50])))
        self.assertTrue(np.alltrue(gap_at_begin == np.arange(0, 2)))
        self.assertTrue(np.alltrue(gap_at_end == np.arange(7, 10)))

        self.assertEqual(ifrom, 2)
        self.assertEqual(ito, 7)

