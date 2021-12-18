import time

import requests
from ext.utils import create_folder, dump_json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class LoopThread(QThread):
    def __init__(self, target, timer:float, parent=None):
        QThread.__init__(self, parent)
        self.timer = timer
        self.target = target
        self.alive = False
        self.pause = False

    def run(self):
        self.alive = True
        while self.alive:
            if not self.pause:
                self.target()
                time.sleep(self.timer)
    
    def setPause(self, arg_1:bool):
        self.pause = arg_1
    
    def stop(self):
        self.alive = False
        self.wait()

class DownloadScanInComboboxThread(QThread):
    def __init__(self, programe, parent=None):
        QThread.__init__(self, parent)
        self.programe = programe
        self.alive = False
        self.pause = False
    
    def setPause(self, arg_1:bool):
        self.pause = arg_1

    def stop(self):
        self.alive = False

    def run(self):
        self.alive = True
        
        scan_name = self.programe.getScanName()
        scan_link = self.programe.config['data']['current-scan-link']
        scan_folder = self.programe.config["data"]["scans-folder"]

        ### GET IMAGES LINKS AND HER PATH ###
        chapters_links = self.programe.config['data']['current-scan-chapters']
        images_links = []
        self.programe.GUI.right_labels.top_label.print('Scrapping images links, please wait...')
        for chapter_link in chapters_links:
            while self.pause:
                time.sleep(0.1)
            if not self.alive:
                self.programe.GUI.right_labels.top_label.print('Operation stoped!')
                return
                
            images = []

            img_results = self.programe.downloader.get_chapter_images_links(chapter_link=chapter_link)
            for chapter_image in img_results['chapter-images']:
                while self.pause:
                    time.sleep(0.1)
                if not self.alive:
                    self.programe.GUI.right_labels.top_label.print('Operation stoped!')
                    return
                    
                folder_path = f"{scan_folder}/{scan_name}/{img_results['chapter-name']}"
                images.append((chapter_image[0], f"{folder_path}/{str(chapter_image[1]).zfill(3)}.jpg"))
                
            images_links.append({
                'chapter-name': img_results['chapter-name'],
                'chapter-number': img_results['chapter-number'],
                'chapter-folder': folder_path,
                'images':images
            })
        self.programe.GUI.right_labels.top_label.print('Images links scrapped! Downloading images...')

        ### DOWNLOAD IMAGES ###
        chapter_count = len(chapters_links)
        
        create_folder(f'{scan_folder}/{scan_name}')
        i = 0
        while len(images_links) > 0:
            while self.pause:
                time.sleep(0.1)
            if not self.alive:
                self.programe.GUI.right_labels.top_label.print('Operation stoped!')
                return
                
            dict = images_links[0]
            while len(dict['images']) > 0:
                while self.pause:
                    time.sleep(0.1)
                if not self.alive:
                    self.programe.GUI.right_labels.top_label.print('Operation stoped!')
                    return
                    
                image = dict['images'][0]

                try:
                    r = requests.get(image[0]).content 
                    try:
                        r = str(r, 'utf-8') 
                    except UnicodeDecodeError:
                        create_folder(dict['chapter-folder'])
                        with open(image[1], "wb+") as f: 
                            f.write(r)
                except:
                    pass
                del dict['images'][0]
            del images_links[0]
            i+=1
            self.programe.GUI.right_labels.top_label.print(f'Chapter {dict["chapter-number"]} download ({i}/{chapter_count})')
        self.programe.GUI.right_labels.top_label.print(f'{scan_name} was downloaded!')

        self.alive = False
