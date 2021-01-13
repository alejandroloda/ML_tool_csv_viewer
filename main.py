#  __  __         _         _____
# |  \/  |       (_)       |  __ \
# | \  / |  __ _  _  _ __  | |__) |_ __  ___    __ _  _ __  __ _  _ __ ___
# | |\/| | / _` || || '_ \ |  ___/| '__|/ _ \  / _` || '__|/ _` || '_ ` _ \
# | |  | || (_| || || | | || |    | |  | (_) || (_| || |  | (_| || | | | | |
# |_|  |_| \__,_||_||_| |_||_|    |_|   \___/  \__, ||_|   \__,_||_| |_| |_|
#                                               __/ |
#                                              |___/

# TODO:
# - Descargar csv modificado
# - Encontrar máximos y minimos en columnas
# - Aplicar modelos básicos
# - Al cargar una tabla nueva, lanzar señal para resetear lo pertinente
# - Porcentaje de carga de tabla


import sys
import pandas as pd
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QAction
from PyQt5.QtCore import Qt

from file_selector import FileSelector
from awesome_table import AwesomeTable
from actions import button_width, Actions


class MyMainWindow(QMainWindow):
    def __init__(self, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.geometry = (300, 300, 1000, 500)
        self.setGeometry(*self.geometry)
        margin = 1
        self.setContentsMargins(margin, 0, margin, margin)
        self.icon_init()

        # File explorer
        self.dockWidget_file_explorer = QDockWidget(self)
        self.dockWidget_file_explorer.setFloating(False)
        self.file_explorer = FileSelector(self)
        self.dockWidget_file_explorer.setWidget(self.file_explorer)
        # self.dockWidget_file_explorer.setWindowTitle("File explorer dock")
        self.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget_file_explorer)

        # Reader (part 1)
        self.table = AwesomeTable(self)
        self.setCentralWidget(self.table)

        # Dock Left Actions
        self.actions = Actions(self)
        self.dockWidget_actions = QDockWidget(self)
        self.dockWidget_actions.setFloating(False)
        self.dockWidget_actions.setWidget(self.actions)
        # self.dockWidget_actions.setMaximumWidth(button_width)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_actions)

        # Reader (part 2)
        df = pd.DataFrame([['valid', 'csv']], columns=['Waiting', 'for'])
        self.refresh_table(df)

    def icon_init(self):
        self.setWindowIcon(QtGui.QIcon("img/icon.png"))
        import ctypes
        myappid = 'alejandroloda.machineLearningCsvTool.v00-01'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def refresh_table(self, filename, sep=';'):
        self.table.refresh_table(filename, sep)
        self.actions.button_tail_head_all.reset_icon_pos()

    def reset_dock_view(self):
        """Turn on visibility of all docks"""
        self.dockWidget_file_explorer.setVisible(True)
        self.dockWidget_actions.setVisible(True)


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

    # inverse_columns_view = QAction("&Inverse columns view")
    # inverse_columns_view.triggered.connect(window.table.inverse_view)
    # file_menu.addAction(inverse_columns_view)

    download_csv_without_hidden_columns = QAction("&Download CSV without hidden columns")
    download_csv_without_hidden_columns.triggered.connect(lambda: window.table.download_csv_of_on_columns())
    file_menu.addAction(download_csv_without_hidden_columns)

    # ---- Prueba ----
    proof = QAction("&Proof")
    proof.triggered.connect(lambda: window.table.download_csv_of_on_columns())
    file_menu.addAction(proof)
    #  __  __                  ___  _
    # |  \/  | ___  _ _  _  _ | __|(_) _ _
    # | |\/| |/ -_)| ' \| || || _| | || ' \
    # |_|  |_|\___||_||_|\_,_||_|  |_||_||_|

    sys.exit(app.exec_())
