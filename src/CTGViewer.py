# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka, Vaclav Chudacek
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
CTGViewer
---------

The CTGViewer module provides the plotting for the CTU-UHB database

Reference
~~~~~~~~~~~

.. autoclass:: CTGViewer
   :members:
"""

from PyQt4 import QtGui
import sys

from Init import init
from MainWindow import Main

DEBUG_PROFILE = False

# conditional import
if DEBUG_PROFILE:
    import cProfile
    import pstats


def main():

    app = QtGui.QApplication(sys.argv)

    init()

    window = Main(sys.argv)

    app.processEvents()

    window.show()
    window.ui.PlotWidget.updatePlots()
    window.setGeometry(50, 50, 1500, 30)

    sys.exit(app.exec_())


if __name__ == '__main__':

    if DEBUG_PROFILE:
        cProfile.run('main()', 'profile_data')
        p = pstats.Stats('profile_data')
        p.sort_stats('time').print_stats(20)
        p.sort_stats('cumulative').print_stats(20)
    else:
        main()
