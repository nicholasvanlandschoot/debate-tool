from rich.console import Console
from rich.text import Text

console = Console()

def parse(str):

    #~ Create a list of every word in str
    splitted = str.split()

    #~ Take every word where there is no dash excluding the first element 
    args = [i for i in splitted[1:] if "-" not in i]
    
    #~ Append a dict of every word starting with - followed by the next word in the list as its value
    argdict = {}
    for i in range(len(splitted) - 1):
        if "-" in splitted[i]:
            argdict.update({splitted[i]: splitted[i + 1]})

    #~ Take every word with a - excluding the first element
    flags = [i for i in splitted[1:] if "-" in i]

    return str, splitted, args, argdict, flags

def listen():
    text = Text(" % ")
    text.stylize("cyan")
    return console.input(text)
