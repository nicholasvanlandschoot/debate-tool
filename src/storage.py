import json
import os
import sys

relpath = os.getcwd()

global root


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
