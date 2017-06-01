# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @author: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

"""
MainWindow
----------------

The MainWindow module is the main class that provides interaction between GUI and the user.
This class integrates all the other functionality.

Reference
~~~~~~~~~~~
.. autoclass:: Main
    :members:
    :private-members:
"""

# system imports
import argparse
from PyQt4 import QtCore

from PyQt4.QtCore import pyqtSlot, QSignalMapper

import Common
from ClinInfoForm import ClinInfo
from Config import ConfigStatic, ConfigIni
from DataBrowserForm import DataBrowserForm
from DataBrowserSelectAttrForm import DataBrowserSelectAttrForm
from Enums import EnumAnnType, EnumPaperFormat, EnumVariableName as EnumVarName, EnumIniVar
from GuiForms import *
from Init import init
from LoadWriteData import LoadData
from MainWindowUI import Ui_MainWindow
from Print import ExportToPdfForm

DEBUG_PROFILE = False
DEBUG_FIGO_ANN = False
DEBUG_MISC = True
DEBUG_TOOLS = True

# conditional import
if DEBUG_PROFILE:
    import cProfile
    import pstats


class Main(QtGui.QMainWindow):

    def __init__(self, args=sys.argv):
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._winTitleDefault = str(self.windowTitle())

        self._log = logging.getLogger(ConfigStatic.logger_name)
        self._log.info('passed')
        self._log.info('profiling: {0}'.format(DEBUG_PROFILE))

        self._dataLoader = LoadData()

        self._config_ini = ConfigIni()
        self._convertFilesForm = ConvertFileForm()
        self._downloadDbForm = DownloadDbForm()
        self._attSelectForm = DataBrowserSelectAttrForm(self._config_ini)
        self._sent_ann_form = SentAnnotationsForm(self._config_ini)
        self._export_to_pdf_form = ExportToPdfForm()
        # self._ann_show_hide_form = AnnShowHide(self._config_ini)

        # dock widgets
        self._clinInfoWidget = ClinInfo()
        self._clinInfoWidget.clear_all()
        self.ui.dockClinInfo.setWidget(self._clinInfoWidget)

        self._dataBrowserWidget = DataBrowserForm()
        self.ui.dockDataBrowser.setWidget(self._dataBrowserWidget)
        self._dataBrowserWidget.plotFileSignal.connect(self.plot_file)
        # self._dataBrowserWidget.debug_stageI_signal.connect(self.debug_plot_stage1)

        valr = self._config_ini.get_var(EnumIniVar.annotationToolbarAlignR)
        self.ui.actionAnnToolbarAlign_right.setChecked(valr)
        self._toolbar_align()

        # self.ui.actionSent_annotations.setEnabled(False)

        self._create_connections()

        self._signal_data = dict()

        self.msgbox_unsaved = QtGui.QMessageBox()
        self.msgbox_unsaved.setText("There are unsaved changes in annotations.")
        self.msgbox_unsaved.setInformativeText("Save now?")
        self.msgbox_unsaved.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard)
        self.msgbox_unsaved.setDefaultButton(QtGui.QMessageBox.Save)
        self.msgbox_unsaved.setIcon(QtGui.QMessageBox.Critical)

        self.msgbox_delete = QtGui.QMessageBox()
        self.msgbox_delete.setText("Are you sure to delele all annotations?")
        self.msgbox_delete.setInformativeText("All annotations will be lost. This can't be undone.")
        self.msgbox_delete.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self.msgbox_delete.setDefaultButton(QtGui.QMessageBox.Save)
        self.msgbox_delete.setIcon(QtGui.QMessageBox.Warning)

        self.msgbox_err = QtGui.QMessageBox()
        self.msgbox_err.setStandardButtons(QtGui.QMessageBox.Ok)
        self.msgbox_err.setDefaultButton(QtGui.QMessageBox.Ok)
        self.msgbox_err.setIcon(QtGui.QMessageBox.Critical)

        if self._export_to_pdf_form.reportlab_imported:
            self.ui.actionExport_to_PDF.setEnabled(True)
        else:
            self.ui.actionExport_to_PDF.setEnabled(False)
            self.ui.actionExport_to_PDF.setToolTip('Export to PDF disabled')

        self._process_cmd_args(args)

        # paper format
        self._set_paper_format(self._config_ini.get_var(EnumIniVar.paperformat))

        # self._save_to_pdf2()
        valg = QtCore.QByteArray(self._config_ini.get_var(EnumIniVar.windowGeometry))
        vals = QtCore.QByteArray(self._config_ini.get_var(EnumIniVar.windowState))
        self.restoreGeometry(valg)
        self.restoreState(vals)

        if len(vals) == 0:
            self.ui.dockDataBrowser.setVisible(False)
            self.ui.dockClinInfo.setVisible(False)
            self.ui.toolBar.setVisible(False)

        self._dock_clin_info_visibility()
        self._dock_databrowse_visibility()
        self._toolbar_ann_visibility()

        self.ui.actionCaliper.setChecked(self._config_ini.get_var(EnumIniVar.caliperVisible))
        self.ui.actionCaliperFHR.setChecked(self._config_ini.get_var(EnumIniVar.caliperFHR))
        self.ui.actionCaliperTOCO.setChecked(self._config_ini.get_var(EnumIniVar.caliperTOCO))
        self._caliper_set()

        if DEBUG_TOOLS is True:
            self.menuDebug = QtGui.QMenu(self.ui.menubar)
            self.menuDebug.setTitle('Debug')
            self.menuDebug.addAction(self.ui.actionDebug_CalibSignal)
            self.ui.menubar.addAction(self.menuDebug.menuAction())

    def _create_connections(self):
        """ Creates connections in MainWindow """

        # TODO rewrite the connection to a modern style
        # Menu: File
        self.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.connect(self.ui.actionOpen, QtCore.SIGNAL('triggered()'), self._open_file)
        self.connect(self.ui.actionOpen_folder, QtCore.SIGNAL('triggered()'), self._open_folder_dialog)

        # Menu: TOOLS
        self.connect(self.ui.actionConvert_files, QtCore.SIGNAL('triggered()'), self._show_convert_files)
        self.connect(self.ui.actionDownload_CTU_UHB_data, QtCore.SIGNAL('triggered()'), self._show_download_db)
        self.connect(self.ui.actionAttribute_selection, QtCore.SIGNAL('triggered()'), self._show_attribute_selection)
        self.connect(self.ui.actionExport_to_PDF, QtCore.SIGNAL('triggered()'), self._export_to_pdf)
        # self.connect(self.ui.actionSet_Clear_Baseline, QtCore.SIGNAL('triggered()'), self._show_set_clear_bsln)
        self.connect(self.ui.actionSent_annotations, QtCore.SIGNAL('triggered()'), self._show_sent_annotations)

        group_paper = QtGui.QActionGroup(self)
        self.ui.actionEU.setActionGroup(group_paper)
        self.ui.actionUS.setActionGroup(group_paper)
        self.connect(self.ui.actionEU, QtCore.SIGNAL('triggered()'), self._set_paper)
        self.connect(self.ui.actionUS, QtCore.SIGNAL('triggered()'), self._set_paper)

        ''' create dictionary in the following format: action: name '''
        e = EnumAnnType
        pui = self.ui
        dactions = {pui.actionCursor: e.select, pui.actionBasal: e.basal, pui.actionBaseline: e.baseline,
                    pui.actionRecovery: e.recovery, pui.actionNo_recovery: e.no_recovery,
                    pui.actionExcessive_UA: e.excessive_ua, pui.actionEllipse: e.ellipse,
                    pui.actionEllipseNote: e.ellipsenote, pui.actionNote: e.note,
                    pui.actionEvaluationNote: e.evaluation_note}

        if DEBUG_FIGO_ANN:
            dactions[pui.actionFloating_Baseline] = e.floating_baseline
            dactions[pui.actionAcceleration] = e.acceleration
            dactions[pui.actionDeceleration] = e.deceleration
            dactions[pui.actionUA] = e.uterine_contraction

        group_ann = QtGui.QActionGroup(self)
        for action in dactions.iterkeys():
            if isinstance(action, QtGui.QAction):  # just to check the type
                action.setActionGroup(group_ann)

        # self.ui.actionBasal.triggered.connect(self._debug_slot)
        # self.ui.actionBaseline.triggered.connect(self._set_annotation_action)

        signal_mapper = QSignalMapper(self)

        # signal_mapper.setMapping(self.ui.actionBaseline, 'baseline')
        # self.connect(self.ui.actionBaseline, QtCore.SIGNAL('triggered()'), signal_mapper.map)
        # self.connect(signal_mapper, QtCore.SIGNAL('mapped()'), self._set_annotation_action)

        # for d in dactions.iteritems():
        for action, name in dactions.iteritems():
            signal_mapper.setMapping(action, name)

            if isinstance(action, QtGui.QAction):  # just to check the type
                action.triggered.connect(signal_mapper.map)
                # self.connect(action, QtCore.SIGNAL('triggered()'), signal_mapper.map)

        signal_mapper.mapped[QtCore.QString].connect(self._ann_set_action)
        # self.connect(self.ui.actionUS, QtCore.SIGNAL('triggered()'), self._set_paper)
        # self.connect(signal_mapper, QtCore.SIGNAL('mapped()'), self._set_annotation_action)

        # signal_mapper = QtCore.QSignalMapper(self)
        #
        # # for d in dactions.iteritems():
        # for action, name in dactions.iteritems():
        #     signal_mapper.setMapping(action, name)
        #
        #     if isinstance(action, QtGui.QAction):  # just to check the type
        #         # action.triggered.connect(signal_mapper.map)
        #         self.connect(action, QtCore.SIGNAL('triggered()'), signal_mapper.map)
        #
        # # signal_mapper.mapped[QtCore.QString].connect(self._set_annotation_action)
        # # self.connect(self.ui.actionUS, QtCore.SIGNAL('triggered()'), self._set_paper)
        # self.connect(signal_mapper, QtCore.SIGNAL('mapped()'), self._set_annotation_action)

        # self.ui.actionAnnShowHide.triggered.connect(self._show_ann_show_hide)
        self.connect(self.ui.actionSave, QtCore.SIGNAL('triggered()'), self._toolbar_ann_save)
        self.connect(self.ui.actionDelete, QtCore.SIGNAL('triggered()'), self._toolbar_ann_delete)

        self.ui.actionCaliper.triggered.connect(self._caliper_set)
        self.ui.actionCaliperFHR.triggered.connect(self._caliper_set)
        self.ui.actionCaliperTOCO.triggered.connect(self._caliper_set)

        self.ui.actionFIGO_acc_dec.triggered.connect(self._caliper_set_figo_acc_dec)
        self.ui.actionFIGO_UA.triggered.connect(self._caliper_set_figo_ua)
        self.ui.actionCaliperReset.triggered.connect(self._caliper_reset)

        # Menu: View
        self.connect(self.ui.actionClinical_information, QtCore.SIGNAL('triggered()'), self._dock_clin_info_toggle)
        self.connect(self.ui.dockClinInfo, QtCore.SIGNAL("visibilityChanged(bool)"), self._dock_clin_info_visibility)
        self.connect(self.ui.actionData_browser, QtCore.SIGNAL('triggered()'), self._dock_databrowse_toggle)
        self.connect(self.ui.dockDataBrowser, QtCore.SIGNAL("visibilityChanged(bool)"),
                     self._dock_databrowse_visibility)
        self.connect(self.ui.actionAnnToolbarVisible, QtCore.SIGNAL('triggered()'), self._toolbar_ann_toggle)
        self.connect(self.ui.toolBar, QtCore.SIGNAL('visibilityChanged(bool)'), self._toolbar_ann_visibility)
        self.connect(self.ui.actionAnnToolbarAlign_right, QtCore.SIGNAL('triggered()'), self._toolbar_align)

        # Menu: Help
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self._show_about)

        # SIGNALS
        self.ui.PlotWidget.fhrPlot.signal_ann_changed.connect(self._toolbar_ann_changed)
        self.ui.PlotWidget.tocoPlot.signal_ann_changed.connect(self._toolbar_ann_changed)
        self._attSelectForm.signal_sel_att_changed.connect(self._update_data_browser)

        if DEBUG_TOOLS is True:
            self.ui.actionDebug_CalibSignal.triggered.connect(self.plot_calibration_signal)

    def _dock_clin_info_visibility(self):
        """ Clinical information dock visibility has changed, set the property of checkbox"""
        self.ui.actionClinical_information.setChecked(self.ui.dockClinInfo.isVisible())

    def _dock_clin_info_toggle(self):
        """ Set clinical information dock widget visible or invisible  """
        if self.ui.actionClinical_information.isChecked():
            self.ui.dockClinInfo.show()
        else:
            self.ui.dockClinInfo.hide()

    def _dock_databrowse_visibility(self):
        """ Visibility of data browser has changed, set the property of checkbox. """
        self.ui.actionData_browser.setChecked(self.ui.dockDataBrowser.isVisible())

    def _dock_databrowse_toggle(self):
        """ Set docks widget visible or invisible  """
        if self.ui.actionData_browser.isChecked():
            self.ui.dockDataBrowser.show()
        else:
            self.ui.dockDataBrowser.hide()

    def _toolbar_ann_toggle(self):
        """ Set toolbar visible  or invisible  """
        b = True if self.ui.actionAnnToolbarVisible.isChecked() else False
        self.ui.toolBar.setVisible(b)
        self.ui.PlotWidget.ann_show(b)

    def _toolbar_ann_visibility(self):
        self.ui.actionAnnToolbarVisible.setChecked(self.ui.toolBar.isVisible())

    def _toolbar_ann_changed(self):
        """ Annotations were changed. Enable saving button. """
        self.ui.actionSave.setEnabled(True)
        # self._dataBrowserWidget.update_model()

    def _toolbar_ann_save(self):
        self.ui.PlotWidget.ann_save()
        self.ui.actionSave.setEnabled(False)

        # update data browser if annotations are selected
        if ClinInfoForm.annotation_name in self._attSelectForm.get_selected_att():
            self._dataBrowserWidget.update_model_without_sort(self._attSelectForm.get_selected_att())

    def _toolbar_restore_geometry(self):
        self.restoreGeometry(self._valg)

    def _toolbar_ann_delete(self):

        # print self.ui.toolBar.saveGeometry()
        ret = self.msgbox_delete.exec_()

        if ret == QtGui.QMessageBox.Yes:
            self.ui.PlotWidget.delete_annotations()

    def _toolbar_align(self):

        self.ui.toolBar.clear()

        if self.ui.actionAnnToolbarAlign_right.isChecked():
            spacer = QtGui.QWidget()
            spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
            self.ui.toolBar.addWidget(spacer)

        self.ui.toolBar.addAction(self.ui.actionCursor)
        self.ui.toolBar.addAction(self.ui.actionBasal)
        self.ui.toolBar.addAction(self.ui.actionBaseline)
        self.ui.toolBar.addAction(self.ui.actionRecovery)
        self.ui.toolBar.addAction(self.ui.actionNo_recovery)
        self.ui.toolBar.addAction(self.ui.actionExcessive_UA)
        # self.ui.toolBar.addWidget(toolb)
        # self.ui.toolBar.addAction(self.ui.actionEllipse)
        self.ui.toolBar.addAction(self.ui.actionEllipseNote)
        self.ui.toolBar.addAction(self.ui.actionNote)
        self.ui.toolBar.addAction(self.ui.actionEvaluationNote)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionCaliper)
        # self.ui.toolBar.addAction(self.ui.actionAnnShowHide)
        self.ui.toolBar.addAction(self.ui.actionSave)
        self.ui.toolBar.addAction(self.ui.actionDelete)

        qmenu = QtGui.QMenu()
        qmenu.addAction(self.ui.actionCaliperFHR)
        qmenu.addAction(self.ui.actionCaliperTOCO)
        qmenu.addAction(self.ui.actionFIGO_acc_dec)
        qmenu.addAction(self.ui.actionFIGO_UA)
        qmenu.addAction(self.ui.actionCaliperReset)
        self.ui.actionCaliper.setMenu(qmenu)

        if DEBUG_FIGO_ANN:
            self.ui.toolBar.addSeparator()
            self.ui.toolBar.addAction(self.ui.actionFloating_Baseline)
            self.ui.toolBar.addAction(self.ui.actionAcceleration)
            self.ui.toolBar.addAction(self.ui.actionDeceleration)
            self.ui.toolBar.addAction(self.ui.actionUA)
            # self.ui.toolBar.addAction(self.ui.actionAnnShowHide)

    def _ann_check_unsaved_changes(self):

        if self.ui.actionSave.isEnabled():
            ret = self.msgbox_unsaved.exec_()

            if ret == QtGui.QMessageBox.Save:
                self._toolbar_ann_save()
            else:
                self.ui.PlotWidget.delete_annotations()
                self.ui.actionSave.setEnabled(False)

    @pyqtSlot(QtCore.QString)
    def _ann_set_action(self, a=EnumAnnType.select):
        """
        Set what annotation action will be performed.
        The possible actions are defined in :py:class:`EnumAnnType`
        """
        self.ui.PlotWidget.set_ann_action(action=a)

    def _open_file(self):
        """ Open file in gui. Files are filtered based on extension """

        self._ann_check_unsaved_changes()

        val = self._config_ini.get_var(EnumIniVar.lastUsedDirFiles)
        file1 = QtGui.QFileDialog.getOpenFileName(self, 'Open File', val, 'Files (*.dat *.csv *.mat *.txt)')

        if file1 == "":
            self._log.debug("File name is empty - no file selected")
            return -1

        file1 = str(file1)
        dummy, ext = Common.get_filename_and_ext(file1)

        if ext == '.dat' or '.mat':
            self.plot_file(file1)
        elif ext == '.csv':
            self.plot_csv_file(file1)
        elif ext == '.txt':
            self.plot_bditxt_file(file1)

        self._config_ini.set_var(EnumIniVar.lastUsedDirFiles, os.path.dirname(file1))
        return 0

    def _open_folder_data_browser(self, sdir):
        """ Open folder in gui.  """

        self._ann_check_unsaved_changes()
        self.ui.dockDataBrowser.show()
        self.ui.actionData_browser.setChecked(True)

        if not os.path.exists(sdir):
            self._log.error('Chosen directory do not exists: {0}'.format(sdir))

        self._dataBrowserWidget.set_attributes_dir_and_load(self._attSelectForm.get_selected_att(), sdir)
        self._config_ini.set_var(EnumIniVar.lastUsedDirFiles, sdir)
        return 0

    def _open_folder_dialog(self):

        sdir = QtGui.QFileDialog.getExistingDirectory(self, 'Open Folder', self._config_ini.get_var(EnumIniVar.lastUsedDirFiles))
        if sdir == "":
            self._log.debug("Data browser open directory: Name is empty - none selected")
            return -1

        sdir = str(sdir)
        self._open_folder_data_browser(sdir)

    def _get_paper_format(self):
        """
        :return: paper format
        :rtype: str
        """
        if self.ui.actionEU.isChecked():
            return EnumPaperFormat.EU
        else:
            return EnumPaperFormat.US

    def plot_file(self, sfile):
        """
        Plot a CTG file. Also plot the annotations if available.

        :param sfile: input file
        :type sfile: str
        """
        sfile = str(sfile)

        self._ann_check_unsaved_changes()
        self.ui.actionCaliper.setChecked(False)
        self._caliper_set()

        try:
            adata = self._dataLoader.read_data(sfile)
        except Exception as ex:
            self._log.error(ex)
            return

        # self._annotator.set_and_load_ann_file(sfile)

        afhr = adata[EnumVarName.fhr]
        auc = adata[EnumVarName.uc]
        atimestamp = adata[EnumVarName.timestamp]
        fs = adata[EnumVarName.fs]
        nr_samples = len(afhr)

        # TODO - samples2time and used function qtime.toString is a bottle neck!
        time_string = Common.samples2time(nr_samples, fs)
        self.ui.PlotWidget.setSamplingFreqAllPlots(fs)
        self.ui.PlotWidget.plot(atimestamp, afhr, auc, time_string)
        # self.ui.PlotWidget.plot(atimestamp, afhr, auc)

        try:
            self.ui.PlotWidget.ann_file_load_and_plot(sfile)
        except IOError as ex:
            self.msgbox_err.setText('A problem occurred when loading annotations for file: {0}'.format(sfile))
            self.msgbox_err.setInformativeText(ex.message)
            self.msgbox_err.exec_()

        self._signal_data = adata
        self.ui.actionExport_to_PDF.setEnabled(True)

        val = adata.get('Pos_IIst')
        # print(val)
        # print(adata.get('ind_stageII'))
        if val != -1 and val is not None:
            self.ui.PlotWidget.plot_stage2_line(val)
            self.ui.PlotWidget.updatePlots()

        # val = adata.get('obsolete_ind_stageII', None)
        # val = int(val) if val is not None else val
        # if val != -1 and val is not None:
        #     self.ui.PlotWidget.plot_stage1_line(val)
        #     self.ui.PlotWidget.updatePlots()

        val = adata.get('Pos_Birth')
        # print val
        if val != -1 and val is not None:
            self.ui.PlotWidget.plot_birth_line(val)
            self.ui.PlotWidget.updatePlots()

        if 'name' in adata:
            self._set_window_title_rec(adata['name'])

        # clinical information
        self._clinInfoWidget.set_all(adata)

    def plot_csv_file(self, sfile):

        try:
            adata, dummy = self._dataLoader.read_csv_file(sfile)
        except Exception as ex:
            self._log.error(ex)
            return

        afhr = adata[EnumVarName.fhr]
        uc = adata[EnumVarName.uc]
        atimestamp = adata[EnumVarName.timestamp]

        self.ui.PlotWidget.plot(atimestamp, afhr, uc)

    def plot_bditxt_file(self, sfile):

        try:
            adata, dummy = self._dataLoader.read_bdi_txtfile(sfile)
        except Exception as ex:
            self._log.error(ex)
            return

        afhr = adata[EnumVarName.fhr]
        uc = adata[EnumVarName.uc]
        atimestamp = adata[EnumVarName.timestamp]

        self.ui.PlotWidget.plot(atimestamp, afhr, uc)

    def plot_calibration_signal(self):

        if self.ui.actionEU.isChecked():
            paper_format = 'EU'
        else:
            paper_format = 'US'

        fs = self.ui.PlotWidget.fhrPlot.get_sampling_freq()
        fhr, uc, timestamp = Common.generate_calib_signal(fs, paper_format)
        self.ui.PlotWidget.plot(timestamp, fhr, uc)

    def _show_about(self):
        win = AboutDialog()
        win.exec_()

    def _show_convert_files(self):
        self._convertFilesForm.show()

    def _show_attribute_selection(self):
        self._attSelectForm.show()

    def _show_download_db(self):
        self._downloadDbForm.show()

    def _show_sent_annotations(self):
        self._sent_ann_form.clear_and_show()

    # def _show_ann_show_hide(self):
    #
    #     # print EnumAnnType.__dict__
    #
    #     if DEBUG_FIGO_ANN is False:
    #         ps = self._ann_show_hide_form.ui
    #         lactions = [ps.cbFloatingBaseline, ps.cbAccel, ps.cbDecel, ps.cbUA]
    #         for l in lactions:
    #             l.setChecked(False)
    #             l.hide()
    #
    #     self._ann_show_hide_form.show()
    #     # self.

    def _set_paper_format(self, val):
        if val == EnumPaperFormat.EU:
            self.ui.actionEU.setChecked(True)
        else:
            self.ui.actionUS.setChecked(True)

        self._set_paper()

    def _set_paper(self):
        if self.ui.actionEU.isChecked():
            self.ui.PlotWidget.set_paper_eu()
        else:
            self.ui.PlotWidget.set_paper_us()

    @pyqtSlot()
    def _debug_slot(self):
        print 'SIGNAL CAUGHT'

    @pyqtSlot()
    def _caliper_set(self):
        bvisible = self.ui.actionCaliper.isChecked()
        bfhr = self.ui.actionCaliperFHR.isChecked()
        btoco = self.ui.actionCaliperTOCO.isChecked()
        self.ui.PlotWidget.fhrPlot.caliper_set_visible(bvisible and bfhr)
        self.ui.PlotWidget.tocoPlot.caliper_set_visible(bvisible and btoco)

    @pyqtSlot()
    def _caliper_set_figo_acc_dec(self):
        self.ui.actionCaliper.setChecked(True)
        self.ui.actionCaliperFHR.setChecked(True)
        self.ui.PlotWidget.fhrPlot.caliper_set_figo_acc_dec()

    @pyqtSlot()
    def _caliper_set_figo_ua(self):
        self.ui.actionCaliper.setChecked(True)
        self.ui.actionCaliperTOCO.setChecked(True)
        self.ui.PlotWidget.tocoPlot.caliper_set_figo_ua()

    @pyqtSlot()
    def _caliper_reset(self):
        self.ui.actionCaliper.setChecked(True)
        self.ui.actionCaliperFHR.setChecked(True)
        self.ui.actionCaliperTOCO.setChecked(True)
        self.ui.PlotWidget.fhrPlot.caliper_reset(False)
        self.ui.PlotWidget.tocoPlot.caliper_reset(False)
        self._caliper_set()

    def _set_window_title_rec(self, name=None):

        if name is None:
            self.setWindowTitle(self._winTitleDefault)
        else:
            s = self._winTitleDefault + ' (' + name + ')'
            self.setWindowTitle(s)

    def _export_to_pdf(self):

        if EnumVarName.fhr not in self._signal_data.keys():
            self._log.info("Attempt to export to PDF without plotting any signal first")

            msgbox = QtGui.QMessageBox()
            msgbox.setText("There is no CTG to export!")
            msgbox.setStandardButtons(QtGui.QMessageBox.Close)
            msgbox.setIcon(QtGui.QMessageBox.Information)
            return msgbox.exec_()

        # save annotations and prepare signals
        self._ann_check_unsaved_changes()
        fhr = self._signal_data[EnumVarName.fhr]
        uc = self._signal_data[EnumVarName.uc]
        atimestamp = self._signal_data[EnumVarName.timestamp]
        fs = self._signal_data[EnumVarName.fs]

        if DEBUG_FIGO_ANN is False:
            pe = self._export_to_pdf_form.ui
            lactions = [pe.cbFloatingBaseline, pe.cbAccel, pe.cbDecel, pe.cbUA]
            for l in lactions:
                l.setChecked(False)
                l.hide()

        self._export_to_pdf_form.set_paper_format(self._get_paper_format())
        self._export_to_pdf_form.set_signals(fhr, uc, fs, atimestamp)
        self._export_to_pdf_form.set_record_name(self._signal_data.get("name"))

        # get annotations if any
        annotator = self.ui.PlotWidget.annotator
        self._export_to_pdf_form.set_annotations(annotator.get_annotations_copy_all())

        self._export_to_pdf_form.show()

    def _update_data_browser(self):
        self._dataBrowserWidget.update_model(self._attSelectForm.get_selected_att())

    def closeEvent(self, event):

        if DEBUG_MISC is False:
            self._ann_check_unsaved_changes()

        self._config_ini.set_var(EnumIniVar.annotationToolbarAlignR, self.ui.actionAnnToolbarAlign_right.isChecked())
        self._config_ini.set_var(EnumIniVar.paperformat, self._get_paper_format())
        self._config_ini.set_var(EnumIniVar.windowGeometry, self.saveGeometry())
        self._config_ini.set_var(EnumIniVar.windowState, self.saveState())
        self._config_ini.set_var(EnumIniVar.caliperVisible, self.ui.actionCaliper.isChecked())
        self._config_ini.set_var(EnumIniVar.caliperFHR, self.ui.actionCaliperFHR.isChecked())
        self._config_ini.set_var(EnumIniVar.caliperTOCO, self.ui.actionCaliperTOCO.isChecked())
        self._config_ini.write_config()

    def _process_cmd_args(self, args):

        parsed_args = parse_cmd_args()

        if parsed_args.physionet_file is not None:
            self.plot_file(parsed_args.physionet_file)
            # self.plot_physionet_file(parsed_args.physionet_file)

        if parsed_args.matlab_file is not None:
            self.plot_file(parsed_args.matlab_file)
            # self.plot_matlab_file(parsed_args.matlab_file)

        if parsed_args.folder is not None:
            self._open_folder_data_browser(parsed_args.folder)

            # print parsed_args.physionet_file
            # print parsed_args.matlab_file


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='CTGViewer -- browsing and viewing CTU-UHB database')
    parser.add_argument('-p', '--physionet-file', help='Input file in the physionet format', required=False)
    parser.add_argument('-m', '--matlab-file', help='Input file in the matlab format', required=False)
    parser.add_argument('-f', '--folder', help='Input folder for browsing', required=False)
    return parser.parse_args()


def main():

    init()
    app = QtGui.QApplication(sys.argv)
    window = Main(sys.argv)
    window.show()
    window.ui.PlotWidget.updatePlots()

    sys.exit(app.exec_())

if __name__ == '__main__':

    if DEBUG_PROFILE:
        cProfile.run('main()', 'profile_data')
        p = pstats.Stats('profile_data')
        p.sort_stats('time').print_stats(20)
        p.sort_stats('cumulative').print_stats(20)
    else:
        main()
