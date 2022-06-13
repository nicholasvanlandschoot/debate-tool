import sys

# ~ import directly when called from within src otherwise call from src
try:
    import storage, gdrive, cli
except:
    from src import storage, gdrive, cli

from rich.console import Console

console = Console()


def USnip(params):
    _, splitted, _, argdict, flags = params
    _name = None
    _snipName = None

    if "-n" in flags:
        try:
            _snipName = argdict["-n"]
        except:
            pass

    if "-l" in flags:
        try:
            _name = storage.objects["name"][argdict["-l"]].id
        except:
            pass

    elif len(splitted) > 1:
        try:
            _name = storage.objects["name"][splitted[1]].id
        except:
            pass
    if _name != None:
        gdrive.fetch_file(_name, storage.objects['id'][_name].name, _snipName)

def UDelete(params):
    _, splitted, _, argdict, flags = params

    _id = None
    if "-l" in flags:
        try:
            _id = storage.objects["name"][argdict["-l"]].id
        except:
            pass

    elif len(splitted) > 1:
        try:
            _id = storage.objects["name"][splitted[1]].id
        except:
            pass

    if _id != None:
        gdrive.deleteFile(_id)


def UCreate(params):
    _, splitted, _, argdict, flags = params

    _name = "Untitled"
    _parent = storage.objects["path"][cli.path].id
    _type = "application/vnd.google-apps.document"

    if "-n" in flags:
        try:
            _name = argdict["-n"]
        except:
            pass
    elif len(splitted) > 1:
        _name = splitted[1]
    else:
        console.print("No name given, creating: Untitled", style="yellow")

    if "-l" in flags:
        try:
            _path = argdict["-l"]
        except:
            pass
    _path = f'{storage.objects["id"][_parent].path}/{_name}'

    if "-folder" in flags:
        _type = "application/vnd.google-apps.folder"
    elif "-doc" in flags:
        _type = "application/vnd.google-apps.document"

    gdrive.create(_name, _parent, _path, _type)


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

    cli.ls(_path)


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
functions = {
    "snip": USnip,
    "exit": UExit,
    "root": URoot,
    "sync": USync,
    "ls": UList,
    "cd": Ucd,
    "create": UCreate,
    "delete": UDelete,
}
