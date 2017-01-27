# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataBrowserSelectAttrUI.ui'
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

class Ui_DataBrowserSelectAttrWin(object):
    def setupUi(self, DataBrowserSelectAttrWin):
        DataBrowserSelectAttrWin.setObjectName(_fromUtf8("DataBrowserSelectAttrWin"))
        DataBrowserSelectAttrWin.resize(534, 442)
        self.gridLayout = QtGui.QGridLayout(DataBrowserSelectAttrWin)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 4, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.listAvailable = QtGui.QListView(DataBrowserSelectAttrWin)
        self.listAvailable.setObjectName(_fromUtf8("listAvailable"))
        self.gridLayout.addWidget(self.listAvailable, 1, 3, 10, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 10, 2, 1, 1)
        self.listSelected = QtGui.QListView(DataBrowserSelectAttrWin)
        self.listSelected.setObjectName(_fromUtf8("listSelected"))
        self.gridLayout.addWidget(self.listSelected, 1, 1, 10, 1)
        self.btnLeftAll = QtGui.QPushButton(DataBrowserSelectAttrWin)
        self.btnLeftAll.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/arrow-left-double-2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLeftAll.setIcon(icon)
        self.btnLeftAll.setObjectName(_fromUtf8("btnLeftAll"))
        self.gridLayout.addWidget(self.btnLeftAll, 9, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DataBrowserSelectAttrWin)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 11, 1, 1, 3)
        self.label = QtGui.QLabel(DataBrowserSelectAttrWin)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(DataBrowserSelectAttrWin)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.btnRigthAll = QtGui.QPushButton(DataBrowserSelectAttrWin)
        self.btnRigthAll.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/arrow-right-double-2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRigthAll.setIcon(icon1)
        self.btnRigthAll.setObjectName(_fromUtf8("btnRigthAll"))
        self.gridLayout.addWidget(self.btnRigthAll, 2, 2, 1, 1)
        self.btnRigthSelected = QtGui.QPushButton(DataBrowserSelectAttrWin)
        self.btnRigthSelected.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/arrow-right-2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRigthSelected.setIcon(icon2)
        self.btnRigthSelected.setObjectName(_fromUtf8("btnRigthSelected"))
        self.gridLayout.addWidget(self.btnRigthSelected, 3, 2, 1, 1)
        self.btnlLeftSelected = QtGui.QPushButton(DataBrowserSelectAttrWin)
        self.btnlLeftSelected.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/arrow-left-2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnlLeftSelected.setIcon(icon3)
        self.btnlLeftSelected.setObjectName(_fromUtf8("btnlLeftSelected"))
        self.gridLayout.addWidget(self.btnlLeftSelected, 8, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 8, 0, 4, 1)
        self.btnMoveDown = QtGui.QPushButton(DataBrowserSelectAttrWin)
        self.btnMoveDown.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/arrow-down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMoveDown.setIcon(icon4)
        self.btnMoveDown.setObjectName(_fromUtf8("btnMoveDown"))
        self.gridLayout.addWidget(self.btnMoveDown, 7, 0, 1, 1)
        self.btnMoveUp = QtGui.QPushButton(DataBrowserSelectAttrWin)
        self.btnMoveUp.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/arrow-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMoveUp.setIcon(icon5)
        self.btnMoveUp.setObjectName(_fromUtf8("btnMoveUp"))
        self.gridLayout.addWidget(self.btnMoveUp, 6, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 6, 2, 2, 1)

        self.retranslateUi(DataBrowserSelectAttrWin)
        QtCore.QMetaObject.connectSlotsByName(DataBrowserSelectAttrWin)

    def retranslateUi(self, DataBrowserSelectAttrWin):
        DataBrowserSelectAttrWin.setWindowTitle(_translate("DataBrowserSelectAttrWin", "Data browser - select attributes to view", None))
        self.label.setText(_translate("DataBrowserSelectAttrWin", "Selected attributes", None))
        self.label_2.setText(_translate("DataBrowserSelectAttrWin", "Available attributes", None))

import resources_rc
