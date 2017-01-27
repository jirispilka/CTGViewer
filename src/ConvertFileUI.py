# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConvertFileUI.ui'
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

class Ui_ConvertFile(object):
    def setupUi(self, ConvertFile):
        ConvertFile.setObjectName(_fromUtf8("ConvertFile"))
        ConvertFile.resize(538, 417)
        self.gridLayout = QtGui.QGridLayout(ConvertFile)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labFile2Convert = QtGui.QLabel(ConvertFile)
        self.labFile2Convert.setObjectName(_fromUtf8("labFile2Convert"))
        self.gridLayout.addWidget(self.labFile2Convert, 11, 3, 1, 1)
        self.btnBrowseSource = QtGui.QPushButton(ConvertFile)
        self.btnBrowseSource.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnBrowseSource.setObjectName(_fromUtf8("btnBrowseSource"))
        self.gridLayout.addWidget(self.btnBrowseSource, 3, 7, 1, 1)
        self.btnBrowseDest = QtGui.QPushButton(ConvertFile)
        self.btnBrowseDest.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnBrowseDest.setObjectName(_fromUtf8("btnBrowseDest"))
        self.gridLayout.addWidget(self.btnBrowseDest, 4, 7, 1, 1)
        self.line = QtGui.QFrame(ConvertFile)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 5, 1, 1, 6)
        self.label_6 = QtGui.QLabel(ConvertFile)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.line_3 = QtGui.QFrame(ConvertFile)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 2, 1, 1, 6)
        self.lnDestination = QtGui.QLineEdit(ConvertFile)
        self.lnDestination.setObjectName(_fromUtf8("lnDestination"))
        self.gridLayout.addWidget(self.lnDestination, 4, 3, 1, 4)
        self.cbFrom = QtGui.QComboBox(ConvertFile)
        self.cbFrom.setObjectName(_fromUtf8("cbFrom"))
        self.gridLayout.addWidget(self.cbFrom, 0, 3, 1, 1)
        self.label = QtGui.QLabel(ConvertFile)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)
        self.label_3 = QtGui.QLabel(ConvertFile)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 11, 1, 1, 1)
        self.label_2 = QtGui.QLabel(ConvertFile)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)
        self.textEditInfo = QtGui.QTextEdit(ConvertFile)
        self.textEditInfo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEditInfo.setReadOnly(True)
        self.textEditInfo.setObjectName(_fromUtf8("textEditInfo"))
        self.gridLayout.addWidget(self.textEditInfo, 13, 1, 1, 7)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 5, 1, 3)
        self.label_5 = QtGui.QLabel(ConvertFile)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 12, 1, 1, 1)
        self.lnSource = QtGui.QLineEdit(ConvertFile)
        self.lnSource.setObjectName(_fromUtf8("lnSource"))
        self.gridLayout.addWidget(self.lnSource, 3, 3, 1, 4)
        self.label_7 = QtGui.QLabel(ConvertFile)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)
        self.cbTo = QtGui.QComboBox(ConvertFile)
        self.cbTo.setObjectName(_fromUtf8("cbTo"))
        self.gridLayout.addWidget(self.cbTo, 1, 3, 1, 1)
        self.btnStop = QtGui.QPushButton(ConvertFile)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/document-close-3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStop.setIcon(icon)
        self.btnStop.setObjectName(_fromUtf8("btnStop"))
        self.gridLayout.addWidget(self.btnStop, 11, 6, 1, 2)
        self.btnConvert = QtGui.QPushButton(ConvertFile)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/icon_convert.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnConvert.setIcon(icon1)
        self.btnConvert.setObjectName(_fromUtf8("btnConvert"))
        self.gridLayout.addWidget(self.btnConvert, 11, 5, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 3)

        self.retranslateUi(ConvertFile)
        self.cbFrom.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(ConvertFile)
        ConvertFile.setTabOrder(self.cbFrom, self.cbTo)
        ConvertFile.setTabOrder(self.cbTo, self.lnSource)
        ConvertFile.setTabOrder(self.lnSource, self.lnDestination)
        ConvertFile.setTabOrder(self.lnDestination, self.btnConvert)
        ConvertFile.setTabOrder(self.btnConvert, self.btnStop)
        ConvertFile.setTabOrder(self.btnStop, self.textEditInfo)
        ConvertFile.setTabOrder(self.textEditInfo, self.btnBrowseSource)
        ConvertFile.setTabOrder(self.btnBrowseSource, self.btnBrowseDest)

    def retranslateUi(self, ConvertFile):
        ConvertFile.setWindowTitle(_translate("ConvertFile", "Convert files", None))
        self.labFile2Convert.setText(_translate("ConvertFile", "0", None))
        self.btnBrowseSource.setText(_translate("ConvertFile", "..", None))
        self.btnBrowseDest.setText(_translate("ConvertFile", "..", None))
        self.label_6.setText(_translate("ConvertFile", "Convert from:", None))
        self.label.setText(_translate("ConvertFile", "Source:", None))
        self.label_3.setText(_translate("ConvertFile", "Files to convert:", None))
        self.label_2.setText(_translate("ConvertFile", "Destination:", None))
        self.label_5.setText(_translate("ConvertFile", "Information:", None))
        self.label_7.setText(_translate("ConvertFile", "Convert to:", None))
        self.btnStop.setText(_translate("ConvertFile", "Stop", None))
        self.btnConvert.setText(_translate("ConvertFile", "Convert", None))

import resources_rc
