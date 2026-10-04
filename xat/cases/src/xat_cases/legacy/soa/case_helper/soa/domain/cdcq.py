#!/usr/bin/python3
# coding=UTF-8
import json
import os
import sys
# import logging
from xat_ecu.legacy.common.logger import logger  as logging
import subprocess
import time
import re
import platform

sysstr = platform.system()
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from codesrc.components.pressure.utils import get_script_path, make_subprocess, check_endecrypt_json, spawn_sftp, spawn_ssh
from codesrc.public.utils.connection import RemoteToolsAdb


script_path = os.path.join(get_script_path(), 'domain')
plink_win_path = os.path.join(get_script_path(), 'bin', 'plink.exe')


# 检查cdcq日志
def check_cdcq(data_path):
    data = os.listdir(data_path)
    logging.info(f'data========{data}')
    for i in data:
        a = i.split('.')[0]
        logging.info(f'a========={a}')
        if a in data and a != 'qlog_default' and a != 'bootes':
            # if a in data:
            os.system(f'rm -rf {data_path}/{a}')
            logging.info(f'cdcq日志和压缩包有重复，已清理:{a}')
            time.sleep(2)


def pull_cdcq_log(bgm_addr, i, cdcq_log_path):
    """
    端口映射方式
    """
    try:
        if os.path.exists(cdcq_log_path) is False:
            os.makedirs(cdcq_log_path)
        os.chdir(cdcq_log_path)
        logging.info(f'开始拉第{i}次cdcq日志')
        cmds1 = [
            f'ssh -p 11222 -o StrictHostKeyChecking=no root@{bgm_addr} "/mnt/bin/sync"',
            f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/cp -r /data/log/ /data/logs"',
            f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/cp -r /mnt/etc/soa/common/service_monitor.json /data/logs"',
            f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/cp -r /data/bootes/ /data/bootes2"',
            f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/tar -zcvf /data/logs.tar.gz /data/logs"',
            f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/tar -zcvf /data/bootes2.tar.gz /data/bootes2"',
            'mkdir -p coredump'
        ]
        for cmd1 in cmds1:
            make_subprocess(cmd1)

        cmds3 = [
            f"get -r data/bootes2.tar.gz {cdcq_log_path}",
            f"get -r /data/logs.tar.gz {cdcq_log_path}",
            f"get -r /var/log {os.path.join(cdcq_log_path, 'coredump')}"
        ]
        try:
            spawn_sftp(cmds3, bgm_addr)
        except Exception as e:
            logging.info(e)
        cmds2 = [
            'tar -xvf logs.tar.gz',
            'tar -xvf bootes2.tar.gz'
        ]
        for cmd2 in cmds2:
            make_subprocess(cmd2)
        try:
            logging.info('开始2次解压cdcq gz log')
            data_path = './data/logs/log'
            check_cdcq(data_path)
            cmd3 = 'gunzip ./data/logs/log/*.gz'
            make_subprocess(cmd3)
        except Exception as e:
            logging.info(f'没有cdcq logs，无需备份{e}')

    except Exception as e:
        logging.info(f'pull cdcq log failed================={e}')
        pull_cdcq_log(bgm_addr, i, cdcq_log_path)


def rm_cdcq_log(bgm_addr, bgm_pwd, index,item=None):
    """端口映射方式"""
    if not (item and  'cdc' in item["poweroff"]):
        logging.info('cdcq 不下电 日志不清理')
    else:
        logging.info('开始清理cdcq日志')
        try:
            cmd = f'ssh -p 11222 -o StrictHostKeyChecking=no root@{bgm_addr} "/mnt/bin/rm -rf /data/log/* /data/bootes/* /data/bootes2/*  /data/bootes2.tar.gz  /data/logs/* /data/logs.tar.gz  /var/log/* /data/varlog*"'
            make_subprocess(cmd)
            logging.info('cdcq日志清理Finish')
        except Exception as e:
            logging.info(f'cdcq 日志清理 failed================={e}')


def check_cdcq_network(bgm_addr, bgm_ip, cdca_ip, acu_ip, tcam_ip):
    if sysstr == 'Windows':
        from pexpect import popen_spawn, EOF
    else:
        from pexpect import spawn, EOF
    cmd = f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/ping -c 2  {bgm_ip}"'
    if sysstr == 'Windows':
        child = popen_spawn(cmd, timeout=20)
    else:
        child = spawn(cmd, timeout=20)
    res1 = child.expect(['Are*', 'adb*', EOF])
    time.sleep(2)
    if res1 == 0:
        child.sendline('yes')
        child.read()
    acu_cmds = [
        f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/ping -c 2  {bgm_ip}"',
        f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/ping -c 2  {cdca_ip}"',
        f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/ping -c 2  {tcam_ip}"',
        f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/ping -c 2  {acu_ip}"'
    ]
    for cmd in acu_cmds:
        if not make_subprocess(cmd):
            return False
    return True


def pre_cdcq(bgm_addr):
    """
        cdcq前置准备环境方法
        1、第一次刷机后需要配置ssh-key
        2、mount /mnt目录获取权限，备份bootes日志配置文件使用sftp交互模式拉取到本地修改
        3、修改后推送到域控/mnt/etc/soa/common/ 目录下
    """
    cmds1 = [
        f'ssh-keygen -f "/root/.ssh/known_hosts" -R "[{bgm_addr}]:11222"',
        f"mkdir -p {os.path.join(script_path, 'script', 'cdcqbootesjson')}",
        f"chmod -R 755  {os.path.join(script_path, 'script', 'cdcqbootesjson')}"
    ]
    for cmd1 in cmds1:
        make_subprocess(cmd1)
    # 处理cdc q 侧 crash指定文件修改
    update_jidu_slm_cmd1 = r"/mnt/bin/sed -i '/polaris_service_carservice/,/<\/SLM:component>/d' /mnt/scripts/slm/jidu_slm.xml"
    update_jidu_slm_cmd2 = r"/mnt/bin/sed -i '/pavaro_wti/,/<\/SLM:component>/d' /mnt/scripts/slm/jidu_slm.xml"
    update_jidu_slm_cmd3 = r"/mnt/bin/sed -i '/bacu_wti_adapter_app/,/<\/SLM:component>/d' /mnt/scripts/slm/jidu_slm.xml"
    cmds2 = [
        # ssh -o 跳过映射cdcq和bgm之间的秘钥验证上电后跳过一次即可
        f'ssh -p 11222 -o StrictHostKeyChecking=no root@{bgm_addr} "/ifs/bin/mount -urw /mnt/; /mnt/bin/cp -r /mnt/etc/soa/common/bootes_config.json /mnt/etc/soa/common/bootes_config_old.json"',
        f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/mount -urw /mnt/; /mnt/bin/mkdir -p /data/bootes"',
        f'ssh -p 11222 root@{bgm_addr} "{update_jidu_slm_cmd1}"',
        f'ssh -p 11222 root@{bgm_addr} "{update_jidu_slm_cmd2}"',
        f'ssh -p 11222 root@{bgm_addr} "{update_jidu_slm_cmd3}"'
    ]
    spawn_ssh(cmds2)
    cmds3 = [
        f'ssh-keygen -f "/root/.ssh/known_hosts" -R "[{bgm_addr}]:11222"',
        f"get -r /mnt/etc/soa/common/bootes_config_old.json {os.path.join(script_path, 'script', 'cdcqbootesjson', 'bootes_config_old.json')}"
    ]
    spawn_sftp(cmds3, bgm_addr)
    # sftp的get方法异步执行，sleep一下
    time.sleep(10)
    update_cdcq_bootes_file(bgm_addr)
    logging.info('CDCQ 环境配置 Finish')


def update_cdcq_bootes_file(bgm_addr):
    with open(f"{os.path.join(script_path, 'script', 'cdcqbootesjson', 'bootes_config_old.json')}", 'r',
              encoding='utf-8') as f:
        data = json.load(f)
        if 'log_config' in data.keys() and data['log_config']['spdlogConfig']['spdLogMaxSize'] == 10:
            logging.info('cdcq bootes_config.json无需修改')
        else:
            data['log_config']['spdlogConfig']['eaSpdlogFile'] = True
            data['log_config']['spdlogConfig']['spdLogDir'] = '/data/bootes/'
            data['log_config']['spdlogConfig']['spdLogMaxSize'] = 10
            data['log_config']['spdlogConfig']['spdLogFileWithPid'] = True
            with open(f"{os.path.join(script_path, 'script', 'cdcqbootesjson', 'bootes_config.json')}", 'w',
                      encoding='utf-8') as f1:
                f1.write(json.dumps(data, indent=4, ensure_ascii=False))
                logging.info('cdcq bootes_config 本地修改 success')
            cmd2s = [
                f"put -r {os.path.join(script_path, 'script', 'cdcqbootesjson', 'bootes_config.json')} /mnt/etc/soa/common/"
            ]
            spawn_sftp(cmd2s, bgm_addr)
            # sftp的put方法异步执行，sleep一下
            time.sleep(10)
        cmds = [
            f'rm -rf {os.path.join(script_path, "script", "cdcqbootesjson")}'
        ]
        for cmd in cmds:
            make_subprocess(cmd)

def config_cdcq(bgm_addr, bgm_pwd, script_path):
    try:
        if sysstr == 'Windows':
            cmds = [
                f'pscp -pw {bgm_pwd} -scp {script_path}/script/port_mapping/config_cdcq.sh  root@{bgm_addr}:/update/tools/',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "chmod 755 /update/tools/config_cdcq.sh"',
                f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/update/tools/config_cdcq.sh"'
            ]
        else:
            cmds = [
                f'sshpass -p {bgm_pwd} scp -r {script_path}/script/port_mapping/config_cdcq.sh  root@{bgm_addr}:/update/tools/',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "chmod 755 /update/tools/config_cdcq.sh"',
                f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/update/tools/config_cdcq.sh"'
            ]
        for cmd in cmds:
            make_subprocess(cmd)
    except Exception as e:
        logging.info(f'<cdcq> cdcq配置失败failed{e}')


def pre_cdcq_endecrypt_test(bgm_addr):
    if sysstr == 'Windows':
        cmds1 = [
            f'plink -no-antispoof -P 11222 -ssh root@{bgm_addr} "/ifs/bin/mount -urw /mnt"',
            f'plink -no-antispoof -P 11222 -ssh root@{bgm_addr} "/mnt/bin/mkdir -p /data/tools"',
            f'plink -no-antispoof -P 11222 -ssh root@{bgm_addr} "/ifs/bin/chmod -R 777 /data/tools"'
        ]
        for cmd in cmds1:
            make_subprocess(cmd, get_script_path())

    else:
        cmds1 = [
            f'ssh-keygen -f "/root/.ssh/known_hosts" -R "[{bgm_addr}]:11222"',
            f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/mount -urw /mnt"',
            f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/mkdir -p /data/tools"',
            f'ssh -p 11222 root@{bgm_addr} "/ifs/bin/chmod -R 777 /data/tools"'
        ]
        spawn_ssh(cmds1)

    cmds2 = [
        f'/ifs/bin/mount -urw /mnt',
        f'put -r {os.path.join(get_script_path(), "cdc_qnx_aarch_64", "endecrypt_test")}  /data/tools/endecrypt_test'
    ]
    spawn_sftp(cmds2, bgm_addr, get_script_path())
    return True


def pre_cdcq_endecrypt_json(bgm_addr):
    if sysstr == 'Windows':
        run_test_cmds = [
            f'mkdir {os.path.join(script_path, "script", "cdcqendecryptjson")}',
            f'plink -no-antispoof -P 11222 -ssh root@{bgm_addr} "cd /data/tools/;/ifs/bin/chmod -R 777 /data/tools"',
            f'plink -no-antispoof -P 11222 -ssh root@{bgm_addr} "cd /data/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/lib64;/data/tools/endecrypt_test"'
        ]
        for run_test_cmd in run_test_cmds:
            make_subprocess(run_test_cmd, get_script_path())
        cmd = f'echo y | {plink_win_path} -no-antispoof -P 11222 -ssh root@{bgm_addr} "/mnt/bin/cat /data/tools/endecrypt.json"'
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        if result.returncode == 0:
            content = result.stdout
            pattern = r'"encrypt":"([^"]*)"'
            match = re.search(pattern, content)
            if match:
                encrypt_content = match.group(1)
                return encrypt_content
            else:
                logging.info("<CDCQ> No result match found")
                return "CDCQ"
        else:
            logging.info("<CDCQ> Error executing command:")
            logging.info(result.stderr)
    else:
        cmds1 = [
            f'mkdir -p {os.path.join(script_path, "script", "cdcqendecryptjson")}',
            f'chmod -R 755 {script_path}/script/*',
            f'ssh -p 11222 root@{bgm_addr} "cd /data/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/lib64;/data/tools/endecrypt_test"',
        ]
        for cmd1 in cmds1:
            make_subprocess(cmd1)
        cmds1 = [
            f'get -r /data/tools/endecrypt.json  {os.path.join(script_path, "script", "cdcqendecryptjson")}'
        ]
        spawn_sftp(cmds1, bgm_addr, get_script_path())
        json_path = f'{os.path.join("cdcqendecryptjson", "endecrypt.json")}'
        if sysstr == 'Linux':
            make_subprocess(f'chmod -R 755 {script_path}/script/*')
        cdcq_encrypt = check_endecrypt_json(json_path, 'CDCQ')
        return cdcq_encrypt


def recovery_cdcq_endecrypt(bgm_addr):
    try:
        if sysstr == 'Windows':
            cmds1 = [
                f'plink -P 11222 -ssh root@{bgm_addr} -batch "/mnt/bin/rm -rf /data/tools"'
            ]
        else:
            cmds1 = [
                f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/rm -rf /data/tools"'
            ]
        for cmd1 in cmds1:
            make_subprocess(cmd1, get_script_path())
    except Exception as e:
        logging.info(f'<cdcq> recovery_cdcq_endecrypt failed:{e}')


def clean_cdcq_win_ssh(bgm_addr):
    from subprocess import Popen, PIPE
    cmd = f'ssh-keygen -f $env:USERPROFILE\\.ssh\\known_hosts -R "[{bgm_addr}]:11222"'
    process = Popen(["powershell.exe", cmd], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        logging.info(f"Command executed successfully:\n{stdout.decode('utf-8')}")
    else:
        logging.info(f"Error executing command:\n{stderr.decode('utf-8')}")


def get_cdcq_endecrypt_version(bgm_addr):
    try:
        if sysstr == 'Windows':
            clean_cdcq_win_ssh(bgm_addr)
            cmd = f'echo y | plink -no-antispoof -P 11222 -ssh root@{bgm_addr} "/mnt/bin/cat /mnt/etc/build.prop"'
            logging.info('<cdcq> cdcq_version')
            make_subprocess(cmd, get_script_path())
        else:
            p = subprocess.Popen(
                f'ssh -p 11222 root@{bgm_addr} "/mnt/bin/cat /mnt/etc/build.prop"', stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            logging.info(f'<cdcq> cdcq_version: {out.decode()}')
    except Exception as e:
        logging.info(f'<cdcq> cdcq_version 获取 failed: {e}')
        return 'CDCQ'


def pull_log(obdaddr, username, password, destpath, port=None):
    if not os.path.exists(destpath):
        os.makedirs(destpath, exist_ok=True)
    conn = RemoteTools(host=obdaddr, user=username, port=port, connect_kwargs={'password': ''})
    conn.run('pwd', env={})
    conn.check_conn()
    if conn.is_connected == False:
        return logging.info('connect error')
    data_path = '/data/log'
    conn.get(remote_path=data_path, local_path=destpath)
    var_path = '/var/log'
    conn.get(remote_path=var_path, local_path=destpath)
    bootes_path = '/data/bootes'
    conn.get(remote_path=bootes_path, local_path=destpath)
    conn.close()
