import os,abc,yaml
from base.shell import *
from base.utils import log,singleton



#环境的抽象类
class Environment(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def check_environment(self):
        pass

    @abc.abstractmethod
    def get_conf(self):
        pass



@singleton
class EnvironmentAndroid(Environment):
    def __init__(self):
        self.conf=self.get_conf()
        self.appium = self.conf.get("appium")  #key: apk、appActivity、appPackage、version
        self.path=self.conf.get("path")
        self.devices=self.conf.get("devices")

        #最开始运行时动态获取，存储suit和device的对应关系
        self.current_device={}

        self.current_path=None


    def get_conf(self):

        environment_info_path = str(
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/config_android.yaml")))

        log.info('获取环境配置 Path:' + environment_info_path)
        with open(environment_info_path,"r") as f:
            conf=yaml.load(f)

        return conf

    def callback_current_device(self,device:dict):
        #传入当前的device信息
        self.current_device=device

    def callback_current_path(self,current_path):

        self.current_path=current_path




    def check_environment(self):
        log.info('检查环境...')

        # 判断是否设置环境变量ANDROID_HOME
        if "ANDROID_HOME" in os.environ:
            command = os.path.join(
                os.environ["ANDROID_HOME"],
                "platform-tools",
                "adb")
        else:
            raise EnvironmentError(
                "Adb not found in $ANDROID_HOME path: %s." %
                os.environ["ANDROID_HOME"])

        # 检查设备
        current_devices = Device.get_android_devices()
        if len(current_devices)==0:
            log.info('没有设备连接')
            exit()
        for device in self.devices:
            deviceName=device.get("deviceName")
            if deviceName in current_devices:
                log.info('已正常连接设备{}'.format(deviceName))
            else:
                log.error('设备{}未正常连接'.format(deviceName))



        # 检查appium版本
        appium_v= Shell.invoke('appium -v')
        if self.appium.get("version") not in appium_v:
            log.info('appium 版本有问题')
            exit()
        else:
            log.info('appium version {}'.format(appium_v))

        #检测appium-doctor输出
        result=Shell.invoke('appium-doctor').splitlines()
        log.info(result)

@singleton
class EnvironmentIOS(Environment):
    pass





