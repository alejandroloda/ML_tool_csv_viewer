#  __  __         _         _____
# |  \/  |       (_)       |  __ \
# | \  / |  __ _  _  _ __  | |__) |_ __  ___    __ _  _ __  __ _  _ __ ___
# | |\/| | / _` || || '_ \ |  ___/| '__|/ _ \  / _` || '__|/ _` || '_ ` _ \
# | |  | || (_| || || | | || |    | |  | (_) || (_| || |  | (_| || | | | | |
# |_|  |_| \__,_||_||_| |_||_|    |_|   \___/  \__, ||_|   \__,_||_| |_| |_|
#                                               __/ |
#                                              |___/

# TODO:
# - Dock lateral con acciones
# - Apagar/Encender columnas
# - Mostrar solo columnas encendidas/apagadas
# - Descargar csv modificado
# - Encontrar máximos y minimos en columnas
# - Aplicar modelos básicos

import sys
import pandas as pd

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTableView, QAction
from PyQt5.QtCore import Qt, QAbstractTableModel

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
        self.table = AwesomeTable(self)

        df = pd.DataFrame([['valid', 'csv']], columns=['Waiting', 'for'])
        self.refresh_table(df)
        self.setCentralWidget(self.table)

    def refresh_table(self, df):
        self.table.refresh_table(df)

    def reset_dock_view(self):
        self.dockWidget_file_explorer.setVisible(True)

    def off_column(self):
        # self.table.setColumnHidden(0, True)
        self.table.hideColumn(0)


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

    # def toggle_column_visibility(self, n=0):

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


if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow("ML tool")
    window.show()

    #  __  __
    # |  \/  | ___  _ _  _  _
    # | |\/| |/ -_)| ' \| || |
    # |_|  |_|\___||_||_|\_,_|
    menu_bar = window.menuBar()
    file_menu = menu_bar.addMenu("&View")
    new_action = QAction("All &dock actives")
    new_action.triggered.connect(window.reset_dock_view)
    # new_action.setShortcut(QKeySequence.New)
    file_menu.addAction(new_action)

    proof = QAction("&Proof")
    proof.triggered.connect(lambda: window.table.toggle_column_visibility(1))
    file_menu.addAction(proof)
    #  __  __                  ___  _
    # |  \/  | ___  _ _  _  _ | __|(_) _ _
    # | |\/| |/ -_)| ' \| || || _| | || ' \
    # |_|  |_|\___||_||_|\_,_||_|  |_||_||_|

    sys.exit(app.exec_())
