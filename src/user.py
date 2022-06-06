from sys import exit as leave
from src import storage
from rich.console import Console

console = Console()

def URoot(params):
    _, splitted, _, argdict, flags = params
    _root = None

    if ("-l" in flags):
        try:
            _root = argdict["-l"]
            storage.store_root(_root)
            return(_root)
        except:
            pass

    if(len(splitted) > 1):
        _root = splitted[1]
        storage.store_root(_root)
        return(_root)

    else:
        console.print("not valid, can not store new root", style="red")
        return None


def UExit(params):
    leave()

functions={
    "exit":UExit,
    "root":URoot
}
