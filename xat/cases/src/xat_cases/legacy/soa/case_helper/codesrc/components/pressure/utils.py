#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm
@Author  ：'wxa'
@Date    ：2023/4/7 14:49
"""
import json
import os
import subprocess
import time
from json import JSONDecodeError
import platform

sysstr = platform.system()

if sysstr == 'Windows':
    from pexpect import popen_spawn, EOF
else:
    from pexpect import spawn, EOF, TIMEOUT

# ssh config
PARTTERN_ASK = 'Are you sure you want to continue connecting'
PROMPT = ['# ', '>>> ', '> ', '\$ ']
PARTTERN_PSWD = '[P|p]assword'


def get_script_path():
    script_path = os.path.dirname(os.path.abspath(__file__))
    return script_path


def log_info(msg):
    print(f'[LOG] {msg}')

def string_decode(string):
    '''
    解密
    :param string:
    :return:
    '''
    import base64
    # string = base64.b64decode(string.encode()).decode()
    return string

def get_config_info():
    """
    获取配置文件
    """
    root_dir1 = os.path.dirname(os.path.abspath(__file__))
    print(root_dir1)
    path = os.path.join(root_dir1, "conf", "pressure.json")
    with open(path, 'r', encoding='utf-8') as f:
        res = json.load(f)
    
    #
    res['bgm_uname']=string_decode(res['bgm_uname'])
    res['bgm_pwd']=string_decode(res['bgm_pwd'])
    res['acu_pwd']=string_decode(res['acu_pwd'])
    res['acu_name']=string_decode(res['acu_name'])
    res['tcam_username']=string_decode(res['tcam_username'])
    res['tcam_pwd']=string_decode(res['tcam_pwd'])
    res['cdcq_uname']=string_decode(res['cdcq_uname'])
    
    return res

def hand_usbrelay_on(domain_name,nucapp=None):
    '''
    操作继电器 上电
    :param nucapp:是使用网络通信的 继电器  138台架
    :param domain_name:
    :return:
    '''

    domain = domain_name.lower()
    if nucapp:
        if domain == "bgm":
            nucapp.bgm_power_on()
        elif domain == "tcam":
            nucapp.tcam_power_on()
        elif domain == "acu":
            nucapp.acu_power_on()
        elif domain == "cdc":
            nucapp.cdc_power_on()
        elif domain == "all":
            nucapp.bgm_power_on()
            nucapp.tcam_power_on()
            nucapp.cdc_power_on()
            nucapp.acu_power_on()
        else:
            pass
    else:
        os.system(f'poweron {domain}')

def hand_usbrelay_off( domain_name,nucapp=None):
    '''
    操作继电器  下电
    :param nucapp: 为None  是使用网络通信的 继电器  138台架
    :param domain_name:
    :return:
    '''

    domain = domain_name.lower()
    if nucapp:
        if domain == "bgm":
            nucapp.bgm_power_off()
        elif domain == "tcam":
            nucapp.tcam_power_off()
        elif domain == "acu":
            nucapp.acu_power_off()
        elif domain == "cdc":
            nucapp.cdc_power_off()
        elif domain == "all":
            nucapp.bgm_power_off()
            nucapp.tcam_power_off()
            nucapp.cdc_power_off()
            nucapp.acu_power_off()
        else:
            pass
    else:
        os.system(f'poweroff {domain}')


def power_off_on():
    os.system('poweroff all')
    time.sleep(10)
    os.system('poweron all')
    time.sleep(60)


def make_ssh_client(bgm_addr, bgm_pwd, cmd):
    import paramiko
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=bgm_addr, port=22, username='root', password=bgm_pwd, timeout=180)
        print('bgm连接 success')
        stdin, stdout, stderr = ssh_client.exec_command(cmd, timeout=180)
        returncode = stdout.channel.recv_exit_status()
        if returncode == 0:
            print(f'{cmd} success')
            ssh_client.close()
            return True
        else:
            print(f'{cmd} failed')
            ssh_client.close()
            return False
    except Exception as e:
        print(f'{cmd} failed{e},请联系相关人员处理!')


def make_subprocess(cmd, script_path=get_script_path()):
    script_path = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    env_sm = None
    if script_path is not None:
        if sysstr == 'Windows':
            env_sm = {**os.environ,
                      'PATH': f"{os.path.join(script_path, 'bin')};{os.environ['PATH']}"}
        else:
            if sysstr == 'Linux':
                env_sm = {**os.environ, 'LD_LIBRARY_PATH': os.path.join(script_path, 'lib'),
                          'PATH': f"{os.path.join(script_path, 'bin')}:{os.environ['PATH']}"}
            else:
                env_sm = {**os.environ, 'LD_LIBRARY_PATH': os.path.join(script_path, 'lib'),
                          'PATH': f"{os.path.join(script_path, 'bin')}:{os.environ['PATH']}"}

    p = subprocess.Popen(cmd, shell=True, env=env_sm)
    p.communicate()
    p.wait()
    if p.returncode == 0:
        print(f'{cmd} success')
        p.kill()
        return True
    else:
        print(cmd)
        msg = f'{cmd} failed, 请联系相关人员处理!'
        print(msg)
        p.kill()
        return False


def check_endecrypt_json(json_path, area_name):
    try:
        data_path = os.path.join(get_script_path(), 'domain', 'script', json_path)
        if not os.path.exists(data_path):
            return area_name
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'encrypt' in data.keys() and data['encrypt']:
                return data['encrypt']
            else:
                print(f'get endecrypt failed! result: {data}')
                return area_name
    except JSONDecodeError as e:
        print(f'get encrypt failed!   {e}')
        return area_name


def check_bgm_is_on(bgm_uname, bgm_addr, bgm_pwd):
    import paramiko
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=bgm_addr, port=22,
                           username=bgm_uname, password=bgm_pwd, timeout=500)
        print('bgm连接 success')
        ssh_client.close()
        return True
    except Exception as e:
        print(f'bgm连接 failed{e}')
        return False


def spawn_ssh(cmds):
    if sysstr == 'Windows':
        from pexpect import popen_spawn, EOF
    else:
        from pexpect import spawn, EOF
    for cmd in cmds:
        if sysstr == 'Windows':
            child = popen_spawn.PopenSpawn(cmd, timeout=20)
        else:
            child = spawn(cmd, timeout=20)
        res1 = child.expect(['Are*', 'root*', 'The*', EOF])
        if res1 == 0 or res1 == 2:
            child.sendline('yes')
            child.read()
        else:
            child.read()


def spawn_sftp(cmds1, bgm_addr, script_path=get_script_path()):
    if sysstr == 'Windows':
        from pexpect import popen_spawn, EOF
    else:
        from pexpect import spawn, EOF
    for cmd1 in cmds1:
        env_sm = None
        if script_path is not None:
            if sysstr == 'Windows':
                env_sm = {**os.environ,
                          'PATH': f"{os.path.join(script_path, 'bin')};{os.environ['PATH']}"}
            else:
                env_sm = {**os.environ, 'LD_LIBRARY_PATH': os.path.join(script_path, 'lib'),
                          'PATH': f"{os.path.join(script_path, 'bin')}:{os.environ['PATH']}"}
        if sysstr == 'Windows':
            psftp_path = os.path.join(script_path, 'bin', 'psftp.exe')
            cmds2 = f'{psftp_path} -P 11222 root@{bgm_addr}'
            child = popen_spawn.PopenSpawn(cmds2, timeout=30, env=env_sm)
            res1 = child.expect(['Are*', 'psftp*', 'Using', 'root', 'jidu', '  169*', 'You*', EOF])
            if res1 == 0 or res1 == 5 or res1 == 6:
                child.sendline('yes')
                child.expect('psftp*')
                child.sendline(cmd1)
                child.expect('psftp*')
                child.sendline('exit')
            elif res1 == 1 or res1 == 2:
                child.sendline(cmd1)
                child.expect('psftp*')
                child.sendline('exit')
            else:
                child.read()
        else:
            cmds2 = f'sftp -P 11222 root@{bgm_addr}'
            child = spawn(cmds2, timeout=20)
            res1 = child.expect(['Are*', 'sftp*', 'root', 'jidu', EOF])
            if res1 == 0:
                child.sendline('yes')
                child.expect('sftp*')
                child.sendline(cmd1)
                child.expect('sftp*')
                child.sendline('exit')
            elif res1 == 1:
                child.sendline(cmd1)
                child.expect('sftp*')
                child.sendline('exit')
            else:
                child.read()


def _get_ip_for_mac(pattern='inet 169.254.'):
    # check the installations of "CLT (Comand Line Tools)"
    clt_path = '/Library/Developer/CommandLineTools'
    default_python3_exe_path = '/usr/bin/python3'
    tcpdump_cmd = "xargs -I {} sudo tcpdump udp -c 1 -i {} | awk '{print $3}' | sed 's/.13400$//' "

    if os.path.exists(clt_path) and os.path.exists(default_python3_exe_path):
        _prefix = f"ip a | grep \"{pattern}\"" + " | head -n 1 | awk '{print $5}' | sed 's/:$//' | "
        cmd = _prefix + tcpdump_cmd
        log_info(f'use "ip": {cmd}')
    else:
        # 如果用户没有安装clt，并且默认位置没有python的话，会启用备用方案 ifconfig。这个会存在一定概率失效（低概率）
        _prefix = f"ifconfig | grep -4 \"{pattern}\"" + " | head -n 1 | awk '{print $1}' | sed 's/:$//' | "
        cmd = _prefix + tcpdump_cmd
        log_info(f'use "ifconfig": {cmd}')
    env_sm = handle_env()
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, env=env_sm)
    return p


def get_obd_ip():
    if sysstr == 'Windows':
        print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(get_script_path())))))
        env_sm = {**os.environ,
                  'PATH': f"{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(get_script_path()))), 'bin')};{os.environ['PATH']}"}
        cmd = r'''
        $preiface = ".\Device\NPF_";
        $iface = (Get-WmiObject -Query "SELECT * FROM Win32_NetworkAdapterConfiguration" | Where-Object { $_.IPAddress -ne $null -and $_.IPAddress[0].StartsWith("169.254") }).SettingID;
        $udppacket = WinDump -i "$preiface$iface" -nn -s 0 -c 1 "dst port 13400" | Out-String;
        if ($udppacket -match "169\.254\.\d{1,3}\.\d{1,3}"){$matchedIP = $Matches[0]};
        Write-Host "$matchedIP";
        '''

        result = subprocess.run(["powershell.exe", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, env=env_sm)
        output = result.stdout.strip()

        print(f"<utils> Found BGM ip: {output}")

        if output.startswith("169.254"):
            return output
        else:
            print("<utils> BGM ip not found, proceed with default")
            return "169.254.1.1"

    else:
        if sysstr == 'Linux':
            cmd = "ip a | grep -2 'inet 169.254.' | head -n 1 | awk '{print $2}' | sed 's/:$//' | xargs -I {} sudo tcpdump -c 1 -i {} udp and ether broadcast and port 13400 | awk '{print $3}' | sed 's/.13400$//'"
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        else:
            p = _get_ip_for_mac()
        try:
            print("开始获取bgm_ip")
            out, err = p.communicate(timeout=20)
            for line in out.splitlines():
                adb_ip = line.decode('utf-8', 'ignore')
                return adb_ip
        except Exception as e:
            print(f'ADB-IP 获取 failed: {e}')
            from soa_lib.interface.nuc_app import get_obd_ip
            return get_obd_ip()


class SshHandle:
    def __init__(self, user_info: list, ipaddr, ipport=22):
        self.user, self.passwd = user_info
        self.ipaddr, self.ipport = ipaddr, ipport
        self.connection = None
        self._init_host()

    # def close(self):
    #     self.connection.close()

    def send(self, msg):
        self.connection.sendline(msg)
        self.connection.expect(PROMPT)
        log_info(f'Handle ssh: {self.connection.before}')

    def _init_host(self):
        cmd = f'ssh-keygen -R "[{self.ipaddr}]:{self.ipport}"'
        try:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            log_info(f'failed to clear known host')

    def connect(self):
        host = f'{self.user}@{self.ipaddr}'
        cmd = f'ssh -p {self.ipport} {host}'
        self.connection = spawn(cmd)
        ret = self.connection.expect([TIMEOUT, PARTTERN_ASK, PARTTERN_PSWD] + PROMPT)

        if ret == 0:
            log_info(f'Connect to {host} timeout.')
            return
        if ret == 1:
            self.connection.sendline('yes')
            ret = self.connection.expect([TIMEOUT, PARTTERN_PSWD])
            if ret == 0:
                log_info(f'Connect to {host} timeout.')
                return
            self.connection.sendline(self.passwd)
            self.connection.expect(PROMPT)
            return self.connection


def handle_ssh(user_info: list, ipaddr, ipport=22):
    ssh = SshHandle(user_info, ipaddr, ipport)
    ssh.connect()
    log_info('start to send message.')


class EnvHandle:
    def __init__(self, platform='Darwin'):
        self._env = None
        self._already_set = False

    def set(self, script_path):
        if not self._already_set:
            self._env = {**os.environ, 'LD_LIBRARY_PATH': os.path.join(script_path, 'lib'),
                         'PATH': f"{os.path.join(script_path, 'bin')}:{os.environ['PATH']}"}
            self._already_set = True

    def get(self):
        return self._env


def handle_env(script_path=get_script_path(), platform='Darwin'):
    # 后面考虑放到setup.py里，只生成一次
    env_obj = EnvHandle(platform)
    env_obj.set(script_path)
    return env_obj.get()


class MakeSubprocess(subprocess.Popen):
    def __init__(self, cmd, shell=False, stdout=None, env_sm=False, platform='Darwin'):
        env = None
        if env_sm:
            env_obj = handle_env(platform=platform)
            env = env_obj.get()
        super().__init__(cmd, shell=shell, stdout=stdout, env=env)


def spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds, script_path=get_script_path()):
    if sysstr == 'Windows':
        from pexpect import popen_spawn, EOF
        env_sm = {**os.environ,
                  'PATH': f"{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(script_path))), 'bin')};{os.environ['PATH']}"}
        plink_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(script_path))), 'bin', 'plink.exe')
        jidu_cmds = f'{plink_path} -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr}'

        child = popen_spawn.PopenSpawn(jidu_cmds, timeout=20, env=env_sm)
    else:
        from pexpect import spawn, EOF

        jidu_cmds = f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr}'
        child = spawn(jidu_cmds, timeout=20)

    res1 = child.expect(['Are*', 'jiduer*', EOF])
    if res1 == 0:
        child.sendline('yes')
        child.expect('jiduer*')
        child.sendline(bgm_pwd)
        child.expect('jiduer*')
        child.sendline('sudo -s')
        child.expect('Password:*')
        child.sendline(bgm_pwd)
        for root_cmd in root_cmds:
            child.expect('root*')
            child.sendline(root_cmd)
        child.expect('root*')
        child.sendline('exit')
    elif res1 == 1:
        child.sendline('sudo -s')
        child.expect('Password*')
        child.sendline(bgm_pwd)
        for root_cmd in root_cmds:
            child.expect('root*')
            child.sendline(root_cmd)
        child.expect('root*')
        child.sendline('exit')


def get_host_ip():
    """
    获取跳板机ip方法
    """
    try:
        cmd = "ip a | grep 'inet 172.18' | awk '{print $2}' | awk -F '/' '{print $1}'"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        host_ip = out.decode().replace('\n', '')
        print(host_ip)
        return host_ip
    except Exception as e:
        print(f'<host> host 版本号获取 failed    {e}')
        return 'host_ip'


from scapy.all import sendp, get_if_addr, get_if_list, PcapReader

def get_iface(ipaddr):
    '''
    @desp: 获取iface
    @param ipaddr: ip地址
    '''
    res = None
    for iface in sorted(get_if_list()):
        if ipaddr == get_if_addr(iface):
            res = iface
            break
    return res


class PcapManager(object):
    '''
    @desp: pcap管理器：拨包/停止拨包
    '''

    def __init__(self, pcap_path, ipaddr):
        self._iface = get_iface(ipaddr)
        self._pcap_reader = self.read_pcap(pcap_path)

    @staticmethod
    def read_pcap(file_path):
        return PcapReader(file_path)

    def send(self, length=-1):
        '''
        @deps: 拨包函数
        '''

        for i, packet in enumerate(self._pcap_reader):
            if length >= 0 and i >= length:
                break
            sendp(packet, self._iface, verbose=False)