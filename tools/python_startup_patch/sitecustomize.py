"""Local startup patch for Windows Python environments with slow WMI probes.

Use only when a command such as pip or pytest hangs inside platform.uname().
Example:

PowerShell:
  $env:PYTHONPATH='tools/python_startup_patch'
  python -m pip install -e . --no-deps --no-build-isolation
"""

import collections
import platform
import sys

if sys.platform == "win32":
    platform.machine = lambda: "AMD64"
    platform.system = lambda: "Windows"
    platform.win32_ver = lambda *args, **kwargs: ("10", "10.0.0", "SP0", "Multiprocessor Free")
    Uname = collections.namedtuple("uname_result", "system node release version machine processor")
    platform.uname = lambda: Uname("Windows", "local", "10", "10.0.0", "AMD64", "AMD64")
