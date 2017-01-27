# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnnShowHideUI.ui'
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

class Ui_AnnShowHideForm(object):
    def setupUi(self, AnnShowHideForm):
        AnnShowHideForm.setObjectName(_fromUtf8("AnnShowHideForm"))
        AnnShowHideForm.resize(279, 266)
        self.gridLayout = QtGui.QGridLayout(AnnShowHideForm)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cbBaseline = QtGui.QCheckBox(AnnShowHideForm)
        self.cbBaseline.setChecked(True)
        self.cbBaseline.setObjectName(_fromUtf8("cbBaseline"))
        self.gridLayout.addWidget(self.cbBaseline, 1, 0, 1, 1)
        self.cbNoRecovery = QtGui.QCheckBox(AnnShowHideForm)
        self.cbNoRecovery.setChecked(True)
        self.cbNoRecovery.setObjectName(_fromUtf8("cbNoRecovery"))
        self.gridLayout.addWidget(self.cbNoRecovery, 3, 0, 1, 1)
        self.btnUnselect = QtGui.QPushButton(AnnShowHideForm)
        self.btnUnselect.setObjectName(_fromUtf8("btnUnselect"))
        self.gridLayout.addWidget(self.btnUnselect, 1, 1, 1, 1)
        self.cbRecovery = QtGui.QCheckBox(AnnShowHideForm)
        self.cbRecovery.setChecked(True)
        self.cbRecovery.setObjectName(_fromUtf8("cbRecovery"))
        self.gridLayout.addWidget(self.cbRecovery, 2, 0, 1, 1)
        self.cbAccel = QtGui.QCheckBox(AnnShowHideForm)
        self.cbAccel.setChecked(True)
        self.cbAccel.setObjectName(_fromUtf8("cbAccel"))
        self.gridLayout.addWidget(self.cbAccel, 4, 1, 1, 1)
        self.cbFloatingBaseline = QtGui.QCheckBox(AnnShowHideForm)
        self.cbFloatingBaseline.setChecked(True)
        self.cbFloatingBaseline.setObjectName(_fromUtf8("cbFloatingBaseline"))
        self.gridLayout.addWidget(self.cbFloatingBaseline, 3, 1, 1, 1)
        self.cbExcessiveUA = QtGui.QCheckBox(AnnShowHideForm)
        self.cbExcessiveUA.setChecked(True)
        self.cbExcessiveUA.setObjectName(_fromUtf8("cbExcessiveUA"))
        self.gridLayout.addWidget(self.cbExcessiveUA, 4, 0, 1, 1)
        self.cbMark = QtGui.QCheckBox(AnnShowHideForm)
        self.cbMark.setChecked(True)
        self.cbMark.setObjectName(_fromUtf8("cbMark"))
        self.gridLayout.addWidget(self.cbMark, 5, 0, 1, 1)
        self.cbDecel = QtGui.QCheckBox(AnnShowHideForm)
        self.cbDecel.setChecked(True)
        self.cbDecel.setTristate(False)
        self.cbDecel.setObjectName(_fromUtf8("cbDecel"))
        self.gridLayout.addWidget(self.cbDecel, 5, 1, 1, 1)
        self.cbNote = QtGui.QCheckBox(AnnShowHideForm)
        self.cbNote.setChecked(True)
        self.cbNote.setObjectName(_fromUtf8("cbNote"))
        self.gridLayout.addWidget(self.cbNote, 6, 0, 1, 1)
        self.cbUA = QtGui.QCheckBox(AnnShowHideForm)
        self.cbUA.setChecked(True)
        self.cbUA.setObjectName(_fromUtf8("cbUA"))
        self.gridLayout.addWidget(self.cbUA, 6, 1, 1, 1)
        self.cbBasal = QtGui.QCheckBox(AnnShowHideForm)
        self.cbBasal.setChecked(True)
        self.cbBasal.setObjectName(_fromUtf8("cbBasal"))
        self.gridLayout.addWidget(self.cbBasal, 0, 0, 1, 1)
        self.btnSelectAll = QtGui.QPushButton(AnnShowHideForm)
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.gridLayout.addWidget(self.btnSelectAll, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AnnShowHideForm)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)

        self.retranslateUi(AnnShowHideForm)
        QtCore.QMetaObject.connectSlotsByName(AnnShowHideForm)

    def retranslateUi(self, AnnShowHideForm):
        AnnShowHideForm.setWindowTitle(_translate("AnnShowHideForm", "Dialog", None))
        self.cbBaseline.setText(_translate("AnnShowHideForm", "Baseline", None))
        self.cbNoRecovery.setText(_translate("AnnShowHideForm", "No recovery", None))
        self.btnUnselect.setText(_translate("AnnShowHideForm", "Unselect all", None))
        self.cbRecovery.setText(_translate("AnnShowHideForm", "Recovery", None))
        self.cbAccel.setText(_translate("AnnShowHideForm", "Accelerations", None))
        self.cbFloatingBaseline.setText(_translate("AnnShowHideForm", "Floating baseline", None))
        self.cbExcessiveUA.setText(_translate("AnnShowHideForm", "Excessive UA", None))
        self.cbMark.setText(_translate("AnnShowHideForm", "Mark", None))
        self.cbDecel.setText(_translate("AnnShowHideForm", "Decelerations", None))
        self.cbNote.setText(_translate("AnnShowHideForm", "Note", None))
        self.cbUA.setText(_translate("AnnShowHideForm", "Uterine contractions", None))
        self.cbBasal.setText(_translate("AnnShowHideForm", "Basal", None))
        self.btnSelectAll.setText(_translate("AnnShowHideForm", "Select all", None))

