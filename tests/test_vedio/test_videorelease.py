#-*- coding: utf-8 -*-

from base.action import ElementActions
from lib.pages.set import ProductPages as p, UserPages as up,VedioPages as vp
from base.verify import Validator,NotFoundElementError
from base.utils import log
from flaky import flaky



class Test_videorelease():

    def test_case1(self,action):
        count=5
        action.click(p.特卖首页.发布)

        for index in range(count):
            action.click(p.特卖首页.发布_上传视频)
            videoele=action.find_ele(vp.视频发布页.视频选择,is_Multiple=True)[0]
            action.click_ele(videoele)

            action.click(vp.视频发布页.视频选择后下一步).click(vp.视频发布页.视频处理后下一步)

            action.sleep(8).click(vp.视频发布页.视频发布,wait=15)

            result=action.is_toast_show('视频发布成功',wait=20)
            log.info('result: {}'.format(result))
            action.get_img('上传后截图')

            action.back_press()







