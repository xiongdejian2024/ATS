#!/usr/bin/python3
# coding=UTF-8
import json
import os
import sys
import subprocess
import logging
import time
from collections import OrderedDict


import platform

sysstr = platform.system()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from codesrc.components.pressure.utils import make_subprocess, make_ssh_client, check_endecrypt_json, get_script_path, handle_env, spawn_bgm
from codesrc.public.utils.connection import RemoteToolsAdb


script_path = os.path.join(get_script_path(), 'domain')


def get_bgm_version(bgm_uname, bgm_addr, bgm_pwd):
    try:
        p = subprocess.Popen(
            f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "cat /app/etc/build.prop"', stdout=subprocess.PIPE,
            shell=True)
        out, err = p.communicate()
        data = out.decode()
        datas = data.split('\n')
        v = datas[9].split('=')[1]
        logging.info('<bgm> bgm_version:')
        logging.info(v)
        return v
    except Exception as e:
        logging.info(f'<bgm> bgm 版本号获取 failed    {e}')
        return 'BGM'


def tar_bgm(bgm_pwd, bgm_addr):
    try:
        if sysstr == 'Windows':
            cmd = [f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "mkdir -p /update/logs"',
                   f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "chmod -R 777 /update/logs"',
                   f'plink -p {bgm_pwd} ssh root@{bgm_addr} -batch "cp -r /log/bootes /update/logs"',
                   f'plink -p {bgm_pwd} ssh root@{bgm_addr} -batch "tar -zcvPf /update/logs.tar.gz /update/logs"']
        else:
            cmd = [f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "mkdir -p /update/logs"',
                   f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "chmod -R 777 /update/logs"',
                   f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "cp -r /log/bootes /update/logs"',
                   f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "tar -zcvPf /update/logs.tar.gz /update/logs"']
        for i in cmd:
            make_subprocess(i)
    except Exception as e:
        logging.error(f'bgm 备份 failed{e}')


# 获取bgm log
def pull_bgm_log(bgm_uname, bgm_pwd, bgm_addr, i, bgm_log_path):
    if os.path.exists(bgm_log_path) is False:
        if bgm_uname == 'root':
            os.makedirs(bgm_log_path)
        elif bgm_uname == 'jiduer':
            bgm_log_path = os.path.join(bgm_log_path, "update")
            os.makedirs(bgm_log_path)

    os.chdir(bgm_log_path)
    logging.info(f"开始拉第{i}次bgm日志")
    try:
        if bgm_uname == 'root':
            tar_bgm(bgm_pwd, bgm_addr)
            if sysstr == 'Windows':
                cmds1 = [f'pscp -pw {bgm_pwd} -scp root@{bgm_addr}:/update/logs.tar.gz ./',
                         f'pscp -pw {bgm_pwd} -scp root@{bgm_addr}:/log/jetlog* ./',
                         f'pscp -pw {bgm_pwd} -scp root@{bgm_addr}:/log/coredump ./',
                         f'pscp -pw {bgm_pwd} -scp root@{bgm_addr}:/log/jetcrash ./',
                         f'tar -xvf logs.tar.gz',
                         f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "rm -rf /update/logs.tar.gz"',
                         f'pscp -pw {bgm_pwd} -scp root@{bgm_addr}:/app/etc/service_monitor.json ./']
            else:
                cmds1 = [f'sshpass -p {bgm_pwd} scp -r root@{bgm_addr}:/update/logs.tar.gz ./',
                         f'sshpass -p {bgm_pwd} scp -r root@{bgm_addr}:/log/jetlog* ./',
                         f'sshpass -p {bgm_pwd} scp -r root@{bgm_addr}:/log/coredump ./',
                         f'sshpass -p {bgm_pwd} scp -r root@{bgm_addr}:/log/jetcrash ./',
                         f'tar -xvf logs.tar.gz',
                         f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "rm -rf /update/logs.tar.gz"',
                         f'sshpass -p {bgm_pwd} scp -r root@{bgm_addr}:/app/etc/service_monitor.json ./']
            for cmd1 in cmds1:
                make_subprocess(cmd1)
        if bgm_uname == 'jiduer':
            root_cmds = [
                "sync",
                "mkdir -p /update/logs",
                "chmod -R 777 /update/logs",
                "cp -r /log/bootes /update/logs",
            ]
            spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds)
            cmds = [
                f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/update/logs ./',
                f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/log/jetlog* ./',
                f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/log/coredump ./',
                f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/log/jetcrash ./',
            ]
            for cmd in cmds:
                make_subprocess(cmd)
            logging.info('Pull bgm log Finish')
    except Exception as e:
        logging.error(f'pull bgm log  failed {e}')


def rm_bgm_log(bgm_uname, bgm_pwd, bgm_addr, index, item=None):
    try:
        if bgm_uname == 'root':
            if 0 <= index <= 10 or 20 < index <= 25:
                logging.info('开始清理bgm日志')
                if sysstr == 'Windows':
                    cmd = (
                        f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "rm -rf /update/acu_adapter/* /update/logs* /update/image* /update/installer /update/bootes/* /update/coredump/* /update/logs.tar.gz /update/bootes2.tar.gz /log/jetlog* /log/coredump/* /log/bootes/* /log/jetcrash/*"')
                else:
                    cmd = (
                        f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "rm -rf /update/acu_adapter/* /update/logs* /update/image* /update/installer /update/bootes/* /update/coredump/* /update/logs.tar.gz /update/bootes2.tar.gz /log/jetlog* /log/coredump/* /log/bootes/* /log/jetcrash/*"')
                make_subprocess(cmd)
                cmd = (f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "sync"')
                make_subprocess(cmd)
                logging.info('bgm日志清理 success')
            else:
                logging.info('bgm未下电，日志不清理')
        elif bgm_uname == 'jiduer':
            if not (item and 'bgm' in item["poweroff"]):
                logging.info('bgm未下电，日志不清理')
            else:
                root_cmds = [
                    "rm -rf /data/debug_script_executed_count /update/bootes/* /update/coredump/* /update/logs/* /log/jetlog* /log/coredump/* /log/bootes/* /log/jetcrash/*",
                    "sync"
                ]
                spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds)
                logging.info('bgm日志清理 Finish')
    except Exception as e:
        logging.info(f'bgm清理日志时候连接 failed；bgm连接 failed，bgm重新上下电{e}')
        os.system('poweroff bgm')
        time.sleep(10)
        os.system('poweron bgm')
        time.sleep(60)
        rm_bgm_log(bgm_uname, bgm_pwd, bgm_addr, index)


def check_bgm_network(bgm_uname, bgm_addr, bgm_pwd, cdca_ip, cdcq_ip, tcam_ip, acu_ip):
    bgm_cmds = [
        f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "ping -c 2 {cdca_ip}"',
        f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "ping -c 2 {cdcq_ip}"',
        f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "ping -c 2 {tcam_ip}"',
        f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "ping -c 2 {acu_ip}"',
    ]
    for cmd in bgm_cmds:
        if not make_subprocess(cmd):
            return False
    return True


def pre_bgm(bgm_uname, bgm_addr, bgm_pwd):
    cmds = [
        f"mkdir -p {os.path.join(script_path, 'script', 'bgmbootesjson')}",
    ]
    for cmd1 in cmds:
        make_subprocess(cmd1)
    if bgm_uname == 'root':
        cmds = [
            f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "cp -r /app/etc/s2s.json /app/etc/s2s_old.json"',
            f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "cp -r /app/etc/runenv.sh /app/etc/runenv_old.sh"',
            f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "mv /data/debug.sh /data/debug.sh.bak2"',
            f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "rm -rf /home/root/.ssh/known_hosts /update/image* /update/installer"',
            f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "cp -r /app/etc/bootes_config.json  /app/etc/bootes_config_old.json"',
            f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/app/etc/s2s_old.json {os.path.join(script_path, "script", "bgmbootesjson/")}',
            f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/app/etc/bootes_config_old.json {os.path.join(script_path, "script", "bgmbootesjson/")}',
            f'chmod -R 777 {script_path}/script/*',
        ]
        for cmd1 in cmds:
            make_subprocess(cmd1)
        update_bgm_s2s(bgm_uname, bgm_addr, bgm_pwd)
        update_bgm_runenv(bgm_uname, bgm_addr, bgm_pwd)
        update_bgm_bootes_file(bgm_uname, bgm_addr, bgm_pwd)
    elif bgm_uname == 'jiduer':
        root_cmds = [
            "rm -rf /data/debug.sh",
            "cp /app/etc/runenv.sh /data/debug.sh",
            "sed -i 's/debug.sh/notexists.sh/g' /data/debug.sh",
            "sed -i 's/\/app\/etc/\/data\/pressureetc/g' /data/debug.sh",
            # "sed -i 's/BOOTES_HOME_DIR=.*/BOOTES_HOME_DIR=\/data\/pressureetc/g' /data/debug.sh",
            "grep -q '  export BOOTES_HOME_DIR' /data/debug.sh || sed -i '15a\\  export BOOTES_HOME_DIR=/data\/pressureetc' /data/debug.sh",
            "rm -rf /data/pressureetc/",
            "mkdir -p /data/pressureetc/",
            "cp -r /app/etc/* /data/pressureetc/",
            "cp -r /data/pressureetc/s2s.json /data/pressureetc/s2s_old.json",
            "cp -r /data/pressureetc/bootes_config.json /data/pressureetc/bootes_config_old.json",
            "sed -i 's/BOOTES_HOME_DIR=.*/BOOTES_HOME_DIR=\/data\/pressureetc/g' /data/pressureetc/bgm_app_env.sh",
            "rm /data/debug_script_executed_count",
            "sync"
        ]

        spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds)
        time.sleep(10)
        scp_cmds = [
            f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/data/pressureetc/s2s_old.json {os.path.join(script_path, "script", "bgmbootesjson/")}',
            f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/data/pressureetc/bootes_config_old.json {os.path.join(script_path, "script", "bgmbootesjson/")}'
        ]
        for cmd1 in scp_cmds:
            make_subprocess(cmd1)

        update_bgm_s2s(bgm_uname, bgm_addr, bgm_pwd)
        update_bgm_bootes_file(bgm_uname, bgm_addr, bgm_pwd)

    logging.info('BGM  环境配置 Finish')


def update_bgm_s2s(bgm_uname, bgm_addr, bgm_pwd):
    with open(f'{os.path.join(script_path, "script", "bgmbootesjson", "s2s_old.json")}', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if 'mcuIpUdp' in data.keys() and data['mcuIpUdp'] == '169.254.93.253':
            logging.info('bgm s2s 文件无需修改')
        else:
            data["LogStorageFlag"] = True
            new_data = OrderedDict()
            for k, v in data.items():
                if k == 'tcpReqClientPort':
                    new_data["mcuIpUdp"] = "169.254.93.253"
                    new_data["mpuIpUdp"] = "169.254.1.1"
                new_data[k] = v
            new_dict = dict(new_data)
            with open(f'{os.path.join(script_path, "script", "bgmbootesjson", "s2s.json")}', 'w',
                      encoding='utf-8') as fs:
                fs.write(json.dumps(new_dict, indent=4, ensure_ascii=False))
                logging.info('s2s 本地修改 success')
            if bgm_uname == 'root':
                cmds = [
                    f'sshpass -p {bgm_pwd} scp -r {os.path.join(script_path, "script", "bgmbootesjson", "s2s.json")} {bgm_uname}@{bgm_addr}:/app/etc/',
                    f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "cat /app/etc/s2s.json"',
                ]
                for cmd in cmds:
                    make_subprocess(cmd)
            elif bgm_uname == 'jiduer':
                cmds = [
                    f'sshpass -p {bgm_pwd} scp -r {os.path.join(script_path, "script", "bgmbootesjson", "s2s.json")} {bgm_uname}@{bgm_addr}:/tmp/jiduer',
                ]
                for cmd in cmds:
                    make_subprocess(cmd)
                root_cmds = [
                    "mv /tmp/jiduer/s2s.json /data/pressureetc",
                    "sync",
                ]
                spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds)
                time.sleep(2)


def update_bgm_bootes_file(bgm_uname, bgm_addr, bgm_pwd):
    with open(f'{script_path}/script/bgmbootesjson/bootes_config_old.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if 'log_config' in data.keys() and data['log_config']['spdlogConfig']['spdLogMaxSize'] == 10:
            logging.info('bgm bootes_config.json无需修改')
        else:
            data['log_config']['spdlogConfig']['eaSpdlogFile'] = True
            data['log_config']['spdlogConfig']['spdLogMaxSize'] = 10
            data['log_config']['spdlogConfig']['spdLogFileWithPid'] = True
            logging.info(data)
            with open(f'{os.path.join(script_path, "script", "bgmbootesjson", "bootes_config.json")}', 'w',
                      encoding='utf-8') as f1:
                f1.write(json.dumps(data, indent=4, ensure_ascii=False))
                logging.info('bgm bootes_config 本地修改 success')
            if bgm_uname == 'root':
                cmds2 = [
                    f'sshpass -p {bgm_pwd} scp -r {os.path.join(script_path, "script", "bgmbootesjson", "bootes_config.json")} root@{bgm_addr}:/app/etc/',
                    f'rm -rf {os.path.join(script_path, "script", "bgmbootesjson")}'
                ]
                for cmd2 in cmds2:
                    make_subprocess(cmd2)
            elif bgm_uname == 'jiduer':
                cmds = [
                    f'sshpass -p {bgm_pwd} scp -r {os.path.join(script_path, "script", "bgmbootesjson", "bootes_config.json")} {bgm_uname}@{bgm_addr}:/tmp/jiduer',
                    f'rm -rf {os.path.join(script_path, "script", "bgmbootesjson")}'
                ]
                for cmd in cmds:
                    make_subprocess(cmd)
                root_cmds = [
                    "mv /tmp/jiduer/bootes_config.json /data/pressureetc",
                    "sync",
                ]
                spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds)
                time.sleep(2)


def config_bgm(bgm_addr, bgm_pwd):
    if sysstr == 'Windows':
        cmds = [
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "echo 1 > /proc/sys/net/ipv4/ip_forward"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 3131 -j DNAT --to-destination 172.16.9.31:5555"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 1313 -j DNAT --to-destination 172.16.9.13:5555"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 11222 -j DNAT --to-destination 172.16.9.11:22"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 21222 -j DNAT --to-destination 172.16.9.21:22"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/usr/sbin/iptables -P INPUT ACCEPT"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/usr/sbin/iptables -P OUTPUT ACCEPT"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "/usr/sbin/iptables -P FORWARD ACCEPT"',
            f'plink -pw {bgm_pwd} -ssh root@{bgm_addr} -batch "mkdir -p /update/tools"',
        ]
    else:
        cmds = [
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "echo 1 > /proc/sys/net/ipv4/ip_forward"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 3131 -j DNAT --to-destination 172.16.9.31:5555"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 1313 -j DNAT --to-destination 172.16.9.13:5555"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 11222 -j DNAT --to-destination 172.16.9.11:22"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/usr/sbin/iptables -t nat -A PREROUTING --dst 169.254.1.1 -p tcp --dport 21222 -j DNAT --to-destination 172.16.9.21:22"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/usr/sbin/iptables -P INPUT ACCEPT"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/usr/sbin/iptables -P OUTPUT ACCEPT"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "/usr/sbin/iptables -P FORWARD ACCEPT"',
            f'sshpass -p {bgm_pwd} ssh root@{bgm_addr} "mkdir -p /update/tools"',
        ]
    for cmd in cmds:
        make_subprocess(cmd)
    logging.info('<bgm> bgm配置完成')


def pre_bgm_endecrypt_test(bgm_uname, bgm_addr, bgm_pwd, bgm_ver):
    if bgm_ver == 'v1.0.0':
        if sysstr == 'Windows':
            cmds1 = [
                f'pscp -pw {bgm_pwd} -scp {os.path.join(get_script_path(), "bgm_linux_aarch_64", "endecrypt_test")} {bgm_uname}@{bgm_addr}:/update/tools',
                f'plink -pw {bgm_pwd} -ssh {bgm_uname}@{bgm_addr} -batch "cd /update/tools/; /bin/chmod 777 endecrypt_test"',
                f'plink -pw {bgm_pwd} -ssh {bgm_uname}@{bgm_addr} -batch "cd /update/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;/update/tools/endecrypt_test"'
            ]
        else:
            cmds1 = [
                f'sshpass -p {bgm_pwd} scp -r {os.path.join(get_script_path(), "bgm_linux_aarch_64", "endecrypt_test")} {bgm_uname}@{bgm_addr}:/update/tools',
                f"sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} 'chmod 777 -R /update/tools/*'",
                f"sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} 'cd /update/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;/update/tools/endecrypt_test'"
            ]
        for cmd in cmds1:
            if not make_subprocess(cmd, get_script_path()):
                return False
        return True
    elif bgm_ver == 'v1.1.0':
        if sysstr == 'Windows':
            cmds1 = [
                f'pscp -pw {bgm_pwd} -scp {os.path.join(get_script_path(), "bgm_linux_aarch_64", "endecrypt_test")} {bgm_uname}@{bgm_addr}:/update/tools',
                f'plink -pw {bgm_pwd} -ssh {bgm_uname}@{bgm_addr} -batch "cd /update/tools/; /bin/chmod 777 endecrypt_test"',
                f'plink -pw {bgm_pwd} -ssh {bgm_uname}@{bgm_addr} -batch "cd /update/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;/update/tools/endecrypt_test"'
            ]
        else:
            cmds1 = [
                f'sshpass -p {bgm_pwd} scp -r {os.path.join(get_script_path(), "bgm_linux_aarch_64", "endecrypt_test")} {bgm_uname}@{bgm_addr}:/tmp/jiduer',
            ]
        for cmd in cmds1:
            make_subprocess(cmd, get_script_path())

        root_cmds = [
            "mv /tmp/jiduer/endecrypt_test /update/tools",
            "sync",
            "chmod 755 -R /update/tools",
            "cd /update/tools/;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;/update/tools/endecrypt_test'",
        ]
        spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds, get_script_path())
    return True


def pre_bgm_endecrypt_json(bgm_uname, bgm_addr, bgm_pwd):
    if sysstr == 'Windows':
        cmds1 = [
            f'mkdir {os.path.join(script_path, "script", "bgmendecryptjson")}',
            f'pscp -pw {bgm_pwd} -scp {bgm_uname}@{bgm_addr}:/update/tools/endecrypt.json {os.path.join(script_path, "script", "bgmendecryptjson")}',
        ]
    else:
        cmds1 = [
            f'mkdir -p {script_path}/script/bgmendecryptjson',
            f'sshpass -p {bgm_pwd} scp -r {bgm_uname}@{bgm_addr}:/update/tools/endecrypt.json {script_path}/script/bgmendecryptjson',
            f'chmod -R 755 {script_path}/script/*'
        ]
    for cmd in cmds1:
        make_subprocess(cmd, get_script_path())
    json_path = f'{os.path.join("bgmendecryptjson", "endecrypt.json")}'
    bgm_encrypt = check_endecrypt_json(json_path, 'BGM')
    return bgm_encrypt


def recovery_bgm_endecrypt(bgm_uname, bgm_addr, bgm_pwd, bgm_ver):
    try:
        if bgm_ver == 'v1.0.0':
            if sysstr == 'Windows':
                cmds1 = [
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "rm -rf /update/tools"',
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P INPUT DROP',
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P OUTPUT DROP"',
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P FORWARD DROP"'
                ]
            else:
                cmds1 = [
                    f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "rm -rf /update/tools"',
                    f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P INPUT DROP"',
                    f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P OUTPUT DROP"',
                    f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P FORWARD DROP"'
                ]
            for cmd1 in cmds1:
                make_subprocess(cmd1, get_script_path())
        elif bgm_ver == 'v1.1.0':
            if sysstr == 'Windows':
                cmds1 = [
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "rm -rf /update/tools"',
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P INPUT DROP',
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P OUTPUT DROP"',
                    f'plink -pw {bgm_pwd} -ssh -batch {bgm_uname}@{bgm_addr} "/usr/sbin/iptables -P FORWARD DROP"'
                ]
            else:
                root_cmds = [
                    "rm -rf /update/tools",
                    "/usr/sbin/iptables -P INPUT DROP",
                    "/usr/sbin/iptables -P OUTPUT DROP",
                    "/usr/sbin/iptables -P FORWARD DROP"
                ]
                spawn_bgm(bgm_uname, bgm_addr, bgm_pwd, root_cmds, get_script_path())
    except Exception as e:
        logging.info(f'<bgm> recovery_bgm_endecrypt failed: {e}')


def get_bgm_endecrypt_version(bgm_uname, bgm_addr, bgm_pwd):
    try:
        if sysstr == 'Windows':
            script_path = get_script_path()
            env_sm = {**os.environ,
                      'PATH': f"{os.path.join(script_path, 'bin')};{os.environ['PATH']}"}
            p = subprocess.Popen(
                f'plink -pw {bgm_pwd} -ssh {bgm_uname}@{bgm_addr} -batch "cat /app/etc/build.prop"',
                stdout=subprocess.PIPE,
                shell=True, env=env_sm)
        else:
            if sysstr == 'Linux':
                p = subprocess.Popen(
                    f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "cat /app/etc/build.prop"',
                    stdout=subprocess.PIPE,
                    shell=True)
            else:
                p = subprocess.Popen(
                    f'sshpass -p {bgm_pwd} ssh {bgm_uname}@{bgm_addr} "cat /app/etc/build.prop"',
                    stdout=subprocess.PIPE,
                    shell=True, env=handle_env())

        out, err = p.communicate()
        logging.info('<bgm> bgm_version:')
        logging.info(out.decode())
    except Exception as e:
        logging.info(f'<bgm> bgm_version 获取 failed: {e}')
        return 'BGM'


def pull_log(obdaddr, username, password, destpath, port=None):
    if not os.path.exists(destpath):
        os.makedirs(destpath, exist_ok=True)
    conn = RemoteTools(host=obdaddr, user=username, port=port, connect_kwargs={'password': password})
    conn.run('pwd', env={})
    conn.check_conn()
    if conn.is_connected ==False:
        return logging.info('connect error')
    conn.run(f'echo {password} | sudo -S chmod a+r /log/ -R')
    remote_path = '/log/'
    log_file = []
    for file in str(conn.run(f'ls {remote_path}')).split():
        if 'log' in file or 'bootes' in file or 'coredump' in file:
            log_file.append(file)
    logging.info(log_file)
    for f in log_file:
        l_path = os.path.join(destpath, f)
        r_path = remote_path + '/' + f
        conn.get(remote_path=r_path, local_path=l_path)
    conn.close()


def first_ssh_bgm(username, password, obdaddr):
    from pexpect import spawn, EOF
    cmd = f"ssh {username}@{obdaddr}"
    child = spawn(cmd, timeout=20)
    res1 = child.expect(['Are*', 'password*', EOF])
    if res1 == 0:
        child.sendline('yes')
        child.expect('assword:*')
        child.sendline(password)
        child.expect('jiduer*')
        child.sendline('exit')
    child.close()
