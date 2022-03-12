from GUI import custom_messagebox


def info_app_info_menu(window):
    width = 500
    height = 200
    '''
    version: 第1位: 大版本号
             第2位: 小版本号
             第3位: 面向用户性commit次数 (不包括"更新版本号"之类的commit)
             括号: 总发布版本数 (从 2022-3-11 加入此规则, 遂从这一次版本开始计算)
    '''
    version = '版本: 2.1.8 (3)'
    msg_list = ['软件名: 自动登录', version, '日期: 22.3.11', '作者: XingC',
                'github: https://github.com/XingC123/login_wifi',
                '声明: 仅做学习交流之用,因其他用法造成的一切问题本人概不负责']
    custom_messagebox.CustomMessagebox(window, '关于软件', width, height, msg_list)
