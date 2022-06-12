from rich.console import Console
from rich.text import Text

try:
    import storage
except:
    from src import storage

console = Console()
path = "root"


def parse(str) -> tuple:
    """This method parses a user passed command to paramaters in various forms

    Args:
        str (string): user passed input (should be passed listen() method which returns the str)

    Returns:
        tuple: tuple of len 5 containing paramaters in various forms
        unpack using: str, splitted, args, argdict, flags

        str: original user passed string
        splitted: list of all words in string
        args: list of all arguments (not flags starting with - and not first command)
        argdict dictionary of arguments for values with flag for key
        flags: list of flags (starts with -)
    """

    # ~ Create a list of every word in str
    splitted = str.split()

    # ~ Take every word where there is no dash excluding the first element
    args = [i for i in splitted[1:] if "-" not in i]

    # ~ Append a dict of every word starting with - followed by the next word in the list as its value
    argdict = {}
    for i in range(len(splitted) - 1):
        if "-" in splitted[i]:
            argdict.update({splitted[i]: splitted[i + 1]})

    # ~ Take every word with a - excluding the first element
    flags = [i for i in splitted[1:] if "-" in i]

    return (str, splitted, args, argdict, flags)


def listen() -> str:
    """Listen for a user passed command in the terminal
       should be passed to the parse method to fetch paramaters in readable form.
    Returns:
        string: string of input
    """

    # ~ create and stylize text to display on the terminal with the input method
    text = Text(f"{path} % ")
    text.stylize("bold cyan")

    # ~ display text and return new input
    return console.input(text)


def cd(_root) -> None:
    """Change path in terminal and defualt ls/cd etc."""

    global path
    try:
        path = storage.objects["path"][_root.replace("'", "")].path
    except:
        console.print("does not exist", style="red")

    return None


def ls(_path) -> None:
    """Print ls to screen"""

    for i in storage.objects_all:
        # ~ get path of object s
        path = str(i.path)

        # ~ if it is child of path print it
        if _path in path:
            console.print(path, style="#1b83e3")
    return None
