from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QLabel,
                             QLineEdit, QListView, QTabWidget, QVBoxLayout,
                             QWidget)


class SelectAllChaptersCheckBox(QCheckBox):
    def __init__(self, name:str, parent=None):
        super(QCheckBox, self).__init__(parent=parent)
        self.setObjectName(name)
        self.setText('Select All chapters')
        self.stateChanged.connect(self.on_state_changed)

    def on_state_changed(self, state):
        chapters_view = self.parent().findChild(ChaptersCheckBoxesView, 'chapters_checkboxes_view')
        if int(state) == 2:
            chapters_view.check_all()
        elif int(state) == 0:
            chapters_view.uncheck_all()

class ChaptersCheckBoxesModel(QStandardItemModel):
    def __init__(self, name, parent=None):
        super(QStandardItemModel, self).__init__(parent=parent)
        self.setObjectName(name)
        self.items = []
        
    def set_items(self, chapters_numbers):
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
    
    def check_all(self):
        check = Qt.Checked
        for item in self.items:
            item.setData(QVariant(check), Qt.CheckStateRole)

    def uncheck_all(self):
        check = Qt.Unchecked
        for item in self.items:
            item.setData(QVariant(check), Qt.CheckStateRole) 

class ChaptersCheckBoxesView(QListView):
    def __init__(self, model, name, parent=None):
        super(QListView, self).__init__(parent=parent)
        self.setObjectName(name)
        self.model = model
        self.setModel(self.model)

    def check_all(self):
        self.model.check_all()

    def uncheck_all(self):
        self.model.uncheck_all()

    def get_items_checked_text(self):
        items = self.model.items
        return [item.text() for item in items if item.checkState() == Qt.Checked]

class FuturChaptersCheckBox(QCheckBox):
    def __init__(self, name:str, parent=None):
        super(QCheckBox, self).__init__(parent=parent)
        self.setObjectName(name)
        self.setText('Download futur chapters automatically')


class CompressionCombobox(QComboBox):
    def __init__(self, name:str, parent=None):
        QComboBox.__init__(self, parent=parent)
        self.setObjectName(name)
        line_edit = QLineEdit(self)
        line_edit.setEnabled(False)
        self.setLineEdit(line_edit)
        self.set_items(['None', 'Faster', 'Normal', 'Super', 'Maximum', 'Ultra'])
    
    def set_items(self, new_items):
        self.clear()
        self.addItems(new_items)
    
    def get_text(self):
        return self.lineEdit().text()

class SizeCombobox(QComboBox):
    def __init__(self, name:str, parent=None):
        QComboBox.__init__(self, parent=parent)
        self.setObjectName(name)
        line_edit = QLineEdit(self)
        line_edit.setEnabled(False)
        self.setLineEdit(line_edit)
        self.set_items(['Original'])
    
    def set_items(self, new_items):
        self.clear()
        self.addItems(new_items)
    
    def get_text(self):
        return self.lineEdit().text()

class ColorsCombobox(QComboBox):
    def __init__(self, name:str, parent=None):
        QComboBox.__init__(self, parent=parent)
        self.setObjectName(name)
        line_edit = QLineEdit(self)
        line_edit.setEnabled(False)
        self.setLineEdit(line_edit)
        self.set_items(['Originals', 'Black & White'])
    
    def set_items(self, new_items):
        self.clear()
        self.addItems(new_items)
    
    def get_text(self):
        return self.lineEdit().text()

class OptionsTab(QWidget):
    def __init__(self, name:str, parent=None):
        super(QWidget, self).__init__(parent=parent)
        self.setObjectName(name)

        self.tabs = QTabWidget()
        self.tabs.setObjectName('tab_widget')
        self.options_tab = QWidget()
        self.options_tab.setObjectName('options')


        option_tab_layout_child1 = QVBoxLayout()

        self.select_all_chapters_checkbox = SelectAllChaptersCheckBox(name='select_all_chapters_checkbox')
        model = ChaptersCheckBoxesModel(name='chapters_checkboxes_model')
        self.chapters_checkboxes_view = ChaptersCheckBoxesView(model=model, name='chapters_checkboxes_view')
        self.futur_chapters_checkbox = FuturChaptersCheckBox(name='futur_chapters_checkbox')
        option_tab_layout_child1.addWidget(self.select_all_chapters_checkbox, stretch=1)
        option_tab_layout_child1.addWidget(self.chapters_checkboxes_view, stretch=5)
        option_tab_layout_child1.addWidget(self.futur_chapters_checkbox, stretch=1)


        option_tab_layout_child2 = QVBoxLayout()

        option_tab_layout_child2_child1 = QHBoxLayout()
        compression_label = QLabel()
        compression_label.setObjectName('compression_label')
        compression_label.setText('Compression:')
        option_tab_layout_child2_child1.addWidget(compression_label, stretch=1)
        self.compression_combobox = CompressionCombobox(name='compression_combobox')
        option_tab_layout_child2_child1.addWidget(self.compression_combobox, stretch=6)
        
        option_tab_layout_child2_child2 = QHBoxLayout()
        size_label=QLabel()
        size_label.setObjectName('size_label')
        size_label.setText('Size:')
        option_tab_layout_child2_child2.addWidget(size_label, stretch=1)
        self.size_combobox = SizeCombobox(name='size_combobox')
        option_tab_layout_child2_child2.addWidget(self.size_combobox, stretch=6)

        option_tab_layout_child2_child3 = QHBoxLayout()
        colors_label = QLabel()
        colors_label.setObjectName('colors_label')
        colors_label.setText('Colors:')
        option_tab_layout_child2_child3.addWidget(colors_label, stretch=1)
        self.colors_combobox = ColorsCombobox(name='colors_combobox')
        option_tab_layout_child2_child3.addWidget(self.colors_combobox, stretch=8)

        option_tab_layout_child2.addLayout(option_tab_layout_child2_child1)
        option_tab_layout_child2.addLayout(option_tab_layout_child2_child2)
        option_tab_layout_child2.addLayout(option_tab_layout_child2_child3)


        option_tab_layout = QHBoxLayout()
        option_tab_layout.addLayout(option_tab_layout_child1, stretch=2)
        option_tab_layout.addLayout(QVBoxLayout(), stretch=1)
        option_tab_layout.addLayout(option_tab_layout_child2, stretch=2)
        self.options_tab.setLayout(option_tab_layout)

        self.tabs.addTab(self.options_tab, 'Options')

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
