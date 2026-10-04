import os,sys,time,pexpect

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
from xat_ecu.legacy.driver.ssh_client import *
from func_timeout import func_set_timeout

class SSH(object):

    def get_bgm_log(self):
        conn = SSHClient(hostname="169.254.1.1", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____SSH_SSH_LOG_NUC_LITE_PY_PASSWORD', ""))
        outmsg, errmsg = conn.exec_cmd(f"cd /log;rm bgm_log.tar.gz;rm tcam_log.tar.gz;tar -zcvf bgm_log.tar.gz ./*",6000,1)
        conn.close()
        self.__scp_bgm_log()

        # 取出BGM的所有log，默认放在当前目录下
    def __scp_bgm_log(self):
        ssh_newkey = 'Are you sure you want to continue connecting'
        log_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
        child = pexpect.spawn(f'scp -r root@169.254.1.1:/log/bgm_log.tar.gz /root/log/bgm_log_{log_time}.tar.gz')
        print(f"/root/log/bgm_log_{log_time}.tar.gz")
        pexpect.TIMEOUT = 6000
        ret = child.expect([ssh_newkey, '[P|p]assword:'])
        # ret == 0 输入yes，再输入密码
        # ret == 1 输入密码
        if ret == 0:
            child.sendline('yes')
            child.expect('[P|p]assword:')
            child.sendline(f'mars1bgm')
            child.expect("100%")
            child.close()
            # print(child.before)
        else:
            child.sendline(f'mars1bgm')
            child.expect("100%")
            child.close()

    @func_set_timeout(30)
    def __tcam_enter(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(f"169.254.1.1", f"22", f"root", f"mars1bgm")
        chan = ssh.invoke_shell()  # 创建一个交互式的shell窗口
        chan.settimeout(1000)
        chan.send(f'ssh root@172.16.5.31\n')
        flag = 0
        while True:
            stdout = chan.recv(1024).decode('utf-8')
            if f"root@172.16.5.31's password:" in stdout:
                # print(stdout, end='')
                chan.send(f'oelinux123\n')
                time.sleep(2)
                # print("\nTCAM连接成功")
                break
            elif "yes" in stdout: 
                time.sleep(2)
                # print(stdout, end='')
                chan.send("yes\n")
            else:
                pass
                # print(f"尝试连接TCAM，超时时间30s")
        return chan,ssh

    def get_tcam_log(self):
        chan,ssh = self.__tcam_enter()
        time.sleep(1)
        chan.send(
            f'cd /mnt/sdcard/;rm /mnt/sdcard/log/tcam_soa.tar.gz; tar -zcvf /mnt/sdcard/log/tcam_log.tar.gz /mnt/sdcard/log\n')
        while True:
            time.sleep(1)
            stdout = chan.recv(1024).decode('utf-8')
            # print(stdout, end='')
            if "/mnt/sdcard #" in stdout:
                time.sleep(1)
                break
        chan.close()
        ssh.close()
        # self.__get_tcam_tar_by_bgm()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(f"169.254.1.1", f"22", f"root", f"mars1bgm")
        chan = ssh.invoke_shell()
        chan.settimeout(1000)
        time.sleep(10)
        chan.send(
            f'rm /log/tcam_log.tar.gz;scp -r root@172.16.5.31:/mnt/sdcard/log/tcam_log.tar.gz /log/tcam_log.tar.gz\n')
        time.sleep(1)
        while True:
            stdout = chan.recv(1024).decode('utf-8')
            # chan.send('yes\n')
            # print(stdout, end='')
            if f"root@172.16.5.31's password:" in stdout:
                time.sleep(1)
                chan.send(f'oelinux123\n')
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
                # print(f"==========log成功从tcam传输到bgm上啦==========")
                break
        chan.close()
        ssh.close()
        # self.__scp_tcam_log()
        ssh_newkey = 'Are you sure you want to continue connecting'
        log_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
        child = pexpect.spawn(f'scp -r root@169.254.1.1:/log/tcam_log.tar.gz /root/log/tcam_log_{log_time}.tar.gz')
        self.pack_location = f"/root/log//tcam_log_{log_time}.tar.gz"
        pexpect.TIMEOUT = 6000
        ret = child.expect([ssh_newkey, '[P|p]assword:'])
        # ret == 0 输入yes，再输入密码
        # ret == 1 输入密码
        if ret == 0:
            child.sendline('yes')
            child.expect('[P|p]assword:')
            child.sendline(f'169.254.1.1')
            # print(child.before)
            child.expect("100%")
            child.close()
            # print(f"TCAM log 已经全部取到 {self.__local} 路径下啦0")
        else:
            child.sendline('mars1bgm')
            # print(child.before)
            child.expect("100%")
            child.close()
            # print(f"TCAM log 已经全部取到 {self.__local} 路径下啦1")
        conn = SSHClient(hostname="169.254.1.1", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____SSH_SSH_LOG_NUC_LITE_PY_PASSWORD', ""))
        outmsg, errmsg = conn.exec_cmd("rm -rf /log/tcam_log.tar.gz")
        conn.close()
        print(f"/root/log/tcam_log_{log_time}.tar.gz")

    def BGMorTCAM(self):
        if (sys.argv[1] == "BGM"):
            self.get_bgm_log()
        elif (sys.argv[1] == "TCAM"):
            self.get_tcam_log()
        elif (sys.argv[1] == "ALL"):
            self.get_bgm_log()
            self.get_tcam_log()
        else:
            print("输入的参数不正确，目前仅支持BGM or TCAM")

if __name__ == '__main__':
    SSH().BGMorTCAM()