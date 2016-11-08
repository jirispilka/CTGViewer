# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddNoteUI.ui'
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

class Ui_AddNote(object):
    def setupUi(self, AddNote):
        AddNote.setObjectName(_fromUtf8("AddNote"))
        AddNote.resize(162, 160)
        AddNote.setMinimumSize(QtCore.QSize(160, 160))
        AddNote.setMaximumSize(QtCore.QSize(162, 160))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/note.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AddNote.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(AddNote)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textNote = QtGui.QTextEdit(AddNote)
        self.textNote.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textNote.setLineWrapColumnOrWidth(0)
        self.textNote.setAcceptRichText(False)
        self.textNote.setObjectName(_fromUtf8("textNote"))
        self.verticalLayout.addWidget(self.textNote)
        self.buttonBox = QtGui.QDialogButtonBox(AddNote)
        self.buttonBox.setMaximumSize(QtCore.QSize(167, 25))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddNote)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddNote.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddNote.reject)
        QtCore.QMetaObject.connectSlotsByName(AddNote)

    def retranslateUi(self, AddNote):
        AddNote.setWindowTitle(_translate("AddNote", "Add Note", None))

import resources_rc
