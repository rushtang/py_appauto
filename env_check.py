from base.shell import Shell
from base.utils import log
from base.environment import EnvironmentAndroid


#检测环境和启动appium


if __name__ == '__main__':
    env=EnvironmentAndroid()
    env.check_environment()


