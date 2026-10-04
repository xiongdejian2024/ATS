#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :cdca_adb.py
@Time         :2023/8/9 21:52
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import os
import sys
import time

import base64

from xat_ecu.legacy.common.constant import CDCA_CONSTANT, BGM_CONSTANT
from xat_ecu.legacy.common.file_handle import ecu_simulator_abspath

current_path = os.path.dirname(os.path.realpath(__file__))
project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.singleton import SingletonMeta
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download, file_upload


class CDCA_ADB(metaclass=SingletonMeta):
    def __init__(self, connect_type='obd'):
        self.device_name = "BGM"
        self.adb_path = os.path.join(ecu_simulator_abspath, 'interface', 'bgm', 'adb')
        self.HOST_PORT = f'{self.get_host()}:{self.get_port()}'
        self.connect_type = connect_type
        self.current_name = 'root'

    @staticmethod
    def decode_encrypt_string(s):
        return base64.b64decode(s).decode()

    def get_host(self):
        return self.decode_encrypt_string(CDCA_CONSTANT.CDCQ_HOSTNAME)

    def get_port(self):
        return self.decode_encrypt_string(CDCA_CONSTANT.CDCQ_PORT)

    def get_bgm_password(self):
        return self.decode_encrypt_string(BGM_CONSTANT.BGM_PASSWORD)

    def get_bgm_username(self):
        return self.decode_encrypt_string(BGM_CONSTANT.BGM_USERNAME)

    def type_commands(self, commands, timeout=60, **kwargs):
        use_root = kwargs.get('use_root')
        ct = kwargs.get('connect_type')
        if ct is not None:
            connect_type = ct
        else:
            connect_type = self.connect_type
        if '/update/adb' in commands and not use_root:
            outmsg = self.adb_commands(commands, timeout, **kwargs)
        else:
            self.enter_root()
            status, outmsg = command_send(device_name=self.device_name, cmd=commands, timeout=timeout, **kwargs)
            logger.info(f'{commands}执行结果为:{outmsg}')
        return outmsg

    def adb_commands(self, commands, timeout=60, **kwargs):
        ct = kwargs.get('connect_type')
        if ct is not None:
            connect_type = ct
        else:
            connect_type = self.connect_type
        kwargs['connect_type'] = connect_type
        self.exit_root()
        status, outmsg = command_send(device_name=self.device_name, cmd=commands, timeout=timeout, **kwargs)
        self.check_adb_return(outmsg)
        logger.info(f'{commands}执行结果为:{outmsg}')
        return outmsg

    def check_adb_return(self, msg):
        if f"error: device '{self.HOST_PORT}' not found" in msg:
            raise Exception(f'adb execute error, reason: {msg}')

    def exit_root(self, **kwargs):
        ct = kwargs.get('connect_type')
        if ct is not None:
            connect_type = ct
        else:
            connect_type = self.connect_type
        kwargs['connect_type'] = connect_type
        if self.current_name == 'root':
            command_send(device_name=self.device_name,
                         cmd=f'echo {self.get_bgm_password()} | su -c ls {self.get_bgm_username()};'
                             f'su - {self.get_bgm_username()}', **kwargs)
            self.current_name = f'{self.get_bgm_username()}'

    def enter_root(self, **kwargs):
        ct = kwargs.get('connect_type')
        if ct is not None:
            connect_type = ct
        else:
            connect_type = self.connect_type
        kwargs['connect_type'] = connect_type
        if self.current_name != 'root':
            command_send(device_name=self.device_name, cmd=f'echo {self.get_bgm_password()} | sudo -S ls;sudo -s',
                         **kwargs)
            self.current_name = 'root'

    def upload_adb_to_bgm(self, bgm_path='/update'):
        file_upload(device_name=self.device_name, local_path=self.adb_path, remote_path='/tmp',
                    connect_type=self.connect_type)
        self.type_commands(commands=f'chmod 777 /tmp/adb')
        self.type_commands(commands=f'cp -rf /tmp/adb {bgm_path}/')

    def use_root(self):
        self.type_commands(f'/update/adb -s {self.HOST_PORT} root')

    def connect(self):
        ret = self.type_commands('ls /update/adb')
        if 'No such file or directory' in ret:
            self.upload_adb_to_bgm()
        self.exit_root()
        ret = self.type_commands(f'/update/adb connect {self.HOST_PORT}')
        logger.info(ret)
        self.enter_root()
        if 'connected' in ret:
            self.use_root()
            return True
        else:
            raise Exception(f'连接adb失败: {ret}')

    def check_connect_status(self):
        ret = self.type_commands(f'/update/adb -s {self.HOST_PORT} devices', connect_type='obd')
        if f'{self.HOST_PORT}' in ret:
            ret = self.type_commands(f'/update/adb -s {self.HOST_PORT} shell id')
            if 'uid=0' in ret:
                logger.info('adbd is already running as root')
            else:
                self.use_root()
            return True
        else:
            self.connect()

    def disconnect(self):
        ret = self.type_commands(f'/update/adb disconnect {self.HOST_PORT}')
        if "disconnected" in ret:
            return True

    def clear_log(self):
        self.check_connect_status()
        self.type_commands(f'/update/adb -s {self.HOST_PORT} shell rm -rf /data/log/*')

    def get_log(self, my_local='/root'):
        self.check_connect_status()
        log_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
        self.type_commands('rm -rf /log/log.tar.gz')
        self.type_commands(f'/update/adb -s {self.HOST_PORT} shell rm -rf /data/log.tar.gz')
        self.type_commands(f'/update/adb -s {self.HOST_PORT} shell tar -zcvf /data/log.tar.gz /data/log/',
                           timeout=600)
        self.type_commands(f'/update/adb -s {self.HOST_PORT} pull /data/log.tar.gz /log/', timeout=600, use_root=True)
        file_download(device_name=self.device_name, remote_path='/log/log.tar.gz',
                      local_path=f'{my_local}/cdca_log{log_time}.tar.gz')


if __name__ == '__main__':
    # CDCA_ADB.upload_adb_to_bgm()
    CDCA_ADB().get_log()
