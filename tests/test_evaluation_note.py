# -*- coding: utf-8 -*-
#
# Created on Jan 21, 2017
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
    from PyQt4.QtGui import QApplication
    from PyQt4.QtTest import QTest
    from PyQt4.QtCore import Qt
    from GuiForms import EvaluationNoteDialog
    from Enums import EnumInitialCTG, EnumInterventions, EnumNeurology
except:
    raise ImportError('Import error')

app = QApplication(sys.argv)


class TestAnnotator(unittest.TestCase):

    def setUp(self):
        self.form = EvaluationNoteDialog()

        self.eval_string = 'initial_ctg:abnormal__intervention:cesarean section__concern:3__ph:7.2__neurology:none'

    def set_predefined_values(self):
        self.form.ui.cbInitialCTG.setCurrentIndex(1)
        self.form.ui.cbIntervention.setCurrentIndex(1)
        self.form.ui.cbNeurology.setCurrentIndex(1)

        self.form.ui.sbLevelConcern.setValue(3)
        self.form.ui.sbph.setValue(7.2)

    def tearDown(self):
        pass

    def test_clear(self):
        self.set_predefined_values()

        self.form.clear()
        self.assertEqual(self.form.ui.cbInitialCTG.currentText(), '')
        self.assertEqual(self.form.ui.cbIntervention.currentText(), '')
        self.assertEqual(self.form.ui.cbNeurology.currentText(), '')

        self.assertEqual(self.form.ui.sbLevelConcern.value(), -1)
        self.assertEqual(self.form.ui.sbph.value(), 6.5)

    def test_fill_all_combos(self):
        """
        Test whether all combo boxes are properly filled with Enums values
        :return:
        """
        self.form.fill_all_combos()

        # assertions here
        self.helper_fill_all_combos(EnumInitialCTG, self.form.ui.cbInitialCTG)
        self.helper_fill_all_combos(EnumInterventions, self.form.ui.cbIntervention)
        self.helper_fill_all_combos(EnumNeurology, self.form.ui.cbNeurology)

    def helper_fill_all_combos(self, en, cb):
        """

        :param en: Enum with values
        :param cb: pointer to combox box
        :return:
        """

        d = en.__dict__
        d = {key: val for key, val in d.iteritems() if key[0:2] != '__'}

        for i in range(0, cb.count()):
            s = str(cb.itemText(i))
            if not s == '':
                self.assertTrue(s in d.values(), msg='values: {0}:{1}'.format(s, d))

    def test_set_combobox_value(self):

        val = self.form._set_combobox_value(self.form.ui.cbInitialCTG, EnumInitialCTG.normal)
        self.assertEqual(val, 0)

        self.assertRaises(ValueError, self.form._set_combobox_value, self.form.ui.cbInitialCTG, 'not existing value')

    def test_make_evaluation_string(self):

        self.set_predefined_values()

        sout = self.form.make_evaluation_string()
        self.assertEqual(sout, self.eval_string)

    def test_set_values_from_evaluation_string(self):

        self.form.clear()

        self.form.set_values_from_evaluation_string(self.eval_string)

        self.assertEqual(self.form.ui.cbInitialCTG.currentText(), 'abnormal')
        self.assertEqual(self.form.ui.cbIntervention.currentText(), 'cesarean section')
        self.assertEqual(self.form.ui.cbNeurology.currentText(), 'none')

        self.assertEqual(self.form.ui.sbLevelConcern.value(), 3)
        self.assertEqual(self.form.ui.sbph.value(), 7.2)

        self.assertRaises(ValueError, self.form.set_values_from_evaluation_string, 'ph:5')
        self.assertRaises(ValueError, self.form.set_values_from_evaluation_string, 'concern:15')


if __name__ == "__main__":
    unittest.main()

