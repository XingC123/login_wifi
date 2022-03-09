from tkinter.font import Font
# 重要配置
rootconfig = 'rootconfig'
# 启动程序自动执行的配置名称列表
startwithboot = 'startwithboot'
# 按优先级排序的配置名称列表
config_priority = 'config_priority'
# 自动点击
autoclick = 'autoclick'
autoclick_interval = 'autoclick_interval'
# 动作列表
action_list = 'action_list'
# 动作类型: 点击/输入/打开网址/打开文件 -> click/click_blank/input
action_mode = 'action_mode'
action_x = 'action_x'
action_y = 'action_y'
input_content = 'input_content'
click_action = 'click'
input_action = 'input'
open_webbroswer_action = 'open_webbroswer'
open_file_action = 'open_file'
# 单个动作的对象
click_object = 'click_object'

# 文件中部分section名称
userconfig = 'userconfig'

# [新wifi自动登录]
account = 'account'
account_x = 'account_x'
account_y = 'account_y'
password = 'password'
password_x = 'password_x'
password_y = 'password_y'
login_x = 'login_x'
login_y = 'login_y'
webpath = 'webpath'
autoStart = 'autoStart'
autoClose = 'autoClose'
guard_service = 'guard_service'
brower_name = 'brower_name'
work_mode = 'work_mode'
webdriver_type = 'webdriver_type'
webdriver_path = 'webdriver_path'
account_id = 'account_id'
pwd_id = 'pwd_id'
login_id = 'login_id'
button_click_mode = 'button_click_mode'
func_object = 'func_object'
# 22.3.9
normal_object = 'normal_object'
alpha_object = 'alpha_object'


# 字体
class CustomFont:
    def __init__(self):
        font_size = 10
        self.microsoft_yahei_10 = Font(family='microsoft yahei', size=font_size)
