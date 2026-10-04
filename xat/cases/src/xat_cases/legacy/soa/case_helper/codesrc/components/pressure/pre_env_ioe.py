import os
import subprocess
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from xat_cases.legacy.soa.case_helper.codesrc.components.pressure.utils import get_script_path, make_subprocess, get_obd_ip, handle_ssh, spawn_bgm
from xat_ecu.legacy.common.logger import logger  as logging
from xat_cases.legacy.soa.case_helper.soa.domain.bgm import first_ssh_bgm
import platform

sysstr = platform.system()


def IoE_start(obd_addr, username, password, force_flag=True):
    """执行开始"""
    logging.info('bmg重启后第一次连接')
    first_ssh_bgm(username, password, obd_addr)
    logging.info('<IoE> Port Mapping Start')
    script_path = os.path.join(get_script_path(), 'domain')
    # 配置bgm环境
    ip_forward_status = get_ip_forward_status(obd_addr, username, password)
    logging.info(f"bgm环境配置ip_forward_status为{ip_forward_status}")
    if force_flag or ip_forward_status != '1':
        config_bgm(obd_addr, username, password)
        # 配置cdcq环境
        config_cdcq(obd_addr, username, password, script_path)
        # # 配置cdca环境
        while True:
            config_cdca(obd_addr, username, password, script_path)
            data = os.popen("adb devices").read()
            if f"{obd_addr}:1313" in data:
                break
            else:
                logging.info(f"cdca环境配置失败重新配置{data}")

        # 配置tcam环境
        config_tcam(obd_addr, username, password, script_path)
        # 配置acu环境
        config_acu(obd_addr, username, password, script_path)
        logging.info('<IoE> Port Mapping Finish')
    else:
        return "<IoE> Port Mapping Is Finished"


def config_bgm(obd_addr, username, password):
    if username == 'root':
        if sysstr == 'Windows':
            cmds = [
                f'echo y | plink -no-antispoof -ssh root@{obd_addr} -pw {password} "echo 1 > /proc/sys/net/ipv4/ip_forward"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 31222 -j DNAT --to-destination 172.16.9.31:5555"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 1313 -j DNAT --to-destination 172.16.9.13:5555"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 11222 -j DNAT --to-destination 172.16.9.11:22"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 21222 -j DNAT --to-destination 172.16.9.21:22"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "/usr/sbin/iptables -P INPUT ACCEPT"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "/usr/sbin/iptables -P OUTPUT ACCEPT"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "/usr/sbin/iptables -P FORWARD ACCEPT"',
                f'plink -ssh root@{obd_addr} -pw {password} -batch "mkdir -p /update/tools"',
            ]
        else:
            handle_ssh(['root', 'mars1bgm'], obd_addr)
            cmds = [
                f'sshpass -p {password} ssh root@{obd_addr} "echo 1 > /proc/sys/net/ipv4/ip_forward"',
                f'sshpass -p {password} ssh root@{obd_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 31222 -j DNAT --to-destination 172.16.9.31:5555"',
                f'sshpass -p {password} ssh root@{obd_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 1313 -j DNAT --to-destination 172.16.9.13:5555"',
                f'sshpass -p {password} ssh root@{obd_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 11222 -j DNAT --to-destination 172.16.9.11:22"',
                f'sshpass -p {password} ssh root@{obd_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 21222 -j DNAT --to-destination 172.16.9.21:22"',
                f'sshpass -p {password} ssh root@{obd_addr} "/usr/sbin/iptables -P INPUT ACCEPT"',
                f'sshpass -p {password} ssh root@{obd_addr} "/usr/sbin/iptables -P OUTPUT ACCEPT"',
                f'sshpass -p {password} ssh root@{obd_addr} "/usr/sbin/iptables -P FORWARD ACCEPT"',
                f'sshpass -p {password} ssh root@{obd_addr} "mkdir -p /update/tools"',
            ]
        for cmd in cmds:
            make_subprocess(cmd, get_script_path())
    elif username == 'jiduer':
        root_cmds = [
            "echo 1 > /proc/sys/net/ipv4/ip_forward",
            f"/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 31222 -j DNAT --to-destination 172.16.9.31:22",
            f"/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 1313 -j DNAT --to-destination 172.16.9.13:5555",
            f"/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 11222 -j DNAT --to-destination 172.16.9.11:22",
            f"/usr/sbin/iptables -t nat -A PREROUTING --dst {obd_addr} -p tcp --dport 21222 -j DNAT --to-destination 172.16.9.21:22",
            "/usr/sbin/iptables -P INPUT ACCEPT",
            "/usr/sbin/iptables -P OUTPUT ACCEPT",
            "/usr/sbin/iptables -P FORWARD ACCEPT",
            "mkdir -p /update/tools/"

        ]
        spawn_bgm(username, obd_addr, password, root_cmds)
    print('<IoE> bgm配置finish')


def config_cdcq(obd_addr, username, password, script_path):
    if username == 'root':
        try:
            if sysstr == 'Windows':
                cmds = [
                    f'pscp -pw {password} -scp {os.path.join(script_path, "script", "port_mapping", "config_cdcq.sh")} root@{obd_addr}:/update/tools/',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 777 /update/tools/config_cdcq.sh"',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "/update/tools/config_cdcq.sh"'
                ]
            else:
                cmds = [
                    f'sshpass -p {password} scp -r {os.path.join(script_path, "script", "port_mapping", "config_cdcq.sh")}  root@{obd_addr}:/update/tools/',
                    f'sshpass -p {password} ssh root@{obd_addr} "chmod 755 /update/tools/config_cdcq.sh"',
                    f'sshpass -p {password} ssh root@{obd_addr} "/update/tools/config_cdcq.sh"'
                ]
            for cmd in cmds:
                make_subprocess(cmd, get_script_path())
        except Exception as e:
            print(f'<IoE> cdcq配置Failed{e}')
    elif username == 'jiduer':
        try:
            if sysstr == 'Windows':
                scp_cmds = [
                    f'pscp -pw {password} -scp -r {os.path.join(script_path, "script", "port_mapping", "config_cdcq.sh")} {username}@{obd_addr}:/tmp/jiduer',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 755 -R /tmp/jiduer/config_cdcq.sh"',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "/tmp/jiduer/config_cdcq.sh"'
                ]
            else:
                scp_cmds = [
                    f'sshpass -p {password} scp -r {os.path.join(script_path, "script", "port_mapping", "config_cdcq.sh")}  {username}@{obd_addr}:/tmp/jiduer',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 -R /tmp/jiduer/config_cdcq.sh"',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "/tmp/jiduer/config_cdcq.sh"'

                ]
            for cmd in scp_cmds:
                make_subprocess(cmd, get_script_path())
            print('<IoE> cdcq配置Finish')
        except Exception as e:
            print(f'<IoE> cdcq配置失败failed{e}')


def config_cdca(obd_addr, username, password, script_path):
    if username == 'root':
        try:
            if sysstr == 'Windows':
                cmd1 = [
                    f'pscp -pw {password} -scp {os.path.join(script_path, "bin", "adb")} root@{obd_addr}:/update/tools/',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 755 /update/tools/adb"',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "/update/tools/adb connect 172.16.5.13"',
                    f'pscp -pw {password} -scp {script_path}/script/port_mapping/config_cdca_v1.0.sh  root@{obd_addr}:/update/tools/',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 755 /update/tools/config_cdca_v1.0.sh"',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "/update/tools/config_cdca_v1.0.sh"'
                    f'adb connect {obd_addr}:1313'
                ]
            else:
                cmd1 = [
                    f'sshpass -p {password} scp -r {os.path.join(script_path, "bin", "adb")}  root@{obd_addr}:/update/tools/',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 /update/tools/adb"',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "/update/tools/adb connect 172.16.5.13"',
                    f'sshpass -p {password} scp -r {script_path}/script/port_mapping/config_cdca_v1.0.sh  root@{obd_addr}:/update/tools/',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 /update/tools/config_cdca_v1.0.sh"',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "/update/tools/config_cdca_v1.0.sh"',
                    f'adb connect {obd_addr}:1313'
                ]
            for cmd in cmd1:
                make_subprocess(cmd, get_script_path())
            print("#####################")
        except Exception as e:
            print(f'<IoE> cdca配置失败{e}')
    elif username == 'jiduer':
        if sysstr == 'Windows':
            scp_cmds = [
                f'pscp -pw {password} -scp -r {os.path.join(script_path, "bin", "adb")}  {username}@{obd_addr}:/tmp/jiduer/',
                f'pscp -pw {password} -scp -r {os.path.join(script_path, "script", "port_mapping", "config_cdca.sh")}  {username}@{obd_addr}:/tmp/jiduer/',
                f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 755 -R /tmp/jiduer/config_cdca.sh"',
                f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 755 -R /tmp/jiduer/adb"',
                f'plink -ssh {username}@{obd_addr} -pw {password} -batch "/tmp/jiduer/config_cdca.sh"'
            ]
        else:
            scp_cmds = [
                f'sshpass -p {password} scp -r {os.path.join(script_path, "bin", "adb")}  {username}@{obd_addr}:/tmp/jiduer',
                f'sshpass -p {password} scp -r {os.path.join(script_path, "script", "port_mapping", "config_cdca.sh")}  {username}@{obd_addr}:/tmp/jiduer',
                f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 -R /tmp/jiduer/config_cdca.sh"',
                f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 -R /tmp/jiduer/adb"',
                f'sshpass -p {password} ssh {username}@{obd_addr} "/tmp/jiduer/config_cdca.sh"',
                f'sshpass -p {password} ssh {username}@{obd_addr} "/tmp/jiduer/config_cdca.sh"'
            ]
        for cmd in scp_cmds:
            make_subprocess(cmd)
        # 适配windows adb connect
        if sysstr == 'Windows':
            scp_cmds = [
                f'adb.exe -s {obd_addr}:1313 root',
                f'adb.exe connect {obd_addr}:1313'
            ]
            for cmd in scp_cmds:
                make_subprocess(cmd, get_script_path())
        else:
            cmd1 = [
                f'adb -s {obd_addr}:1313 root',
                f'adb connect {obd_addr}:1313'
            ]
            for cmd in cmd1:
                make_subprocess(cmd, get_script_path())
        print('<IoE> cdca配置Fininsh')


def config_tcam(obd_addr, username, password, script_path):
    if username == 'root':
        try:
            if sysstr == 'Windows':
                cmd1 = [
                    f'pscp -pw {password} -scp -r {os.path.join(script_path, "script", "port_mapping", "config_tcam.sh")}  root@{obd_addr}:/update/tools/',
                    f'plink -pw {password} -ssh -batch {username}@{obd_addr} "chmod 755 /update/tools/config_tcam.sh"',
                    f'plink -pw {password} -ssh -batch {username}@{obd_addr} "/update/tools/config_tcam.sh"',
                ]
            else:
                cmd1 = [
                    f'sshpass -p {password} scp -r {os.path.join(script_path, "script", "port_mapping", "config_tcam.sh")}  root@{obd_addr}:/update/tools/',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 /update/tools/config_tcam.sh"',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "/update/tools/config_tcam.sh"',
                ]
            for cmd in cmd1:
                make_subprocess(cmd, get_script_path())
        except Exception as e:
            print(f'<IoE> tcam配置失败{e}')
    elif username == 'jiduer':
        try:
            if sysstr == 'Windows':
                scp_cmds = [
                    f'pscp -pw {password} -scp -r {os.path.join(script_path, "script", "port_mapping", "config_tcam.sh")}  {username}@{obd_addr}:/tmp/jiduer',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 755 -R /tmp/jiduer/config_tcam.sh"',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "/tmp/jiduer/config_tcam.sh"'
                ]
            else:
                scp_cmds = [
                    f'sshpass -p {password} scp -r {os.path.join(script_path, "script", "port_mapping", "config_tcam.sh")}  {username}@{obd_addr}:/tmp/jiduer',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 -R /tmp/jiduer/config_tcam.sh"',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "/tmp/jiduer/config_tcam.sh"'
                ]
            for cmd in scp_cmds:
                make_subprocess(cmd, get_script_path())
            print('<IoE> Tcam配置Finish')
        except Exception as e:
            print(f'<IoE> tcam配置失败{e}')


def config_acu(obd_addr, username, password, script_path):
    if username == 'root':
        try:
            if sysstr == 'Windows':
                cmd1 = [
                    f'pscp -pw {password} -scp {os.path.join(script_path, "script", "port_mapping", "config_acu.sh")}  root@{obd_addr}:/update/tools/',
                    f'plink -ssh root@{obd_addr} -pw {password} -batch "chmod 755 /update/tools/config_acu.sh"',
                    f'plink -ssh root@{obd_addr} -pw {password} -batch "/update/tools/config_acu.sh"'
                ]
            else:
                cmd1 = [
                    f'sshpass -p {password} scp -r {os.path.join(script_path, "script", "port_mapping", "config_acu.sh")}  root@{obd_addr}:/update/tools/',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 /update/tools/config_acu.sh"',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "/update/tools/config_acu.sh"'
                ]
            for cmd in cmd1:
                make_subprocess(cmd, get_script_path())
        except Exception as e:
            print(f'<IoE> acu配置失败{e}')
    elif username == 'jiduer':
        try:
            if sysstr == 'Windows':
                scp_cmds = [
                    f'pscp -pw {password} -scp -r {os.path.join(script_path, "script", "port_mapping", "config_acu.sh")}  {username}@{obd_addr}:/tmp/jiduer',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "chmod 755 -R /tmp/jiduer/config_acu.sh"',
                    f'plink -ssh {username}@{obd_addr} -pw {password} -batch "/tmp/jiduer/config_acu.sh"'

                ]
            else:
                scp_cmds = [
                    f'sshpass -p {password} scp -r {os.path.join(script_path, "script", "port_mapping", "config_acu.sh")}  {username}@{obd_addr}:/tmp/jiduer',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "chmod 755 -R /tmp/jiduer/config_acu.sh"',
                    f'sshpass -p {password} ssh {username}@{obd_addr} "/tmp/jiduer/config_acu.sh"'
                ]
            for cmd in scp_cmds:
                make_subprocess(cmd, get_script_path())
            print(f'<IoE> ACU配置Finish')
        except Exception as e:
            print(f'<IoE> acu配置失败{e}')


def get_ip_forward_status(obd_addr, username, password):
    if sysstr == 'Windows':
        script_path = os.path.dirname(os.path.dirname(os.path.dirname(get_script_path())))
        env_sm = {**os.environ,
                  'PATH': f"{os.path.join(script_path, 'bin')};{os.environ['PATH']}"}
        init_cmd = f'echo y | plink -no-antispoof -ssh {username}@{obd_addr} -pw {password} "dir"'
        subprocess.Popen(
            init_cmd,
            stdout=subprocess.PIPE,
            shell=True, env=env_sm)
        p = subprocess.Popen(
            f'plink -pw {password} -ssh {username}@{obd_addr} -batch "cat /proc/sys/net/ipv4/ip_forward"',
            stdout=subprocess.PIPE,
            shell=True, env=env_sm)
    else:
        p = subprocess.Popen(
            # ssh -o 跳过秘钥验证上电后跳过一次即可
            f'sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{obd_addr} "cat /proc/sys/net/ipv4/ip_forward"',
            stdout=subprocess.PIPE,
            shell=True)
    out, err = p.communicate()
    data = out.decode()
    print(f'BGM ip_forward status is {data}')
    return data.replace('\n', '')


if __name__ == '__main__':
    import optparse

    usage = "%prog -i <obd addr> -u <bgm username> -p <bgm password>"
    optParser = optparse.OptionParser(usage)
    optParser.add_option('-I', '-i', dest='obd_addr', type='string', help='input obd addr')
    optParser.add_option('-U', '-u', default='jiduer', dest='username', type='string', help='input bgm username')
    optParser.add_option('-P', '-p', default='bgm@Axzfr778', dest='password', type='string', help='input bgm password')

    (options, args) = optParser.parse_args()
    obd_addr = options.obd_addr or get_obd_ip()
    IoE_start(obd_addr, options.username, options.password)
