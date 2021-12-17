import json
import os


def open_json(path:str):
    """
    Open json and give data\n
    Args :\n
        `path` (str) : path of json file\n
    """
    try:
        with open(file=path, mode='r', encoding="utf-8") as f:
            data = json.load(f)
            f.close()
            return data
    except:
        return

def dump_json(path:str, data:dict):
    """
    Open json and dump data\n
    Args :\n
        `path` (str) : path of json file\n
        `data` (dict) : data to dump in json file\n
    Return :\n
        `result` (bool) : is succesfully\n
    """
    try:
        with open(file=path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            f.close()
            return True
    except:
        return False

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
