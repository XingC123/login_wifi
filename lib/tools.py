import psutil
import requests


def proc_exist(process_name):
    # 检测指定进程是否运行
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == process_name:
            return True
    return False


def check_internet():
    # 检测是否可以上网
    # url = "http://www.baidu.com"
    # try:
    #     status = urllib.urlopen(url).code
    #     print(status)
    # except:
    #     print({'result': 'false', 'msg': 'URL cannot access'})
    try:
        # html = requests.get("https://www.baidu.com", timeout=2)
        requests.get("https://www.baidu.com", timeout=2)
    except:
        print('无网络')
        return False
    else:
        print('有网络')
        return True


def str2int(string):
    if string != '':
        return int(string)
    else:
        return -1


if __name__ == '__main__':
    if proc_exist('qq.exe'):
        print('在运行')
    else:
        print('未找到')
