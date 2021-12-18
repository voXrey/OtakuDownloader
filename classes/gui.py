from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from classes.widgets.downloader_buttons import DownloaderButtons
from classes.widgets.options_tab import OptionsTab
from classes.widgets.right_labels import RightLabels
from classes.widgets.scan_folder_selector import ScanFolderSelector
from classes.widgets.scan_selector import ScanSelector


class GUI(QMainWindow):
    def __init__(self, programe):
        super().__init__()
        self.programe = programe

        ### Set window ###
        self.setWindowTitle("OtakuDownloader") # set window title
        self.setWindowIcon(QIcon('assets/icon.jpg')) # set window icon
        self.heightForWidth(2)

        self.setWidgets()

    def setWidgets(self):
        """
        Create app widgets
        """
        self.scans_folder_selector = ScanFolderSelector(name='folder_selector', programe=self.programe)
        self.scan_selector = ScanSelector(name='scan_selector', programe=self.programe)
        self.scan_selector.combobox.set_items(self.programe.downloader.get_scans_names())
        self.options_tab = OptionsTab(name='options_tab')
        self.downloader_buttons = DownloaderButtons(name='downloader_buttons', programe=self.programe)
        self.right_labels = RightLabels(name='right_labels')

        self.central_widget = QWidget()
        HLayout = QVBoxLayout()
        HLayout.addWidget(self.scans_folder_selector)
        HLayout.addWidget(self.scan_selector)
        HLayout.addWidget(self.options_tab)
        HLayout.addWidget(self.downloader_buttons)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(HLayout, stretch=1)
        main_layout.addWidget(self.right_labels, stretch=1)

        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

        self.update_selected_folder_label()
        self.update_all_buttons()

    def update_hide_pause_button(self):
        if self.programe.download_scan_in_combobox_thread.pause:
            self.programe.download_scan_in_combobox_thread.setPause(False)
            self.downloader_buttons.unpause_button.setHidden(True)
            self.downloader_buttons.pause_button.setHidden(False)
        else:
            self.programe.download_scan_in_combobox_thread.setPause(True)
            self.downloader_buttons.pause_button.setHidden(True)
            self.downloader_buttons.unpause_button.setHidden(False)

    def update_stop_button(self):
        self.downloader_buttons.stop_button.setEnabled(False)
        if self.programe.download_scan_in_combobox_thread.alive:
            self.downloader_buttons.stop_button.setEnabled(True)

    def stop_button_clicked(self):
        if self.programe.download_scan_in_combobox_thread.pause: self.update_hide_pause_button()
        self.programe.download_scan_in_combobox_thread.stop()
        self.update_stop_button()
        self.update_all_buttons()

    def select_scans_folder(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path == "": folder_path = self.programe.config["data"]["scans-folder"]
        self.programe.config["data"]["scans-folder"] = folder_path
        self.programe.update_config()
        self.update_selected_folder_label()
    
    def update_selected_folder_label(self):
        folder = self.programe.config["data"]['scans-folder']
        self.scans_folder_selector.label.update_text(folder)
    
    def update_scans_names_list(self):
        scans_names = self.programe.downloader.get_scans_names()
        self.scan_selector.combobox.set_items(scans_names)
        self.scan_selector.combobox.setEditText(self.programe.config['data']['current-scan-name'])
    
    def validate_scan_name(self):
        self.downloader_buttons.download_button.setEnabled(False)

        current_text = self.scan_selector.combobox.currentText()
        scans_names = self.programe.downloader.get_scans_names()
        if current_text in scans_names:
            scan_link = self.programe.downloader.get_scan_link(name=current_text)
            scan_chapters = self.programe.downloader.scan_chapters(scan_link)
            scan_chapters_numbers = [chapter_link.split("/")[-1] for chapter_link in scan_chapters]

            self.programe.config['data']['current-scan-link'] = scan_link
            self.programe.config['data']['current-scan-name'] = current_text
            self.programe.config['data']['current-scan-chapters'] = scan_chapters
            self.programe.update_config()

            self.options_tab.chapters_checkboxes_view.model.set_items(chapters_numbers=scan_chapters_numbers)

        else:
            self.scan_selector.combobox.setEditText('Provid valid name please')
            self.programe.config['data']['current-scan-link'] = None
            self.programe.config['data']['current-scan-name'] = None
            self.programe.update_config()

        self.update_download_button()

    def update_download_button(self):
        self.downloader_buttons.download_button.setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            if self.programe.config['data']['current-scan-link'] is not None:
                self.downloader_buttons.download_button.setEnabled(True)
                return
    
    def update_validation_button(self):
        self.scan_selector.button.setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            self.scan_selector.button.setEnabled(True)
            return

    def update_select_folder_button(self):
        self.scans_folder_selector.button.setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            self.scans_folder_selector.button.setEnabled(True)
            return

    def update_pause_button(self):
        self.downloader_buttons.pause_button.setEnabled(False)
        if self.programe.download_scan_in_combobox_thread.alive:
            self.downloader_buttons.pause_button.setEnabled(True)
            return
    
    def update_stop_button(self):
        self.downloader_buttons.stop_button.setEnabled(False)
        if self.programe.download_scan_in_combobox_thread.alive:
            self.downloader_buttons.stop_button.setEnabled(True)
            return

    def update_all_buttons(self):
        self.update_download_button()
        self.update_validation_button()
        self.update_select_folder_button()
        self.update_pause_button()
        self.update_stop_button()

    def update_scan_combobox(self):
        self.scan_selector.combobox.lineEdit().setEnabled(False)
        if not self.programe.download_scan_in_combobox_thread.alive:
            self.scan_selector.combobox.lineEdit().setEnabled(True)
            return

    def download_button_clicked(self):
        self.downloader_buttons.download_button.setEnabled(False)
        self.scan_selector.button.setEnabled(False)
        self.scans_folder_selector.button.setEnabled(False)
        self.scan_selector.combobox.lineEdit().setEnabled(False)
        self.downloader_buttons.pause_button.setEnabled(True)
        self.downloader_buttons.stop_button.setEnabled(True)

        self.update_chapters()
        self.programe.download_scan_in_combobox_thread.start()

        self.programe.download_scan_in_combobox_thread.finished.connect(self.update_all_buttons)
        self.programe.download_scan_in_combobox_thread.finished.connect(self.update_scan_combobox)
        
    def update_chapters(self):
        items_text = self.options_tab.chapters_checkboxes_view.get_items_checked_text()
        main_url = self.programe.config['data']['current-scan-link']
        chapter_links = []
        for item_text in items_text:
            chapter_link = self.programe.downloader.scan_chapter_link_with_number(main_url=main_url, number=item_text)
            chapter_links.append(chapter_link)
        
        self.programe.config['data']['current-scan-chapters'] = chapter_links
        self.programe.update_config()
