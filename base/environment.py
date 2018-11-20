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
        self.get_conf()
        self.appium = self.conf.get("appium")  #key: apk、appActivity、appPackage、version
        self.report=self.conf.get("report")  #key: html_report、xml_report
        self.devices=self.conf.get("devices")  #key: deviceName、platformName、platformVersion


    def get_conf(self):

        environment_info_path = str(
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/config_android.yaml")))

        log.info('获取环境配置 Path:' + environment_info_path)
        with open(environment_info_path,"r") as f:
            self.conf=yaml.load(f)

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
        devices = Device.get_android_devices()
        env_devices=self.devices.get("deviceName")
        if not devices:
            log.info('没有设备连接')
            exit()
        elif env_devices not in devices:
            log.info('已连接设备:{}不包含设备{}',format(devices,env_devices))
        else:
            log.info('已设备连接{}'.format(env_devices))



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





