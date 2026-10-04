#!/usr/bin/python3
# coding=UTF-8

import os
import sys
project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.common.logger import logger  as logging
from json import JSONDecodeError

import platform

sysstr = platform.system()

if sysstr == 'Windows':
    from pexpect import popen_spawn
else:
    from pexpect import spawn
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(os.path.join(project_root, 'test_case/soa/case_helper'))
from codesrc.components.pressure.utils import make_subprocess, check_endecrypt_json, get_script_path
from codesrc.public.utils.connection import RemoteToolsAdb


script_path = os.path.join(get_script_path(), 'domain')
plink_path = os.path.join(get_script_path(), 'bin', 'plink.exe')
sshpass_mac_path = os.path.join(get_script_path(), 'bin', 'sshpass')


def pull_acu_log(bgm_addr, bgm_pwd, acu_pwd, acu_name, acu_log_path, i):
    """
    端口映射方式
    """
    if os.path.exists(acu_log_path) is False:
        os.makedirs(acu_log_path)
    os.chdir(acu_log_path)
    logging.info(f'开始拉第{i}次acu日志')
    try:
        if sysstr == 'Windows':
            cmds1 = [f'pscp -pw {acu_pwd} -P 21222 -scp {acu_name}@{bgm_addr}:/opt/log/bootes ./']
        else:
            cmds1 = [
                f'sshpass -p {acu_pwd} scp -o StrictHostKeyChecking=no -P 21222 -r {acu_name}@{bgm_addr}:/opt/log/bootes ./'
            ]
        for cmd in cmds1:
            make_subprocess(cmd)
    except Exception as e:
        logging.info(f'pull Acu log failed================={e}')
        pull_acu_log(bgm_addr, bgm_pwd, acu_pwd, acu_name, acu_log_path, i)


def rm_acu_log(bgm_addr, bgm_pwd, acu_pwd, acu_name, index,item=None):
    """
    端口映射方式
    """
    if not (item and  'acu' in item["poweroff"]):
        logging.info('acu 不下电 日志不清理')
    else:
        logging.info('开始清理acu日志')
        try:
            if sysstr == 'Windows':
                cmds1 = [
                    f'plink -ssh {acu_name}@{bgm_addr} -pw {acu_pwd} -P 21222 -batch "rm -rf /opt/log/bootes/*"'
                ]
            else:
                cmds1 = [
                    f'sshpass -p {acu_pwd} ssh -p21222 {acu_name}@{bgm_addr} "echo {acu_pwd} | sudo -S rm -rf /opt/log/bootes/*"',
                    f'sshpass -p {acu_pwd} ssh -p21222 {acu_name}@{bgm_addr} "echo {acu_pwd} | sudo -S rm -rf /opt/log/*"'
                ]
            for cmd in cmds1:
                make_subprocess(cmd)
            logging.info('acu日志清理Finish')
        except Exception as e:
            logging.info(f'ACU 日志清理 failed================={e}')

def get_acu_bootes_version(bgm_addr, acu_name, acu_pwd):
    """
        获取acu bootes版本号
    """
    try:
        child1 = spawn(
            f'sshpass -p {acu_pwd} ssh -p 21222 -o StrictHostKeyChecking=no {acu_name}@{bgm_addr}' + ' \"cat /opt/integration-version.txt|grep Carina|awk \'{print $2}\'\"',
            timeout=120)
        data = child1.read().decode('utf-8').strip()
        logging.info(f'<acu> acu_version: {data}')
        return True, data
    except Exception as e:
        logging.info(f'<acu> acu 版本号获取 failed    {e}')
        return False, "acu"


def get_acu_version(bgm_addr, acu_name, acu_pwd):
    """
        获取acu版本号
    """
    result, data = get_acu_bootes_version(bgm_addr, acu_name, acu_pwd)
    if result:
        return data
    else:
        try:
            child1 = spawn(
                f'sshpass -p {acu_pwd} ssh -p 21222 -o StrictHostKeyChecking=no {acu_name}@{bgm_addr} "cat /opt/integration-version.txt|grep Carina"',
                timeout=120)
            data = child1.read().decode('utf-8')
            datas = data.split('\n')
            for line in datas:
                if 'Carina' in line:
                    v = line.split()[-1]
                    logging.info(f'<acu> acu_version: {v}')
                    return v
                else:
                    continue
        except Exception as e:
            logging.info(f'<acu> acu 版本号获取 failed    {e}')
            return 'ACU'


def check_acu_network(bgm_addr, bgm_ip, acu_name, acu_pwd, cdca_ip, cdcq_ip, tcam_ip):
    if sysstr == 'Windows':
        acu_cmds = [
            f'plink -ssh {acu_name}@{bgm_addr} -pw {acu_pwd} -P 21222 -batch "ping -c 2  {bgm_ip}"',
            f'plink -ssh {acu_name}@{bgm_addr} -pw {acu_pwd} -P 21222 -batch "ping -c 2  {cdca_ip}"',
            f'plink -ssh {acu_name}@{bgm_addr} -pw {acu_pwd} -P 21222 -batch "ping -c 2  {cdcq_ip}"',
            f'plink -ssh {acu_name}@{bgm_addr} -pw {acu_pwd} -P 21222 -batch "ping -c 2  {tcam_ip}"'
        ]
    else:
        acu_cmds = [
            f'sshpass -p {acu_pwd} ssh -p21222 {acu_name}@{bgm_addr} "ping -c 2  {bgm_ip}"',
            f'sshpass -p {acu_pwd} ssh -p21222 {acu_name}@{bgm_addr} "ping -c 2  {cdca_ip}"',
            f'sshpass -p {acu_pwd} ssh -p21222 {acu_name}@{bgm_addr} "ping -c 2  {cdcq_ip}"',
            f'sshpass -p {acu_pwd} ssh -p21222 {acu_name}@{bgm_addr} "ping -c 2  {tcam_ip}"'
        ]
    for cmd in acu_cmds:
        if not make_subprocess(cmd):
            return False
    return True


def config_acu(bgm_addr, bgm_pwd, script_path):
    try:
        if sysstr == 'Windows':
            cmd1 = [
                f'pscp -pw {bgm_pwd} -scp {script_path}/script/port_mapping/config_acu.sh  root@{bgm_addr}:/update/tools/',
                f'plink -ssh root@{bgm_addr} -pw {bgm_pwd} -batch "chmod 755 /update/tools/config_acu.sh"',
                f'plink -ssh root@{bgm_addr} -pw {bgm_pwd} -batch "/update/tools/config_acu.sh"',
                f'plink -ssh root@{bgm_addr} -pw {bgm_pwd} -batch "/update/tools/config_acu.sh"'
            ]
        else:
            cmd1 = [
                f'sshpass -p {bgm_pwd} scp -r {script_path}/script/port_mapping/config_acu.sh  root@{bgm_addr}:/update/tools/',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "chmod 755 /update/tools/config_acu.sh"',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/update/tools/config_acu.sh"',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/update/tools/config_acu.sh"'
            ]
        for cmd in cmd1:
            make_subprocess(cmd)
    except Exception as e:
        logging.info(f'<acu> acu配置失败{e}')


def pre_acu_endecrypt_test(bgm_addr, acu_name, acu_pwd):
    if sysstr == 'Windows':
        cmds1 = [
            f'pscp -pw {acu_pwd} -P 21222 -scp {os.path.join(get_script_path(), "acu_arm_linux_aarch_64", "endecrypt_test")} {acu_name}@{bgm_addr}:/opt/data/',
            f'plink -ssh {acu_name}@{bgm_addr} -pw {acu_pwd} -P 21222 -batch "cd /opt/data/;"chmod -R 777 /opt/data/endecrypt_test"',
            f'plink -ssh {acu_name}@{bgm_addr} -pw {acu_pwd} -P 21222 -batch "cd /opt/data/; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/jidu_output/acu_adapter/bootes/lib:/opt/certs_key/lib:/opt/data/safety/usr/lib;/opt/data/endecrypt_test"',
        ]
    else:
        cmds1 = [
            f'sshpass -p {acu_pwd} scp -P 21222 -r {os.path.join(get_script_path(), "acu_arm_linux_aarch_64", "endecrypt_test")} {acu_name}@{bgm_addr}:/opt/data/',
            f'sshpass -p {acu_pwd} ssh -p 21222 {acu_name}@{bgm_addr} "cd /opt/data/; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/jidu_output/acu_adapter/bootes/lib:/opt/certs_key/lib:/opt/data/safety/usr/lib;/opt/data/endecrypt_test"',
        ]
    for cmd1 in cmds1:
        if not make_subprocess(cmd1, get_script_path()):
            return False
    return True


def pre_acu_endecrypt_json(bgm_addr, acu_name, acu_pwd):
    if sysstr == 'Windows':
        cmds1 = [
            f'mkdir {os.path.join(script_path, "script", "acuendecryptjson")}',
            f'pscp -pw {acu_pwd} -P 21222 -scp {acu_name}@{bgm_addr}:/opt/data/endecrypt.json {os.path.join(script_path, "script", "acuendecryptjson")}',
        ]
    else:
        cmds1 = [
            f'mkdir -p {script_path}/script/acuendecryptjson',
            f'sshpass -p {acu_pwd} scp -P 21222 -r {acu_name}@{bgm_addr}:/opt/data/endecrypt.json {script_path}/script/acuendecryptjson/',
            f'chmod -R 755 {script_path}/script/*'
        ]
    for cmd in cmds1:
        make_subprocess(cmd, get_script_path())
    json_path = f'{os.path.join("acuendecryptjson", "endecrypt.json")}'
    try:
        acu_encrypt = check_endecrypt_json(json_path, 'ACU')
        return acu_encrypt
    except JSONDecodeError as e:
        logging.info(f'{e}')
        return 'ACU'


def recovery_acu_endecrypt(bgm_addr, acu_name, acu_pwd):
    try:
        if sysstr == 'Windows':
            cmd1 = [
                f'plink -pw {acu_pwd} -P 21222 -batch -ssh {acu_name}@{bgm_addr} "rm -rf /opt/data/endecrypt_test /opt/data/endecrypt.json"',
            ]
        else:
            cmd1 = [
                f'sshpass -p {acu_pwd} ssh -p 21222 {acu_name}@{bgm_addr} "rm -rf /opt/data/endecrypt_test /opt/data/endecrypt.json"',
            ]
        for cmd in cmd1:
            make_subprocess(cmd, get_script_path())
    except Exception as e:
        logging.info(f'<acu> recovery_acu_endecrypt failed: {e}')


def get_acu_endecrypt_version(bgm_addr, acu_name, acu_pwd):
    try:
        if sysstr == 'Windows':
            cmd = f'echo y | plink -no-antispoof -pw {acu_pwd} -P 21222 -ssh {acu_name}@{bgm_addr} "cat /opt/jidu_output/acu_adapter/version"'
            logging.info('<acu> acu_version')
            make_subprocess(cmd, get_script_path())
        else:
            if sysstr == 'Linux':
                child1 = spawn(
                    f'sshpass -p {acu_pwd} ssh -p 21222 {acu_name}@{bgm_addr} "cat /opt/jidu_output/acu_adapter/version"',
                    timeout=120)
                logging.info('<acu> acu_version:')
                logging.info(child1.read().decode('utf-8'))
            else:
                cmd = f'sshpass -p {acu_pwd} ssh -p 21222 {acu_name}@{bgm_addr} "cat /opt/jidu_output/acu_adapter/version"',
                logging.info('<acu> acu_version')
                make_subprocess(cmd, get_script_path())
    except Exception as e:
        logging.info(f'<acu> acu 版本号获取 failed    {e}')
        return 'ACU'


def pull_log(obdaddr, username, password, destpath, port=None):
    if not os.path.exists(destpath):
        os.makedirs(destpath, exist_ok=True)
    conn = RemoteTools(host=obdaddr, user=username, port=port, connect_kwargs={'password': password})
    conn.run('pwd', env={})
    conn.check_conn()
    if conn.is_connected ==False:
        return logging.info('connect error')
    remote_path = '/opt/log/bootes'
    conn.get(remote_path=remote_path, local_path=destpath)
    conn.close()
