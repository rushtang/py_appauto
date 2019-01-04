# -*- coding: utf-8 -*-
import os,sys,pytest
from base.utils import log
from base.environment import EnvironmentAndroid

import subprocess




#Device类，用get_android_devices返回执行adb devices命令时的devices信息（即获取当前链接的机子devicename）
class Device:
    @staticmethod
    def get_android_devices():
        android_devices_list = []
        for device in Shell.invoke('adb devices').splitlines():
            if 'device' in device and 'devices' not in device:
                device = device.split('\t')[0]
                android_devices_list.append(device)
        return android_devices_list



class Shell:
    @staticmethod
    def invoke(cmd,cwd=None,is_log=True):
        # shell设为true，程序将通过shell来执行
        # stdin, stdout, stderr分别表示程序的标准输入、输出、错误句柄。
        # 他们可以是PIPE，文件描述符或文件对象，也可以设置为None，表示从父进程继承。
        # subprocess.PIPE实际上为文本流提供一个缓存区
        if is_log==True:
            log.info("执行命令: {}".format(cmd))
        p= subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=cwd)
        output, errors=p.communicate()
        o = output.decode("utf-8")
        return o

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



class ADB:
    """
      参数:  device_id
    """

    def __init__(self, device_id=""):

        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-s %s" % device_id

    def adb(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return Shell.invoke(cmd)

    def shell(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args),)
        return Shell.invoke(cmd)

    def get_device_state(self):
        """
        获取设备状态： offline | bootloader | device
        """
        return self.adb("get-state").stdout.read().strip()

    def get_device_id(self):
        """
        获取设备id号，return serialNo
        """
        return self.adb("get-serialno").stdout.read().strip()

    def get_android_version(self):
        """
        获取设备中的Android版本号，如4.2.2
        """
        return self.shell(
            "getprop ro.build.version.release").strip()

    def get_sdk_version(self):
        """
        获取设备SDK版本号
        """
        return self.shell("getprop ro.build.version.sdk").strip()


