import logging,os,yaml,copy,time






#单例装饰器
def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance

@singleton
class Conf():
    def __init__(self):
        self.config_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "data/config.yaml")))
        self.info=self.get_info()
        self.androidname='android'
        self.iosname='ios'
        self.platform=self.info.get('platform')['run']

    def get_info(self):

        with open(self.config_path, "r") as f:
            info = yaml.load(f)
        return info

    def set_info(self):
        with open(self.config_path, "w") as f:
            yaml.dump(self.info,f)

    def set_platform(self,platform):
        log.info("设置平台为：{}".format(platform))
        d=copy.deepcopy(self.info)
        d['platform']['run']=platform
        self.info=d
        self.set_info()





class Logbuilder():
    def __init__(self, loggername,loglevel=None):

        self.loggername=loggername


    def getlog(self):

        # 创建一个logger
        self.logger = logging.getLogger(self.loggername)
        self.logger.setLevel(logging.INFO)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(name)s %(levelname)s %(asctime)s \n %(message)s', "%H:%M:%S")


        # 创建一个handler，添加handler,用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)

        return self.logger



log=Logbuilder("log:").getlog()


def get_attrsname(obj):
    #获取当前对象的非私有的属性名字列表

    attrs=[attr for attr in dir(obj) if not callable(attr) and not attr.startswith("__")]

    return attrs


class Waittime_count:
    #用于计算一个步骤的执行时间，如果超出规定时间就输出日志

    def __init__(self,msg="等待时间有：",durationtime=8):
        self.msg=msg
        self.starttime=None
        self.endtime=None
        self.durationtime=durationtime


    def start(self):
        self.starttime=time.time()

    def end(self):
        self.endtime=time.time()
        Waittime=round(self.starttime - self.endtime, 2)
        if Waittime>self.durationtime:
            log.info(self.msg+" {}s ".format(Waittime))

