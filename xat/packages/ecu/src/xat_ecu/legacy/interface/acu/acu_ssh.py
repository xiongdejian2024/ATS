#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :acu_ssh.py
@Time         :2023/8/7 16:16
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import os
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.singleton import SingletonMeta
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download


class ACU_SSH(metaclass=SingletonMeta):
    device_name = "ACU"

    @classmethod
    def type_commands(cls, commands, output=False, root_permission=True, timeout=60, **kwargs):
        status, outmsg = command_send(device_name=cls.device_name, cmd=commands, timeout=timeout, **kwargs)
        logger.info(f'{commands}执行结果为:{outmsg}')
        return outmsg

    @classmethod
    def get_ts_security(cls):
        cmd = "cd /opt/profile/jiducerts;openssl x509 -in ecu_cert.pem -text | grep VID |awk -F 'VID:|;' '{print $2}'"
        status, ret = command_send(device_name=cls.device_name, cmd=cmd)
        logger.info(ret)
        return ret

    @classmethod
    def get_log(cls, my_local='/root'):
        log_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
        cmd = 'cd /data/log/;rm -rf *;cp -rf /opt/log /data/log/;tar -zcvf acu_log.tar.gz log/;' \
              'chmod 777 acu_log.tar.gz'
        cls.type_commands(commands=cmd, timeout=600)
        file_download(device_name=cls.device_name, remote_path='/data/log/acu_log.tar.gz',
                      local_path=f'{my_local}/acu_log{log_time}.tar.gz')


if __name__ == '__main__':
    ACU_SSH.get_log()
