# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import sys, logging
from PyQt4 import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QApplication
import numpy as np
from scipy.signal import decimate
from scipy.interpolate import interp1d

from Annotator import Annotator
from PyQwtNavigationPlot import PyQwtNavigationPlot
from PyQwtWidgetGui import FhrPlot
from PyQwtWidgetGui import TocoPlot
from Config import ConfigStatic
from Common import remove_nans_at_begin_and_end, samples2time


class PlotWidget(QWidget):
    """

        * parent
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._log = logging.getLogger(ConfigStatic.logger_name)
        self._log.info('passed')

        # self.setMinimumSize(600, 600)
        self.setMinimumSize(700, 600)
        # self.setMaximumSize(1200,800)
        
        # self._styleManager = styleManager()
        # self._styleManager.setStyleManager(self._styleManager)

        self.annotator = Annotator()

        vbox = QVBoxLayout()

        controled_plots = list()
        self.fhrPlot = FhrPlot(self)
        self.tocoPlot = TocoPlot(self)
        # self.tocoPlot.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

        controled_plots.append(self.fhrPlot)
        controled_plots.append(self.tocoPlot)
        self.navPlot = PyQwtNavigationPlot(self, controled_plots)

        self.__plots_all = [self.fhrPlot, self.tocoPlot, self.navPlot]

        # self.plotTools = PyQwtPlotTools(self, self.fhrPlot, self._styleManager)
        # self.plot.setMargin(5)

        vbox.addWidget(self.fhrPlot)
        vbox.addWidget(self.tocoPlot)
        # vbox.addLayout(self.plotTools.ToolbarHBoxLayout)
        vbox.addWidget(self.navPlot)
        self.setLayout(vbox)
        # self.setCentralWidget(self.fhrPlot)
        # self.setMinimumSize(90, 90)
        # self.setMinimumSize(1000, 100)

        self.fhrPlot.signal_ann_changed.connect(self.update_nav_plot)
        self.tocoPlot.signal_ann_changed.connect(self.update_nav_plot)
        self.fhrPlot.canvas_picker.signal_ann_moved_outside_view.connect(self.ann_moved_outside_view)
        self.tocoPlot.canvas_picker.signal_ann_moved_outside_view.connect(self.ann_moved_outside_view)

    def setSamplingFreqAllPlots(self, fs):
        self.fhrPlot.set_sampling_freq(fs)
        self.tocoPlot.set_sampling_freq(fs)
        self.navPlot.set_sampling_freq(fs)
        # The FHR and TOCO for navigation plot are downsampled below. But we still keep the same sampling frequncy in
        # order to don't mess the navigation and time scale
        # self.navPlot.set_sampling_freq(ConfigStatic.navigation_plot_downsample_fs)

    def plot(self, time_samples, fhr, toco, timestring=None):

        self.clear_all_plots()
        self.fhrPlot.plot(time_samples, fhr, timestring)
        self.tocoPlot.plot(time_samples, toco, timestring)
        # self.navPlot.plot(time_samples, fhr, timestring)

        ''' FHR + TOCO for navigation plot  - artifacts are problem here'''
        # offset = self.navPlot.get_toco_offset()
        # x1= fhr.copy()
        # x1[x1 == 0] = -100
        # self.navPlot.plot(time_samples, x1, timestring)
        # self.navPlot.plot(time_samples, toco + offset, timestring)
        #
        # x1[x1 == 0] = -100
        # self.navPlot.plot(time_samples, x1+50, timestring)
        # self.navPlot.plot(time_samples, toco, timestring)

        ''' Downsampling for navigation plot. Need to interpolate artifacts '''
        fs = self.fhrPlot.get_sampling_freq()
        fs_nav = ConfigStatic.navigation_plot_downsample_fs
        ndecimate = int(fs/fs_nav)

        offset = self.navPlot.get_toco_offset()
        x1_fhr = x1 = fhr.copy()
        x2 = toco.copy()

        dummy, gap_at_begin, gap_at_end, ifrom, ito = remove_nans_at_begin_and_end(x1)

        # interpolace FHR
        ind = np.logical_or(x1 == 0, x1 == -1)
        f = interp1d(time_samples[~ind], x1[~ind])
        x1 = f(time_samples[ifrom:ito])  # remove artefact at begin and end

        if len(gap_at_begin) > 0:
            x1 = np.hstack((gap_at_begin, x1))

        if len(gap_at_end) > 0:
            x1 = np.hstack((x1, gap_at_end))

        # downsample
        x1 = decimate(x1, ndecimate)
        x2 = decimate(x2, ndecimate)

        # create new time samples and time string
        time_string_resampled = samples2time(len(x1), fs_nav)
        # time_samples = range(0, len(fhr), ndecimate)
        time_samples = time_samples[::ndecimate]

        # make invisible those values that were interpolated across artifacts (0 or -1)
        ind = np.where(np.logical_or(x1_fhr == 0, x1_fhr == -1))[0]
        for i in ind:
            ii = int(i/ndecimate)
            try:
                x1[ii] = 2 * offset
                if ii > 3:
                    x1[ii - 4:ii] = 2 * offset
                if ii < len(x1) - 3:
                    x1[ii:ii + 4] = 2 * offset
            except:
                self._log.warning('Index outside of range ')

        # print ind
        # for t in time_samples:
        #     if x1_fhr[t] == 0 or x1_fhr[t] == -1:
        #
        #         i = time_samples.index(t)
        #         # print t, i, t/float(i)
        #         x1[i] = 2*offset
        #
        #         if i > 3:
        #             x1[i-4:i] = 2*offset
        #         if i < len(x1) - 3:
        #             x1[i:i+4] = 2*offset

        # make invisible first values (transition effect of the decimate filter)
        x1[ifrom:ifrom+5] = 2*offset

        self.navPlot.plot(time_samples, x1, time_string_resampled)
        self.navPlot.plot(time_samples, x2 + offset, time_string_resampled)

    def plot_stage1_line(self, pos_samp):
        for p in self.__plots_all:
            p.plot_first_stage_line(pos_samp)

    def plot_stage2_line(self, pos_samp):
        for p in self.__plots_all:
            p.plot_second_stage_line(pos_samp)

    def plot_birth_line(self, pos_samp):
        for p in self.__plots_all:
            p.plot_bith_line(pos_samp)

    # def plot_baseline_constant(self, val):
    #     self.fhrPlot.plot_baseline_constant(val)

    def clear_all_plots(self):
        for p in self.__plots_all:
            p.clear_plot()

    def updatePlots(self):
        self.fhrPlot.updateAxis()
        self.tocoPlot.updateAxis()
        # self.navPlot.setXAxis()
        self.navPlot.updateAxis()
        self.navPlot.correct_point_boundaries()

    def set_paper_eu(self):
        self.fhrPlot.set_paper_eu()
        self.tocoPlot.set_paper_eu()
        # self.navPlot.set_paper_eu()
        self.updatePlots()

    def set_paper_us(self):
        self.fhrPlot.set_paper_us()
        self.tocoPlot.set_paper_us()
        # self.navPlot.set_paper_us()
        self.updatePlots()

    def set_ann_action(self, action):
        self.fhrPlot.set_ann_action(action)
        self.tocoPlot.set_ann_action(action)

    def ann_file_load_and_plot(self, sfile):
        self.annotator.ann_file_load(sfile)
        self.ann_set_and_plot()

    def ann_set_and_plot(self):
        self.fhrPlot.ann_set_and_plot(self.annotator.get_annotations_fhr())
        self.tocoPlot.ann_set_and_plot(self.annotator.get_annotations_toco())
        self.navPlot.ann_set(self.annotator.get_annotations_copy_all())
        self.navPlot.plot_ann_navplot_marker()

    def delete_annotations(self):
        self.fhrPlot.ann_delete_all()
        self.tocoPlot.ann_delete_all()
        self.navPlot.ann_delete_all()

    def ann_save(self):
        dfhr = self.fhrPlot.ann_get()
        dtoco = self.tocoPlot.ann_get()
        self.annotator.set_annotations_and_save(dfhr, dtoco)

    def ann_show(self, bshow=True):
        self.fhrPlot.ann_plot_curves(bshow)
        self.tocoPlot.ann_plot_curves(bshow)
        self.navPlot.plot_ann_navplot_marker(bshow)

    def ann_moved_outside_view(self, step):
        if step > 0:
            self.navPlot.change_selected_pointright(step)
        else:
            self.navPlot.change_selected_pointleft(abs(step))

    def update_nav_plot(self):
        # self.navPlot.ann_set(self.annotator.get_annotations_copy())
        self.navPlot.ann_set(self.annotator.get_annotations_copy_all())
        self.navPlot.plot_ann_navplot_marker()

    def resizeEvent(self, ev):
        self.updatePlots()

    def keyPressEvent(self, event):

        if event.key() == Qt.Qt.Key_Left:
            self.navPlot.change_selected_pointleft()

        if event.key() == Qt.Qt.Key_Right:
            self.navPlot.change_selected_pointright()

        return QWidget.keyPressEvent(self, event)

    def wheelEvent(self, event):

        if event.delta() > 0:
            self.navPlot.change_selected_pointleft()
        elif event.delta() < 0:
            self.navPlot.change_selected_pointright()

        return QWidget.wheelEvent(self, event)

    def mousePressEvent(self, event):
        # print 'mpress'
        return QWidget.mousePressEvent(self, event)


def main():
    app = QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    window.updatePlots()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
