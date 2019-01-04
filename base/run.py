from base.shell import Shell
from base.utils import log,Conf,ls_by_key,Logbuilder
from base.environment import EnvironmentAndroid
import os,jprops,allure,pytest,logging
from multiprocessing import Pool


class Run():

    def __init__(self,platform=Conf().androidname):

        self.conf=Conf()
        self.platform=platform
        self.conf.set_platform(platform) # 设置执行平台

        self.env=EnvironmentAndroid()
        self.devices=self.env.devices


        self.xml_report_path =os.path.join(self.env.path.get("report"),'xml')
        self.html_report_path = os.path.join(self.env.path.get("report"),'html')
        self.properties_path=os.path.join(self.xml_report_path,'environment.properties')

    def get_run_args(self):

        #配置用于输出到报告的日志格式

        log_format = '--log-format=%(levelname)s %(asctime)s  %(message)s \n'.format()
        log_date_format = '--log-date-format=%H:%M:%S'
        log_level='--log-level={}'.format(str(logging.INFO))


        args = ['-s', '-q',log_format,log_date_format,log_level,'--alluredir', self.xml_report_path, "--verbose"]

        return args

    def generate_report(self):

        #给报告中添加执行环境信息
        env_dict={}

        env=self.env.conf

        #修改把yaml格式改成对应的键值对
        devices=env.get('devices')
        env.pop('devices')
        new_env=dict(env, **devices)

        env_dict.update(new_env)
        env_dict.update(self.conf.info)


        env_properties = {}

        for key0,value0 in env_dict.items():
            for key,value in value0.items():
                env_properties['{}.{}'.format(key0,key)]=str(value)

        try:
            with open( self.properties_path,'w',encoding='utf-8') as fp:
                jprops.store_properties(fp, env_properties)
        except:
            log.error('配置环境未输出到报告中')

        #执行生成报告命令
        cmd = 'allure generate %s -o %s --clean' % (self.xml_report_path, self.html_report_path)
        try:
            Shell.invoke(cmd)
            log.info("测试报告成功生成")
        except:
            log.error("Html测试报告生成失败,确保已经安装了Allure-Commandline")




    def exec(self,sys_argv):


        if len(sys_argv) != 0:
            self._exec_pytest(sys_argv)

        else:
            dir_tests = os.path.basename(self.env.path.get('tests'))
            scheduling_info = self._scheduling_process()

            pool=Pool(len(scheduling_info))

            for device_key,suitlist_value in scheduling_info.items():

                testsuite_paths=[]
                current_device=self.env.devices.get(device_key)

                for suit in suitlist_value:
                    testsuite_paths.append(os.path.join(dir_tests,suit))

                try:
                    pool.apply_async(self._batch_exec_pytest,args=(self.platform,current_device,testsuite_paths))
                except Exception as e:
                    raise ChildProcessError

            pool.close()
            pool.join()


    def _exec_pytest(self,sys_argv):
        #读取命令行参数，单设备执行
        args = sys_argv + self.get_run_args()


        #清除log对象已有的handler
        for handle in log.handlers:
            log.removeHandler(handle)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(levelname)s %(message)s'.format(os.getpid()), "%H:%M:%S")

        #添加用于输出到控制台的handler
        console_handler=Logbuilder().get_consolehandler(formatter)
        log.addHandler(console_handler)

        current_device=self.env.devices.get('device1')
        # 当前进程的环境对象通过回调写入current_device
        self.env.callback_current_device(current_device)

        pytest.main(args)



    @staticmethod
    def _batch_exec_pytest(platform,current_device,testsuite_paths):
        # 通过多进程调度执行用例（多台设备）
        #testsuite_paths 为list ，格式为[tests/test_suit2,tests/test_suit3]

        log.info('Run task pid={}  testsuite_paths: {}...'.format(os.getpid(), testsuite_paths))

        #清除log对象已有的handler
        for handle in log.handlers:
            log.removeHandler(handle)

        # 定义handler的输出格式
        formatter = logging.Formatter('pid:{} %(levelname)s %(message)s'.format(os.getpid()), "%H:%M:%S")

        #添加用于输出到控制台的handler
        console_handler=Logbuilder().get_consolehandler(formatter)

        log.addHandler(console_handler)


        run=Run(platform)

        #当前进程的环境对象通过回调写入current_device
        run.env.callback_current_device(current_device)

        #导入参数执行pytest
        args=testsuite_paths+run.get_run_args()

        pytest.main(args)





    def _scheduling_process(self):
        #给多台设备分配测试任务的调度算法（简单平均调度）
        #其中suit1是文件夹的名字、device1是配置中device设备的key

        """
        :return:
        {
        device1:[suit1,suit2]
        device2:[suit3,suit4]
        device3:[suit5]
        }

        """

        tests_path=self.env.path.get('tests')
        suitname_list=ls_by_key(tests_path,'test')


        if len(suitname_list)==0 or len(self.devices)==0:
            raise IndexError('data is bad')

        task_num,mod =divmod(len(suitname_list),len(self.devices))

        suitname_list_slice=[]
        tmp=[]
        count=0
        for suitname in suitname_list:
            tmp.append(suitname)
            if count<(len(suitname_list)-mod):
                if len(tmp)==task_num:
                    suitname_list_slice.append(tmp)
                    tmp=[]
            count+=1

        #对最后一个加入整除后剩余的
        last_ele=suitname_list_slice[-1]
        suitname_list_slice[-1]=last_ele+tmp


        scheduling_info={}
        count=0
        for device_key in self.devices:
            scheduling_info[device_key]=suitname_list_slice[count]
            count=count+1

        log.info("多设备分配的测试集执行为: {}\n".format(str(scheduling_info)))


        return scheduling_info



