# -*- coding: utf-8 -*-

import pytest,os,logging
from appium import webdriver
from base.action import ElementActions
from base.environment import EnvironmentAndroid
from base.utils import log



#pytest的setup和down工作




#初始化driver对象，在package的领域只会执行一次
@pytest.fixture("package")
def driverenv():


    env=EnvironmentAndroid()
    current_device=env.current_device

    capabilities = {
                    'platformName': current_device.get("platformName"),
                    'platformVersion': current_device.get("platformVersion"),
                    'deviceName': current_device.get("deviceName"),
                    'udid': current_device.get("deviceName"),
                    'systemPort':current_device.get('systemPort'),
                    'app': env.appium.get("app"),
                    'clearSystemFiles': True,
                    'appActivity': env.appium.get("appActivity"),
                    'appPackage': env.appium.get("appPackage"),
                    'automationName': 'UIAutomator2',
                    'noSign': True,
                    'recreateChromeDriverSessions': True,
                    "unicodeKeyboard": True,
                    "noReset":True,
                    "fullReset":False,
                    "newCommandTimeout": 300
                    }
    # systemPort=current_device.get('systemPort')
    # if systemPort!=None:
    #     capabilities['systemPort']=systemPort
    #
    log.info('当前执行的appium相关配置为：'+str(capabilities))

    host=current_device.get('appiumserver')

    driver = webdriver.Remote(host, capabilities)

    return driver


#初始化ElementActions类的对象，在package的领域只会执行一次，并且通过yield实现package执行结束前的数据清理工作
@pytest.fixture("package")
def action(driverenv):
    element_action=ElementActions(driverenv)
    yield element_action   #返回并且挂载ElementActions的实例，在对应作用域结束前，执行driver.quit()

    element_action.driver.quit()





#用例执行前后：加入日志说明、结束前的截图输出到报告上
@pytest.fixture(autouse=True)
def caserun(action):

    log.info("————————————————————————执行用例 ----------——————————————" )
    yield
    action.sleep(1).get_img("用例结束前的截图")
    log.info("————————————————————————该用例执行结束 ----------——————————————")










