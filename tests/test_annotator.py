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
from PyQt4.QtCore import QPointF
import tempfile
sys.path.append('../')

try:
    from Annotator import Annotator, distance_to_point, compute_dist_ellipse, compute_dist_caliper
    from AnnotationObject import PyQwtPlotCurveAnnotator, PyQwtPlotFloatingBaseline, PyQwtPlotEllipseAnnotator, \
        PyQwtPlotMarkerAnnotator
    from Enums import EnumAnnType as en_ann
except:
    raise ImportError('Import error')


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

    def test_load_not_existing_annotations(self):

        self.annotator.ann_file_load('not_existing_files')
        self.assertDictEqual(self.annotator.get_annotations_fhr(), dict())
        self.assertDictEqual(self.annotator.get_annotations_toco(), dict())

    def test_load_comma_separated_annotations(self):

        self.annotator.ann_file_load(os.path.join('files', 'ann_comma_format.ann'))
        annotations_fhr = self.annotator.get_annotations_fhr()

        d = annotations_fhr['1']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '1')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.basal)
        self.assertEqual(d.x_from, 1)
        self.assertEqual(d.x_to, 19200)
        self.assertEqual(d.yval1, 145)
        self.assertEqual(d.yval2, 145)
        self.assertEqual(d.get_text(), '')

    def test_load_improper_annotations(self):

        self.assertRaises(IOError, self.annotator.ann_file_load, os.path.join('files', 'ann_improper_old.ann'))
        self.assertRaises(IOError, self.annotator.ann_file_load, os.path.join('files', 'ann_improper_wrong.ann'))
        self.assertRaises(IOError, self.annotator.ann_file_load, os.path.join('files', 'ann_unsupported_type.ann'))

    def test_load_annotation(self):

        filemat = os.path.join('files', '1001.mat')

        self.annotator.set_annotation_file(filemat)
        self.assertTrue(self.annotator._get_signal_annotated())

        self.annotator.ann_file_load(filemat)

        annotations_fhr = self.annotator.get_annotations_fhr()
        annotations_toco = self.annotator.get_annotations_toco()

        d = annotations_fhr['1']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '1')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.basal)
        self.assertEqual(d.x_from, 1)
        self.assertEqual(d.x_to, 19200)
        self.assertEqual(d.yval1, 145)
        self.assertEqual(d.yval2, 145)
        self.assertEqual(d.get_text(), '')

        d = annotations_fhr['2']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '2')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.baseline)
        self.assertEqual(d.x_from, 9800)
        self.assertEqual(d.x_to, 11800)
        self.assertEqual(d.yval1, 125)
        self.assertEqual(d.yval2, 125)
        self.assertEqual(d.get_text(), '')

        d = annotations_fhr['3']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '3')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.recovery)
        self.assertEqual(d.x_from, 1169)
        self.assertEqual(d.x_to, 1562)
        self.assertEqual(d.yval1, 149)
        self.assertEqual(d.yval2, 149)
        self.assertEqual(d.get_text(), '')

        d = annotations_fhr['4']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '4')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.no_recovery)
        self.assertEqual(d.x_from, 2991)
        self.assertEqual(d.x_to, 3213)
        self.assertEqual(d.yval1, 139)
        self.assertEqual(d.yval2, 139)
        self.assertEqual(d.get_text(), '')

        d = annotations_fhr['5']
        assert isinstance(d, PyQwtPlotEllipseAnnotator)
        self.assertEqual(d.id, '5')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.ellipsenote)
        self.assertEqual(d.x_from, 8393)
        self.assertEqual(d.x_to, 8742)
        self.assertEqual(d.yval1, 101)
        self.assertEqual(d.yval2, 142)
        self.assertEqual(d.get_text(), 'TEST')

        d = annotations_fhr['6']
        assert isinstance(d, PyQwtPlotMarkerAnnotator)
        self.assertEqual(d.id, '6')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.note)
        self.assertEqual(d.x_from, 14545)
        self.assertEqual(d.x_to, 14545)
        self.assertEqual(d.yval1, None)
        self.assertEqual(d.yval2, None)
        self.assertEqual(d.get_text(), 'bad signal quality')

        d = annotations_toco['7']
        assert isinstance(d, PyQwtPlotEllipseAnnotator)
        self.assertEqual(d.id, '7')
        self.assertEqual(d.get_parent_name(), en_ann.plot_toco)
        self.assertEqual(d.get_curve_type(), en_ann.ellipsenote)
        self.assertEqual(d.x_from, 6037)
        self.assertEqual(d.x_to, 6532)
        self.assertEqual(d.yval1, 0)
        self.assertEqual(d.yval2, 91)
        self.assertEqual(d.get_text(), '')

        d = annotations_toco['8']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '8')
        self.assertEqual(d.get_parent_name(), en_ann.plot_toco)
        self.assertEqual(d.get_curve_type(), en_ann.excessive_ua)
        self.assertEqual(d.x_from, 496)
        self.assertEqual(d.x_to, 1550)
        self.assertEqual(d.yval1, 55)
        self.assertEqual(d.yval2, 55)
        self.assertEqual(d.get_text(), '')

        d = annotations_fhr['9']
        assert isinstance(d, PyQwtPlotFloatingBaseline)
        self.assertEqual(d.id, '9')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.floating_baseline)
        self.assertEqual(d.x_from, 12)
        self.assertEqual(d.x_to, 200)
        self.assertEqual(d.yval1, 146)
        self.assertEqual(d.yval2, 155)
        self.assertEqual(d.get_baseline_points_to_save_in_str(), '12-146,50-138,100-140,200-150')

        d = annotations_fhr['10']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '10')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.acceleration)
        self.assertEqual(d.x_from, 20)
        self.assertEqual(d.x_to, 50)
        self.assertEqual(d.yval1, 123)
        self.assertEqual(d.yval2, 123)
        self.assertEqual(d.get_text(), '')

        d = annotations_fhr['11']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '11')
        self.assertEqual(d.get_parent_name(), en_ann.plot_fhr)
        self.assertEqual(d.get_curve_type(), en_ann.deceleration)
        self.assertEqual(d.x_from, 50)
        self.assertEqual(d.x_to, 100)
        self.assertEqual(d.yval1, 146)
        self.assertEqual(d.yval2, 146)
        self.assertEqual(d.get_text(), '')

        d = annotations_toco['12']
        assert isinstance(d, PyQwtPlotCurveAnnotator)
        self.assertEqual(d.id, '12')
        self.assertEqual(d.get_parent_name(), en_ann.plot_toco)
        self.assertEqual(d.get_curve_type(), en_ann.uterine_contraction)
        self.assertEqual(d.x_from, 100)
        self.assertEqual(d.x_to, 200)
        self.assertEqual(d.yval1, 20)
        self.assertEqual(d.yval2, 20)
        self.assertEqual(d.get_text(), '')

    def test_save_annotations(self):

        ann = dict()
        ann_expected = dict()

        dummy, data_file = tempfile.mkstemp('.mat')
        self.annotator.set_annotation_file(data_file)
        ann_file = self.annotator.get_annotation_file()

        ann['1'] = PyQwtPlotCurveAnnotator(en_ann.plot_fhr, en_ann.basal, 1, 10, 150, 150)
        ann['2'] = PyQwtPlotCurveAnnotator(en_ann.plot_fhr, en_ann.baseline, 2, 11, 155, 155)
        ann['3'] = PyQwtPlotCurveAnnotator(en_ann.plot_fhr, en_ann.recovery, 3, 12, 140, 140)
        ann['4'] = PyQwtPlotCurveAnnotator(en_ann.plot_fhr, en_ann.no_recovery, 4, 14, 110, 110)
        ann['5'] = PyQwtPlotMarkerAnnotator(en_ann.plot_fhr, en_ann.note, 1, 1, None, None, 'test_note')
        ann['6'] = PyQwtPlotEllipseAnnotator(en_ann.plot_fhr, en_ann.ellipsenote, 1, 10, 1, 10, 'test ellipse')
        ann['7'] = PyQwtPlotCurveAnnotator(en_ann.plot_toco, en_ann.excessive_ua, 5, 16, 56, 50)
        ann['8'] = PyQwtPlotCurveAnnotator(en_ann.plot_fhr, en_ann.acceleration, 8, 12, 100, 100)
        ann['9'] = PyQwtPlotCurveAnnotator(en_ann.plot_fhr, en_ann.deceleration, 9, 13, 101, 101)
        ann['10'] = PyQwtPlotCurveAnnotator(en_ann.plot_toco, en_ann.uterine_contraction, 10, 14, 51, 51)

        note = '1-100,2-101,5-102,100-125'
        ann['11'] = PyQwtPlotFloatingBaseline(en_ann.plot_fhr, en_ann.floating_baseline, 1, 100, 120, 125,note)
        ann['11'].set_baseline_points_from_str(note)

        ann_expected['1'] = '1;fhr;basal;1;10;150;150;\n'
        ann_expected['2'] = '2;fhr;baseline;2;11;155;155;\n'
        ann_expected['3'] = '3;fhr;recovery;3;12;140;140;\n'
        ann_expected['4'] = '4;fhr;no_recovery;4;14;110;110;\n'
        ann_expected['5'] = '5;fhr;note;1;1;None;None;test_note\n'
        ann_expected['6'] = '6;fhr;ellipsenote;1;10;1;10;test ellipse\n'
        ann_expected['7'] = '7;toco;excessive_ua;5;16;56;56;\n'
        ann_expected['8'] = '8;fhr;acceleration;8;12;100;100;\n'
        ann_expected['9'] = '9;fhr;deceleration;9;13;101;101;\n'
        ann_expected['10'] = '10;toco;uterine_contraction;10;14;51;51;\n'
        ann_expected['11'] = '11;fhr;floating_baseline;1;100;120;125;1-100,2-101,5-102,100-125\n'

        for key in ann.iterkeys():
            temp = dict()
            temp[key] = ann[key]
            self.annotator.set_annotations_and_save(temp, dict())

            with open(ann_file, 'r') as fr:
                c = fr.read()
                self.assertEqual(c, ann_expected[key])

            if os.path.exists(self.annotator.get_annotation_file()):
                os.remove(self.annotator.get_annotation_file())

        if os.path.exists(data_file):
            os.remove(data_file)


if __name__ == "__main__":
    unittest.main()

