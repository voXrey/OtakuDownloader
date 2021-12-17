import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from ext.utils import dump_json, open_json
import sys
import time

from classes.downloader import Downloader
from classes.gui import GUI
from classes.threads import LoopThread, DownloadScanInComboboxThread


class Programe(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self.setStyle(path='assets/stylesheet.qss')
        self.setConfig()

        self.downloader = Downloader(self)
        self.setThreads()
        self.GUI = GUI(self)

        self.GUI.show()

    def setThreads(self):
        self.download_scans_to_dl_thread = LoopThread(target=self.downloader.download_images_to_dl, timer=0)
        self.download_scans_to_dl_thread.start()

        self.download_scan_in_combobox_thread = DownloadScanInComboboxThread(programe=self)
    
    def setConfig(self):
        """
        Get and set the programe configuration
        """
        # set a default config (prevent errors)
        default_config = open_json(path='datas/default_config.json')
        # get config dict in json file
        self.config = open_json(path="datas/config.json") 

        if self.config is None: self.config = default_config # if there is a config error use default config
        self.config["data"]["current-scan-chapters"] = [] 
        self.config["data"]["current-scan-link"] = None
        self.last_config = self.config # set a backup config (prevent bugs)

    def update_config(self):
        return dump_json(path='datas/config.json', data=self.config)

    def setStyle(self, path:str):
        file = QtCore.QFile(path)
        if not file.open( QtCore.QFile.ReadOnly): return
        qss = QtCore.QTextStream(file)
        self.setStyleSheet(qss.readAll())

    def getScanName(self):
        scan_name = self.GUI.scans_combobox.lineEdit().text()
        scans_names = self.downloader.get_scans_names()
        if not scan_name in scans_names: return None
        return scan_name

    
    

if __name__ == '__main__':
    programe = Programe()
    programe.exec_()
