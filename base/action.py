# -*- coding: utf-8 -*-

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from base.utils import log,singleton,Waittime_count
import allure,time
from base.verify import NotFoundElementError,NotFoundTextError
from base.environment import EnvironmentAndroid




#封装元素操作的类


@singleton
class ElementActions:
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.env = EnvironmentAndroid()
        #通过driver.get_window_size()获取的分辨率会不准确，所以读取配置的Resolution
        self.Resolution =self.env.current_device.get('Resolution')

        if self.Resolution==None:
            self.Resolution=[1080, 1920]

        self.width =self.Resolution[0]
        self.height =self.Resolution[1]

    def reset(self, driver: webdriver.Remote):
        """因为是单例,所以当driver变动的时候,需要重置一下driver

        Args:
            driver: driver

        """
        self.driver = driver



    def get_img(self,name="app截图"):
        #获取当前app的截图并加载到报告的对应附件中

        png_data=self.driver.get_screenshot_as_png()
        current_time = time.strftime('_%H:%M:%S_', time.localtime(time.time()))
        current_name=name+current_time+ '.png'

        allure.attach(png_data,name=current_name,attachment_type=allure.attachment_type.PNG)


    def start_activity(self, app_activity, **opts):
        message='start_activity:    '+app_activity
        log.info(message)
        self.driver.start_activity(self.env.appium.get("appPackage"), app_activity, **opts)

        self.driver.wait_activity(app_activity, 10, interval=0.3)
        return self


    def sleep(self,s,islog=True):
        if islog==True:
            message="sleep等待 {} s ".format(str(s))
            log.info(message)
        time.sleep(s)
        return self

    def back_press(self):
        self._send_key_event('KEYCODE_BACK')


    def tap(self,locator):
        #获取当前屏幕的分辨率，元素通过相对位置点击
        """

        :param locator: value格式为 "x,y"
        :return:
        """
        if locator.get('type')!="tap":
            log.error('定位方式错误，不能通过坐标位置定位点击 \nlocator: {}'.format(str(locator)))
        else:
            position=locator.get('value').split(',')
            x=int(position[0])*self.width/1080
            y=int(position[1])*self.height/1920
            positions=[(x,y)]
            log.info("通过坐标({},{}), 成功点击 页面【{}】的元素【{}】".format(x,y,locator.get('page'),locator.get('name')))

            self.driver.tap(positions,duration=400)

    def long_press(self,locator,time=2000):
        #长按操作，locator的type为tap时支持坐标位置长按
        """
        :param locator:
        :param time: 单位毫秒
        :return:
        """
        if locator.get('type')=="tap":
            position = locator.get('value').split(',')
            x = int(position[0]) * self.width / 1080
            y = int(position[1]) * self.height / 1920
            TouchAction(self.driver).long_press(x=x,y=y,duration=time).perform()

        else:
            ele=self._find_element(locator)
            TouchAction(self.driver).long_press(el=ele, duration=time).perform()

        log.info("[长按] 页面【{}】的元素【{}】".format(locator.get('page'), locator.get('name')))




    def swip_left(self, count=1):
        """向左滑动,一般用于ViewPager

        Args:
            count: 滑动次数

        """

        for x in range(count):
            self.driver.swipe(self.width * 9 / 10, self.height / 2, self.width / 10, self.height / 2, 1000)
        log.info("----------向左滑动----------")
        return self

    def swip_right(self,count=1):
        """
            向右滑
        """

        for x in range(count):
            self.driver.swipe(self.width / 10, self.height / 2, self.width * 9/ 10, self.height / 2, 1000)
        log.info("----------向右滑动----------")
        return self

    def swip_down(self, count=1,half=False):
        """向下滑动,常用于下拉刷新

        Args:
            count: 滑动次数
            half:是否为滑动一半
        """
        for x in range(count):
            if half==False:
                self.driver.swipe(self.width / 2, self.height * 9 / 10, self.width / 2, self.height * 1 / 10, 1000)
            else:
                self.driver.swipe(self.width / 2, self.height * 3 / 5, self.width / 2, self.height * 1 / 5, 1000)
        log.info("---------向下滑动----------")
        return self

    def swip_up(self, count=1):
        """向上滑动,常用于下拉刷新

        Args:
            count: 滑动次数
        """

        for x in range(count):
            self.driver.swipe(self.width / 2, self.height *1 / 10, self.width / 2, self.height * 9 / 10, 1000)

        log.info("----------向上滑动---------")
        return self



    def find_ele_child(self, locator_parent, locator_child, is_Multiple=False, wait=8):
        # 通过父结点定位方式查找子结点元素
        #定位方式限制：如果子节点定位方式为name时，父节点定位方式只能为id、name、class name

        """
        :param locator_parent: 父节点定位器对象
        :param locator_child:  子节点定位器对象
        :param is_Multiple: 是否查找多个
        :param wait:
        :return: 查找不到时返回None或者[]
        """

        if locator_child['type'] != 'name':
            element_parent = self.find_ele(locator_parent)
            return  self.find_ele_child_byelement(element_parent,locator_child,is_Multiple,wait)
        else:
            return  self._find_ele_child_byname(locator_parent, locator_child, is_Multiple,wait)


    def find_ele_child_byelement(self, element_parent, locator_child, is_Multiple=False, wait=6):
        #通过父结点元素查找子结点元素,不支持name定位方式

        if locator_child['type'] == 'name':
            log.error('find_ele_child_byelement的定位方式错误')
            raise NotFoundElementError

        value_child, type_child = locator_child['value'], locator_child['type']
        try:
            WebDriverWait(self.driver, wait).until(
                lambda driver: element_parent.find_element(type_child, value_child))

            log.info(
                "页面【{}】的元素【{}】成功查询到查找子节点 元素【{}】"
                    .format(locator_child.get("page"), element_parent,
                            locator_child.get('name')))

            if is_Multiple == False:
                return element_parent.find_element(type_child, value_child)
            else:
                return element_parent.find_elements(type_child, value_child)
        except:
            log.info(
                "页面【{}】的元素【{}】未能查询到查找子节点 元素【{}】\n locator_child{}"
                    .format(locator_child.get("page"), element_parent,
                            locator_child.get('name'), locator_child))

            if is_Multiple == False:
                return None
            else:
                return []


    def find_ele_parent(self, locator_parent,locator_child,wait=2):
        # 通过子节点来定位父节点元素,locator_parent有多个元素（通过遍历父节点，找出包含符合条件子节点的父节点）
        #定位方式限制 子节点 定位方式不能是name

        if locator_child['type'] == 'name':
            log.error('find_ele_parent的定位方式错误')
            raise NotFoundElementError

        elelist_parent = self.find_ele(locator_parent, is_Multiple=True)

        for element_parent in elelist_parent:
            child_eles=self.find_ele_child_byelement(element_parent,locator_child,is_Multiple=True,wait=wait)
            log.info(child_eles)

            if child_eles!=[]:
                    log.info("成功遍历查找到元素 {}".format(child_eles))
                    return element_parent
        log.info('未找到元素, elelist_parent:{}'.format(str(elelist_parent)))

        return None


    def find_ele_fromparent(self,locator_tmp,locator_target,is_Multiple=False,wait=5):
        #通过uiautomator查找定位元素的兄弟节点元素,不支持xpath，且兄弟节点必须同级
        """
        支持的定位方式有：text(name),description(特有的),id,class name
        """

        log.info("页面【{}】通过元素【{}】查找兄弟元素【{}】".format(locator_tmp.get("page"), locator_tmp.get('name'), locator_target.get("name")))

        map={
            "name":"textContains",
            "description":"descriptionContains",
            "id":"resourceId",
            "class name":"className"
        }
        type_tmp=map.get(locator_tmp["type"])
        type_target=map.get(locator_target["type"])

        if type_tmp==None or type_target==None:
            log.error('当前定位方式不支持')
            raise NotFoundElementError

        value_tmp=locator_tmp["value"]
        value_target =locator_target["value"]


        ui_value='new UiSelector().{}(\"{}\").fromParent(new UiSelector().{}(\"{}\"))'.format(type_tmp,value_tmp,type_target,value_target)


        try:
            WebDriverWait(self.driver, wait).until(
            lambda driver: driver.find_element_by_android_uiautomator(ui_value))

            if is_Multiple == False:
                return self.driver.find_element_by_android_uiautomator(ui_value)
            else:
                return self.driver.find_elements_by_android_uiautomator(ui_value)

        except:
            log.info('页面【{}】未找到 元素【{}】\n locator: {}'.format(locator_tmp.get("page"), locator_target.get('name'),str(locator_target)))
            if is_Multiple == False:
                return None
            else:
                return []


    def find_ele(self,locator,is_Multiple=False,wait = 5):
        #通过定位器查找元素,不用于断言（断言元素存在用 is_element_exist ，断言页面是否含有对应文本关键字的请用is_text_displayed）
        #需要查找多个时，返回list
        #没有查找到时，返回None 或 []

        """
               Args:
                   locator:  定位器对象
                   is_Multiple: 是否查找多个
        """


        log.info("查找 页面【{}】的元素【{}】".format(locator.get("page"), locator.get("name")))
        if is_Multiple==False:
            return self._find_element(locator,is_raise=False,wait=wait)
        else:
            return self._find_elements(locator,is_raise=False,wait=wait)





    def is_element_exist(self, locator,wait=2):
        """检查元素是否存在"""

        if self._find_element(locator,is_raise=False,wait=wait)==None:
            log.error("没有查找到  页面【{}】的元素【{}】".format(locator.get("page"),locator.get("name")))
            return False
        else:
            log.info("已查找到  页面【{}】的元素【{}】".format(locator.get("page"),locator.get("name")))
            return True


    def click(self, locator, count=1,wait=5):
        """基础的点击事件

        Args:
            locator:定位器
            count: 点击次数
        """
        msg="[点击]  页面【{}】的元素【{}】".format(locator.get("page"),locator.get("name"))
        log.info(msg)

        element = self._find_element(locator,wait=wait)

        self.click_ele(element,count,is_log=False)

        return self


    def click_ele(self,element,count=1,is_log=True):
        #对元素对象进行点击
        if is_log==True:
            log.info("[点击]{}次元素 {}".format(count,element))


        if count == 1:

            element.click()
        else:
            touch_action = TouchAction(self.driver)
            try:
                for x in range(count):
                    self.sleep(0.1, islog=False)
                    touch_action.tap(element).perform()
            except:
                pass


        self.sleep(0.1, islog=False)

        return self




    def get_text(self, locator):
        """获取元素中的text文本
        查找到单个元素，返回文本字符串

        Args:
            locator:定位器
            count: 点击次数

        Returns:
            如果没有该控件返回None

        Examples:
            TextView 是否显示某内容
        """
        element = self._find_element(locator,wait=1)
        log.info("获取元素中的text文本\n locator: \n{}".format(locator))
        return self.get_text_ele(element)

    def get_text_ele(self,element):
        if element != None:
            return element.get_attribute("text")
        else:
            return None





    def text(self, locator, value, clear_first=False, click_first=True):
        """输入文本

        Args:
            locator: 定位器
            value: 文本内容
            clear_first: 是否先清空原来文本
            click_first: 是否先点击选中
        Raises:
            NotFoundElementError

        """
        element=self._find_element(locator)
        log.info("在【{}】页面 对元素【{}】输入文本【{}】".format(locator.get("page"), locator.get("name"), value))

        self.text_ele(element,value,clear_first, click_first)

        return self
    def text_ele(self,element,value,clear_first=False, click_first=True):

        if click_first:
            element.click()
        if clear_first:
            element.clear()
        element.send_keys(value)




    def is_toast_show(self, message, wait=5):
        """Android检查是否有对应Toast显示,常用于断言

        Args:
            message: Toast信息
            wait:  等待时间

        Returns:
            True 显示Toast

        """

        toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % message)
        try:
            WebDriverWait(self.driver, wait, 0.2).until(expected_conditions.presence_of_element_located(toast_loc))

            log.info("当前页面成功找到toast: %s" % message)
            return True

        except :
            log.error("当前页面中未能找到toast为: %s" % message)

            return False

    def is_text_displayed(self, text, retry_time=0, is_raise=False):
        """检查页面中是否有文本关键字

        如果希望检查失败的话,不再继续执行case,使用 is_raise = True

        Args:
            text: 关键字(请确保想要的检查的关键字唯一)
            is_retry: 是否重试,默认为true
            retry_time: 重试次数,默认为5
            is_raise: 是否抛异常
        Returns:
            True: 存在关键字
        Raises:
            如果is_raise = true,可能会抛NotFoundElementError

        """

        try:
            if retry_time!=0:
                result= WebDriverWait(self.driver, retry_time).until(
                    lambda driver: self._find_text_in_page(text))
            else:
                result=self._find_text_in_page(text)
            if result == True:
                log.info("[Text]页面中找到了 %s 文本" % text)
            return result
        except TimeoutException:
            log.error("[Text]页面中未找到 %s 文本" % text)
            if is_raise:
                raise NotFoundTextError
            else:
                return False


    def dialog_ok(self, wait=5):
        locator = {'name': '对话框确认键', 'type': 'id', 'value': 'android:id/button1'}
        self.click(locator)

    def set_number_by_soft_keyboard(self, nums):
        """模仿键盘输入数字,主要用在输入取餐码类似场景

        Args:
            nums: 数字
        """
        list_nums = list(nums)
        for num in list_nums:
            self._send_key_event('KEYCODE_NUM', num)


    # ======================= private ====================

    def _find_ele_child_byname(self, locator_parent, locator_child, is_Multiple=False, wait=8):
        #使用uiautomator通过父节点，定位子节点。

        value_parent, type_parent = locator_parent['value'], locator_parent['type']
        value_child, type_child = locator_child['value'], locator_child['type']

        try:
            map = {
                "name": "textContains",
                "id": "resourceId",
                "class name": "className"
            }
            type_parent = map.get(type_parent)

            if type_parent == None:
                log.error('当前定位方式不支持')
                raise NotFoundElementError

            ui_value = 'new UiSelector().{}(\"{}\").childSelector(new UiSelector().textContains(\"{}\"))'.format(
                type_parent, value_parent, value_child)

            WebDriverWait(self.driver, wait).until(
                lambda driver: driver.find_element_by_android_uiautomator(ui_value))

            log.info("页面【{}】的元素【{}】成功查找子节点 元素【{}】".format(locator_parent.get("page"), locator_parent.get("name"),
                                                        locator_child.get('name')))

            if is_Multiple == False:
                return self.driver.find_element_by_android_uiautomator(ui_value)
            else:
                return self.driver.find_elements_by_android_uiautomator(ui_value)


        except:
            log.info(
                "页面【{}】的元素【{}】未能查询到查找子节点 元素【{}】\n locator_parent:{} \n locator_child{}"
                    .format(locator_parent.get("page"), locator_parent.get("name"),
                            locator_child.get('name'), locator_parent, locator_child))

            if is_Multiple == False:
                return None
            else:
                return []



    def _find_text_in_page(self, text):
        """检查页面中是否有文本关键字
        拿到页面全部source,暴力检查text是否在source中
        Args:
            text: 检查的文本

        Returns:
            True : 存在

        """
        log.info("[查找] 文本 %s " % text)

        return text in self.driver.page_source


    def _find_element(self, locator, is_need_displayed=True,wait = 5,is_raise=True):
        """查找单个元素,如果有多个返回第一个

        Args:
            locator: 定位器
            is_need_displayed: 是否需要定位的元素必须展示
            is_raise: 是否抛出异常

        Returns: 元素 ,没找到返回 None

        Raises: NotFoundElementError
                未找到元素会抛 NotFoundElementError 异常

        """

        waittime_count=Waittime_count(msg='[查找] 页面【{}】该元素【{}】等待时间:'.format(locator.get("page"),locator.get("name")))
        waittime_count.start()
        try:
            if is_need_displayed:
                WebDriverWait(self.driver, wait).until(
                    lambda driver: self._get_element_by_type(driver, locator).is_displayed())
            else:
                WebDriverWait(self.driver, wait).until(
                    lambda driver: self._get_element_by_type(driver, locator) is not None)

            waittime_count.end()
            return self._get_element_by_type(self.driver, locator)
        except Exception as e:

            if is_raise==True:
                log.error(
                    "【{}】页面中未能找到元素【{}】\n locator: \n {}".format(locator.get("page"), locator.get("name"), locator))
                raise NotFoundElementError
            else:
                return None


    def _find_elements(self, locator,wait = 6,is_raise=False):
        """查找元素,可查找出多个

        Args:
            locator: 定位器
            is_raise: 是否抛出异常

        Returns:元素列表 或 []

        """
        try:
            WebDriverWait(self.driver, wait).until(
                lambda driver: self._get_element_by_type(driver, locator, False).__len__() > 0)
            return self._get_element_by_type(self.driver, locator, False)
        except:

            if is_raise == True:
                log.error(
                    "【{}】页面中未能找到元素【{}】\n locator: \n {}".format(locator.get("page"), locator.get("name"), locator))
                raise NotFoundElementError
            else:
                return []

    @staticmethod
    def _get_element_by_type(driver, locator, element=True):
        """通过locator定位元素(默认定位单个元素)

        Args:
            driver:driver
            locator:定位器
            element:
                true:查找单个元素
                false:查找多个元素

        Returns:单个元素 或 元素list

        """
        value = locator['value']
        ltype = locator['type']


        #find_element在安卓中appium定位不支持通过name查找,但uiautomator可以且速度快
        if ltype == 'name':
            ui_value = 'new UiSelector().textContains(\"{}\")'.format(value)
            return driver.find_element_by_android_uiautomator(
                ui_value) if element else driver.find_elements_by_android_uiautomator(ui_value)
        else:
            return driver.find_element(ltype, value) if element else driver.find_elements(ltype, value)

    def _send_key_event(self, arg, num=0):
        """
        操作实体按键
        Code码：https://developer.android.com/reference/android/view/KeyEvent.html
        Args:
            arg: event_list key
            num: KEYCODE_NUM 时用到对应数字

        """
        event_list = {'KEYCODE_HOME': 3, 'KEYCODE_BACK': 4, 'KEYCODE_MENU': 82, 'KEYCODE_NUM': 8}
        if arg == 'KEYCODE_NUM':
            self.driver.press_keycode(8 + int(num))
        elif arg in event_list:
            self.driver.press_keycode(int(event_list[arg]))
