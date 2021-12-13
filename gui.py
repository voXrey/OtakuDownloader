import threading
import time
import requests
import json
import sys
import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import functions
import utils



class ThreadHandler:
    def __init__(self):
        self.threads = {}
    
    def createThread(self, name:str, target):
        self.threads[name] = {
            'target':target,
            'operating':False
        }
    
    def getThread(self, name:str):
        thread = threading.Thread(name=name, target=self.threads[name]['target'])
        return thread
    
    def enableThread(self, name:str):
        self.threads[name]['operating'] = True
    
    def disableThread(self, name:str):
        self.threads[name]['operating'] = False

    def isEnableThread(self, name:str):
        return self.threads[name]['operating']

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        ### Get configuration
        config = utils.open_json(path="config.json") # get json
        self.default_config = {
            "data": {
                "current-scan-link": None,
                "scans-folder": None,
                "current-scan-chapters": []
            }
        } # set a default config (prevent errors)
        if config is None: config = self.default_config # if there is a config error use default config
        self.data = config["data"] # save config data in window class
        self.data["current-scan-chapters"] = [] # modify last data

        self.last_config = config # set a save config (prevent bugs)

        ### Set downloads stats dict
        self.stats = {
            "chapters-downloaded" : None,
            "images-downloaded" : None,
            "begining-timestamp" : None,
            "ending-timestamp" : None
        }

        ### Set window
        self.setWindowTitle("OtakuDownloader") # set window title
        self.setMinimumSize(QSize(1200, 800)) # set window minimum size
        self.setWindowIcon(QIcon('icon.jpg')) # set window icon

        self.create_widgets() # create widgets
        self.set_widgets() # place widgets in window

        ### Create thread handler
        self.thread_handler = ThreadHandler()
        self.set_threads() # set threads in thread handler and start some threads


    def create_widgets(self):
        """
        Create app widgets
        """
        ### Left widgets
        # Select folder button
        # button which select the global folder to download scans
        self.__button__folder_select = QPushButton("Select scans folder", self) # create button object and add text
        self.__button__folder_select.setObjectName("folder_select_button") # set the object name
        self.__button__folder_select.clicked.connect(self.select_scans_folder) # connect button to self.select_scans_folder function

        # Selected folder label
        # label which is wirtten the selected golbal folder to download scans
        self.__label__folder_selected = QLabel(parent=self) # create label object
        self.__label__folder_selected.setObjectName("folder_selected_label") # set the object name
        self.update_selected_folder_label() # update label text
        
        
        # Scan's search bar (combobox)
        # user write scan's link in this line edit
        line_edit__scan_link = QLineEdit(self) # create line edit object
        line_edit__scan_link.setObjectName("scan_link_line_edit") # set the object name
        line_edit__scan_link.textChanged.connect(self.update_get_scan_chapters_button)
        line_edit__scan_link.setText(self.data["current-scan-link"]) # set last link (or no) in line edit

        self.__combobox__scan_name = QComboBox(self) # create line edit object
        self.__combobox__scan_name.addItems(self.get_scans_names())
        self.__combobox__scan_name.setLineEdit(line_edit__scan_link)
        self.__combobox__scan_name.setObjectName("scan_name_combobx") # set the object name

        # TO MODIFY BY 'VALIDATION'
        self.__button__get_scan_chapters = QPushButton("Get scan chapters", self)
        self.__button__get_scan_chapters.setObjectName("get_scan_button")
        self.__button__get_scan_chapters.clicked.connect(self.get_scan_chapters)

        # Download chapters button
        # button to download all chapters of a scan's link
        self.__button__download_chapters = QPushButton("Download chapters", self) # create button object
        self.__button__download_chapters.setObjectName("download_chapters_button") # set the object name
        self.__button__download_chapters.clicked.connect(self.download_chapters) # connect button to self.download_chapters function

        ### Right widgets
        # General info label
        # tall label to the right to give info to user
        self.__label__general_info = QLabel(parent=self) # create label object
        self.__label__general_info.setObjectName("general_info_label") # set the object name
        self.text_label_general_info = [] # set text list (to simulate a consol)

        # Stats label
        # little label to the right to give download stats to user
        self.__label__stats_info = QLabel(parent=self) # create label object
        self.__label__stats_info.setObjectName("stats_info_label") # set the object name

    def set_widgets(self):
        """
        Place widgets in window
        """
        ### Constants variables
        # window
        margin_left_right = self.size().width()/20 # defined the margin to the right and to the left
        margin_top_bottom = margin_left_right # defined the margin  at the bottom and at the top
        # widgets
        default_widget_width = (self.size().width()/2)-(margin_left_right*2) # defined the default widget width
        default_widget_height = self.size().height()/18 # defined the default widget height
        
        ### Left widgets
        # Select folder button
        widget1_X, widget1_Y = margin_left_right, margin_top_bottom
        self.__button__folder_select.setGeometry(widget1_X, widget1_Y, default_widget_width, default_widget_height)

        # Selected folder label
        widget2_X, widget2_Y = margin_left_right, (widget1_Y+default_widget_height)
        self.__label__folder_selected.setGeometry(widget2_X, widget2_Y, default_widget_width, default_widget_height)

        # Scan's link line edit
        widget3_X, widget3_Y =margin_left_right, (widget2_Y+default_widget_height+default_widget_height/2)
        self.__combobox__scan_name.setGeometry(widget3_X, widget3_Y, default_widget_width, default_widget_height/1.5)

        # TO MODIFY BY 'VALIDATION'
        widget4_X, widget4_Y = margin_left_right, (widget3_Y+default_widget_height)
        self.__button__get_scan_chapters.setGeometry(widget4_X, widget4_Y, default_widget_width, default_widget_height)

        # Download chapters button
        widget5_X, widget5_Y = margin_left_right, (widget4_Y+default_widget_height)
        self.__button__download_chapters.setGeometry(widget5_X, widget5_Y, default_widget_width, default_widget_height)

        ### Right widgets
        # General info label
        widget_right1_X, widget_right1_Y = self.size().width()/2, margin_top_bottom
        widget_right1_W, widget_right1_H = self.size().width()/2-margin_left_right, self.size().height()/1.5
        self.__label__general_info.setGeometry(widget_right1_X, widget_right1_Y, widget_right1_W, widget_right1_H)
        self.__label__general_info.setAlignment(Qt.AlignBottom)
        self.__label__general_info.setMargin(5)

        # Stats label
        self.__label__general_info.setStyleSheet("background-color: #202020")
        widget_right2_X, widget_right2_Y = widget_right1_X, (widget_right1_Y+widget_right1_H+(margin_top_bottom/2))
        widget_right2_W, widget_right2_H = widget_right1_W, (self.size().height()-widget_right2_Y-(margin_top_bottom/2))
        self.__label__stats_info.setGeometry(widget_right2_X, widget_right2_Y, widget_right2_W, widget_right2_H)
        self.__label__stats_info.setAlignment(Qt.AlignTop)
        self.__label__stats_info.setMargin(5)
        self.__label__stats_info.setStyleSheet("background-color: #202020")

    def set_threads(self):
        self.thread_handler.createThread(name='update-buttons-loop', target=self.update_buttons_loop)
        self.thread_handler.createThread(name='update-right-labels-loop', target=self.update_right_labels_loop)
        self.thread_handler.createThread(name='get-scan-chapters', target=self.get_scan_chapters_process)
        self.thread_handler.createThread(name='download-chapters', target=self.download_chapters_process)

        thread_update_buttons_loop = self.thread_handler.getThread(name='update-buttons-loop')
        self.thread_handler.enableThread(name='update-buttons-loop')
        thread_update_buttons_loop.start()

        thread_update_right_labels_loop = self.thread_handler.getThread(name='update-right-labels-loop')
        self.thread_handler.enableThread(name='update-right-labels-loop')
        thread_update_right_labels_loop.start()


    ### Manage right labels ###
    # add a text in general info label
    def print_general_info_label(self, new_text:str):
        self.text_label_general_info.append(new_text)
    
    # update general info label
    def update_general_info_label(self):
        if len(self.text_label_general_info) > 40:
            self.text_label_general_info = self.text_label_general_info[-41:]
        
        text = "\n".join(self.text_label_general_info)
        self.__label__general_info.setText(text)

    # update stats info label
    def update_stats_info_label(self):
        if self.stats["ending-timestamp"] is None:
            if self.stats["begining-timestamp"] is not None:
                text = "Please wait..."
            else:
                text = "Download a scan to obtain download stats"
        else:
            chapters_downloaded = self.stats["chapters-downloaded"]
            images_downloaded = self.stats["images-downloaded"]
            time_taken = self.stats["ending-timestamp"]-self.stats["begining-timestamp"]

            text=""
            text+=f"Chapters downloaded : {chapters_downloaded}\n"
            text+=f"Images downloaded : {images_downloaded}\n"
            text+=f"Time taken : {int(time_taken)}s\n"
            text+=f"Images downloaded/s and /min : {int(images_downloaded/time_taken)} img/s, {int(images_downloaded/time_taken*60)} img/min\n"
            text+=f"Chapters downloaded/min : {int(chapters_downloaded/time_taken*60)} chap/min\n"

        self.__label__stats_info.setText(text)

    # update right labels
    def update_right_labels(self):
        self.update_general_info_label()
        self.update_stats_info_label()

    # loop for update right labels
    def update_right_labels_loop(self):
        while True:
            self.update_right_labels()
            self.maybe_stop_thread()
            time.sleep(0.5)


    ### Select the scans folder ###
    # when button is clicked
    def select_scans_folder(self):
        path_to_file = QFileDialog.getExistingDirectory()
        if path_to_file == "": path_to_file = self.data["scans-folder"]
        self.data["scans-folder"] = path_to_file
        self.update_selected_folder_label()
        self.update_data()


    ### Download chapters ###
    # when button is clicked
    def download_chapters(self):
        self.thread_handler.enableThread(name='download-chapters')

        self.update_download_button()
        self.update_buttons()
        
        thread = self.thread_handler.getThread(name='download-chapters')
        thread.start()

    # thread function
    def download_chapters_process(self):
        self.stats = {
            "chapters-downloaded" : None,
            "images-downloaded" : None,
            "begining-timestamp" : None,
            "ending-timestamp" : None
        }

        chapters_links = self.data["current-scan-chapters"]
        scan_name = self.data["current-scan-name"]
        scan_folder = self.data["scans-folder"]+"/"+scan_name

        chapters_count = len(chapters_links)
        images_downloaded = 0

        start_time = time.time()
        self.stats["begining-timestamp"] = start_time

        for chapter_link in chapters_links:
            self.maybe_stop_thread()
            stats = functions.dl_chapter_with_link(folder=scan_folder, chapter_link=chapter_link)
            self.print_general_info_label(f"{stats['img-dl']}/{stats['img-count']} pages downloaded for chapter {stats['chapter-number']}")
            self.update_general_info_label()
            images_downloaded+=stats['img-dl']

        end_time = time.time()
        if end_time == start_time: end_time=start_time+1
        self.stats["ending-timestamp"] = end_time

        self.print_general_info_label(f"{chapters_count} chapters succesfully downloaded!")
        self.update_general_info_label()

        self.stats["chapters-downloaded"] = chapters_count
        self.stats["images-downloaded"] = images_downloaded

        self.thread_handler.disableThread(name='download-chapters')


    ### Get scan chapters ###
    # when button is clicked
    def get_scan_chapters(self):
        self.thread_handler.enableThread(name='get-scan-chapters')

        self.update_get_scan_chapters_button()
        self.update_buttons()

        thread = self.thread_handler.getThread(name='get-scan-chapters')
        thread.start()

    # thread function
    def get_scan_chapters_process(self):
        scan_link = self.get_scan_link()

        self.print_general_info_label(f"Scaning chapters in '{scan_link}' please wait...")
        self.update_general_info_label()
        
        self.data["current-scan-link"] = scan_link
        self.data["current-scan-name"] = self.__combobox__scan_name.lineEdit().text()
        self.update_data()

        chapters_links = functions.scan_chapters(main_url=scan_link)
        
        self.data["current-scan-chapters"] = chapters_links
        self.update_data()

        self.print_general_info_label(f"{len(chapters_links)} chapters links found!")
        self.update_general_info_label()

        self.thread_handler.disableThread(name='get-scan-chapters')


    ### Update programm ###
    # update data
    def update_data(self):
        config = utils.open_json(path="config.json")
        if config is None: config=self.last_config
        config["data"] = self.data
        utils.dump_json(path="config.json", data=config)
        self.last_config = config

    # update selected folder label
    def update_selected_folder_label(self):
        folder = self.data['scans-folder']
        if folder is None: folder_text = "No folder selected"
        else: folder_text = f"Folder selected : '{folder}'"
        self.__label__folder_selected.setText(folder_text)

    # update select folder button
    def update_select_folder_button(self):
        if not self.thread_handler.isEnableThread(name='download-chapters'):
            return self.__button__folder_select.setEnabled(True)
        self.__button__folder_select.setDisabled(True)

    # update line edit for scan's link
    def update_line_edit_scan_link(self):
        if not self.thread_handler.isEnableThread(name='get-scan-chapters'):
            if not self.thread_handler.isEnableThread(name='download-chapters'):
                return self.__combobox__scan_name.lineEdit().setEnabled(True)
        self.__combobox__scan_name.lineEdit().setDisabled(True)

    # update download button
    def update_download_button(self):
        if self.data["scans-folder"] is not None:
            if len(self.data["current-scan-chapters"]) > 0:
                if not self.thread_handler.isEnableThread(name='get-scan-chapters'):
                    if not self.thread_handler.isEnableThread(name='download-chapters'):
                        return self.__button__download_chapters.setEnabled(True)
        self.__button__download_chapters.setDisabled(True)

    # update get scan chapters button
    def update_get_scan_chapters_button(self):
        try:
            if not self.thread_handler.isEnableThread(name='get-scan-chapters'):
                if not self.thread_handler.isEnableThread(name='download-chapters'):
                    return self.__button__get_scan_chapters.setEnabled(True)
            self.__button__get_scan_chapters.setDisabled(True)
        except:
            pass
    

    # update buttons
    def update_buttons(self):
        self.update_get_scan_chapters_button()
        self.update_download_button()
        self.update_select_folder_button()
        self.update_line_edit_scan_link()

    # update buttons loop
    def update_buttons_loop(self):
        while True:
            self.update_buttons()
            self.maybe_stop_thread()
            time.sleep(1)


    ### Get scan's info
    # get scans names list
    def get_scans_names(self):
        r = requests.get("https://mangascan.cc/search")
        decoded = json.loads(r.content.decode('utf-8'))
        suggestions_list = decoded["suggestions"]
        return [sugg['value'] for sugg in suggestions_list]
    
    # get scan link with his name
    def get_scan_link(self):
        r = requests.get("https://mangascan.cc/search")
        decoded = json.loads(r.content.decode('utf-8'))
        suggestions_list = decoded["suggestions"]
        
        name = self.__combobox__scan_name.lineEdit().text()

        partial_link = [dic['data'] for dic in suggestions_list if dic['value'] == name][0]
        link = "https://mangascan.cc/manga/" + partial_link
        return link


    ### Stop thread if main thread is stoped ###
    def maybe_stop_thread(self):
        if not threading.main_thread().is_alive(): sys.exit()
