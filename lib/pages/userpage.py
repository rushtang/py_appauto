from base.page import BasePage
from base.action import ElementActions
from base.utils import log


#name方式查询本质是：
# new UiSelector().textContains' + '(\"' + value + '\")



class UserCenterPage(BasePage):
    name = '用户中心页'



    def pageinto(self,action:ElementActions):
        from .set import ProductPages as p
        p.特卖首页.pageinto(action)
        action.tap(p.特卖首页.进入用户中心按钮)


    def is_logined(self,action:ElementActions):
        #已登陆时返回True

        if action.find_ele(self.注册登陆,wait=2)!=None:
            return False
        else:
            return True



    def load_android(self):

        self.设置按钮=self.get_locator('设置按钮','id','com.jm.android.jumei:id/mine_top_setting_iv')
        self.注册登陆=self.get_locator('注册登陆','id','com.jm.android.jumei:id/mine_top_register_login_tv')

        self.顶部=self.get_locator('顶部','id','com.jm.android.jumei:id/mine_top_logined_ll')
        self.顶部名字=self.get_locator('顶部名字','xpath','.//android.widget.TextView[contains(@text, "我的")]')
        self.用户中心列表=self.get_locator('用户中心列表','id','com.jm.android.jumei:id/mine_card_parent_ll')
        self.用户中心列表_列表1=self.get_locator('用户中心列表_列表1','id','com.jm.android.jumei:id/mine_card_content')  #查询出多个中的第一个


        # 查询出多个元素,text属性表示数量,第一个收藏数量、第二个为收藏专柜数量、第三个为浏览记录数量
        self.用户中心列表_列表1_相关数量=self.get_locator('相关数量','id',
                                                'com.jm.android.jumei:id/mine_card_content_item_title_tv')
        self.收藏商品=self.get_locator('收藏商品','name','收藏商品')

        self.收藏专柜=self.get_locator('收藏专柜','name','收藏专柜')

        self.浏览记录=self.get_locator('浏览记录','name','浏览记录')


        #订单
        self.查看全部订单=self.get_locator('查看全部订单','id','com.jm.android.jumei:id/more_card_label_url_tv')
        self.待付款=self.get_locator('待付款','name','待付款')
        self.待发货=self.get_locator('待发货','name','待发货')


class BrowseRecordPage(BasePage):
    name="浏览记录页"

    def load_android(self):
        #value为空，通过newlocator获取该locator
        self.当前浏览商品=self.get_locator('当前浏览商品','name','')
        self.编辑=self.get_locator('编辑','name','编辑',dynamic=True)

        #返回多个
        self.编辑页浏览商品选择按钮=self.get_locator('编辑页浏览商品选择按钮','id','com.jm.android.jumei:id/scan_select',page='浏览记录编辑页')
        self.编辑完成=self.get_locator('编辑完成','name','完成',page='浏览记录编辑页')
        self.删除=self.get_locator('删除','id','com.jm.android.jumei:id/scan_del',page='浏览记录编辑页')
        self.删除弹窗确定按钮=self.get_locator('删除弹窗确定按钮','id','com.jm.android.jumei:id/positive',page='浏览记录编辑页')



class FavouritePage(BasePage):
    name = "收藏页"

    def load_android(self):
        # value为空，通过newlocator获取该locator
        self.当前收藏商品=self.get_locator('当前收藏商品','name','')

        self.删除收藏=self.get_locator('删除收藏','id','com.jm.android.jumei:id/dialog_collect_product_btn_delete') #长按收藏商品时才出现
        self.删除收藏取消=self.get_locator('删除收藏取消','id','com.jm.android.jumei:id/dialog_collect_product_btn_cancel')





class SetAppPage(BasePage):
    name='设置页'

    def pageinto(self,action:ElementActions):
        usercenter=UserCenterPage()
        usercenter.pageinto(action)
        action.click(usercenter.设置按钮)



    def load_android(self):

        self.关于聚美按钮 = self.get_locator('关于聚美按钮', 'name', '关于聚美')
        self.退出账号=self.get_locator('退出账号','id','com.jm.android.jumei:id/exit_login_btn',dynamic=True)

        self.版本号 = self.get_locator('版本号', 'id', 'com.jm.android.jumei:id/help_vistion', page='设置页-关于聚美',dynamic=True)
        self.开发者选项 = self.get_locator('开发者选项', 'name', '开发者选项')
        self.后台环境 = self.get_locator('后台环境', 'name', '后台环境', page='设置页-开发者',dynamic=True)
        self.测试环境按钮 = self.get_locator('测试环境', 'name', '测试环境', page='设置页-开发者',dynamic=True)





class LoginPage(BasePage):

    name="登录页"

    def pageinto(self,action:ElementActions):
        action.sleep(0.5).start_activity(self.activity)
        usercenterpage=UserCenterPage()
        # usercenterpage.pageinto(action)
        if action.find_ele(usercenterpage.注册登陆)!=None:
            action.click(usercenterpage.注册登陆)
        else:
            log.info('app已是登陆状态，无法进入登陆页')


    def login(self,action:ElementActions,account,password):
        self.switch_密码登录tag(action)
        action.text(self.账号输入框,account).text(self.密码输入框,password).click(self.登录按钮)
        action.sleep(5)

    def switch_密码登录tag(self,action:ElementActions):
        action.click(self.密码登录tag)


    def load_android(self):
        self.activity="com.jumei.login.loginbiz.activities.login.LoginActivity"

        self.密码登录tag=self.get_locator("密码登录tag",'id','com.jm.android.jumei:id/tab_login_account')

        self.账号输入框=self.get_locator("账号输入框",'id','com.jm.android.jumei:id/lg_user_name',switch='switch_密码登录tag')
        self.密码输入框=self.get_locator( "密码输入框", 'id', 'com.jm.android.jumei:id/lg_password',switch='switch_密码登录tag')
        self.登录按钮=self.get_locator("登录按钮", 'id', 'com.jm.android.jumei:id/login_account',switch='switch_密码登录tag')


    def load_ios(self):
        self.账号输入框="4455"
