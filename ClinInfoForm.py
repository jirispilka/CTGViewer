# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import sys
from PyQt4.QtGui import QApplication, QWidget, QFont


from ClinInfoWidgetUI import Ui_ClinInfoWidget


# list_clin_info = ['pH','BDecf','pCO2','BE','Apgar1','Apgar5','NICU_days','Seizures','HIE',
#                   'Intubation','Main_diag','Other_diag','Gest_weeks','Weight_g','Sex',
#                   'Age','Gravidity','Parity','Diabetes','Hypertension','Preeclampsia',
#                   'Liq_praecox','Pyrexia','Meconium','Presentation','Induced','Istage',
#                   'NoProgress','CK_KP','IIstage','Deliv_type','dbID','Rec_type','Pos_IIst','Sig2Birth']

dictClinInfoFullNames = dict()
dictClinInfoFullNames['name'] = 'Name'
dictClinInfoFullNames['pH'] = 'pH'
dictClinInfoFullNames['BDecf'] = 'BDecf'
dictClinInfoFullNames['BE'] = 'BE'
dictClinInfoFullNames['Apgar1'] = 'Apgar 1 min.'
dictClinInfoFullNames['Apgar5'] = 'Apgar 5 min.'
dictClinInfoFullNames['NICU_days'] = 'NICU [days]'
dictClinInfoFullNames['Seizures'] = 'Seizures'
dictClinInfoFullNames['HIE'] = 'HIE'
dictClinInfoFullNames['Intubation'] = 'Intubation'
dictClinInfoFullNames['Main_diag'] = 'Main diagnosis'
dictClinInfoFullNames['Other_diag'] = 'Other diagnoses'
dictClinInfoFullNames['Gest_weeks'] = 'Gestation [weeks]'
dictClinInfoFullNames['Weight_g'] = 'weight [g]'
dictClinInfoFullNames['Sex'] = 'Sex'
dictClinInfoFullNames['Age'] = 'Age'
dictClinInfoFullNames['Gravidity'] = 'Gravidity'
dictClinInfoFullNames['Parity'] = 'Parity'
dictClinInfoFullNames['Diabetes'] = 'Diabetes'
dictClinInfoFullNames['Hypertension'] = 'Hypertension'
dictClinInfoFullNames['Preeclampsia'] = 'Preeclampsia'
dictClinInfoFullNames['Liq_praecox'] = 'Liq_praecox'
dictClinInfoFullNames['Pyrexia'] = 'Pyrexia'
dictClinInfoFullNames['Meconium'] = 'Meconium'
dictClinInfoFullNames['Presentation'] = 'Presentation'
dictClinInfoFullNames['Induced'] = 'Induced'
dictClinInfoFullNames['Istage'] = 'Istage [min.]'
dictClinInfoFullNames['IIstage'] = 'IIstage [min.]'
dictClinInfoFullNames['NoProgress'] = 'NoProgress'
dictClinInfoFullNames['CK_KP'] = 'CK_KP'
dictClinInfoFullNames['Deliv_type'] = 'Delivery type'
dictClinInfoFullNames['Rec_type'] = 'Record type'
dictClinInfoFullNames['Pos_Ist'] = 'Position I stage [samples]'
dictClinInfoFullNames['Pos_IIst'] = 'Position II stage [samples]'
dictClinInfoFullNames['Sig2Birth'] = 'Distance Sig2Birth [min.]'
dictClinInfoFullNames['ClinAnnotation'] = 'Annotation (acidosis)'
dictClinInfoFullNames['resuscitationWard'] = 'Resuscitation on delivery ward'
dictClinInfoFullNames['NICU'] = 'NICU (yes/no)'
dictClinInfoFullNames['NICUacidosis'] = 'NICU (acidosis)'
dictClinInfoFullNames['Note'] = 'Note'

metainfofile = '.metainfo.csv'
metainfofile_md5sum = '.metainfo.md5sum'


class ClinInfo(QWidget):
    """
    classdocs
    """

    def __init__(self, parent=None):
        """
        Constructor
        """

        QWidget.__init__(self, parent)

        self.ui = Ui_ClinInfoWidget()
        self.ui.setupUi(self)

        self._textClear = 'N/A'

        self._fontChecked = QFont()
        self._fontChecked.setStrikeOut(False)

        self._fontNotChecked = QFont()
        self._fontNotChecked.setStrikeOut(True)

        self.clear_all()

    def clear_all(self):
        self.ui.label_apgar1.setText(self._textClear)
        self.ui.label_apgar5.setText(self._textClear)
        self.ui.label_bdecf.setText(self._textClear)
        self.ui.label_be.setText(self._textClear)
        self.ui.label_gravidity.setText(self._textClear)
        self.ui.label_IIstage.setText(self._textClear)
        self.ui.label_Istage.setText(self._textClear)
        self.ui.label_maternal_age.setText(self._textClear)
        self.ui.label_parity.setText(self._textClear)
        self.ui.label_pco2.setText(self._textClear)
        self.ui.label_ph.setText(self._textClear)
        self.ui.label_presentation.setText(self._textClear)
        self.ui.label_sex.setText(self._textClear)
        self.ui.label_sig2birth.setText(self._textClear)
        self.ui.label_week_gestation.setText(self._textClear)
        self.ui.label_weigth.setText(self._textClear)
        self.ui.label_annot.setText(self._textClear)

        # risk factors
        self.__set_label_not_present(self.ui.label_diabetes)
        self.__set_label_not_present(self.ui.label_fever)
        self.__set_label_not_present(self.ui.label_hypertension)
        self.__set_label_not_present(self.ui.label_libpreacox)
        self.__set_label_not_present(self.ui.label_meconium)
        self.__set_label_not_present(self.ui.label_preeclampsia)

    def set_all(self, dict_clin_info):

        self.clear_all()

        # print dictClinInfo.keys()
        self.__set_label(dict_clin_info, 'Apgar1', self.ui.label_apgar1)
        self.__set_label(dict_clin_info, 'Apgar5', self.ui.label_apgar5)
        self.__set_label(dict_clin_info, 'BDecf', self.ui.label_bdecf)
        self.__set_label(dict_clin_info, 'BE', self.ui.label_be)
        self.__set_label(dict_clin_info, 'Gravidity', self.ui.label_gravidity)
        self.__set_label(dict_clin_info, 'IIstage', self.ui.label_IIstage)
        self.__set_label(dict_clin_info, 'Istage', self.ui.label_Istage)
        self.__set_label(dict_clin_info, 'Age', self.ui.label_maternal_age)
        self.__set_label(dict_clin_info, 'Parity', self.ui.label_parity)
        self.__set_label(dict_clin_info, 'pCO2', self.ui.label_pco2)
        self.__set_label(dict_clin_info, 'pH', self.ui.label_ph)
        self.__set_label(dict_clin_info, 'Presentation', self.ui.label_presentation)
        self.__set_label(dict_clin_info, 'Sex', self.ui.label_sex)
        self.__set_label(dict_clin_info, 'Sig2Birth', self.ui.label_sig2birth)
        self.__set_label(dict_clin_info, 'Gest_weeks', self.ui.label_week_gestation)
        self.__set_label(dict_clin_info, 'Weight_g', self.ui.label_weigth)
        self.__set_label(dict_clin_info, 'ClinAnnotation', self.ui.label_annot)

        # ['Seizures', '', 'NoProgress', 'Intubation', '', 'CK_KP', '', '',
        # 'Induced', '', '', '', 'Pos_IIst', 'Deliv_type', '',
        # '', 'HIE', '', '', '', 'NICU_days', 'Main_diag', 'Pyrexia',
        # '', '', 'Rec_type', '', '', '', 'dbID', '', '', '', 'Other_diag', '']

        self.__set_risk_factors(dict_clin_info, 'Diabetes', self.ui.label_diabetes)
        self.__set_risk_factors(dict_clin_info, '', self.ui.label_fever)
        self.__set_risk_factors(dict_clin_info, 'Hypertension', self.ui.label_hypertension)
        self.__set_risk_factors(dict_clin_info, 'Liq_praecox', self.ui.label_libpreacox)
        self.__set_risk_factors(dict_clin_info, 'Meconium', self.ui.label_meconium)
        self.__set_risk_factors(dict_clin_info, 'Preeclampsia', self.ui.label_preeclampsia)

    def __set_label_not_present(self, label):
        label.setFont(self._fontNotChecked)
        label.setEnabled(False)

    def __set_label(self, dict_ci, key, label):
        if key in dict_ci:
            label.setText(str(dict_ci[key]))

    def __set_risk_factors(self, dict_ci, key, label):
        if key in dict_ci:
            if dict_ci[key] > 0:
                label.setFont(self._fontChecked)
                label.setEnabled(True)
                # checkBox.setCheckable(False)


def main():
    app = QApplication(sys.argv)

    window = ClinInfo()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
