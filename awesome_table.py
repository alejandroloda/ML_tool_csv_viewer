import pandas as pd
import csv

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTableView, QFileDialog
from PyQt5.QtCore import Qt, QAbstractTableModel


class PandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        try:
            QAbstractTableModel.__init__(self, parent)
            self._data = data
            self.header_labels = data.columns
        except Exception as err:
            print(err)

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
        self.last_df = None

        # self.doubleClicked.connect(self.print_column_name)
        self.horizontalHeader().sectionDoubleClicked.connect(self.toggle_column_visibility)

    def refresh_table(self, df):
        if type(df) is str:
            df = pd.read_csv(df, sep=';')

        self.last_df = df
        model = PandasModel(df)
        self.columns = df.columns
        self.visible_columns = [1 for _ in self.columns]
        self.setModel(model)

    def body_head_tail_table(self, n, rows=5):
        try:
            # All visible
            [self.setRowHidden(i, False) for i in range(self.last_df.shape[0])]
            # Head
            if n == 0:
                [self.setRowHidden(i, True) for i in range(rows, self.last_df.shape[0])]
            # Tail
            elif n == 1:
                [self.setRowHidden(i, True) for i in range(0, self.last_df.shape[0] - rows)]
            # Body
            else:
                pass
        except Exception as err:
            print(err)

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

    def inverse_view(self):
        try:
            [self.toggle_column_visibility(n) for n in range(len(self.columns))]
        except Exception as err:
            print(err)

    # TODO Only save visible columns
    def download_csv_of_on_columns(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filename, _ = QFileDialog.getSaveFileName(self, "Choose CSV", "",
                                                      "CSV Files (*.csv);;All Files (*)", options=options)

            with open(filename, 'w') as stream:
                writer = csv.writer(stream, delimiter=';', lineterminator='\n')
                writer.writerow(self.columns)
                for row in range(self.model().rowCount()):
                    rowdata = []
                    for column in range(self.model().columnCount()):
                        # item = self.model().item(row, column)
                        item = self.model().index(row, column).data()
                        if item is not None:
                            rowdata.append(item)
                        else:
                            rowdata.append('')

                    writer.writerow(rowdata)
        except Exception as err:
            print(str(err))
