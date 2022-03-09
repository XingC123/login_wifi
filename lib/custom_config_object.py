from environment.custom_constant import custom_constant


def str2int(string):
    if string != '' and string is not None:
        return int(string)
    else:
        return -1


class FunctionObject:
    # 基本功能 对象
    def __init__(self):
        self.func_object = None

    def init_func_object(self, webpath='', work_mode='', autostart=False, autoclose=False, guard_service=False):
        self.func_object = {custom_constant.webpath: webpath,
                            custom_constant.work_mode: work_mode,
                            custom_constant.autoStart: autostart, custom_constant.autoClose: autoclose,
                            custom_constant.guard_service: guard_service
                            }


class NormalLoginObject:
    # 稳定模式 的配置对象
    def __init__(self):
        self.normal_object = None
        self.func_object = FunctionObject()

    def init_config_object(self):
        self.set_normal_object(mode='init')

    def set_normal_object(self, account='', ax='', ay='',
                          pwd='', pwdx='', pwdy='',
                          loginx='', loginy='',
                          brower_name='', webpath='', work_mode='1',
                          autostart=False, autoclose=False, guard_service=False,
                          mode='normal', ):
        def if_allow_set_object():
            if webpath != '':
                if str2int(work_mode) == 1 and \
                        account != '' and ax != '' and ay != '' and pwd != '' and pwdx != '' and pwdy != '' and \
                        loginx != '' and loginy != '' and brower_name != '':
                    return True
            raise ValueError("Normal: if_allow_set_object(): 参数不全")

        if mode == 'init' or if_allow_set_object():
            self.func_object.init_func_object(webpath, work_mode, autostart, autoclose, guard_service)
            self.normal_object = {custom_constant.account: account,
                                  custom_constant.account_x: ax, custom_constant.account_y: ay,
                                  custom_constant.password: pwd, custom_constant.password_x: pwdx,
                                  custom_constant.password_y: pwdy,
                                  custom_constant.login_x: loginx, custom_constant.login_y: loginy,
                                  custom_constant.brower_name: brower_name,
                                  custom_constant.func_object: self.func_object.func_object
                                  }

    def check_config(self):
        # 检测配置
        for i in self.normal_object.keys():
            if i != custom_constant.func_object:
                if self.normal_object[i] == '':
                    return False
            else:
                for j in self.normal_object[i].keys():
                    if self.normal_object[i][j] == '':
                        return False
        return True


class AlphaLoginObject:
    # ALPHA模式 的配置对象
    def __init__(self):
        self.alpha_object = None
        self.func_object = FunctionObject()

    def init_config_object(self):
        self.set_alpha_object(mode='init')

    def set_alpha_object(self, account='', pwd='', webpath='', work_mode='2', webdriver_type='', webdriver_path='',
                         account_id='', pwd_id='', login_id='', button_click_mode='click',
                         autostart=False, autoclose=False, guard_service=False,
                         mode='normal'):
        def if_allow_set_object():
            if webpath != '':
                if str2int(work_mode) == 2 and \
                        account != '' and pwd != '' and webdriver_path != '' and webdriver_type != '' and \
                        account_id != '' and pwd_id != '' and login_id != '' and button_click_mode != '':
                    return True
            raise ValueError("ALPHA: if_allow_set_object(): 参数不全")

        if mode == 'init' or if_allow_set_object():
            self.func_object.init_func_object(webpath, work_mode, autostart, autoclose, guard_service)
            self.alpha_object = {custom_constant.account: account, custom_constant.password: pwd,
                                 custom_constant.webdriver_path: webdriver_path,
                                 custom_constant.webdriver_type: webdriver_type,
                                 custom_constant.account_id: account_id, custom_constant.pwd_id: pwd_id,
                                 custom_constant.login_id: login_id,
                                 custom_constant.button_click_mode: button_click_mode,
                                 custom_constant.func_object: self.func_object.func_object
                                 }

    def check_config(self):
        # 检测配置
        for i in self.alpha_object.keys():
            if i != custom_constant.func_object:
                if self.alpha_object[i] == '':
                    return False
            else:
                for j in self.alpha_object[i].keys():
                    if self.alpha_object[i][j] == '':
                        return False
        return True
