# -*- coding: utf-8 -*-
from base.utils import log,Conf,get_attrsname
from base.action import ElementActions
import abc,inspect




class BasePage(metaclass=abc.ABCMeta):
    #抽象类BasePage，不能被实例化，实际使用的子类
    #初始化时，通过平台决定加载的元素（实际使用page的元素时，使用对应平台的元素）

    def __init__(self):
        conf = Conf()
        if conf.platform==conf.androidname:
            self.load_android()
        elif conf.platform==conf.iosname:
            self.load_ios()
        else:
            raise AttributeError

    name = ""

    @abc.abstractmethod
    def load_android(self):
        self.activity=""
        pass


    def load_ios(self):
        pass


    #获取定位器对象(字典结构)，定位器对象返回的就是元素本身，包含对应元素属性
    #元素属性有：元素名、元素的定位方式、对应定位方式的值、是否是动态元素、查找元素的等待时间、元素的页面名
    def get_locator(self,elename, type, value, dynamic=False,timeOutInSeconds=None,page=None):
        if page==None:
            page=self.name

        locator=dict(page=page, name=elename, type=type, value=value, dynamic=dynamic)
        if timeOutInSeconds!=None:
            locator.update(timeOutInSeconds=timeOutInSeconds)
        return locator




def check_page(Pages,action: ElementActions):
    #只能检测静态页面（即可用activity直接跳转的）

    static_pagelist=getattr(Pages,'static_pagelist')
    page_names=static_pagelist()

    for page_name in page_names:
        page=getattr(Pages,page_name)
        elements_name=get_attrsname(page)

        #进入可通过activity跳转的对应页面
        if hasattr(page,'activity')==False:
            continue
        else:
            action.start_activity(getattr(page,'activity'))

            # 对元素进行遍历查询
            for element_name in elements_name:
                element=getattr(page,element_name)
                if isinstance(element,dict):
                    if element.get('dynamic')==False:
                        action.check_ele(locator=element)

















