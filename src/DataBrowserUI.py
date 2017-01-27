# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataBrowserUI.ui'
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

class Ui_DataBrowser(object):
    def setupUi(self, DataBrowser):
        DataBrowser.setObjectName(_fromUtf8("DataBrowser"))
        DataBrowser.resize(191, 513)
        self.gridLayout = QtGui.QGridLayout(DataBrowser)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnNext = QtGui.QPushButton(DataBrowser)
        self.btnNext.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/next_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNext.setIcon(icon)
        self.btnNext.setObjectName(_fromUtf8("btnNext"))
        self.gridLayout.addWidget(self.btnNext, 3, 3, 1, 1)
        self.tableView = QtGui.QTableView(DataBrowser)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 4)
        self.labRecName = QtGui.QLabel(DataBrowser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labRecName.sizePolicy().hasHeightForWidth())
        self.labRecName.setSizePolicy(sizePolicy)
        self.labRecName.setMinimumSize(QtCore.QSize(0, 0))
        self.labRecName.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setKerning(True)
        self.labRecName.setFont(font)
        self.labRecName.setTextFormat(QtCore.Qt.PlainText)
        self.labRecName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labRecName.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.labRecName.setObjectName(_fromUtf8("labRecName"))
        self.gridLayout.addWidget(self.labRecName, 3, 1, 1, 1)
        self.btnPrev = QtGui.QPushButton(DataBrowser)
        self.btnPrev.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnPrev.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/previous_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPrev.setIcon(icon1)
        self.btnPrev.setObjectName(_fromUtf8("btnPrev"))
        self.gridLayout.addWidget(self.btnPrev, 3, 2, 1, 1)
        self.label = QtGui.QLabel(DataBrowser)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.retranslateUi(DataBrowser)
        QtCore.QMetaObject.connectSlotsByName(DataBrowser)

    def retranslateUi(self, DataBrowser):
        DataBrowser.setWindowTitle(_translate("DataBrowser", "BrowseFolder", None))
        self.btnNext.setToolTip(_translate("DataBrowser", "Next record (alt+right)", None))
        self.btnNext.setShortcut(_translate("DataBrowser", "Alt+Right", None))
        self.labRecName.setText(_translate("DataBrowser", "Record name", None))
        self.btnPrev.setToolTip(_translate("DataBrowser", "Previous record (alt+left)", None))
        self.btnPrev.setShortcut(_translate("DataBrowser", "Alt+Left", None))
        self.label.setText(_translate("DataBrowser", "Name", None))

import resources_rc
