# -*- coding: utf-8 -*-
#
# Created on Apr 13, 2016
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2016, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)


from PyQt4.QtGui import QApplication as App
from PyQt4.QtCore import QTime, pyqtSignal, pyqtSlot, QSignalMapper
import os
import logging
import time

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4, landscape, cm
    from reportlab.lib import colors
    from reportlab.pdfbase.pdfmetrics import stringWidth
    REPORTLAB_IMPORTED = True

except ImportError:
    REPORTLAB_IMPORTED = False


from ExportPdfUI import Ui_ExportToPdf
from Common import samples2time, time_locator
from Enums import *
from Config import ConfigStatic
from AnnotationObject import *


def temporary_read_data(sfile):
    sfile = str(sfile)

    from LoadWriteData import LoadData
    dl = LoadData()
    adata = dl.read_data(sfile)

    return adata


class ExportToPdfForm(QtGui.QWidget):

    stop_signal = pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self._log = logging.getLogger(ConfigStatic.logger_name)
        self._log.info('passed')

        self.ui = Ui_ExportToPdf()
        self.ui.setupUi(self)

        self.reportlab_imported = REPORTLAB_IMPORTED
        self.cprint = Print()

        self.btnSave = self.ui.buttonBox.button(Qt.QDialogButtonBox.Save)
        self.btnCancel = self.ui.buttonBox.button(Qt.QDialogButtonBox.Cancel)

        # self.ui.rbPaperEU.clicked.connect(self.slotik)
        # self.ui.rbPaperUS.clicked.connect(self.slotik)

        self.signal_mapper = QSignalMapper(self)

        # self.connect(self.ui.rbPaperEU, QtCore.SIGNAL("clicked()"), signal_mapper, QtCore.SLOT("map()"))
        # self.connect(self.ui.rbPaperEU, QtCore.SIGNAL("clicked()"), self.signal_mapper, QtCore.SLOT("map()"))

        self.signal_mapper.setMapping(self.ui.rbPaperEU, EnumPaperFormat.EU)
        self.signal_mapper.setMapping(self.ui.rbPaperUS, EnumPaperFormat.US)

        self.ui.rbPaperEU.clicked.connect(self.signal_mapper.map)
        self.ui.rbPaperUS.clicked.connect(self.signal_mapper.map)

        self.signal_mapper.mapped[QtCore.QString].connect(self.slot_paper_format)

        # self.signal_mapper.mapped.connect(self.slot_paper_format)
        # self.signal_mapper.connect(QtCore.SIGNAL("mapped()"), QtCore.SLOT("clicked()"))

        # connection
        self.ui.btnBrowse.clicked.connect(self._open_dir_source)
        self.ui.btnSelectAll.clicked.connect(self._select_all)
        self.ui.btnUnselect.clicked.connect(self._unselect_all)
        self.btnSave.clicked.connect(self.save)
        self.btnCancel.clicked.connect(self.close)
        self.ui.lnFileName.textChanged.connect(self.line_edit_changed)

        self.ui.lnFileName.setText(os.path.expanduser("~")+os.path.sep)

        self._progress_dialog = QtGui.QProgressDialog()
        self._progress_dialog.setLabelText("Exporting CTG file to pdf ...")
        self._progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self._progress_dialog.close()

        self._progress_dialog.canceled.connect(self._stop_progress)
        self.cprint.nr_pages_processed.connect(self._update_progress)

        self.msgBoxError = QtGui.QMessageBox()
        self.msgBoxError.setText("The output file name is empy!")
        self.msgBoxError.setDefaultButton(QtGui.QMessageBox.Close)
        self.msgBoxError.setIcon(QtGui.QMessageBox.Critical)

        self.msgbox_unsaved = QtGui.QMessageBox()
        self.msgbox_unsaved.setText("The file already exists.")
        self.msgbox_unsaved.setInformativeText("Overwrite?")
        self.msgbox_unsaved.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        self.msgbox_unsaved.setDefaultButton(QtGui.QMessageBox.Ok)
        self.msgbox_unsaved.setIcon(QtGui.QMessageBox.Warning)

        e = EnumAnnType
        self._dict_ann = {self.ui.cbBasal: e.basal, self.ui.cbBaseline: e.baseline, self.ui.cbRecovery: e.recovery,
                          self.ui.cbNoRecovery: e.no_recovery, self.ui.cbExcessiveUA: e.excessive_ua,
                          self.ui.cbNote: e.note, self.ui.cbMark: e.ellipsenote,
                          self.ui.cbFloatingBaseline: e.floating_baseline, self.ui.cbAccel: e.acceleration,
                          self.ui.cbDecel: e.deceleration, self.ui.cbUA: e.uterine_contraction}

        self.ui.lbStatus.setText("(saving to pdf might take a while)")

    @pyqtSlot(QtCore.QString)
    def slot_paper_format(self, sformat):
        # print sformat
        self.set_paper_format(sformat)

    def _open_dir_source(self):

        dir1, dummy = os.path.split(str(self.ui.lnFileName.text()))
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Select a filename for exporting', dir1)

        if file_name == "":
            return -1
        else:
            file_name = str(file_name)
            self.ui.lnFileName.setText(file_name)

        return 0

    def line_edit_changed(self):
        self.btnSave.setEnabled(True)

    def get_file_to_save(self):
        """
        Split the path, check if file exist.
        Default: Save to USER HOME directory
        """

        file_name = str(self.ui.lnFileName.text())
        path, file_name = os.path.split(file_name)

        if file_name == "":
            self.msgBoxError.exec_()
            return -1

        if not file_name.endswith(".pdf"):
            file_name += '.pdf'

        if path == "":
            file_name = os.path.join(os.path.expanduser('~'), file_name)
        else:
            file_name = os.path.join(path, file_name)

        return file_name

    def set_paper_format(self, pformat):
        """Interface method to the Print() class"""

        if pformat == EnumPaperFormat.EU:
            self.ui.rbPaperEU.setChecked(True)
            self.cprint.set_paper_format(pformat)
        else:
            self.ui.rbPaperUS.setChecked(True)
            self.cprint.set_paper_format(pformat)

    def set_signals(self, fhr, toco, fs, timestamp):
        """Interface method to the Print() class"""
        self.cprint.set_signals(fhr, toco, fs, timestamp)

    def set_annotations(self, ann):
        """Interface method to the Print() class"""
        self.cprint.set_annotations(ann)

    def set_record_name(self, s):
        """Interface method to the Print() class"""
        self.cprint.set_record_name(s)

    def save(self):

        file_name = self.get_file_to_save()

        if file_name == -1:
            return -1

        if os.path.exists(file_name):
            if self.msgbox_unsaved.exec_() == QtGui.QMessageBox.Cancel:
                return

        self.btnSave.setEnabled(False)
        self.btnCancel.setEnabled(False)
        App.processEvents()

        try:
            self._progress_dialog.close()
            self._progress_dialog.setRange(0, self.cprint.number_of_pages_to_print())
            self._progress_dialog.setValue(0)
            self._progress_dialog.open()

            self.cprint.set_ann_to_print(self._get_ann_to_print())
            self.cprint.set_file_name(file_name)
            self.cprint.print_()

        except IOError, e:
            self._progress_dialog.close()
            self.msgBoxError.setText(str(e))
            self.msgBoxError.exec_()
            self.btnSave.setEnabled(True)
            self.btnCancel.setEnabled(True)
            return -1

        self._progress_dialog.close()
        s = "PDF saved to: " + file_name
        self.ui.lbStatus.setText(s)
        self._log.info(s)
        App.processEvents()

        time.sleep(2)

        self.ui.lbStatus.setText("")
        self.btnSave.setEnabled(True)
        self.btnCancel.setEnabled(True)
        self.close()

    def _select_all(self):

        for cb in self._dict_ann.iterkeys():
            if isinstance(cb, QtGui.QCheckBox):
                if cb.isVisible():
                    cb.setChecked(True)

    def _unselect_all(self):

        for cb in self._dict_ann.iterkeys():
            if isinstance(cb, QtGui.QCheckBox):
                if cb.isVisible():
                    cb.setChecked(False)

    def _get_ann_to_print(self):

        l = [name for cb, name in self._dict_ann.iteritems() if cb.isChecked()]

        # l = list()
        # if cb.isChecked():
        #     l.append(name)

        return l

    def _update_progress(self, i):
        self._progress_dialog.setValue(i)

    def _stop_progress(self):
        self.btnSave.setEnabled(True)
        self.btnCancel.setEnabled(True)
        self.cprint.stop_print()
        self._progress_dialog.close()


class Print(Qt.QObject):

    nr_pages_processed = pyqtSignal(['int'])

    def __init__(self):
        Qt.QObject.__init__(self)

        self._file_name = ''
        self._paper_format = EnumPaperFormat.EU
        self._record_name = ''  # name of the CTG file

        self._ann_names_to_print = [d for key, d in EnumAnnType.__dict__.iteritems() if not key.startswith('__')]

        self._default_font_name = "Helvetica"
        self._default_font_size = 10

        self._adj_x = 0  # adjudst CTG file x - axis (in samples) to printable paper area
        self._adj_y1 = 0
        self._adj_y2 = 0

        self._line_dash = tuple([8, 2])
        self._line_solid = tuple([1, 0])
        self._line_width_adjust = 2

        # signals
        self._fhr = None
        self._toco = None
        self._fs = None
        self._timestamp = None
        self._ann = dict()

        self._fhr_plot = None
        self._toco_plot = None
        self._time_plot = None  # time stamp accommodated for plot
        self._time_ticks = None  # ticks of x-axis
        self._time_string = None  # ticks of x-axis
        self._paper_speed = 0
        self._paper_bpm = 0
        self._locator_minute = -1

        self._fhr_min_val = None
        self._fhr_max_val = None

        self._toco_step = []
        self._toco_axis = []
        self._fhr_step = []
        self._fhr_axis = []

        # paper
        # # letter = 215.9 X 279.4 mm
        # # A4 = 210 X 297 mm

        self._paper_size = None
        self._fhr_paper_height = None
        self._toco_paper_height = None
        self._toco_resolution = None

        self._paper_width = None  # width of the paper
        self._paper_height = None  # height of the paper
        self._paper_plot_width = None  # width of the plotting area
        self._paper_plot_height = None  # height of the plotting area

        self._margin = 0.1 * cm
        self._axis_space = .7 * cm
        self._title_space = .5 * cm

        self._toco_max_val = 120

        self.set_paper_format()

        self.__continue_print = True

    def ppaper(self, c):
        self.pborder(c)
        self.pline_sep_fhr_toco(c)
        self.pbackgorund(c)
        self.pgrid(c)
        self.pyaxis(c)
        # self.pxaxis(c)

    def pborder(self, c):

        margin = self._margin
        axis_space = self._axis_space
        c.translate(margin + axis_space, margin + axis_space)

        # wrapping rectangle
        c.setStrokeColor(colors.black, .7)
        c.rect(0, 0, width=self._paper_plot_width, height=self._paper_plot_height)

    def pline_sep_fhr_toco(self, c):
        """ print line separating FHR and TOCO """
        c.setStrokeColor(colors.black, .7)
        c.line(0, self._toco_paper_height, self._paper_plot_width, self._toco_paper_height)

    def pgrid(self, c):

        c.setStrokeColor(colors.gray, .4)

        # create grid TOCO + FHR
        # X AXIS
        xaxis = range(0, int(self._paper_width), int(self._paper_speed))

        path = c.beginPath()
        path.moveTo(0 * cm, 0 * cm)

        for x in xaxis:
            path.moveTo(x * cm, 0)
            path.lineTo(x * cm, self._paper_plot_height)

        # Y AXIS (step one cm, expect integer size of plot)
        # yaxis = range(0, int(self._paper_height))
        # path.moveTo(0 * cm, self._toco_paper_height)
        # for y in yaxis:
        #     path.moveTo(0, y * cm)
        #     path.lineTo(self._paper_plot_width, y * cm)

        # TOCO
        for i in range(0, len(self._toco_axis)):
            path.moveTo(0, i * self._toco_step)
            path.lineTo(self._paper_plot_width, i * self._toco_step)

        # FHR
        offset_paper = (10 * cm / self._paper_bpm)  # below the min y axis values, there is addtional 10 bpm
        offset = self._toco_paper_height + offset_paper
        for i in range(0, len(self._fhr_axis)):
            path.moveTo(0, i * cm + offset)
            path.lineTo(self._paper_plot_width, i * cm + offset)

        c.drawPath(aPath=path, stroke=1, fill=0)

    def pyaxis(self, c):

        shift1 = -self._axis_space - 2
        shift2 = 4
        c.translate(self._axis_space, 0)

        # TOCO
        for i in range(0, len(self._toco_axis)-1):
            c.drawRightString(shift1, i * self._toco_step - shift2, '{0}'.format(self._toco_axis[i]))

        # FHR
        offset = self._toco_paper_height + (10 * cm / self._paper_bpm) - shift2
        for i in range(0, len(self._fhr_axis)):
            c.drawRightString(shift1, i * cm + offset, '{0}'.format(self._fhr_axis[i]))

        c.translate(-self._axis_space, 0)

    def pxaxis(self, c, nfrom=0, nto=0):

        c.setStrokeColor(colors.black, 1)
        ox = .4*cm
        oy = .2*cm

        c.translate(0, -self._axis_space + oy)

        ind = np.logical_and(nfrom <= self._time_ticks, self._time_ticks < nto)
        ind = np.where(ind)[0]

        for i in ind:
            x = self._time_ticks[i]
            qtime = QTime.fromString(self._time_string[x], "hh:mm:ss:zzz")

            # self._time_plot[nfrom] - shift axis to begin (for more than 1 pae)
            c.drawString(self._time_plot[x]-self._time_plot[nfrom]-ox, 0, str(qtime.toString("hh:mm")))

        c.translate(0, +self._axis_space - oy)

    def ptitle(self, c, page=0, nr_pages=0):

        oy = 0.1 * cm
        c.translate(0, self._paper_plot_height + oy)

        qtime = QTime.fromString(self._time_string[-1], "hh:mm:ss:zzz")
        # stime = qtime.toString("hh:mm")
        stime = qtime.toString("h") + "h" + qtime.toString("mm")

        text = "Record name: {0}; duration: {1}; page: {2}/{3}".format(self._record_name, stime, page, nr_pages)
        d = stringWidth(text, self._default_font_name, self._default_font_size)
        c.drawString(self._paper_plot_width - d - 1, 0, text)

        c.translate(0, -self._paper_plot_height-oy)

    def pfhr(self, c, nfrom=0, nto=0):
        """
        Print FHR signal. First translate the (0,0) of the canvas to FHR plot (do not forget to put it back afterwards).
        Then plot the signal adjusted to have proper CTG resolution.
        """
        if nto == 0:
            nto = len(self._time_plot)

        c.translate(0, self._toco_paper_height)
        c.setStrokeColor(colors.black, 1)

        # path = c.beginPath()
        # path.moveTo(self._time_plot[0], self._fhr_plot[nfrom])
        #
        # d = nto - nfrom  # need to keep the x-axis the same at each page
        # for xi, yi in zip(self._time_plot[0:d], self._fhr_plot[nfrom:nto]):
        #     path.lineTo(xi, yi)
        #
        # c.drawPath(aPath=path, stroke=1, fill=0)

        # SKIP ARTEFACTS
        d = nto - nfrom  # need to keep the x-axis the same at each page
        t = self._time_plot[0:d]
        y = self._fhr_plot[nfrom:nto]

        cnt = 0
        while cnt < len(y):

            bdrawingpath = False
            while cnt < len(y) and not y[cnt] == 0:

                if bdrawingpath is False:
                    path = c.beginPath()
                    path.moveTo(t[cnt], y[cnt])
                    bdrawingpath = True
                    cnt += 1
                    continue

                path.lineTo(t[cnt], y[cnt])
                cnt += 1

            if bdrawingpath:
                c.drawPath(aPath=path, stroke=1, fill=0)
            else:
                cnt += 1

        c.translate(0, -self._toco_paper_height)

    def ptoco(self, c, nfrom=0, nto=0):
        """
        Print TOCO signal
        """

        if nto == 0:
            nto = len(self._time_plot)

        c.setStrokeColor(colors.black, 1)
        path = c.beginPath()
        path.moveTo(0, 0)

        d = nto - nfrom  # need to keep the x-axis the same at each page
        for xi, yi in zip(self._time_plot[0:d], self._toco_plot[nfrom:nto]):
            path.lineTo(xi, yi)

        c.drawPath(aPath=path, stroke=1, fill=0)

    def pannotation(self, c, nfrom=0, nto=0):

        if nto == 0:
            nto = len(self._time_plot)

        c.setStrokeColor(colors.black)

        for key, curve in self._ann.iteritems():

            # if not isinstance(curve, PyQwtPlotCurveAnnotator):
            #     continue
            # #

            if not curve.get_curve_type() in self._ann_names_to_print:
                continue

            x1 = curve.x_from
            x2 = curve.x_to
            y1 = curve.yval1
            y2 = curve.yval2

            # x1_orig = x1
            # x2_orig = x2

            # check whether an annotation should be plotted in the current window
            if x2 < nfrom or x1 > nto:
                # print 'continue'
                continue

            # print nfrom, nto, x1, x2

            if curve.get_parent_name() == EnumAnnType.plot_fhr:
                c.translate(0, self._toco_paper_height)
                # continue

            # PEN, COLOR, SYMBOL
            pen = curve.get_default_pen()
            color = pen.color().getRgb()
            symbol = curve.get_symbol()

            alpha = color[3] / float(255)

            c.setStrokeColorRGB(color[0] / 255, color[1] / 255, color[2] / 255, alpha=alpha)
            c.setDash(self._line_solid)

            if pen.style() == Qt.Qt.DotLine:
                c.setDash(self._line_dash)

            w_symbol = symbol.size().width() / 2

            if isinstance(curve, PyQwtPlotCurveAnnotator):

                # this have to be here - before shift to begin
                plot_begin_marker = plot_end_marker = True
                if x1 < nfrom:
                    x1 = nfrom
                    plot_begin_marker = False

                if x2 > nto:
                    x2 = nto
                    plot_end_marker = False

                # shift annotation to begin at plotting area
                if nfrom > 0:
                    x1 -= nfrom
                    x2 -= nfrom

                c.setLineWidth(pen.width() - self._line_width_adjust)

                x1, x2, y1, y2 = self.adjust_xy_vals(x1, x2, y1, y2, curve.get_parent_name())
                c.line(x1, y1, x2, y2)

                # draw markers
                color = symbol.pen().color().getRgb()
                c.setStrokeAlpha(color[3]/float(255))
                c.setDash(self._line_solid)
                if plot_begin_marker:
                    c.line(x1, y1 - w_symbol, x1, y2 + w_symbol)

                if plot_end_marker:
                    c.line(x2, y1 - w_symbol, x2, y2 + w_symbol)

            elif isinstance(curve, PyQwtPlotMarkerAnnotator):

                if nfrom > 0:
                    x1 -= nfrom
                    x2 -= nfrom

                # shift annotation to begin at plotting area
                x1, x2 = self.adjust_x_vals(x1, x2)
                self.pann_note(c, curve, x1, self._paper_plot_width, 0)

            elif isinstance(curve, PyQwtPlotEllipseAnnotator):

                if nfrom > 0:
                    x1 -= nfrom
                    x2 -= nfrom

                c.setLineWidth(pen.width() - self._line_width_adjust)
                x1, x2, y1, y2 = self.adjust_xy_vals(x1, x2, y1, y2, curve.get_parent_name())

                # ellipse
                color = curve.brush.color().getRgb()
                alpha = color[3] / float(255)
                c.setFillColorRGB(color[0] / 255, color[1] / 255, color[2] / 255, alpha=alpha)

                # print self._paper_plot_width
                # print x_plot_from, x_plot_to, x1, x2, y1, y2

                self.draw_ellipse(c, x1, y1, x2, y2, 0, self._paper_plot_width)

                # line + wrapping rectangle + text
                if curve.get_curve_type() == EnumAnnType.ellipsenote and len(curve.get_text()) > 0 \
                        and x1 > 0:
                    y_min = curve.yval1 + (curve.yval2 - curve.yval1)
                    self.pann_note(c, curve, x1, self._paper_plot_width, y_min)

            if curve.get_parent_name() == EnumAnnType.plot_fhr:
                c.translate(0, -self._toco_paper_height)

        # c.translate(0, -self._toco_paper_height)

    def pann_note(self, c, curve, x1, x_plot_to, y_min=0):
        """
        Print text/ellipse not. This function print line, wrapping rectangle and text
        :type curve PyQwtPlotMarkerAnnotator, PyQwtPlotEllipseAnnotator
        """
        if curve.get_parent_name() == EnumAnnType.plot_fhr:
            y_max = self._fhr_paper_height
        else:
            y_max = self._toco_paper_height

        c.setFillColor(colors.black, 1)
        text = curve.get_text()
        pen = curve.get_default_pen()
        lines = text.split("\n")

        h = len(lines) * self._default_font_size
        w = [stringWidth(s, self._default_font_name, self._default_font_size) for s in lines]
        w = max(w)

        # horizontal line
        c.setStrokeAlpha(curve.pdf_alpha_line)
        c.setLineWidth(pen.width())
        c.line(x1, y_min, x1, y_max)

        margin = 4  # margin of text in a rectangle

        # WRAPPING rectangle
        # if the rectangle would be between two pages
        if x1 + w + margin > x_plot_to:
            x1 = x1 - w - margin

        c.setStrokeAlpha(0)
        c.setFillAlpha(curve.pdf_alpha_rect)
        c.rect(x1, y_max - h - margin, w + margin, h + margin, fill=1)

        # text
        c.setStrokeColor(colors.black, 1)
        c.setFillAlpha(1)
        font_size = self._default_font_size - 1
        c.setFont(self._default_font_name, font_size)

        if curve.get_parent_name() == EnumAnnType.plot_fhr:
            offset_from_top = self._fhr_paper_height - font_size - margin / 2
        else:
            offset_from_top = self._toco_paper_height - font_size - margin / 2

        # text
        cnt = 0  # cnt urcuje take radkovani
        for l in lines:
            c.drawString(x1 + margin / 2, offset_from_top - cnt * font_size, l.strip())
            cnt += 1.1

    def pbackgorund(self, c, bfill=1):

        paper_w_px = self._paper_plot_width

        # c.fill
        c.setStrokeColor(colors.black, 0)
        c.setFillColor(colors.gray, .1)
        c.rect(0, 0, width=paper_w_px, height=self._toco_paper_height, fill=bfill)

        if self._paper_format == EnumPaperFormat.EU:
            c.setFillColor(colors.red, .1)
            c.rect(0, self._toco_paper_height, width=paper_w_px, height=1.5 * cm, fill=bfill)
            c.rect(0, self._toco_paper_height + .5 * cm + 6 * cm, width=paper_w_px, height=1.5 * cm, fill=bfill)

            c.setFillColor(colors.yellow, .2)
            c.rect(0, self._toco_paper_height + 1.5 * cm, width=paper_w_px, height=1.5 * cm, fill=bfill)
            c.rect(0, self._toco_paper_height + 5 * cm, width=paper_w_px, height=1.5 * cm, fill=bfill)
        else:
            c.setFillColor(colors.red, .1)
            o = 10 / float(self._paper_bpm)
            c.rect(0, self._toco_paper_height, width=paper_w_px, height=2 * cm, fill=bfill)
            c.rect(0, self._toco_paper_height + (5 + o) * cm, width=paper_w_px, height=2 * cm, fill=bfill)

            c.setFillColor(colors.yellow, .2)
            c.rect(0, self._toco_paper_height + 2 * cm, width=paper_w_px, height=1 * cm, fill=bfill)
            c.rect(0, self._toco_paper_height + (4 + o) * cm, width=paper_w_px, height=1 * cm, fill=bfill)

        c.setStrokeColor(colors.black, 1)
        c.setFillColor(colors.black, 1)

    def print_(self):

        # margin = self._margin
        # axis_space = self._axis_space
        # paper_width_px = self._paper_plot_width
        # paper_height_px = self._paper_plot_height

        self.__continue_print = True

        self.adjust_signals_for_plot()

        c = canvas.Canvas(self._file_name, pagesize=[self._paper_width, self._paper_height])
        c.setFont(self._default_font_name, self._default_font_size)

        k = self.number_of_pages_to_print()
        w = self._paper_plot_width

        for i in range(0, k):

            if self.__continue_print is False:
                return

            c.setFont(self._default_font_name, self._default_font_size)

            ibegin = i*w
            iend = (i+1)*w
            ind = np.logical_and(ibegin <= self._time_plot, self._time_plot < iend)
            ind = np.where(ind)[0]
            # print ind[0], ind[-1]

            self.ppaper(c)
            self.ptitle(c, i+1, k)
            self.pxaxis(c, ind[0], ind[-1])
            self.pfhr(c, ind[0], ind[-1])
            self.ptoco(c, ind[0], ind[-1])
            self.pannotation(c, ind[0], ind[-1])
            c.showPage()

            self.nr_pages_processed.emit(i+1)

        c.save()

    def number_of_pages_to_print(self):

        self.adjust_signals_for_plot()
        k = self._time_plot[-1] / float(self._paper_plot_width)
        k = int(k + 1)
        return k

    def adjust_xy_vals(self, x1, x2, y1, y2, parent_name):
        """
        """
        x1, x2 = self.adjust_x_vals(x1, x2)
        y1, y2 = self.adjust_y_vals(y1, y2, parent_name)
        return x1, x2, y1, y2

    def adjust_x_vals(self, x1, x2):
        x1 /= self._adj_x
        x2 /= self._adj_x
        return x1, x2

    def adjust_y_vals(self, y1, y2, parent_name):
        """
        Adjust the y values of FHR/TOCO to fit into the printed area
        :param y1: the first y coordinate
        :param y2: the second y coordinate
        :param parent_name: either FHR or TOCO (defined using EnumAnnType)
        :return: adjusted value
        """

        if y2 is None:
            y2 = y1

        if parent_name == EnumAnnType.plot_fhr:
            y1 -= self._fhr_min_val
            y2 -= self._fhr_min_val
            y1 *= self._adj_y1
            y2 *= self._adj_y1
        else:
            y1 *= self._adj_y2
            y2 *= self._adj_y2

        return y1, y2

    def draw_ellipse(self, c, x1, y1, x2, y2, x_from, x_to):

        a = float(np.abs(x2 - x1))/2
        b = float(np.abs(y2 - y1))/2

        xi = np.arange(-a, a+1, 1)
        yi = np.zeros(len(xi))

        # compute the whole ellipse
        for i in range(0, len(xi)):
            tmp = b * b * (1 - (xi[i] * xi[i] / float(a * a)))
            if tmp >= 0:
                yi[i] = np.sqrt(tmp)

        xi += x1 + a
        # cut the ellipse from the both sides
        ind = np.where(np.logical_and(xi >= x_from, xi <= x_to))[0]
        xi = xi[ind]
        yi = yi[ind]

        # create the upper/ lower ellipse
        xi = np.hstack((xi, xi[::-1]))
        yi = np.hstack((y1 + b + yi, y1 + b - yi[::-1]))

        # draw
        p = c.beginPath()
        p.moveTo(xi[0], yi[0])
        for i in range(0, len(xi)):
            p.lineTo(xi[i], yi[i])
        c.drawPath(p, fill=1)

    def set_paper_size(self, size=A4):
        self._paper_size = size

    def get_file_name(self):
        return self._file_name

    def set_file_name(self, name):
        self._file_name = name

    def set_record_name(self, name):
        self._record_name = name

    def set_ann_to_print(self, ann_names):
        self._ann_names_to_print = ann_names

    def set_signals(self, fhr, toco, fs, timestamp):
        """Set the FHR and TOCO signal"""
        self._fhr = fhr
        self._toco = toco
        self._fs = fs
        self._timestamp = timestamp

    def adjust_signals_for_plot(self):
        """This function needs to be called just prior to print. To adjust the signals to printable area"""
        fhr = self._fhr
        toco = self._toco
        fs = self._fs
        timestamp = self._timestamp

        """ set signals for plot """
        self._fhr_plot = np.array(fhr)
        self._fhr_plot -= self._fhr_min_val

        with np.errstate(invalid='ignore'):
            self._fhr_plot[self._fhr_plot < 0] = 0

        self._adj_y1 = self._fhr_paper_height / (self._fhr_max_val - self._fhr_min_val)
        self._adj_y2 = self._toco_paper_height / self._toco_max_val

        # make x axis for plot (to ensure 1cm/min or 3cm/min)
        number_cm = self._paper_plot_width / cm / self._paper_speed  # number of samples per centimeter
        self._adj_x = number_cm * self._fs * 60 / self._paper_plot_width  # number of samples for the plot width / plot width

        nr_samples = len(self._fhr)
        self._time_string = samples2time(nr_samples, self._fs)
        self._time_ticks = time_locator(self._time_string, self._locator_minute, -1, self._timestamp[-1], fs)

        self._fhr_plot *= self._adj_y1
        self._toco_plot = np.array(toco) * self._adj_y2
        self._time_plot = np.array(timestamp) / self._adj_x

    def set_annotations(self, ann):
        self._ann = ann

    def set_paper_format(self, pformat=EnumPaperFormat.EU):

        self._paper_format = pformat

        if pformat == EnumPaperFormat.EU:
            self.__set_paper_eu()
        else:
            self.__set_paper_us()

        w, dummy = landscape(self._paper_size)  # keep for later
        self._paper_plot_width = int((w - self._axis_space - 2 * self._margin) / cm) * cm  #
        self._paper_width = self._axis_space + self._paper_plot_width + 2 * self._margin

        self._paper_height = self._title_space + self._fhr_paper_height + self._toco_paper_height + \
                             self._axis_space + 2 * self._margin

        self._paper_plot_height = self._fhr_paper_height + self._toco_paper_height

        self._toco_step = self._toco_paper_height / (self._toco_max_val / self._toco_resolution)
        self._toco_axis = range(0, self._toco_max_val + 1, self._toco_resolution)

        offset = 10
        self._fhr_step = self._fhr_paper_height / self._paper_bpm
        self._fhr_axis = range(self._fhr_min_val + offset, self._fhr_max_val + 1, self._paper_bpm)

    def __set_paper_eu(self):
        self._paper_speed = EnumPlotSpeed.oneCmMin
        self._paper_bpm = EnumPlotBpm.twentyBpmCm

        self._locator_minute = 5

        self._fhr_min_val = 50
        self._fhr_max_val = 210

        self._paper_size = A4  # EU
        self._toco_resolution = 20

        self._fhr_paper_height = 8 * cm  # EU
        self._toco_paper_height = 2.5 * cm  # EU

    def __set_paper_us(self):
        self._paper_speed = EnumPlotSpeed.threeCmMin
        self._paper_bpm = EnumPlotBpm.thirtyBpmCm
        # self._paper_speed = EnumPlotSpeed.oneCmMin

        self._locator_minute = 1

        self._fhr_min_val = 20
        self._fhr_max_val = 240

        self._paper_size = letter
        self._toco_resolution = 20

        o = 10/float(self._paper_bpm)
        self._fhr_paper_height = (7 + o) * cm
        self._toco_paper_height = 2.5 * cm

    def stop_print(self):
        self.__continue_print = False


def main():

    import sys
    app = QtGui.QApplication(sys.argv)

    e = ExportToPdfForm()
    e.set_paper_format(EnumPaperFormat.EU)

    #  READ CTG DATA
    # sfile = '/home/jirka/data/CTU_UHB_physionet/1001.dat'
    sfile = '/home/jirka/data/data_barry_schifrin_final/EHA1469_2010.mat'
    # sfile = 'e:\data\data_barry_schifrin_final\EHA0389_2007.mat'
    adata = temporary_read_data(sfile)
    fhr = adata[EnumVariableName.fhr]
    uc = adata[EnumVariableName.uc]
    timestamp = adata[EnumVariableName.timestamp]
    fs = 4

    e.cprint.set_signals(fhr, uc, fs, timestamp)

    from Annotator import Annotator
    annotator = Annotator()
    annotator.ann_file_load(sfile)
    e.cprint.set_annotations(annotator.get_annotations_copy_all())

    e.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
