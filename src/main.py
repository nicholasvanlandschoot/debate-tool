import json
from rich.console import Console
from rich.text import Text

# ~ import directly when called from within src otherwise call from src
try:
    import cli, gdrive, storage, user
except:
    from src import cli, gdrive, storage, user

console = Console()
developerMode = True


def main() -> None:

    # ~ set root if it exists in config otherwise get it from user and store it
    try:
        with open(f"{storage.relpath}/userdata/config.json") as f:
            jsonObj = json.load(f)
        storage.root = jsonObj["root"]
    except:
        text = Text("enter root % ")
        text.stylize("cyan")
        storage.store_root(console.input(text))

    # ~ Validate user credentials or login using OAuth
    gdrive.validate()

    # ~ load drive objects from drive
    storage.load_drive(storage.root)

    # ~ As the application runs listen to and parse input
    while True:
        ui = cli.listen()
        params = cli.parse(ui)

        # ~ Call string bound function or call error if there is no corresponding function
        try:
            called = ui.split()[0]
            user.functions[called](params)
        except Exception as e:
            if developerMode:
                console.print(f"Command failed → error {e}", style="red")
            else:
                console.print(f"Command does not exist", style="red")


if __name__ == "__main__":
    main()
