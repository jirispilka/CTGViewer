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
import sys
from PyQt4.QtCore import QPointF

from Annotator import Annotator, distance_to_point, compute_dist_ellipse, compute_dist_caliper
sys.path.append('../')


class TestAnnotator(unittest.TestCase):

    def setUp(self):
        self.annotator = Annotator()

    def tearDown(self):
        pass

    def test_distance_to_point(self):
        self.assertAlmostEqual(distance_to_point(QPointF(0, 0), 3, 3), 4.24, places=2)

    def test_distance_to_ellipse(self):
        dcxcy, dcxy2, dx2cy, dcxy1, dx1cy = compute_dist_ellipse(0, 1, 0, 1, QPointF(0, 0))
        self.assertAlmostEqual(dcxcy, 0.707, places=2)
        self.assertAlmostEqual(dcxy2, 1.118, places=2)
        self.assertAlmostEqual(dx2cy, 1.118, places=2)
        self.assertAlmostEqual(dcxy1, 0.500, places=2)
        self.assertAlmostEqual(dx1cy, 0.500, places=2)

    def test_distance_to_caliper(self):
        x_from = 0
        x_to = 10
        y1 = 0
        y2 = 20
        pos = QPointF(7, 15)
        d_center, d_y2, d_x2, d_y1, d_x1 = compute_dist_caliper(x_from, x_to, y1, y2, pos)
        self.assertAlmostEqual(d_center, 5.385, places=2)
        self.assertEqual(d_x1, 7)
        self.assertEqual(d_x2, 3)
        self.assertEqual(d_y1, 15)
        self.assertEqual(d_y2, 5)

    def test_load_annotations(self):

        self.annotator.ann_file_load('not_existing_files')
        self.assertDictEqual(self.annotator.get_annotations_fhr(), dict())
        self.assertDictEqual(self.annotator.get_annotations_toco(), dict())





if __name__ == "__main__":
    unittest.main()

