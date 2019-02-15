# -*- coding: utf-8 -*-

from base.utils import Conf
from lib.pages.set import ProductPages as p, UserCenterPage as up
from lib.reuse_business import base_business


conf=Conf()


if conf.platform==conf.androidname:
    from base.conftest_android import *
elif conf.platform==conf.iosname:
    from base.conftest_ios import *


@pytest.fixture('package',autouse=True)
def suitinit(action):
    # p.特卖首页.home(action)
    # base_business.set_appenv(action)
    # p.特卖首页.pageinto(action)
    base_business.login(action,'user1')
    # action.back_press()
    pass










