# -*- coding: utf-8 -*-

import pytest
from appium import webdriver
from base.action import ElementActions
from base.environment import EnvironmentAndroid
from base.utils import log
import allure

#pytest的setup和down工作


#初始化driver对象，在package的领域只会执行一次
@pytest.fixture("package")
def driverenv():
    env=EnvironmentAndroid()
    capabilities = {'platformName': env.devices.get("platformName"),
                    'platformVersion': env.devices.get("platformVersion"),
                    'deviceName': env.devices.get("deviceName"),
                    'app': env.appium.get("app"),
                    'clearSystemFiles': True,
                    'appActivity': env.appium.get("appActivity"),
                    'appPackage': env.appium.get("appPackage"),
                    'automationName': 'UIAutomator2',
                    'noSign': True,
                    'recreateChromeDriverSessions': True,
                    "unicodeKeyboard": "True",
                    "noReset":True,
                    "fullReset":False
                    }
    host = env.appium.get("host")
    driver = webdriver.Remote(host, capabilities)

    return driver


#初始化ElementActions类的对象，在package的领域只会执行一次，并且通过yield实现package执行结束前的数据清理工作
@pytest.fixture("package")
def action(driverenv):
    element_action=ElementActions(driverenv)
    log.info("\n初始化driver")
    yield element_action   #返回并且挂载ElementActions的实例，在对应作用域结束前，执行driver.quit()

    element_action.driver.quit()


#用例执行前后：加入日志说明、结束前的截图输出到报告上
@pytest.fixture(autouse=True)
def caserun(action):
    log.info("————————————————————————执行用例 ----------——————————————" )
    yield
    # element_action=ElementActions(driverenv)
    action.sleep(1).get_img("用例结束前的截图")
    log.info("————————————————————————该用例执行结束 ----------——————————————")










