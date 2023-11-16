"""Check if figlet is installed.
"""
from pathlib import Path

root = Path(__file__).parent.parent.absolute()
import sys
sys.path.append(str(root))

import _utils

_utils.check_file("Check cowsay command",path="/usr/games/cowsay")

HELLO = r"""
 _______
< hello >
 -------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
"""
_utils.check_command_output(
    title="/usr/games/cowsay hello",
    command=["/usr/games/cowsay", "hello"],
    stdout=HELLO)
