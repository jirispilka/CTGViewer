# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClinInfoWidgetUI.ui'
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

class Ui_ClinInfoWidget(object):
    def setupUi(self, ClinInfoWidget):
        ClinInfoWidget.setObjectName(_fromUtf8("ClinInfoWidget"))
        ClinInfoWidget.resize(323, 525)
        self.gridLayout = QtGui.QGridLayout(ClinInfoWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gpRiskFactors = QtGui.QGroupBox(ClinInfoWidget)
        self.gpRiskFactors.setObjectName(_fromUtf8("gpRiskFactors"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gpRiskFactors)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_hypertension = QtGui.QLabel(self.gpRiskFactors)
        self.label_hypertension.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_hypertension.setObjectName(_fromUtf8("label_hypertension"))
        self.verticalLayout.addWidget(self.label_hypertension)
        self.label_preeclampsia = QtGui.QLabel(self.gpRiskFactors)
        self.label_preeclampsia.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_preeclampsia.setObjectName(_fromUtf8("label_preeclampsia"))
        self.verticalLayout.addWidget(self.label_preeclampsia)
        self.label_diabetes = QtGui.QLabel(self.gpRiskFactors)
        self.label_diabetes.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_diabetes.setObjectName(_fromUtf8("label_diabetes"))
        self.verticalLayout.addWidget(self.label_diabetes)
        self.label_meconium = QtGui.QLabel(self.gpRiskFactors)
        self.label_meconium.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_meconium.setObjectName(_fromUtf8("label_meconium"))
        self.verticalLayout.addWidget(self.label_meconium)
        self.label_fever = QtGui.QLabel(self.gpRiskFactors)
        self.label_fever.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_fever.setObjectName(_fromUtf8("label_fever"))
        self.verticalLayout.addWidget(self.label_fever)
        self.label_libpreacox = QtGui.QLabel(self.gpRiskFactors)
        self.label_libpreacox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_libpreacox.setObjectName(_fromUtf8("label_libpreacox"))
        self.verticalLayout.addWidget(self.label_libpreacox)
        self.gridLayout.addWidget(self.gpRiskFactors, 2, 0, 2, 1)
        self.gpBiochem = QtGui.QGroupBox(ClinInfoWidget)
        self.gpBiochem.setObjectName(_fromUtf8("gpBiochem"))
        self.formLayout_2 = QtGui.QFormLayout(self.gpBiochem)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label1 = QtGui.QLabel(self.gpBiochem)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label1)
        self.label_ph = QtGui.QLabel(self.gpBiochem)
        self.label_ph.setObjectName(_fromUtf8("label_ph"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_ph)
        self.label2 = QtGui.QLabel(self.gpBiochem)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label2)
        self.label_be = QtGui.QLabel(self.gpBiochem)
        self.label_be.setObjectName(_fromUtf8("label_be"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_be)
        self.label3 = QtGui.QLabel(self.gpBiochem)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label3)
        self.label_bdecf = QtGui.QLabel(self.gpBiochem)
        self.label_bdecf.setObjectName(_fromUtf8("label_bdecf"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_bdecf)
        self.label3_2 = QtGui.QLabel(self.gpBiochem)
        self.label3_2.setObjectName(_fromUtf8("label3_2"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label3_2)
        self.label_pco2 = QtGui.QLabel(self.gpBiochem)
        self.label_pco2.setObjectName(_fromUtf8("label_pco2"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.label_pco2)
        self.gridLayout.addWidget(self.gpBiochem, 1, 1, 2, 1)
        self.gpOtherOutcome = QtGui.QGroupBox(ClinInfoWidget)
        self.gpOtherOutcome.setObjectName(_fromUtf8("gpOtherOutcome"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gpOtherOutcome)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label1_7 = QtGui.QLabel(self.gpOtherOutcome)
        self.label1_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label1_7.setObjectName(_fromUtf8("label1_7"))
        self.gridLayout_2.addWidget(self.label1_7, 2, 0, 1, 2)
        self.label1_8 = QtGui.QLabel(self.gpOtherOutcome)
        self.label1_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label1_8.setObjectName(_fromUtf8("label1_8"))
        self.gridLayout_2.addWidget(self.label1_8, 3, 0, 2, 2)
        self.label_apgar1 = QtGui.QLabel(self.gpOtherOutcome)
        self.label_apgar1.setObjectName(_fromUtf8("label_apgar1"))
        self.gridLayout_2.addWidget(self.label_apgar1, 0, 2, 1, 2)
        self.label1_5 = QtGui.QLabel(self.gpOtherOutcome)
        self.label1_5.setObjectName(_fromUtf8("label1_5"))
        self.gridLayout_2.addWidget(self.label1_5, 0, 0, 1, 2)
        self.label1_6 = QtGui.QLabel(self.gpOtherOutcome)
        self.label1_6.setObjectName(_fromUtf8("label1_6"))
        self.gridLayout_2.addWidget(self.label1_6, 1, 0, 1, 2)
        self.label_apgar5 = QtGui.QLabel(self.gpOtherOutcome)
        self.label_apgar5.setObjectName(_fromUtf8("label_apgar5"))
        self.gridLayout_2.addWidget(self.label_apgar5, 1, 2, 1, 2)
        self.label_weigth = QtGui.QLabel(self.gpOtherOutcome)
        self.label_weigth.setObjectName(_fromUtf8("label_weigth"))
        self.gridLayout_2.addWidget(self.label_weigth, 2, 2, 1, 2)
        self.label_sex = QtGui.QLabel(self.gpOtherOutcome)
        self.label_sex.setObjectName(_fromUtf8("label_sex"))
        self.gridLayout_2.addWidget(self.label_sex, 3, 2, 2, 2)
        self.label_annot = QtGui.QLabel(self.gpOtherOutcome)
        self.label_annot.setObjectName(_fromUtf8("label_annot"))
        self.gridLayout_2.addWidget(self.label_annot, 5, 2, 1, 1)
        self.label1_9 = QtGui.QLabel(self.gpOtherOutcome)
        self.label1_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label1_9.setObjectName(_fromUtf8("label1_9"))
        self.gridLayout_2.addWidget(self.label1_9, 5, 0, 1, 2)
        self.gridLayout.addWidget(self.gpOtherOutcome, 3, 1, 1, 1)
        self.gpGeneral = QtGui.QGroupBox(ClinInfoWidget)
        self.gpGeneral.setObjectName(_fromUtf8("gpGeneral"))
        self.formLayout = QtGui.QFormLayout(self.gpGeneral)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label4 = QtGui.QLabel(self.gpGeneral)
        self.label4.setObjectName(_fromUtf8("label4"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label4)
        self.label_maternal_age = QtGui.QLabel(self.gpGeneral)
        self.label_maternal_age.setObjectName(_fromUtf8("label_maternal_age"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_maternal_age)
        self.label5 = QtGui.QLabel(self.gpGeneral)
        self.label5.setObjectName(_fromUtf8("label5"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label5)
        self.label_gravidity = QtGui.QLabel(self.gpGeneral)
        self.label_gravidity.setObjectName(_fromUtf8("label_gravidity"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_gravidity)
        self.label6 = QtGui.QLabel(self.gpGeneral)
        self.label6.setObjectName(_fromUtf8("label6"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label6)
        self.label_parity = QtGui.QLabel(self.gpGeneral)
        self.label_parity.setObjectName(_fromUtf8("label_parity"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_parity)
        self.label7_2 = QtGui.QLabel(self.gpGeneral)
        self.label7_2.setObjectName(_fromUtf8("label7_2"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label7_2)
        self.label_week_gestation = QtGui.QLabel(self.gpGeneral)
        self.label_week_gestation.setObjectName(_fromUtf8("label_week_gestation"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.label_week_gestation)
        self.label7 = QtGui.QLabel(self.gpGeneral)
        self.label7.setObjectName(_fromUtf8("label7"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label7)
        self.label_presentation = QtGui.QLabel(self.gpGeneral)
        self.label_presentation.setObjectName(_fromUtf8("label_presentation"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.label_presentation)
        self.gridLayout.addWidget(self.gpGeneral, 0, 0, 2, 1)
        self.groupBox = QtGui.QGroupBox(ClinInfoWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label1_2 = QtGui.QLabel(self.groupBox)
        self.label1_2.setObjectName(_fromUtf8("label1_2"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label1_2)
        self.label_Istage = QtGui.QLabel(self.groupBox)
        self.label_Istage.setObjectName(_fromUtf8("label_Istage"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_Istage)
        self.label_IIstage = QtGui.QLabel(self.groupBox)
        self.label_IIstage.setObjectName(_fromUtf8("label_IIstage"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_IIstage)
        self.label1_3 = QtGui.QLabel(self.groupBox)
        self.label1_3.setObjectName(_fromUtf8("label1_3"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label1_3)
        self.label1_4 = QtGui.QLabel(self.groupBox)
        self.label1_4.setObjectName(_fromUtf8("label1_4"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label1_4)
        self.label_sig2birth = QtGui.QLabel(self.groupBox)
        self.label_sig2birth.setObjectName(_fromUtf8("label_sig2birth"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_sig2birth)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)

        self.retranslateUi(ClinInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(ClinInfoWidget)

    def retranslateUi(self, ClinInfoWidget):
        ClinInfoWidget.setWindowTitle(_translate("ClinInfoWidget", "Form", None))
        self.gpRiskFactors.setTitle(_translate("ClinInfoWidget", "Risk factors", None))
        self.label_hypertension.setText(_translate("ClinInfoWidget", "Hypertension", None))
        self.label_preeclampsia.setText(_translate("ClinInfoWidget", "Pre-eclampsia", None))
        self.label_diabetes.setText(_translate("ClinInfoWidget", "Diabetes", None))
        self.label_meconium.setText(_translate("ClinInfoWidget", "Meconium", None))
        self.label_fever.setText(_translate("ClinInfoWidget", "Fever", None))
        self.label_libpreacox.setText(_translate("ClinInfoWidget", "Liq. preacox", None))
        self.gpBiochem.setTitle(_translate("ClinInfoWidget", "Biochemical markers", None))
        self.label1.setText(_translate("ClinInfoWidget", "pH:", None))
        self.label_ph.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label2.setText(_translate("ClinInfoWidget", "BE:", None))
        self.label_be.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label3.setText(_translate("ClinInfoWidget", "BDecf:", None))
        self.label_bdecf.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label3_2.setText(_translate("ClinInfoWidget", "pCO2:", None))
        self.label_pco2.setText(_translate("ClinInfoWidget", "N/A", None))
        self.gpOtherOutcome.setTitle(_translate("ClinInfoWidget", "Others outcomes", None))
        self.label1_7.setText(_translate("ClinInfoWidget", "Weigth [g]:", None))
        self.label1_8.setText(_translate("ClinInfoWidget", "Sex:", None))
        self.label_apgar1.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label1_5.setText(_translate("ClinInfoWidget", "Apgar 1 min:", None))
        self.label1_6.setText(_translate("ClinInfoWidget", "Apgar 5 min:", None))
        self.label_apgar5.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label_weigth.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label_sex.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label_annot.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label1_9.setText(_translate("ClinInfoWidget", "Annotation:", None))
        self.gpGeneral.setTitle(_translate("ClinInfoWidget", "General information", None))
        self.label4.setText(_translate("ClinInfoWidget", "Maternal age:", None))
        self.label_maternal_age.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label5.setText(_translate("ClinInfoWidget", "Gravidity:", None))
        self.label_gravidity.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label6.setText(_translate("ClinInfoWidget", "Parity:", None))
        self.label_parity.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label7_2.setText(_translate("ClinInfoWidget", "Week of gest.:", None))
        self.label_week_gestation.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label7.setText(_translate("ClinInfoWidget", "Presentation:", None))
        self.label_presentation.setText(_translate("ClinInfoWidget", "N/A", None))
        self.groupBox.setTitle(_translate("ClinInfoWidget", "Delivery details [min.]", None))
        self.label1_2.setText(_translate("ClinInfoWidget", "I. stage:", None))
        self.label_Istage.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label_IIstage.setText(_translate("ClinInfoWidget", "N/A", None))
        self.label1_3.setText(_translate("ClinInfoWidget", "II. stage:", None))
        self.label1_4.setText(_translate("ClinInfoWidget", "sig. - birth:", None))
        self.label_sig2birth.setText(_translate("ClinInfoWidget", "N/A", None))

