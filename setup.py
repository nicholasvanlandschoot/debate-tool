import os
from rich.console import Console
import subprocess
import sys



console = Console()

console.print("configuring debate-tool", style="blue")

if not os.path.exists("userdata"):
    os.mkdir("userdata")

if not os.path.exists("userdata/config.json"):
    open("userdata/config.json", "w")

if not os.path.exists("userdata/driveObjects.json"):
    open("userdata/driveObjects.json", "w")

console.print("finished config", style="green")