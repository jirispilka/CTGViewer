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

        x = np.array([0, 0, 10, 20, 30, 0, 40, 50, 0, 0, 0])
        x_out, gap_at_begin, gap_at_end, ifrom, ito = remove_nans_at_begin_and_end(x)

        self.assertTrue(np.alltrue(x_out == np.array([10, 20, 30, 0, 40, 50])))
        self.assertTrue(np.alltrue(gap_at_begin == np.arange(0, 2)))
        self.assertTrue(np.alltrue(gap_at_end == np.arange(8, 11)))

        self.assertEqual(ifrom, 2)
        self.assertEqual(ito, 8)

        x = np.array([np.nan, np.nan, 10, 20, 30, 40, 50, np.nan, np.nan, np.nan])
        x_out, gap_at_begin, gap_at_end, ifrom, ito = remove_nans_at_begin_and_end(x)

        self.assertTrue(np.alltrue(x_out == np.array([10, 20, 30, 40, 50])))
        self.assertTrue(np.alltrue(gap_at_begin == np.arange(0, 2)))
        self.assertTrue(np.alltrue(gap_at_end == np.arange(7, 10)))

        self.assertEqual(ifrom, 2)
        self.assertEqual(ito, 7)

    def test_samples2time(self):

        atime = samples2time(10, 1)
        self.assertEqual(atime[0], '00:00:01:000')
        self.assertEqual(atime[4], '00:00:05:000')

        atime = samples2time(10, 1, time_begin='01:10:10:000')
        self.assertEqual(atime[6], '01:10:17:000')

    def test_time_locator(self):

        timestring = None
        self.assertIsNone(time_locator(timestring, 0, 0, 0, 0))

        timestring = ['00:00:00:000', '00:30:00:000', '01:00:00:000', '01:30:00:000', '02:00:00:000']
        ticks_expected = [0.0, 2.0, 4.0]

        # guess hour location
        ticks = time_locator(timestring, -1, -1, 5, 1/float(30 * 60))

        for t1, t2 in zip(ticks, ticks_expected):
            self.assertEqual(t1, t2)

        # specify hour locator
        ticks = time_locator(timestring, -1, 1, 5, 1 / float(30 * 60))
        for t1, t2 in zip(ticks, ticks_expected):
            self.assertEqual(t1, t2)

        # minute locator
        timestring = ['00:00:00:000', '00:00:30:000', '00:01:00:000', '00:01:30:000', '00:02:00:000']
        ticks = time_locator(timestring, 1, -1, 5, 1/float(.5 * 60))

        for t1, t2 in zip(ticks, ticks_expected):
            self.assertEqual(t1, t2)

    def test_calib_signal(self):

        fs = 1
        fhr, uc, timestamp = generate_calib_signal(fs, 'EU')
        self.assertEqual(fhr[0], 50)
        self.assertEqual(fhr[60], 60)
        self.assertEqual(fhr[120], 70)

        self.assertEqual(uc[0], 0)
        self.assertEqual(uc[60], 10)
        self.assertEqual(uc[120], 15)

        self.assertEqual(timestamp[0], 1)
        self.assertEqual(timestamp[20], 21)

        self.assertEqual(len(fhr), len(uc))
        self.assertEqual(len(fhr), len(timestamp))


