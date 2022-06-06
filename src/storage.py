import json
import os
import sys

relpath = os.getcwd()

global root

def store_root(_root):
    global root
    root = _root

    jsonObj = {}
    if os.path.exists(f'{relpath}/userdata/config.json'):
        try:
            with open(f'{relpath}/userdata/config.json', 'r') as f:
                jsonObj = json.load(f)
        except:
            pass
    
    jsonObj.update({'root':_root})
    jsonObj = json.dumps(jsonObj)

    with open(f'{relpath}/userdata/config.json', 'w') as f:
        f.write(jsonObj)

    return jsonObj