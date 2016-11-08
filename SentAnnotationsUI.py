# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SentAnnotationsUI.ui'
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

class Ui_SentAnnotations(object):
    def setupUi(self, SentAnnotations):
        SentAnnotations.setObjectName(_fromUtf8("SentAnnotations"))
        SentAnnotations.resize(556, 424)
        self.gridLayout = QtGui.QGridLayout(SentAnnotations)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(SentAnnotations)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_7 = QtGui.QLabel(SentAnnotations)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)
        self.textEditBody = QtGui.QTextEdit(SentAnnotations)
        self.textEditBody.setAcceptRichText(False)
        self.textEditBody.setObjectName(_fromUtf8("textEditBody"))
        self.gridLayout.addWidget(self.textEditBody, 9, 2, 1, 2)
        self.lnTo = QtGui.QLineEdit(SentAnnotations)
        self.lnTo.setObjectName(_fromUtf8("lnTo"))
        self.gridLayout.addWidget(self.lnTo, 7, 2, 1, 2)
        self.lnFrom = QtGui.QLineEdit(SentAnnotations)
        self.lnFrom.setObjectName(_fromUtf8("lnFrom"))
        self.gridLayout.addWidget(self.lnFrom, 4, 2, 1, 2)
        self.lnSubject = QtGui.QLineEdit(SentAnnotations)
        self.lnSubject.setObjectName(_fromUtf8("lnSubject"))
        self.gridLayout.addWidget(self.lnSubject, 8, 2, 1, 2)
        self.label_6 = QtGui.QLabel(SentAnnotations)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 9, 0, 1, 1)
        self.textEditInfo = QtGui.QTextEdit(SentAnnotations)
        self.textEditInfo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEditInfo.setReadOnly(True)
        self.textEditInfo.setObjectName(_fromUtf8("textEditInfo"))
        self.gridLayout.addWidget(self.textEditInfo, 14, 0, 1, 5)
        self.btnBrowseSource = QtGui.QPushButton(SentAnnotations)
        self.btnBrowseSource.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btnBrowseSource.setObjectName(_fromUtf8("btnBrowseSource"))
        self.gridLayout.addWidget(self.btnBrowseSource, 0, 4, 1, 1)
        self.line = QtGui.QFrame(SentAnnotations)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 10, 0, 1, 5)
        self.label = QtGui.QLabel(SentAnnotations)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_5 = QtGui.QLabel(SentAnnotations)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 13, 0, 1, 1)
        self.label_2 = QtGui.QLabel(SentAnnotations)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.line_2 = QtGui.QFrame(SentAnnotations)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 5)
        self.lnSource = QtGui.QLineEdit(SentAnnotations)
        self.lnSource.setObjectName(_fromUtf8("lnSource"))
        self.gridLayout.addWidget(self.lnSource, 0, 3, 1, 1)
        self.labFiles2Sent = QtGui.QLabel(SentAnnotations)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labFiles2Sent.setFont(font)
        self.labFiles2Sent.setObjectName(_fromUtf8("labFiles2Sent"))
        self.gridLayout.addWidget(self.labFiles2Sent, 2, 4, 1, 1)
        self.label_3 = QtGui.QLabel(SentAnnotations)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 3, 1, 1)
        self.btnSent = QtGui.QPushButton(SentAnnotations)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/send-file-16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSent.setIcon(icon)
        self.btnSent.setObjectName(_fromUtf8("btnSent"))
        self.gridLayout.addWidget(self.btnSent, 11, 4, 1, 1)

        self.retranslateUi(SentAnnotations)
        QtCore.QMetaObject.connectSlotsByName(SentAnnotations)
        SentAnnotations.setTabOrder(self.lnSource, self.lnFrom)
        SentAnnotations.setTabOrder(self.lnFrom, self.lnTo)
        SentAnnotations.setTabOrder(self.lnTo, self.lnSubject)
        SentAnnotations.setTabOrder(self.lnSubject, self.textEditBody)
        SentAnnotations.setTabOrder(self.textEditBody, self.btnSent)
        SentAnnotations.setTabOrder(self.btnSent, self.textEditInfo)
        SentAnnotations.setTabOrder(self.textEditInfo, self.btnBrowseSource)

    def retranslateUi(self, SentAnnotations):
        SentAnnotations.setWindowTitle(_translate("SentAnnotations", "Sent annotations", None))
        self.label_4.setText(_translate("SentAnnotations", "Sent from (email)", None))
        self.label_7.setText(_translate("SentAnnotations", "Subject", None))
        self.label_6.setText(_translate("SentAnnotations", "Text body", None))
        self.btnBrowseSource.setText(_translate("SentAnnotations", "..", None))
        self.label.setText(_translate("SentAnnotations", "Data directoty:", None))
        self.label_5.setText(_translate("SentAnnotations", "Information:", None))
        self.label_2.setText(_translate("SentAnnotations", "Sent to (email):", None))
        self.labFiles2Sent.setText(_translate("SentAnnotations", "0", None))
        self.label_3.setText(_translate("SentAnnotations", "Annotations to sent:", None))
        self.btnSent.setText(_translate("SentAnnotations", "Sent", None))

import resources_rc
