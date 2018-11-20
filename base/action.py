# -*- coding: utf-8 -*-

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from base.utils import log,singleton,Waittime_count
import allure,time
from base.exceptions import NotFoundElementError,NotFoundTextError
from base.environment import EnvironmentAndroid




#封装元素操作的类


@singleton
class ElementActions:
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']
        self.env = EnvironmentAndroid()
    def reset(self, driver: webdriver.Remote):
        """因为是单例,所以当driver变动的时候,需要重置一下driver

        Args:
            driver: driver

        """
        self.driver = driver
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']
        return self
    def reset_attribute(self):
        #重置坐标
        log.info("重置driver坐标")
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']



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
        self.sleep(2,islog=False)
        return self


    def sleep(self,s,islog=True):
        if islog==True:
            message="sleep等待 {} s ".format(str(s))
            log.info(message)
        time.sleep(s)
        return self

    def back_press(self):
        self._send_key_event('KEYCODE_BACK')



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


    def find_ele_recursive(self,element,locator,is_Multiple=False,wait=5):
        # 通过元素对象来串联查找,返回元素对象  (属于通过父结点元素递归查找子结点元素)
        # 需要查找多个时，返回list
        #当前串联查询不执行name的定位方式
        """
        Args:
            element: self.driver.find_element函数的返回值，即元素对象
            locator:  定位器对象
            is_Multiple: 是否查找多个，查找单个时只会返回第一个找到的元素对象
        """
        if 'timeOutInSeconds' in locator:
            wait = locator['timeOutInSeconds']
        else:
            wait = wait

        value = locator['value']
        ltype = locator['type']
        log.info("串联查找页面【{}】的元素【{}】\n element:{}".format(locator.get("page"), locator.get("name"),element))
        try:
            WebDriverWait(self.driver, wait).until(
                lambda driver: self._get_element_by_type(driver, locator, False).__len__() > 0)
            if is_Multiple == False:
                return element.find_element(ltype, value)
            else:
                return element.find_elements(ltype, value)

        except:
            log.info("串联查找未找到  locator: {} \n element:{}  ".format(element,str(locator)))
            return None


    def find_ele(self,locator,is_Multiple=False):
        #通过定位器查找元素
        #需要查找多个时，返回list
        #没有查找到时，返回None 或 []

        """
               Args:
                   locator:  定位器对象
                   is_Multiple: 是否查找多个
        """


        log.info("查找 页面【{}】的元素【{}】".format(locator.get("page"), locator.get("name")))
        if is_Multiple==False:
            return self._find_element(locator,is_raise=False)
        else:
            return self._find_elements(locator,is_raise=False)


    def find_ele_traversing(self,elements,target_ele_locator,return_ele_locator=None):
        #对list的元素对象组进行遍历，查找其元素子节点中目标元素对象是否存在,如果存在返回需要返回的元素对象
        #通过遍历没有找到符合条件的元素时，返回None
        #默认返回目标元素的父节点元素对象
        """
            Args:
                elements:  self.driver.find_elements函数的返回值，即元素对象的list组
                target_ele_locator:  目标查找元素的定位器对象
                return_ele_locator:  返回元素的定位器对象
        """

        log.info("遍历查找 页面【{}】的元素【{}】".format(target_ele_locator.get("page"), target_ele_locator.get("name")))
        for element in elements:
            target_ele=self.find_ele_recursive(element,target_ele_locator,wait=1.5)
            if target_ele!=None:
                if return_ele_locator == None:
                    log.info("成功遍历查找到元素 {}".format(element))
                    return element
                else:
                    log.info(
                        "成功遍历查找到 页面【{}】的元素【{}】".format(return_ele_locator.get("page"), return_ele_locator.get("name")))
                    return element.find_element(return_ele_locator)

        return None





    def is_element_exist(self, locator):
        """检查元素是否存在"""

        if self._find_element(locator,is_raise=False)==None:
            log.error("没有查找到  页面【{}】的元素【{}】".format(locator.get("page"),locator.get("name")))
            return False
        else:
            log.info("已查找到  页面【{}】的元素【{}】".format(locator.get("page"),locator.get("name")))
            return True


    def click(self, locator, count=1):
        """基础的点击事件

        Args:
            locator:定位器
            count: 点击次数
        """
        msg="[点击]  页面【{}】的元素【{}】".format(locator.get("page"),locator.get("name"))
        log.info(msg)
        element = self._find_element(locator)

        self.click_ele(element,count,is_log=False)
        return self


    def click_ele(self,element,count=1,is_log=True):
        #对元素对象进行点击
        if is_log==True:
            log.info("[点击]元素 {}".format(element))

        self.sleep(0.5, islog=False)
        waittime_count=Waittime_count()
        waittime_count.start()

        if count == 1:


            element.click()
        else:
            touch_action = TouchAction(self.driver)
            try:
                for x in range(count):
                    touch_action.tap(element).perform()
            except:
                pass

        waittime_count.end()

        self.sleep(1.5, islog=False)

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




    def is_toast_show(self, message, wait=15):
        """Android检查是否有对应Toast显示,常用于断言

        Args:
            message: Toast信息
            wait:  等待时间,默认15秒

        Returns:
            True 显示Toast

        """
        locator = {'name': '[Toast] %s' % message, 'timeOutInSeconds': wait, 'type': 'xpath',
                   'value': '//*[contains(@text,\'%s\')]' % message}
        try:
            el = self._find_element(locator, is_need_displayed=False)
            return el is not None
        except NotFoundElementError:
            log.error("[Toast] 页面中未能找到 %s toast" % locator)
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
        locator = {'name': '对话框确认键', 'timeOutInSeconds': wait, 'type': 'id', 'value': 'android:id/button1'}
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


    def _find_element(self, locator, is_need_displayed=True,wait = 10,is_raise=True):
        """查找单个元素,如果有多个返回第一个

        Args:
            locator: 定位器
            is_need_displayed: 是否需要定位的元素必须展示
            is_raise: 是否抛出异常

        Returns: 元素 ,没找到返回 None

        Raises: NotFoundElementError
                未找到元素会抛 NotFoundElementError 异常

        """
        if 'timeOutInSeconds' in locator:
            wait = locator['timeOutInSeconds']
        else:
            wait = wait
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


    def _find_elements(self, locator,wait = 10,is_raise=False):
        """查找元素,可查找出多个

        Args:
            locator: 定位器
            is_raise: 是否抛出异常

        Returns:元素列表 或 []

        """
        if 'timeOutInSeconds' in locator:
            wait = locator['timeOutInSeconds']
        else:
            wait = wait

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

        #uiautomator不懂，有时间研究一下
        #find_element不支持通过name查找,但uiautomator可以且速度快
        if ltype == 'name':
            ui_value = 'new UiSelector().textContains' + '(\"' + value + '\")'
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
