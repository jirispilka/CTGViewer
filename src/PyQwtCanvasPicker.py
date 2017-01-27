# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

"""
PyQwtCanvasPicker
----------------
The PyQwtCanvasPicker emits signals with cursor position when a plot is clicked
"""

from PyQt4.QtCore import pyqtSignal, QPoint
from PyQt4 import Qt
from PyQt4.Qwt5.Qwt import QwtPlotCanvas, QwtPlot

bDEBUG = False


class PyQwtCanvasPicker(Qt.QObject):

    signal_point_clicked = pyqtSignal(['QPoint'])

    def __init__(self, plot):
        Qt.QObject.__init__(self, plot)
        self.__selectedCurve = None
        self.__selectedPoint = -1
        self.__plot = plot

        canvas = plot.canvas()
        canvas.installEventFilter(self)

        # We want the focus, but no focus rect.
        # The selected point will be highlighted instead.
        canvas.setFocusPolicy(Qt.Qt.StrongFocus)
        canvas.setCursor(Qt.Qt.PointingHandCursor)
        canvas.setFocusIndicator(QwtPlotCanvas.ItemFocusIndicator)
        canvas.setFocus()

    def eventFilter(self, object, event):
        """
        if event.type() == Qt.QEvent.FocusIn:
            self.__showCursor(True)
        if event.type() == Qt.QEvent.FocusOut:
            self.__showCursor(False)
        """

        if event.type() == Qt.QEvent.Paint:
            Qt.QApplication.postEvent(self, Qt.QEvent(Qt.QEvent.User))

        elif (event.type() == Qt.QEvent.MouseButtonPress) | (event.type() == Qt.QEvent.MouseMove):

            clicked_point = self._compute_point_clicked(event)
            self._point_clicked(clicked_point)
            return True

        return QwtPlot.eventFilter(self, object, event)

    def _compute_point_clicked(self, event):
        """
        The clicked point stored in event.x() and event.y() is transformed to x and y axis for
        particular plot attached.

        :param event: event
        :type  event: QEvent
        :rtype: QPoint
        """
        clickedpointx = self.__plot.invTransform(QwtPlot.xBottom, event.pos().x())
        clickedpointy = self.__plot.invTransform(QwtPlot.xBottom, event.pos().y())

        if bDEBUG:
            print event.pos()
            print clickedpointx
            print clickedpointy

        return QPoint(int(clickedpointx), int(clickedpointy))

    def _point_clicked(self, point):
        """
        This signal is emitted when user click on a plot.
        """
        self.signal_point_clicked.emit(point)
