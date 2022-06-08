import json
import os
import sys
import threading
from rich.console import Console

try: import gdrive
except: from src import gdrive

relpath = os.getcwd()
console = Console()

global root

objects_all = []
objects = {
    'name':{},
    'id':{},
    'path':{},
}

class DriveObject():
    def __init__(self, name, id, path) -> None:
        self.name = name
        self.id = id
        self.path = path

        objects_all.append(self)
        
        objects["name"].update({self.name:self})
        objects["id"].update({self.id:self})
        objects["path"].update({self.path:self})
    
        try:
            with open (f"{relpath}/userdata/driveObjects.json", "r") as f:
                jsonObj = json.load(f)
        except:
            jsonObj = {}

        jsonObj.update({name:{
                        "name":self.name,
                        "id":self.id,
                        "path":self.path
                        }})

        jsonObj = json.dumps(jsonObj, indent=4)
        with open(f"{relpath}/userdata/driveObjects.json", "w") as f:
            f.write(jsonObj)
    
    
    def _forget(self):

        #% Constant {O(C_1 + 3C_2)}
        objects_all.remove(self)
        del objects["id"][self.id]
        del objects["path"][self.path]
        del objects["name"][self.name]


def store_root(_root) -> dict:
    """Stores new root string to json under "root"

    Args:
        _root (string): driveId as string

    Returns:
        dict: {'root': 'new rootId'}
    """

    # ~ store new root in memory
    global root
    root = _root

    # ~ if config exists load -> jsonObj. Otherwise jsonObj -> empty dict
    jsonObj = {}
    if os.path.exists(f"{relpath}/userdata/config.json"):
        try:
            with open(f"{relpath}/userdata/config.json", "r") as f:
                jsonObj = json.load(f)
        except:
            pass

    # ~ update root in dict then serialize
    jsonObj.update({"root": _root})
    jsonObj = json.dumps(jsonObj)

    # ~ write dict to config
    with open(f"{relpath}/userdata/config.json", "w") as f:
        f.write(jsonObj)

    # ~ return root from dict for test
    return json.loads(jsonObj)["root"]

def load_drive(root):
    path = objects["id"][root].path
    
    children = gdrive.ls(root)

    for i in children:
        name = i.get('name')
        if(name in objects["name"].keys()):
            console.print(f'naming conflict, not adding {name}', style='red')
            DriveObject(name, i.get('id'))

        thread = threading.Thread(target=load_drive(i))
        thread.start()

