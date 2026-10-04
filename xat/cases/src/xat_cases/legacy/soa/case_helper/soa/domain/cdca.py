#!/usr/bin/python3
# coding=UTF-8
import json
import os
import sys
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger  as logging
import re
import stat
import time
import pexpect

import platform

sysstr = platform.system()

if sysstr == 'Windows':
    from pexpect import popen_spawn

else:
    from pexpect import spawn
sys.path.append(os.path.join(project_root, 'soa_lib'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from codesrc.components.pressure.utils import get_script_path, make_subprocess, check_endecrypt_json
from codesrc.components.pressure.pre_env_ioe import IoE_start
from codesrc.public.utils.connection import RemoteToolsAdb
from codesrc.components.pressure.utils import hand_usbrelay_on,hand_usbrelay_off
script_path = os.path.join(get_script_path(), 'domain')
adb_win_path = os.path.join(get_script_path(), 'bin', 'adb.exe')
adb_mac_path = os.path.join(get_script_path(), 'bin', 'adb')


def check_cdca_is_on(cdca_addr):
    if sysstr == 'Windows':
        child_android = popen_spawn.PopenSpawn(f"adb -s {cdca_addr} shell", timeout=300)
    else:
        child_android = spawn(f"adb -s {cdca_addr} shell", timeout=300)
    time.sleep(10)
    return child_android.expect(['msmnile*', pexpect.EOF])


# 检查cdca日志
def check_cdca(data_path):
    data = os.listdir(data_path)
    logging.info(f'data========{data}')
    for i in data:
        a = i.split('.')[0]
        logging.info(f'a========={a}')
        if a in data and a != 'alog_default' and a != 'bootes':
            # if a in data:
            os.system(f'rm -rf {data_path}/{a}')
            logging.info(f'cdca日志和压缩包有重复，已清理:{a}')
            time.sleep(2)


# 获取cdca log
def pull_cdca_log(cdca_addr, cdca_log_path, i):
    if os.path.exists(cdca_log_path) is False:
        os.makedirs(cdca_log_path)
    os.chdir(cdca_log_path)
    logging.info(f'开始拉第{i}次cdca日志')
    try:
        os.system(f'adb -s {cdca_addr} root')
        time.sleep(10)
    except Exception as e:
        logging.info(e)
        logging.info('cdca adb root failed')
        for k in range(3):
            time.sleep(5)
            pull_cdca_log(cdca_addr, cdca_log_path, i)
    cmds1 = [
        f'adb -s {cdca_addr} shell "sync"',
        f'adb -s {cdca_addr} shell "tar -zcvf /data/log.tar.gz /data/log"',
        f'adb -s {cdca_addr} pull /data/log.tar.gz ./',
        f'adb -s {cdca_addr} shell "tar -zcvf /data/bootes.tar.gz /data/bootes"',
        f'adb -s {cdca_addr} pull /data/bootes.tar.gz ./']
    for cmd1 in cmds1:
        make_subprocess(cmd1)
    try:
        cmds2 = 'tar -xvf log.tar.gz'
        make_subprocess(cmds2)
        data_path = './data/log'
        check_cdca(data_path)
        cmds3 = [
            'gunzip ./data/log/*.gz',
            'tar -xvf bootes.tar.gz',
            f'adb -s {cdca_addr} pull /data/tombstones ./'
        ]
        for cmd3 in cmds3:
            make_subprocess(cmd3)
    except Exception as e:
        logging.info(f'没有cdca logs，无需备份{e}')


# 清理cdca log
def rm_cdca_log(cdca_addr, index,item=None):
    """清理cdca old log"""
    if not (item and  'cdc' in item["poweroff"]):
        logging.info('cdca 不下电 日志不清理')
    else:
        os.system(f'adb -s {cdca_addr} root')
        time.sleep(5)
        if sysstr == 'Windows':
            child = popen_spawn.PopenSpawn(
                f'adb -s {cdca_addr} shell  "rm  -rf  /data/log.tar.gz /data/log/* /data/bootes/* /data/bootes.tar.gz  /data/tombstones"',
                timeout=20)
        else:
            child = spawn(
                f'adb -s {cdca_addr} shell  "rm  -rf  /data/log.tar.gz /data/log/* /data/bootes/* /data/bootes.tar.gz /data/tombstones"',
                timeout=20)
        time.sleep(5)
        child.read()
        logging.info('cdca日志清理Finish')


def get_cdca_version_getprop(cdca_addr):
    try:
        child1 = spawn(f'adb -s {cdca_addr} shell "getprop | grep carina"', timeout=120)
        data = child1.read().decode('utf-8')
        v = re.split(r'[/\]]\s*', data)[3]
        logging.info('<cdca> cdca_version:')
        logging.info(v)
        return v
    except Exception as e:
        logging.info(f'<cdca> cdca 版本号获取 failed    {e}')
        return 'CDCA'


def get_cdca_version(cdca_addr):
    try:
        child1 = spawn(f'adb -s {cdca_addr} shell "getprop |grep carina"', timeout=500)
        v = child1.read().decode('utf-8').split('\n')[0].split('/')[-1][:-2]
        if v:
            logging.info(f'CDC 版本号为：{v}')
            return v
        else:
            child2 = spawn(f'adb -s {cdca_addr} shell "strings /system/lib64/libbootescore.so| grep bootes1"',
                           timeout=500)
            res = child2.read().decode('utf-8')
            v = res.split('\n')[0]
            if v:
                logging.info(f'<cdc> cdc_version: {v}')
                return v
            else:
                return 'CDC'
    except Exception as e:
        logging.info(f'cdca 版本号获取 failed    {e}')
        return 'CDC'


def check_cdca_network(cdca_addr, bgm_ip, cdcq_addr, tcam_ip, acu_ip):
    cdca_cmds = [
        f'adb -s {cdca_addr} root',
        f'adb -s {cdca_addr} shell "ping -c 2  {bgm_ip}"',
        f'adb -s {cdca_addr} shell "ping -c 2  {cdcq_addr}"',
        f'adb -s {cdca_addr} shell "ping -c 2  {tcam_ip}"',
        f'adb -s {cdca_addr} shell "ping -c 2  {acu_ip}"'
    ]
    for cmd in cdca_cmds:
        if not make_subprocess(cmd):
            return False
    return True


def pre_cdca(bgm_addr, cdca_addr, bgm_uname, bgm_pwd,nucapp=None):
    """
    cdca配置文件修改函数
    1、刷机后需要登录remount退出一次、在执行一次上下电操作
    2、有上下电操作执行一次ioe端口映射
    3、pull所依赖脚本inti_selinux推到cdca
    4、备份日志文件配置脚本，拉取下来本地修改后上传
    """
    logging.info('CDCA  登录')
    login_cdca(cdca_addr)
    logging.info('CDC 重启')
    hand_usbrelay_off("cdc",nucapp)
    # os.system('poweroff cdc')
    time.sleep(20)
    # os.system('poweron cdc')
    hand_usbrelay_on("cdc",nucapp)
    t=80
    logging.info(f'CDC 上电延时{t}秒')
    time.sleep(t)
    IoE_start(bgm_addr, bgm_uname, bgm_pwd, force_flag=True)
    cmds1 = [
        f'adb -s {cdca_addr} root',
    ]
    for cmd1 in cmds1:
        make_subprocess(cmd1)
    time.sleep(5)
    cmds1 = [
        f'adb -s {cdca_addr} remount',
        f'adb connect {cdca_addr}',
        f'adb -s {cdca_addr} push {os.path.join(script_path, "bin", "init_selinux")} /system/bin/init',
        f'adb -s {cdca_addr} shell "cp -r /system/etc/soa/common/bootes_config.json /system/etc/soa/common/bootes_config_old.json"',
        f"mkdir -p {os.path.join(script_path, 'script', 'cdcabootesjson')}",
        f"adb -s {cdca_addr} pull  /system/etc/soa/common/bootes_config_old.json {os.path.join(script_path, 'script', 'cdcabootesjson')}"
    ]
    for cmd1 in cmds1:
        make_subprocess(cmd1)
    update_cdca_bootes_file(cdca_addr)
    logging.info('CDCA  环境配置success')


def update_cdca_bootes_file(cdca_addr):
    with open(f"{os.path.join(script_path, 'script', 'cdcabootesjson', 'bootes_config_old.json')}", 'r',
              encoding='utf-8') as f:
        data = json.load(f)
        if 'log_config' in data.keys() and data['log_config']['spdlogConfig']['spdLogMaxSize'] == 10:
            logging.info('cdca bootes_config.json无需修改')
        else:
            data['log_config']['spdlogConfig']['eaSpdlogFile'] = True
            data['log_config']['spdlogConfig']['spdLogDir'] = '/data/bootes/'
            data['log_config']['spdlogConfig']['spdLogMaxSize'] = 10
            data['log_config']['spdlogConfig']['spdLogFileWithPid'] = True
            logging.info(data)
            with open(f"{os.path.join(script_path, 'script', 'cdcabootesjson', 'bootes_config.json')}", 'w',
                      encoding='utf-8') as f1:
                f1.write(json.dumps(data, indent=4, ensure_ascii=False))
                logging.info('cdca bootes_config 本地修改 success')
            os.system(f'adb -s {cdca_addr} root')
            cmds2 = [
                f"adb -s {cdca_addr} push {os.path.join(script_path, 'script', 'cdcabootesjson', 'bootes_config.json')} /system/etc/soa/common/",
                f'adb -s {cdca_addr} shell "mkdir -p /data/bootes"',
                f'adb -s {cdca_addr} shell "chmod -R 777 /data/bootes"'
            ]
            for cmd2 in cmds2:
                make_subprocess(cmd2)
        cmds = [
            f'rm -rf {os.path.join(script_path, "script", "cdcabootesjson")}'
        ]
        for cmd in cmds:
            make_subprocess(cmd)    


def config_cdca(bgm_addr, bgm_pwd, script_path):
    try:
        if sysstr == 'Windows':
            cmd1 = [
                f'pscp -pw {bgm_pwd} -scp {script_path}/bin/adb  root@{bgm_addr}:/update/tools/',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} "chmod 755 /update/tools/adb"',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} "/update/tools/adb connect 172.16.5.13"',
                f'pscp -pw {bgm_pwd} -scp {script_path}/script/port_mapping/config_cdca.sh  root@{bgm_addr}:/update/tools/',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} "chmod 755 /update/tools/config_cdca.sh"',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} "/update/tools/config_cdca.sh"'
            ]
        else:
            cmd1 = [
                f'sshpass -p {bgm_pwd} scp -r {script_path}/bin/adb  root@{bgm_addr}:/update/tools/',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "chmod 755 /update/tools/adb"',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/update/tools/adb connect 172.16.5.13"',
                f'sshpass -p {bgm_pwd} scp -r {script_path}/script/port_mapping/config_cdca.sh  root@{bgm_addr}:/update/tools/',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "chmod 755 /update/tools/config_cdca.sh"',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/update/tools/config_cdca.sh"'
            ]
        for cmd in cmd1:
            make_subprocess(cmd, get_script_path())
    except Exception as e:
        logging.info(f'<cdca> cdca配置失败{e}')


def pre_cdca_endecrypt_test(cdca_addr):
    cmds1 = [
        f'adb connect {cdca_addr}',
        f'adb -s {cdca_addr} root'
    ]
    for cmd1 in cmds1:
        make_subprocess(cmd1, get_script_path())
    time.sleep(10)

    remount_cmd = f'adb -s {cdca_addr} remount'
    if not make_subprocess(remount_cmd, get_script_path()):
        logging.info("<CDCA> remount action fisrt attempt fail, retrying")
        time.sleep(10)

    cmds2 = [
        f'adb -s {cdca_addr} remount',
        f'adb -s {cdca_addr} shell "mkdir -p /data/tools"',
        f'adb -s {cdca_addr} push {os.path.join(get_script_path(), "cdc_android_aarch_64", "endecrypt_test")} /data/tools',
        f'adb -s {cdca_addr} shell "chmod 777 -R /data/tools/*"',
        f'adb -s {cdca_addr} shell "cd /data/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/system/lib64;/data/tools/endecrypt_test"',
    ]
    for cmd1 in cmds2:
        if not make_subprocess(cmd1, get_script_path()):
            logging.info(
                "<CDCA> CDCA remount 失败，请重新执行程序；若多次运行均失败，请尝试在任务管理器中关闭adb、整车上下电或者reboot CDC")
            return False
    return True


def pre_cdca_endecrypt_json(cdca_addr):
    if sysstr == 'Windows':
        cmds1 = [
            f'adb -s {cdca_addr} root',
            f'adb -s {cdca_addr} remount',
            f'mkdir {os.path.join(script_path, "script", "cdcaendecryptjson")}',
            f'adb -s {cdca_addr} pull /data/tools/endecrypt.json {os.path.join(script_path, "script", "cdcaendecryptjson")}',
            f'adb -s {cdca_addr} pull /data/tools/endecrypt.json {os.path.join(script_path, "script", "cdcaendecryptjson")}',
        ]
    else:
        cmds1 = [
            f'adb -s {cdca_addr} root',
            f'adb -s {cdca_addr} remount',
            f'mkdir -p {script_path}/script/cdcaendecryptjson',
            f'adb -s {cdca_addr} pull /data/tools/endecrypt.json {script_path}/script/cdcaendecryptjson',
            f'adb -s {cdca_addr} pull /data/tools/endecrypt.json {script_path}/script/cdcaendecryptjson',
            f'chmod -R 755 {script_path}/script/*'
        ]
    for cmd1 in cmds1:
        make_subprocess(cmd1, get_script_path())
    json_path = f'{os.path.join("cdcaendecryptjson", "endecrypt.json")}'
    cdca_encrypt = check_endecrypt_json(json_path, 'CDCA')
    return cdca_encrypt


def recovery_cdca_endecrypt(cdca_addr):
    try:
        cmds1 = [
            f'adb -s {cdca_addr} root',
            f'adb -s {cdca_addr} remount',
            f'adb -s {cdca_addr} shell "rm -rf /data/tools"',
            f'adb -s {cdca_addr} shell "iptables -P INPUT ACCEPT"',
            f'adb -s {cdca_addr} shell "iptables -P OUTPUT ACCEPT"',
            f'adb -s {cdca_addr} shell "iptables -P FORWARD ACCEPT"'
        ]
        for cmd1 in cmds1:
            make_subprocess(cmd1, get_script_path())
    except Exception as e:
        logging.info(f'<cdca> recovery_cdca_endecrypt failed:{e}')


def get_cdca_endecrypt_version(cdca_addr):
    try:
        if sysstr == 'Windows':
            child = popen_spawn.PopenSpawn(f"{adb_win_path} connect {cdca_addr}", timeout=20)
            child1 = popen_spawn.PopenSpawn(f'{adb_win_path} -s {cdca_addr} shell "getprop | grep bootes"', timeout=120)
        else:
            if sysstr == 'Linux':
                child1 = spawn(f'adb -s {cdca_addr} shell "getprop | grep bootes"', timeout=120)
            else:
                child1 = spawn(f'{adb_mac_path} -s {cdca_addr} shell "getprop | grep bootes"', timeout=120)
        logging.info('<cdca> cdca_version:')
        logging.info(child1.read().decode('utf-8'))
    except Exception as e:
        logging.info(f'<cdca> cdca 版本号获取 failed    {e}')
        return 'CDCA'


def login_cdca(cdca_addr):
    cmds = [
        f'adb -s {cdca_addr} root',
        f'adb -s {cdca_addr} remount'
    ]
    for cmd in cmds:
        make_subprocess(cmd)
    cmds = f'adb -s {cdca_addr} shell'
    child = spawn(cmds, timeout=20)
    child.expect(['msmnile_gvmq*'])
    child.sendline('exit')
    child.close()

def pull_log(obdaddr, username, password, destpath, port=None):
    conn = RemoteToolsAdb(host=obdaddr, port=port)
    conn.connect()
    for remote_path in ['/data/log', '/data/bootes']:
        _pull_folder(conn, remote_path, os.path.join(destpath, os.path.basename(remote_path)))
    conn.close()

def _pull_folder(conn, remote_path, destpath):
    if not os.path.exists(destpath):
        os.makedirs(destpath, exist_ok=True)
    for file in conn.list(remote_path):
        _filename = file.filename.decode()
        if _filename.startswith('.'):
            continue
        _remote_file = f"{remote_path}/{_filename}"
        if stat.S_ISDIR(file.mode):
            _pull_folder(conn, _remote_file, os.path.join(destpath, _filename))
        else:
            conn.pull(_remote_file, os.path.join(destpath, _filename))

