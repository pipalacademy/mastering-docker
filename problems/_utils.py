from pathlib import Path
import subprocess
import re
import os

def ok(title):
    print("✔", title)

def fail(title):
    print("✘", title)

def check_file(title, path, exists=True):
    path = Path(path)

    if exists == path.exists():
        ok(title)
    else:
        return fail(title)

def check_file_executable(title, path):
    if os.access(str(path), os.X_OK):
        ok(title)
    else:
        fail(title)

re_space = re.compile(" *$", re.M)

def trim(text):
    return re_space.sub("", text).strip()

def check_command_output(title, command, stdout=""):
    p = subprocess.Popen(command,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     text=True)
    p.wait()
    a = trim(p.stdout.read())
    b = trim(stdout.strip())
    if a == b:
        ok(title)
    else:
        fail(title)

