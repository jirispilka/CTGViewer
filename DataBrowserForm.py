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
DataModel
--------------------

"""

import os
import logging
from PyQt4 import QtCore, QtGui, Qt

import Common
from Enums import EnumIniVar
from Config import ConfigStatic, ConfigIni
from GuiForms import MetainfoFileConvertWorker
import ClinInfoForm
from LoadWriteData import LoadData
from DataBrowserUI import Ui_DataBrowser
import Annotator

bWriteStageIIcorrect = False


# noinspection PyInterpreter
class DataBrowserForm(QtGui.QWidget):

    plotFileSignal = QtCore.pyqtSignal(['QString'])
    # debug_stageI_signal = QtCore.pyqtSignal(['int'])

    def __init__(self, parent=None, config_ini=None):

        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_DataBrowser()
        self.ui.setupUi(self)

        self._log = logging.getLogger(ConfigStatic.logger_name)
        self._log.info('passed')

        # self.setMinimumSize(300, 100)

        # CONFIG
        self._config_ini = config_ini or ConfigIni()

        self._dataLoader = LoadData()

        self._source_dir = ''
        self._filesExtDat = '.dat'
        self._filesExtHea = '.hea'
        self._filesExtMat = '.mat'
        self._files_ext = ''
        self._nr_files_metainfo = 0
        self._metainfo_handler = MetainfoFileConvertWorker()

        self._model = QtGui.QStandardItemModel()
        self._table = self.ui.tableView

        self.msgBoxError = QtGui.QMessageBox()
        self.msgBoxError.setDefaultButton(QtGui.QMessageBox.Close)
        self.msgBoxError.setIcon(QtGui.QMessageBox.Critical)

        self._progress_dialog = QtGui.QProgressDialog()
        self._progress_dialog.setLabelText("Creating file metainfo ...")
        self._progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self._progress_dialog.close()

        # connections
        self._table.doubleClicked.connect(self._table_double_click)
        self.ui.btnNext.clicked.connect(self._current_row_increment)
        self.ui.btnPrev.clicked.connect(self._current_row_decrement)
        self._metainfo_handler.nr_file_processed.connect(self._update_metainfo_progress)
        self._progress_dialog.canceled.connect(self._stop_create_metainfo)

        self._selected_att = list()

        if bWriteStageIIcorrect:
            import datetime
            self._metainfofile_stage2_corr = 'metainfo_corrected_' + str(datetime.datetime.utcnow()) + '.csv'

    @staticmethod
    def __get_val_str(dictci, key):
        if key in dictci:
            return str(dictci[key])
        else:
            return None

    @staticmethod
    def __get_value_by_type(dictci, key):
        """

        :param dictci: dict
        :param key: str
        :return:
        """
        assert isinstance(dictci, dict)
        value = dictci.get(key, "")

        tests = [
            # (Type, Test)
            (int, int),
            (float, float)
        ]

        if value == 'nan' or value == 'NaN':
            return str(value)

        for typ, test in tests:
            try:
                test(value)
                return typ(value)
            except ValueError:
                pass
        # No match
        return str(value)

    def _get_selected_row(self):
        item = self._table.selectedIndexes()
        try:
            row = item[0].row()
            return row
        except:
            return -1

    def get_source_dir(self):
        return self._source_dir

    def set_source_dir(self, sdir):
        self._source_dir = sdir

    def set_attributes_dir_and_load(self, attributes, sdir):
        """
        Set the source directory to be used in the model.
        Load all header files
        :param attributes:
        :param sdir:
        """
        self.set_source_dir(sdir)
        afileshea = sorted(Common.get_files_with_ext_mask(self._source_dir, self._filesExtHea))
        afilesmat = sorted(Common.get_files_with_ext_mask(self._source_dir, self._filesExtMat))

        if len(afileshea) > 0 and len(afilesmat) > 1:
            # self.msgBoxError.setIcon(QtGui.QMessageBox.)
            self.msgBoxError.setStandardButtons(Qt.QMessageBox.Save)
            self.msgBoxError.setText('Both types of header files (hea, mat) found in the specified directory.')
            self.msgBoxError.setInformativeText("""The application does not support both data types at once.
            Please remove either dat or matlab files""")
            self.msgBoxError.exec_()
            return

        if len(afileshea) > 0:
            afiles = afileshea
            self._files_ext = self._filesExtDat
        else:
            afiles = afilesmat
            self._files_ext = self._filesExtMat

        if self._set_model(attributes, afiles) != 0:
            return

        self._table.setModel(self._model)
        # self._table.sortByColumn(0, 0)
        self._table.resizeColumnsToContents()
        self._table.resizeRowsToContents()

        self._table_settings()
        self._change_to_row(0)

    def update_model(self, selected_att):

        if self._set_model(selected_att) == -1:
            return

        self._table.setModel(self._model)
        self._table.sortByColumn(0, 0)
        self._table.resizeColumnsToContents()
        self._table.resizeRowsToContents()

        self._table_settings()
        self._change_to_row(0)

        self._table.update()

    def update_model_without_sort(self, selected_att):

        if self._set_model(selected_att) == -1:
            return

        self._table.setModel(self._model)
        self._table.update()

    def _model_settings(self):
        pass

    def _table_settings(self):

        self._table.setSortingEnabled(True)
        # self._table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)  # disable editting
        self._table.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked)  # disable editting

        # font
        font = self._table.font()
        # size = font.pointSize()
        font.setPointSize(10)
        self._table.setFont(font)

        self._table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  # select whole rows

    def _stop_create_metainfo(self):
        self._metainfo_handler.stop()
        self._progress_dialog.close()

    def _set_model(self, selected_att, afiles=None):
        """
        Set data for current model. A metainfo file is created if is not up to date.

        :param selected_att: attributes to be shown in the view
        :param afiles: list of files. If afiles is None just update the model.
        :type: selected_att: list()
        :type: afiles: list()
        """

        self._selected_att = selected_att

        if bWriteStageIIcorrect:
            self._metainfofile_stage2_corr = os.path.join(self._source_dir, self._metainfofile_stage2_corr)

        if afiles is None:
            if self._source_dir is None or self._source_dir == "":
                return -1
        else:
            self._progress_dialog.close()
            if not self._metainfo_handler.metainfo_up_to_date(self._source_dir, afiles):
                self._progress_dialog.setRange(0, len(afiles))
                self._progress_dialog.setValue(0)
                self._progress_dialog.open()

                if self._metainfo_handler.metainfo_create_csv(self._source_dir, afiles) == -1:
                    return -1

        csv_list = self._metainfo_handler.metainfo_read_csv(self._source_dir)
        nrfiles = len(csv_list)

        self._model = QtGui.QStandardItemModel(nrfiles, 1)
        irow = 0
        for dictrow in csv_list:

            # print dictrow
            self._model.setItem(irow, 0, QtGui.QStandardItem(dictrow['name']))

            icol = 1
            if len(self._selected_att) != 0 and self._selected_att[0] != '':
                for att in self._selected_att:
                    val = self.__get_val_str(dictrow, att)
                    # val = self.__get_value_by_type(dictrow, att)  # not working
                    if val is not None:
                        self._model.setItem(irow, icol, QtGui.QStandardItem(val))

                    if att == ClinInfoForm.annotation_name:
                        ann_extension = Annotator.Annotator().ann_extension
                        ann_file = dictrow['name'] + ann_extension
                        ann_file = os.path.join(self._source_dir, ann_file)
                        val = str(Common.file_exists(ann_file) and Common.get_mumber_lines(ann_file) > 0)
                        # val = '1' if val is True else '0'
                        self._model.setItem(irow, icol, QtGui.QStandardItem(val))

                    icol += 1
            irow += 1

        # header (attribute Name)
        temp = list()
        temp.append('Name')
        if len(self._selected_att) != 0 and self._selected_att[0] != '':
            self._model.setHorizontalHeaderLabels(temp+self._selected_att)
        return 0

    def _change_to_row(self, row):

        item = self._model.index(row, 0)
        val = self._model.data(item, Qt.Qt.DisplayRole)
        fname = val.toString()

        self._table.selectRow(row)
        self.ui.labRecName.setText(fname)

        # print row
        # print val.toString()

        self._plot_file_emit(fname)

        # cnt = 0
        # temp = list()
        # temp.append('Name')
        # for s in temp+self._selected_att:
        #     if s == 'Istage':
        #         item = self._model.index(row, cnt)
        #         val = self._model.data(item, Qt.Qt.DisplayRole)
        #         print val.toString()
        #         val = int(val.toString())
        #         self.debug_stageI_signal.emit(val)
        #
        #     cnt += 1

    def _write_stage2_corrected(self):

        nr = self._model.rowCount()
        nc = self._model.columnCount()

        # write header
        with open(self._metainfofile_stage2_corr, 'w+') as fw:
            # self._he
            temp = list()
            temp.append('Name')
            temp += self._selected_att

            cnt = 1
            for s in temp:
                fw.write(s)
                if not cnt == len(temp):
                    fw.write(',')
                else:
                    fw.write('\n')
                cnt += 1

        # write the values
        with open(self._metainfofile_stage2_corr, 'a') as fw:
            for i in range(0, nr):
                cnt = 1
                for j in range(0, nc):
                    item = self._model.index(i, j)
                    val = self._model.data(item, Qt.Qt.DisplayRole)
                    val_str = val.toString()

                    fw.write(val_str)
                    if not cnt == nc:
                        fw.write(',')
                    else:
                        fw.write('\n')

                    # print val_str
                    cnt += 1

    def _current_row_increment(self):

        if bWriteStageIIcorrect:
            self._write_stage2_corrected()

        nmax = self._model.rowCount()-1
        nsel = self._get_selected_row()

        if nsel < nmax:
            self._change_to_row(nsel + 1)

    def _current_row_decrement(self):

        if bWriteStageIIcorrect:
            self._write_stage2_corrected()

        nsel = self._get_selected_row()
        if nsel > 0:
            self._change_to_row(nsel - 1)

    def __load_file_on_row(self, row):
        # fname = self._model.data(item[0], Qt.DisplayRole).toString()
        pass

    def _plot_file_emit(self, fname):

        # fname = Common.get_filename_without_ext(fname)
        fname = str(fname) + self._files_ext
        fname = os.path.join(self._source_dir, fname)
        self.plotFileSignal.emit(QtCore.QString(fname))

    def _table_double_click(self):
        row = self._get_selected_row()
        self._change_to_row(row)

    def keyPressEvent(self, event):

        if event.key() == Qt.Qt.Key_Return:
            self._table_double_click()

        return QtGui.QWidget.keyPressEvent(self, event)

    def _update_metainfo_progress(self, i):
        self._progress_dialog.setValue(i)


class Login(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handle_login(self):
        if self.textName.text() == 'foo' and self.textPass.text() == 'bar':
            self.accept()
        else:
            QtGui.QMessageBox.warning(self, 'Error', 'Bad user or password')


"""
class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)

    if Login().exec_() == QtGui.QDialog.Accepted:
        window = Window()
        window.show()
"""

import sys
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dataModel = DataBrowserForm()
    dataModel.show()

    # dataModel.set_source_dir_and_load('/home/jirka/data/igabrno/CTU_UHB_physionet')
    dataModel.set_attributes_dir_and_load(None, '/home/jirka/data/CurrentDB_10Hz/matfiles')

    sys.exit(app.exec_())