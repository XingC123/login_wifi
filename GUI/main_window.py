import threading
import time
import tkinter.filedialog
import webbrowser
from tkinter import *
from tkinter import ttk

import pyautogui
import pyperclip

# XingC
# environment
import environment
import environment.config.main_config as main_config
import environment.custom_constant.custom_constant as custom_constant
# lib
import lib.necessary_lib as necessary_lib
import lib.stop_with_main_thread as stop_with_main_thread
import lib.tools as venusTools
from lib.custom_config_object import AlphaLoginObject, NormalLoginObject
# GUI
import GUI.app_info
import GUI.get_xy_window as get_xy_window
import GUI.custom_messagebox as custom_messagebox
# func
from func.login.login_webdriver import Login


class MainWindow:
    width_root_window = 1000
    height_root_window = 600

    def __init__(self, work_path):
        # 创建配置文件
        self.root_config = environment.config.main_config.MainConfig(work_path)
        self.work_path = work_path

        # 窗口内元素配置对象
        self.normal_object = None
        self.alpha_object = None

        # 是否正在执行login任务
        self.login_work_state = False

        # 主窗口
        self.root_window = Tk()
        # 菜单
        self.menubar = Menu(self.root_window)

        # 主框架
        self.root_frame = Frame(self.root_window,
                                width=MainWindow.width_root_window,
                                height=MainWindow.height_root_window)
        self.root_frame.pack_propagate(False)
        self.root_frame.pack()
        # 框架1
        self.main_frame1 = Frame(self.root_frame,
                                 width=MainWindow.width_root_window / 2,
                                 height=MainWindow.height_root_window)
        self.main_frame1.pack_propagate(False)
        self.main_frame1.pack(side=LEFT)
        # 框架2
        self.main_frame2 = Frame(self.root_frame,
                                 width=MainWindow.width_root_window / 2,
                                 height=MainWindow.height_root_window)
        self.main_frame2.pack_propagate(False)
        self.main_frame2.pack(side=LEFT)

        # 主frame的grid布局行号
        now_row_frame1 = 0
        now_row_frame2 = 0

        def currow_frame1():
            # 返回当前已使用的最大行号+1
            nonlocal now_row_frame1
            now_row_frame1 += 1
            return now_row_frame1

        def currow_frame2():
            # 返回当前已使用的最大行号+1
            nonlocal now_row_frame2
            now_row_frame2 += 1
            return now_row_frame2

        # 运行模式
        work_mode_frame = Frame(self.main_frame1, bd=1, relief=GROOVE)
        work_mode_frame.grid(row=currow_frame1(), column=0)
        self.all_work_mode = [1, 2]  # 所有运行模式
        self.work_mode_value_int = IntVar()
        self.work_mode_value_int.set(1)
        Label(work_mode_frame, text='运行模式').grid(row=0, column=0, columnspan=2)
        self.work_mode_stable_checkbutton = Checkbutton(work_mode_frame, text='稳定模式',
                                                        variable=self.work_mode_value_int,
                                                        onvalue=1,
                                                        command=self.load_element_by_mode)
        self.work_mode_stable_checkbutton.grid(row=1, column=0)
        self.work_mode_ALPHA_checkbutton = Checkbutton(work_mode_frame, text='ALPHA模式',
                                                       variable=self.work_mode_value_int,
                                                       onvalue=2,
                                                       command=self.load_element_by_mode)
        self.work_mode_ALPHA_checkbutton.grid(row=1, column=1)
        work_mode_tip_frame = Frame(work_mode_frame)
        work_mode_tip_frame.grid(row=2, column=0, columnspan=2)
        Label(work_mode_tip_frame, text='注意事项:').grid(row=0, column=0, columnspan=2)
        Label(work_mode_tip_frame, text='1. 账号+密码+网址 为所有模式必须。').grid(row=1, column=0)
        Label(work_mode_tip_frame, text='2. 带 * 号为 ALPHA模式 必须，其他模式可不填。').grid(row=2, column=0)
        Label(work_mode_tip_frame, text='3. 其余未标注项为 稳定模式 必须').grid(row=3, column=0)
        Label(work_mode_tip_frame, text='4. 若使用 稳定模式 ，推荐保留默认浏览器后台。').grid(row=4, column=0)

        # 账号框
        account_frame = Frame(self.main_frame1, bd=1, relief=GROOVE)
        account_frame.grid(row=currow_frame1(), column=0)
        Label(account_frame, text="* 账号").grid(row=0, column=0)
        self.account_text = Text(account_frame, height=1, width=20)
        self.account_text.grid(row=0, column=1, columnspan=3)
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

        Button(account_frame, text='采集坐标', command=get_account_xy).grid(row=2, column=0, columnspan=4)

        # 密码框
        password_frame = Frame(self.main_frame1, bd=1, relief=GROOVE)
        password_frame.grid(row=currow_frame1(), column=0)
        Label(password_frame, text="* 密码").grid(row=0, column=0)
        self.password_text = Text(password_frame, height=1, width=20)
        self.password_text.grid(row=0, column=1, columnspan=3)
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

        Button(password_frame, text='采集坐标', command=get_password_xy).grid(row=2, column=0, columnspan=4)

        # 登录按钮坐标
        login_frame = Frame(self.main_frame1, bd=1, relief=GROOVE)
        login_frame.grid(row=currow_frame1(), column=0)
        Label(login_frame, text='登录按钮坐标').grid(row=0, column=0, columnspan=4)
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

        Button(login_frame, text='采集坐标', command=get_login_xy).grid(row=2, column=0, columnspan=4)

        # 网址
        webpath_frame = Frame(self.main_frame1)
        webpath_frame.grid(row=currow_frame1(), column=0)
        Label(webpath_frame, text="* 网址").grid(row=0, column=0)
        self.webpath_text = Text(webpath_frame, height=3, width=30)
        self.webpath_text.grid(row=0, column=1)

        # 要打开的浏览器
        brower_name_frame = Frame(self.main_frame1, bd=1, relief=GROOVE)
        brower_name_frame.grid(row=currow_frame1(), column=0)
        Label(brower_name_frame, text='登录所使用的浏览器的进程名').grid(row=0, column=0)
        self.brower_name_text = Text(brower_name_frame, width=20, height=1)
        self.brower_name_text.grid(row=0, column=1)
        Label(brower_name_frame, text='注: 可在任务管理器运行浏览器并查看').grid(row=1, column=0, columnspan=2)

        # 浏览器驱动
        webdriver_frame = Frame(self.main_frame2, bd=1, relief=GROOVE)
        webdriver_frame.grid(row=currow_frame2(), column=0)
        Label(webdriver_frame, text='ALPHA模式 专属参数项').grid(row=0, column=0, columnspan=3, pady=5)
        Label(webdriver_frame, text='* 浏览器驱动类型').grid(row=1, column=0)
        self.webdriver_type_value_str = StringVar()
        self.webdriver_type_value_str.set('Microsoft edge Chromium')
        self.webdriver_type_list = ['Microsoft edge Chromium', 'Microsoft edge Chromium 80 以下', 'Chrome', 'Firefox']
        self.webdriver_type_combobox = ttk.Combobox(webdriver_frame, height=4, width=40, state='readonly',
                                                    textvariable=self.webdriver_type_value_str,
                                                    values=self.webdriver_type_list)
        self.webdriver_type_combobox.grid(row=1, column=1)
        Label(webdriver_frame, text='注: 驱动版本要与浏览器版本相对应 (也许可相差个别小版本。自测~)').grid(row=2, column=0, columnspan=3)
        Label(webdriver_frame, text='* 浏览器驱动地址').grid(row=3, column=0)
        self.webdriver_path_text = Text(webdriver_frame, height=3, width=30)
        self.webdriver_path_text.grid(row=3, column=1)

        def choose_file():
            MainWindow.choose_file(self.webdriver_path_text)

        Button(webdriver_frame, text='打开', command=choose_file).grid(row=3, column=2)
        Label(webdriver_frame, text='注: 以下id请自行从html源代码查找').grid(row=4, column=0, columnspan=4)
        Label(webdriver_frame, text='* 账号框id').grid(row=5, column=0)
        self.account_id_text = Text(webdriver_frame, height=1, width=30)
        self.account_id_text.grid(row=5, column=1)
        Label(webdriver_frame, text='* 密码框id').grid(row=6, column=0)
        self.password_id_text = Text(webdriver_frame, height=1, width=30)
        self.password_id_text.grid(row=6, column=1)
        Label(webdriver_frame, text='* 登录框id').grid(row=7, column=0)
        self.login_id_text = Text(webdriver_frame, height=1, width=30)
        self.login_id_text.grid(row=7, column=1)
        Label(webdriver_frame, text='注: FireFox无防御脚本, 你可能会被网站检测从而无法登录').grid(row=8, column=0, columnspan=4)

        # 立即登录
        Button(self.main_frame2, text="登录", command=self.login_wifi).grid(row=currow_frame2(), column=0)

        # 自动执行
        auto_start_frame = Frame(self.main_frame2)
        auto_start_frame.grid(row=currow_frame2(), column=0)
        self.auto_start_value_bool = BooleanVar()
        self.auto_start_value_bool.set(False)
        self.auto_start_checkbutton = Checkbutton(auto_start_frame, text="自动执行",
                                                  variable=self.auto_start_value_bool,
                                                  onvalue=True, offvalue=False)
        self.auto_start_checkbutton.grid(row=0, column=0)

        # 自动关闭窗口
        auto_close_window_frame = Frame(self.main_frame2)
        auto_close_window_frame.grid(row=currow_frame2(), column=0)
        self.auto_close_window_value_bool = BooleanVar()
        self.auto_close_window_value_bool.set(False)
        self.auto_close_window_checkbutton = Checkbutton(auto_close_window_frame, text="自动关闭窗口",
                                                         variable=self.auto_close_window_value_bool,
                                                         onvalue=True, offvalue=False)
        self.auto_close_window_checkbutton.grid(row=0, column=0)

        # 守护进程
        guard_service_frame = Frame(self.main_frame2)
        guard_service_frame.grid(row=currow_frame2(), column=0)
        self.guard_service_value_bool = BooleanVar()
        self.guard_service_value_bool.set(False)
        self.guard_service_checkbutton = Checkbutton(guard_service_frame, text='守护进程 (若要操作计算机, 请勿开启)',
                                                     variable=self.guard_service_value_bool,
                                                     onvalue=True, offvalue=False)
        self.guard_service_checkbutton.grid(row=0, column=0)
        Label(guard_service_frame, text='(关闭主程序才能关闭守护进程)').grid(row=1, column=0)
        # 保存配置
        config_button_frame = Frame(self.main_frame2)
        config_button_frame.grid(row=currow_frame2(), column=0)

        def save_config():
            try:
                self.save_config()
            except Exception as ex:
                print("__init__: save_config(): 出现如下异常: %s" % ex)
                custom_messagebox.CustomMessagebox(self.root_window, '保存配置', 300, 200, ['保存失败, 参数不能为空'], True)
            else:
                custom_messagebox.CustomMessagebox(self.root_window, '保存配置', 300, 200, ['保存成功'], True)

        Button(config_button_frame, text='保存到本地配置', command=save_config).grid(row=0, column=0)
        # 加载配置
        Button(config_button_frame, text='加载本地配置', command=self.load_config).grid(row=0, column=1)
        Button(config_button_frame, text='强制加载本地配置', command=self.force_load_config).grid(row=0, column=2)

        # 界面初始化
        self.init_all_elements_in_window()

        # 配置初始化
        def init_config():
            self.load_config('boot')

        load_config_thread = threading.Thread(target=init_config)
        load_config_thread.daemon = True
        load_config_thread.start()

        self.root_window.config(menu=self.menubar)
        self.root_window.mainloop()

    # 方法
    # 窗口控件
    def init_root_window(self):
        # 初始化主窗口
        necessary_lib.fit_screen_zoom(self.root_window)
        self.root_window.title('wifi登录')
        self.root_window.geometry(necessary_lib.middle_screen(self.root_window,
                                                              MainWindow.width_root_window,
                                                              MainWindow.height_root_window))
        # self.root_window.resizable(False, False)  # 禁用窗口大小调整
        self.root_window.minsize(MainWindow.width_root_window, MainWindow.height_root_window)
        self.root_window.maxsize(int(MainWindow.width_root_window * 1.5), int(MainWindow.height_root_window * 1.5))

    def init_all_elements_in_window(self):
        # 初始化主窗口
        self.init_root_window()
        # 初始化菜单
        self.init_root_window_menu()
        # 根据工作模式初始化其他部件
        self.load_element_by_mode()

    def init_root_window_menu(self):
        info_menu = Menu(self.menubar, tearoff=False)

        def app_info():
            GUI.app_info.info_app_info_menu(self.root_window)

        info_menu.add_command(label='关于软件', command=app_info)

        self.menubar.add_cascade(label='关于', menu=info_menu)

    def load_element_by_mode(self):
        work_mode = self.work_mode_value_int.get()
        if work_mode == 1:
            # 账号
            self.account_x_text['state'] = NORMAL
            self.account_y_text['state'] = NORMAL
            # 密码
            self.password_x_text['state'] = NORMAL
            self.password_y_text['state'] = NORMAL
            # 登录按钮
            self.login_x_text['state'] = NORMAL
            self.login_y_text['state'] = NORMAL
            # 登录所使用的浏览器名称
            self.brower_name_text['state'] = NORMAL
        elif work_mode == 2:
            # 账号
            self.account_x_text['state'] = DISABLED
            self.account_y_text['state'] = DISABLED
            # 密码
            self.password_x_text['state'] = DISABLED
            self.password_y_text['state'] = DISABLED
            # 登录按钮
            self.login_x_text['state'] = DISABLED
            self.login_y_text['state'] = DISABLED
            # 登录所使用的浏览器名称
            self.brower_name_text['state'] = DISABLED
            # 弹窗提示
            custom_messagebox.CustomMessagebox(self.root_window, 'ALPHA模式 说明', 400, 300,
                                               ['ALPHA模式 目前尚不完善, 在执行 login 后会自动结束任务而不会返回任何结果。请确保你的账号以及密码正确无误!'],
                                               True)

    # 其他方法
    def get_cur_work_mode(self):
        # 返回当前工作模式
        return self.work_mode_value_int.get()

    def generate_object(self, work_mode):
        # 生成登录对象
        try:
            if work_mode == 1:
                if self.alpha_object is not None:
                    self.alpha_object = None
                # 创建 普通模式 配置对象
                self.normal_object = NormalLoginObject()
                # 生成
                self.normal_object.set_normal_object(
                    self.account_text.get(0.0, END)[:-1], self.account_x_text.get(0.0, END)[:-1],
                    self.account_y_text.get(0.0, END)[:-1],
                    self.password_text.get(0.0, END)[:-1], self.password_x_text.get(0.0, END)[:-1],
                    self.password_y_text.get(0.0, END)[:-1],
                    self.login_x_text.get(0.0, END)[:-1], self.login_y_text.get(0.0, END)[:-1],
                    self.brower_name_text.get(0.0, END)[:-1], self.webpath_text.get(0.0, END)[:-1], work_mode,
                    self.auto_start_value_bool.get(), self.auto_close_window_value_bool.get(),
                    self.guard_service_value_bool.get()
                )
            elif work_mode == 2:
                if self.normal_object is not None:
                    self.normal_object = None
                # 创建 ALPHA模式 配置对象
                self.alpha_object = AlphaLoginObject()
                # 生成
                self.alpha_object.set_alpha_object(
                    self.account_text.get(0.0, END)[:-1], self.password_text.get(0.0, END)[:-1],
                    self.webpath_text.get(0.0, END)[:-1], work_mode,
                    self.webdriver_type_combobox.get(), self.webdriver_path_text.get(0.0, END)[:-1],
                    self.account_id_text.get(0.0, END)[:-1], self.password_id_text.get(0.0, END)[:-1],
                    self.login_id_text.get(0.0, END)[:-1],
                    self.auto_start_value_bool.get(), self.auto_close_window_value_bool.get(),
                    self.guard_service_value_bool.get()
                )
        except:
            raise ValueError('generate_object(self): 生成对象失败')

    def login_wifi(self, mode='normal'):
        def login():
            if mode == 'boot':
                time.sleep(5)
            try:
                self.login_wifi_main()
            except Exception as e:
                print('login_wifi(self): ', end='')
                print(e)

        def stop_work():
            stop_with_main_thread.stop_thread(tip_thread)

        def tip_window():
            if mode == 'boot':
                tip_title = '正在自动执行设定的任务'
                tip = '将在5s后执行'
            else:
                tip_title = '执行任务'
                tip = '正在执行...'

            custom_messagebox.CustomMessagebox(self.root_window, tip_title, 400, 200, [tip],
                                               True, login, True, stop_work)

        tip_thread = threading.Thread(target=tip_window)
        tip_thread.daemon = True
        tip_thread.start()

        # 守护进程
        self.guard_service()

    def login_wifi_main(self):
        if not venusTools.check_internet():
            # 标记login任务状态
            self.login_work_state = True
            if self.get_cur_work_mode() == 1:
                if self.normal_object is None:
                    self.generate_object(self.get_cur_work_mode())
                # 打开网址
                webbrowser.open(self.normal_object.normal_object[custom_constant.func_object][custom_constant.webpath])
                while True:
                    if venusTools.proc_exist(self.normal_object.normal_object[custom_constant.brower_name]):
                        time.sleep(20)
                        break
                    time.sleep(5)

                # 输入账号
                pyautogui.click(int(self.normal_object.normal_object[custom_constant.account_x]),
                                int(self.normal_object.normal_object[custom_constant.account_y]))
                pyperclip.copy(self.normal_object.normal_object[custom_constant.account])
                time.sleep(5)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(5)

                # 点击其他地方
                pyautogui.click(10, 400)
                time.sleep(2)

                # 输入密码
                pyautogui.click(int(self.normal_object.normal_object[custom_constant.password_x]),
                                int(self.normal_object.normal_object[custom_constant.password_y]))
                pyperclip.copy(self.normal_object.normal_object[custom_constant.password])
                time.sleep(5)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(5)

                # 点击登录
                pyautogui.click(int(self.normal_object.normal_object[custom_constant.login_x]),
                                int(self.normal_object.normal_object[custom_constant.login_y]))

                #
                pyperclip.copy('自动登录')
            elif self.get_cur_work_mode() == 2:
                if self.alpha_object is None:
                    self.generate_object(self.get_cur_work_mode())
                Login(self.alpha_object.alpha_object, self.work_path).run()

            # 自动关闭窗口
            if self.auto_close_window_value_bool.get():
                self.root_window.destroy()

            self.login_work_state = False
        else:
            custom_messagebox.CustomMessagebox(self.root_window, "连接wifi", 300, 200, ['已连接网络, 无需重复认证'], True)

    def get_xy(self, x_element, y_element):
        get_xy_window.GetXY(self.root_window, x_element, y_element)

    def load_config(self, mode='normal'):
        try:
            self.load_config_main(mode)
        except Exception as ex:
            print("load_config(self, mode='normal'): 出现如下异常: %s" % ex)
            custom_messagebox.CustomMessagebox(self.root_window, '加载配置', 300, 200, ['加载失败, 配置文件损坏, 所需参数丢失'], True)
        else:
            if mode == 'boot':
                if self.auto_start_value_bool.get():
                    # time.sleep(5)
                    self.login_wifi(mode)
            if not self.auto_start_value_bool.get():
                # 如果不需要自动登录, 则显示加载结果
                custom_messagebox.CustomMessagebox(self.root_window, '加载配置', 300, 200, ['加载成功'], True)

    def force_load_config(self):
        self.load_config('force')

    def load_config_main(self, mode):
        # 加载本地配置
        self.root_config.read_config()
        # 工作模式
        work_mode = venusTools.str2int(self.root_config.get_value(custom_constant.userconfig,
                                                                  custom_constant.work_mode))
        print('load_config_main(self, mode): workmode = [', work_mode, ']')
        if work_mode in self.all_work_mode:
            if work_mode == 1:
                self.normal_object = NormalLoginObject()
                self.normal_object.normal_object = eval(
                    self.root_config.get_value(custom_constant.userconfig, custom_constant.normal_object))
                if mode == 'force' or self.normal_object.check_config():
                    # 账号
                    MainWindow.set_value(self.account_text,
                                         self.normal_object.normal_object[custom_constant.account])
                    MainWindow.set_value(self.account_x_text,
                                         self.normal_object.normal_object[custom_constant.account_x])
                    MainWindow.set_value(self.account_y_text,
                                         self.normal_object.normal_object[custom_constant.account_y])
                    # 密码
                    MainWindow.set_value(self.password_text,
                                         self.normal_object.normal_object[custom_constant.password])
                    MainWindow.set_value(self.password_x_text,
                                         self.normal_object.normal_object[custom_constant.password_x])
                    MainWindow.set_value(self.password_y_text,
                                         self.normal_object.normal_object[custom_constant.password_y])
                    # 登录
                    MainWindow.set_value(self.login_x_text,
                                         self.normal_object.normal_object[custom_constant.login_x])
                    MainWindow.set_value(self.login_y_text,
                                         self.normal_object.normal_object[custom_constant.login_y])
                    # 浏览器进程名
                    MainWindow.set_value(self.brower_name_text,
                                         self.normal_object.normal_object[custom_constant.brower_name])
                    # 基础功能
                    # 网址
                    MainWindow.set_value(self.webpath_text,
                                         self.normal_object.normal_object[custom_constant.func_object][
                                             custom_constant.webpath])
                    # 工作模式
                    MainWindow.set_value(self.work_mode_value_int,
                                         work_mode)
                    # 自动关闭
                    MainWindow.set_value(self.auto_close_window_value_bool,
                                         self.normal_object.normal_object[custom_constant.func_object][
                                             custom_constant.autoClose])
                    # 自动执行
                    MainWindow.set_value(self.auto_start_value_bool,
                                         self.normal_object.normal_object[custom_constant.func_object][
                                             custom_constant.autoStart])
                    # 守护进程
                    MainWindow.set_value(self.guard_service_value_bool,
                                         self.normal_object.normal_object[custom_constant.func_object][
                                             custom_constant.guard_service])
                else:
                    raise ValueError('load_config_main(self, mode): 配置损坏')
            elif work_mode == 2:
                self.alpha_object = AlphaLoginObject()
                self.alpha_object.alpha_object = eval(
                    self.root_config.get_value(custom_constant.userconfig, custom_constant.alpha_object))
                if mode == 'force' or self.alpha_object.check_config():
                    # 账号
                    MainWindow.set_value(self.account_text,
                                         self.alpha_object.alpha_object[custom_constant.account])
                    # 密码
                    MainWindow.set_value(self.password_text,
                                         self.alpha_object.alpha_object[custom_constant.password])
                    # 浏览器驱动地址
                    MainWindow.set_value(self.webdriver_path_text,
                                         self.alpha_object.alpha_object[custom_constant.webdriver_path])
                    # 浏览器类型
                    if self.alpha_object.alpha_object[custom_constant.webdriver_type] in self.webdriver_type_list:
                        MainWindow.set_value(self.webdriver_type_value_str,
                                             self.alpha_object.alpha_object[custom_constant.webdriver_type])
                    else:
                        raise ValueError('load_config_main(self, mode): 浏览器类型错误')
                    # 账号框id
                    MainWindow.set_value(self.account_id_text,
                                         self.alpha_object.alpha_object[custom_constant.account_id])
                    # 密码框id
                    MainWindow.set_value(self.password_id_text,
                                         self.alpha_object.alpha_object[custom_constant.pwd_id])
                    # 登录按钮id
                    MainWindow.set_value(self.login_id_text,
                                         self.alpha_object.alpha_object[custom_constant.login_id])
                    # 基础功能
                    # 网址
                    MainWindow.set_value(self.webpath_text,
                                         self.alpha_object.alpha_object[custom_constant.func_object][
                                             custom_constant.webpath])
                    # 工作模式
                    MainWindow.set_value(self.work_mode_value_int,
                                         work_mode)
                    # 自动关闭
                    MainWindow.set_value(self.auto_close_window_value_bool,
                                         self.alpha_object.alpha_object[custom_constant.func_object][
                                             custom_constant.autoClose])
                    # 自动执行
                    MainWindow.set_value(self.auto_start_value_bool,
                                         self.alpha_object.alpha_object[custom_constant.func_object][
                                             custom_constant.autoStart])
                    # 守护进程
                    MainWindow.set_value(self.guard_service_value_bool,
                                         self.alpha_object.alpha_object[custom_constant.func_object][
                                             custom_constant.guard_service])
                else:
                    raise ValueError('load_config_main(self, mode): 配置损坏')

            # 配置加载完需要更新的界面
            self.load_element_by_mode()
        else:
            raise ValueError("load_config_main(self, mode): 参数不全")

    def save_config(self):
        # 保存配置
        work_mode = self.get_cur_work_mode()
        if work_mode in self.all_work_mode:
            if work_mode == 1:
                self.generate_object(work_mode)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.work_mode, work_mode)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.normal_object,
                                           self.normal_object.normal_object)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.func_object,
                                           self.normal_object.func_object.func_object)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.alpha_object, '')
            elif work_mode == 2:
                self.generate_object(work_mode)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.work_mode, work_mode)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.alpha_object,
                                           self.alpha_object.alpha_object)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.func_object,
                                           self.alpha_object.func_object.func_object)
                self.root_config.set_value(custom_constant.userconfig, custom_constant.normal_object, '')
            else:
                raise ValueError("save_config(self): 参数不全")

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
    def choose_file(cls, element):
        # 选择本地文件
        path = tkinter.filedialog.askopenfilename()
        if path is not None and path != '':
            MainWindow.set_value(element, path)

    @classmethod
    def set_value(cls, element, content):
        if str(type(element)) == "<class 'tkinter.Text'>":
            element.delete(0.0, END)
            element.insert(0.0, content)
        else:
            element.set(content)
