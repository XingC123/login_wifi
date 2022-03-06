from GUI.main_window import MainWindow
from lib import runNeedLib


def start_main_window():
    MainWindow(runNeedLib.getCurRunPath(__file__))


if __name__ == '__main__':
    start_main_window()
