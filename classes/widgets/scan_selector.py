from classes.signal_worker import Worker
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QWidget)


class Label(QLabel):
    def __init__(self, text:str, name:str, parent=None):
        QLabel.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setText(text)
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignVCenter)

class Combobox(QComboBox):
    def __init__(self, name:str, parent=None):
        QComboBox.__init__(self, parent=parent)
        self.setObjectName(name)
        line_edit = QLineEdit(self)
        self.setLineEdit(line_edit)
    
    def set_items(self, new_items):
        self.clear()
        self.addItems(new_items)

class Button(QPushButton):
    def __init__(self, text:str,  name, parent=None):
        QPushButton.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setText(text)

class ScanSelector(QWidget):
    signal = pyqtSignal(str)
    def __init__(self, name:str, programe, parent=None):
        QWidget.__init__(self, parent=parent)
        self.programe = programe
        self.setObjectName(name)

        self.label = Label(text='Choose the scan to download:', name='scan_selector_label')
        self.combobox = Combobox(name='scan_selector_combobox')
        self.button = Button(text='entry', name='button')
        self.button.clicked.connect(self.button_clicked)

        self.layout_child = QHBoxLayout()
        self.layout_child.addWidget(self.combobox, stretch=5)
        self.layout_child.addWidget(self.button, stretch=1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.layout_child)

        self.setLayout(self.layout)

    def button_clicked(self):
        otherClass = Worker(programe=self.programe)
        self.signal.connect(otherClass.onJob)
        self.signal.emit('validation_button_clicked')
