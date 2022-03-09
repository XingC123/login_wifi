from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from environment.custom_constant import custom_constant


class Login:
    def __init__(self, alpha_object):
        # 变量定义
        self.Alpha_object = alpha_object
        # 驱动路径
        self.driver_path = self.Alpha_object[custom_constant.webdriver_path]
        # 网址
        self.url = self.Alpha_object[custom_constant.webpath]
        # 账号 & 密码
        self.account_str = self.Alpha_object[custom_constant.account]
        self.password_str = self.Alpha_object[custom_constant.password]
        # hook元素的id
        self.account_id = self.Alpha_object[custom_constant.account_id]
        self.pwd_id = self.Alpha_object[custom_constant.pwd_id]
        self.login_id = self.Alpha_object[custom_constant.login_id]
        # 初始化一个drive
        self.driver = None
        # hook的giwifi元素数组
        self.element_list = [self.account_id, self.pwd_id, self.login_id]
        # 按钮点击方式
        self._button_click_mode = self.Alpha_object[custom_constant.button_click_mode]

        # 初始化
        self.init_webdriver(self.driver_path)

    def init_webdriver(self, driver_path):
        if self.Alpha_object[custom_constant.webdriver_type] == 'Microsoft edge Chromium':
            self.driver = webdriver.ChromiumEdge(executable_path=driver_path)
        elif self.Alpha_object[custom_constant.webdriver_type] == 'Chrome':
            self.driver = webdriver.Chrome(executable_path=driver_path)
        elif self.Alpha_object[custom_constant.webdriver_type] == 'Firefox':
            self.driver = webdriver.Firefox(executable_path=driver_path)

    def open_url(self, url):
        # 打开页面
        self.driver.get(url)

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
                if self._button_click_mode == 'submit':
                    element.submit()
                else:
                    element.click()

    def run(self):
        # 执行login
        self.open_url(self.url)
        # hook目标元素
        for i in self.element_list:
            self.work_after_loaded(i)
