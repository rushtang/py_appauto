# -*- coding: utf-8 -*-

import pytest

from base.utils import Conf

conf=Conf()

if conf.platform==conf.androidname:
    from base.conftest_android import *
elif conf.platform==conf.iosname:
    from base.conftest_ios import *
else:
    from base.conftest_android import *


#运行时通过执行的配置的平台决定导入的模块
#导入base.conftest里的pytest上下文环境函数:driverenv、action(ElementActions的实例)、caselog
#pytest框架运行原理：先运行test文件夹下面的conftest.py，然后才运行带test开头的py文件
#具体详情，请看base.conftest的注释











