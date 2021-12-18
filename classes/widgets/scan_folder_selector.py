from classes.signal_worker import Worker
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class Button(QPushButton):
    def __init__(self, text:str, name:str, parent=None):
        QPushButton.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setText(text)

class Label(QLabel):
    def __init__(self, text:str, name:str, parent=None):
        QLabel.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignVCenter)

        self.update_text(text)
    
    def update_text(self, folder_path:str):
        if folder_path is None: folder_text = "No folder selected"
        else: folder_text = f"Folder selected : '{folder_path}'"
        self.setText(folder_text)

class ScanFolderSelector(QWidget):
    signal = pyqtSignal(str)
    def __init__(self, name:str, programe, parent=None):
        QWidget.__init__(self, parent=parent)
        self.programe = programe
        self.setObjectName(name)

        self.button = Button(text='Select folder', name='scan_folder_selector_button')
        self.button.clicked.connect(self.scan_selector_button_clicked)
        self.label = Label(text=None, name='scan_folder_selector_label')
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button, stretch=1)
        self.layout.addWidget(self.label, stretch=5)
        self.setLayout(self.layout)

    def scan_selector_button_clicked(self):
        otherClass = Worker(programe=self.programe)
        self.signal.connect(otherClass.onJob)
        self.signal.emit('select_scan_folder_button_clicked')
