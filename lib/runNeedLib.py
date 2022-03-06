import os.path
import sys
from pathlib import Path


def getCurRunPath(filePath):
    if getattr(sys, 'frozen', False):
        # return Path(sys.executable).parent
        return os.path.dirname(sys.executable)

    elif __file__:
        # return Path(filePath).parent
        return os.path.dirname(filePath)
