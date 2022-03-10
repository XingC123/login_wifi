import os.path
import sys


def getCurRunPath(filePath):
    if getattr(sys, 'frozen', False):
        # return Path(sys.executable).parent
        return os.path.dirname(sys.executable)

    elif __file__:
        # return Path(filePath).parent
        return os.path.dirname(filePath)


def generate_complete_filepath(dirname, filename):
    return os.path.join(dirname, filename)
