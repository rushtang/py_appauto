# -*- coding: utf-8 -*-

from base.page import BasePage
from base.action import ElementActions
from base.utils import log

#元素定位方式尽量不要xpath，容易很慢(Appium对于xpath定位执行效率是比较低的)
#已通过find_elements_by_android_uiautomator实现通过name元素定位


class HomePage(BasePage):

    name="特卖首页"


    def home(self,action:ElementActions):
        action.driver.wait_activity(self.activity,8,interval=0.3)
        try:
            action.click(self.关闭初始化弹出窗,wait=3)
        except:
            log.info('无弹窗需要关闭,所以不会找到元素 关闭初始化弹出窗')
        action.tap(self.关闭初始化浮窗)



    def pageinto(self,action:ElementActions):
        action.start_activity(self.activity)




    def load_android(self):
        self.activity="com.jm.android.jumei.home.activity.NewHomeActivity"

        self.关闭初始化浮窗=self.get_locator('关闭初始化浮窗','tap','891,132')
        self.关闭初始化弹出窗=self.get_locator("关闭初始化弹出窗",'id','com.jm.android.jumei:id/image_home_full_close')

        self.搜索输入框=self.get_locator("搜索输入框",'id','com.jm.android.jumei:id/tv_go_search')

        self.导航栏=self.get_locator("导航栏",'id','com.jm.android.jumei:id/home_navigate_tab')
        self.导航栏_推荐=self.get_locator("导航栏_推荐",'xpath','//android.widget.TextView[@text="推荐"]')

        self.推荐商品栏=self.get_locator("推荐商品栏",'id','com.jm.android.jumei:id/content_recycle_view')
        self.推荐商品栏_商品栏=self.get_locator("推荐商品栏_商品",'class name','android.widget.LinearLayout')
        self.商品栏_购物车加入=self.get_locator("商品_购物车加入",'id','com.jm.android.jumei:id/add_cart_iv')

        #元素通过坐标位置点击
        self.进入用户中心按钮=self.get_locator('进入用户中心按钮','tap','987,1483')


        self.发布=self.get_locator('发布','id','com.jm.android.jumei:id/iv_publish_video')
        self.发布_上传视频=self.get_locator('上传视频','name','上传视频')


    def load_ios(self):
        self.搜索输入框="4455"


class CategoryListPage(BasePage):

    name="分类列表搜索页"

    def pageinto(self, action: ElementActions):
        action.start_activity(self.activity).sleep(0.5)


    def load_android(self):
        self.activity="com.jumei.list.category.CategoryListActivity"

        self.搜索输入框=self.get_locator("搜索输入框",'id','com.jm.android.jumei:id/search_input')
        self.搜索按钮=self.get_locator("搜索按钮",'id','com.jm.android.jumei:id/search_bt')




class SearchListPage(BasePage):

    name = "搜索后列表页"


    def pageinto(self,action:ElementActions,key="专场"):
        categorylistpage=CategoryListPage()
        categorylistpage.pageinto(action)
        action.text(categorylistpage.搜索输入框,key).click(categorylistpage.搜索按钮)


    def load_android(self):

        #有多个,点击进入商品详情页
        self.商品项标题s=self.get_locator("商品项标题",'id','com.jm.android.jumei:id/goods_title',dynamic=True)


class ProductDetailsPage(BasePage):
    name = "商品详情页"


    def load_android(self):



        self.收藏按钮=self.get_locator('收藏按钮','id','com.jm.android.jumei:id/my_favourite')
        self.分享按钮=self.get_locator('分享按钮','id','com.jm.android.jumei:id/share')



        self.促销=self.get_locator("促销",'name','促销')  #点击后会出现弹窗
        self.促销弹窗标题=self.get_locator("促销弹窗标题",'id','com.jm.android.jumei:id/tv_detail_title',dynamic=True)  #text 属性为促销
        self.促销弹窗关闭 = self.get_locator("促销弹窗关闭", 'id', 'com.jm.android.jumei:id/rl_close',dynamic=True)

        self.运费 = self.get_locator("运费", 'name', '运费')
        self.运费跳转页标题=self.get_locator("运费跳转页标题", 'id', 'com.jm.android.jumei:id/title',page='运费说明页')  #text属性为 运费
        self.运费跳转页关闭 = self.get_locator("运费跳转页关闭", 'id', 'com.jm.android.jumei:id/close_ImgBtn',page='运费说明页')



        self.说明 = self.get_locator( "说明", 'name', '说明')
        self.说明弹窗标题=self.get_locator("说明弹窗标题", 'id', 'com.jm.android.jumei:id/tv_detail_title')  #text 属性为说明
        self.说明弹窗关闭=self.get_locator("说明弹窗关闭", 'id', 'com.jm.android.jumei:id/rl_close')


        #商品参数相关
        self.商品参数列表=self.get_locator('商品参数列表','id','com.jm.android.jumei:id/properties_view')

        #返回多个,第一个为商品名称、第二个为品牌
        self.商品参数列表_商品参数值s=self.get_locator('商品参数列表_商品参数值s','id',"com.jm.android.jumei:id/goods_value")


        #购买相关
        self.加入购物车 = self.get_locator("加入购物车", 'id', 'com.jm.android.jumei:id/tv_addcart')
        self.立即购买 = self.get_locator('立即购买', 'id', 'com.jm.android.jumei:id/tv_directbuy')

        self.购买弹窗=self.get_locator('购买弹窗','id','com.jm.android.jumei:id/sl_root')
        self.skus=self.get_locator('sku选择列表_第一个','id','com.jm.android.jumei:id/tv_sku_name') #有多个
        self.不支持退货提示弹窗=self.get_locator('不支持退货提示弹窗','id','android:id/content')
        self.确认购买=self.get_locator('确认购买','id','com.jm.android.jumei:id/tv_confirm')

        self.购物车列表按钮=self.get_locator('购物车列表按钮','id','com.jm.android.jumei:id/shopcar_left')
        self.购物车数量显示=self.get_locator('购物车数量显示','id','com.jm.android.jumei:id/shopcar_number_tv')













