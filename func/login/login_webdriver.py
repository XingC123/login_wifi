import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from lib.selenium_anti_detection.selenium_anti_detection import selenium_anti_detection
from environment.custom_constant import custom_constant


class Login:
    def __init__(self, alpha_object, run_root_path):
        # 变量定义
        self.Alpha_object = alpha_object
        # 初始化 主py 文件运行目录
        self.run_root_path = run_root_path
        # 驱动路径
        self.driver_path = self.Alpha_object[custom_constant.webdriver_path]
        # 网址
        self.url = self.Alpha_object[custom_constant.func_object][custom_constant.webpath]
        # 账号 & 密码
        self.account_str = self.Alpha_object[custom_constant.account]
        self.password_str = self.Alpha_object[custom_constant.password]
        # hook元素的id
        self.account_id = self.Alpha_object[custom_constant.account_id]
        self.pwd_id = self.Alpha_object[custom_constant.pwd_id]
        self.login_id = self.Alpha_object[custom_constant.login_id]
        # 初始化一个drive
        self.driver = None
        # hook的登录元素数组
        self.element_list = [self.account_id, self.pwd_id, self.login_id]
        # 登录过程可视化
        self.login_visualization = self.Alpha_object[custom_constant.func_object][custom_constant.login_visualization]

        # 初始化
        self.init_webdriver(self.driver_path)

    def init_webdriver(self, driver_path):
        if self.Alpha_object[custom_constant.webdriver_type].startswith('Microsoft edge Chromium') or \
                self.Alpha_object[custom_constant.webdriver_type] == 'Chrome':
            # Microsoft Edge Chromium
            # Microsoft Edge 80及更高版本有了重大更新：不再支持使用ChromeDriver和ChromeOptions自动化或测试Microsoft Edge (Chromium)
            if self.Alpha_object[custom_constant.webdriver_type] == 'Microsoft edge Chromium 80 以下' or \
                    self.Alpha_object[custom_constant.webdriver_type] == 'Chrome':
                driver_options = webdriver.ChromeOptions()
            else:
                # edge 80以上
                driver_options = webdriver.EdgeOptions()
                driver_options.use_chromium = True

            # 支持拓展
            driver_options.add_experimental_option('useAutomationExtension', False)
            # 隐藏自动化测试提示
            # 修改window.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
            # CDP执行JavaScript 代码  重定义windows.navigator.webdriver的值
            driver_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
            # 登录过程可视化
            if not self.login_visualization:
                # 不可视化
                driver_options.add_argument('--disable-gpu')  # 谷歌文档说以此来规避bug
                driver_options.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败

            if self.Alpha_object[custom_constant.webdriver_type] == 'Microsoft edge Chromium 80 以下' or \
                    self.Alpha_object[custom_constant.webdriver_type] == 'Chrome':
                # 创建driver对象
                self.driver = webdriver.Chrome(executable_path=driver_path, options=driver_options)
            else:
                # 创建driver对象
                self.driver = webdriver.ChromiumEdge(executable_path=driver_path, options=driver_options)

            # 修改window.navigator.webdriver，防机器人识别机制，selenium自动登陆判别机制
            # CDP执行JavaScript 代码  重定义windows.navigator.webdriver的值
            # self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            #     "source": """
            #         Object.defineProperty(navigator, 'webdriver', {
            #           get: () => undefined
            #         })
            #       """
            # })
            # 加载防检测selenium的js脚本
            js = selenium_anti_detection()
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js
            })
        elif self.Alpha_object[custom_constant.webdriver_type] == 'Firefox':
            self.driver = webdriver.Firefox(executable_path=driver_path)

    def open_url(self, url):
        # 打开页面
        self.driver.get(url)
        self.driver.maximize_window()

    def work_after_loaded(self, id_str):
        # input_type = ['text', 'password']
        # 时间单位均为 s
        # 最长等待时间
        max_delay_time = 10
        # 检测间隔
        check_interval = 0.5
        # 若存在, 则返回对象
        try:
            element = self.driver.find_element(By.ID, id_str)
        except:
            print('ERROR: work_after_loaded(self, id_str): ', end=', ')
            print('未找到元素 ->', id_str)
        else:
            # 若成功取得目标元素
            # 等待该元素加载完毕
            WebDriverWait(self.driver, max_delay_time, check_interval).until(
                ec.presence_of_element_located((By.ID, id_str)))
            # 获取该元素的类型
            element_type = element.get_attribute('type')
            if element_type == 'text':
                element.send_keys(self.account_str)
            elif element_type == 'password':
                element.send_keys(self.password_str)
            elif element_type == 'button':
                # element.submit() 会直接刷新页面, 无法达到理想效果?
                # if self.button_click_mode == 'submit':
                #     element.submit()
                # else:
                #     element.click()
                js = 'document.getElementById("' + id_str + '").click()'
                self.driver.execute_script(js)

    def run(self):
        # 执行login
        # time.sleep(3)  # 也许过快会造成打开浏览器地址栏只有"data:,"的bug
        try:
            self.open_url(self.url)
        except Exception as e:
            print('登录run()')
            print(e)
        else:
            # hook目标元素
            for i in self.element_list:
                self.work_after_loaded(i)

            # 等待5s, 防止过快响应导致login不成功
            time.sleep(5)
        finally:
            self.driver.close()
