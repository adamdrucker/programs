import os
import subprocess
from pathlib import Path
import shutil
import argparse

'''
TODO:
1. find large files, sort by size, log output
2. run a shell command, capture stdout/stderr, handles errors
'''

# cwd with os
project_path = os.getcwd()
#print(project_path)

my_home="/home/adam"
# this will include all hidden files
home_contents = os.listdir(my_home)
#print(home_contents)

# this is the syntax for running shell commands with subprocess
#subprocess.run(["df", "-h"])

target_dir = "/home/adam/Documents/pdf"
#os.system(f"du -ah {target_dir} | sort -rh")

# pathing with pathlib.Path
#print(Path.cwd())
my_cwd = Path.cwd()
my_home = Path.home()
print(f"my cwd: {my_cwd}", f"my home: {my_home}")

print(f"this file is located: {Path(__file__).parent}")
path = Path("/home/adam/programs/Python/refresh/week1/week1.py")
print(path.name)
