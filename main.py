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
# - Mostrar solo columnas encendidas/apagadas
# - Descargar csv modificado
# - Encontrar máximos y minimos en columnas
# - Aplicar modelos básicos


import sys
import pandas as pd

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QAction
from PyQt5.QtCore import Qt

from file_selector import FileSelector
from awesome_table import AwesomeTable


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
        # self.dockWidget_file_explorer.setWindowTitle("File explorer dock")
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

    show_all_columns = QAction("&Show all columns")
    show_all_columns.triggered.connect(window.table.show_all_columns)
    file_menu.addAction(show_all_columns)

    inverse_columns_view = QAction("&Inverse columns view")
    inverse_columns_view.triggered.connect(window.table.inverse_view)
    file_menu.addAction(inverse_columns_view)

    # ---- Prueba ----
    proof = QAction("&Proof")
    proof.triggered.connect(lambda: window.table.download_csv_of_on_columns())
    file_menu.addAction(proof)
    #  __  __                  ___  _
    # |  \/  | ___  _ _  _  _ | __|(_) _ _
    # | |\/| |/ -_)| ' \| || || _| | || ' \
    # |_|  |_|\___||_||_|\_,_||_|  |_||_||_|

    sys.exit(app.exec_())
