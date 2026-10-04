#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :cdcq_ssh.py
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


class CDCQ_SSH(metaclass=SingletonMeta):
    device_name = "CDCQ"

    @classmethod
    def type_commands(cls, commands, timeout=60, **kwargs):
        status, outmsg = command_send(device_name=cls.device_name, cmd=commands, timeout=timeout, **kwargs)
        logger.info(f'{commands}执行结果为:{outmsg}')
        return outmsg

    @classmethod
    def get_ts_security(cls):
        cmd = "cd /persist/data;openssl x509 -in cdc.pem -noout -text | grep VID | awk -F 'VID:|;' '{print $2}'"
        status, ret = command_send(device_name=cls.device_name, cmd=cmd)
        logger.info(ret)
        return ret

    @classmethod
    def get_log(cls, my_local='/root'):
        log_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
        cmd = 'cd /data/log;rm -f cdcq_log.tar.gz;tar -zcvf cdcq_log.tar.gz ./*;chmod 777 cdcq_log.tar.gz'
        cls.type_commands(commands=cmd, timeout=600)
        file_download(device_name=cls.device_name, remote_path='/data/log/cdcq_log.tar.gz',
                      local_path=f'{my_local}/cdcq_log{log_time}.tar.gz')

    @classmethod
    def clear_log(cls):
        cls.type_commands(commands='rm -rf /data/log/*')


if __name__ == '__main__':
    CDCQ_SSH.get_log()
