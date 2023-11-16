"""Check if figlet is installed.
"""
from pathlib import Path

root = Path(__file__).parent.parent.absolute()
import sys
sys.path.append(str(root))

import _utils

_utils.check_file("Check figlet command",path="/usr/bin/figlet")

HELLO = r"""
 _          _ _
| |__   ___| | | ___
| '_ \ / _ \ | |/ _ \
| | | |  __/ | | (_) |
|_| |_|\___|_|_|\___/
"""
_utils.check_command_output(
    title="figlet hello",
    command=["figlet", "hello"],
    stdout=HELLO)
