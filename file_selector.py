from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QHBoxLayout, QLineEdit, QMessageBox, QLabel
from PyQt5.QtCore import Qt


class WarningBox(QMessageBox):
    def __init__(self, title, text):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QMessageBox.Warning)
        self.exec_()


class FileSelector(QWidget):
    def __init__(self, main):
        super().__init__()
        self.filename = ""
        self.main = main
        self.text_file_explorer = None
        self.text_separator = None
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()

        self.text_file_explorer = QLineEdit(self)
        self.text_file_explorer.setReadOnly(True)
        hbox.addWidget(self.text_file_explorer)

        button_file_explorer = QPushButton('Choose file', self)
        button_file_explorer.clicked.connect(self.open_file_name_dialog)
        hbox.addWidget(button_file_explorer)

        hbox.addWidget(QLabel("Sep:"))

        self.text_separator = QLineEdit(self)
        self.text_separator.setText(';')
        self.text_separator.setAlignment(Qt.AlignCenter)
        self.text_separator.setFixedWidth(30)
        hbox.addWidget(self.text_separator)

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
            if self.text_separator.text():
                self.main.refresh_table(self.filename, self.text_separator.text())
            else:
                WarningBox("Wrong separator", "Separator cannot be empty or invalid")
        else:
            WarningBox("Wrong file", "File cannot be empty or invalid")
