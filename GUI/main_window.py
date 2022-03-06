import threading
import time
import webbrowser
from tkinter import *

import pyautogui
import pyperclip
import requests

# XingC
# environment
import environment
import environment.config.main_config as main_config
from environment.custom_constant import custom_constant
# lib
import lib.necessary_lib as necessary_lib
import lib.stop_with_main_thread as stop_with_main_thread
# GUI
from GUI import get_xy_window
import GUI.custom_messagebox as custom_messagebox


class MainWindow:
    width_root_window = 600
    height_root_window = 500

    def __init__(self, work_path):
        # 创建配置文件
        self.root_config = environment.config.main_config.MainConfig(work_path)

        # 主窗口
        self.root_window = Tk()

        # 主框架
        self.main_frame = Frame(self.root_window,
                                width=MainWindow.width_root_window,
                                height=MainWindow.height_root_window)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack()

        # 账号框
        account_frame = Frame(self.main_frame, bd=1, relief=GROOVE)
        account_frame.grid(row=0, column=0)
        Label(account_frame, text="账号").grid(row=0, column=0)
        self.account_text = Text(account_frame, height=1, width=20)
        self.account_text.grid(row=0, column=1)
        # x坐标
        Label(account_frame, text='x坐标').grid(row=1, column=0)
        self.account_x_text = Text(account_frame, height=1, width=6)
        self.account_x_text.grid(row=1, column=1)
        # y坐标
        Label(account_frame, text='y坐标').grid(row=1, column=2)
        self.account_y_text = Text(account_frame, height=1, width=6)
        self.account_y_text.grid(row=1, column=3)

        def get_account_xy():
            self.get_xy(self.account_x_text, self.account_y_text)

        Button(account_frame, text='采集坐标', command=get_account_xy).grid(row=2, column=0)

        # 密码框
        password_frame = Frame(self.main_frame, bd=1, relief=GROOVE)
        password_frame.grid(row=1, column=0)
        Label(password_frame, text="密码").grid(row=0, column=0)
        self.password_text = Text(password_frame, height=1, width=20)
        self.password_text.grid(row=0, column=1)
        # x坐标
        Label(password_frame, text='x坐标').grid(row=1, column=0)
        self.password_x_text = Text(password_frame, height=1, width=6)
        self.password_x_text.grid(row=1, column=1)
        # y坐标
        Label(password_frame, text='y坐标').grid(row=1, column=2)
        self.password_y_text = Text(password_frame, height=1, width=6)
        self.password_y_text.grid(row=1, column=3)

        def get_password_xy():
            self.get_xy(self.password_x_text, self.password_y_text)

        Button(password_frame, text='采集坐标', command=get_password_xy).grid(row=2, column=0)

        # 登录按钮坐标
        login_frame = Frame(self.main_frame, bd=1, relief=GROOVE)
        login_frame.grid(row=2, column=0)
        Label(login_frame, text='登录按钮坐标').grid(row=0, column=0)
        # x坐标
        Label(login_frame, text='x坐标').grid(row=1, column=0)
        self.login_x_text = Text(login_frame, height=1, width=6)
        self.login_x_text.grid(row=1, column=1)
        # y坐标
        Label(login_frame, text='y坐标').grid(row=1, column=2)
        self.login_y_text = Text(login_frame, height=1, width=6)
        self.login_y_text.grid(row=1, column=3)

        def get_login_xy():
            self.get_xy(self.login_x_text, self.login_y_text)

        Button(login_frame, text='采集坐标', command=get_login_xy).grid(row=2, column=0)

        # 网址
        webpath_frame = Frame(self.main_frame)
        webpath_frame.grid(row=3, column=0)
        Label(webpath_frame, text="网址").grid(row=0, column=0)
        self.webpath_text = Text(webpath_frame, height=1, width=30)
        self.webpath_text.grid(row=0, column=1)

        # 立即登录
        Button(self.main_frame, text="登录", command=self.login_wifi_main).grid(row=4, column=0)

        # 自动执行
        auto_start_frame = Frame(self.main_frame)
        auto_start_frame.grid(row=5, column=0)
        self.auto_start_value_bool = BooleanVar()
        self.auto_start_value_bool.set(False)
        self.auto_start_checkbutton = Checkbutton(auto_start_frame, text="自动执行",
                                                  variable=self.auto_start_value_bool,
                                                  onvalue=True, offvalue=False)
        self.auto_start_checkbutton.grid(row=0, column=0)

        # 自动关闭窗口
        auto_close_window_frame = Frame(self.main_frame)
        auto_close_window_frame.grid(row=6, column=0)
        self.auto_close_window_value_bool = BooleanVar()
        self.auto_close_window_value_bool.set(False)
        self.auto_close_window_checkbutton = Checkbutton(auto_close_window_frame, text="自动关闭窗口",
                                                         variable=self.auto_close_window_value_bool,
                                                         onvalue=True, offvalue=False)
        self.auto_close_window_checkbutton.grid(row=0, column=0)

        # 守护进程
        guard_service_frame = Frame(self.main_frame)
        guard_service_frame.grid(row=7, column=0)
        self.guard_service_value_bool = BooleanVar()
        self.guard_service_value_bool.set(False)
        self.guard_service_checkbutton = Checkbutton(guard_service_frame, text='守护进程',
                                                     variable=self.guard_service_value_bool,
                                                     onvalue=True, offvalue=False)
        self.guard_service_checkbutton.grid(row=0, column=0)

        # 保存配置
        def save_config():
            try:
                self.save_config()
            except Exception as ex:
                print("出现如下异常: %s" % ex)
                custom_messagebox.CustomMessagebox(self.root_window, '保存配置', 300, 200, ['保存失败', '参数不能为空'])
            else:
                custom_messagebox.CustomMessagebox(self.root_window, '保存配置', 300, 200, ['保存成功'])

        Button(self.main_frame, text='保存到本地配置', command=save_config).grid(row=8, column=0)

        # 加载配置
        Button(self.main_frame, text='加载本地配置', command=self.load_config).grid(row=8, column=1)

        # 界面初始化
        self.init_root_window()

        # 配置初始化
        def init_config():
            event = threading.Event()

            def stop_work():
                if event.is_set() is False:
                    stop_with_main_thread.stop_thread(execute_thread)

            def check_finish():
                event.wait()

            def execute_work():
                self.load_config('boot')
                event.set()

            def tip_window():
                custom_messagebox.CustomMessagebox(self.root_window, '正在自动执行设定的任务', 400, 200, ['将在5s后执行'],
                                                   True, check_finish, True, event, stop_work)

            execute_thread = threading.Thread(target=execute_work)

            threading.Thread(target=tip_window).start()
            execute_thread.start()

        load_config_thread = threading.Thread(target=init_config)
        load_config_thread.daemon = True
        load_config_thread.start()

        self.root_window.mainloop()

    # 方法
    def init_root_window(self):
        # 初始化主窗口
        necessary_lib.fit_screen_zoom(self.root_window)
        self.root_window.title('wifi登录')
        self.root_window.geometry(necessary_lib.middle_screen(self.root_window,
                                                              MainWindow.width_root_window,
                                                              MainWindow.height_root_window))
        self.root_window.resizable(False, False)

    def login_wifi(self):
        self.login_wifi_main()

        # 守护进程
        self.guard_service()

    def login_wifi_main(self):
        if not MainWindow.check_internet():
            webpath = self.webpath_text.get("0.0", END).lstrip()
            if webpath != '':
                account = self.account_text.get("0.0", END).lstrip()
                password = self.password_text.get("0.0", END).lstrip()
                account_x = self.account_x_text.get(0.0, END).lstrip()
                account_y = self.account_y_text.get(0.0, END).lstrip()
                password_x = self.password_x_text.get(0.0, END).lstrip()
                password_y = self.password_y_text.get(0.0, END).lstrip()
                login_x = self.login_x_text.get(0.0, END).lstrip()
                login_y = self.login_y_text.get(0.0, END).lstrip()
                if account != '' and password != '' and \
                        account_x != '' and account_y != '' and \
                        password_x != '' and password_y != '' and \
                        login_x != '' and login_y != '':
                    # 打开网址
                    webbrowser.open(webpath)
                    time.sleep(5)

                    # 输入账号
                    pyautogui.click(int(account_x), int(account_y))
                    pyperclip.copy(account)
                    time.sleep(5)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(5)

                    # 点击其他地方
                    pyautogui.click(10, 400)
                    time.sleep(2)

                    # 输入密码
                    pyautogui.click(int(password_x), int(password_y))
                    pyperclip.copy(password)
                    time.sleep(5)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(5)

                    # 点击登录
                    pyautogui.click(int(login_x), int(login_y))

                    #
                    pyperclip.copy('自动登录')

                    # 自动关闭窗口
                    if self.auto_close_window_value_bool.get():
                        self.root_window.destroy()
        else:
            custom_messagebox.CustomMessagebox(self.root_window, "连接wifi", 300, 200, ['已连接网络, 无需重复认证'])

    def get_xy(self, x_element, y_element):
        get_xy_window.GetXY(self.root_window, x_element, y_element)

    def load_config(self, mode='normal'):
        try:
            self.load_config_main(mode)
        except Exception as ex:
            print("出现如下异常: %s" % ex)
            custom_messagebox.CustomMessagebox(self.root_window, '加载配置', 300, 200, ['加载失败', '配置文件损坏, 所需参数丢失'])
        else:
            if not self.auto_start_value_bool.get():
                # 如果不需要自动登录, 则显示加载结果
                custom_messagebox.CustomMessagebox(self.root_window, '加载配置', 300, 200, ['加载成功'])

    def load_config_main(self, mode):
        # 加载本地配置
        self.root_config.read_config()
        # 账号
        account = self.root_config.get_value(custom_constant.userconfig, custom_constant.account).lstrip()
        account_x = self.root_config.get_value(custom_constant.userconfig, custom_constant.account_x).lstrip()
        account_y = self.root_config.get_value(custom_constant.userconfig, custom_constant.account_y).lstrip()
        # 密码
        password = self.root_config.get_value(custom_constant.userconfig, custom_constant.password).lstrip()
        password_x = self.root_config.get_value(custom_constant.userconfig, custom_constant.password_x).lstrip()
        password_y = self.root_config.get_value(custom_constant.userconfig, custom_constant.password_y).lstrip()
        # 登录按钮
        login_x = self.root_config.get_value(custom_constant.userconfig, custom_constant.login_x).lstrip()
        login_y = self.root_config.get_value(custom_constant.userconfig, custom_constant.login_y).lstrip()
        # 自动执行
        autoStart = self.root_config.get_value(custom_constant.userconfig, custom_constant.autoStart).lstrip()
        # 自动关闭
        autoClose = self.root_config.get_value(custom_constant.userconfig, custom_constant.autoClose).lstrip()
        # 网址
        webpath = self.root_config.get_value(custom_constant.userconfig, custom_constant.webpath).lstrip()
        # 守护进程
        guard_service = self.root_config.get_value(custom_constant.userconfig, custom_constant.guard_service).lstrip()

        if account != '' and account_x != '' and account_y != '' and \
                password != '' and password_x != '' and password_y != '' and \
                login_x != '' and login_y != '' and \
                webpath != '':
            MainWindow.set_value(self.account_text, account)
            MainWindow.set_value(self.account_x_text, account_x)
            MainWindow.set_value(self.account_y_text, account_y)
            MainWindow.set_value(self.password_text, password)
            MainWindow.set_value(self.password_x_text, password_x)
            MainWindow.set_value(self.password_y_text, password_y)
            MainWindow.set_value(self.login_x_text, login_x)
            MainWindow.set_value(self.login_y_text, login_y)
            MainWindow.set_value(self.auto_start_value_bool, autoStart)
            MainWindow.set_value(self.auto_close_window_value_bool, autoClose)
            MainWindow.set_value(self.webpath_text, webpath)
            MainWindow.set_value(self.guard_service_value_bool, guard_service)

            if mode == 'boot':
                if self.auto_start_value_bool.get():
                    time.sleep(5)
                    self.login_wifi()
        else:
            raise ValueError("参数不全")

    def save_config(self):
        # 保存配置
        account = self.account_text.get(0.0, END).lstrip()
        account_x = self.account_x_text.get(0.0, END).lstrip()
        account_y = self.account_y_text.get(0.0, END).lstrip()
        password = self.password_text.get(0.0, END).lstrip()
        password_x = self.password_x_text.get(0.0, END).lstrip()
        password_y = self.password_y_text.get(0.0, END).lstrip()
        login_x = self.login_x_text.get(0.0, END).lstrip()
        login_y = self.login_y_text.get(0.0, END).lstrip()
        webpath = self.webpath_text.get(0.0, END).lstrip()

        if account != '' and account_x != '' and account_y != '' and \
                password != '' and password_x != '' and password_y != '' and \
                login_x != '' and login_y != '' and \
                webpath != '':
            # 账号
            self.root_config.set_value(custom_constant.userconfig, custom_constant.account, account)
            self.root_config.set_value(custom_constant.userconfig, custom_constant.account_x, account_x)
            self.root_config.set_value(custom_constant.userconfig, custom_constant.account_y, account_y)
            # 密码
            self.root_config.set_value(custom_constant.userconfig, custom_constant.password, password)
            self.root_config.set_value(custom_constant.userconfig, custom_constant.password_x, password_x)
            self.root_config.set_value(custom_constant.userconfig, custom_constant.password_y, password_y)
            # 登录按钮
            self.root_config.set_value(custom_constant.userconfig, custom_constant.login_x, login_x)
            self.root_config.set_value(custom_constant.userconfig, custom_constant.login_y, login_y)
            # 自动执行
            self.root_config.set_value(custom_constant.userconfig, custom_constant.autoStart,
                                       self.auto_start_value_bool.get())
            # 自动关闭
            self.root_config.set_value(custom_constant.userconfig, custom_constant.autoClose,
                                       self.auto_close_window_value_bool.get())
            # 网址
            self.root_config.set_value(custom_constant.userconfig, custom_constant.webpath,
                                       webpath)
            # 守护进程
            self.root_config.set_value(custom_constant.userconfig, custom_constant.guard_service,
                                       self.guard_service_value_bool.get())
        else:
            raise ValueError("参数不全")

    # 守护进程
    def guard_service(self):
        if self.guard_service_value_bool.get():
            # 若启用守护进程
            def guard_service():
                while True:
                    if not MainWindow.check_internet():
                        self.login_wifi_main()
                    time.sleep(5)

            guard_service_thread = threading.Thread(target=guard_service)
            guard_service_thread.daemon = True
            guard_service_thread.start()

    @classmethod
    def check_internet(cls):
        # 网络检测
        # url = "http://www.baidu.com"
        # try:
        #     status = urllib.urlopen(url).code
        #     print(status)
        # except:
        #     print({'result': 'false', 'msg': 'URL cannot access'})
        try:
            html = requests.get("https://www.baidu.com", timeout=2)
        except:
            print('无网络')
            return False
        else:
            print('有网络')
            return True

    @classmethod
    def set_value(cls, element, content):
        if str(type(element)) == "<class 'tkinter.Text'>":
            element.delete(0.0, END)
            element.insert(0.0, content)
        else:
            element.set(content)
