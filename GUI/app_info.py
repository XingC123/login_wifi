from GUI import custom_messagebox


def info_app_info_menu(window):
    width = 500
    height = 200
    msg_list = ['软件名: 自动登录', '版本: 2.1', '日期: 22.3.11', '作者: XingC',
                'github: https://github.com/XingC123/login_wifi',
                '声明: 仅做学习交流之用,因其他用法造成的一切问题本人概不负责']
    custom_messagebox.CustomMessagebox(window, '关于软件', width, height, msg_list)
