import os
import subprocess
import sys


print("configuring debate-tool")

os.system("python3 -m venv venv")

while True:
    try:
        os.system("./venv/bin/python3 -m pip install --upgrade pip")
        os.system("./venv/bin/pip3 install -r requirements.txt")
        break
    except:
        pass

if not os.path.exists("userdata"):
    os.mkdir("userdata")

if not os.path.exists("userdata/config.json"):
    with open("userdata/config.json", "w") as f:
        f.write("{}")

if not os.path.exists("userdata/driveObjects.json"):
    with open("userdata/driveObjects.json", "w") as f:
        f.write("{}")

if not os.path.exists("userdata/snippets.json"):
    with open("userdata/snippets.json", "w") as f:
        f.write("{}")


print("finished config")
print("move into vitrual enviroment: source ./venv/bin/activate")