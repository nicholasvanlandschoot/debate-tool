from rich.console import Console
from rich.text import Text

console = Console()

def parse(str):
    
    splitted = str.split()
    args = [i for i in splitted[1:] if '-' not in i]
    argdict = {}
    for i in range(len(splitted)-1): 
        if('-' in splitted[i]):
            argdict.update({splitted[i]: splitted[i+1]})
    
    flags = [i for i in splitted[1:] if '-' in i]

    return str, splitted, args, argdict, flags

def listen():
    text = Text(' % ')
    text.stylize('cyan')
    return console.input(text)