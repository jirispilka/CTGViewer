# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExportPdfUI.ui'
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

class Ui_ExportToPdf(object):
    def setupUi(self, ExportToPdf):
        ExportToPdf.setObjectName(_fromUtf8("ExportToPdf"))
        ExportToPdf.resize(420, 470)
        self.gridLayout = QtGui.QGridLayout(ExportToPdf)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ExportToPdf)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.lnFileName = QtGui.QLineEdit(ExportToPdf)
        self.lnFileName.setObjectName(_fromUtf8("lnFileName"))
        self.gridLayout.addWidget(self.lnFileName, 1, 1, 1, 2)
        self.btnBrowse = QtGui.QPushButton(ExportToPdf)
        self.btnBrowse.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.gridLayout.addWidget(self.btnBrowse, 1, 3, 1, 1)
        self.gbAnn = QtGui.QGroupBox(ExportToPdf)
        self.gbAnn.setObjectName(_fromUtf8("gbAnn"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbAnn)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cbBasal = QtGui.QCheckBox(self.gbAnn)
        self.cbBasal.setChecked(True)
        self.cbBasal.setObjectName(_fromUtf8("cbBasal"))
        self.gridLayout_2.addWidget(self.cbBasal, 0, 0, 1, 1)
        self.btnSelectAll = QtGui.QPushButton(self.gbAnn)
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.gridLayout_2.addWidget(self.btnSelectAll, 0, 3, 1, 1)
        self.cbAccel = QtGui.QCheckBox(self.gbAnn)
        self.cbAccel.setObjectName(_fromUtf8("cbAccel"))
        self.gridLayout_2.addWidget(self.cbAccel, 7, 3, 1, 1)
        self.cbDecel = QtGui.QCheckBox(self.gbAnn)
        self.cbDecel.setTristate(False)
        self.cbDecel.setObjectName(_fromUtf8("cbDecel"))
        self.gridLayout_2.addWidget(self.cbDecel, 8, 3, 1, 1)
        self.cbUA = QtGui.QCheckBox(self.gbAnn)
        self.cbUA.setObjectName(_fromUtf8("cbUA"))
        self.gridLayout_2.addWidget(self.cbUA, 9, 3, 1, 1)
        self.cbFloatingBaseline = QtGui.QCheckBox(self.gbAnn)
        self.cbFloatingBaseline.setObjectName(_fromUtf8("cbFloatingBaseline"))
        self.gridLayout_2.addWidget(self.cbFloatingBaseline, 5, 3, 1, 1)
        self.cbMark = QtGui.QCheckBox(self.gbAnn)
        self.cbMark.setChecked(True)
        self.cbMark.setObjectName(_fromUtf8("cbMark"))
        self.gridLayout_2.addWidget(self.cbMark, 8, 0, 1, 1)
        self.cbNote = QtGui.QCheckBox(self.gbAnn)
        self.cbNote.setChecked(True)
        self.cbNote.setObjectName(_fromUtf8("cbNote"))
        self.gridLayout_2.addWidget(self.cbNote, 9, 0, 1, 1)
        self.cbExcessiveUA = QtGui.QCheckBox(self.gbAnn)
        self.cbExcessiveUA.setChecked(True)
        self.cbExcessiveUA.setObjectName(_fromUtf8("cbExcessiveUA"))
        self.gridLayout_2.addWidget(self.cbExcessiveUA, 7, 0, 1, 1)
        self.cbRecovery = QtGui.QCheckBox(self.gbAnn)
        self.cbRecovery.setChecked(True)
        self.cbRecovery.setObjectName(_fromUtf8("cbRecovery"))
        self.gridLayout_2.addWidget(self.cbRecovery, 4, 0, 1, 1)
        self.cbNoRecovery = QtGui.QCheckBox(self.gbAnn)
        self.cbNoRecovery.setChecked(True)
        self.cbNoRecovery.setObjectName(_fromUtf8("cbNoRecovery"))
        self.gridLayout_2.addWidget(self.cbNoRecovery, 5, 0, 1, 1)
        self.btnUnselect = QtGui.QPushButton(self.gbAnn)
        self.btnUnselect.setObjectName(_fromUtf8("btnUnselect"))
        self.gridLayout_2.addWidget(self.btnUnselect, 1, 3, 1, 1)
        self.cbBaseline = QtGui.QCheckBox(self.gbAnn)
        self.cbBaseline.setChecked(True)
        self.cbBaseline.setObjectName(_fromUtf8("cbBaseline"))
        self.gridLayout_2.addWidget(self.cbBaseline, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.gbAnn, 5, 1, 3, 3)
        self.gbPaper = QtGui.QGroupBox(ExportToPdf)
        self.gbPaper.setObjectName(_fromUtf8("gbPaper"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbPaper)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rbPaperEU = QtGui.QRadioButton(self.gbPaper)
        self.rbPaperEU.setObjectName(_fromUtf8("rbPaperEU"))
        self.verticalLayout.addWidget(self.rbPaperEU)
        self.rbPaperUS = QtGui.QRadioButton(self.gbPaper)
        self.rbPaperUS.setObjectName(_fromUtf8("rbPaperUS"))
        self.verticalLayout.addWidget(self.rbPaperUS)
        self.gridLayout.addWidget(self.gbPaper, 2, 1, 2, 3)
        self.buttonBox = QtGui.QDialogButtonBox(ExportToPdf)
        self.buttonBox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 16, 3, 1, 1)
        self.lbStatus = QtGui.QLabel(ExportToPdf)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lbStatus.setFont(font)
        self.lbStatus.setObjectName(_fromUtf8("lbStatus"))
        self.gridLayout.addWidget(self.lbStatus, 16, 1, 1, 2)

        self.retranslateUi(ExportToPdf)
        QtCore.QMetaObject.connectSlotsByName(ExportToPdf)

    def retranslateUi(self, ExportToPdf):
        ExportToPdf.setWindowTitle(_translate("ExportToPdf", "Export to PDF", None))
        self.label.setText(_translate("ExportToPdf", "File name:", None))
        self.btnBrowse.setText(_translate("ExportToPdf", "Browse", None))
        self.gbAnn.setTitle(_translate("ExportToPdf", "Annotations to export:", None))
        self.cbBasal.setText(_translate("ExportToPdf", "Basal", None))
        self.btnSelectAll.setText(_translate("ExportToPdf", "Select all", None))
        self.cbAccel.setText(_translate("ExportToPdf", "Accelerations", None))
        self.cbDecel.setText(_translate("ExportToPdf", "Decelerations", None))
        self.cbUA.setText(_translate("ExportToPdf", "Uterine contractions", None))
        self.cbFloatingBaseline.setText(_translate("ExportToPdf", "Floating baseline", None))
        self.cbMark.setText(_translate("ExportToPdf", "Mark", None))
        self.cbNote.setText(_translate("ExportToPdf", "Note", None))
        self.cbExcessiveUA.setText(_translate("ExportToPdf", "Excessive UA", None))
        self.cbRecovery.setText(_translate("ExportToPdf", "Recovery", None))
        self.cbNoRecovery.setText(_translate("ExportToPdf", "No recovery", None))
        self.btnUnselect.setText(_translate("ExportToPdf", "Unselect all", None))
        self.cbBaseline.setText(_translate("ExportToPdf", "Baseline", None))
        self.gbPaper.setTitle(_translate("ExportToPdf", "Paper format", None))
        self.rbPaperEU.setText(_translate("ExportToPdf", "EU (1cm/min, 20bpm/cm)", None))
        self.rbPaperUS.setText(_translate("ExportToPdf", "US (3cm/min, 30bpm/cm)", None))
        self.lbStatus.setText(_translate("ExportToPdf", "(saving to pdf might take a while)", None))

