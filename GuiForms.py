# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)


import csv
import hashlib
import io
import logging
import os
import sys
import textwrap
import urllib
from PyQt4 import Qt
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal, QString
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders

try:
    import zlib
    import zipfile
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

# local imports
from AboutUI import Ui_DialogAbout
from ConvertFileUI import Ui_ConvertFile
from DownloadCtuUhbUI import Ui_DownloadCtuUhb
from AddNoteUI import Ui_AddNote
from SentAnnotationsUI import Ui_SentAnnotations
from AnnShowHideUI import Ui_AnnShowHideForm
from LoadWriteData import LoadData
import ClinInfoForm
import Common
from Config import ConfigStatic
from Enums import *


class AboutDialog(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_DialogAbout()
        self.ui.setupUi(self)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, pal.background().color())
        self.ui.textBrowser.setPalette(pal)
        self.ui.textBrowser.setOpenExternalLinks(True)


class AddNoteDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_AddNote()
        self.ui.setupUi(self)

        self.btnOk = self.ui.buttonBox.button(Qt.QDialogButtonBox.Ok)
        self.btnCancel = self.ui.buttonBox.button(Qt.QDialogButtonBox.Cancel)

        # self.btnOk.clicked.connect(self.set_text)
        self.btnCancel.clicked.connect(self.clear_text)
        # self.ui.btnClear.clicked.connect(self._clear_baseline)
        # self.ui.btnClose.clicked.connect(self.close)
        # self.ui.spinBox.valueChanged.connect(self._update)

    def clear_text(self):
        self.ui.textNote.setText('')

    def get_text(self):
        s = str(self.ui.textNote.toPlainText())
        s = s.replace('\n', ' ')
        w = self.ui.textNote.width()
        s = textwrap.fill(s, w/8+1)
        return s

    def set_text(self, s):
        self.ui.textNote.setText(s)

    def show(self):
        self.ui.textNote.setFocus()
        return self.exec_()


# class SetClearBaselineDialog(QtGui.QDialog):
#
#     baseline_signal = pyqtSignal(['int'])
#
#     def __init__(self):
#         QtGui.QDialog.__init__(self)
#         self.ui = Ui_SetBaselineUI()
#         self.ui.setupUi(self)
#         self._clear_baseline()
#
#         self.ui.btnSet.clicked.connect(self._set_baseline)
#         self.ui.btnClear.clicked.connect(self._clear_baseline)
#         self.ui.btnClose.clicked.connect(self.close)
#         self.ui.spinBox.valueChanged.connect(self._update)
#
#     def _set_baseline(self):
#         self._update()
#
#     def _clear_baseline(self):
#         self.ui.spinBox.setValue(0)
#         self._update()
#
#     def _update(self):
#         self.baseline_signal.emit(self.ui.spinBox.value())


class ConvertFileForm(QtGui.QWidget):

    stop_signal = pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_ConvertFile()
        self.ui.setupUi(self)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, pal.background().color())
        self.ui.textEditInfo.setPalette(pal)
        self.ui.textEditInfo.setReadOnly(True)

        self.listAllowedFormats = ['dat', 'csv', 'mat', 'txt']
        self.listFormatTooltips = ['physionet format', 'comma separated value', 'matlab format', 'BDI txt']

        self._files_to_convert = []
        self._dataLoader = LoadData()
        self._convertWorker = MetainfoFileConvertWorker()
        self._convertWorker.file_processed.connect(self._update_text_edit)

        self._dictClinInfo = ClinInfoForm.dictClinInfoFullNames

        self._setup_combo_boxes()

        self.ui.btnBrowseSource.clicked.connect(self._open_dir_source)
        self.ui.btnBrowseDest.clicked.connect(self._open_directory_dest)
        self.ui.btnConvert.clicked.connect(self._convert)
        self.ui.btnStop.clicked.connect(self._stop)

        self.msgBoxError = QtGui.QMessageBox()
        self.msgBoxError.setDefaultButton(QtGui.QMessageBox.Close)
        self.msgBoxError.setIcon(QtGui.QMessageBox.Critical)

        self._bAbort = False
        self.ui.btnStop.setEnabled(False)

        # s = '/home/jirka/data/igabrno/CTU_UHB_physionet'
        # self.ui.lnSource.setText(s)
        # self.ui.lnDestination.setText(s)

        # self.ui.lnSource.editingFinished.connect(self.checkSourceDirForFiles)

    def _setup_combo_boxes(self):

        # cnt = 0
        self.ui.cbFrom.addItem('dat')
        self.ui.cbFrom.addItem('mat')
        self.ui.cbTo.addItem('csv')

        # for l in self.listAllowedFormats:
        #    self.ui.cbFrom.addItem(l)
        #    self.ui.cbTo.addItem(l)
        #    self.ui.cbFrom.setItemData(cnt, self.listFormatTooltips[cnt], Qt.Qt.ToolTipRole)
        #    self.ui.cbTo.setItemData(cnt, self.listFormatTooltips[cnt], Qt.Qt.ToolTipRole)
        #    cnt += 1

        self.ui.cbFrom.setCurrentIndex(0)
        self.ui.cbTo.setCurrentIndex(0)

    def _open_dir_source(self):
        open_dialog = QtGui.QFileDialog(self, 'Open directory', '')
        dir1 = open_dialog.getExistingDirectory()

        if dir == "":
            return -1
        else:
            dir1 = str(dir1)
            self.ui.lnSource.setText(dir1)
            self.check_source_dir_for_files()

        return 0

    def _open_directory_dest(self):
        open_dialog = QtGui.QFileDialog(self, 'Open directory', '')
        dir1 = open_dialog.getExistingDirectory()

        if dir == "":
            return -1
        else:
            dir1 = str(dir1)
            self.ui.lnDestination.setText(dir1)

        return 0

    def check_source_dir_for_files(self):

        dir1 = str(self.ui.lnSource.text())
        ext_mask = str(self.ui.cbFrom.itemText(self.ui.cbFrom.currentIndex()))

        check_directory_exists(dir1)

        files = Common.get_files_with_ext_mask(dir1, ext_mask)
        files.sort()

        self.ui.labFile2Convert.setText(str(len(files)))
        self._files_to_convert = files

    def _update_text_edit(self, msg):
        self.ui.textEditInfo.append(msg)
        Qt.QCoreApplication.processEvents()

    def _stop(self):
        self.ui.btnStop.setEnabled(False)
        self._convertWorker.stop()

    def _convert(self):

        self.ui.textEditInfo.clear()
        self.ui.btnConvert.setEnabled(False)
        self.ui.btnStop.setEnabled(True)

        # check source files
        ext_from = str(self.ui.cbFrom.currentText())
        ext_to = str(self.ui.cbTo.currentText())

        if ext_from == ext_to:
            self.msgBoxError.setText('Cannot convert to the same format')
            self.msgBoxError.exec_()
            return

        dir1 = str(self.ui.lnSource.text())
        dir2 = str(self.ui.lnDestination.text())

        try:
            check_directory_exists(dir1)
        except Exception as ex:
            self.msgBoxError.setText('Error in source directory')
            self.msgBoxError.setInformativeText(ex.message)
            self.msgBoxError.exec_()
            return

        try:
            check_directory_exists(dir2)
        except Exception as ex:
            self.msgBoxError.setText('Error in destination directory')
            self.msgBoxError.setInformativeText(ex.message)
            self.msgBoxError.exec_()
            return

        self.check_source_dir_for_files()

        print len(self._files_to_convert)
        if len(self._files_to_convert) == 0:
            self.msgBoxError.setText('No files with format {0} in specified directory {1}'.format(ext_from, dir1))
            self.msgBoxError.exec_()
            return

        if ext_from == 'dat' and ext_to == 'csv':

            # self._convertWorker.convert_files_csv(dir2, self._files_to_convert)

            files_convert_hea = list()
            for f in self._files_to_convert:
                files_convert_hea.append(self._dataLoader.get_physionet_header_name_for_dat(f))

            self._convertWorker.metainfo_create_csv(dir2, files_convert_hea)
            return

        if ext_from == 'mat' and ext_to == 'csv':
            self._convertWorker.convert_files_csv(dir2, self._files_to_convert)
            self._convertWorker.metainfo_create_csv(dir2, self._files_to_convert)
            return


class MetainfoFileConvertWorker(Qt.QObject):
    """
    Worker for converting files.
    This worker has been extracted to be independent from GUI
    """

    file_processed = pyqtSignal(['QString'])
    nr_file_processed = pyqtSignal(['int'])

    def __init__(self):
        Qt.QObject.__init__(self)

        self._log = logging.getLogger(ConfigStatic.logger_name)
        self._dataLoader = LoadData()
        self._dict_clin_info = ClinInfoForm.dictClinInfoFullNames
        self._metainfo = ClinInfoForm.metainfofile
        self._metainfo_md5 = ClinInfoForm.metainfofile_md5sum
        self._stop = False

    @staticmethod
    def get_md5sum(files):

        md5 = hashlib.md5()
        for f in files:
            with open(f, 'r') as fr:
                md5.update(fr.read(8192))

        return md5.hexdigest()

    def metainfo_up_to_date(self, dir_dest, files):
        """
        Create md5sum from given files and compare it with metainfo md5sum

        :param dir_dest:
        :param files:
        :return: True or False
        """

        sfile_metainfo = os.path.join(dir_dest, self._metainfo)
        sfile_metainfo_md5 = os.path.join(dir_dest, self._metainfo_md5)

        if not Common.file_exists(sfile_metainfo):
            return False

        if not Common.file_exists(sfile_metainfo_md5):
            return False

        md5sum = self.get_md5sum(files)

        # read md5sum from file
        with open(sfile_metainfo_md5, 'r') as fr:
            md5expected = fr.readline()

        return md5expected == md5sum

    def metainfo_md5sum_update(self, dir_dest, files):
        """
        For the given files - write md5sum

        :param dir_dest:
        :param files:
        :return:
        """
        sfile_metainfo_md5 = os.path.join(dir_dest, self._metainfo_md5)
        md5sum = self.get_md5sum(files)

        with open(sfile_metainfo_md5, 'w+') as fw:
            fw.write(md5sum)

    def metainfo_create_header_csv(self, sfile_clinical_info):

        with open(sfile_clinical_info, 'w+') as f_clin_info:
            cnt = 0
            for s in self._dict_clin_info.keys():
                f_clin_info.write(self._dict_clin_info[s])
                cnt += 1
                if cnt == len(self._dict_clin_info):
                    f_clin_info.write('\n')
                else:
                    f_clin_info.write(',')

    def metainfo_create_csv(self, dir_dest, files):
        """
        Write information in given files into a metainfo file (ussually csv file)

        :param dir_dest:
        :param files:
        :return:
        """

        # TBME2015 classification (TEMPORARY)
        bloadclassification = False
        if bloadclassification:
            sfile = '/home/jirka/svn_working_copy/iga_brno/matlab/ENSL/barry_schifrin/TBME2015_classification_1288.json'
            dclassification = dict()
            import json
            with open(sfile, 'r') as f:
                dclassification = json.load(f)

        self._stop = False
        sfile_metainfo = os.path.join(dir_dest, self._metainfo)

        self.metainfo_create_header_csv(sfile_metainfo)
        fclin_info = open(sfile_metainfo, 'a')
        cnt_files = 0

        for f in files:
            if self._stop is True:
                self.file_processed.emit(QString('Metainfo creation stoped'))
                return -1

            try:
                header = self._dataLoader.read_data(f)

                if bloadclassification:
                    name = header['name']
                    # print name
                    if name in dclassification:
                        # print dclassification[name]
                        header['Note'] = dclassification[name]

                cnt = 0
                for key in self._dict_clin_info.keys():
                    if key in header:
                        val = header[key]
                        fclin_info.write(str(val))
                    else:
                        fclin_info.write('')

                    cnt += 1
                    if cnt == len(self._dict_clin_info):
                        fclin_info.write('\n')
                    else:
                        fclin_info.write(',')

                cnt_files += 1
                self.nr_file_processed.emit(cnt_files)

            except Exception, msg:
                self._log.error('File {0} - ERROR: msg={1}'.format(sfile_metainfo, msg))

        self.metainfo_md5sum_update(dir_dest, files)

        msg = 'File {0} written'.format(sfile_metainfo)
        self.file_processed.emit(QString(msg))

    def metainfo_read_csv(self, dir_dest):
        """
        Read metainformation stored in a csv file
        :param dir_dest:
        :return: csv_list: list of dictionaries (each line of csv is stored as dictionary)
        """

        sfile_metainfo = os.path.join(dir_dest, self._metainfo)

        # print sfile_metainfo
        # print Common.file_exists(sfile_metainfo) is True

        f = open(sfile_metainfo, 'r')

        filecontent = csv.reader(f, delimiter=',')
        bhas_header = csv.Sniffer().has_header(f.read(2048))
        f.seek(0)  # return to begin

        if bhas_header is False:
            raise IOError('The csv file must contain a header: {0}'.format(sfile_metainfo))

        bread_header = True
        csv_list = list()
        header_names = []

        for row in filecontent:
            # print row

            if bread_header is True:

                bread_header = False
                for item in row:
                    # print item

                    # get the dictionary keys from items
                    # e.g. for item Position II stage [samples] find IIstage
                    for key, val in self._dict_clin_info.items():
                        if val == item:
                            header_names.append(key)

                # print header_names
                continue

            d = dict(zip(header_names, row))
            csv_list.append(d)
            # print d

        f.close()

        return csv_list

    def stop(self):
        self._stop = True

    def convert_files_csv(self, dir_dest, files):
        """
        Convert files to csv format. Save them to a destination directory

        :param dir_dest:
        :param files:
        :return:
        """
        self._stop = False
        ext_to = 'csv'
        cnt_files = 0

        for f in files:
            if self._stop is True:
                self.file_processed.emit(QString('Conversion of files stopped'))
                return

            adata_all = self._dataLoader.read_data(f)
            file_name = Common.get_filename_without_ext(f)
            name_new = os.path.join(dir_dest, (file_name+'.'+ext_to))

            try:
                # data fhr, uc
                self._dataLoader.write_csv_file(name_new, adata_all)
                msg = 'File {0} - Converted'.format(name_new)

            except Exception, msg:
                msg = 'File {0} - ERROR: {1}'.format(name_new, msg)

            cnt_files += 1
            self.nr_file_processed.emit(cnt_files)
            self.file_processed.emit(QString(msg))


class DownloadDbForm(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_DownloadCtuUhb()
        self.ui.setupUi(self)

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, pal.background().color())
        self.ui.textEditInfo.setPalette(pal)
        self.ui.textEditInfo.setReadOnly(True)

        self.ui.btnBrowseDirs.clicked.connect(self._open_directory_source)
        self.ui.btnStart.clicked.connect(self._start_download)
        self.ui.btnStop.clicked.connect(self._stop)

        self.msgBoxError = QtGui.QMessageBox()
        self.msgBoxError.setDefaultButton(QtGui.QMessageBox.Close)
        self.msgBoxError.setIcon(QtGui.QMessageBox.Critical)

        self.msgBoxWarn = QtGui.QMessageBox()
        self.msgBoxWarn.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self.msgBoxWarn.setIcon(QtGui.QMessageBox.Information)

        self._bAbort = False
        self.ui.btnStop.setEnabled(False)
        self.ui.progressBar.reset()

        self._MD5SUMS = 'MD5SUMS'
        self._attempsToDownloadFile = 5

    def _open_directory_source(self):
        open_dialog = QtGui.QFileDialog(self, 'Open directory', '')
        dir1 = open_dialog.getExistingDirectory()

        if dir == "":
            return -1
        else:
            dir1 = str(dir1)
            self.ui.lnDestDir.setText(dir1)
            self.ui.textEditInfo.clear()

        return 0

    def _start_download(self):
        """
        prepare for downloading - check the directories and url
        """

        self._bAbort = False

        self._url = str(self.ui.lineEditUrl.text())
        self.ui.textEditInfo.clear()

        self._dirDest = str(self.ui.lnDestDir.text())

        try:
            check_directory_exists(self._dirDest)
        except Exception as ex:
            self.msgBoxError.setText('Error in destination directory')
            self.msgBoxError.setInformativeText(ex.message)
            self.msgBoxError.exec_()
            return

        files = Common.directory_listing(self._dirDest)

        ret = 0
        if len(files) > 0:
            self.msgBoxWarn.setText('The destination directory is not empty.')
            self.msgBoxWarn.setInformativeText(""" It is recommended to download database into an empty directory.
                                               Continue download? """)
            ret = self.msgBoxWarn.exec_()

        if ret == Qt.QMessageBox.No:
            return

        # check if MD5SUMS exist
        name_dest = os.path.join(self._dirDest, self._MD5SUMS)
        fname, dummy = urllib.urlretrieve(self._url + self._MD5SUMS, name_dest)

        b_not_found = False
        with io.open(fname, 'rt') as fin:
            for s in fin.readlines():
                ind = s.find(fname + ' was not found on this server')
                if ind > -1:
                    b_not_found = True

        if b_not_found:
            self.msgBoxError.setText('Error in the database url')
            s = 'File: ' + self._MD5SUMS + ' was not found at the server.'
            s += 'Download can not continue without this file. ' \
                 'Please check the database url and make sure that file MD5SUMS exists.'
            self.msgBoxError.setInformativeText(s)
            self.msgBoxError.exec_()
            return
        else:
            # if all ok -> run the actual download
            self.ui.btnStart.setEnabled(False)
            self.ui.btnStop.setEnabled(True)

            if self.run_download() == 0:
                self.ui.textEditInfo.append('Download completed')
                self.ui.btnStart.setEnabled(True)
                self.ui.btnStop.setEnabled(False)

    def run_download(self):
        """
        Download all files from given url and MD5SUMS file
        """

        # set the progress bar
        md5_file = os.path.join(self._dirDest, self._MD5SUMS)
        nrfiles = Common.get_mumber_lines(md5_file)
        self.ui.progressBar.setRange(1, nrfiles)
        self.ui.progressBar.update()

        # process all files in file: self._MD5SUMS

        with io.open(md5_file, 'rt') as fin:

            processed_files = 0
            for line in fin.readlines():

                if self._bAbort:
                    self.ui.textEditInfo.append('ABORTED')
                    return 1

                md5, fname = line.split('  ')
                md5 = md5.strip()
                fname = fname.strip()

                # do not download this file
                if fname.find('HEADER.shtml') > -1:
                    processed_files += 1
                    continue

                cnt = 0
                bmd5_ok = False
                name_dest = os.path.join(self._dirDest, fname)

                # for a given number of attempts try to download a file
                while cnt < self._attempsToDownloadFile:
                    cnt += 1
                    fname, dummy = urllib.urlretrieve(self._url + fname, name_dest)
                    Qt.QCoreApplication.processEvents()
                    bmd5_ok = self.check_md5(md5, fname)

                    if bmd5_ok:
                        break

                if bmd5_ok:
                    self.ui.textEditInfo.append("Downloaded file: " + name_dest)
                else:
                    s = "Failed to download file: " + name_dest
                    s += ' MD5SUM do not match'
                    self.ui.textEditInfo.append(s)

                processed_files += 1
                self.ui.progressBar.setValue(processed_files)
                Qt.QCoreApplication.processEvents()

        return 0

    def check_md5(self, md5expected, filename):
        return md5expected == self.md5_for_file(filename)

    def md5_for_file(self, filename):
        """
        get md5sum for a given filename
        """

        md5 = hashlib.md5()
        file1 = open(filename, 'rb')

        while True:
            data = file1.read(65536)
            if not data:
                break
            md5.update(data)

        file1.close()
        return md5.hexdigest()

    def _stop(self):
        self.ui.btnStop.setEnabled(False)
        self._bAbort = True
        self.ui.btnStart.setEnabled(True)


# class AnnShowHide(QtGui.QWidget):
#
#     stop_signal = pyqtSignal()
#
#     def __init__(self, configini):
#         QtGui.QWidget.__init__(self)
#
#         self.ui = Ui_AnnShowHideForm()
#         self.ui.setupUi(self)
#
#         self._config_ini = configini
#
#         e = EnumAnnType
#         self._dict_ann = {self.ui.cbBasal: e.basal, self.ui.cbBaseline: e.baseline, self.ui.cbRecovery: e.recovery,
#                           self.ui.cbNoRecovery: e.no_recovery, self.ui.cbExcessiveUA: e.excessive_ua,
#                           self.ui.cbNote: e.note, self.ui.cbMark: e.ellipsenote,
#                           self.ui.cbFloatingBaseline: e.floating_baseline, self.ui.cbAccel: e.acceleration,
#                           self.ui.cbDecel: e.deceleration, self.ui.cbUA: e.uterine_contraction}
#
#         self.ui.btnSelectAll.clicked.connect(self._select_all)
#         self.ui.btnUnselect.clicked.connect(self._unselect_all)
#
#         # self.btnSave.clicked.connect(self.save)
#         # self.btnCancel.clicked.connect(self.close)
#
#     def _select_all(self):
#
#         for cb in self._dict_ann.iterkeys():
#             if isinstance(cb, QtGui.QCheckBox):
#                 if cb.isVisible():
#                     cb.setChecked(True)
#
#     def _unselect_all(self):
#
#         for cb in self._dict_ann.iterkeys():
#             if isinstance(cb, QtGui.QCheckBox):
#                 if cb.isVisible():
#                     cb.setChecked(False)


class SentAnnotationsForm(QtGui.QWidget):

    stop_signal = pyqtSignal()

    def __init__(self, configini):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_SentAnnotations()
        self.ui.setupUi(self)

        self._config_ini = configini

        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, pal.background().color())
        self.ui.textEditInfo.setPalette(pal)
        self.ui.textEditInfo.setReadOnly(True)

        self.ui.btnBrowseSource.clicked.connect(self._open_dir_source)
        self.ui.btnSent.clicked.connect(self._sent)

        self._files_to_sent = list()

        self.msgBoxError = QtGui.QMessageBox()
        self.msgBoxError.setDefaultButton(QtGui.QMessageBox.Close)
        self.msgBoxError.setIcon(QtGui.QMessageBox.Critical)

        # self.ui.lnSource.setText("/home/jirka/data/data_schrifrin_final")
        # self.check_source_dir_for_files()

    def _open_dir_source(self):

        open_dialog = QtGui.QFileDialog(self, 'Select directory with CTG and annotations',
                                        self._config_ini.get_var(EnumIniVar.lastUsedDirFiles))
        dir1 = open_dialog.getExistingDirectory()

        if dir1 == "":
            return -1
        else:
            dir1 = str(dir1)
            self.ui.lnSource.setText(dir1)
            self.check_source_dir_for_files()

        return 0

    def check_source_dir_for_files(self):

        dir1 = str(self.ui.lnSource.text())
        check_directory_exists(dir1)

        files = Common.get_files_with_ext_mask(dir1, '.ann')
        files.sort()

        self.ui.labFiles2Sent.setText(str(len(files)))
        self._files_to_sent = files

    def _sent(self):

        self.ui.textEditInfo.clear()
        dir1 = str(self.ui.lnSource.text())

        try:
            check_directory_exists(dir1)
        except Exception as ex:
            self.msgBoxError.setText('Error in source directory')
            self.msgBoxError.setInformativeText(ex.message)
            self.msgBoxError.exec_()
            return

        if self.ui.lnFrom.text() == '':
            self.msgBoxError.setText('Recepient is empty')
            self.msgBoxError.exec_()
            return

        if self.ui.lnTo.text() == '':
            self.msgBoxError.setText('Recepient is empty')
            self.msgBoxError.exec_()
            return

        if self.ui.lnTo.text() == '':
            self.msgBoxError.setText('Senders is empty')
            self.msgBoxError.exec_()
            return

        self.check_source_dir_for_files()

        if len(self._files_to_sent) == 0:
            self.msgBoxError.setText('No annotations were found in specified directory {0}'.format(dir1))
            self.msgBoxError.exec_()
            return

        self.ui.btnSent.setEnabled(False)
        self._update_text_edit('Annotations available: {0}'.format(len(self._files_to_sent)))

        # zip
        sfile_zip = 'barry_schifrin_annotations' + datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + '.zip'
        zf = zipfile.ZipFile(sfile_zip, 'w', compression)

        self._update_text_edit("Packing files ...")
        for f in self._files_to_sent:
            self._update_text_edit('{0}'.format(f))
            zf.write(f)

        zf.close()

        self._update_text_edit("Packing finished")
        self._update_text_edit("Sending email ...")

        try:
            res = mail(str(self.ui.lnTo.text()),
                       "Annotations from: {0} - {1}".format(str(self.ui.lnFrom.text()), self.ui.lnSubject.text()),
                       str(self.ui.textEditBody.document().toPlainText()), sfile_zip)

            if len(res) == 0:
                self._update_text_edit("\n Email with annotations has been sent.")
            else:
                self._update_text_edit("\n Error: {0}".format(str(res)))
            self._sent_finished()

        except Exception, msg:
            self._update_text_edit("\n Error: {0}".format(msg))

    def _sent_finished(self):
        self.ui.btnSent.setEnabled(True)

    def _update_text_edit(self, msg):
        self.ui.textEditInfo.append(msg)
        Qt.QCoreApplication.processEvents()

    def clear_and_show(self):
        self.ui.textEditInfo.clear()
        self.ui.lnSource.clear()
        self.ui.btnSent.setEnabled(True)
        self.ui.labFiles2Sent.clear()
        self.show()


def check_directory_exists(dir1):

    if not os.path.exists(dir1):
        raise Exception('Chosen directory do not exists: {0}'.format(dir1))


def mail(to, subject, text, attach):

    gmail_user = "jiri.spilka.work@gmail.com"
    # gmail_pwd = "do4asn0heslo"
    gmail_pwd = "xshebqnzilrqqphl"

    msg = MIMEMultipart()

    msg['From'] = "jiri.spilka.work@gmail.com"
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_pwd)
    result = server.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    server.close()

    return result


def main():
    app = QtGui.QApplication(sys.argv)
    # window = ConvertFileForm()
    # window = DownoladDbForm()
    # winwow = AnnShowHide()
    # window.show()
    # sys.exit(app.exec_())

    # r = ConvertFileWorker()
    # r.metainfo_read_csv('/home/jirka/data/igabrno/CTU_UHB_physionet')


if __name__ == '__main__':
        main()