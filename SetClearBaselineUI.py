# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SetClearBaselineUI.ui'
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

class Ui_SetBaselineUI(object):
    def setupUi(self, SetBaselineUI):
        SetBaselineUI.setObjectName(_fromUtf8("SetBaselineUI"))
        SetBaselineUI.resize(471, 45)
        self.gridLayout = QtGui.QGridLayout(SetBaselineUI)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnClose = QtGui.QPushButton(SetBaselineUI)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 0, 6, 1, 1)
        self.btnClear = QtGui.QPushButton(SetBaselineUI)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/application-exit-4.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClear.setIcon(icon)
        self.btnClear.setObjectName(_fromUtf8("btnClear"))
        self.gridLayout.addWidget(self.btnClear, 0, 5, 1, 1)
        self.label_2 = QtGui.QLabel(SetBaselineUI)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label = QtGui.QLabel(SetBaselineUI)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBox = QtGui.QSpinBox(SetBaselineUI)
        self.spinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBox.setAcceptDrops(False)
        self.spinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox.setAccelerated(True)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(250)
        self.spinBox.setProperty("value", 50)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.btnSet = QtGui.QPushButton(SetBaselineUI)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/valid-512.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSet.setIcon(icon1)
        self.btnSet.setObjectName(_fromUtf8("btnSet"))
        self.gridLayout.addWidget(self.btnSet, 0, 4, 1, 1)

        self.retranslateUi(SetBaselineUI)
        QtCore.QMetaObject.connectSlotsByName(SetBaselineUI)

    def retranslateUi(self, SetBaselineUI):
        SetBaselineUI.setWindowTitle(_translate("SetBaselineUI", "Set/Clear Baseline", None))
        self.btnClose.setText(_translate("SetBaselineUI", "Close", None))
        self.btnClear.setText(_translate("SetBaselineUI", "Clear", None))
        self.label_2.setText(_translate("SetBaselineUI", "BPM", None))
        self.label.setText(_translate("SetBaselineUI", "Baseline:", None))
        self.btnSet.setText(_translate("SetBaselineUI", "Set", None))

import resources_rc
