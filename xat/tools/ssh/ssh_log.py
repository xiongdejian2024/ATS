import os
import sys
import wexpect
import timeit
import time
from scapy.all import *

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
from xat_ecu.legacy.driver.ssh_client import *
from xat_ecu.legacy.interface.nuc_app import *


class SSH(object):
    def __init__(self):
        self.__local = '.'  # 存储路径
        self.__remote = r'/log/bgm_log.tar.gz'  # 目标文件所在路径
        self.__remote_upper = r'/root/log/bgm_log/bgm_log.tar.gz'  # 上位机日志路径
        self.__hostname_upper = "172.18.128.73"
        self.__hostname_bgm = "169.254.1.1"
        self.__username = "root"
        self.__password_upper = __import__("os").environ.get('XAT_CREDENTIAL____SSH_SSH_LOG_PY___PASSWORD_UPPER', "")
        self.__password_bgm = __import__("os").environ.get('XAT_CREDENTIAL____SSH_SSH_LOG_PY___PASSWORD_BGM', "")

    def set_hostname_upper(self, hostname):
        self.__hostname_upper = hostname

    def set_hostname_bgm(self, hostname):
        self.__hostname_bgm = hostname

    def set_local(self, local):
        self.__local = local

    def set_remote(self, remote):
        self.__remote = remote

    def get_bgm_info(self):
        conn = SSHClient(
            hostname=self.__hostname_bgm,
            username=self.__username,
            password=self.__password_bgm,
        )
        outmsg, errmsg = conn.exec_cmd("cat /app/etc/build.prop")
        conn.close()
        print(outmsg)

    def get_log(self):
        conn = SSHClient(
            hostname=self.__hostname_bgm,
            username=self.__username,
            password=self.__password_bgm,
        )
        outmsg, errmsg = conn.exec_cmd(
            f"cd /log;rm bgm_log.tar.gz;rm tcam_log.tar.gz;tar -zcvf bgm_log.tar.gz ./*"
        )
        conn.close()
        self.__scp_bgm_log()

    def __scp_bgm_log(self):
        ssh_newkey = 'Are you sure you want to continue connecting'
        child = wexpect.spawn('cmd.exe')
        child.expect('>')
        child.sendline(
            f"scp -r root@{self.__hostname_bgm}:/log/bgm_log.tar.gz {self.__local}/bgm_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz"
        )
        ret = child.expect([ssh_newkey, '[P|p]assword:'])
        # ret == 0 输入yes，再输入密码
        # ret == 1 输入密码
        if ret == 0:
            child.sendline('yes')
            child.expect('[P|p]assword:')
            child.sendline(f'{self.__password_bgm}')
            # print(child.before)
            # print(f"bgm_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz 已经全部取到 {self.__local} 路径下啦0")
            print(
                fr"{self.__local}\bgm_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz "
            )
        else:
            child.sendline('mars1bgm')
            # print(child.before)
            print(
                fr"{self.__local}\bgm_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz "
            )
            # print(f"bgm_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz 已经全部取到 {self.__local} 路径下啦1")

    def __scp_tcam_log(self):
        ssh_newkey = 'Are you sure you want to continue connecting'
        child = wexpect.spawn('cmd.exe')
        child.expect('>')
        child.sendline(
            f"scp -r root@{self.__hostname_bgm}:/log/tcam_log.tar.gz {self.__local}/tcam_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz"
        )
        ret = child.expect([ssh_newkey, '[P|p]assword:'])
        # ret == 0 输入yes，再输入密码
        # ret == 1 输入密码
        if ret == 0:
            child.sendline('yes')
            child.expect('[P|p]assword:')
            child.sendline(f'{self.__password_bgm}')
            # print(child.before)
            print(
                fr"{self.__local}\bgm_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz "
            )
            # print(f"tcam_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz 已经全部取到 {self.__local} 路径下啦0")
        else:
            child.sendline('mars1bgm')
            # print(child.before)
            print(
                fr"{self.__local}\bgm_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz "
            )
            print(
                f"tcam_log_{time.strftime('%Y-%m-%d_%H_%M_%S')}.tar.gz 已经全部取到 {self.__local} 路径下啦1"
            )
        conn = SSHClient(
            hostname=self.__hostname_bgm,
            username=self.__username,
            password=self.__password_bgm,
        )
        outmsg, errmsg = conn.exec_cmd("rm -rf /log/tcam_log.tar.gz")
        conn.close()

    def __get_tcam_tar_by_bgm(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            f"{self.__hostname_bgm}", 22, f"{self.__username}", f"{self.__password_bgm}"
        )
        chan = ssh.invoke_shell()  # 创建一个交互式的shell窗口
        chan.settimeout(1000)
        time.sleep(1)
        chan.send('ssh root@172.16.5.31\n')
        time.sleep(1)
        while True:
            stdout = chan.recv(1024).decode('utf-8')
            # print(stdout, end='')
            if "root@172.16.5.31's password:" in stdout:
                chan.send('oelinux123\n')
                time.sleep(1)
                break
            else:
                chan.send("yes\n")
        time.sleep(1)
        # chan.send('cd /mnt/sdcard/;rm /mnt/sdcard/log/tcam_soa.tar.gz; tar -zcvf /mnt/sdcard/log/tcam_log.tar.gz /mnt/sdcard/log/soa /mnt/sdcard/log/jidu /mnt/sdcard/log/diagd_iautosar/usrdata /umdp  /mnt/sdcard/log/mcu_log.txt /mnt/sdcard/log/backup/*  /mnt/sdcard/log/diagd_iautosar /mnt/sdcard/log/UDS*.dlt /mnt/sdcard/log/SUVS*.dlt\n')
        # 东软log
        chan.send(
            'cd /mnt/sdcard/;rm /mnt/sdcard/log/tcam_soa.tar.gz; tar -zcvf /mnt/sdcard/log/tcam_log.tar.gz /mnt/sdcard/log/soa /mnt/sdcard/log/jidu\n'
        )
        # 普通log
        while True:
            time.sleep(1)
            stdout = chan.recv(1024).decode('utf-8')
            # print(stdout, end='')
            if "/mnt/sdcard #" in stdout:
                time.sleep(1)
                break
        chan.close()
        ssh.close()

    def get_tcam_log(self):
        self.__get_tcam_tar_by_bgm()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            f"{self.__hostname_bgm}", 22, f"{self.__username}", f"{self.__password_bgm}"
        )
        chan = ssh.invoke_shell()
        chan.settimeout(1000)
        time.sleep(10)
        chan.send(
            f'rm /log/tcam_log.tar.gz;scp -r root@172.16.5.31:/mnt/sdcard/log/tcam_log.tar.gz /log/tcam_log.tar.gz\n'
        )
        time.sleep(1)
        while True:
            stdout = chan.recv(1024).decode('utf-8')
            # chan.send('yes\n')
            # print(stdout, end='')
            if "root@172.16.5.31's password:" in stdout:
                chan.send('oelinux123\n')
                time.sleep(1)
                break
            else:
                time.sleep(1)
                chan.send("yes\n")
        time.sleep(1)
        while True:
            stdout = chan.recv(1024).decode('utf-8')
            # print(stdout, end='')
            if "100%" in stdout:
                # print(f"==========log成功从tcam:172.16.5.31传输到bgm:{self.__hostname_bgm}上啦==========")
                break
        chan.close()
        ssh.close()
        self.__scp_tcam_log()

    def __get_doip(self):
        # show_interfaces()
        pack = sniff(iface=get_obd_iface(), filter='dst port 13400', count=1)
        wrpcap('get_bgm_doip.pcap', pack)
        pcaps = rdpcap("get_bgm_doip.pcap")
        packet = pcaps[0]
        if "169.254" in packet['IP'].src:
            # print(packet['IP'].src)
            return packet['IP'].src
        else:
            self.get_doip()

    def reset_doip(self):
        bgm_doip = self.__get_doip()
        self.set_hostname_bgm(f'{bgm_doip}')
        logger.info(f"BGM DoIP >> {bgm_doip} << 成功获取到啦 ")
        return bgm_doip

    def BGMorTCAM(self):
        if sys.argv[1] == "BGM":
            self.get_bgm_log()
        elif sys.argv[1] == "TCAM":
            self.get_tcam_log()
        else:
            print("输入的参数不正确，目前仅支持BGM or TCAM")


if __name__ == '__main__':
    start = timeit.default_timer()
    ssh_test = SSH()
    ssh_test.reset_doip()
    ssh_test.set_local(r"D:\python_project\sat\tools\ssh")
    ssh_test.BGMorTCAM()
    # # ssh_test.get_bgm_log()
    # ssh_test.get_tcam_log()
    end = timeit.default_timer()
    logger.info("耗时:", (end - start), "秒")
