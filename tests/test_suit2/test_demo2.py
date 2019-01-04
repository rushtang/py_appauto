# -*- coding: utf-8 -*-
from base.action import ElementActions
from lib.pages.set import ProductPages as p
from base.verify import NotFoundTextError
from base.utils import log

#测试用例demo，pytest框架自动加载执行



class Test_demo():




    def test_home(self, action: ElementActions):
        #用例必传参数action(通过conftest.py中生成的，类型为ElementActions的对象)    函数参数注解格式： obj: class
        #函数注解语法  见https://python3-cookbook.readthedocs.io/zh_CN/latest/c07/p03_attach_informatinal_matadata_to_function_arguments.html

        # up.登录页.login(action,'13550234762','tmhrush2233')

        #  p为ProductPages的别名
        action.sleep(8)\
            .click(p.特卖首页.搜索输入框)
        #因为调用action的大部分公用方法是返回self，所以可以一条语句执行多次不同方法

        action.text(p.分类列表搜索页.搜索输入框,"口红")\
            .click(p.分类列表搜索页.搜索按钮)

        action.click(p.搜索后列表页.第一个商品项)

        #循环下拉，检查是否有对应关键字，找到后终止
        for count in range(20):
            if action.swip_down().is_text_displayed("商品参数"):
                break
        #没有对应关键字抛出错误
        if action.is_text_displayed("口红") ==False:
            raise NotFoundTextError

        action.sleep(1)


    def test_推荐频道(self, action: ElementActions):


        p.特卖首页.home(action)

        导航栏ele=action.find_ele(p.特卖首页.导航栏)
        推荐按钮ele=action.find_ele_child(导航栏ele,p.特卖首页.导航栏_推荐)

        action.click_ele(推荐按钮ele)

        #循环下拉，找到对应商品点击后终止
        for count in range(10):
            action.swip_down()

            推荐商品栏ele=action.find_ele(p.特卖首页.推荐商品栏)
            商品栏列表eles=action.find_ele_child(推荐商品栏ele,p.特卖首页.推荐商品栏_商品栏,is_Multiple=True)

            product_ele=action.find_ele_traversing(商品栏列表eles,p.特卖首页.商品栏_购物车加入)
            if product_ele!=None:
                action.click_ele(product_ele).sleep(4)

                break

        log.info("成功进入该商品的详情页")

        #检测基础说明弹窗（促销类型、运费、说明）
        action.swip_down(half=True)
        action.get_img('商品的详情页')

        促销ele=action.find_ele(p.商品详情页.促销)
        if 促销ele!=None:
            action.click_ele(促销ele)
            title=action.get_text(p.商品详情页.促销_弹窗_标题)
            if "促销" not in  title:
                log.error("弹窗没有找到对应的促销标题")
                action.get_img('促销_弹窗')

            action.click(p.商品详情页.促销_弹窗_关闭)
        else:
            log.info("当前详情页为没促销的")
            action.get_img('详情页_促销')


        action.click(p.商品详情页.运费)
        title=action.get_text(p.商品详情页.运费_跳转页_标题)
        if "运费" not in title:
            log.error("跳转页没有找到对应的运费标题")
            action.get_img('运费_跳转页')

        action.click(p.商品详情页.运费_跳转页_关闭)

        action.click(p.商品详情页.说明)
        title=action.get_text(p.商品详情页.说明_弹窗_标题)
        if "说明" not in title:
            log.error("弹窗没有找到对应的说明标题")
            action.get_img('说明_弹窗')

        action.click(p.商品详情页.说明_弹窗_关闭)















