import json
import os
import subprocess
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
current_path = os.path.join(current_path.split("sat")[0], "sat/tools/monitor/")
from xat_ecu.legacy.driver.ssh_client import SSHClient
from xat_ecu.legacy.common.logger import Logger

logger = Logger().get_logger("test")


def environment_init(un_tar_path):
    """
    在NGINX目录初始化资源监控web环境（每个上位机仅需执行一次）
    un_tar_path：解压缩的路径：allure report 目录
    """
    tarFile = os.path.join(current_path, "envir_init.tar.gz")
    check_cmd = f"tar -xvzf {tarFile} -C {un_tar_path}"
    logger.info("环境初始化命令：{}".format(check_cmd))
    pi = subprocess.Popen(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
    stdout = pi.stdout.read()
    logger.info("环境初始化结果：{}".format(stdout))


class system_resource:
    def __init__(self, X_time, cpuUser, cpuSys, cpuIdle, memfree, active, memtotal,
                 NetRead, NetWrite, DiskRead, DiskWrite, updateSpace, logSpace, dataSpace):
        self.X_time = X_time
        self.cpuUser = cpuUser
        self.cpuSys = cpuSys
        self.cpuIdle = cpuIdle
        self.memfree = memfree
        self.active = active
        self.memtotal = memtotal
        self.NetRead = NetRead
        self.NetWrite = NetWrite
        self.DiskRead = DiskRead
        self.DiskWrite = DiskWrite
        self.updateSpace = updateSpace
        self.logSpace = logSpace
        self.dataSpace = dataSpace


class Monitor:
    def __init__(self, hostname, port, username, password, report_dir, nginx_dir, count=200, period=3):
        """
        hostname：监控的主机名
        username：主机登录账号
        password：主机登录密码
        report_dir: 测试报告存放目录
        count：监控的次数
        period：每次监控的时间间隔
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.report_dir = report_dir
        self.nginx_dir = nginx_dir
        self.count = count
        self.period = period
        self.put_sh_flag = False
        self.report_init()
        self.ssh_client = SSHClient(self.hostname, self.port, self.username, self.password)
        self.ssh_client.connect()

    def report_init(self):
        """
        创建单次报告目录结构
        tarFile：待解压缩的tar包
        un_tar_path：解压缩的路径：allure report 目录
        dirName :创建的报告的目录名
        """
        tarFile = os.path.join(current_path, "report.tar.gz")
        report_dir = os.path.join(self.nginx_dir, self.report_dir)
        # 创建报告目录
        mkdir_cmd = f"mkdir {report_dir}"
        logger.info("报告目录创建命令：{}".format(mkdir_cmd))
        if not os.path.exists(report_dir):
            pi = subprocess.Popen(mkdir_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
            stdout = pi.stdout.read()
            logger.info("报告目录创建结果：".format(stdout))
        # 报告目录初始化
        mkdir_cmd = f"tar -xvzf {tarFile} -C {report_dir}"
        logger.info("报告目录初始化命令：{}".format(mkdir_cmd))
        pi = subprocess.Popen(mkdir_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        stdout = pi.stdout.read()
        logger.info("报告目录初始化结果：{}".format(stdout))

        # 拷贝data.json
        json_file = os.path.join(current_path, "data.json")
        copy_cmd = f"cp {json_file} {report_dir}"
        logger.info("数据拷贝命令：{}".format(copy_cmd))
        pi = subprocess.Popen(copy_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
        stdout = pi.stdout.read()
        logger.info("数据拷贝命令结果：{}".format(stdout))

    def scpFileToRemoteNode(self, local_path, remote_path):

        SCP_CMD_BASE = r"""
          expect -c "
          set timeout 300 ;
          spawn scp -P {port} -r {local_source} {username}@{host}:{remote_path} ;
          expect *assword* {{{{ send {password}\r }}}} ;
          expect *\r ;
          expect \r ;
          expect eof
          "
      """.format(username=self.username, password=self.password, host=self.hostname,
                 local_source=local_path, remote_path=remote_path, port=self.port)
        SCP_CMD = SCP_CMD_BASE.format(localsource=local_path)
        p = subprocess.Popen(SCP_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.communicate()
        os.system(SCP_CMD)

    def get_sys_resource(self, ethName):
        connect_status = self.ssh_client.is_connected()
        if connect_status:
            if not self.put_sh_flag:
                self.scpFileToRemoteNode(os.path.join(current_path, "net.sh"), "/home/root/net.sh")
                self.put_sh_flag = True
                time.sleep(1)
            stdin, stdout = self.ssh_client.exec_cmd('sh /home/root/net.sh ' + ethName, wait_time=5)
            logger.info("获取到资源：{}".format(stdin))
            res = filter(lambda x: x.count(ethName) == 1, stdin.split('\n'))
            res_list = list(res)
            r = res_list[0].split()
            update_Space = filter(lambda x: x.count("update") == 1, stdin.split('\n'))
            updateSpace = list(update_Space)[0].split()[4][0:-1]
            log_Space = filter(lambda x: x.count("log") == 1, stdin.split('\n'))
            logSpace = list(log_Space)[0].split()[4][0:-1]
            data_Space = filter(lambda x: x.count("data") == 1, stdin.split('\n'))
            dataSpace = list(data_Space)[0].split()[4][0:-1]
            resource = system_resource(X_time=r[0], cpuSys=r[8], cpuUser=r[7], cpuIdle=r[9],
                                       memtotal=r[4], memfree=r[5], active=r[6], NetRead=r[2],
                                       NetWrite=r[3], DiskRead=r[10], DiskWrite=r[11], updateSpace=updateSpace,
                                       logSpace=logSpace, dataSpace=dataSpace)
            return resource
        else:
            logger.info(f"hostname:{self.hostname} connect fail")
            return ""

    def start_monitor(self):
        """
        生成并返回的data.json文件的格式
        {
            "script": "jidu1121",
            "xAxisdata": ["10:52:38","10:52:48"],
            "cpuUser": [4,2.2],
            "cpuSys": [1,0.8],
            "cpuIdle": [],
            "memfree": [430.2,419.5],
            "active": [4051,4051],
            "memtotal": [15666.9,15666.9],
            "NetRead": [12.7,10.7],
            "NetWrite": [-10,-8.6],
            "DiskRead": [0,0],
            "DiskWrite": [-305.6,-747.8]
            "updateSpace": [4,2.2],
            "logSpace": [1,0.8],
            "dataSpace": [1,0.8]
        }
        """
        data_resources = {"script": "BGM" if self.hostname == "172.16.5.1" else "TCAM",
                          "xAxisdata": [],
                          "cpuUser": [],
                          "cpuSys": [],
                          "cpuIdle": [],
                          "memfree": [],
                          "active": [],
                          "memtotal": [],
                          "NetRead": [],
                          "NetWrite": [],
                          "DiskRead": [],
                          "DiskWrite": [],
                          "updateSpace": [],
                          "logSpace": [],
                          "dataSpace": []
                          }
        for i in range(self.count):
            resource = self.get_sys_resource("eth0.5")
            if not resource:
                logger.info("获取系统资源失败，继续进行下次获取....")
                continue
            data_resources["xAxisdata"].append(resource.X_time)
            data_resources["cpuUser"].append(float(resource.cpuUser))
            data_resources["cpuSys"].append(float(resource.cpuSys))
            data_resources["cpuIdle"].append(float(resource.cpuIdle))
            data_resources["memtotal"].append(float(resource.memtotal))
            data_resources["memfree"].append(float(resource.memfree))
            data_resources["active"].append(float(resource.active))
            data_resources["NetRead"].append(float(resource.NetRead))
            data_resources["NetWrite"].append(-float(resource.NetWrite))
            data_resources["DiskRead"].append(float(resource.DiskRead))
            data_resources["DiskWrite"].append(-float(resource.DiskWrite))
            data_resources["updateSpace"].append(float(resource.updateSpace))
            data_resources["logSpace"].append(float(resource.logSpace))
            data_resources["dataSpace"].append(float(resource.dataSpace))
            logger.info(data_resources)
            with open(os.path.join(self.nginx_dir, self.report_dir)+"/data.json", 'w', encoding='utf-8') as fw:
                json.dump(data_resources, fw, indent=4, ensure_ascii=False)
            time.sleep(self.period)


if __name__ == '__main__':
    environment_init("/root/allure_report/")
    moni = Monitor("172.16.5.1", 22, "root", "mars1bgm", "BGM20221123", "/root/allure_report/")
    moni.start_monitor()
