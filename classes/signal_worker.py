from PyQt5.QtCore import *


class Worker(QObject):
    def __init__(self, programe, parent=None):
        super(Worker, self).__init__(parent)
        self.programe = programe
        
    @pyqtSlot(str)
    def onJob(self, signal):
        if signal == 'select_scan_folder_button_clicked':
            self.programe.select_scan_folder_button_clicked()
        elif signal == 'pause_button_clicked' or signal == 'unpause_button_clicked':
            self.programe.pause_download_button_clicked()
        elif signal == 'stop_button_clicked':
            self.programe.stop_download_button_clicked()
        elif signal == 'download_button_clicked':
            self.programe.download_button_clicked()
        elif signal == 'validation_button_clicked':
            self.programe.validation_button_clicked()