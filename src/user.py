import sys

# ~ import directly when called from within src otherwise call from src
try:
    import storage, gdrive, cli
except:
    from src import storage, gdrive, cli

from rich.console import Console

console = Console()


def Ucd(params):
    _, splitted, _, argdict, flags = params
    _path = "root"

    if "-l" in flags:
        try:
            _path = storage.objects["name"][argdict["-l"]].path
        except:
            pass

    elif len(splitted) == 2:
        try:
            _path = storage.objects["name"][splitted[1].replace("'", "")].path
        except:
            pass

    cli.cd(_path)


def UList(params):
    _, splitted, _, argdict, flags = params
    _path = cli.path

    if "-l" in flags:
        try:
            _path = storage.objects["name"][argdict["-l"]].path
        except:
            pass

    elif len(splitted) == 2:
        try:
            _path = storage.objects["name"][splitted[1].replace("'", "")].path
        except:
            pass

    storage.ls(_path)


def USync(params):
    _, splitted, _, argdict, flags = params

    _root = storage.objects["path"][cli.path].id

    if "-l" in flags:
        try:
            _root = storage.objects["name"][argdict["-l"]].id
        except:
            pass
    elif len(splitted) == 2:
        _root = storage.objects["name"][splitted[1].replace("'", "")].id

    storage.sync_drive(_root)


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
functions = {"exit": UExit, "root": URoot, "sync": USync, "ls": UList, "cd": Ucd}
