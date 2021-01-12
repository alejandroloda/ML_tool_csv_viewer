from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

button_width = 35


class ActionButton(QPushButton):
    def __init__(self, text, parent, tooltip, fun_connect):
        super().__init__(text, parent)
        self.setGeometry(0, 0, button_width, button_width)
        self.setToolTip(tooltip)
        self.is_clicked = False
        self.fun_connect = fun_connect
        self.clicked.connect(self.clicked_function)
        self.icons = None
        self.actual_icon = 0

    def clicked_function(self):
        """Intercepts function to take note if button is clicked or not"""
        self.is_clicked = not self.is_clicked
        self.fun_connect()
        self.next_icon()

    def next_icon(self):
        if self.icons is None:
            pass
        else:
            self.actual_icon = (self.actual_icon + 1) % len(self.icons)
            self.use_icon(self.actual_icon)

    def use_icon(self, n=0):
        icon = QtGui.QIcon(self.icons[n])
        self.setIcon(icon)

    def add_icons(self, list_of_filenames):
        self.icons = list_of_filenames
        self.use_icon()

    def add_icon(self, filepath):
        self.add_icons([filepath, ])


class Actions(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        vbox = QVBoxLayout()

        self.button_show_hide_columns = ActionButton('', self, "Show/Hide all columns", self.main.table.inverse_view)
        self.button_show_hide_columns.add_icons(['img/actions/visibility.svg', 'img/actions/visibility_not.svg'])
        vbox.addWidget(self.button_show_hide_columns)
