import json
import os
import time

import bs4
import requests


class Downloader:
    def __init__(self, programe):
        self.programe = programe
        self.images_to_dl = []

    def download_images_to_dl(self):
        if len(self.images_to_dl) > 0:
            img = self.images_to_dl[0]
            if not os.path.exists(img[1]):
                os.makedirs(img[1])
            self.download_image_with_link(path=img[2], image_link=img[0])
            del self.images_to_dl[0]
        else:
            time.sleep(1)

    def download_image_with_link(self, path:str, image_link:list):
        dl = False
        try: 
            r = requests.get(image_link).content 
            try: 
                r = str(r, 'utf-8') 
            except UnicodeDecodeError:
                with open(path, "wb+") as f: 
                    f.write(r)
                dl = True
        except: 
            pass
        return dl

    def get_chapter_images_links(self, chapter_link:str):
        chapter_number = chapter_link.split("/")[-1]
        chapter_name = "chapitre-"+str(chapter_number).zfill(5)

        r = requests.get(chapter_link)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')

        images = soup.findAll("img", {"class": "img-responsive"})
        links = []
        for i,image in enumerate(images):
            try: links.append((image["data-src"], i))
            except: pass

        img_results = {
            "chapter-name" : chapter_name,
            "chapter-number" : chapter_number,
            "chapter-images": links
        }

        return img_results

    def scan_chapters(self, main_url:str):
        """
        Get all scan's chapters's link\n
        Args :\n
            `main_url` (str) : the scan url\n
        Return :\n
            `chapters_links` (list of str) : the list of chapters's links\n
        """
        r = requests.get(main_url)
        soup = bs4.BeautifulSoup(r.text, 'html.parser') 
        chapters_ul = soup.findAll("ul", {"class":"chapters"})[0]
        chapters_a = chapters_ul.findAll("a")
        return [chapter_a["href"] for chapter_a in reversed(chapters_a)]
    
    def scan_chapter_link_with_number(self, main_url:str, number):
        return f'{main_url}/{number}'

    def get_scans_names(self):
        r = requests.get("https://mangascan.cc/search")
        decoded = json.loads(r.content.decode('utf-8'))
        suggestions_list = decoded["suggestions"]
        return [sugg['value'] for sugg in suggestions_list]
    
    def get_scan_link(self, name):
        r = requests.get("https://mangascan.cc/search")
        decoded = json.loads(r.content.decode('utf-8'))
        suggestions_list = decoded["suggestions"]

        partial_link = [dic['data'] for dic in suggestions_list if dic['value'] == name][0]
        link = "https://mangascan.cc/manga/" + partial_link
        return link
