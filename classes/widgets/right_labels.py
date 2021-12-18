from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class TopLabel(QLabel):
    def __init__(self, name:str, parent=None):
        QLabel.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignBottom)

        self.texts = []
        self.texts_limit = 30
        self.update_text()
    
    def update_text(self):
        if len(self.texts) > self.texts_limit:
            self.texts = self.texts[-self.texts_limit:]
        self.setText('\n'.join(self.texts))

    def print(self, text:str):
        self.texts.append(text)
        self.update_text()

class BottomLabel(QLabel):
    def __init__(self, name:str, parent=None):
        QLabel.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignTop)

        self.texts = []
        self.texts_limit = 10
        self.update_text()
    
    def update_text(self):
        if len(self.texts) > self.texts_limit:
            self.texts = self.texts[-self.texts_limit:]
        self.setText('\n'.join(self.texts))

    def print(self, text:str):
        self.texts.append(text)
        self.update_text()

class RightLabels(QWidget):
    def __init__(self, name:str, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setObjectName(name)

        self.top_label = TopLabel(name='top_label')
        self.bottom_label = BottomLabel(name='bottom_label')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.top_label, stretch=5)
        self.layout.addWidget(self.bottom_label, stretch=2)
        self.setLayout(self.layout)
