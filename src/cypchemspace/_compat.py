"""Small runtime compatibility helpers."""

from __future__ import annotations


def avoid_windows_wmi_platform_probe() -> None:
    """Avoid slow Windows WMI platform probing during scientific imports.

    Some Python/Windows environments make ``platform.machine()`` call WMI, which
    can hang while importing pandas. The exact CPU string is irrelevant for this
    course package, so we provide a stable lightweight value before pandas is
    imported.
    """

    import platform
    import sys

    if sys.platform == "win32":
        platform.machine = lambda: "AMD64"
