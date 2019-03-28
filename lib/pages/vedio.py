from base.page import BasePage
from base.action import ElementActions
from base.utils import log



class VideoReleasePage(BasePage):
    name="视频发布页"

    def load_android(self):

        #有多个，通过index来选择视频
        self.视频选择=self.get_locator('视频选择','id','com.jm.android.jumei:id/iv_thumb')

        self.视频选择后下一步=self.get_locator('选择后下一步','id','com.jm.android.jumei:id/save_button1')
        self.视频处理后下一步 = self.get_locator('处理后下一步', 'id', 'com.jm.android.jumei:id/btn_next')
        self.视频发布=self.get_locator('视频发布','id','com.jm.android.jumei:id/social_publish_submit')
        self.视频描述=self.get_locator('视频描述','id','com.jm.android.jumei:id/social_input_txt')
