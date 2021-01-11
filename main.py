#  __  __         _         _____
# |  \/  |       (_)       |  __ \
# | \  / |  __ _  _  _ __  | |__) |_ __  ___    __ _  _ __  __ _  _ __ ___
# | |\/| | / _` || || '_ \ |  ___/| '__|/ _ \  / _` || '__|/ _` || '_ ` _ \
# | |  | || (_| || || | | || |    | |  | (_) || (_| || |  | (_| || | | | | |
# |_|  |_| \__,_||_||_| |_||_|    |_|   \___/  \__, ||_|   \__,_||_| |_| |_|
#                                               __/ |
#                                              |___/

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow, QPushButton, QHBoxLayout, \
    QLineEdit, QDockWidget, QTableView

from PyQt5.QtCore import Qt


class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.file = ""
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


class MyMainWindow(QMainWindow):
    def __init__(self, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.geometry = (300, 300, 1000, 500)
        self.setGeometry(*self.geometry)

        self.dockWidget_file_explorer = QDockWidget('Files List', self)
        self.dockWidget_file_explorer.setFloating(False)
        # # Crear tree y asignar
        self.file_explorer = FileSelector()
        self.dockWidget_file_explorer.setWidget(self.file_explorer)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget_file_explorer)

        main_widget = FileSelector()
        self.setCentralWidget(main_widget)


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
