import os
import cli
import user
import gdrive
from rich.console import Console

console = Console()
developerMode = True

def main():
    
    console.print(os.getcwd(), style='yellow')
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
