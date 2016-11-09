# -*- coding: utf-8 -*-
#
# Created on Mar 8, 2014
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see ctgViewer.py for details)

"""
DataBrowserSelectAttributesForm
-------------------------------

Select attributes that will be used for browsing database files

"""

import logging
import sys
from PyQt4 import QtGui, QtCore, Qt

from ClinInfoForm import dictClinInfoFullNames
from Config import ConfigStatic, ConfigIni
from DataBrowserSelectAttrUI import Ui_DataBrowserSelectAttrWin
from Enums import EnumIniVar


class DataBrowserSelectAttrForm(QtGui.QWidget):

    signal_sel_att_changed = QtCore.pyqtSignal()

    def __init__(self, config_ini=None):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_DataBrowserSelectAttrWin()
        self.ui.setupUi(self)

        self._log = logging.getLogger(ConfigStatic.logger_name)
        self._log.info('passed')

        # CONFIG
        if config_ini is None:
            self._config_ini = ConfigIni()
        else:
            self._config_ini = config_ini

        self._modelSelectedAtt = QtGui.QStandardItemModel()
        self._modelAvailableAtt = QtGui.QStandardItemModel()

        self.ui.listSelected.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)
        self.ui.listAvailable.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)

        self.connect(self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save), QtCore.SIGNAL('clicked()'), self._save)
        self.connect(self.ui.buttonBox.button(QtGui.QDialogButtonBox.Close), QtCore.SIGNAL('clicked()'), self._cancel)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(False)

        # self.connect(self.ui.btnMoveDown, QtCore.SIGNAL('clicked()'), self._btn_down)
        self.connect(self.ui.btnMoveDown, QtCore.SIGNAL('pressed()'), self._btn_down)

        self.connect(self.ui.btnMoveUp, QtCore.SIGNAL('clicked()'), self._btn_up)
        self.connect(self.ui.btnRigthAll, QtCore.SIGNAL('clicked()'), self._btn_rigth_all)
        self.connect(self.ui.btnLeftAll, QtCore.SIGNAL('clicked()'), self._btn_left_all)
        self.connect(self.ui.btnlLeftSelected, QtCore.SIGNAL('clicked()'), self._btn_left_selected)
        self.connect(self.ui.btnRigthSelected, QtCore.SIGNAL('clicked()'), self._btn_rigth_selected)

        self._selected_att = self._config_ini.get_var(EnumIniVar.dataBrowserSelectedAttributes)
        self._availableAtt = dictClinInfoFullNames
        self.ui.listSelected.setModel(self._modelSelectedAtt)

        self._set_model_list_views()

    def _set_model_list_views(self):

        for att in self._availableAtt.keys():
            # print att

            if att in self._selected_att:
                self._modelSelectedAtt.appendRow(QtGui.QStandardItem(self._availableAtt[att]))
            else:
                self._modelAvailableAtt.appendRow(QtGui.QStandardItem(self._availableAtt[att]))

        self.ui.listSelected.setModel(self._modelSelectedAtt)
        self.ui.listAvailable.setModel(self._modelAvailableAtt)

        # self._modelSelectedAtt.sort(0)
        self._modelAvailableAtt.sort(0)

    def _cancel(self):
        self.close()

    def _btn_down(self):

        indicies = self.ui.listSelected.selectedIndexes()
        nr_rows = self._modelSelectedAtt.rowCount()

        if len(indicies) == 1:
            row = indicies[0].row()

            if row + 1 == nr_rows:
                return

            item = QtGui.QStandardItem(self._modelSelectedAtt.item(row))
            item_below = QtGui.QStandardItem(self._modelSelectedAtt.item(row+1))

            self._modelSelectedAtt.setItem(row, item_below)
            self._modelSelectedAtt.setItem(row+1, item)

            index = self._modelSelectedAtt.index(row+1, 0)
            self.ui.listSelected.setCurrentIndex(index)

            self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(True)

    def _btn_up(self):

        indicies = self.ui.listSelected.selectedIndexes()
        nr_rows = self._modelSelectedAtt.rowCount()

        if len(indicies) == 1:
            row = indicies[0].row()

            if row - 1 < 0:
                return

            item = QtGui.QStandardItem(self._modelSelectedAtt.item(row))
            item_above = QtGui.QStandardItem(self._modelSelectedAtt.item(row-1))

            self._modelSelectedAtt.setItem(row, item_above)
            self._modelSelectedAtt.setItem(row-1, item)

            index = self._modelSelectedAtt.index(row-1, 0)
            self.ui.listSelected.setCurrentIndex(index)

            self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(True)

    def _btn_left_all(self):

        self.ui.listAvailable.selectAll()
        self._btn_left_selected()

    def _btn_left_selected(self):
        """
        Move the selected indicies to the left column
        """
        indicies = self.ui.listAvailable.selectedIndexes()

        if len(indicies) > 0:
            row = indicies[0].row()
            item = QtGui.QStandardItem(self._modelAvailableAtt.item(row))
            self._modelAvailableAtt.removeRow(row)
            self._modelSelectedAtt.appendRow(item)
            self._btn_left_selected()  # recursively remove
            self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(True)

    def _btn_rigth_all(self):

        self.ui.listSelected.selectAll()
        self._btn_rigth_selected()

    def _btn_rigth_selected(self):

        indicies = self.ui.listSelected.selectedIndexes()

        if len(indicies) > 0:
            row = indicies[0].row()
            item = QtGui.QStandardItem(self._modelSelectedAtt.item(row))
            self._modelSelectedAtt.removeRow(row)
            self._modelAvailableAtt.appendRow(item)
            self._btn_rigth_selected()  # recursively remove
            self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(True)

    def _save(self):

        # selected_att = list()  # delete list of selected attributes
        self._selected_att = []

        # get items in model
        for i in range(self._modelSelectedAtt.rowCount()):
            # print i
            item = self._modelSelectedAtt.item(i)
            s = item.text()

            dict1 = self._availableAtt.iteritems()
            # iterate through all attributes to get key under which the attributes are stored in physionet header
            for d in dict1:
                if s == d[1]:
                    self._selected_att.append(d[0])

        # temp = str(self._selectedAtt).strip('[]')
        self._config_ini.set_var(EnumIniVar.dataBrowserSelectedAttributes, self._selected_att)
        self._config_ini.write_config()
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(False)
        self.signal_sel_att_changed.emit()

    def get_selected_att(self):
        return self._selected_att

    def closeEvent(self, event):

        self._modelAvailableAtt.sort(0)

        if self.ui.buttonBox.button(QtGui.QDialogButtonBox.Save).isEnabled() is False:
            return

        msgboxwarning = QtGui.QMessageBox()
        msgboxwarning.setText('There are unsaved changes.')
        msgboxwarning.setInformativeText('Save them now?')
        msgboxwarning.setIcon(QtGui.QMessageBox.Warning)
        msgboxwarning.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        ret = msgboxwarning.exec_()

        if ret == QtGui.QMessageBox.Yes:
            self._save()


def main():
    app = QtGui.QApplication(sys.argv)
    window = DataBrowserSelectAttrForm()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()