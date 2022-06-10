import json
import os
import sys
import threading
import time
from rich.console import Console

try:
    import gdrive
except:
    from src import gdrives

relpath = os.getcwd()
console = Console()

global root
root = None

objects_all = []
objects = {
    "name": {},
    "id": {},
    "path": {},
}


class DriveObject:
    def __init__(self, name, id, path) -> None:
        """Initalize and store in objects['name'],['id'], ['path'] and objects_all list"""
        if(name in objects['name']):
            console.print(f'cannot add drive Object {name} at {path} because a duplicate name exists', style='yellow')
            return None

        self.name = name
        self.id = id
        self.path = path

        objects_all.append(self)

        # ~ store in loacal memory
        objects["name"].update({self.name: self})
        objects["id"].update({self.id: self})
        objects["path"].update({self.path: self})

        # ~ if dict exists and is readable load it
        try:
            with open(f"{relpath}/userdata/driveObjects.json", "r") as f:
                jsonObj = json.load(f)
        except:
            jsonObj = {}

        # ~ store in memory to unserialized jsonObj
        jsonObj.update({name: {"name": self.name, "id": self.id, "path": self.path}})

        # ~ store object in json
        jsonObj = json.dumps(jsonObj, indent=4)
        with open(f"{relpath}/userdata/driveObjects.json", "w") as f:
            f.write(jsonObj)

    def _forget(self):

        # ~ remove from all collections then move to garbage
        #% Constant {O(C_1 + 3C_2)}
        objects_all.remove(self)
        del objects["id"][self.id]
        del objects["path"][self.path]
        del objects["name"][self.name]
        del self


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

    console.print(f"changed root to {_root}", style="green")

    # ~ return root from dict for test
    return json.loads(jsonObj)["root"]

def ls(_path):
    for i in objects_all:
        path = str(i.path)
        if( _path in path):
            console.print(path, style='#1b83e3')

def load_drive(_root):
    resync = [i for i in objects_all if objects["id"][_root].path in i.path]
    for i in resync:
        i._forget()

    DriveObject("root", _root, "root")

    def rload_drive(_root):

        #~ get parent path
        try:
            path = objects["id"][_root].path
        except:
            return None

        # ~ get children to recur
        children = gdrive.ls(_root)

        # ~ loop through all children and reccur on theirs
        for i in children:
            name = i.get("name")
            id = i.get("id")

            #~ remove spaces and print path
            name = name.replace(" ", "")

            console.print(f"{path}/{name}")

            #~ init and store drive object
            DriveObject(name, id, f"{path}/{name}")

            #~ Check to see if is folder or items, decreases fetch time as checking item never yields a result
            if(i.get('mimeType') == 'application/vnd.google-apps.folder'):

                #~ create thread to fetch all children 

                th = threading.Thread(target=rload_drive(id))
                th.start()
    

    startTime = time.perf_counter()
    rload_drive(_root)
    console.print(f'{time.perf_counter() - startTime} seconds to fetch all drive objects')

def sync_drive(_root):
    
    props = [objects["id"][_root].name, _root, objects["id"][_root].path]

    resync = [i for i in objects_all if objects["id"][_root].path in i.path]
    for i in resync:
        i._forget()

    DriveObject(props[0], props[1], props[2])

    def rload_drive(_root):

        #~ get parent path
        try:
            path = objects["id"][_root].path
        except:
            return None

        # ~ get children to recur
        children = gdrive.ls(_root)

        # ~ loop through all children and reccur on theirs
        for i in children:
            name = i.get("name")
            id = i.get("id")

            #~ remove spaces and print path
            name = name.replace(" ", "")

            console.print(f"{path}/{name}")

            #~ Check to see if is folder or items, decreases fetch time as checking item never yields a result
            if(i.get('mimeType') == 'application/vnd.google-apps.folder'):

                #~ init and store drive object
                DriveObject(name, id, f"{path}/{name}")

                #~ create thread to fetch all children 

                th = threading.Thread(target=rload_drive(id))
                th.start()
    

    startTime = time.perf_counter()
    rload_drive(_root)
    console.print(f'{time.perf_counter() - startTime} seconds to sync')