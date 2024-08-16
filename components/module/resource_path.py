"""
Path resource for executable - exe for Windows or etc
"""

import os
import sys

def resource_path(relative_path: os.PathLike[str]) -> os.PathLike[str]:

    """ Get absolute path to resource. """

    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)