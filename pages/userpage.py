from base.page import BasePage
from base.action import ElementActions



class LoginPage(BasePage):

    name="登录页"

    def login(self,action:ElementActions,account,password):
        action.sleep(0.5).start_activity(self.activity)
        action.click(self.账号密码登录tag)
        action.text(self.账号输入框,account).text(self.密码输入框,password).click(self.登录按钮)
        action.sleep(5)


    def load_android(self):
        self.activity="com.jumei.login.loginbiz.activities.login.LoginActivity"

        self.账号密码登录tag=self.get_locator("账号密码登录tag",'id','com.jm.android.jumei:id/tab_login_account')

        self.账号输入框=self.get_locator("账号输入框",'id','com.jm.android.jumei:id/lg_user_name')
        self.密码输入框=self.get_locator( "密码输入框", 'id', 'com.jm.android.jumei:id/lg_password')
        self.登录按钮=self.get_locator("登录按钮", 'id', 'com.jm.android.jumei:id/login_account')


    def load_ios(self):
        self.账号输入框="4455"