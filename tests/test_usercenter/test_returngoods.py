#-*- coding: utf-8 -*-

from base.action import ElementActions
from lib.pages.set import ProductPages as p, UserPages as up,BuyPages as bp
from base.verify import Validator,NotFoundElementError
from lib.reuse_business import base_business,shopping_business
from base.utils import log
from flaky import flaky

class Test_productbrowse():

    def clear_browsenumber(self,action:ElementActions):
        action.click(up.用户中心.浏览记录)
        if action.is_element_exist(up.浏览记录.编辑):
            action.click(up.浏览记录.编辑)
            product_eles=action.find_ele(up.浏览记录.编辑页浏览商品选择按钮,is_Multiple=True)
            for product_ele in product_eles:
                action.click_ele(product_ele)
            action.click(up.浏览记录.删除).click(up.浏览记录.删除弹窗确定按钮)

        log.info('当前浏览记录为空~')



    def get_browsenumber(self,action:ElementActions):
        tmpele = action.find_ele(up.用户中心.用户中心列表)
        tmpele2 = action.find_ele_child(tmpele, up.用户中心.用户中心列表_列表1)
        browsenumberele = action.find_ele_child(tmpele2, up.用户中心.用户中心列表_列表1_相关数量,is_Multiple=True)[2]
        browsenumber = action.get_text_ele(browsenumberele)

        log.info('当前浏览记录值为{}'.format(browsenumber))

        return browsenumber

    #已登陆时生成浏览记录
    @flaky()
    def test_case1(self,action):

        base_business.login(action)

        self.clear_browsenumber(action)
        productname=shopping_business.browseproduct(action,key='爽肤水')

        up.用户中心.pageinto(action)
        new_browsenumber=int(self.get_browsenumber(action))

        logmsg="断言成功：浏览记录正常+1"
        errormsg="断言失败：当前new_browsenumber={}".format(new_browsenumber)
        Validator.assert_eq(1,new_browsenumber,errormsg,logmsg)

        #访问浏览记录页
        action.click(up.用户中心.浏览记录)

        map={ 'value':productname}
        browseproduct_locator=up.浏览记录.newlocator(up.浏览记录.当前浏览商品,map)
        action.get_img('当天的浏览记录')
        Validator.assert_true(action.is_element_exist(browseproduct_locator),'断言失败：没找到对应的浏览商品名')






class Test_favourite():



    #收藏商品，然后再删除对应的收藏
    def test_case1(self,action):
        base_business.login(action)
        productname=shopping_business.browseproduct(action,key='爽肤水')
        action.click(p.商品详情页.收藏按钮)

        toast=action.is_toast_show('收藏成功')
        Validator.assert_true(toast,"断言失败: 没收藏成功的提示")

        up.用户中心.pageinto(action)
        action.click(up.用户中心.收藏商品)

        product_locator=up.收藏页.newlocator(up.收藏页.当前收藏商品, 'value', productname)
        action.get_img('收藏商品列表')
        Validator.assert_true(action.is_element_exist(product_locator),'断言失败： 没找到对应收藏的商品')

        #删除收藏
        action.long_press(product_locator,time=4000)
        action.click(up.收藏页.删除收藏)
        toast = action.is_toast_show('删除成功')
        Validator.assert_true(toast, "断言失败: 没删除成功的提示")



class Test_debug():

    def test_case1(self,action):


        up.用户中心.pageinto(action)
        action.click(up.用户中心.查看全部订单)
        action.get_img('我的订单')

        map={'value':".//android.widget.TextView[@text='爱的']"}
        productname_locator=bp.我的订单页.newlocator(bp.我的订单页.订单商品名,map)

        eles=action.find_ele(productname_locator,is_Multiple=True,wait=5)
        log.info(eles)

        product_ele=action.find_ele_parent(bp.我的订单页.订单商品项s,productname_locator,wait=4)
        log.info(product_ele)

        price_ele=action.find_ele_child_byelement(product_ele,bp.我的订单页.订单商品单价格s)
        log.info(action.get_text_ele(price_ele))






