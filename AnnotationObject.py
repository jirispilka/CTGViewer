# -*- coding: utf-8 -*-
#
# Created on Apr 13, 2016
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2016, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

"""
AnnotationObject
----------------

Reference
~~~~~~~~~

.. autoclass:: AnnotationObject
    :members:

.. autoclass:: PyQwtPlotCurveAnnotator
    :members:

.. autoclass:: PyQwtPlotMarkerAnnotator
    :members:

.. autoclass:: PyQwtPlotEllipseAnnotator
    :members:

.. autoclass:: PyQwtPlotFloatingBaseline
    :members:

"""

from PyQt4.Qwt5 import Qwt
from PyQt4 import QtGui, Qt, QtCore
from Enums import EnumAnnType
from Config import ConfigStatic

import numpy as np
import itertools
import textwrap


class AnnotationObject(object):
    """
    The AnnotationObject is predecessor object that implements several functions that are in common for
    various types of annotation objects.
    """

    newid = itertools.count().next

    def __init__(self, parent_name='', curve_type=None, x1=None, x2=None, y1=None, y2=None, s=''):

        self.id = AnnotationObject.newid()

        # information to be saved in annotation file
        self.__parent_name = parent_name
        self.__curve_type = curve_type
        self.x_from = x1
        self.x_to = x2
        self.yval1 = y1
        self.yval2 = y2
        self.valid = True  # if a curve is valid and should be plotted
        self.text = Qwt.QwtText(self.text_wrap(str(s)))

        self.__too_small_limit = 0

        self.font_app = QtGui.QFont()

        # QPen settings
        self.pen_def = Qt.QPen()
        self.pen_symbol = Qt.QPen()
        self.symbol = Qwt.QwtSymbol()

        self.__default_pen = Qt.QPen()
        self.color_highlight = Qt.Qt.darkMagenta

    def get_default_pen(self):
        return self.__default_pen

    def set_default_pen(self):
        self.__default_pen = Qt.QPen(self.pen_def)

    def get_symbol(self):
        return self.symbol

    def get_symbol_highlight(self):
        symbol = Qwt.QwtSymbol(self.symbol)
        pen = Qt.QPen(self.pen_symbol)
        pen.setColor(self.color_highlight)
        symbol.setPen(pen)
        symbol.setBrush(Qt.QBrush(self.color_highlight))  # new 2016-07-14
        return symbol

    def get_color_highlight(self):
        return self.color_highlight

    def get_curve_type(self):
        return self.__curve_type

    def get_parent_name(self):
        return self.__parent_name

    def define_pen(self, color=Qt.Qt.gray, width=4, line=Qt.Qt.SolidLine):
        self.pen_def = Qt.QPen(color)
        self.pen_def.setWidth(width)
        self.pen_def.setStyle(line)

    def define_pen_symbol(self, c=Qt.Qt.black, w=4, l=Qt.Qt.SolidLine):
        self.pen_symbol = Qt.QPen(c)
        self.pen_symbol.setWidth(w)
        self.pen_symbol.setStyle(l)

    def define_symbol(self, s=Qwt.QwtSymbol.VLine, c=Qt.Qt.black, qsize=Qt.QSize(15, 15)):
        self.symbol = Qwt.QwtSymbol(s, Qt.QBrush(c), self.pen_symbol, qsize)

    def define_pen_symbol_light(self):
        c = self.pen_def.color()
        c.setAlpha(120)
        self.pen_def.setColor(c)
        self.pen_def.setWidth(3)
        self.pen_symbol.setWidth(3)
        self.pen_symbol.setColor(c)
        # st = self.symbol.style()
        self.define_symbol(Qwt.QwtSymbol.VLine, c, Qt.QSize(7, 7))

    def set_xy_values(self, x1, x2, y1=None, y2=None):
        self.x_from = x1
        self.x_to = x2
        self.yval1 = y1
        self.yval2 = y2

    def correct_val_order(self):

        if self.x_from > self.x_to:
            self.x_from, self.x_to = self.x_to, self.x_from

        if self.yval1 > self.yval2:
            self.yval1, self.yval2 = self.yval2, self.yval1

    def correct_y1_y2(self):
        """
        Basal, baseline, Recovery, No-recovery, Uterine contraction should have the same y1 adn y2 value
        """
        if not self.yval1 == self.yval2:
            self.yval2 = self.yval1

    def is_too_small(self):

        if self.__too_small_limit == 0:
            return False
        else:
            return abs(self.x_to - self.x_from) < self.__too_small_limit

    @staticmethod
    def text_wrap(s):
        w = 200
        s = s.replace('\n', ' ')
        s = textwrap.fill(s, w / 8 + 1)
        return s

    def get_text(self):
        return str(self.text.text())

    def set_text(self, s):
        self.text.setText(s)

    def set_text_property(self):
        c = Qt.QColor(Qt.Qt.black)
        self.text.setColor(c)
        c.setAlpha(20)
        self.text.setBackgroundBrush(c)

        # c2 = Qt.QColor(Qt.Qt.black)
        # pen = Qt.QPen()
        # pen.setColor(c2)
        # self.text.setBackgroundPen(pen)

        self.font_app.setBold(False)
        self.text.setFont(self.font_app)

    def set_too_small_limit(self, val):
        self.__too_small_limit = val


class PyQwtPlotCurveAnnotator(AnnotationObject, Qwt.QwtPlotCurve):
    """
    Definitions for basal heart rate, baseline, recovery, and no recovery
    """

    def __init__(self, parent_name='', curve_type=None, x1=None, x2=None, y1=None, y2=None, s=''):

        super(AnnotationObject, self).__init__()
        AnnotationObject.__init__(self, parent_name, curve_type, x1, x2, y1, y2, s)
        Qwt.QwtPlotCurve.__init__(self)

        self.set_too_small_limit(1)

        if curve_type == EnumAnnType.basal:
            c = Qt.QColor(Qt.Qt.gray)
            c.setAlpha(200)
            self.define_pen(c, 4)
            c.setAlpha(0)  # invisible symbol
            self.define_pen_symbol(c)
            self.define_symbol()

        elif curve_type == EnumAnnType.baseline:
            self.define_pen(Qt.Qt.blue, 4, Qt.Qt.DotLine)
            self.define_pen_symbol(Qt.Qt.blue)
            self.define_symbol(Qwt.QwtSymbol.VLine, Qt.Qt.blue)

        elif curve_type == EnumAnnType.recovery:
            self.define_pen(Qt.Qt.green)
            self.define_pen_symbol(Qt.Qt.green)
            self.define_symbol(Qwt.QwtSymbol.VLine, Qt.Qt.green)

        elif curve_type == EnumAnnType.no_recovery:
            self.define_pen(Qt.Qt.red)
            self.define_pen_symbol(Qt.Qt.red)
            self.define_symbol(Qwt.QwtSymbol.VLine, Qt.Qt.red)

        elif curve_type == EnumAnnType.excessive_ua:
            self.define_pen(Qt.Qt.red, 4, Qt.Qt.DotLine)
            self.define_pen_symbol(Qt.Qt.red)
            self.define_symbol(Qwt.QwtSymbol.VLine, Qt.Qt.red)

        elif curve_type == EnumAnnType.acceleration:
            self.define_pen(Qt.Qt.darkGreen, 4, Qt.Qt.SolidLine)
            self.define_pen_symbol(Qt.Qt.darkGreen, 2)
            self.define_symbol(Qwt.QwtSymbol.Triangle, Qt.Qt.darkGreen)
            self.set_too_small_limit(0) # this allows to put only symbol without connecting line

        elif curve_type == EnumAnnType.deceleration:
            self.define_pen(Qt.Qt.magenta, 4, Qt.Qt.SolidLine)
            self.define_pen_symbol(Qt.Qt.magenta, 2)
            self.define_symbol(Qwt.QwtSymbol.DTriangle, Qt.Qt.magenta)
            self.set_too_small_limit(0)

        elif curve_type == EnumAnnType.uterine_contraction:
            self.define_pen(Qt.Qt.red, 3, Qt.Qt.SolidLine)
            self.define_pen_symbol(Qt.Qt.red, 2)
            self.define_symbol(Qwt.QwtSymbol.Triangle, Qt.Qt.red)
            self.set_too_small_limit(0)

        else:
            raise Exception('Do not use PyQwtPlotCurveAnnotator for this type of curve')

        self.set_default_pen()
        self.setPen(self.pen_def)
        self.setSymbol(self.symbol)

    def copy(self):
        pn = self.get_parent_name()
        t = self.get_curve_type()
        return PyQwtPlotCurveAnnotator(pn, t, self.x_from, self.x_to, self.yval1, self.yval2, self.get_text())

    def correct_val_order(self):

        if self.x_from > self.x_to:
            self.x_from, self.x_to = self.x_to, self.x_from

    def set_pen_symbol_light(self):
        self.define_pen_symbol_light()
        self.setPen(self.pen_def)
        self.setSymbol(self.symbol)

    def plot(self):
        x = [self.x_from, self.x_to]
        y = self.yval1 * np.ones((len(x), 1), float)

        self.setData(x, y)

    def plot_xy(self, x1, x2, y1, y2=None):
        x = [x1, x2]
        y1 = y1 * np.ones((len(x), 1), float)

        self.setData(x, y1)

    def draw_my(self, x, y):
        self.draw(x, y)


class PyQwtPlotMarkerAnnotator(AnnotationObject, Qwt.QwtPlotMarker):
    """
    Definition of annotation box. This class is base class for note.
    """

    def __init__(self, parent_name='', curve_type=None, x1=None, x2=None, y1=None, y2=None, s=''):
        super(AnnotationObject, self).__init__()
        AnnotationObject.__init__(self, parent_name, curve_type, x1, x2, y1, y2, s)
        Qwt.QwtPlotMarker.__init__(self)

        if curve_type == EnumAnnType.note:

            self.setLineStyle(Qwt.QwtPlotMarker.VLine)
            self.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)

            c = Qt.QColor(Qt.Qt.black)
            c.setAlpha(30)
            self.define_pen(c, 3)
            self.setLinePen(self.pen_def)

            self.set_text_property()
            self.pdf_alpha_rect = 0.08
            self.pdf_alpha_line = 0.1
        else:
            raise Exception('Do not use PyQwtPlotMarkerAnnotator for this type of curve')

        self.set_default_pen()
        self.setPen(self.pen_def)
        self.setSymbol(self.symbol)

    def copy(self):
        pn = self.get_parent_name()
        t = self.get_curve_type()
        return PyQwtPlotMarkerAnnotator(pn, t, self.x_from, self.x_to, self.yval1, self.yval2, self.get_text())

    def define_pen_symbol_light(self):
        c = self.pen_def.color()
        c.setAlpha(60)
        self.pen_def.setColor(c)
        self.pen_def.setWidth(2)
        self.define_symbol(Qwt.QwtSymbol.VLine, c, Qt.QSize(7, 7))

        f = QtGui.QFont(self.font_app)
        f.setPointSize(self.font_app.pointSize() - 2)
        self.text.setFont(f)

    def set_pen_symbol_light(self):
        self.define_pen_symbol_light()
        self.setPen(self.pen_def)

    def correct_val_order(self):
        """ Not used """
        pass

    def correct_y1_y2(self):
        """ Not used """
        pass

    def plot(self):
        self.setLabel(self.text)
        self.setValue(self.x_from, 0)

    def plot_xy(self, x1, x2=None, y1=None, y2=None):
        self.setValue(x1, 0)

    def setPen(self, pen):
        self.setLinePen(pen)

    def draw_my(self, x=None, y=None):
        """auxially function"""
        self.plot()


class PyQwtPlotEllipseAnnotator(AnnotationObject, Qwt.QwtPlotCurve):
    """
    Definitions for an ellipse
    """
    newid = itertools.count().next

    def __init__(self, parent_name='', curve_type=None, x1=None, x2=None, y1=None, y2=None, s=''):
        super(AnnotationObject, self).__init__()
        AnnotationObject.__init__(self, parent_name, curve_type, x1, x2, y1, y2, s)
        Qwt.QwtPlotCurve.__init__(self)
        self.set_too_small_limit(100)

        if curve_type == EnumAnnType.ellipse or curve_type == EnumAnnType.ellipsenote:
            self.define_pen(Qt.Qt.blue, 3, Qt.Qt.SolidLine)
            self.define_pen_symbol(Qt.Qt.blue)
            self.define_symbol(Qwt.QwtSymbol.VLine, Qt.Qt.blue)

            # define fill of ellipse
            c = Qt.QColor(Qt.Qt.blue)
            c.setAlpha(20)
            self.brush = Qt.QBrush(c)
            self.setBrush(Qt.QBrush(c))

            # define pen for horizontal line
            c = Qt.QColor(Qt.Qt.black)
            c.setAlpha(40)
            self.pen_hline = Qt.QPen(c)
            self.pen_hline.setWidth(2)
            self.pen_hline.setStyle(Qt.Qt.SolidLine)

            self.pdf_alpha_rect = 0.08
            self.pdf_alpha_line = 0.1

            self.set_text_property()

        else:
            raise Exception('Do not use PyQwtPlotEllipseAnnotator for this type of curve')

        self.set_default_pen()
        self.setPen(self.pen_def)
        self.setSymbol(self.symbol)

    def copy(self):
        pn = self.get_parent_name()
        t = self.get_curve_type()
        return PyQwtPlotEllipseAnnotator(pn, t, self.x_from, self.x_to, self.yval1, self.yval2, self.get_text())

    def draw(self, painter, xMap, yMap, canvasRect):
        """
        :param painter:
        :type painter: QtGui.QPainter
        """

        painter.setPen(self.pen())
        painter.setBrush(self.brush)

        i = 0
        px1 = xMap.transform(self.x(i))
        py1 = yMap.transform(self.y(i))
        px2 = xMap.transform(self.x(i + 1))
        py2 = yMap.transform(self.y(i + 1))

        # w = py2 - py1  # width of rectangle
        # ybottom = py1 + w

        px2 = px2 if px2 > canvasRect.left() else canvasRect.left()-2
        py2 = py2 if py2 < canvasRect.bottom() else canvasRect.bottom()
        py2 = py2 if py2 > canvasRect.top() else canvasRect.top()

        # print px1, px2, py1, py2
        # print py2 - py1

        # drawEllipse(int x, int y, int width, int height)
        painter.drawEllipse(px1, py1, px2 - px1, py2 - py1)

        if self.get_curve_type() == EnumAnnType.ellipsenote and len(self.get_text()) > 0:

            x_line = min(px1, px2-1)

            painter.setPen(self.pen_hline)
            painter.drawLine(x_line, py1 + (py2 - py1)/2, x_line, canvasRect.top())

            textsize = self.text.textSize(painter.font())
            texrect = QtCore.QRect(x_line, canvasRect.top(), textsize.width(), textsize.height())

            self.text.draw(painter, texrect)

    def set_pen_symbol_light(self):
        self.define_pen_symbol_light()
        self.setPen(self.pen_def)

    def correct_y1_y2(self):
        """ Not used """
        pass

    def plot(self):
        self.plot_xy(self.x_from, self.x_to, self.yval1, self.yval2)

    def plot_xy(self, x1, x2, y1, y2):

        x = [x1, x2]
        y = [y1, y2]

        self.setData(x, y)

    def draw_my(self, x=None, y=None):
        """auxially function"""
        self.plot()


class PyQwtPlotFloatingBaseline(AnnotationObject, Qwt.QwtPlotCurve):
    """
    Definition and drawing of floating baseline
    """
    newid = itertools.count().next

    def __init__(self, parent_name='', curve_type=None, x1=None, x2=None, y1=None, y2=None, s=''):
        super(AnnotationObject, self).__init__()
        AnnotationObject.__init__(self, parent_name, curve_type, x1, x2, y1, y2, s)
        Qwt.QwtPlotCurve.__init__(self)

        # self.text.text()  - contains points for floating baseline
        # in the following format: x1-y1, x2-y2, x3-y3, etc.

        self._fbaseline_x = []
        self._fbaseline_y = []

        if curve_type == EnumAnnType.floating_baseline:

            c = Qt.QColor(Qt.Qt.blue)
            c.setAlpha(100)

            cb = Qt.QColor(Qt.Qt.blue)
            cb.setAlpha(0)

            self.define_pen(color=c, width=3, line=Qt.Qt.SolidLine)
            self.define_pen_symbol(c, 3)
            self.define_symbol(Qwt.QwtSymbol.Rect, cb, Qt.QSize(12, 12))
            self.set_too_small_limit(0)

            self.setStyle(Qwt.QwtPlotCurve.Lines)
            self.setCurveAttribute(Qwt.QwtPlotCurve.Fitted, True)

            self.fitter = Qwt.QwtSplineCurveFitter()
            self.fitter.setFitMode(Qwt.QwtSplineCurveFitter.ParametricSpline)
            self.fitter.setSplineSize(500)
            self.setCurveFitter(self.fitter)

            self.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)

        else:
            raise Exception('Do not use PyQwtPlotFloatingBaseline for this type of curve')

        self.set_default_pen()
        self.setPen(self.pen_def)
        self.setSymbol(self.symbol)

    def set_pen_symbol_light(self):
        self.define_pen_symbol_light()
        self.setPen(self.pen_def)

    def correct_y1_y2(self):
        """ Not used - do not make y1 = y2"""
        pass

    def correct_val_order(self):
        """
        Sort values in fbaseline
        """

        z = zip(self._fbaseline_x, self._fbaseline_y)
        z.sort()

        self._fbaseline_x, self._fbaseline_y = zip(*z)
        self._fbaseline_x = list(self._fbaseline_x)
        self._fbaseline_y = list(self._fbaseline_y)

    def draw_my(self, x=None, y=None):
        """auxially function"""
        self.plot()

    def add_point_xy(self, x, y):
        """
        Add x and y points to floating baseline.
        Correct value orders and save first and last points
        """

        self._fbaseline_x.append(x)
        self._fbaseline_y.append(y)
        self.correct_val_order()

        self.x_from = self._fbaseline_x[0]
        self.x_to = self._fbaseline_x[-1]
        self.yval1 = self._fbaseline_y[0]
        self.yval2 = self._fbaseline_y[-1]

    def get_points(self):
        return self._fbaseline_x, self._fbaseline_y

    def get_nr_points(self):
        return len(self._fbaseline_x)

    def get_baseline_points_to_save_in_str(self):
        """
        :rtype str
        """
        lvalues = ["{0}-{1}".format(t1, t2) for t1, t2 in zip(self._fbaseline_x, self._fbaseline_y)]
        s = str(lvalues)
        s = s.replace(']', '').replace('[', '').replace('\'', '').replace(' ', '')
        return s

    def set_baseline_points_from_str(self, s):
        """
        :param s input string in format x1-y1,x2-y2,x3-y3
        :type s str
        """
        lvalues = s.split(",")
        for val in lvalues:
            val = val.strip().split("-")
            self._fbaseline_x.append(int(val[0]))
            self._fbaseline_y.append(int(val[1]))

        self.correct_val_order()

    def set_specific_xy(self, i, x, y):

        n = self.get_nr_points()
        if i < 0 or i > n - 1:
            return -1

        self._fbaseline_x[i] = x
        self._fbaseline_y[i] = y

    def remove_specific_xy(self, i):

        n = self.get_nr_points()
        if i < 0 or n == 0:
            return

        # if no point has been selected -> delete the last one
        if i > n - 1:
            i = n - 1

        del self._fbaseline_x[i]
        del self._fbaseline_y[i]

    def plot(self):
        self.setData(self._fbaseline_x, self._fbaseline_y)

    def plot_xy(self, x1, x2, y1, y2=None):
        pass


class Caliper(AnnotationObject, Qwt.QwtPlotCurve):
    """
    Definitions for an ellipse
    """
    newid = itertools.count().next

    def __init__(self, parent='', parent_name='', curve_type=EnumAnnType.caliper, x1=100, x2=700, y1=60, y2=80, s=''):
        super(AnnotationObject, self).__init__()
        AnnotationObject.__init__(self, parent_name, curve_type, x1, x2, y1, y2, s)
        Qwt.QwtPlotCurve.__init__(self)
        self.set_too_small_limit(100)

        self.__p_parent = parent
        # print self.__p_parent.get_sam

        if curve_type == EnumAnnType.caliper:

            self.x_dist_from_left = 0

            self.define_pen(Qt.Qt.black, 2, Qt.Qt.SolidLine)
            self.define_pen_symbol(Qt.Qt.black)
            self.define_symbol(Qwt.QwtSymbol.VLine, Qt.Qt.black)

            # define fill of ellipse
            c = Qt.QColor(Qt.Qt.black)
            c.setAlpha(30)
            self.brush = Qt.QBrush(c)
            self.setBrush(Qt.QBrush(c))

            # define pen for horizontal line
            c = Qt.QColor(Qt.Qt.black)
            c.setAlpha(60)
            self.pen_hline = Qt.QPen(c)
            self.pen_hline.setWidth(2)
            self.pen_hline.setStyle(Qt.Qt.SolidLine)

            self.set_text_property()

        else:
            raise Exception('Do not use Caliper for this type of curve')

        self.set_default_pen()
        self.setPen(self.pen_def)
        self.setSymbol(self.symbol)

    def copy(self):
        pn = self.get_parent_name()
        t = self.get_curve_type()
        return Caliper(self.__p_parent, pn, t, self.x_from, self.x_to, self.yval1, self.yval2, self.get_text())

    def reinit(self):
        self.set_xy_values(100, 700, 60, 80)

    def draw(self, painter, xMap, yMap, canvasRect):
        """
        :param painter:
        :type painter: QtGui.QPainter
        """

        painter.setPen(self.pen())
        painter.setBrush(self.brush)

        i = 0
        px1 = xMap.transform(self.x(i))
        py1 = yMap.transform(self.y(i))
        px2 = xMap.transform(self.x(i + 1))
        py2 = yMap.transform(self.y(i + 1))

        px2 = px2 if px2 > canvasRect.left() else canvasRect.left()-2
        py2 = py2 if py2 < canvasRect.bottom() else canvasRect.bottom()
        py2 = py2 if py2 > canvasRect.top() else canvasRect.top()

        ''' rect '''
        painter.drawRect(px1, py1, px2 - px1, py2 - py1)

        ''' lines '''
        painter.setPen(self.pen_hline)
        # x1, y1, x2, y2
        painter.drawLine(canvasRect.left(), py1, canvasRect.right(), py1)
        painter.drawLine(canvasRect.left(), py2, canvasRect.right(), py2)
        painter.drawLine(px1, canvasRect.bottom(), px1, canvasRect.top())
        painter.drawLine(px2, canvasRect.bottom(), px2, canvasRect.top())

        ''' text '''
        painter.setPen(self.pen())
        # font = painter.font()  # type: QtGui.QFont
        # font.setPointSize(font.pointSize()+2)
        # font.setBold(True)
        # painter.setFont(font)

        # compute width and height (need to have a sampling frequency!)
        fs = self.__p_parent.get_sampling_freq()
        w = abs(self.x(i + 1) - self.x(i)) / fs

        qtime = QtCore.QTime(0, 0)
        qtime = qtime.addSecs(int(w))
        self.set_text('{0}'.format(qtime.toString('mm:ss')))

        ''' decide text position '''
        # available - top (between line), bottom (between lines), x2

        textsize = self.text.textSize(painter.font())

        # TIME
        offset_y = 19
        offset_x = 6

        if textsize.height() < abs(min(py1, py2) - canvasRect.top()):
            textpos_y = min(py1, py2) - offset_y
        else:
            textpos_y = max(py1, py2) - offset_y

        if textsize.width() + offset_x > abs(px2 - px1):
            # if there is not enough space to plot time between lines x1 and x2

            # print textsize.width() + offset_x, abs(max(px1, px2) - canvasRect.right())
            # textpos_x = max(px1, px2) + 2
            if textsize.width() + offset_x < abs(max(px1, px2) - canvasRect.right()):
                textpos_x = max(px1, px2) + 2
            else:
                textpos_x = min(px1, px2) - textsize.width() - offset_x - 2
        else:
            textpos_x = px1 + (px2 - px1) / 2 - (textsize.width() + offset_x) / 2  # x - center

        # textpos_x = px1 + (px2 - px1) / 2 - (textsize.width() + offset_x) / 2  # x - center
        textrect = QtCore.QRect(textpos_x, textpos_y, textsize.width() + offset_x, textsize.height() + 1)
        self.text.draw(painter, textrect)

        # BPM
        offset_x = textsize.width() + 2

        h = abs(int(self.y(i + 1) - self.y(i)))
        self.set_text('{0}'.format(h))

        if textsize.width() < abs(min(px1, px2) - canvasRect.left()):
            textpos_x = min(px1, px2) - offset_x
        else:
            textpos_x = max(px1, px2) + 2

        textpos_y = py1 + (py2 - py1) / 2 - (textsize.height() + 1) / 2
        textrect = QtCore.QRect(textpos_x, textpos_y, textsize.width(), textsize.height()+1)
        self.text.draw(painter, textrect)

    def set_text_property(self):
        c = Qt.QColor(Qt.Qt.black)
        self.text.setColor(Qt.Qt.white)
        c.setAlpha(180)
        self.text.setBackgroundBrush(c)
        self.font_app.setBold(False)
        self.font_app.setPointSize(self.font_app.pointSize()+1)
        self.text.setFont(self.font_app)

    def set_pen_symbol_light(self):
        self.define_pen_symbol_light()
        self.setPen(self.pen_def)

    def correct_y1_y2(self):
        """ Not used """
        pass

    def plot(self):
        self.plot_xy(self.x_from, self.x_to, self.yval1, self.yval2)

    def plot_xy(self, x1, x2, y1, y2):

        x = [x1, x2]
        y = [y1, y2]

        self.setData(x, y)

    def draw_my(self, x=None, y=None):
        """auxially function"""
        self.plot()


class PyQwtPlotEvaluationNote(AnnotationObject, Qwt.QwtPlotMarker):
    """
    Definition of annotation box for CTG evaluation.
    This includes evaluation of initial CTG, level of concern, interventions, pH, and neorological assesment
    """

    def __init__(self, parent_name='', curve_type=None, x1=None, x2=None, y1=None, y2=None, s=''):
        super(AnnotationObject, self).__init__()
        AnnotationObject.__init__(self, parent_name, curve_type, x1, x2, y1, y2, s)
        Qwt.QwtPlotMarker.__init__(self)

        if curve_type == EnumAnnType.evaluation_note:

            self.sep = ConfigStatic.ann_evaluation_note_sep
            self.sep_type_and_value = ConfigStatic.ann_evaluation_note_sep_type_and_value

            # s = self.text_wrap_evaluations(s)
            self.set_text(s)

            self.setLineStyle(Qwt.QwtPlotMarker.VLine)
            self.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
            # self.setLabelAlignment(Qt.Qt.AlignTop)
            # label = self.label()
            # assert isinstance(label, Qwt.QwtText)
            # print label.
            # label.setLayoutAttribute()

            c = Qt.QColor(Qt.Qt.black)
            c.setAlpha(30)
            self.define_pen(c, 3)
            self.setLinePen(self.pen_def)

            self.set_text_property()
            self.pdf_alpha_rect = 0.08
            self.pdf_alpha_line = 0.1
        else:
            raise Exception('Do not use PyQwtPlotMarkerAnnotator for this type of curve')

        self.set_default_pen()
        self.setPen(self.pen_def)
        self.setSymbol(self.symbol)

    def copy(self):
        pn = self.get_parent_name()
        t = self.get_curve_type()
        return PyQwtPlotEvaluationNote(pn, t, self.x_from, self.x_to, self.yval1, self.yval2, self.get_text())

    def define_pen_symbol_light(self):
        c = self.pen_def.color()
        c.setAlpha(60)
        self.pen_def.setColor(c)
        self.pen_def.setWidth(2)
        self.define_symbol(Qwt.QwtSymbol.VLine, c, Qt.QSize(7, 7))

        f = QtGui.QFont(self.font_app)
        f.setPointSize(self.font_app.pointSize() - 2)
        self.text.setFont(f)

    def text_wrap_evaluations(self, evals):
        """
        This is inverse function to get_text()

        The input is 1 line string: initial_ctg:abnormal__neurology:brain injury
        The output is left aligned:
        initial_ctg: abnormal    .
        neurology: brain injury  .

        :param evals: string of evaluation separated by __
        :return:
        """
        # compute value for text padding (to be align on right)
        n = 0
        for r in evals.split(self.sep):
            r = r.strip('\n')
            r = Qwt.QwtText(r)
            if n < r.textSize().width():
                n = r.textSize().width()

        eval_list = list()
        for r in evals.split(self.sep):

            if r == '':
                continue

            r = r.strip('\n')
            s = r.split(self.sep_type_and_value)
            s = '{0}{1} {2}'.format(s[0], self.sep_type_and_value, s[1])

            r = Qwt.QwtText(s)
            while r.textSize().width() < n:
                s += ' '
                r = Qwt.QwtText(s)

            # to have correct alignment
            s += '.'
            eval_list.append(s)

        s = '\n'.join(eval_list)
        return s

    def get_text(self):
        """
        Get 1 line string from Qwt label

        The text is in a form:
        initial_ctg: abnormal    .
        neurology: brain injury  .

        This function returns: initial_ctg:abnormal__neurology:brain injury

        :return:
        """
        s = str(self.text.text())
        # print s
        s = s.split('\n')
        eval_new = list()
        for r in s:
            # get rid of the last dot
            while r[-1] == '.':
                r = r[0:-1]

            r = r.split(self.sep_type_and_value)
            r0 = r[0].rstrip().lstrip()
            r1 = r[1].rstrip().lstrip()
            eval_new.append('{0}{1}{2}'.format(r0, self.sep_type_and_value, r1))
        return self.sep.join(eval_new)

    def set_text(self, s):
        s = self.text_wrap_evaluations(s)
        self.text.setText(s)

    def set_pen_symbol_light(self):
        self.define_pen_symbol_light()
        self.setPen(self.pen_def)

    def correct_val_order(self):
        """ Not used """
        pass

    def correct_y1_y2(self):
        """ Not used """
        pass

    def plot(self):
        self.setLabel(self.text)
        self.setValue(self.x_from, 0)

    def plot_xy(self, x1, x2=None, y1=None, y2=None):
        self.setValue(x1, 0)

    def setPen(self, pen):
        self.setLinePen(pen)

    def draw_my(self, x=None, y=None):
        """auxially function"""
        self.plot()