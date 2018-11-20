from base.shell import Shell
from base.utils import log,Conf
from base.environment import EnvironmentAndroid
import os,jprops,allure




class Run():

    def __init__(self,platform=Conf().androidname):

        self.conf=Conf()
        self.conf.set_platform(platform)  # 设置执行平台

        self.env=EnvironmentAndroid()

        self.xml_report_path =os.path.join(self.env.report.get("dir"),'xml')
        self.html_report_path = os.path.join(self.env.report.get("dir"),'html')
        self.properties_path=os.path.join(self.xml_report_path,'environment.properties')

    def get_run_args(self):

        log_format = '--log-format=%(name)s%(levelname)s %(asctime)s   \n %(message)s \n'
        log_date_format = '--log-date-format=%H:%M:%S'
        args = ['-s', '-q', log_format, log_date_format, '--alluredir', self.xml_report_path, "--verbose"]

        return args

    def generate_report(self):

        #给报告中添加执行环境信息
        env_dict={}
        env_dict.update(self.env.conf)
        env_dict.update(self.conf.info)
        env_properties = {}

        for key0,value0 in env_dict.items():
            for key,value in value0.items():
                env_properties['{}.{}'.format(key0,key)]=value

        with open( self.properties_path,'w',encoding='utf-8') as fp:
            jprops.store_properties(fp, env_properties)

        #执行生成报告命令
        cmd = 'allure generate %s -o %s --clean' % (self.xml_report_path, self.html_report_path)
        try:
            Shell.invoke(cmd)
            log.info("测试报告成功生成")
        except:
            log.error("Html测试报告生成失败,确保已经安装了Allure-Commandline")