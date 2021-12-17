from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from classes.widgets import *
from ext.utils import open_json


class GUI(QMainWindow):
    def __init__(self, programe):
        super().__init__()
        self.programe = programe

        ### Set window ###
        self.setWindowTitle("OtakuDownloader") # set window title
        self.setMinimumSize(QSize(1200, 800)) # set window minimum size
        self.setWindowIcon(QIcon('assets/icon.jpg')) # set window icon
        self.heightForWidth(2)

        self.setWidgets()

    def setWidgets(self):
        """
        Create app widgets
        """
        self.select_folder_button = SelectFolderButton(text='Select scans folder', parent=self, name='select_folder_button')
        self.select_folder_button.clicked.connect(self.select_scans_folder)

        self.folder_label = FolderLabel(parent=self, name='folder_label')
        self.update_selected_folder_label()

        self.scans_combobox = ScansCombobox(parent=self, name='scans_combobox')
        self.update_scans_names_list()

        self.download_button = DownloadButton(text='Download scan', parent=self, name='download_button')
        self.download_button.clicked.connect(self.download_button_clicked)

        self.validation_button = ValidationButton(text='Entry', parent=self, name='validation_button')
        self.validation_button.clicked.connect(self.validate_scan_name)

        self.check_all_checkbox = ChaptersCheckBoxSlectAll(name='check_all_checkbox', parent=self)
        model = ChaptersCheckBoxes()
        self.chapters_list = ChaptersView(model=model, parent=self, name='chapters_view')

        self.pause_button = PauseButton(text='Pause', parent=self, name='pause_button')
        self.pause_button.clicked.connect(self.update_hide_pause_button)

        self.no_pause_button = PauseButton(text='No Pause', parent=self, name='no_pause_button')
        self.no_pause_button.clicked.connect(self.update_hide_pause_button)

        self.stop_button = StopButton(text='Stop', parent=self, name='stop_button')
        self.stop_button.clicked.connect(self.stop_button_clicked)

        self.top_right_label = TopRightLabel(parent=self, name='top_right_label')
        self.bottom_right_label = BottomRightLabel(parent=self, name='bottom_right_label')

        self.update_all_buttons()
        self.no_pause_button.setHidden(True)
        self.update_stop_button()

    def update_hide_pause_button(self):
        if self.programe.download_scan_in_combobox_thread.pause:
            self.programe.download_scan_in_combobox_thread.setPause(False)
            self.no_pause_button.setHidden(True)
            self.pause_button.setHidden(False)
        else:
            self.programe.download_scan_in_combobox_thread.setPause(True)
            self.pause_button.setHidden(True)
            self.no_pause_button.setHidden(False)

    def update_hide_stop_button(self):
        self.stop_button.setEnabled(False)
        if self.programe.download_scan_in_combobox_thread.alive:
            self.setEnabled(True)

    def stop_button_clicked(self):
        if self.programe.download_scan_in_combobox_thread.pause: self.update_hide_pause_button()
        self.programe.download_scan_in_combobox_thread.stop()
        self.update_hide_stop_button()
        self.update_all_buttons()

    def resizeEvent(self, event):
        self.select_folder_button.resize()
        self.folder_label.resize()
        self.scans_combobox.resize()
        self.download_button.resize()

        self.check_all_checkbox.resize()
        self.chapters_list.resize()

        self.validation_button.resize()
        self.pause_button.resize()
        self.no_pause_button.resize()
        self.stop_button.resize()
        
        self.top_right_label.resize()
        self.bottom_right_label.resize()

    def select_scans_folder(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path == "": folder_path = self.programe.config["data"]["scans-folder"]
        self.programe.config["data"]["scans-folder"] = folder_path
        self.programe.update_config()
        self.update_selected_folder_label()
    
    def update_selected_folder_label(self):
        folder = self.programe.config["data"]['scans-folder']
        self.folder_label.updateText(folder)
    
    def update_scans_names_list(self):
        scans_names = self.programe.downloader.get_scans_names()
        self.scans_combobox.update_items(scans_names)
        self.scans_combobox.setEditText(self.programe.config['data']['current-scan-name'])
    
    def validate_scan_name(self):
        self.download_button.setEnabled(False)

        current_text = self.scans_combobox.currentText()
        scans_names = self.programe.downloader.get_scans_names()
        if current_text in scans_names:
            scan_link = self.programe.downloader.get_scan_link(name=current_text)
            scan_chapters = self.programe.downloader.scan_chapters(scan_link)
            scan_chapters_numbers = [chapter_link.split("/")[-1] for chapter_link in scan_chapters]

            self.programe.config['data']['current-scan-link'] = scan_link
            self.programe.config['data']['current-scan-name'] = current_text
            self.programe.config['data']['current-scan-chapters'] = scan_chapters
            self.programe.update_config()

            chapters_view = self.chapters_list
            chapters_view.model.setItems(chapters_numbers=scan_chapters_numbers)

        else:
            self.scans_combobox.setEditText('Provid valid name please')
            self.programe.config['data']['current-scan-link'] = None
            self.programe.config['data']['current-scan-name'] = None
            self.programe.update_config()

        self.update_download_button()

    def update_download_button(self):
        self.download_button.setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            if self.programe.config['data']['current-scan-link'] is not None:
                self.download_button.setEnabled(True)
                return
    
    def update_validation_button(self):
        self.validation_button.setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            self.validation_button.setEnabled(True)
            return

    def update_select_folder_button(self):
        self.select_folder_button.setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            self.select_folder_button.setEnabled(True)
            return

    def update_pause_button(self):
        self.pause_button.setEnabled(False)
        if self.programe.download_scan_in_combobox_thread.alive:
            self.pause_button.setEnabled(True)
            return
    
    def update_stop_button(self):
        self.stop_button.setEnabled(False)
        if self.programe.download_scan_in_combobox_thread.alive:
            self.stop_button.setEnabled(True)
            return

    def update_all_buttons(self):
        self.update_download_button()
        self.update_validation_button()
        self.update_select_folder_button()
        self.update_pause_button()
        self.update_stop_button()

    def update_scan_combobox(self):
        self.scans_combobox.lineEdit().setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            self.scans_combobox.lineEdit().setEnabled(True)
            return

    def download_button_clicked(self):
        self.download_button.setEnabled(False)
        self.validation_button.setEnabled(False)
        self.select_folder_button.setEnabled(False)
        self.scans_combobox.lineEdit().setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)

        self.update_chapters()
        self.programe.download_scan_in_combobox_thread.start()

        self.programe.download_scan_in_combobox_thread.finished.connect(self.update_all_buttons)
        self.programe.download_scan_in_combobox_thread.finished.connect(self.update_scan_combobox)
        
    def update_chapters(self):
        items_text = self.chapters_list.getItemsCheckedText()
        main_url = self.programe.config['data']['current-scan-link']
        chapter_links = []
        for item_text in items_text:
            chapter_link = self.programe.downloader.scan_chapter_link_with_number(main_url=main_url, number=item_text)
            chapter_links.append(chapter_link)
        
        self.programe.config['data']['current-scan-chapters'] = chapter_links
        self.programe.update_config()