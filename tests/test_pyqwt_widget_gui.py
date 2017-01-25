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
    from Enums import EnumAnnType
    from PyQwtWidgetGui import PyQwtWidgetGui
except:
    raise ImportError('Import error')


class TestAnnotator(unittest.TestCase):

    def setUp(self):
        pass
        # pyqwt_widget = PyQwtWidgetGui()

        # app = Qt.QApplication(sys.argv)
        # self.pyqwt_widget = PyQwtWidgetGui()
        # self.pyqwt_widget.show()
        # sys.exit(app.exec_())

    def tearDown(self):
        pass
        # self.pyqwt_widget.close()

    # def test_plot(self):
    #
    #     x = np.array([100, 200, 300])
    #     y = np.array([100, 200, 300])
    #     a = 5
    #     # self.pyqwt_widget.plot(x, y)
    #     pass

    def test_set_x_axis(self):

        # self.pyqwt_widget.setXAxis()
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()

