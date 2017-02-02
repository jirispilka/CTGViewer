# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)


# noinspection PyPackageRequirements
"""
PyQwtWidgetGui
----------------

The PyQwtWidgetGui module provides the plotting widget base class. This class ensures:
    * proper ratio of scales cm/min, bpm/cm
    * appearance of all derived plot

Reference
~~~~~~~~~~~

.. autoclass:: PyQwtWidgetGui
   :members:

.. autoclass:: TimeScaleDraw
   :members:

.. autoclass:: EnumPlotSpeed
.. autoclass:: EnumPlotBpm

"""

from PyQt4 import QtCore, QtGui, Qt
# import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5 import Qwt

import numpy as np
import logging
import sys

from Config import ConfigStatic
from Annotator import CanvasPickerAnnotator
from AnnotationObject import *
from Enums import *
from Common import time_locator, samples2time

DEBUG_PROFILE = False

if DEBUG_PROFILE:
    import cProfile
    import pstats


class PyQwtWidgetGui(Qwt.QwtPlot):
    """
    Base class plotting widget based on PyQwt.

    :param parent:
    """
    DEBUG_Y_AXIS_SIZE = False
    DEBUG_X_AXIS_SIZE = False

    signal_plot_cleared = QtCore.pyqtSignal()
    signal_ann_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None, name=''):
        Qwt.QwtPlot.__init__(self, parent)

        self._log = logging.getLogger(ConfigStatic.logger_name)
        self._log.info('passed')

        self.__name = name
        self._font_app = QtGui.QFont()

        dpi = 96
        # TODO test physicalDpi (funguje v MainWindow.py)
        self._dpi2px = dpi*(1/2.54)
        self._plotSpeed = EnumPlotSpeed.oneCmMin
        self._plotBpm = EnumPlotBpm.twentyBpmCm
        self._plotBpmMajorTick = self._plotBpm

        #: Doc comment for instance attribute qux.
        self._minView = 0
        self._maxView = 240
        self._min_view_paper_lim = 0
        self._max_view_paper_lim = 240
        self._paper_format = EnumPaperFormat.EU
        self._minTime = 0
        self._maxTime = 0
        self._centerPoint = 0
        self.__sampling_freq = 4

        self._x = np.zeros(1)
        self._y = np.zeros(1)
        self._timeString = list()

        self._define_paper()

        # self.__canvasXMap = self.canvasMap(Qwt.QwtPlot.xBottom)
        # self.__canvasYMap = self.canvasMap(Qwt.QwtPlot.yLeft)

        self.setCanvasBackground(Qt.Qt.white)
        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time [min]")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "")

        # curves
        self.curve1 = Qwt.QwtPlotCurve('signal')
        # #self.curve1.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        # self.curve1.setPen(QPen(Qt.Qt.black,0, Qt.Qt.SolidLine))
        # self.curve1.setYAxis(Qwt.QwtPlot.yLeft)
        # self.curve1.attach(self)
        self._baseline = Qwt.QwtPlotMarker()

        ''' annotations '''
        self.__d_ann_all_curves = dict()
        self.d_ann_all_curves_navplot = dict()
        self.__ann_action = 0
        self.caliper = Caliper(self, EnumAnnType.plot_fhr, EnumAnnType.caliper)
        # self.caliper.plot()

        # time scale - for string time scale
        self.timeScale = TimeScaleDraw(self)
        self.setAxisScaleDraw(Qwt.QwtPlot.xBottom, self.timeScale)

        # time scale - for Y axis
        self.yAxisScale = AxisYScaleDraw(self)
        self.setAxisScaleDraw(Qwt.QwtPlot.yLeft, self.yAxisScale)

        self._bPlotDatesXAxis = False
        self._time_tics_located = list()
        self._locator_min = 5
        self._locator_hour = 0

        # grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.enableYMin(True)
        self.grid.enableXMin(True)
        self.grid.setMajPen(QtGui.QPen(Qt.Qt.lightGray, 0, Qt.Qt.SolidLine))
        self.grid.setMinPen(QtGui.QPen(Qt.Qt.lightGray, 0, Qt.Qt.DotLine))
        self.grid.attach(self)

        self.__set_axis_app_font()

        # self.replot()
        # self.setAxisScaleDraw(Qwt.QwtPlot.xBottom)
        # self.scaleDiv.attach(self)
        # self.setYAxis()

    def __set_axis_app_font(self):
        self.setAxisFont(Qwt.QwtPlot.xBottom, self._font_app)
        self.setAxisFont(Qwt.QwtPlot.yLeft, self._font_app)

    def clear_plot(self):
        """
        When a plot is cleared a signal is emitted in order to allow the Plot to reinit
        """
        self._timeString = []
        self._bPlotDatesXAxis = False
        self._time_tics_located = []
        self.ann_delete_all(False, False)
        self.clear()  # calls deattach all items
        self.signal_plot_cleared.emit()

    def get_sampling_freq(self):
        return self.__sampling_freq

    def set_sampling_freq(self, fs):
        self.__sampling_freq = fs

    def get_ann_action(self):
        return self.__ann_action

    def set_ann_action(self, action=EnumAnnType.select):

        self.__ann_action = action

        if action == EnumAnnType.select:
            self.canvas().setCursor(Qt.Qt.ArrowCursor)

        elif action == EnumAnnType.basal or action == EnumAnnType.baseline \
                or action == EnumAnnType.recovery or action == EnumAnnType.no_recovery \
                or action == EnumAnnType.ellipse or action == EnumAnnType.evaluation_note:
            self.canvas().setCursor(Qt.Qt.CrossCursor)

        elif action == EnumAnnType.caliper:
            self.canvas().setCursor(Qt.Qt.ArrowCursor)

        else:
            self.canvas().setCursor(Qt.Qt.CrossCursor)

    def _define_paper(self):
        """
        Define paper speed and size.
        """
        self._plotSpeedStr = 'cm/min'
        self._plotBpmStr = 'bpm/cm'
        self.set_paper_eu()
        # self._plotSpeed = EnumPlotSpeed.oneCmMin
        # self._plotBpm = EnumPlotBpm.twentyBpmCm
        # self._plotSpeed = float(1)/float(EnumPlotSpeed.threeCmMin)
        # self._plotBpm = EnumPlotBpm.thirtyBpmCm
        # 1 cm/min * nFs * 60 sec * 5 min
        # self._nTickSamples = self._plotSpeed * self.__sampling_freq * 60 * 5

    def set_paper_speed(self, val):
        self._plotSpeed = val

    def set_paper_bpm(self, val):
        self._plotBpm = val

    def set_paper_bpm_major_tick(self, val):
        self._plotBpmMajorTick = val

    def set_paper_eu(self):
        self._paper_format = EnumPaperFormat.EU
        self._plotSpeed = EnumPlotSpeed.oneCmMin
        self._plotBpm = EnumPlotBpm.twentyBpmCm
        self.set_paper_bpm_major_tick(self._plotBpm)
        self.setYMinMax(50, 201)

    def set_paper_us(self):
        self._paper_format = EnumPaperFormat.US
        self._plotSpeed = float(1)/float(EnumPlotSpeed.threeCmMin)
        self._plotBpm = EnumPlotBpm.thirtyBpmCm
        self.set_paper_bpm_major_tick(self._plotBpm)
        self.setYMinMax(30, 241)

    def plot(self, x, y, timestring=None):
        """
        Plot data. Numpy arrays should be used instead of list, the plotting speed is about 20x faster.
        Time string is used for plotting time on X axis. Prior plotting either minutes or hours are located
        based on user preference.

        :param x: x axis values
        :param y: y axis values
        :param timestring: time strings for x axis labels
        :type x: numpy.array | list()
        :type y: numpy.array | list()
        :type timestring: list()
        """

        self._x = x
        self._y = y

        y[np.isnan(y)] = 0

        ind1 = y > self._minView
        ind2 = y < self._maxView
        ab_not_mask = np.logical_and(ind1, ind2)

        self.curve1 = MaskedCurve(x, y, ab_not_mask)
        self.curve1.attach(self)

        if timestring is not None:
            self._bPlotDatesXAxis = True
            self._timeString = timestring
            self.timeScale.setTimeString(timestring, self.__sampling_freq)
            # self.run_time_locator()
            self._time_tics_located = time_locator(timestring, self._locator_min, self._locator_hour,
                                                   int(self._x[-1]), self.__sampling_freq)
        else:
            self._bPlotDatesXAxis = False

        # #self.curve1.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        self.curve1.setPen(QtGui.QPen(Qt.Qt.black, 0, Qt.Qt.SolidLine))
        self.curve1.setYAxis(Qwt.QwtPlot.yLeft)
        # self.curve1.attach(self)

        self.setXAxis()

    def plot_first_stage_line(self, stage1pos_samp):
        """
        Plot the first stage of labour

        :param stage1pos_samp:
        :return:
        """
        meanline2 = Qwt.QwtPlotMarker()
        meanline2.setLineStyle(Qwt.QwtPlotMarker.VLine)
        meanline2.setLinePen(Qt.QPen(Qt.Qt.darkCyan, 4))

        meanline2.setXValue(stage1pos_samp)
        meanline2.attach(self)

    def plot_second_stage_line(self, stage2pos_samp):
        """
        Plot the second stage of labour

        :param stage2pos_samp:
        :return:
        """
        meanline = Qwt.QwtPlotMarker()
        meanline.setLineStyle(Qwt.QwtPlotMarker.VLine)
        meanline.setLinePen(Qt.QPen(Qt.Qt.darkBlue, 4))

        meanline.setXValue(stage2pos_samp)
        meanline.attach(self)

    def plot_bith_line(self, pos_samp):
        """
        Plot line indicating birth time

        :param pos_samp:
        :return:
        """
        meanline = Qwt.QwtPlotMarker()
        meanline.setLineStyle(Qwt.QwtPlotMarker.VLine)
        meanline.setLinePen(Qt.QPen(Qt.Qt.green, 4))

        meanline.setXValue(pos_samp)
        meanline.attach(self)

    def plot_ann_navplot_marker(self, bshow=True):

        # print 'length'
        # print len(self.d_ann_all_curves_navplot)

        if len(self.d_ann_all_curves_navplot) > 0:
            for key, curve in self.d_ann_all_curves_navplot.iteritems():
                # print key, curve
                curve.detach()

        self.d_ann_all_curves_navplot.clear()
        for key, curve in self.__d_ann_all_curves.iteritems():

            name = curve.get_parent_name()
            typ = curve.get_curve_type()

            if name == EnumAnnType.plot_toco:
                offset = ConfigStatic.plot_toco_offset
            else:
                offset = 0

            if typ == EnumAnnType.baseline or typ == EnumAnnType.recovery or typ == EnumAnnType.no_recovery \
                    or typ == EnumAnnType.excessive_ua or typ == EnumAnnType.acceleration \
                    or typ == EnumAnnType.deceleration or typ == EnumAnnType.uterine_contraction:
                c = PyQwtPlotCurveAnnotator(name, typ, curve.x_from, curve.x_to, curve.yval1-offset)

                self.__apply_nav_marker(c, bshow)

            elif typ == EnumAnnType.ellipsenote:
                c = PyQwtPlotEllipseAnnotator(name, typ, curve.x_from, curve.x_to,
                                              curve.yval1-offset, curve.yval2-offset, '')
                self.__apply_nav_marker(c, bshow)

            elif typ == EnumAnnType.note:
                c = PyQwtPlotMarkerAnnotator(name, typ, curve.x_from, curve.x_to, None, None, 'n')
                self.__apply_nav_marker(c, bshow)

        self.replot()

    def __apply_nav_marker(self, c, bshow=True):
        c.set_pen_symbol_light()
        self.d_ann_all_curves_navplot[c.id] = c

        if bshow is True:
            c.attach(self)
            c.plot()

    def ann_basal(self, y):

        #  only one basal allowed - return if a basal already present
        for key, curve in self.__d_ann_all_curves.iteritems():
            if curve.get_curve_type() == EnumAnnType.basal:
                return 0

        curve_basal = PyQwtPlotCurveAnnotator(self.__name, EnumAnnType.basal)
        nmin = int(min(self._minTime, self._x.min()))
        nmax = int(max(self._maxView, self._x.max()))
        curve_basal.set_xy_values(nmin, nmax, y)
        self.__d_ann_all_curves[curve_basal.id] = curve_basal
        self.signal_ann_changed.emit()
        self.ann_plot_curves()

    def ann_line_start(self, pos, en=EnumAnnType.baseline):
        curve = PyQwtPlotCurveAnnotator(self.__name, en)
        curve.set_xy_values(pos.x(), pos.x(), pos.y(), pos.y())
        self.ann_add(curve)
        return curve

    def ann_note(self, pos, s):
        """
        Add annotation type Note

        :param pos: x and y position
        :param s: text for annotation
        :type pos: QPointF
        :type s: str
        """
        note = PyQwtPlotMarkerAnnotator(self.__name, EnumAnnType.note, int(pos.x()), int(pos.x()), None, None, s=s)
        self.ann_add(note)

    def ann_ellipse(self, pos, curve_type=EnumAnnType.ellipsenote, s=''):
        """
        Add ellipse to a signal

        :param pos: x and y position
        :param curve_type: EnumAnnType
        :param s: text fo annotation
        :type pos: QPointF
        """
        ellipse = PyQwtPlotEllipseAnnotator(self.__name, curve_type, int(pos.x()), int(pos.x()), int(pos.y()), pos.y(), s)
        self.ann_add(ellipse)
        return ellipse

    def ann_evaluation_note(self, pos, s):
        """
        Add annotation type Evaluation Note

        :param pos: x and y position
        :param s: text for annotation
        :type pos: QPointF
        :type s: str
        """
        note = PyQwtPlotEvaluationNote(self.__name, EnumAnnType.evaluation_note, int(pos.x()), int(pos.x()), None, None, s)
        self.ann_add(note)

    def ann_floating_baseline(self, pos, en=EnumAnnType.floating_baseline):

        pos = self.ann_floating_baseline_outside_signal(pos)

        for key, curve in self.__d_ann_all_curves.iteritems():
            if isinstance(curve, PyQwtPlotFloatingBaseline):
                curve.add_point_xy(pos.x(), pos.y())
                curve.plot()
                self.replot()
                self.signal_ann_changed.emit()
                return curve

        curve = PyQwtPlotFloatingBaseline(self.__name, en)
        curve.add_point_xy(pos.x(), pos.y())
        self.ann_add(curve)
        return curve

    def ann_floating_baseline_outside_signal(self, pos):

        assert isinstance(pos, QtCore.QPoint) or isinstance(pos, QtCore.QPointF)

        if pos.x() < self.xAxisMinSample():
            pos.setX(self.xAxisMinSample())

        if pos.x() > self.xAxisMaxSample():
            pos.setX(self.xAxisMaxSample())

        return pos

    def ann_add(self, curve):
        """
        Add the annotation (curve) into dictionary of annotations and plot
        :param curve:
        :return:
        """

        self.__d_ann_all_curves[curve.id] = curve
        self.ann_plot_curves()
        self.signal_ann_changed.emit()

    def ann_plot_curves(self, bplot=True):
        """ Plot all annotations (basal, baseline, recovery, notes)
        The curve is an object inherited from Qwt library.
        Qwt thus performs the actual drawing
        """

        for key, curve in self.__d_ann_all_curves.iteritems():

            if bplot is True:  # and curve.get_curve_type() == EnumAnnType.floating_baseline:
                curve.attach(self)
                curve.plot()
            else:
                curve.detach()

        self.replot()

    def ann_delete_all(self, replot=True, emit_signal=True):
        """ Delete all annotations (basal, baseline, recovery, notes)

        :param replot: replot current plot
        :param emit_signal: emit signal that plot has changed
        :return:
        """

        for key, curve in self.__d_ann_all_curves.iteritems():
            curve.detach()

        for key, curve in self.d_ann_all_curves_navplot.iteritems():
            curve.detach()

        self.__d_ann_all_curves.clear()
        self.d_ann_all_curves_navplot.clear()

        if emit_signal:
            self.signal_ann_changed.emit()

        if replot:
            self.replot()

    def ann_delete_curve(self, curve):
        if curve.id in self.__d_ann_all_curves:
            del self.__d_ann_all_curves[curve.id]
            curve.detach()
            self.signal_ann_changed.emit()
            self.replot()

    def ann_set_and_plot(self, dann):
        self.ann_set(dann)
        self.ann_plot_curves()

    def ann_set(self, dann):
        self.__d_ann_all_curves = dann

    def ann_get(self):
        return self.__d_ann_all_curves

    def caliper_set_visible(self, bvisible=False):

        # print self.caliper
        # print self.caliper in self.itemList()

        if bvisible:
            self.caliper_outside_view()
            self.caliper.attach(self)
            self.caliper.plot()
        else:
            self.caliper.detach()

        self.replot()

    def caliper_is_visible(self):
        return self.caliper in self.itemList()

    def caliper_set_figo_acc_dec(self):

        ca = self.caliper
        ca.set_xy_values(ca.x_from, ca.x_from + 15 * self.__sampling_freq, ca.yval1, ca.yval1 + 15)
        self.caliper.plot()
        self.replot()

    def caliper_set_figo_ua(self):

        ca = self.caliper
        ca.set_xy_values(ca.x_from, ca.x_from + 45 * self.__sampling_freq, ca.yval1, ca.yval1 + 20)
        self.caliper.plot()
        self.replot()

    def caliper_outside_view(self):

        bx_left = self.caliper.x_to < self._minTime < self._maxTime
        bx_right = self.caliper.x_from > self._maxTime > self._minTime

        if bx_left:
            d = self._minTime - self.caliper.x_from
            self.caliper.x_from += d
            self.caliper.x_to += d

        if bx_right:
            d = self._maxTime - self.caliper.x_to
            self.caliper.x_from += d
            self.caliper.x_to += d

    def caliper_reset(self, breplot=True):
        self.caliper.reinit()
        self.caliper.plot()
        self.replot()

    def plotTemp(self, x, y):
        """
        Temporary code showing how to plot an additional line
        """
        # curve = Qwt.QwtPlotCurve()
        abnotmask = np.logical_and(y > self._minView, y < self._maxView)
        curve = MaskedCurve(x, y, abnotmask)
        curve.setPen(Qt.QPen(Qt.Qt.darkRed, 2))
        curve.setStyle(Qwt.QwtPlotCurve.Steps)

        # curve.setData(x, y)

        curve.attach(self)

#         self.titles.append('Style: NoCurve, Symbol: XCross')
#         curve = Qwt.QwtPlotCurve()
#         curve.setStyle(Qwt.QwtPlotCurve.NoCurve)
#         curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.XCross,
#                                       Qt.QBrush(),
#                                       Qt.QPen(Qt.Qt.darkMagenta),
#                                       Qt.QSize(5, 5)))

    def set_locator_minute(self, interval):
        self._locator_min = interval
        self._locator_hour = -1

    def set_locator_hour(self, interval):
        self._locator_min = -1
        self._locator_hour = interval

    # def run_time_locator(self):
    #     """
    #     Locates time points at the X axis. The points could be minutes or hours.
    #     If both equal to -1 the time is guessed.
    #     """
    #
    #     if self._timeString is None:
    #         self._log.warning("Time string used of X axis is None")
    #         return
    #
    #     bminute_locator = False
    #     bhour_locator = False
    #
    #     if not self._locator_min == -1:
    #         bminute_locator = True
    #         interval_time = self._locator_min
    #         ninterval_samples = self.__sampling_freq * 60
    #         arange = range(0, 59, interval_time)
    #
    #     elif not self._locator_hour == -1:
    #         bhour_locator = True
    #         interval_time = self._locator_hour
    #         ninterval_samples = self.__sampling_freq * 3600
    #         arange = range(0, 24, interval_time)
    #     else:
    #         # guess range for hours locator
    #         qfirst_time = QtCore.QTime.fromString(self._timeString[0], "hh:mm:ss:zzz")
    #         qlast_time = QtCore.QTime.fromString(self._timeString[-1], "hh:mm:ss:zzz")
    #         qdiff_time = qlast_time.hour() - qfirst_time.hour()
    #
    #         # interval time based on signal length
    #         if qdiff_time > 120:
    #             interval_time = 0
    #         elif qdiff_time > 48:
    #             interval_time = 6
    #         elif qdiff_time > 24:
    #             interval_time = 2
    #         else:
    #             interval_time = 1
    #
    #         bhour_locator = True
    #         ninterval_samples = self.__sampling_freq * 3600
    #         arange = range(0, 24, interval_time)
    #
    #     nlastsample = int(self._x[-1])
    #     qfirst_time = QtCore.QTime.fromString(self._timeString[0], "hh:mm:ss:zzz")
    #
    #     # find the first xtick of axis
    #     t = 0
    #     startsample = 0
    #     while t < nlastsample:
    #         qtime = qfirst_time.addMSecs(1000 * t / self.__sampling_freq)
    #         if bhour_locator:
    #             if (qtime.hour() in arange) & (qtime.minute() == 0) & (qtime.second() == 0) & (qtime.msec() == 0):
    #                 startsample = t
    #                 break
    #
    #         elif bminute_locator:
    #             if (qtime.minute() in arange) & (qtime.second() == 0) & (qtime.msec() == 0):
    #                 startsample = t
    #                 break
    #
    #         t += 1
    #
    #     # compute ticks
    #     value = startsample
    #     while value < nlastsample:
    #
    #         if not value in self._time_tics_located:
    #             self._time_tics_located.append(value)
    #
    #         # update for next iteration
    #         value += interval_time * ninterval_samples

    def ylabel(self, text=""):
        """ set the y axis label. The font is based on application font """
        font = self._font_app
        font.setBold(True)
        qtext = Qwt.QwtText(text)
        qtext.setFont(font)
        self.setAxisTitle(Qwt.QwtPlot.yLeft, qtext)

    def xlabel(self, text=""):
        """ set the x axis label """
        self.setAxisTitle(Qwt.QwtPlot.xBottom, text)

    def xAxisMinSample(self):
        return self._x[0]

    def xAxisMaxSample(self):
        return self._x[-1]

    def setYMinMax(self, miny, maxy):
        self._min_view_paper_lim = self._minView = miny
        self._max_view_paper_lim = self._maxView = maxy

    def setYAxisTick(self):

        offset = 0
        if self._paper_format == EnumPaperFormat.EU:
            offset = 10

        self._yAxisTicksMajor = range(self._min_view_paper_lim + offset, self._max_view_paper_lim, self._plotBpmMajorTick)
        self._yAxisTicksMedium = range(self._min_view_paper_lim, self._max_view_paper_lim, 10)

    def viewYMaxSample(self):
        return self._maxView

    def viewYMinSample(self):
        return self._minView

    def viewXMaxSample(self):
        """
        Returns maximum of x axis for current view (display)
        """
        return self._maxTime

    def viewXMinSample(self):
        return self._minTime

    def xAxisEnabled(self, benabled):
        self.enableAxis(Qwt.QwtPlot.xBottom, benabled)

    def yAxisEnabled(self, benabled):
        self.enableAxis(Qwt.QwtPlot.yLeft, benabled)

    def plotSpeed(self):
        return self._plotSpeed

    def plotBpm(self):
        return self._plotBpm

    def plotSpeedStr(self):
        return self._plotSpeedStr

    def plotBpmStr(self):
        return self._plotBpmStr

    def getMarginsYPx(self):
        """
        Get margins of y axis of current plot - length (in pixels) between end of an axis and
        end of plot widget.

        :return: returns margins of current plot (in pixels)
        :rtype: int,int
        """
        return self._getMarginsPx(Qwt.QwtPlot.yLeft)

    def getMarginsXPx(self):
        """
        Get margins of x axis of this plot - length (in pixels) between end of an axis and
        end of plot widget.

        :rtype: int,int
        """
        p1, p2 = self._getMarginsPx(Qwt.QwtPlot.xBottom)
        return p2, p1

    def _getMarginsPx(self, naxisid):
        """
        Get margins of this plot - length (in pixels) between end of an axis and
        end of plot widget. The size of plot in pixels is equal to p1() - p2()

        :param naxisid: id of axis
        :type  naxisid: QwtPlot.Axis
        :rtype: int,int
        """
        canvasmap = self.canvasMap(naxisid)
        return canvasmap.p2(), canvasmap.p1()

    def size_plot_area(self):
        """
        Return  sizeof canvas, i.e. the size of actual plot. When this class is initialized
        use build in function QWidget.size() instead of :py:func:`getMarginsXPx`

        :rtype: QSize(width, height)
        """
        minpx, maxpx = self.getMarginsXPx()
        w = maxpx - minpx

        minpx, maxpx = self.getMarginsYPx()
        h = maxpx - minpx

        return QtCore.QSize(w, h)

    def setXAxisScale(self, x1, x2):
        self.setAxisScale(Qwt.QwtPlot.xBottom, x1, x2, 0)

    def xAxisViewMaxSample(self):
        """
        Returns a maximum sample that will be plotted. The calculation of max samples is based
        on preset dpi and bpm/cm ratio

        :rtype: int
        """

        width = self.size_plot_area().width()
        fs = self.__sampling_freq
        # nFs*60sec = pocet vzorku za 1 minutu
        xAxisSamp = fs*60*self._plotSpeed*(width/self._dpi2px)
        return xAxisSamp

    def setXAxis(self, center_point=None, breplot=True):
        """
        Set scale of X axis.  First get width of this plot. Then use preset cm/min
        ratio and use it to compute X axis scale.

        :param center_point: user's clicked point at :py:mod:`PyQwtNavigationPlot`
        :param breplot: boolean replot
        :type  center_point: int
        """
        x_ax_samp = self.xAxisViewMaxSample()

        if center_point is not None:
            self._centerPoint = center_point

        self._minTime = self._centerPoint - x_ax_samp/2
        self._maxTime = self._centerPoint + x_ax_samp/2

        # if data are available
        if self.curve1.dataSize() > 0:

            # if user clicked near begin or end of a signal
            if x_ax_samp >= (self.xAxisMinSample() + self.xAxisMaxSample()):
                self._minTime = self.xAxisMinSample()
                self._maxTime = self.xAxisMaxSample()
            else:
                if self._minTime < self.xAxisMinSample():
                    self._maxTime += -1*self._minTime
                    self._minTime = self.xAxisMinSample()

                if self._maxTime > self.xAxisMaxSample():
                    self._minTime -= self._maxTime - self.xAxisMaxSample()
                    self._maxTime = self.xAxisMaxSample()

        if self.DEBUG_X_AXIS_SIZE:
            print 'minTimeMinutes {0}'.format(self._minTime)
            print 'maxTimeMin_Samples {0}'.format(x_ax_samp)
            print 'maxTimeMinutes {0}'.format(self._maxTime)

        if not self._bPlotDatesXAxis:
            # nFs = self.__sampling_freq
            # self._nTickSamples = self._plotSpeed * nFs * 60 * 5
            self.setAxisScale(Qwt.QwtPlot.xBottom, self._minTime, self._maxTime , 0)

        else:
            # pokud zalozim novy objekt QwtScaleDiv() musim pouzit konstruktor, kde se nastavuji parametry
            # jinak bude vzdt scaleDiv false
            scalediv = self.axisScaleDiv(Qwt.QwtScaleDiv.MajorTick)
            # print scaleDiv.isValid()
            scalediv.setTicks(Qwt.QwtScaleDiv.MajorTick, self._time_tics_located)
            scalediv.setTicks(Qwt.QwtScaleDiv.MinorTick, [])
            scalediv.setTicks(Qwt.QwtScaleDiv.MediumTick, [])
            scalediv.setInterval(self._minTime, self._maxTime)
            self.setAxisScaleDiv(Qwt.QwtPlot.xBottom, scalediv)
            # print self.axisScaleDiv(Qwt.QwtScaleDiv.MajorTick).ticks(Qwt.QwtScaleDiv.MajorTick)
            # print self.axisScaleDiv(Qwt.QwtScaleDiv.MajorTick).ticks(Qwt.QwtScaleDiv.MinorTick)

        if breplot:
            self.replot()

    def findClosestXPoint(self, point, nDirection = None):
        """
        Not used so far.
        """
        nDiff = self._x[-1]
        nCount = 0
        for x in self._x:

            nCount += 1
            if nDirection == -1:
                nDiff = x - point
                if nDiff > 0:
                    return nCount-2
            else:
                nDiff = point - x
                if nDiff < 0:
                    return nCount

    def setYAxis(self, height=None, bReplot=True):
        """
        Set scale of Y axis.  First get height of this plot. Then use preset bmp/cm
        ratio and use it to compute y axis scale

        :param height: height of the widget
        :type  height: int
        """

        if height is None:
            height = self.size_plot_area().height()

        y_ax = self._plotBpm * (float(height)/self._dpi2px)
        self._maxView = self._minView + y_ax

        if self.DEBUG_Y_AXIS_SIZE:
            print '_minView {0}'.format(self._minView)
            print '_maxView {0}'.format(self._maxView)

        self.setAxisScale(Qwt.QwtPlot.yLeft, self._minView, self._maxView, 0)
        self.setYAxisTick()

        #self._yAxisTicks = range(60,220,20)
        #self._yAxisTicksMin = range(50,210,20)

        # pokud zalozim novy objekt QwtScaleDiv() musim pouzit konstruktor, kde se natavuji parametry
        scaleDiv = self.axisScaleDiv(Qwt.QwtScaleDiv.MajorTick)
        #print scaleDiv.isValid()
        scaleDiv.setTicks(Qwt.QwtScaleDiv.MajorTick, self._yAxisTicksMajor)
        scaleDiv.setTicks(Qwt.QwtScaleDiv.MinorTick, [])
        scaleDiv.setTicks(Qwt.QwtScaleDiv.MediumTick, self._yAxisTicksMedium)
        scaleDiv.setInterval(self._minView, self._maxView)
        self.setAxisScaleDiv(Qwt.QwtPlot.yLeft, scaleDiv)

        if bReplot:
            self.replot()

    def updateAxis(self):
        """
        Update X and Y axis. Replot after both axes were set.
        """
        self.setYAxis(None, False)
        self.setXAxis(None, False)
        self.replot()

    # def samples2time(self, nr_samples, fs, time_begin=Qt.QString("00:00:00:000")):
    #
    #     sformat = "hh:mm:ss:zzz"
    #     qtime = QtCore.QTime.fromString(time_begin, sformat)
    #     ms = 1000 / fs
    #     atime = list()
    #
    #     for dummy in range(0, nr_samples):
    #         qtime = qtime.addMSecs(ms)
    #         atime.append(qtime.toString(sformat))
    #
    #     return atime


class MaskedData(Qwt.QwtArrayData):

    def __init__(self, x, y, mask):
        Qwt.QwtArrayData.__init__(self, x, y)
        self.__mask = np.asarray(mask, bool)
        # keep a copy of x and y for boundingRect()
        self.__x = np.asarray(x)
        self.__y = np.asarray(y)

    # __init__()

    def copy(self):
        return self

    def mask(self):
        return self.__mask

    def boundingRect(self):
        """Return the bounding rectangle of the data, accounting for the mask.
        """
        xmax = self.__x[self.__mask].max()
        xmin = self.__x[self.__mask].min()
        ymax = self.__y[self.__mask].max()
        ymin = self.__y[self.__mask].min()

        return Qt.QRectF(xmin, ymin, xmax-xmin, ymax-ymin)


class MaskedCurve(Qwt.QwtPlotCurve):

    def __init__(self, x, y, mask):
        Qwt.QwtPlotCurve.__init__(self)
        self.setData(MaskedData(x, y, mask))

    def draw(self, painter, xMap, yMap, rect):
        """
        # When the array indices contains the indices of all valid data points,
        # a chunks of valid data is indexed by
        # indices[first], indices[first+1], .., indices[last].
        # The first index of a chunk of valid data is calculated by:
        # 1. indices[i] - indices[i-1] > 1
        # 2. indices[0] is always OK
        # The last index of a chunk of valid data is calculated by:
        # 1. index[i] - index[i+1] < -1
        # 2. index[-1] is always OK
        """

        indices = np.arange(self.data().size())[self.data().mask()]

        # if indices.shape[0] == 0:
        #     Qwt.QwtPlotCurve.drawFromTo(self, painter, xMap, yMap, 0, len(self.data().mask()))
            # return

        fs = np.array(indices)
        fs[1:] -= indices[:-1]
        # print fs
        # print len(fs)
        fs[0] = 2
        fs = indices[fs > 1]
        ls = np.array(indices)
        ls[:-1] -= indices[1:]
        ls[-1] = -2
        ls = indices[ls < -1]
        for first, last in zip(fs, ls):
            Qwt.QwtPlotCurve.drawFromTo(self, painter, xMap, yMap, first, last)


class TimeScaleDraw(Qwt.QwtScaleDraw):
    """
    Subclass of QwtScaleDraw because of time axis. Note: function axisScaleDiv will
    invalidate manually set ticks.

    :param plot: parent
    :type  plot: :py:mod:`PyQwtWidgetGui`
    """

    # COLORS
    # myplot->axisWidget (QwtPlot::xBottom)->setPalette (palette).

    # QwtScaleWidget *qwtsw = myqwtplot.axisWidget(QwtPlot::xBottom);
    # QPalette palette = qwtsw->palette();
    # palette.setColor( QPalette::WindowText, Qt::gray); // for ticks
    # palette.setColor( QPalette::Text, Qt::gray); // for ticks' labels
    # qwtsw->setPalette( palette );

    def __init__(self, plot):
        Qwt.QwtScaleDraw.__init__(self)
        self._plot = plot
        self._timeFirst = QtCore.QTime()
        self._timeString = list()
        self._fs = self._plot.get_sampling_freq()

    def setTimeString(self, timeString, fs):
        """
        Set a time string used for X axis.

        :param timeString: list of time strings, e.g ['11:41:50','11:41:51']
        :param fs: sampling frequency
        :type  timeString: list()
        """
        self._timeString = timeString
        self._timeFirst = QtCore.QTime.fromString(timeString[0], "hh:mm:ss:zzz")
        self._fs = fs

    def getTimeString(self):
        """
        Get a time axis.

        :rtype: list()
        """
        return self._timeString

    def label(self, axisValue):
        # print str(axisValue)

        if not self._plot._bPlotDatesXAxis:
            return Qwt.QwtText(str(int(axisValue)))
        else:
            remaindermsecs = axisValue/self._fs - int(axisValue) / self._fs
            qtime = self._timeFirst.addSecs(int(axisValue) / self._fs)
            qtime = qtime.addMSecs(1000*remaindermsecs+1)
            # print "value {0}, qtime {1}".format(int(axisValue),qTime)

            return Qwt.QwtText(qtime.toString("hh:mm"))


class AxisYScaleDraw(Qwt.QwtScaleDraw):
    """
    Subclass of QwtScaleDraw because of time axis.
    """

    def __init__(self, parent):
        Qwt.QwtScaleDraw.__init__(self)
        self.parent = parent
        self._fontMetrics = QtGui.QFontMetrics(QtGui.QFont())
        self._max_w = 20

    def label(self, axis_value):

        s = QtCore.QString(str(int(axis_value)))

        # doplnuji string podle pozadovane sirky
        while self._fontMetrics.width(s) <= self._max_w:
            s = ' '+s

        # s = '{:>8}'.format(axis_value) # tohle nefunguje protoze mezera ma jinou sirku nez cislo
        # print self._fontMetrics.width(s)

        return Qwt.QwtText(s)


class StanPaper:

    def __init__(self, red=0, green=0, blue=0, nmin=0, nmax=0):

        self.pen_color = QtGui.QColor(red, green, blue)
        self.pen_color.setAlpha(80)

        self.min = nmin
        self.max = nmax


class PyQwtFhrPlotDraw(Qwt.QwtPlotCurve):
    """
    PyQwtFhrPlotDraw
    ---------------
    The PyQwtFhrPlotDraw draw the CTG paper (similar to paper used in STAN machines)

    :param parent: pointer to parent
    """

    def __init__(self, parent):
        Qwt.QwtPlotCurve.__init__(self)

        self.__plot = parent

        patol1 = StanPaper(255, 160, 160, 30, 80)  # (red, green, blue, min, max)
        patol2 = StanPaper(255, 160, 160, 180, 240)
        susp1 = StanPaper(255, 255, 120, 80, 110)
        susp2 = StanPaper(255, 255, 120, 150, 180)
        gray1 = StanPaper(190, 190, 190, 0, 30)
        gray2 = StanPaper(190, 190, 190, 240, 500)
        self._allSettings = list()
        self._allSettings.append(patol1)
        self._allSettings.append(patol2)
        self._allSettings.append(susp1)
        self._allSettings.append(susp2)
        self._allSettings.append(gray1)
        self._allSettings.append(gray2)

    def drawFromTo(self, painter, xMap, yMap, start, stop):
        """
        Draws rectangles (for the CTG paper)
        This function is called automatically

        :param painter:
        :param xMap:
        :param yMap:
        :param start:
        :param stop:
        :type  painter: QtGui.QPainter
        """
        xminmarginpx, dummy = self.__plot.getMarginsXPx()
        px1 = xMap.transform(self.__plot.viewXMinSample()) - xminmarginpx
        px2 = xMap.transform(self.__plot.viewXMaxSample()) + 2*xminmarginpx

        # draw for all backgrounds
        for c in self._allSettings:
            painter.setPen(Qt.QPen(c.pen_color, 1))
            painter.setBrush(c.pen_color)
            py2 = yMap.transform(c.min)
            py1 = yMap.transform(c.max)
            painter.drawRect(px1, py1, px2 - px1, py2 - py1)


class FhrPlot(PyQwtWidgetGui):

    def __init__(self, parent=None):
        PyQwtWidgetGui.__init__(self, parent, EnumAnnType.plot_fhr)

        self._parent = parent
        self._timeString = None
        # self.curve1.setPen(QPen(Qt.Qt.black))
        self.setYMinMax(50, 210)
        self.ylabel("FHR [bpm]")
        self.xlabel("")
        self.xAxisEnabled(False)
        self.set_locator_minute(1)
        self.reinit()

        # annotations
        # self.annotator = AnnotatorHelper(self)
        self.canvas_picker = CanvasPickerAnnotator(self)
        self.canvas_picker.signal_ann_moved.connect(self.ann_moved)

        self.signal_plot_cleared.connect(self.reinit)

    def reinit(self):
        self._log.info('FHR plot reinit')
        self._fhrDraw = PyQwtFhrPlotDraw(self)
        self._fhrDraw.attach(self)

    def ann_moved(self):
        self.signal_ann_changed.emit()


class TocoPlot(PyQwtWidgetGui):

    def __init__(self, parent=None):
        PyQwtWidgetGui.__init__(self, parent, EnumAnnType.plot_toco)

        self.set_paper_bpm(40)
        self.setYMinMax(-10, 110)
        self.ylabel("UC [a.u.]")
        self.xlabel("")
        color = QtGui.QColor(230, 230, 230)
        self.setCanvasBackground(color)
        self.set_locator_minute(1)
        self._height = 150
        self.setMaximumHeight(self._height)

        self.canvas_picker = CanvasPickerAnnotator(self)
        self.canvas_picker.signal_ann_moved.connect(self.ann_moved)

    def set_paper_eu(self):
        self._plotSpeed = EnumPlotSpeed.oneCmMin

    def set_paper_us(self):
        self._plotSpeed = float(1)/float(EnumPlotSpeed.threeCmMin)

    def ann_moved(self):
        self.signal_ann_changed.emit()


class DebugPyQwtWidgetGui(QtGui.QWidget):
    """
    Class intended only for debugging
        * parent
    """

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        # musim importovat tady, jinak mam kruhovou zavislost
        from PyQwtNavigationPlot import PyQwtNavigationPlot
        from LoadWriteData import LoadData
        # from StyleManager import styleManager
        # from PyQwtPlotTools import PyQwtPlotTools

        self.setMinimumSize(800, 500)

        # self._styleManager = styleManager()
        # self._styleManager.setStyleManager(self._styleManager)

        vbox = QtGui.QVBoxLayout()

        controled_plots = list()
        self.fhrPlot = FhrPlot(self)
        self.tocoPlot = TocoPlot(self)
        # self.tocoPlot.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

        controled_plots.append(self.fhrPlot)
        controled_plots.append(self.tocoPlot)
        self.navPlot = PyQwtNavigationPlot(self, controled_plots)

        # self.navPlot = PyQwtNavigationPlot(self,controledPlots)
        # self.plotTools = PyQwtPlotTools(self, self.fhrPlot, self._styleManager)
        # self.plot.setMargin(5)

        vbox.addWidget(self.fhrPlot)
        vbox.addWidget(self.tocoPlot)
        # vbox.addLayout(self.plotTools.ToolbarHBoxLayout)
        vbox.addWidget(self.navPlot)

        self.setLayout(vbox)

        self._dataLoader = LoadData()
        file1 = 'files/1001.dat'

        # l = self._dataLoader.readPhysionetHeader(file2)
        adata, dummy = self._dataLoader.read_physionet_signal16(file1)

        # dictClinInfo = lHeader[2]
        # print dictClinInfo['Pos_IIst']

        fhr = adata[EnumVariableName.fhr]
        toco = adata[EnumVariableName.uc]
        time_string = samples2time(len(fhr), 4)
        time_samp = adata['time_samp']
        # timeStamp_samp = aData[:,2]*4

        self.fhrPlot.plot(time_samp,fhr, time_string)
        self.tocoPlot.plot(time_samp, toco, time_string)
        self.navPlot.plot(time_samp, fhr, time_string)

        # self.fhrPlot.clearPlot()
        # self.tocoPlot.clearPlot()
        # self.navPlot.clearPlot()

    def updatePlots(self):
        self.fhrPlot.updateAxis()
        self.tocoPlot.updateAxis()
        self.navPlot.setXAxis()

    def resizeEvent(self, ev):
        self.updatePlots()
        # self.fhrPlot.updateAxis()


def main():
    app = Qt.QApplication(sys.argv)
    window = DebugPyQwtWidgetGui()
    window.show()
    window.updatePlots()
    sys.exit(app.exec_())

if __name__ == '__main__':
    if DEBUG_PROFILE:
        cProfile.run('main()', 'profile_data')
        p = pstats.Stats('profile_data')
        p.sort_stats('time').print_stats(20)
        p.sort_stats('cumulative').print_stats(20)
    else:
        main()
