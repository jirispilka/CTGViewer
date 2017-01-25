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
    from GuiForms import AddNoteDialog
    from Enums import EnumAnnType as en_ann
except:
    raise ImportError('Import error')

app = QApplication(sys.argv)


class TestAnnotator(unittest.TestCase):

    def setUp(self):
        self.form = AddNoteDialog()

    def tearDown(self):
        pass

    def test_set_text(self):
        s = 'TEST - TEST'
        self.form.set_text(s)
        self.assertEqual(s, self.form.ui.textNote.toPlainText())

    def test_get_text(self):

        input_s = 'This is very long text that will be probably broken to several lines'
        self.form.ui.textNote.setText(input_s)

        s = self.form.get_text()
        s = s.replace('\n', ' ')

        self.assertEqual(s, input_s)

    def test_clear_text(self):
        self.form.ui.textNote.setText('TEST')
        self.form.clear_text()
        self.assertEqual(self.form.ui.textNote.toPlainText(), '')


if __name__ == "__main__":
    unittest.main()

