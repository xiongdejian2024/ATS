#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : test_example.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/7/4 17:54
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import time

import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common.common import set_bench_vlan9_ip
from xat_ecu.legacy.protocol.ProtocolServerKeywords import ProtocolServerKeywords
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.driver.ssh_interface import file_upload, command_send


def check_mock_doip_server_config(commands='ls /data', time_out=60, remote_path="/tmp/"):
    status, outmsg = command_send(device_name="BGM", cmd="cat /sys/power/sys_resumed", connect_type="obd", timeout=time_out)
    logger.info(f'检查冷启动执行结果为:{outmsg}')
    if "1" in outmsg: # 1为热启动，需要改为冷启动，在重启BGM
        status, outmsg = command_send(device_name="BGM", cmd="/app/bin/swdl -nw 10 0", connect_type="obd",
                                      timeout=time_out)
        logger.info(f'执行冷启动执行结果为:{outmsg}')
        status, outmsg = command_send(device_name="BGM", cmd="reboot", connect_type="obd",
                                      timeout=time_out)
        logger.info(f'重启reboot:{outmsg}')
        time.sleep(30)

    status, outmsg = command_send(device_name="BGM", cmd="ls /data", connect_type="obd", timeout=time_out)
    logger.info(f'{commands}执行结果为:{outmsg}')
    dir_msg = [i.replace("\n", "").replace("\t", "") for i in str(outmsg).split(' ') if i]
    if "debug.sh" not in dir_msg:
        logger.info(f"没有发现debug.sh文件在/data/目录下")
        debug_path = os.path.join(os.getcwd(), 'debug.sh')
        file_upload(device_name="BGM", local_path=debug_path, remote_path=remote_path, connect_type="obd")

        status, outmsg = command_send(device_name="BGM", cmd=f"cp -r {remote_path}debug.sh /data/", connect_type="obd",
                                      timeout=time_out)
        logger.info(f"cp debug file to data out message:{outmsg}")

    if "sl" not in dir_msg:
        logger.info(f"没有发现sl在/data/目录下")
        sl_path = os.path.join(os.getcwd(), "../data/sl.tar.gz")
        file_upload(device_name="BGM", local_path=sl_path, remote_path=remote_path, connect_type="obd")
        status, outmsg = command_send(device_name="BGM", cmd=f"cp -r {remote_path}sl.tar.gz /data/", connect_type="obd",
                                      timeout=time_out)
        logger.info(f"cp sl file to data out message:{outmsg}")
        status, outmsg = command_send(device_name="BGM", cmd=f"tar -zxvf /data/sl.tar.gz", connect_type="obd",
                                      timeout=time_out)
        logger.info(f"tar sl file to data out message:{outmsg}")

    if "debug.sh" not in dir_msg or "sl" not in dir_msg:
        status, outmsg = command_send(device_name="BGM", cmd="reboot", connect_type="obd",
                                      timeout=time_out)
        logger.info(f'重启reboot:{outmsg}')
        time.sleep(30)
    

def delete_bgm_reboot_count_file(commands='rm /data/debug_script_executed_count', timeout=60):
    status, outmsg = command_send(device_name="BGM", cmd=commands, connect_type="obd", timeout=timeout)
    logger.info(f'{commands}执行结果为:{outmsg}')


@allure.feature("Demon")
@allure.story("example Demo")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        set_bench_vlan9_ip('172.16.9.21')

        self.server_mock = ProtocolServerKeywords('doip', '172.16.9.21', 13400)
        self.server_mock.init_middleware()

        super().before_class(self, ecu)
        logger.info("before_class")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        self.server_mock.doip_sock_obj.tcp_server_sock.stop()
        super().after_class(self, ecu)
        logger.info("after_class")

    @allure.title("测试当ACU作为服务端mock的诊断请求")
    def test_mock_doip_server_caseid_0001(self):
        self.server_mock.doip_update_service_data_0x8001({
            0x1011: {
                0x27: {
                    0x01: ['6701123456']
                },
                0x10: {
                    0x01: ['5001'],
                    0x03: ['5003']
                },
                0x11: {
                    0x01: ['5101'],
                    0x81: ['5181'],
                }
            }
        })

        self.sd_tester.update_serverdoipid(0x1011, ecu="TCAM")
        self.sd_tester.send_data([0x10, 0x03])
        self.sd_tester.send_data([0x27, 0x01])
        self.sd_tester.send_data([0x11, 0x01])
        time.sleep(15)

