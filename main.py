#  __  __         _         _____
# |  \/  |       (_)       |  __ \
# | \  / |  __ _  _  _ __  | |__) |_ __  ___    __ _  _ __  __ _  _ __ ___
# | |\/| | / _` || || '_ \ |  ___/| '__|/ _ \  / _` || '__|/ _` || '_ ` _ \
# | |  | || (_| || || | | || |    | |  | (_) || (_| || |  | (_| || | | | | |
# |_|  |_| \__,_||_||_| |_||_|    |_|   \___/  \__, ||_|   \__,_||_| |_| |_|
#                                               __/ |
#                                              |___/

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow, QPushButton, QTextEdit, QHBoxLayout, \
    QLineEdit


class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 100  # Donde empieza desde la izq
        self.top = 100  # Donde empieza desde arriba
        self.width = 640  # Cuanto mide horizontal
        self.height = 480  # Cuanto mide vertical

        self.file = ""

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        hbox = QHBoxLayout()
        self.text_file_explorer = QLineEdit(self)
        self.text_file_explorer.setReadOnly(True)
        hbox.addWidget(self.text_file_explorer)
        self.button_file_explorer = QPushButton('Elegir archivo', self)
        self.button_file_explorer.clicked.connect(self.openFileNameDialog)
        hbox.addWidget(self.button_file_explorer)

        self.setLayout(hbox)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
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

        self.file_explorer = FileSelector()
        self.setCentralWidget(self.file_explorer)

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
