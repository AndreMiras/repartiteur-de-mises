#!/usr/bin/python -d

import sys
from PyQt4 import QtCore, QtGui
from gui import Ui_Form
from distributor import Distributor


class MyForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.okCancelButtonBox,
            QtCore.SIGNAL("accepted()"), self.get_quotes)
        QtCore.QObject.connect(
            self.ui.okCancelButtonBox.button(
            QtGui.QDialogButtonBox.Reset),
            QtCore.SIGNAL("clicked()"), self.clear_content)
        QtCore.QObject.connect(self.ui.tableWidget,
            QtCore.SIGNAL("itemSelectionChanged()"), self.get_quotes)
        QtCore.QObject.connect(self.ui.integerBetCheckBox,
            QtCore.SIGNAL("stateChanged(int)"), self.get_quotes)
        QtCore.QObject.connect(self.ui.targetedProfitSpinBox,
            QtCore.SIGNAL("valueChanged(int)"), self.get_quotes)
        QtCore.QObject.connect(self.ui.addColumnPushButton,
            QtCore.SIGNAL("clicked()"), self.add_empty_column)
        QtCore.QObject.connect(self.ui.removeColumnPushButton,
            QtCore.SIGNAL("clicked()"), self.remove_last_column)
        self.n_pmu_row = 0
        self.quotes_row = 1
        self.bets_row = 2
        self.effective_profits_row = 3
        self.clear_content()

    def clear_content(self):
        self.ui.totalBetLabel.setNum(0)
        QtGui.QApplication.processEvents()
        self.ui.tableWidget.clearContents()
        self.init_columns()

    def init_columns(self):
        """
        - Changes the default columns width.
        - Adds PMU numbers to the PMU column.
        """
        self.init_n_pmu_columns()
        self.init_columns_width()

    def init_columns_width(self):
        """
        Smaller default column width.
        """
        for i in range(self.ui.tableWidget.columnCount()):
            self.ui.tableWidget.setColumnWidth(i, 45)
            nTableWidgetItem = QtGui.QTableWidgetItem(str(i + 1))
            self.ui.tableWidget.setItem(
                self.n_pmu_row, i, nTableWidgetItem)

    def init_n_pmu_columns(self):
        """
        Adds default (incremental) N PMU columns values.
        """
        for i in range(self.ui.tableWidget.columnCount()):
            nTableWidgetItem = QtGui.QTableWidgetItem(str(i + 1))
            self.ui.tableWidget.setItem(self.n_pmu_row, i, nTableWidgetItem)

    def add_empty_column(self):
        column_count = self.ui.tableWidget.columnCount()
        self.ui.tableWidget.setColumnCount(column_count + 1)
        self.init_columns()

    def remove_last_column(self):
        column_count = self.ui.tableWidget.columnCount()
        self.ui.tableWidget.setColumnCount(column_count - 1)

    def get_used_columns_indexes(self):
        """
        Returns a list of used TableWidgetItem.
        i.e. only the ones that have a "Mise" set.
        """
        indexes = []
        for i in range(self.ui.tableWidget.columnCount()):
            tableWidgetItem = self.ui.tableWidget.item(
                self.quotes_row, i)
            if (tableWidgetItem and tableWidgetItem.text()):
                indexes.append(i)
        return indexes

    def get_quotes(self):
        quotes = []
        nb_quotes = self.ui.tableWidget.columnCount()
        targeted_profit = self.ui.targetedProfitSpinBox.value()
        for i in range(nb_quotes):
            # val = a->text().toInt();
            tableWidgetItem = self.ui.tableWidget.item(self.quotes_row, i)
            if (tableWidgetItem and tableWidgetItem.text()):
                quote = int(tableWidgetItem.text())
                quotes.append(quote)
                # quotes = (5, 8, 7, 12, 10, 7)
        self.resolve_and_set_view(targeted_profit, quotes)

    def resolve_and_set_view(self, targeted_profit, quotes):
        dist = Distributor(targeted_profit, quotes)
        dist.set_integer_only(self.ui.integerBetCheckBox.isChecked());
        bets = dist.get_bets()
        effective_profits = dist.get_effective_profits()
        used_indexes = self.get_used_columns_indexes()
        nb_bets = len(bets)
        for i in range(nb_bets):
            bet = bets[i]
            used_index = used_indexes[i]
            effective_profit = effective_profits[i]
            betTableWidgetItem = QtGui.QTableWidgetItem(str(bet))
            betTableWidgetItem.setFlags(
                QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            effectiveProfitTableWidgetItem = \
                QtGui.QTableWidgetItem(str(effective_profit))
            effectiveProfitTableWidgetItem.setFlags(
                QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(
                self.bets_row, used_index, betTableWidgetItem)
            self.ui.tableWidget.setItem(
                self.effective_profits_row, used_index,
                effectiveProfitTableWidgetItem)
        self.ui.totalBetLabel.setNum(dist.get_total_bet())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
