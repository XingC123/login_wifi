import threading
import time
import webbrowser
from tkinter import *

import pyautogui
import pyperclip

import GUI.custom_messagebox as custom_messagebox
# XingC
# environment
import environment
import environment.config.main_config as main_config
# lib
import lib.necessary_lib as necessary_lib
import lib.stop_with_main_thread as stop_with_main_thread
import lib.tools as venusTools
# GUI
from GUI import get_xy_window
from environment.custom_constant import custom_constant


class MainWindow:
    width_root_window = 600
    height_root_window = 600

    def __init__(self, work_path):
        # 创建配置文件
        self.root_config = environment.config.main_config.MainConfig(work_path)

        # 是否正在执行login任务
        self.login_work_state = False

        # 主窗口
        self.root_window = Tk()

        # 主框架
        self.main_frame = Frame(self.root_window,
                                width=MainWindow.width_root_window,
                                height=MainWindow.height_root_window)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack()

        # 主frame的grid布局行号
        now_row = 0

        def currow():
            # 返回当前已使用的最大行号+1
            nonlocal now_row
            now_row += 1
            return now_row

        # 账号框
        account_frame = Frame(self.main_frame, bd=1, relief=GROOVE)
        account_frame.grid(row=currow(), column=0)
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
        password_frame.grid(row=currow(), column=0)
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
        login_frame.grid(row=currow(), column=0)
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
        webpath_frame.grid(row=currow(), column=0)
        Label(webpath_frame, text="网址").grid(row=0, column=0)
        self.webpath_text = Text(webpath_frame, height=1, width=30)
        self.webpath_text.grid(row=0, column=1)

        # 要打开的浏览器
        brower_name_frame = Frame(self.main_frame, bd=1, relief=GROOVE)
        brower_name_frame.grid(row=currow(), column=0)
        Label(brower_name_frame, text='登录所使用的浏览器的进程名').grid(row=0, column=0)
        self.brower_name_text = Text(brower_name_frame, width=20, height=1)
        self.brower_name_text.grid(row=0, column=1)
        Label(brower_name_frame, text='注: 可在任务管理器运行浏览器并查看').grid(row=1, column=0)

        # 立即登录
        Button(self.main_frame, text="登录", command=self.login_wifi_main).grid(row=currow(), column=0)

        # 自动执行
        auto_start_frame = Frame(self.main_frame)
        auto_start_frame.grid(row=currow(), column=0)
        self.auto_start_value_bool = BooleanVar()
        self.auto_start_value_bool.set(False)
        self.auto_start_checkbutton = Checkbutton(auto_start_frame, text="自动执行",
                                                  variable=self.auto_start_value_bool,
                                                  onvalue=True, offvalue=False)
        self.auto_start_checkbutton.grid(row=0, column=0)

        # 自动关闭窗口
        auto_close_window_frame = Frame(self.main_frame)
        auto_close_window_frame.grid(row=currow(), column=0)
        self.auto_close_window_value_bool = BooleanVar()
        self.auto_close_window_value_bool.set(False)
        self.auto_close_window_checkbutton = Checkbutton(auto_close_window_frame, text="自动关闭窗口",
                                                         variable=self.auto_close_window_value_bool,
                                                         onvalue=True, offvalue=False)
        self.auto_close_window_checkbutton.grid(row=0, column=0)

        # 守护进程
        guard_service_frame = Frame(self.main_frame)
        guard_service_frame.grid(row=currow(), column=0)
        self.guard_service_value_bool = BooleanVar()
        self.guard_service_value_bool.set(False)
        self.guard_service_checkbutton = Checkbutton(guard_service_frame, text='守护进程',
                                                     variable=self.guard_service_value_bool,
                                                     onvalue=True, offvalue=False)
        self.guard_service_checkbutton.grid(row=0, column=0)
        # 保存配置
        config_button_frame = Frame(self.main_frame)
        config_button_frame.grid(row=currow(), column=0)

        def save_config():
            try:
                self.save_config()
            except Exception as ex:
                print("出现如下异常: %s" % ex)
                custom_messagebox.CustomMessagebox(self.root_window, '保存配置', 300, 200, ['保存失败', '参数不能为空'])
            else:
                custom_messagebox.CustomMessagebox(self.root_window, '保存配置', 300, 200, ['保存成功'])

        Button(config_button_frame, text='保存到本地配置', command=save_config).grid(row=0, column=0)
        # 加载配置
        Button(config_button_frame, text='加载本地配置', command=self.load_config).grid(row=0, column=1)
        Button(config_button_frame, text='强制加载本地配置', command=self.force_load_config).grid(row=0, column=2)

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
        if venusTools.check_internet():
            webpath = self.webpath_text.get("0.0", END)
            if webpath != '':
                account = self.account_text.get("0.0", END)
                password = self.password_text.get("0.0", END)
                account_x = self.account_x_text.get(0.0, END)
                account_y = self.account_y_text.get(0.0, END)
                password_x = self.password_x_text.get(0.0, END)
                password_y = self.password_y_text.get(0.0, END)
                login_x = self.login_x_text.get(0.0, END)
                login_y = self.login_y_text.get(0.0, END)
                brower_name = self.brower_name_text.get(0.0, END)[::-1].replace('\r', '').replace('\n', '')[::-1]
                if account != '' and password != '' and \
                        account_x != '' and account_y != '' and \
                        password_x != '' and password_y != '' and \
                        login_x != '' and login_y != '' and \
                        brower_name != '':
                    # 标记login任务状态
                    self.login_work_state = True
                    # 打开网址
                    webbrowser.open(webpath)
                    while True:
                        if venusTools.proc_exist(brower_name):
                            time.sleep(10)
                            break
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

                    self.login_work_state = False
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

    def force_load_config(self):
        self.load_config('force')

    def load_config_main(self, mode):
        # 加载本地配置
        self.root_config.read_config()
        # 账号
        account = self.root_config.get_value(custom_constant.userconfig, custom_constant.account)
        account_x = self.root_config.get_value(custom_constant.userconfig, custom_constant.account_x)
        account_y = self.root_config.get_value(custom_constant.userconfig, custom_constant.account_y)
        # 密码
        password = self.root_config.get_value(custom_constant.userconfig, custom_constant.password)
        password_x = self.root_config.get_value(custom_constant.userconfig, custom_constant.password_x)
        password_y = self.root_config.get_value(custom_constant.userconfig, custom_constant.password_y)
        # 登录按钮
        login_x = self.root_config.get_value(custom_constant.userconfig, custom_constant.login_x)
        login_y = self.root_config.get_value(custom_constant.userconfig, custom_constant.login_y)
        # 自动执行
        autoStart = self.root_config.get_value(custom_constant.userconfig, custom_constant.autoStart)
        # 自动关闭
        autoClose = self.root_config.get_value(custom_constant.userconfig, custom_constant.autoClose)
        # 网址
        webpath = self.root_config.get_value(custom_constant.userconfig, custom_constant.webpath)
        # 守护进程
        guard_service = self.root_config.get_value(custom_constant.userconfig, custom_constant.guard_service)
        # 登录所使用的浏览器进程名
        brower_name = self.root_config.get_value(custom_constant.userconfig, custom_constant.brower_name)

        if mode == 'force' or account != '' and account_x != '' and account_y != '' and \
                password != '' and password_x != '' and password_y != '' and \
                login_x != '' and login_y != '' and \
                webpath != '' and \
                brower_name != '':
            try:
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
                MainWindow.set_value(self.brower_name_text, brower_name)
            except Exception as e:
                print('ERROR: 强制加载配置: ', end=', ')
                print(e)

            if mode == 'boot':
                if self.auto_start_value_bool.get():
                    time.sleep(5)
                    self.login_wifi()
        else:
            raise ValueError("参数不全")

    def save_config(self):
        # 保存配置
        account = self.account_text.get(0.0, END)
        account_x = self.account_x_text.get(0.0, END)
        account_y = self.account_y_text.get(0.0, END)
        password = self.password_text.get(0.0, END)
        password_x = self.password_x_text.get(0.0, END)
        password_y = self.password_y_text.get(0.0, END)
        login_x = self.login_x_text.get(0.0, END)
        login_y = self.login_y_text.get(0.0, END)
        webpath = self.webpath_text.get(0.0, END)
        brower_name = self.brower_name_text.get(0.0, END)

        if account != '' and account_x != '' and account_y != '' and \
                password != '' and password_x != '' and password_y != '' and \
                login_x != '' and login_y != '' and \
                webpath != '' and \
                brower_name != '':
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
            # 登录所使用的浏览器的名称
            self.root_config.set_value(custom_constant.userconfig, custom_constant.brower_name,
                                       brower_name)
        else:
            raise ValueError("参数不全")

    # 守护进程
    def guard_service(self):
        if self.guard_service_value_bool.get():
            # 若启用守护进程
            def guard_service():
                while True:
                    if not venusTools.check_internet() and not self.login_work_state:
                        self.login_wifi_main()
                    time.sleep(5)

            guard_service_thread = threading.Thread(target=guard_service)
            guard_service_thread.daemon = True
            guard_service_thread.start()

    @classmethod
    def set_value(cls, element, content):
        if str(type(element)) == "<class 'tkinter.Text'>":
            element.delete(0.0, END)
            element.insert(0.0, content)
        else:
            element.set(content)
