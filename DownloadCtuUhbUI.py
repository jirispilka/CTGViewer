# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DownloadCtuUhbUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DownloadCtuUhb(object):
    def setupUi(self, DownloadCtuUhb):
        DownloadCtuUhb.setObjectName(_fromUtf8("DownloadCtuUhb"))
        DownloadCtuUhb.resize(707, 467)
        self.gridLayout = QtGui.QGridLayout(DownloadCtuUhb)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(DownloadCtuUhb)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(DownloadCtuUhb)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)
        self.btnBrowseDirs = QtGui.QPushButton(DownloadCtuUhb)
        self.btnBrowseDirs.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnBrowseDirs.setObjectName(_fromUtf8("btnBrowseDirs"))
        self.gridLayout.addWidget(self.btnBrowseDirs, 1, 4, 1, 1)
        self.label_2 = QtGui.QLabel(DownloadCtuUhb)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(DownloadCtuUhb)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 8, 1, 1, 4)
        self.lnDestDir = QtGui.QLineEdit(DownloadCtuUhb)
        self.lnDestDir.setObjectName(_fromUtf8("lnDestDir"))
        self.gridLayout.addWidget(self.lnDestDir, 1, 1, 1, 3)
        self.textEditInfo = QtGui.QTextEdit(DownloadCtuUhb)
        self.textEditInfo.setObjectName(_fromUtf8("textEditInfo"))
        self.gridLayout.addWidget(self.textEditInfo, 9, 0, 1, 5)
        self.lineEditUrl = QtGui.QLineEdit(DownloadCtuUhb)
        self.lineEditUrl.setObjectName(_fromUtf8("lineEditUrl"))
        self.gridLayout.addWidget(self.lineEditUrl, 0, 1, 1, 4)
        self.line = QtGui.QFrame(DownloadCtuUhb)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 7, 0, 1, 5)
        self.btnStart = QtGui.QPushButton(DownloadCtuUhb)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/icon_convert.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStart.setIcon(icon)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.gridLayout.addWidget(self.btnStart, 5, 2, 1, 1)
        self.btnStop = QtGui.QPushButton(DownloadCtuUhb)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/document-close-3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStop.setIcon(icon1)
        self.btnStop.setObjectName(_fromUtf8("btnStop"))
        self.gridLayout.addWidget(self.btnStop, 5, 3, 1, 2)

        self.retranslateUi(DownloadCtuUhb)
        QtCore.QMetaObject.connectSlotsByName(DownloadCtuUhb)
        DownloadCtuUhb.setTabOrder(self.lineEditUrl, self.lnDestDir)
        DownloadCtuUhb.setTabOrder(self.lnDestDir, self.btnStart)
        DownloadCtuUhb.setTabOrder(self.btnStart, self.btnStop)
        DownloadCtuUhb.setTabOrder(self.btnStop, self.textEditInfo)
        DownloadCtuUhb.setTabOrder(self.textEditInfo, self.btnBrowseDirs)

    def retranslateUi(self, DownloadCtuUhb):
        DownloadCtuUhb.setWindowTitle(_translate("DownloadCtuUhb", "Download CTU-UHB database from physionet", None))
        self.label.setText(_translate("DownloadCtuUhb", "Database url:", None))
        self.label_3.setText(_translate("DownloadCtuUhb", "Details:", None))
        self.btnBrowseDirs.setText(_translate("DownloadCtuUhb", "..", None))
        self.label_2.setText(_translate("DownloadCtuUhb", "Save to directory:", None))
        self.lineEditUrl.setText(_translate("DownloadCtuUhb", "http://physionet.org/physiobank/database/ctu-uhb-ctgdb/", None))
        self.btnStart.setText(_translate("DownloadCtuUhb", "Start download", None))
        self.btnStop.setText(_translate("DownloadCtuUhb", "Stop download", None))

import resources_rc
