#  __  __         _         _____
# |  \/  |       (_)       |  __ \
# | \  / |  __ _  _  _ __  | |__) |_ __  ___    __ _  _ __  __ _  _ __ ___
# | |\/| | / _` || || '_ \ |  ___/| '__|/ _ \  / _` || '__|/ _` || '_ ` _ \
# | |  | || (_| || || | | || |    | |  | (_) || (_| || |  | (_| || | | | | |
# |_|  |_| \__,_||_||_| |_||_|    |_|   \___/  \__, ||_|   \__,_||_| |_| |_|
#                                               __/ |
#                                              |___/
import csv
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow, QPushButton, QHBoxLayout, \
    QLineEdit, QDockWidget, QTableView, QVBoxLayout

from PyQt5.QtCore import Qt, QAbstractTableModel



class FileSelector(QWidget):
    def __init__(self, main):
        super().__init__()
        self.file = ""
        self.main = main
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        self.text_file_explorer = QLineEdit(self)
        self.text_file_explorer.setReadOnly(True)
        hbox.addWidget(self.text_file_explorer)

        self.button_file_explorer = QPushButton('Elegir archivo', self)
        self.button_file_explorer.clicked.connect(self.openFileNameDialog)
        hbox.addWidget(self.button_file_explorer)

        self.button_refresh = QPushButton('Aplicar', self)
        # TODO
        # self.button_refresh.clicked.connect(self.openFileNameDialog)
        hbox.addWidget(self.button_refresh)

        self.setLayout(hbox)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Elegir CSV", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            self.file = filename
            self.text_file_explorer.setText(self.file)
            print(filename)


class PandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

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
        table = QTableView()

        import pandas as pd
        df = pd.read_csv("test.csv", sep=';')
        print(df)
        model = PandasModel(df)
        table.setModel(model)
    # self.table_view = MyWindow("test.csv")
        #
        self.setCentralWidget(table)


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow("ML tool")
    window.show()
    # ex = FileSelector()

    # self.pushButton = QtWidgets.QPushButton(Import_data)
    # self.pushButton.setGeometry(QtCore.QRect(600, 20, 81, 23))
    # self.pushButton.setObjectName("pushButton")
    # self.pushButton.clicked.connect(self.browse_data1)
    sys.exit(app.exec_())
