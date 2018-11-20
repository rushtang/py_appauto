# -*- coding: utf-8 -*-

import pytest
from appium import webdriver
from base.action import ElementActions
from base.environment import EnvironmentIOS
from base.utils import log
import allure

#pytest的setp和down工作



@pytest.fixture("session")
def env():
    return EnvironmentIOS()




@pytest.fixture(autouse=True)
def caselog():
    log.info("————————————————————————执行用例 ----------——————————————" )
    yield
    log.info("————————————————————————该用例执行结束 ----------——————————————")










