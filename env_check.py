from base.shell import Shell
from base.utils import log
from base.environment import EnvironmentAndroid


#检测环境和启动appium


if __name__ == '__main__':
    # # log.info("启动appium")
    # # output=Shell.invoke('appium --address 127.0.0.1 --port 4723  --local-timezone --session-override')
    # log.info(output)
    env=EnvironmentAndroid()
    env.check_environment()


