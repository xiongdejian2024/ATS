#!/usr/bin/python3
# coding=UTF-8
import json
import os
import sys
import subprocess
import logging
#from soa_lib.common.logger import logger  as logging
import time

import platform

sysstr = platform.system()

import pexpect

if sysstr == 'Windows':
    from pexpect import popen_spawn, EOF
else:
    from pexpect import spawn, EOF
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from codesrc.components.pressure.utils import check_endecrypt_json, get_script_path, make_subprocess
from codesrc.public.utils.connection import RemoteTools

script_path = os.path.join(get_script_path(), 'domain')
adb_win_path = os.path.join(get_script_path(), 'bin', 'adb.exe')
adb_mac_path = os.path.join(get_script_path(), 'bin', 'adb')


def check_tcam_is_on(tcam_addr):
    if sysstr == 'Windows':
        child_tcam = popen_spawn.PopenSpawn(f"{adb_win_path} -s {tcam_addr} shell", timeout=500)
    else:
        if sysstr == 'Linux':
            child_tcam = spawn(f"adb -s {tcam_addr} shell", timeout=500)
        else:
            child_tcam = spawn(f"{adb_mac_path} -s {tcam_addr} shell", timeout=500)
    time.sleep(10)
    return child_tcam.expect(['Enter*', pexpect.EOF])


def tar_tcam_log(tcam_addr, tcam_pwd):
    # 压缩coredump
    # child = spawn(f'adb -s {tcam_addr} shell "tar -zcvf /mnt/sdcard/coredump.tar.gz /mnt/sdcard/coredump"', timeout=500)
    # res1 = child.expect(['Enter*', pexpect.EOF])
    # time.sleep(5)
    # if res1 == 0:
    #     child.sendline(tcam_pwd)
    #     child.read()
    #     time.sleep(2)
    #     logging.info(f'child======{res1}')
    #     logging.info(f'tcam coredump压缩 success')
    # elif res1 == 1:
    #     logging.info(f'child======{res1}')
    #     logging.info(f'tcam coredump压缩 failed')
    #
    # p1 = subprocess.Popen(f'adb -s {tcam_addr} pull /mnt/sdcard/coredump.tar.gz ./', shell=True)
    # p1.wait()
    # if p1.returncode == 0:
    #     logging.info('tcam coredump tar包拉取 success')

    # p2 = subprocess.Popen(f'"', shell=True)
    # p2.wait()
    # if p2.returncode == 0:
    #     logging.info('tcam jetlog备份 success')
    if sysstr == 'Windows':
        child2 = popen_spawn.PopenSpawn(
            f'{adb_win_path} -s {tcam_addr} shell "mkdir -p /mnt/sdcard/logs"', timeout=500)
    else:
        if sysstr == 'Linux':
            child2 = spawn(
                f'adb -s {tcam_addr} shell "mkdir -p /mnt/sdcard/logs"', timeout=500)
        else:
            child2 = spawn(
                f'{adb_mac_path} -s {tcam_addr} shell "mkdir -p /mnt/sdcard/logs"', timeout=500)
    res1 = child2.expect(['Enter*', pexpect.EOF])
    time.sleep(5)
    if res1 == 0:
        child2.sendline(tcam_pwd)
        child2.read()
        time.sleep(2)
        logging.info(f'child======{res1}')
        logging.info(f'tcam logs创建 success')
    elif res1 == 1:
        logging.info(f'child======{res1}')
        logging.info(f'tcam logs创建 failed')

    if sysstr == 'Windows':
        child3 = popen_spawn.PopenSpawn(
            f'{adb_win_path} -s {tcam_addr} shell "cp -r /mnt/sdcard/log/jetlog* /mnt/sdcard/logs"',
            timeout=500)
    elif sysstr == 'Linux':
        child3 = spawn(
            f'adb -s {tcam_addr} shell "cp -r /mnt/sdcard/log/jetlog* /mnt/sdcard/logs"', timeout=500)
    else:
        child3 = spawn(
            f'{adb_mac_path} -s {tcam_addr} shell "cp -r /mnt/sdcard/log/jetlog* /mnt/sdcard/logs"',
            timeout=500)
    res2 = child3.expect(['Enter*', pexpect.EOF])
    time.sleep(5)
    if res2 == 0:
        child3.sendline(tcam_pwd)
        child3.read()
        time.sleep(2)
        logging.info(f'child======{res2}')
        logging.info(f'tcam jetlog备份 success')
    elif res2 == 1:
        logging.info(f'child======{res2}')
        logging.info(f'tcam jetlog备份 failed')

    if sysstr == 'Windows':
        p3 = subprocess.Popen(
            f'{adb_win_path} -s {tcam_addr}  pull /mnt/sdcard/logs ./', shell=True)
    elif sysstr == 'Linux':
        p3 = subprocess.Popen(
            f'adb -s {tcam_addr}  pull /mnt/sdcard/logs ./', shell=True)
    else:
        p3 = subprocess.Popen(
            f'{adb_mac_path} -s {tcam_addr}  pull /mnt/sdcard/logs ./', shell=True)
    p3.wait()
    if p3.returncode == 0:
        logging.info('tcam jetlog拉取 success')
    # p4 = subprocess.Popen(f'adb -s {tcam_addr} pull /mnt/sdcard/logs.tar.gz ./', shell=True)
    # p4.wait()
    # if p4.returncode == 0:
    #     logging.info('tcam jetlog tar包拉取 success')
    # p5 = subprocess.Popen(f'tar -xvf logs.tar.gz ./', shell=True)
    # p5.wait()
    # if p5.returncode == 0:
    #     logging.info('tcam jetlog tar包解压 success')


# tcam启动判断
def to_tcam(tcam_addr, tcam_pwd):
    pwd = tcam_pwd
    if sysstr == 'Windows':
        child = popen_spawn.PopenSpawn(f"{adb_win_path} -s {tcam_addr} shell root", timeout=20)
    else:
        if sysstr == 'Linux':
            child = spawn(f"adb -s {tcam_addr} shell root", timeout=20)
        else:
            child = spawn(f"{adb_mac_path} -s {tcam_addr} shell root", timeout=20)
    res1 = child.expect(['Enter*', 'adb*', pexpect.EOF])
    if res1 == 0:
        child.sendline(pwd)
        child.read()
        logging.info(f'child======{res1}')
        logging.info(f'tcam登录 success')
    elif res1 == 1:
        logging.info(f'child======{res1}')
        logging.info(f'tcam登录 success')
    elif res1 == 2:
        logging.info(f'tcam登录 failed, 再次进行三次登录测试')
        logging.info(f'child======{res1}')
        # os.system('poweroff tcam')
        # time.sleep(10)
        # # os.system('adb kill-server')
        # os.system('poweron tcam')
        # time.sleep(250)
        # to_tcam(tcam_addr, tcam_pwd)
    time.sleep(15)


# 获取tcam log
def pull_tcam_log(bgm_addr, tcam_pwd, i, tcam_log_path):
    """
    1、切换位ssh方式,更换方法名，
    2、以scp方式指定映射的端口号获取tcam日志,
    3、tcam全程不下电；只拉取最新生成的日志文件（不带序号的jetlog_messages/jetlog_bts）
    """
    if os.path.exists(tcam_log_path) is False:
        os.makedirs(tcam_log_path)
    logging.info(f'开始拉第{i}次tcam日志')
    cmds = [
        f'sshpass -p {tcam_pwd} ssh -o StrictHostKeyChecking=no -p31222 root@{bgm_addr} "sync"',
        f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/mnt/sdcard/log/dmesg.txt {tcam_log_path}',
        f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/mnt/sdcard/log/mcu_log.txt {tcam_log_path}',
        f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/oemapp/etc/bootes/service_monitor.json {tcam_log_path}',
        f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/mnt/sdcard/log/bootes {tcam_log_path}',
        f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/mnt/sdcard/coredump {tcam_log_path}',
        f'sshpass -p {tcam_pwd} ssh -p31222 root@{bgm_addr} "mkdir -p /mnt/sdcard/logs"',
        f'sshpass -p {tcam_pwd} ssh -p31222 root@{bgm_addr} "cp -r /mnt/sdcard/log/jetlog_messages /mnt/sdcard/logs"',
        f'sshpass -p {tcam_pwd} ssh -p31222 root@{bgm_addr} "cp -r /mnt/sdcard/log/jetlog_bts /mnt/sdcard/logs"',
        f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/mnt/sdcard/logs {tcam_log_path}'
    ]
    for cmd in cmds:
        make_subprocess(cmd)


# 清理tcam log
def rm_tcam_log(bgm_addr, tcam_pwd, index,item=None):
    if not (item and  'tcam' in item["poweroff"]):
        logging.info('tcam不下电，日志不清理')
    else:
        cmds = [
            f"sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} 'rm  -rf /mnt/sdcard/log/jetlog*  /mnt/sdcard/log/bootes/* /mnt/sdcard/coredump/* /mnt/sdcard/log/*.txt'"
        ]
        for cmd in cmds:
            make_subprocess(cmd)
        logging.info('tcam 日志清理 Finish')


def get_tcam_version(bgm_addr, tcam_pwd):
    """
        获取tcam版本号函数
        1、通过ssh指定端口号方式执行命令获取版本信息
        2、过滤所需版本信息
    """
    try:
        p = subprocess.Popen(
            f'sshpass -p {tcam_pwd} ssh -p 31222 -o StrictHostKeyChecking=no root@{bgm_addr} "cat /oemapp/etc/build.prop"',
            stdout=subprocess.PIPE,
            shell=True)
        out, err = p.communicate()
        data = out.decode()
        datas = data.split('\n')
        v = datas[12].split('=')[-1]
        logging.info(f'<tcam> tcam_version: {v}')
        return v
    except Exception as e:
        logging.info(f'<tcam> tcam 版本号获取 failed    {e}')
        return 'TCAM'


def check_tcam_network(bgm_addr, bgm_ip, cdcq_ip, cdca_ip, acu_ip, tcam_pwd):
    """tcam网络连接加长方法，切换为ssh方式"""
    cmds1 = [
        f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "ping -c 2  {bgm_ip}"',
        f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "ping -c 2  {cdcq_ip}"',
        f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "ping -c 2  {cdca_ip}"',
        f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "ping -c 2  {acu_ip}"',
    ]
    for cmd1 in cmds1:
        if not make_subprocess(cmd1):
            return False
    return True


def make_tcam_spawn(tcam_pwd, cmd, flag):
    if sysstr == 'Windows':
        child = popen_spawn.PopenSpawn(cmd, timeout=100)
    else:
        child = spawn(cmd, timeout=100)
    if flag:
        res1 = child.expect(['Enter*', 'root*', pexpect.EOF])
        time.sleep(10)
        if res1 == 0:
            child.sendline(tcam_pwd)
            child.read()
            logging.info(f'<tcam>    {cmd} success')
            return True
        elif res1 == 1:
            logging.info(f'<tcam>    {cmd} success')
            return True
        else:
            logging.info(f'<tcam>    {cmd} failed')
    else:
        res1 = child.expect(['Enter*', pexpect.EOF])
        time.sleep(10)
        if res1 == 0:
            child.sendline(tcam_pwd)
            data = child.readlines()
            for i in data:
                v = i.decode('utf-8')
                if '100%' in v:
                    logging.info(f'v=========={v}')
                    logging.info(f'{cmd} failed 请联系相关人员！')
                    return False
                elif '0%' in v:
                    logging.info(f'v=========={v}')
                    logging.info(f'{cmd} success')
            return True
        elif res1 == 1:
            logging.info(f'{cmd} failed')


def pre_tcam(bgm_addr, tcam_pwd):
    """
    1、切换为ssh端口映射方式，函数名加后缀ssh
    2、备份配置文件、开机启动文件到可修改权限目录下，执行shell命令修改开机启动文件中指定的日志路径；
    3、日志配置文件备份后拉取下来；本地修改后上传到tcam
    """
    cmds1 = [
        # ssh -o 跳过bgm 和tcam 秘钥验证上电后跳过一次即可
        f'sshpass -p {tcam_pwd} ssh -o StrictHostKeyChecking=no -p 31222 root@{bgm_addr} "cp -r /oemapp/etc/bootes/* /oemdata/etc"',
        f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "cp -r /oemapp/jiduEM.sh /oemdata/bin"',
        f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "chmod 777 -R /oemdata/bin/jiduEM.sh"',
        f"sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} 'sed -i \"s/export BOOTES_HOME_DIR=.*/export BOOTES_HOME_DIR=\/oemdata\/etc/g\"  /oemdata/bin/jiduEM.sh'",
        f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "cp -r /oemdata/etc/bootes_config.json /oemdata/etc/bootes_config_old.json"',
    ]
    for cmd1 in cmds1:
        make_subprocess(cmd1)

    cmds2 = [
        f'mkdir -p {os.path.join(script_path, "script", "tcambootesjson")}',
    ]
    for cmd2 in cmds2:
        make_subprocess(cmd2)
    cmds1 = [
        f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/oemdata/etc/bootes_config_old.json {os.path.join(script_path, "script", "tcambootesjson")}'
    ]
    for cmd1 in cmds1:
        make_subprocess(cmd1)
    update_tcam_bootes_file(bgm_addr, tcam_pwd)
    logging.info('TCAM  环境配置success')
    

def reset_tcam_env(bgm_addr, tcam_pwd):
    """
        # 删除 tcam中 推包文件jiduEM.sh，否则升级会导致tcam 挂死
    
    """
    cmds1 = [
        # ssh -o 跳过bgm 和tcam 秘钥验证上电后跳过一次即可
          f'sshpass -p {tcam_pwd} ssh -o StrictHostKeyChecking=no -p 31222 root@{bgm_addr} "rm -rf  /oemdata/bin/jiduEM.sh"',
    ]
    for cmd1 in cmds1:
        make_subprocess(cmd1)

    logging.info('TCAM  环境恢复success')
    


def update_tcam_bootes_file(bgm_addr, tcam_pwd):
    with open(f'{os.path.join(script_path, "script", "tcambootesjson", "bootes_config_old.json")}', 'r',
              encoding='utf-8') as f:
        data = json.load(f)
        if 'log_config' in data.keys() and data['log_config']['spdlogConfig']['spdLogMaxSize'] == 10:
            logging.info('tcam bootes_config.json无需修改')
        else:
            data['log_config']['spdlogConfig']['eaSpdlogFile'] = True
            data['log_config']['spdlogConfig']['spdLogMaxSize'] = 10
            data['log_config']['spdlogConfig']['spdLogFileWithPid'] = True
            with open(f'{os.path.join(script_path, "script", "tcambootesjson", "bootes_config.json")}', 'w',
                      encoding='utf-8') as f1:
                f1.write(json.dumps(data, indent=4, ensure_ascii=False))
                logging.info('tcam bootes_config 本地修改 success')
            cmds1 = [
                f'sshpass -p {tcam_pwd} scp -P 31222 -r {os.path.join(script_path, "script", "tcambootesjson", "bootes_config.json")} root@{bgm_addr}:/oemdata/etc/',
                f'rm -rf {os.path.join(script_path, "script", "tcambootesjson")}'
            ]
            for cmd1 in cmds1:
                make_subprocess(cmd1)


def config_tcam(bgm_addr, bgm_pwd, script_path, host_addr):
    try:
        if sysstr == 'Windows':
            cmd1 = [
                f'pscp -pw {bgm_pwd} -scp {script_path}/script/port_mapping/config_tcam.sh  root@{bgm_addr}:/update/tools/',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "chmod 755 /update/tools/config_tcam.sh"',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/update/tools/config_tcam.sh {host_addr}"',
                f'adb connect 169.254.1.1:3131'
            ]
        else:
            cmd1 = [
                f'sshpass -p {bgm_pwd} scp -r {script_path}/script/port_mapping/config_tcam.sh  root@{bgm_addr}:/update/tools/',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "chmod 755 /update/tools/config_tcam.sh"',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/update/tools/config_tcam.sh {host_addr}"',
                f'adb connect 169.254.1.1:3131'
            ]
        for cmd in cmd1:
            make_subprocess(cmd)
    except Exception as e:
        logging.info(f'<tcam> tcam配置失败{e}')


def pre_tcam_endecrypt_test(bgm_addr, tcam_addr, tcam_pwd, bgm_ver):
    if bgm_ver == 'v1.0.0':
        cmd = f'adb connect {tcam_addr}'
        make_subprocess(cmd, get_script_path())
        to_tcam(tcam_addr, tcam_pwd)
        cmd = f'adb connect {tcam_addr}'
        make_subprocess(cmd, get_script_path())
        if sysstr == 'Windows':
            cmds1 = f'{adb_win_path} -s {tcam_addr} shell "mkdir -p /oemdata/tools"'
        else:
            if sysstr == 'Linux':
                adbcmd = 'adb'
            else:
                adbcmd = adb_mac_path
            cmds1 = f'{adbcmd} -s {tcam_addr} shell "mkdir -p /oemdata/tools"'
        make_tcam_spawn(tcam_pwd, cmds1, flag=True)
        cmds2 = f'adb -s {tcam_addr} push  {os.path.join(get_script_path(), "tcam_linux_aarch_32", "endecrypt_test")} /oemdata/tools/'
        make_subprocess(cmds2, get_script_path())
        if sysstr == 'Windows':
            cmds3 = [
                f'{adb_win_path} -s {tcam_addr} shell "chmod 777 -R /oemdata/tools/*"',
                f'{adb_win_path} -s {tcam_addr} shell "cd /oemdata/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib/bootes:/oemapp/lib;/oemdata/tools/endecrypt_test"',
                f'{adb_win_path} -s {tcam_addr} shell "chmod 777 -R /oemdata/tools/*"'
            ]
        else:
            if sysstr == 'Linux':
                adbcmd = 'adb'
            else:
                adbcmd = adb_mac_path
            cmds3 = [
                f'{adbcmd} -s {tcam_addr} shell "chmod 777 -R /oemdata/tools/*"',
                f"{adbcmd} -s {tcam_addr} shell 'cd /oemdata/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib/bootes:/oemapp/lib;/oemdata/tools/endecrypt_test'",
                f'{adbcmd} -s {tcam_addr} shell "chmod 777 -R /oemdata/tools/*"'
            ]
        for cmd in cmds3:
            if not make_tcam_spawn(tcam_pwd, cmd, flag=True):
                return False
        return True
    elif bgm_ver == 'v1.1.0':
        cmds = [
            f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "mkdir -p /oemdata/tools"',
            f'sshpass -p {tcam_pwd} scp -P 31222 -r {os.path.join(get_script_path(), "tcam_linux_aarch_32", "endecrypt_test")} root@{bgm_addr}:/oemdata/etc/',
            f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "chmod 777 -R /oemdata/tools/*"',
            f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "cd /oemdata/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib/bootes:/oemapp/lib:/umdp/lib;/oemdata/tools/endecrypt_test"',
        ]
        for cmd in cmds:
            make_subprocess(cmd)


def pre_tcam_endecrypt_json(bgm_addr, tcam_addr, tcam_pwd, bgm_ver):
    if sysstr == 'Windows':
        cmds1 = [
            f'mkdir {os.path.join(script_path, "script", "tcamendecryptjson")}',
            f'{adb_win_path} -s {tcam_addr} pull  /oemdata/tools/endecrypt.json  {os.path.join(script_path, "script", "tcamendecryptjson")}',
        ]
    else:
        if sysstr == 'Linux':
            adbcmd = 'adb'
        else:
            adbcmd = adb_mac_path
        if bgm_ver == 'v1.0.0':
            cmds1 = [
                f'mkdir -p {os.path.join(script_path, "script", "tcamendecryptjson")}',
                f'{adbcmd} -s {tcam_addr} pull  /oemdata/tools/endecrypt.json  {os.path.join(script_path, "script", "tcamendecryptjson")}',
                f'chmod -R 755 {script_path}/script/*'
            ]
        elif bgm_ver == 'v1.1.0':
            cmds1 = [
                f'mkdir -p {os.path.join(script_path, "script", "tcamendecryptjson")}',
                f'sshpass -p {tcam_pwd} scp -P 31222 -r root@{bgm_addr}:/oemdata/tools/endecrypt.json {os.path.join(script_path, "script", "tcamendecryptjson")}',
                f'chmod -R 755 {script_path}/script/*'
            ]
    for cmd in cmds1:
        make_subprocess(cmd, get_script_path())
    json_path = f'{os.path.join("tcamendecryptjson", "endecrypt.json")}'
    tcam_encrypt = check_endecrypt_json(json_path, 'TCAM')
    return tcam_encrypt


def recovery_tcam_endecrypt(tcam_addr, tcam_pwd, bgm_addr=None, bgm_pwd=None):
    try:
        if sysstr == 'Windows':
            cmd1 = [
                f'pscp -pw {bgm_pwd} -scp {os.path.join(script_path, "script", "recovery", "recovery_tcam.sh")}  root@{bgm_addr}:/update/tools/',
                f'plink -pw {bgm_pwd} -ssh -batch root@{bgm_addr} "chmod 755 /update/tools/recovery_tcam.sh"',
                f'plink -pw {bgm_pwd} -ssh -batch root@{bgm_addr} "/update/tools/recovery_tcam.sh"',
            ]
            for cmd in cmd1:
                make_subprocess(cmd, get_script_path())

        # if sysstr == 'Windows':
        #     cmds1 = [
        #         f'{adb_win_path} -s {tcam_addr} shell "rm -rf /oemdata/tools"',
        #         f'{adb_win_path} -s {tcam_addr} shell "iptables -P INPUT DROP"',
        #         f'{adb_win_path} -s {tcam_addr} shell "iptables -P OUTPUT DROP"',
        #         f'{adb_win_path} -s {tcam_addr} shell "iptables -P FORWARD DROP"'
        #     ]
        else:
            if sysstr == 'Linux':
                cmds1 = [
                    f'adb -s {tcam_addr} shell "rm -rf /oemdata/tools"',
                    f'adb -s {tcam_addr} shell "iptables -P INPUT DROP"',
                    f'adb -s {tcam_addr} shell "iptables -P OUTPUT DROP"',
                    f'adb -s {tcam_addr} shell "iptables -P FORWARD DROP"'
                ]
                for cmd1 in cmds1:
                    make_tcam_spawn(tcam_pwd, cmd1, flag=True)
            else:
                cmd1 = [
                    f'sshpass -p {bgm_pwd} scp {os.path.join(script_path, "script", "recovery", "recovery_tcam.sh")} root@{bgm_addr}:/update/tools/',
                    f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "chmod 755 /update/tools/recovery_tcam.sh"',
                    f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/update/tools/recovery_tcam.sh"',
                ]
                for cmd in cmd1:
                    make_subprocess(cmd, get_script_path())
    except Exception as e:
        logging.info(f'<tcam> recovery_tcam_endecrypt failed:{e}')


def get_tcam_endecrypt_version(bgm_addr, tcam_addr, tcam_pwd, bgm_ver):
    if bgm_ver == 'v1.0.0':
        if sysstr == 'Windows':
            child = popen_spawn.PopenSpawn(f"{adb_win_path} connect {tcam_addr}", timeout=20)
        to_tcam(tcam_addr, tcam_pwd)
        try:
            if sysstr == 'Windows':
                child1 = popen_spawn.PopenSpawn(f'{adb_win_path} -s {tcam_addr} shell "cat /oemapp/etc/build.prop"',
                                                timeout=120)
            else:
                if sysstr == 'Linux':
                    adbcmd = 'adb'
                else:
                    adbcmd = adb_mac_path
                child1 = spawn(f'{adbcmd} -s {tcam_addr} shell "cat /oemapp/etc/build.prop"', timeout=120,
                               encoding='utf-8')
            child1.expect(['Enter*', EOF])
            child1.sendline(tcam_pwd)
            while True:
                line = child1.readline()
                if not line:
                    break
                logging.info(line.strip())
        except Exception as e:
            logging.info(f'<tcam> tcam 版本号获取 failed:  {e}')
            return 'TCAM'
    if bgm_ver == 'v1.1.0':
        p = subprocess.Popen(
            f'sshpass -p {tcam_pwd} ssh -p 31222 root@{bgm_addr} "cat /oemapp/etc/build.prop"', stdout=subprocess.PIPE,
            shell=True)
        out, err = p.communicate()
        data = out.decode()
        datas = data.split('\n')
        logging.info(datas)
        return datas


def pull_log(obdaddr, username, password, destpath, port=None):
    if not os.path.exists(destpath):
        os.makedirs(destpath, exist_ok=True)
    conn = RemoteTools(host=obdaddr, user=username, port=port, connect_kwargs={'password': password})
    conn.run('pwd', env={})
    conn.check_conn()
    if conn.is_connected == False:
        return logging.info('connect error')
    remote_path = '/mnt/sdcard/log'
    conn.get(remote_path=remote_path, local_path=destpath)
    coredump_path = '/mnt/sdcard/coredump'
    conn.get(remote_path=coredump_path, local_path=destpath)
    conn.close()


get_tcam_version("169.254.19.1", "tcam@rWh0bhf")