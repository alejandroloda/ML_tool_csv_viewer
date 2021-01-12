import pandas as pd

from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel


class PandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data
        self.header_labels = data.columns

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)


class AwesomeTable(QTableView):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.columns = []
        self.visible_columns = []
        # self.doubleClicked.connect(self.print_column_name)
        self.horizontalHeader().sectionDoubleClicked.connect(self.toggle_column_visibility)

    def refresh_table(self, df):
        if type(df) is str:
            df = pd.read_csv(df, sep=';')
        model = PandasModel(df)
        self.columns = df.columns
        self.visible_columns = [1 for _ in self.columns]
        self.setModel(model)

    def toggle_column_visibility(self, n=None):
        if n is None:
            n = self.get_column_number()
        try:
            visibility = True if self.visible_columns[n] == 1 else False
            self.visible_columns[n] = 0 if visibility else 1
            self.setColumnHidden(n, visibility)
        except Exception as err:
            print(str(err))

    def show_all_columns(self):
        for index, status in enumerate(self.visible_columns):
            if status == 0:
                self.toggle_column_visibility(index)

    def get_column_number(self):
        try:
            if self.currentIndex().column() != -1:
                return self.currentIndex().column()
            return None
        except:
            return None

    def get_column_name(self):
        try:
            if self.currentIndex().column() != -1:
                # return self.model().get_items()[self.currentIndex().row()]
                return self.columns[self.currentIndex().column()]
            return None
        except:
            return None
