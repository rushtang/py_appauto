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
    #元素属性有：元素名、元素的定位方式、对应定位方式的值、是否是动态元素、出现该元素的前置操作（默认为空，填写page类的前置操作方法名）、元素的页面名
    def  get_locator(self,elename, type, value, dynamic=False,switch=None,page=None):

        if page==None:
            page=self.name
        locator=dict(name=elename, type=type, value=value, dynamic=dynamic,switch=switch,page=page)

        return locator

    def newlocator(self,locator:dict,map:dict):
        #动态修改定位元素方式
        for key,value in map.items():
            locator[key]=value

        return locator


    def pageinto(self,action):
        pass



def check_pageset(Pagesset,action: ElementActions):
    #参数Pagesset为元素是Pages的list

    for Pages in Pagesset:

        log.info('\n ++++++检测静态页面集： {}++++++\n'.format(Pages.__name__))

        check_page(Pages,action)




def check_page(Pages,action: ElementActions):

    #只能检测静态页面,即有固定进入方法的：pageinto

    pagesname_list=get_attrsname(Pages)

    for page_name in pagesname_list:
        page=getattr(Pages,page_name)


        #如果为静态页面时可通过page的跳转方法进入对应页面
        if hasattr(page,'pageinto')==False:
            continue
        else:
            log.info(' ----检测静态页面： {}----'.format(page_name))
            elements_name = get_attrsname(page)
            getattr(page,'pageinto')(action)

            # 对元素进行遍历查询
            for element_name in elements_name:
                element=getattr(page,element_name)
                if isinstance(element,dict):
                    if element.get('dynamic')==False:
                        if element.get('switch')!=None:
                            #如果该元素在当前页面有前置步骤，则执行该前置步骤
                            getattr(page,element.get('switch'))(action)

                        action.is_element_exist(locator=element)

















