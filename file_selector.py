from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QHBoxLayout, QLineEdit
import pandas as pd


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
        self.button_refresh.clicked.connect(self.refresh_file)
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
            self.filename = filename
            self.text_file_explorer.setText(self.filename)
            print(filename)

    def refresh_file(self):
        df = pd.read_csv(self.filename, sep=';')
        self.main.refresh_model(df)
