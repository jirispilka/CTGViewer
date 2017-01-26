# -*- coding: utf-8 -*-
#
# Created on Nov 27, 2015
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

"""
Annotator
---------

Reference
~~~~~~~~~

.. autoclass:: Annotator
    :members:
    :private-members:

.. autoclass:: CanvasPickerAnnotator
    :members:

"""

from PyQt4.QtCore import pyqtSignal, QPointF
from PyQt4.Qwt5.Qwt import QwtPlot, QwtPlotCanvas
import os
import logging

import Common
from GuiForms import AddNoteDialog, EvaluationNoteDialog
from AnnotationObject import *
from Enums import EnumAnnType


def distance_to_point(pos, x, y):
    """
    Compute distance to a specific point
    :param pos: clicked position
    :param x: x-coordinate
    :param y: y-coordinate
    :type pos: QPointF
    """
    dx = pos.x() - x
    dy = pos.y() - y
    return np.sqrt(dx ** 2 + dy ** 2)


def compute_dist_ellipse(x1, x2, y1, y2, pos):
    """
    Compute distance to an ellipse
    """
    centerx = x1 + float(x2 - x1) / 2
    centery = y1 + float(y2 - y1) / 2

    dcxcy = distance_to_point(pos, centerx, centery)  # center
    dcxy1 = distance_to_point(pos, centerx, y1)  # bottom
    dcxy2 = distance_to_point(pos, centerx, y2)  # top
    dx1cy = distance_to_point(pos, x1, centery)  # left
    dx2cy = distance_to_point(pos, x2, centery)  # rigth

    # center, top, right, bottom, left
    return dcxcy, dcxy2, dx2cy, dcxy1, dx1cy


def compute_dist_caliper(x1, x2, y1, y2, pos):
    """
    Compute distance to a caliper
    """
    centerx = x1 + (x2 - x1) / 2
    centery = y1 + (y2 - y1) / 2

    d_center = distance_to_point(pos, centerx, centery)
    d_x1 = abs(pos.x() - x1)
    d_x2 = abs(pos.x() - x2)
    d_y1 = abs(pos.y() - y1)
    d_y2 = abs(pos.y() - y2)

    return d_center, d_y2, d_x2, d_y1, d_x1


class Annotator:
    """
    Class Annotator manages loading and saving annotations stored in an .ann file.

    Annotation format:
    id; plot_name; annotation type; x1; x2; y1; y2; text

    For example:
    5;fhr;basal;1;298316;160;160;
    id = 5
    plot_name = fhr (fhr or toco)
    annotation type = basal
    x1 = 1 (begin)
    x2 = 298316 (end)
    y1 = 160
    y2 = 160
    text = (empty)

    Special cases:
    floating baseline: The text field contains point of floating baseline in a format x1-y1; x2-y2 ; .... ; xn-yn
    """

    def __init__(self):

        self.ann_extension = '.ann'
        self._ann_file = ''
        self._path = ''
        self._dannotations_fhr = dict()
        self._dannotations_toco = dict()

        self._sep_items_new = ';'
        self._sep_items = ';'
        self._sep_anns = '\n'
        self._comment = '#'

        self._log = logging.getLogger(ConfigStatic.logger_name)

    def __load_annotations(self):
        """
        Load annotations from .ann file.

        :return: annotations in dict()
        :rtype: dict()
        """

        self._dannotations_fhr = dict()
        self._dannotations_toco = dict()

        if self._get_signal_annotated():
            self._log.info("Loading annotation file: {0}".format(self._ann_file))
            bdosniff = True

            dict_enum_action = EnumAnnType.__dict__

            with open(self._ann_file, 'r') as fp:
                for line in fp.readlines():

                    if line[0] == self._comment:
                        continue

                    if bdosniff is True:
                        bdosniff = False
                        scomma = line.split(',')
                        ssemic = line.split(';')

                        if len(scomma) == 8 or len(scomma) == 5 and (not len(ssemic) == 8):
                            self._sep_items = ','
                        else:
                            self._sep_items = ';'

                    s = line.split(self._sep_items)

                    if len(s) != 8:

                        # there is a blank line
                        if len(s) == 1:
                            if s[0] == '\n':
                                continue

                        if len(s) == 5:
                            raise IOError("Annotations in OLD format!! {0}".format(s))
                            # self._log.warning("Annotations in OLD format!! {0}".format(s))
                            # continue
                        else:
                            raise IOError("Annotations in wrong format!! {0}".format(s))
                            # self._log.warning("Annotations in wrong format!! {0}".format(s))

                    id_curve = str(s[0])
                    parent_name = str(s[1])
                    curve_type = str(s[2])
                    x_from = int(s[3])
                    x_to = int(s[4])
                    yval1 = self.check_int(s[5])
                    yval2 = self.check_int(s[6])
                    note = self.check_str(s[7])

                    if curve_type not in dict_enum_action:
                        print dict_enum_action
                        raise IOError('Unsupported annotation type {0}.'.format(curve_type))

                    if curve_type == EnumAnnType.note:
                        marker = PyQwtPlotMarkerAnnotator(parent_name, curve_type, x_from, x_to, None, None, note)

                    elif curve_type == EnumAnnType.evaluation_note:
                        marker = PyQwtPlotEvaluationNote(parent_name, curve_type, x_from, x_to, None, None, note)

                    elif curve_type == EnumAnnType.ellipse or curve_type == EnumAnnType.ellipsenote:
                        marker = PyQwtPlotEllipseAnnotator(parent_name, curve_type, x_from, x_to, yval1, yval2, note)

                    elif curve_type == EnumAnnType.floating_baseline:
                        marker = PyQwtPlotFloatingBaseline(parent_name, curve_type, x_from, x_to, yval1, yval2, note)
                        marker.set_baseline_points_from_str(note)

                    else:
                        marker = PyQwtPlotCurveAnnotator(parent_name, curve_type, x_from, x_to, yval1, yval2)

                    marker.id = id_curve
                    marker.correct_y1_y2()

                    if parent_name.lower() == EnumAnnType.plot_toco:
                        self._dannotations_toco[marker.id] = marker
                    else:
                        self._dannotations_fhr[marker.id] = marker

        else:
            self._dannotations_fhr = dict()
            self._dannotations_toco = dict()

        # return self._dannotations_fhr

    def _get_signal_annotated(self):
        b = Common.file_exists(self._ann_file) and Common.get_mumber_lines(self._ann_file) > 0
        return b

    @staticmethod
    def check_int(d):
        if d == 'None':
            return None
        else:
            return int(d)

    @staticmethod
    def check_str(s):
        if s == 'None' or s == '\n':
            return ''
        else:
            return str(s)

    def get_annotation_file(self):
        """Return annotation file name"""
        return self._ann_file

    def set_annotation_file(self, data_file):
        """Set the annotation file providing the data file"""

        name = Common.get_filename_without_ext(data_file)

        self._path = os.path.dirname(data_file)
        self._ann_file = os.path.join(self._path, name + self.ann_extension)  # set annotation file

    def ann_file_load(self, data_file):
        """
        Set the annotation file and load it.

        :param data_file: annotation file
        :type data_file: str
        :return:
        """
        self.set_annotation_file(data_file)
        self.__load_annotations()

    def get_annotations_fhr(self):
        return self._dannotations_fhr

    def get_annotations_toco(self):
        return self._dannotations_toco

    def get_annotations_copy_all(self):

        # for key, curve in self._dannotations_fhr.iteritems():
        #     print key, curve.get_parent_name()

        z = self._dannotations_fhr.copy()
        z.update(self._dannotations_toco)

        # for key, curve in z.iteritems():
        #     print key, curve.get_parent_name()
        return z

    # def get_annotations_copy(self):
    #     self._dannotations_fhr.copy()

    def get_annotations_copy(self):

        DeprecationWarning('Use get_annotations_copy_all instead.')

        ann = dict()
        for key, curve in self._dannotations_fhr.iteritems():
            name = curve.get_parent_name()
            typ = curve.get_curve_type()
            if typ == EnumAnnType.note:
                c = PyQwtPlotMarkerAnnotator(name, typ, curve.x_from, curve.x_to, curve.yval1, None,
                                             curve.get_text())

            elif typ == EnumAnnType.ellipse or typ == EnumAnnType.ellipsenote:
                c = PyQwtPlotEllipseAnnotator(name, typ, curve.x_from, curve.x_to, curve.yval1, curve.yval2,
                                              curve.get_text())
            else:
                c = PyQwtPlotCurveAnnotator(name, typ, curve.x_from, curve.x_to, curve.yval1)

            ann[curve.id] = c

        return ann

    def set_annotations(self, dann_fhr, dann_toco):
        self._dannotations_fhr = dann_fhr
        self._dannotations_toco = dann_toco

    def save_annotations(self):

        z = self._dannotations_fhr.copy()
        z.update(self._dannotations_toco)

        with open(self._ann_file, 'w+') as fp:
            for idd, d in z.items():

                name = str(d.get_parent_name())
                curve_type = str(d.get_curve_type())
                d.correct_y1_y2()

                if d.valid:
                    fp.write(str(idd))
                    fp.write(self._sep_items_new)
                    fp.write(name)
                    fp.write(self._sep_items_new)
                    fp.write(curve_type)
                    fp.write(self._sep_items_new)
                    fp.write(str(d.x_from))
                    fp.write(self._sep_items_new)
                    fp.write(str(d.x_to))
                    fp.write(self._sep_items_new)
                    fp.write(str(d.yval1))
                    fp.write(self._sep_items_new)
                    fp.write(str(d.yval2))
                    fp.write(self._sep_items_new)

                    if isinstance(d, PyQwtPlotFloatingBaseline):
                        s = d.get_baseline_points_to_save_in_str()
                    else:
                        s = d.get_text()
                        s = s.replace('\n', ' ')
                    fp.write(s)
                    fp.write(self._sep_anns)

        self._log.info("Saving annotation file: {0}".format(self._ann_file))

    def set_annotations_and_save(self, dann_fhr, dann_toco):
        self.set_annotations(dann_fhr, dann_toco)
        self.save_annotations()


class CanvasPickerAnnotator(Qt.QObject):
    """
    Pick events generated by user such as draw basal, baseline, recovery, etc.
    The CanvasPickerAnnotator calls super function to plot the events
    The CanvasPickerAnnotator should stay independent of drawing and GUI.

    :param p_plot: pointer to :py:class:`FhrPlot`
    :type p_plot: :py:class:`FhrPlot`
    """

    # if annotation changed, emit this signal, these signal are typically caught by FhrPlot and TocoPlot
    signal_ann_moved = pyqtSignal()
    signal_ann_moved_outside_view = pyqtSignal(['int'])

    def __init__(self, p_plot):
        Qt.QObject.__init__(self, p_plot)

        self.__selected_curve = None
        self.__selected_point = -1
        self.__point_clicked = None

        self.__plot = p_plot

        self._add_note_dialog = AddNoteDialog()
        self._add_evaluation_note_dialog = EvaluationNoteDialog()

        self.canvas = self.__plot.canvas()
        self.canvas.installEventFilter(self)

        # # We want the focus, but no focus rect.
        # # The selected point will be highlighted instead.
        self.canvas.setFocusPolicy(Qt.Qt.StrongFocus)
        # canvas.setCursor(Qt.Qt.PointingHandCursor)
        self.canvas.setFocusIndicator(QwtPlotCanvas.ItemFocusIndicator)
        self.canvas.setFocus()

        # self._distance_point = 100
        # self._distance_line = 5
        # self._distance_note = 300
        # self._distance_ellipse = 200
        self._distance = 0.02
        # self._distance_ellipse_center = 500

        self.__bmoving = False
        self.__add_annotation_after_ellipse = False
        # self._current_curve = AnnotationObject()
        # self.__ann_action = self.__plot.get_ann_action()

        self.__curve_to_copy = None
        self.__last_click_pos = None

        # self.canvas.setMouseTracking(True)
        # self.__shiftCurveCursor(True)

    def __compute_point(self, pos):
        """
        The clicked point stored in event.x() and event.y() is transformed to x and y axis for
        particular plot attached.

        :param pos: x and y position
        :type  pos: QPointF
        :rtype: QPointF
        """
        clickedpointx = self.__plot.invTransform(QwtPlot.xBottom, pos.x())
        clickedpointy = self.__plot.invTransform(QwtPlot.yLeft, pos.y())

        return Qt.QPoint(int(clickedpointx), int(clickedpointy))

    def __check_outside_of_plot(self, x1, x2, y1, y2):

        xmin = self.__plot.xAxisMinSample()
        xmax = self.__plot.xAxisMaxSample()

        ymin = self.__plot.viewYMinSample()
        ymax = self.__plot.viewYMaxSample()

        x1 = x1 if x1 > xmin else xmin
        x1 = x1 if x1 < xmax else xmax

        x2 = x2 if x2 > xmin else xmin
        x2 = x2 if x2 < xmax else xmax

        y1 = y1 if y1 > ymin else ymin
        y1 = y1 if y1 < ymax else ymax

        y2 = y2 if y2 > ymin else ymin
        y2 = y2 if y2 < ymax else ymax

        return x1, x2, y1, y2

    def __select(self, pos, bhighlight=True, select_type=None):
        """
        Select an object based on computed distance.
        The x and y values are normalized first to ensure the same units for distance in x and y coordinates.
        The x axis is in samples while the y axis is in BPM.

        :param pos:
        :param bhighlight:
        :param select_type: Select specific type of curve (annotation)
        :type pos: QPointF
        :type select_type: str
        :return:
        """
        # found, distance, point = None, 100, -1

        debug = False
        if debug:
            print 'SELECT'

        dmax = self._distance
        found_curve = None
        found_point = None

        point_dist = np.infty
        line_dist = np.infty
        note_dist = np.infty
        ellipse_dist = np.infty
        caliper_dist = np.infty
        point_i = -1
        bellipse = False
        bcaliper = False

        # the normalization have to be adjusted to aspect ratio of the plot
        size = self.__plot.size_plot_area()
        r_adjust = size.width() / float(size.height())

        xmin = self.__plot.viewXMinSample()
        xmax = self.__plot.viewXMaxSample()
        rx = (xmax - xmin) / r_adjust
        # print xmin, xmax, (xmax - xmin)
        ymin = self.__plot.viewYMinSample()
        ymax = self.__plot.viewYMaxSample()
        ry = abs(ymax - ymin)
        # print ymin, ymax, (ymax - ymin)

        # normalize, aby mely x a y stejne jednotky (puvodne x je ve vzorcich a y v bpm)
        pos_clicked = pos
        pos = QPointF((pos.x() - xmin) / rx, (pos.y() - ymin) / ry)
        # pos = QPointF((pos.x() - xmin), (pos.y() - ymin) )

        self.__unselect()

        # create local copy and add caliper (if visible)
        d_ann = self.__plot.ann_get().copy()

        if self.__plot.caliper_is_visible():
            d_ann[self.__plot.caliper.id] = self.__plot.caliper

        for key, curve in d_ann.iteritems():

            t = curve.get_curve_type()

            if select_type is not None:
                if t != select_type:
                    continue

            x_from = (curve.x_from - xmin) / rx
            x_to = (curve.x_to - xmin) / rx

            y1 = y2 = None
            if curve.yval1 is not None:
                y1 = (curve.yval1 - ymin) / ry

            if curve.yval2 is not None:
                y2 = (curve.yval2 - ymin) / ry

            # x_from = curve.x_from - xmin
            # x_to = curve.x_to - xmin
            # y1 = curve.yval1 - ymin
            # y2 = curve.yval2 - ymin

            # print rx, ry
            # print pos, x_from, x_to, y1, y2

            # if debug:
            #     print 'normalize x a y:', x_from, x_to, y1, y2

            if t == EnumAnnType.basal:
                line_dist = abs(pos.y() - y1)
                if debug:
                    print 'basal (line dist):', line_dist

            elif t == EnumAnnType.baseline or t == EnumAnnType.recovery or t == EnumAnnType.no_recovery or \
                    t == EnumAnnType.excessive_ua or t == EnumAnnType.acceleration or t == EnumAnnType.deceleration or \
                    t == EnumAnnType.uterine_contraction:
                d0 = abs(x_from - pos.x())
                d1 = abs(x_to - pos.x())
                # print d0, d1

                if d0 < d1:
                    point_i = 0
                    point_dist = d0
                else:
                    point_i = 1
                    point_dist = d1

                line_dist = abs(pos.y() - y1)

                if debug:
                    print 'baseline etc (d0,d1,line dist):', d0, d1, line_dist

            elif t == EnumAnnType.ellipsenote:

                d = compute_dist_ellipse(x_from, x_to, y1, y2, pos)
                ellipse_dist = min(d)
                point_i = d.index(ellipse_dist)

                point_i = -1 if point_i == 0 else point_i

                bx = x_from <= pos.x() <= x_to
                by = y1 <= pos.y() <= y2
                bellipse = bx and by

                if debug:
                    print 'ellipse etc (ellipse_dist, bellipse):', ellipse_dist, bellipse

            elif t == EnumAnnType.note or t == EnumAnnType.evaluation_note:
                note_dist = abs(pos.x() - x_from)
                if debug:
                    print 'note etc (note_dist):', note_dist

            elif isinstance(curve, PyQwtPlotFloatingBaseline):
                baseline_x, baseline_y = curve.get_points()

                # potrebuji normalizovat
                baseline_x = [(t - xmin) / rx for t in baseline_x]
                baseline_y = [(t - ymin) / ry for t in baseline_y]

                d = [distance_to_point(pos, x, y) for x, y in zip(baseline_x, baseline_y)]
                point_dist = min(d)
                point_i = d.index(point_dist)

                line_dist = point_dist

                if debug:
                    print 'floating baseline (distances, point , dist):', d, point_i, point_dist

            elif isinstance(curve, Caliper):

                d = compute_dist_caliper(x_from, x_to, y1, y2, pos)
                caliper_dist = min(d)
                point_i = d.index(caliper_dist)

                point_i = -1 if point_i == 0 else point_i

                bx = x_from <= pos.x() <= x_to
                by = y1 <= pos.y() <= y2
                bcaliper = bx and by

                # if clicked inside box and all distances are small

                if debug:
                    print 'caliper etc (caliper_dist, point_i, bcaliper, d):', caliper_dist, point_i, bcaliper, d

            else:
                continue
                # return 0

            if point_dist < dmax and line_dist < dmax:
                # if a point/line is close
                found_curve = curve
                found_point = point_i
                dmax = min(point_dist, line_dist)

            elif line_dist <= dmax and x_from < pos.x() < x_to:
                # if a line is close
                found_curve = curve
                found_point = -1
                dmax = line_dist

            elif note_dist < dmax:
                # if a note is close
                found_curve = curve
                found_point = -1
                dmax = note_dist

            elif ellipse_dist < dmax:
                # if an ellipse is close
                found_curve = curve
                found_point = point_i
                dmax = ellipse_dist

            elif caliper_dist < dmax:
                found_curve = curve
                found_point = point_i
                dmax = caliper_dist

            elif bellipse and found_curve is None:  # if not another curve has been selected
                found_curve = curve
                found_point = -1

            elif bcaliper and found_curve is None:  # if not another curve has been selected
                found_curve = curve
                found_point = -1

        if found_curve is not None:
            self.__selected_curve = found_curve
            self.__selected_point = found_point
            self.__highlight(bhighlight)
            self.__point_clicked = pos_clicked
            return True

        return False

    def __select_curve(self, curve, point, pos):
        self.__selected_curve = curve
        self.__selected_point = point
        self.__point_clicked = pos

    def __unselect(self):
        self.__highlight(False)
        self.__selected_curve = None
        self.__selected_point = -1

    def __highlight(self, b_highlight):

        curve = self.__selected_curve
        # bdrawpoint = self.__selected_point != -1
        if not curve:
            return

        # Use copy constructors to defeat the reference semantics.
        # symbol = curve.get_symbol()
        new_symbol = curve.get_symbol()
        newpen = Qt.QPen(curve.get_default_pen())

        if b_highlight:
            new_symbol = curve.get_symbol_highlight()
            newpen.setColor(curve.get_color_highlight())

        doreplot = self.__plot.autoReplot()
        self.__plot.setAutoReplot(False)

        if curve.get_curve_type() != EnumAnnType.basal:
            curve.setSymbol(new_symbol)

        # curve.draw(self.__selected_point, self.__selected_point)
        # else:
        # if bdrawpoint:
        #     curve.setSymbol(symbol)
        # else:
        curve.setPen(newpen)
        # print curve.xAxis(), curve.yAxis()
        curve.draw_my(curve.xAxis(), curve.yAxis())

        self.__plot.setAutoReplot(doreplot)
        self.__plot.replot()

    def __delete(self):

        curve = self.__selected_curve
        if not curve:
            return

        if isinstance(curve, PyQwtPlotFloatingBaseline):
            curve.remove_specific_xy(self.__selected_point)
            # if engough point, delete it: else delete the floating baseline
            if curve.get_nr_points() > 0:
                curve.plot()
                self.__plot.replot()
                return

        self.__plot.ann_delete_curve(curve)

    def __move(self, pos, bfinished_move=False):
        """
        Move selected item - move either point or complete line

        :param pos: x and y position
        :param bfinished_move: if MouseRelease then moving was finished
        :type  pos: QPointF
        :type  bfinished_move: bool
        """

        curve = self.__selected_curve
        bdragpoint = self.__selected_point != -1

        if not curve:
            return

        # x = self.__plot.invTransform(curve.xAxis(), pos.x())
        # y = self.__plot.invTransform(curve.yAxis(), pos.y())
        x = pos.x()
        y = pos.y()

        # if x < self.__plot.xAxisMinSample:
        #     x = self.__xAxisMinSample

        xmin = self.__plot.viewXMinSample()
        xmax = self.__plot.viewXMaxSample()

        ymin = self.__plot.viewYMinSample()
        ymax = self.__plot.viewYMaxSample()

        y = y if y > ymin else ymin
        y = y if y < ymax else ymax

        # if outside of box then move plot
        if x > xmax:
            self.signal_ann_moved_outside_view.emit(x-xmax)
        elif x < xmin:
            self.signal_ann_moved_outside_view.emit(x-xmin)

        t = curve.get_curve_type()

        # if a point is dragged
        if bdragpoint:

            if t == EnumAnnType.ellipsenote or t == EnumAnnType.caliper:

                if self.__selected_point == 1:
                    curve.set_xy_values(curve.x_from, curve.x_to, curve.yval1, int(y))
                elif self.__selected_point == 2:
                    curve.set_xy_values(curve.x_from, int(x), curve.yval1, curve.yval2)
                elif self.__selected_point == 3:
                    curve.set_xy_values(curve.x_from, curve.x_to, int(y), curve.yval2)
                elif self.__selected_point == 4:
                    curve.set_xy_values(int(x), curve.x_to, curve.yval1, curve.yval2)
                elif self.__selected_point != 0:
                    curve.set_xy_values(curve.x_from, int(x), curve.yval1, int(y))

            elif t == EnumAnnType.floating_baseline:
                curve.set_specific_xy(self.__selected_point, int(x), int(y))

            else:
                # selected left of point of a curve
                if self.__selected_point == 0:
                    curve.set_xy_values(int(x), curve.x_to, curve.yval1, curve.yval2)
                else:
                    curve.set_xy_values(curve.x_from, int(x), curve.yval1, curve.yval2)

            curve.plot()
            if bfinished_move:
                curve.correct_val_order()
                self.signal_ann_moved.emit()

        else:
            dx = int(x - self.__point_clicked.x())
            dy = int(y - self.__point_clicked.y())

            y1_new = y
            y2_new = y

            if t != EnumAnnType.basal:
                x_new_from = curve.x_from + dx
                x_new_to = curve.x_to + dx
            else:
                x_new_from = curve.x_from
                x_new_to = curve.x_to

            if t == EnumAnnType.ellipsenote or t == EnumAnnType.caliper:
                y1_new = curve.yval1 + dy
                y2_new = curve.yval2 + dy

            x_new_from, x_new_to, y1_new, y2_new = self.__check_outside_of_plot(x_new_from, x_new_to, y1_new, y2_new)
            curve.plot_xy(x_new_from, x_new_to, y1_new, y2_new)

            if bfinished_move:
                curve.set_xy_values(int(x_new_from), int(x_new_to), int(y1_new), int(y2_new))
                self.signal_ann_moved.emit()

        self.__plot.replot()

    # def event(self, event):
    #     if event.type() == Qt.QEvent.User:
    #         return True
    #     return Qt.QObject.event(event)

    def eventFilter(self, obj, event):
        """
        Filter mouse and key events:
        * Single click event
        * Double click event
        * MouseMove
        * MouseRelease
        """

        if event.type() == Qt.QEvent.Paint:
            Qt.QApplication.postEvent(self, Qt.QEvent(Qt.QEvent.User))

        elif event.type() == Qt.QEvent.MouseButtonPress:  # and self.__bleft_btn_hold is False:
            self.__last_click_pos = event.pos()
            self.perform_single_click_event(event)

            # Qt.QTimer.singleShot(Qt.QApplication.instance().doubleClickInterval(),
            #                      self.perform_single_click_event)

        elif event.type() == Qt.QEvent.MouseButtonDblClick:
            self.perform_double_click_event(event)

        elif event.type() == Qt.QEvent.MouseMove:
            point = self.__compute_point(event.pos())
            self.__bmoving = True
            self.__move(point)
            return True

        elif event.type() == Qt.QEvent.MouseButtonRelease:
            if self.__bmoving:
                point = self.__compute_point(event.pos())
                self.__bmoving = False
                self.__move(point, True)

                if self.__add_annotation_after_ellipse is True and not self.__selected_curve.is_too_small():
                    self.__add_annotation_after_ellipse = False
                    self._add_note_dialog.clear_text()
                    if self._add_note_dialog.show():
                        # self._current_curve.set_text(self._add_note_dialog.get_text())
                        self.__selected_curve.set_text(self._add_note_dialog.get_text())
                        self.__plot.ann_plot_curves()

            if self.__selected_curve is not None:
                if self.__selected_curve.is_too_small():
                    self.__delete()

        elif event.type() == Qt.QEvent.KeyPress:
            if event.key() == Qt.Qt.Key_Delete:
                self.__delete()

            # elif event.matches(Qt.QKeySequence.Copy):
            #     if self.__selected_curve is not None:
            #         self.__curve_to_copy = self.__selected_curve.copy()
            #
            # elif event.matches(Qt.QKeySequence.Cut):
            #     if self.__selected_curve is not None:
            #         self.__curve_to_copy = self.__selected_curve.copy()
            #         self.__delete()
            #
            # elif event.matches(Qt.QKeySequence.Paste):
            #
            #     if self.__curve_to_copy is not None:
            #         print self.__last_click_pos
            #         print self.__curve_to_copy
            #         d = int(self.__curve_to_copy.x_to - self.__curve_to_copy.x_to)
            #         self.__curve_to_copy.x_from = int(self.__last_click_pos.x())
            #         self.__curve_to_copy.x_to = self.__curve_to_copy.x_from + d
            #         self.__curve_to_copy.yval1 = int(self.__last_click_pos.y())
            #         self.__plot.ann_add(self.__curve_to_copy)
            #         # self.__curve_to_copy = None

        return QwtPlot.eventFilter(self, obj, event)

    def perform_single_click_event(self, event):
        """
        Perform event related to a single click on plot
        :param event:
        :type event:
        """

        action = self.__plot.get_ann_action()
        point = self.__compute_point(event.pos())

        if event.button() == Qt.Qt.LeftButton:

            self.__unselect()

            if action == EnumAnnType.basal:
                self.__plot.ann_basal(point.y())

            elif action == EnumAnnType.baseline or action == EnumAnnType.recovery \
                    or action == EnumAnnType.no_recovery or action == EnumAnnType.excessive_ua \
                    or action == EnumAnnType.acceleration or action == EnumAnnType.deceleration \
                    or action == EnumAnnType.uterine_contraction:

                curve = self.__plot.ann_line_start(point, action)
                self.__select_curve(curve, point, point)

            elif action == EnumAnnType.ellipsenote:
                self._add_note_dialog.clear_text()

                if not (self.__add_annotation_after_ellipse is False and self.__select(point, True, EnumAnnType.ellipsenote)):
                    curve = self.__plot.ann_ellipse(point, action)
                    self.__select_curve(curve, point, point)
                    self.__add_annotation_after_ellipse = True
                else:
                    self.__unselect()

            elif action == EnumAnnType.note:
                self._add_note_dialog.clear_text()
                if not self.__select(point, True, EnumAnnType.note):  # add new annotation
                    if self._add_note_dialog.show():
                        self.__plot.ann_note(point, self._add_note_dialog.get_text())
                else:
                    self.__unselect()

            elif action == EnumAnnType.evaluation_note:
                self._add_evaluation_note_dialog.clear()
                if not self.__select(point, True, EnumAnnType.evaluation_note):  # add new annotation
                    if self._add_evaluation_note_dialog.show():
                        self.__plot.ann_evaluation_note(point, self._add_evaluation_note_dialog.get_text())
                else:
                    self.__unselect()

            elif action == EnumAnnType.floating_baseline:
                curve = self.__plot.ann_floating_baseline(point, action)
                self.__select_curve(curve, point, point)

            # elif action == EnumAnnType.caliper:
            #     print 'Caliper'

            elif action == EnumAnnType.select:
                self.__select(point)

    def perform_double_click_event(self, event):
        """
        Perform event related to a double click (edit the annotations)
        """

        action = self.__plot.get_ann_action()
        point = self.__compute_point(event.pos())

        if event.button() == Qt.Qt.LeftButton:
            if action == EnumAnnType.select:
                self._add_note_dialog.clear_text()
                self._add_evaluation_note_dialog.clear()

                if (self.__add_annotation_after_ellipse is False and self.__select(point, True, EnumAnnType.ellipsenote)) \
                        or (self.__select(point, True, EnumAnnType.note)):
                    # modify current annotation
                    self._add_note_dialog.set_text(self.__selected_curve.text.text())
                    if self._add_note_dialog.show():
                        self.__selected_curve.set_text(self._add_note_dialog.get_text())
                        self.signal_ann_moved.emit()
                        self.__plot.ann_plot_curves()

                elif self.__select(point, True, EnumAnnType.evaluation_note):
                    assert isinstance(self.__selected_curve, PyQwtPlotEvaluationNote)

                    self._add_evaluation_note_dialog.set_values_from_evaluation_string(self.__selected_curve.get_text())

                    if self._add_evaluation_note_dialog.show():
                        eval_str = self._add_evaluation_note_dialog.get_text()
                        self.__selected_curve.set_text(eval_str)
                        self.signal_ann_moved.emit()
                        self.__plot.ann_plot_curves()

# def main():
#     app = Qt.QApplication(sys.argv)
#     window = AnnotatorTemp()
#     window.resize(680, 400)
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     main()
