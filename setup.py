import os
from rich.console import Console

console = Console()

console.print("configuring debate-tool", style="blue")

if not os.path.exists("userdata"):
    os.mkdir("userdata")

if not os.path.exists("userdata/config.json"):
    open("userdata/config.json", "w")

console.print("finished config", style="green")
