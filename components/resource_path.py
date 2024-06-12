"""
Katla resource for executable - exe for Windows
"""

import os
import sys

def resource_path(relative_path: str) -> str:

    """ Get absolute path to resource, works for dev and for PyInstaller """

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)