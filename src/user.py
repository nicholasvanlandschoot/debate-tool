import sys

# ~ import directly when called from within src otherwise call from src
try:
    import storage
except:
    from src import storage

from rich.console import Console

console = Console()


def URoot(params):
    _, splitted, _, argdict, flags = params
    _root = None

    # ~ take any word after -l flag as new root
    if "-l" in flags:
        try:
            _root = argdict["-l"]
            storage.store_root(_root)
            return _root
        except:
            pass

    # ~ if no flag found take first argument as root
    if len(splitted) > 1:
        _root = splitted[1]
        storage.store_root(_root)
        return _root

    # ~ print fail message and return None for test
    else:
        console.print("not valid, can not store new root", style="red")
        return None


def UExit(params):
    sys.exit()


# ~ bind strings that user can pass as commands to functions
functions = {"exit": UExit, "root": URoot}
