
from base.action import ElementActions
from base.utils import log,ArgsData
from lib.pages.set import ProductPages as p,UserPages as up




def login(action:ElementActions,user='user1'):
    """
    让app处于登陆状态，已登陆时则不登陆,登陆后处于在用户中心页
    默认使用args_data中的user1登陆
    """

    up.用户中心.pageinto(action)
    if up.用户中心.is_logined(action) == False:
        action.click(up.用户中心.注册登陆)

        user = ArgsData().users.get(user)
        up.登录页.login(action, user[0],user[1])
        log.info('登陆成功')
    else:
        log.info('app已登陆')



def logout(action:ElementActions):
    """让app处于登出状态，未登陆则不操作, 登出后处于用户中心页"""

    up.用户中心.pageinto(action)
    if up.用户中心.is_logined(action) == True:
        action.click(up.用户中心.设置按钮)
        action.click(up.设置页.退出账号)
        log.info('登出成功')
    else:
        log.info('app已登出')




def set_appenv(action:ElementActions):
    # 设置环境为测试环境

    up.设置页.pageinto(action)

    if not action.is_text_displayed('开发者选项'):
        log.info('没有开发者选项，先启动调试模式~')

        action.click(up.设置页.关于聚美按钮)

        action.click(up.设置页.版本号, count=8)

        for index in range(2):
            action.click(up.设置页.版本号)
            if action.is_toast_show('调试', wait=3) != False:
                break
        action.back_press()

    action.click(up.设置页.开发者选项)
    if action.is_text_displayed('测试环境') == True:
        log.info('环境已设置为测试环境')
    else:
        action.click(up.设置页.后台环境)
        action.sleep(1).click(up.设置页.测试环境按钮)
        action.sleep(5)
        log.info('切换到测试环境成功')





