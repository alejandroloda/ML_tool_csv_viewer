#  __  __         _         _____
# |  \/  |       (_)       |  __ \
# | \  / |  __ _  _  _ __  | |__) |_ __  ___    __ _  _ __  __ _  _ __ ___
# | |\/| | / _` || || '_ \ |  ___/| '__|/ _ \  / _` || '__|/ _` || '_ ` _ \
# | |  | || (_| || || | | || |    | |  | (_) || (_| || |  | (_| || | | | | |
# |_|  |_| \__,_||_||_| |_||_|    |_|   \___/  \__, ||_|   \__,_||_| |_| |_|
#                                               __/ |
#                                              |___/
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel

import pandas as pd

from file_selector import FileSelector


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


class MyMainWindow(QMainWindow):
    def __init__(self, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.geometry = (300, 300, 1000, 500)
        self.setGeometry(*self.geometry)

        # File explorer
        self.dockWidget_file_explorer = QDockWidget(self)
        self.dockWidget_file_explorer.setFloating(False)
        self.file_explorer = FileSelector(self)
        self.dockWidget_file_explorer.setWidget(self.file_explorer)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget_file_explorer)

        # Reader
        self.table = QTableView()

        df = pd.DataFrame([['valid', 'csv']], columns=['Waiting', 'for'])
        self.refresh_model(df)
        self.setCentralWidget(self.table)

    def refresh_model(self, df):
        if type(df) is str:
            df = pd.read_csv(df, sep=';')

        model = PandasModel(df)
        self.table.setModel(model)


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow("ML tool")
    window.show()
    sys.exit(app.exec_())
