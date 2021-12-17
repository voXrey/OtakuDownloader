import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *


class LabelPerso(QLabel):
    def __init__(self, parent, name):
        QLabel.__init__(self, parent=parent)
        self.setObjectName(name)
    
    def getParentSize(self):
        size = self.parent().size()
        return (size.width(), size.height())

    def getMargin(self):
        size = self.parent().size()
        return (size.width()/30, size.height()/20)

class ButtonPerso(QPushButton):
    def __init__(self, text, parent, name):
        QPushButton.__init__(self, text=text, parent=parent)
        self.setObjectName(name)
    
    def getParentSize(self):
        size = self.parent().size()
        return (size.width(), size.height())

    def getMargin(self):
        size = self.parent().size()
        return (size.width()/30, size.height()/20)


class InfoLabel(LabelPerso):
    def __init__(self, parent, name):
        LabelPerso.__init__(self, parent=parent, name=name)
        self.setObjectName(name)
        self.texts = []
        self.setMargin(5)
    
    def print(self, text:str):
        self.texts.append(text)
        if len(self.texts) > 30 : self.texts = self.texts[-30:]
        self.setText('\n'.join(self.texts))

class TopRightLabel(InfoLabel):
    def __init__(self, parent, name):
        InfoLabel.__init__(self, parent=parent, name=name)
        self.setAlignment(Qt.AlignBottom)

    def resize(self):
        WIDTH, HEIGHT = self.getParentSize()
        margin_width, margin_height = self.getMargin()

        x = ((WIDTH/2)+margin_width/2)
        y = margin_height
        width = ((WIDTH/2)-margin_width*1.5)
        height = (HEIGHT*(2/3)-margin_height/2)

        self.setGeometry(x, y, width, height)

class BottomRightLabel(InfoLabel):
    def __init__(self, parent, name):
        InfoLabel.__init__(self, parent=parent, name=name)
        self.setAlignment(Qt.AlignTop)

    def resize(self):
        WIDTH, HEIGHT = self.getParentSize()
        margin_width, margin_height = self.getMargin()

        top_right_label = self.parent().findChild(TopRightLabel, 'top_right_label')
        top_right_label_size = top_right_label.size()

        x = top_right_label.x()
        y = (top_right_label_size.height())+margin_height*2
        width = top_right_label_size.width()
        height = (HEIGHT-(top_right_label_size.height())-margin_height*3)

        self.setGeometry(x, y, width, height)


class SelectFolderButton(ButtonPerso):
    def __init__(self, text, parent, name):
        ButtonPerso.__init__(self, text=text, parent=parent, name=name)
        self.setObjectName(name)

    def resize(self):
        WIDTH, HEIGHT = self.getParentSize()
        margin_width, margin_height = self.getMargin()
        
        x = margin_width
        y = margin_height
        width = ((WIDTH/2)-margin_width*1.5)
        height = HEIGHT/20

        self.setGeometry(x, y, width, height)

class FolderLabel(LabelPerso):
    def __init__(self, parent, name):
        LabelPerso.__init__(self, parent=parent, name=name)
        self.setAlignment(Qt.AlignLeft)
        self.setAlignment(Qt.AlignVCenter)
    
    def resize(self):
        select_folder_button = self.parent().findChild(SelectFolderButton, 'select_folder_button')
        
        x = select_folder_button.x()
        y = select_folder_button.y() + select_folder_button.size().height()
        width = select_folder_button.size().width()
        height = select_folder_button.size().height()

        self.setGeometry(x, y, width, height)
    
    def updateText(self, folder):
        if folder is None: folder_text = "No folder selected"
        else: folder_text = f"Folder selected : '{folder}'"
        self.setText(folder_text)

class ScansCombobox(QComboBox):
    def __init__(self, parent, name):
        QComboBox.__init__(self, parent=parent)
        self.setObjectName(name)
        
        line_edit = QLineEdit(self)
        line_edit.setObjectName('scan_link_line_edit')

        self.setLineEdit(line_edit)
    
    def resize(self):
        folder_label = self.parent().findChild(FolderLabel, 'folder_label')
        
        x = folder_label.x()
        y = folder_label.y() + (folder_label.size().height()*2)
        width = folder_label.size().width()
        height = folder_label.size().height()

        self.setGeometry(x, y, width, height)
    
    def update_items(self, scans_names):
        self.clear()
        self.addItems(scans_names)


class DownloadButton(ButtonPerso):
    def __init__(self, text, parent, name):
        ButtonPerso.__init__(self, text=text, parent=parent, name=name)
        self.setObjectName(name)

    def resize(self):
        scans_combobox = self.parent().findChild(ScansCombobox, 'scans_combobox')

        margin_width, margin_height = self.getMargin()
        
        x = scans_combobox.x()
        y = scans_combobox.y() + scans_combobox.size().height() + (margin_height/4)
        width = scans_combobox.size().width()*(4/5) - (margin_width/4)
        height = scans_combobox.size().height()

        self.setGeometry(x, y, width, height)

class ValidationButton(ButtonPerso):
    def __init__(self, text, parent, name):
        ButtonPerso.__init__(self, text=text, parent=parent, name=name)
        self.setObjectName(name)

    def resize(self):
        download_button = self.parent().findChild(DownloadButton, 'download_button')
        select_folder_button = self.parent().findChild(SelectFolderButton, 'select_folder_button')

        margin_width, margin_height = self.getMargin()
        
        x = download_button.x() + download_button.size().width() + (margin_width/4)
        y = download_button.y()
        width = select_folder_button.size().width()*(1/5)
        height = select_folder_button.size().height()

        self.setGeometry(x, y, width, height)

class PauseButton(ButtonPerso):
    def __init__(self, text, parent, name):
        ButtonPerso.__init__(self, text=text, parent=parent, name=name)
        self.setObjectName(name)

    def resize(self):
        validation_button = self.parent().findChild(ValidationButton, 'validation_button')

        margin_width, margin_height = self.getMargin()
        
        x = validation_button.x()
        y = validation_button.y() + validation_button.size().height() + (margin_height/5)
        width = validation_button.size().width()
        height = validation_button.size().height()

        self.setGeometry(x, y, width, height)


class StopButton(ButtonPerso):
    def __init__(self, text, parent, name):
        ButtonPerso.__init__(self, text=text, parent=parent, name=name)
        self.setObjectName(name)

    def resize(self):
        pause_button = self.parent().findChild(PauseButton, 'pause_button')

        margin_width, margin_height = self.getMargin()
        
        x = pause_button.x()
        y = pause_button.y() + pause_button.size().height() + (margin_height/5)
        width = pause_button.size().width()
        height = pause_button.size().height()

        self.setGeometry(x, y, width, height)


class ChaptersCheckBoxSlectAll(QCheckBox):
    def __init__(self, name, parent=None):
        super(QCheckBox, self).__init__(parent)
        self.setObjectName(name)
        self.stateChanged.connect(self.on_stateChanged)
        self.setText('Select All chapters')

    def on_stateChanged(self, state):
        chapters_view = self.parent().findChild(ChaptersView, 'chapters_view')
        if int(state) == 2:
            chapters_view.checkAll()
        elif int(state) == 0:
            chapters_view.uncheckAll()

    def resize(self):
        download_button = self.parent().findChild(DownloadButton, 'download_button')
        x = download_button.x()
        y = download_button.y() + download_button.size().height()
        width = (download_button.size().width())/2
        height = download_button.size().height()

        self.setGeometry(x, y, width, height)

class ChaptersCheckBoxes(QStandardItemModel):
    def __init__(self, parent=None):
        super(QStandardItemModel, self).__init__(parent=parent)
        self.items = []
        
    def setItems(self, chapters_numbers):
        self.clear()
        self.items = []
        for chapter_number in chapters_numbers:                   
            item = QStandardItem(f'{chapter_number}')
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            check = Qt.Unchecked
            item.setData(QVariant(check), Qt.CheckStateRole)
            self.items.append(item)

        for item in self.items:
            self.appendRow(item)
    
    def checkAll(self):
        check = Qt.Checked
        for item in self.items:
            item.setData(QVariant(check), Qt.CheckStateRole)

    def uncheckAll(self):
        check = Qt.Unchecked
        for item in self.items:
            item.setData(QVariant(check), Qt.CheckStateRole)

class ChaptersView(QListView):
    def __init__(self, model, name, parent=None):
        super(QListView, self).__init__(parent=parent)
        self.setObjectName(name)
        self.model = model
        self.setModel(self.model)
    
    def resize(self):
        check_all_checkbox = self.parent().findChild(ChaptersCheckBoxSlectAll, 'check_all_checkbox')
        x = check_all_checkbox.x()
        y = check_all_checkbox.y() + check_all_checkbox.size().height()
        width = check_all_checkbox.size().width()
        height = (self.parent().size().height() - y)/2

        self.setGeometry(x, y, width, height)

    def checkAll(self):
        self.model.checkAll()

    def uncheckAll(self):
        self.model.uncheckAll()

    def getItemsCheckedText(self):
        items = self.model.items
        return [item.text() for item in items if item.checkState() == Qt.Checked]



if __name__ == '__main__' :
    # for tests
    class MainWindow(QMainWindow):
        def resizeEvent(self, event):
            self.findChild(SelectFolderButton, 'select_folder_button').resize()
            self.findChild(FolderLabel, 'folder_label').resize()
            self.findChild(ScansCombobox, 'scans_combobox').resize()
            self.findChild(DownloadButton, 'download_button').resize()
            self.findChild(ValidationButton, 'validation_button').resize()
            self.findChild(PauseButton, 'pause_button').resize()
            self.findChild(StopButton, 'stop_button').resize()
            self.findChild(TopRightLabel, 'top_right_label').resize()
            self.findChild(BottomRightLabel, 'bottom_right_label').resize()
            
    app = QApplication()

    win = MainWindow()
    win.setMinimumSize(QSize(1200, 800))

    w3 = SelectFolderButton('sel', win, 'select_folder_button')
    w3.resize()
    w6 = FolderLabel(parent=win, name='folder_label')
    w6.resize()
    w7 = ScansCombobox(parent=win, name='scans_combobox')
    w7.resize()
    w1 = DownloadButton('dl', win, 'download_button')
    w1.resize()
    w2 = ValidationButton('val', win, 'validation_button')
    w2.resize()
    w8 = PauseButton('pause', win, 'pause_button')
    w8.resize()
    w9 = StopButton('Stop', win, 'stop_button')
    w9.resize()
    w4 = TopRightLabel(win, name='top_right_label')
    w4.resize()
    w5 = BottomRightLabel(win, name='bottom_right_label')
    w5.resize()

    win.show()
    sys.exit(app.exec_())
