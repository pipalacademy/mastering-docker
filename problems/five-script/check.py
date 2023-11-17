from pathlib import Path

root = Path(__file__).parent.parent.absolute()
import sys
sys.path.append(str(root))

import _utils

_utils.check_file("five.sh exists", path="/home/pipal/five.sh")
_utils.check_file_executable("five.sh is executable", path="/home/pipal/five.sh")

OUTPUT = """
1
2
3
4
5
"""
_utils.check_command_output(
    title="Run five.sh",
    command=["/home/pipal/five.sh"],
    stdout=OUTPUT)
