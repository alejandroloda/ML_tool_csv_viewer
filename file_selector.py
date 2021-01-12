import pandas as pd

from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QHBoxLayout, QLineEdit, QMessageBox


class FileSelector(QWidget):
    def __init__(self, main):
        super().__init__()
        self.filename = ""
        self.main = main
        self.text_file_explorer = None
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        self.text_file_explorer = QLineEdit(self)
        self.text_file_explorer.setReadOnly(True)
        hbox.addWidget(self.text_file_explorer)

        button_file_explorer = QPushButton('Choose file', self)
        button_file_explorer.clicked.connect(self.open_file_name_dialog)
        hbox.addWidget(button_file_explorer)

        button_refresh = QPushButton('Apply', self)
        button_refresh.clicked.connect(self.refresh_table)
        hbox.addWidget(button_refresh)

        self.setLayout(hbox)

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Choose CSV", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            self.filename = filename
            self.text_file_explorer.setText(self.filename)
            print(filename)

    def refresh_table(self):
        if self.filename:
            df = pd.read_csv(self.filename, sep=';')
            self.main.refresh_table(df)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Wrong file")
            msg.setText("File cannot be empty or invalid")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
