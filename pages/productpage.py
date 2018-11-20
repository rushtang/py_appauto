# -*- coding: utf-8 -*-

from base.page import BasePage
from base.action import ElementActions

#元素定位方式尽量不要xpath，容易很慢(Appium对于xpath定位执行效率是比较低的)
#已通过find_elements_by_android_uiautomator实现通过name元素定位


class HomePage(BasePage):

    name="特卖首页"


    def pageinto(self,action:ElementActions):
        action.sleep(8).start_activity(self.activity)




    def load_android(self):
        self.activity="com.jm.android.jumei.home.activity.NewHomeActivity"

        self.搜索输入框=self.get_locator("搜索输入框",'id','com.jm.android.jumei:id/tv_go_search')

        self.导航栏=self.get_locator("导航栏",'id','com.jm.android.jumei:id/home_navigate_tab')
        self.导航栏_推荐=self.get_locator("导航栏_推荐",'xpath','//android.widget.TextView[@text="推荐"]')

        self.推荐商品栏=self.get_locator("推荐商品栏",'id','com.jm.android.jumei:id/content_recycle_view')
        self.推荐商品栏_商品栏=self.get_locator("推荐商品栏_商品",'class name','android.widget.LinearLayout')
        self.商品栏_购物车加入=self.get_locator("商品_购物车加入",'id','com.jm.android.jumei:id/add_cart_iv')



    def load_ios(self):
        self.搜索输入框="4455"


class CategoryListPage(BasePage):

    name="分类列表搜索页"


    def load_android(self):
        self.activity="com.jumei.list.category.CategoryListActivity"

        self.搜索输入框=self.get_locator("搜索输入框",'id','com.jm.android.jumei:id/search_input')
        self.搜索按钮=self.get_locator("搜索按钮",'id','com.jm.android.jumei:id/search_bt')




class SearchListPage(BasePage):

    name = "搜索后列表页"


    def pageinto(self,action:ElementActions,key="专场"):
        分类列表搜索页=CategoryListPage()
        action.start_activity(分类列表搜索页.activity)
        action.text(分类列表搜索页.搜索输入框,key).click(分类列表搜索页.搜索按钮)


    def load_android(self):

        self.第一个商品项=self.get_locator("第一个商品项",'xpath','//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.RelativeLayout',dynamic=True)


class ProductDetailsPage(BasePage):
    name = "商品详情页"


    def load_android(self):

        self.加入购物车 = self.get_locator("加入购物车",'id','com.jm.android.jumei:id/tv_addcart',dynamic=True)


        self.促销=self.get_locator("促销",'name','促销')  #点击后会出现弹窗
        self.促销_弹窗_标题=self.get_locator("促销_弹窗_标题",'id','com.jm.android.jumei:id/tv_detail_title')  #text 属性为促销
        self.促销_弹窗_关闭 = self.get_locator("促销_弹窗_关闭", 'id', 'com.jm.android.jumei:id/rl_close')

        self.运费 = self.get_locator("运费", 'name', '运费')
        self.运费_跳转页_标题=self.get_locator("运费_跳转页的标题", 'id', 'com.jm.android.jumei:id/title',page='运费说明页')  #text属性为 运费
        self.运费_跳转页_关闭 = self.get_locator("运费_跳转页_关闭", 'id', 'com.jm.android.jumei:id/close_ImgBtn',page='运费说明页')



        self.说明 = self.get_locator( "说明", 'name', '说明')
        self.说明_弹窗_标题=self.get_locator("说明_弹窗_标题", 'id', 'com.jm.android.jumei:id/tv_detail_title')  #text 属性为说明
        self.说明_弹窗_关闭=self.get_locator("说明_弹窗_关闭", 'id', 'com.jm.android.jumei:id/rl_close')












