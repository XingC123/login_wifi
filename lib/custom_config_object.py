class AlphaLoginObject:
    # Alpha模式 的配置对象
    def __init__(self, account, password, url, webdriver_path, account_id, pwd_id, login_id, button_click_mode='click'):
        self._account = account  # 账号
        self._password = password  # 密码
        self._url = url  # 网址
        self._webdriver_path = webdriver_path  # 浏览器驱动地址
        # hook的元素的id
        self._account_id = account_id  # 账号框id
        self._pwd_id = pwd_id  # 密码框id
        self._login_id = login_id  # 登录按钮id
        # 按钮点击方式
        self._button_click_mode = button_click_mode

    def get_object_elements(self):
        # 获取元素值
        return self._account, self._password, self._url, self._webdriver_path, \
               self._account_id, self._pwd_id, self._login_id, self._button_click_mode
