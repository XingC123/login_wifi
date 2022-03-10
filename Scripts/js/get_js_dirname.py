from lib import runNeedLib


def get_js_dirname():
    # 返回js目录路径
    return runNeedLib.getCurRunPath(__file__)


def get_filepath_js_dir(filename):
    # 返回js目录下文件路径
    return runNeedLib.generate_complete_filepath(get_js_dirname(), filename)
