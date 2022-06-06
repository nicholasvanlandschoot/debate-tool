import json
import os
import cli
import storage
import user
import gdrive
from rich.console import Console
from rich.text import Text

console = Console()
developerMode = True

def main():
    try:
        with open(f'{storage.relpath}/userdata/config.json') as f:
            jsonObj = json.load(f)
        storage.root = jsonObj["root"]
    except:
        text = Text('enter root % ')
        text.stylize('cyan')
        storage.store_root(console.input(text))

    gdrive.validate()
    while True:
        ui = cli.listen()
        params = cli.parse(ui)

        try:
            called = ui.split()[0]
            user.functions[called](params)
        except Exception as e:
            if developerMode: console.print(f'Command failed → error {e}', style='red')
            else: console.print(f'Command does not exist', style='red')

if __name__ == '__main__':
    main()
