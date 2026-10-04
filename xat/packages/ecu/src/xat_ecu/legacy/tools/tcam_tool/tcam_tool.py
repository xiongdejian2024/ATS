#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : tcam_tool.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/24 19:22
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import os
import sys
import time
import pyttsx3
import paramiko
import threading
from loguru import logger
from ping3 import ping
from datetime import datetime


logger.remove()
logger.add(sys.stdout,
                format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                       "<level>{message}</level>",  # 日志内容
                level="INFO"
                )

log_file_path = os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath('.'), 'test.log')
if os.path.exists(log_file_path):
    os.remove(log_file_path)

logger.add(log_file_path,
                format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                       "{process.name} | "  # 进程名
                       "{thread.name} | "  # 进程名
                       "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                       ":<cyan>{line}</cyan> | "  # 行号
                       "<level>{level}</level>: "  # 等级
                       "<level>{message}</level>",  # 日志内容
                # level="INFO"
                )


class SshOperate(object):

    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh_client = None

    def connect_server(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

    def close_server(self):
        if self.ssh_client:
            self.ssh_client.close()

    def exec_command(self, cmd):
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)

        try:
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            logger.info(f"Command Output:{output}")
            if error:
                logger.warning(f"Command Error:{error}")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/tcam_tool/tcam_tool.py")
            logger.warning(f"exec {cmd} cmd error, got:{e}")

    def __del__(self):
        if self.ssh_client:
            self.ssh_client.close()


def ping_some_ip(host, src_addr=None):
    second = ping(host, src_addr=src_addr)
    return second


def voice_notice(text="tcam offline, tcam offline, please power on again"):
    lock.acquire()
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # 女性语音，索引可能根据安装的语音库而异

        engine.setProperty('rate', 100)  # 语速设置为100
        engine.setProperty('volume', 1)  # 音量设置为1

        engine.say(text)
        engine.runAndWait()
    finally:
        lock.release()


def check_adb_devices():
    adb_dict = {}
    ret = os.popen(f'adb devices -l').readlines()
    if len(ret) == 1:
        logger.debug('未识别到adb 设备...')
        return adb_dict
    else:
        for n in ret[1:]:
            if 'device' in n:
                device_id = str(n).strip().split('device')[0].strip()
                name = str(n).strip().split('device')[1].strip()
                adb_dict[device_id] = name

        logger.debug('adb设备数量={}，adb_list={}'.format(len(adb_dict), adb_dict))
        return adb_dict


def check_adb_online():
    while True:
        try:
            device_dict = check_adb_devices()
            logger.info(f"devices dict is:{device_dict}")
            if not device_dict:
                voice_notice(f"adb devices offline, adb devices offline")
            time.sleep(check_adb_time_interval)
        except KeyboardInterrupt:
            logger.warning(f"exit with: KeyboardInterrupt")
            break
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/tcam_tool/tcam_tool.py")
            logger.warning(f"check adb devices error,got:{e}")


def check_tcam_ip():
    ssh_obj = SshOperate("172.16.5.31", 22, "root", "tcam@rWh0bhf")
    tcam_now_connect_net_flag = True
    while True:
        try:
            result = ping_some_ip(host, src_addr)
            if not result:
                tcam_now_connect_net_flag = False
                logger.warning(f'ping-{host} 失败！')
                voice_notice()
            else:
                logger.info('ping-{}成功，耗时{}s'.format(host, result))
                if not tcam_now_connect_net_flag:
                    try:
                        ssh_obj.connect_server()
                        time_now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
                        ssh_obj.exec_command(f'timedatectl set-timezone Asia/Shanghai')
                        ssh_obj.exec_command(f'date -s "{time_now}"')
                        tcam_now_connect_net_flag = True
                    finally:
                        ssh_obj.close_server()

        except KeyboardInterrupt:
            logger.warning(f"ping tcam theading exit.")
            break
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/tcam_tool/tcam_tool.py")
            logger.warning(f"ping {host} error,got:{e}")
        time.sleep(check_tcam_network_time_interval)


if __name__ == '__main__':
    lock = threading.Lock()
    check_adb_time_interval = 15
    check_tcam_network_time_interval = 5
    host = '172.16.5.31'
    src_addr = None
    threading.Thread(target=check_tcam_ip, daemon=True).start()
    threading.Thread(target=check_adb_online, daemon=True).start()
    while True:
        try:
            key = input()
            if key.lower() == 'q':
                logger.info(f"closing...")
                break
        except KeyboardInterrupt:
            logger.warning(f"force exit...")
            break
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/tcam_tool/tcam_tool.py")
            logger.warning(f"error,got:{e}")
            time.sleep(2)


