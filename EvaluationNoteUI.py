# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EvaluationNoteUI.ui'
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

class Ui_EvaluationNote(object):
    def setupUi(self, EvaluationNote):
        EvaluationNote.setObjectName(_fromUtf8("EvaluationNote"))
        EvaluationNote.resize(395, 264)
        self.gridLayout = QtGui.QGridLayout(EvaluationNote)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(EvaluationNote)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 3)
        self.label_4 = QtGui.QLabel(EvaluationNote)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.cbIntervention = QtGui.QComboBox(EvaluationNote)
        self.cbIntervention.setObjectName(_fromUtf8("cbIntervention"))
        self.gridLayout.addWidget(self.cbIntervention, 2, 1, 1, 2)
        self.label = QtGui.QLabel(EvaluationNote)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.sbLevelConcern = QtGui.QSpinBox(EvaluationNote)
        self.sbLevelConcern.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbLevelConcern.setMinimum(-1)
        self.sbLevelConcern.setMaximum(10)
        self.sbLevelConcern.setProperty("value", -1)
        self.sbLevelConcern.setObjectName(_fromUtf8("sbLevelConcern"))
        self.gridLayout.addWidget(self.sbLevelConcern, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(EvaluationNote)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(EvaluationNote)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(EvaluationNote)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.btnClearInterventation = QtGui.QPushButton(EvaluationNote)
        self.btnClearInterventation.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/icons/clear.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClearInterventation.setIcon(icon)
        self.btnClearInterventation.setObjectName(_fromUtf8("btnClearInterventation"))
        self.gridLayout.addWidget(self.btnClearInterventation, 2, 3, 1, 1)
        self.cbNeurology = QtGui.QComboBox(EvaluationNote)
        self.cbNeurology.setObjectName(_fromUtf8("cbNeurology"))
        self.gridLayout.addWidget(self.cbNeurology, 4, 1, 1, 2)
        self.btnClearNeurology = QtGui.QPushButton(EvaluationNote)
        self.btnClearNeurology.setText(_fromUtf8(""))
        self.btnClearNeurology.setIcon(icon)
        self.btnClearNeurology.setObjectName(_fromUtf8("btnClearNeurology"))
        self.gridLayout.addWidget(self.btnClearNeurology, 4, 3, 1, 1)
        self.btnClearInitialCTG = QtGui.QPushButton(EvaluationNote)
        self.btnClearInitialCTG.setText(_fromUtf8(""))
        self.btnClearInitialCTG.setIcon(icon)
        self.btnClearInitialCTG.setObjectName(_fromUtf8("btnClearInitialCTG"))
        self.gridLayout.addWidget(self.btnClearInitialCTG, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(EvaluationNote)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.btnClearLevelConcern = QtGui.QPushButton(EvaluationNote)
        self.btnClearLevelConcern.setText(_fromUtf8(""))
        self.btnClearLevelConcern.setIcon(icon)
        self.btnClearLevelConcern.setObjectName(_fromUtf8("btnClearLevelConcern"))
        self.gridLayout.addWidget(self.btnClearLevelConcern, 1, 3, 1, 1)
        self.sbph = QtGui.QDoubleSpinBox(EvaluationNote)
        self.sbph.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbph.setMinimum(6.5)
        self.sbph.setMaximum(7.5)
        self.sbph.setSingleStep(0.1)
        self.sbph.setProperty("value", 6.5)
        self.sbph.setObjectName(_fromUtf8("sbph"))
        self.gridLayout.addWidget(self.sbph, 3, 1, 1, 2)
        self.btnClearPh = QtGui.QPushButton(EvaluationNote)
        self.btnClearPh.setText(_fromUtf8(""))
        self.btnClearPh.setIcon(icon)
        self.btnClearPh.setObjectName(_fromUtf8("btnClearPh"))
        self.gridLayout.addWidget(self.btnClearPh, 3, 3, 1, 1)
        self.cbInitialCTG = QtGui.QComboBox(EvaluationNote)
        self.cbInitialCTG.setObjectName(_fromUtf8("cbInitialCTG"))
        self.gridLayout.addWidget(self.cbInitialCTG, 0, 1, 1, 2)

        self.retranslateUi(EvaluationNote)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EvaluationNote.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EvaluationNote.reject)
        QtCore.QMetaObject.connectSlotsByName(EvaluationNote)
        EvaluationNote.setTabOrder(self.sbLevelConcern, self.cbIntervention)
        EvaluationNote.setTabOrder(self.cbIntervention, self.cbNeurology)

    def retranslateUi(self, EvaluationNote):
        EvaluationNote.setWindowTitle(_translate("EvaluationNote", "Evaluation note", None))
        self.label_4.setText(_translate("EvaluationNote", "Initial CTG:", None))
        self.label.setText(_translate("EvaluationNote", "Level of concern:", None))
        self.label_5.setText(_translate("EvaluationNote", "Intervention:", None))
        self.label_3.setText(_translate("EvaluationNote", "pH:", None))
        self.label_6.setText(_translate("EvaluationNote", "Neurological level:", None))
        self.label_2.setText(_translate("EvaluationNote", "score: (0-10)", None))

import resources_rc
