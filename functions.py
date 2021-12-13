
import os

import bs4
import requests


### General functions ###
def create_folder(folder_name:str):
    """
    Create a folder if not exists\n
    Args :\n
        `folder_name` (str) : the name of the folder\n
    Return :\n
        `None`\n
    """
    try:
        os.mkdir(folder_name) 
    except: 
        pass

def download_chapter_images(folder:str, images:list, chapter_name:str):
    """
    Create if not exists the chapter folder and add chapter images after they are downloaded\n
    Args :\n
        `folder` (str) : the name of scan folder, the main folder\n
        `images` (list of str) : the list of images's links\n
        `chapter_name` (str) : the name of images's chapter\n
    Return :\n
        `result` (dict) : contains the images counter 'img-count' and the images downloaded counter 'img-dl'\n
    """
    count = 0
    
    for i, image in enumerate(images):
        try: 
            image_link = image["data-src"]
        except:
            pass

        try: 
            r = requests.get(image_link).content 
            try: 
                r = str(r, 'utf-8') 

            except UnicodeDecodeError:
                subfolder = f"{folder}/{chapter_name}"
                create_folder(subfolder)
                with open(f"{subfolder}/page-{str(i+1).zfill(3)}.jpg", "wb+") as f: 
                    f.write(r) 
                count += 1
        except: 
            pass

    return {
        "img-count": len(images),
        "img-dl": count
    } 

def dl_chapter_with_link(folder:str, chapter_link:str):
    """
    Download all images in a scan chapter\n
    Args :\n
        `folder` (str) : the folder to add chapter\n
        `chapter_link` (str) : the chapter's link to download\n
    Return :\n
        `chapter_stats` (dict) : chapter download statistics\n
    """
    create_folder(folder_name=folder)

    chapter_number = chapter_link.split("/")[-1]
    chapter_name = "chapitre-"+str(chapter_number).zfill(5)

    r = requests.get(chapter_link) 
    soup = bs4.BeautifulSoup(r.text, 'html.parser') 
    images = soup.findAll("img", {"class": "img-responsive"})
    img_results = download_chapter_images(folder=folder, images=images, chapter_name=chapter_name)
    img_results["chapter-name"] = chapter_name
    img_results["chapter-number"] = chapter_number

    return img_results

def scan_chapters(main_url:str):
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
