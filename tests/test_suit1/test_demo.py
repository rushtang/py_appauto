#-*- coding: utf-8 -*-
from base.action import ElementActions
from lib.pages.set import ProductPages as p
from base.verify import NotFoundTextError


#测试用例demo，pytest框架自动加载执行





class Test_demo():

    # def test_检查元素是否存在(self, action: ElementActions):
    #     # 该用例是为了检测check_page方法
    #     page.check_pageset([p, up], action)


    def test_home(self, action: ElementActions):
        #用例必传参数action(通过conftest.py中生成的，类型为ElementActions的对象)    函数参数注解格式： obj: class
        #函数注解语法  见https://python3-cookbook.readthedocs.io/zh_CN/latest/c07/p03_attach_informatinal_matadata_to_function_arguments.html

        # up.登录页.login(action,'13550234762','tmhrush2233')

        #  p为ProductPages的别名
        action.sleep(8)\
            .click(p.特卖首页.搜索输入框)
        #因为调用action的大部分公用方法是返回self，所以可以一条语句执行多次不同方法

        action.text(p.分类列表搜索页.搜索输入框,"迪奥口红")\
            .click(p.分类列表搜索页.搜索按钮)

        action.click(p.搜索后列表页.第一个商品项)

        #循环下拉，检查是否有对应关键字，找到后终止
        for count in range(10):
            if action.swip_down().is_text_displayed("商品参数"):
                break
        #没有对应关键字抛出错误
        if action.is_text_displayed("迪奥") ==False:
            raise NotFoundTextError

        action.sleep(1)
