from classes.signal_worker import Worker
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QStackedWidget,
                             QVBoxLayout, QWidget)


class PauseButton(QPushButton):
    def __init__(self, text:str,  name, parent=None):
        QPushButton.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setText(text)

class UnPauseButton(QPushButton):
    def __init__(self, text:str,  name, parent=None):
        QPushButton.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setText(text)

class StopButton(QPushButton):
    def __init__(self, text:str,  name, parent=None):
        QPushButton.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setText(text)

class DownloadButton(QPushButton):
    def __init__(self, text:str,  name, parent=None):
        QPushButton.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setText(text)

class DownloaderButtons(QWidget):
    signal = pyqtSignal(str)
    def __init__(self, name:str, programe, parent=None):
        QWidget.__init__(self, parent=parent)
        self.programe = programe
        self.setObjectName(name)

        self.pause_button = PauseButton(text='Pause', name='pause_button')
        self.pause_button.clicked.connect(self.pause_button_clicked)
        self.unpause_button = UnPauseButton(text='Stop pause', name='unpause_button')
        self.unpause_button.clicked.connect(self.unpause_button_clicked)
        self.unpause_button.setHidden(True)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.pause_button)
        self.stacked_widget.addWidget(self.unpause_button)

        self.stop_button = StopButton(text='Stop', name='stop_button')
        self.stop_button.clicked.connect(self.stop_button_clicked)
        self.download_button = DownloadButton(text='Download scan', name='download_button')
        self.download_button.clicked.connect(self.download_button_clicked)

        self.layout_child = QHBoxLayout()
        self.layout_child.addWidget(self.stop_button, stretch=1, alignment=Qt.AlignBottom)
        self.layout_child.addWidget(self.stacked_widget, stretch=1, alignment=Qt.AlignBottom)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout_child)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(QWidget(), stretch=1)

        self.setLayout(self.layout)

    def stop_button_clicked(self):
        otherClass = Worker(programe=self.programe)
        self.signal.connect(otherClass.onJob)
        self.signal.emit('stop_button_clicked')
    
    def pause_button_clicked(self):
        otherClass = Worker(programe=self.programe)
        self.signal.connect(otherClass.onJob)
        self.signal.emit('pause_button_clicked')

    def unpause_button_clicked(self):
        otherClass = Worker(programe=self.programe)
        self.signal.connect(otherClass.onJob)
        self.signal.emit('unpause_button_clicked')

    def download_button_clicked(self):
        otherClass = Worker(programe=self.programe)
        self.signal.connect(otherClass.onJob)
        self.signal.emit('download_button_clicked')
