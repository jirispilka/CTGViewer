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
PyQwtNavigationPlot
--------------------

The navigation plot shows overview of complete signals. By clicking on this
plot the controled plots are moved to the clicked position. The area of visible signal
is highlighted using py:class:´PyQwtNavigationPlotHighlight´

Reference
~~~~~~~~~

.. autoclass:: PyQwtNavigationPlot
   :members:
   :undoc-members:

.. autoclass:: PyQwtNavigationPlotHighlight
   :members:
   :undoc-members:

"""
from PyQt4.QtGui import QColor
from PyQt4 import Qt
from PyQt4.Qwt5.Qwt import QwtPlotCurve, QwtScaleDiv, QwtPlot

from PyQwtWidgetGui import PyQwtWidgetGui
from PyQwtCanvasPicker import PyQwtCanvasPicker
from Config import ConfigStatic


class PyQwtNavigationPlot(PyQwtWidgetGui):
    """
    The navigation plot shows overview of complete signals. By clicking on this
    plot a signal is emitted with clicked point position.

    :param parent:
    :param l_controled_plots: list of controled plots
    :type  parent: QWidget
    :type  l_controled_plots: :py:mod:`PyQwtWidgetGui`
    """

    # selectedPointChanged = pyqtSignal(['int'])

    def __init__(self, parent=None, l_controled_plots=None):
        PyQwtWidgetGui.__init__(self, parent)

        self.l_controled_plots = l_controled_plots
        self._timeString = None
        self._selected_point = 0
        # self._paper_height = 75
        self._height = 120
        # self._height = 220
        self._toco_offset = -1*ConfigStatic.plot_toco_offset

        self.xlabel("")
        color = QColor(200, 200, 200)
        self.setCanvasBackground(color)
        self.xAxisEnabled(True)
        self.yAxisEnabled(False)
        # self.yAxisEnabled(True)
        self.setMaximumHeight(self._height)
        self.setMinimumHeight(self._height)

        self.set_locator_minute(60)
        # self.setLocatorHourInterval(2)
        self.setYMinMax(self._toco_offset, 200)
        # self.setYMinMax(0, 300)

        self.canvasPicker = PyQwtCanvasPicker(self)
        self.canvasPicker.signal_point_clicked.connect(self.set_selected_point)

        self._step = 300*self.get_sampling_freq()  # 300 = 5 minutes / for left-rigth arrow move

        self.signal_plot_cleared.connect(self.reinit)
        self.reinit()

    def reinit(self):

        # self._selected_point = 0
        navplothighlight = PyQwtNavigationPlotHighlight(self)
        navplothighlight.attach(self)

        # cm = self.canvasMap(QwtPlot.xBottom)
        # self._pointFmin = self.invTransform(QwtPlot.xBottom, cm.p1())
        # self._pointFmax = self.invTransform(QwtPlot.xBottom, cm.p2())

    def setXAxis(self, center_point=None, breplot=True):

        if self._bPlotDatesXAxis:
            scalediv = self.axisScaleDiv(QwtScaleDiv.MajorTick)
            scalediv.setTicks(QwtScaleDiv.MinorTick, [])
            scalediv.setTicks(QwtScaleDiv.MediumTick, [])
            scalediv.setTicks(QwtScaleDiv.MajorTick, self._time_tics_located)
            # print scalediv.isValid()
            # print self._time_tics_located
            scalediv.setInterval(self._minTime, self.xAxisMaxSample())
            self.setAxisScaleDiv(QwtPlot.xBottom, scalediv)

            if breplot:
                self.replot()

    def setYAxis(self, height=None, bReplot=True):
        self.setAxisScale(QwtPlot.yLeft, self._minView, self._maxView, 0)

    def clear_selected_point(self):
        self._selected_point = 0

    def get_selected_point(self):
        """
        When user clicked on the plot, this variable holds x-coordinate of a point

        :rtype: QPointF
        """
        return self._selected_point

    def set_selected_point(self, point):
        """
        Set point clicked by a user.

        :param point: clicked point
        :type  point: QPointF
        """
        self._selected_point = point.x()
        self.correct_point_boundaries()
        self._selected_point_changed(self._selected_point)

    def change_selected_pointright(self, step=None):

        step = step if step is not None else self._step
        self._selected_point += step
        self.correct_point_boundaries()
        self._selected_point_changed(self._selected_point)

    def change_selected_pointleft(self, step=None):

        step = step if step is not None else self._step
        self._selected_point -= step
        self.correct_point_boundaries()
        self._selected_point_changed(self._selected_point)

    def correct_point_boundaries(self):
        """
        If a point is inside boundaries. Point is restricted to be within r = (xmax - xmin)/2, [r, max_view - r]
        """

        xmin = self.l_controled_plots[0].viewXMinSample()
        xmax = self.l_controled_plots[0].viewXMaxSample()
        r = int((xmax - xmin)/2)

        nmax = self.xAxisMaxSample()
        if self._selected_point < r:
            self._selected_point = r
        elif self._selected_point > nmax - r:
            self._selected_point = nmax - r

    def _selected_point_changed(self, point):
        """
        When user click on navigation plot:
        Updates all controled plots -> set their x axis
        Updates (this) navigation plot.
        """
        for plot in self.l_controled_plots:
            plot.setXAxis(point)

        self.replot()

    def get_toco_offset(self):
        return self._toco_offset


class PyQwtNavigationPlotHighlight(QwtPlotCurve):
    """
    The navigation plot highlight is used for highlighting area where
    user clicked with mouse. This class is inherited from Qwt.QwtPlotCurve.

    :param p_navplot: navigation plot widget
    :type  p_navplot: :py:mod:`PyQwtWidgetGui`
    """

    def __init__(self, p_navplot):
        QwtPlotCurve.__init__(self)

        self.__p_nav_plot = p_navplot
        _color = QColor(0, 0, 0)
        _color.setAlpha(50)
        self._penColor = _color
        self._brushColor = _color

    def drawFromTo(self, painter, xmap, ymap, start, stop):
        """
        Draws rectangles around a point where user clicked

        :param painter:
        :param xmap:
        :param ymap:
        :param start:
        :param stop:
        :type  painter: QPainter
        """
        painter.setPen(Qt.QPen(self._penColor, 1))
        painter.setBrush(self._brushColor)

        maxyview = self.__p_nav_plot.viewYMaxSample()
        minyview = self.__p_nav_plot.viewYMinSample()
        yminmarginpx, ymaxmarginpx = self.__p_nav_plot.getMarginsYPx()

        py1 = ymap.transform(minyview) + yminmarginpx
        py2 = ymap.transform(maxyview) - ymaxmarginpx

        clickedpoint = self.__p_nav_plot.get_selected_point()
        viewxminsamp = self.__p_nav_plot.l_controled_plots[0].viewXMinSample()
        viewxmaxsamp = self.__p_nav_plot.l_controled_plots[0].viewXMaxSample()
        xaxisminsmaple = self.__p_nav_plot.l_controled_plots[0].xAxisMinSample()
        xaxismaxsmaple = self.__p_nav_plot.l_controled_plots[0].xAxisMaxSample()

        # check boundaries for line plotting
        if clickedpoint < viewxminsamp:
            clickedpoint = viewxminsamp
        elif clickedpoint > viewxmaxsamp:
            clickedpoint = viewxmaxsamp

        # drawRect(x,  y, width, height)
        painter.drawRect(xmap.transform(viewxminsamp), py1,
                         xmap.transform(viewxmaxsamp) - xmap.transform(viewxminsamp), py2 - py1)
        painter.drawLine(xmap.transform(clickedpoint), py1, xmap.transform(clickedpoint), py2)

        # painter.setPen(Qt.QPen(QColor(100, 100, 100), 1))
        # painter.setBrush(self._brushColor)
        # p = ymap.transform((maxyview - minyview)/2)
        # painter.drawLine(xmap.transform(xaxisminsmaple), p, xmap.transform(xaxismaxsmaple), p)
