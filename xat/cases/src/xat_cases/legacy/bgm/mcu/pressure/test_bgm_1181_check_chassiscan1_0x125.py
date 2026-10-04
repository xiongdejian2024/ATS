# -*- coding: utf-8 -*-
"""
@File        : 111
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/12/23 14:07
@Description : 屏幕换挡问题复现方法沟通

https://jiduauto.feishu.cn/docx/LIiEdRM6BoxR4axSKwDcQqX8nUh

"""

import time
import pytest
import allure
import sys, os
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download, file_upload
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

import pytest
import allure
from xat_ecu.legacy.common.logger import logger

from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH

from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.sdk_tools import *

test_count = 0


# https://jiduauto.feishu.cn/wiki/MDwbwIuEail9jSkM2XKcIHvZnvf

@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Chassiscan1(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        path = os.path.dirname(__file__)
        self.save_path = os.path.join(path, f'BGM_{otherStyleTime}_log')
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.sd_test_tb_config = tb_config.yaml_content
        self.sd_test = Sd_Tester(**self.sd_test_tb_config)
        # self.sd_test.update_serverdoipid(0x1002)
        self.sd_test.diagnostic_client_sim_start()
        self.sd_test.tester_present()
        self.bgm_ssh = BGM_SSH()
        with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        self.ipdu.pause_bus_send('chassiscan1')
        self.ipdu.rx_flag_reset_bus('chassiscan1')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)
        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()
        except Exception as e:
            logger.info(f"str(e)=={str(e)}")

    @pytest.mark.repeat(200)
    @pytest.mark.bgm_1181_check_chassiscan1_0x125
    def test_flow(self):
        global test_count
        test_count += 1
        iface_name = self.tc_config['bus']['eth_obd']
        self.sff = SniffPacket(iface=iface_name)
        self.sff.start_sniff()
        try:
            # 诊断重启后，ping tcam 和 上位机
            with allure.step(f"诊断重启 bgm ping tcam"):
                logger.info(f"诊断重启 bgm ping tcam")
                self.sd_test.stop_tester_present()
                self.sd_test.reset_ecu_functional_addressing()
                time.sleep(12)
                self.sd_test.tester_present()

            with allure.step(f"重启后 在chassiscan1接收 接收报文"):
                logger.info(f"重启后 在chassiscan1接收 接收报文")
                t = time.time()
                while time.time() - t < 10:
                    msg = self.ipdu.recv_pdu('chassiscan1', 0x125,timeout=2)
                    with allure.step(f"在chassis can1接收的应用报文{msg}"):
                        logger.info(f"msg={msg}")
                    time.sleep(1)

            with allure.step(f"在chassis can1发送 0x521报文"):
                logger.info(f"在chassis can1发送 0x521报文")
                self.ipdu.send_pdu('chassiscan1', 0x521, [0x21, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                   cycle_time=1)
                t = time.time()
                while time.time() - t < 10:
                    msg = self.ipdu.recv_pdu('chassiscan1', 0x125,timeout=2)
                    if msg is None:
                        with allure.step(f"在chassis can1接收的应用报文None"):
                            logger.info(f"msg={msg}")
                    else:
                        msg_id=hex(msg[0])
                        msg_msg = bytes(msg[3]).hex()
                        with allure.step(f"在chassis can1接收的应用报文id={msg_id} msg={msg_msg}"):
                            logger.info(f"msg={msg}")
                        break
                else:
                    self.sff.stop_sniff()
                    # 失败了取日志
                    try:
                        logger.info(f"拉取bgm 日志")
                        self.get_bgm_log()
                        with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
                            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
                            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
                    except Exception as e:
                        logger.error(f"拉取bgm 日志失败》》{str(e)}")
                    while 1:
                        logger.error("bgm重启后，在chassis can1发送 0x521报文 未唤醒")
                        time.sleep(10)
            time.sleep(2)
            self.ipdu.pause_bus_send('chassiscan1')
            time.sleep(3)
            self.ipdu.rx_flag_reset_bus('chassiscan1')

            time.sleep(3)
            self.sff.stop_sniff()
        except Exception as e:
            logger.error(f"失败>>>{str(e)}")
            time.sleep(5)
            self.sff.stop_sniff()
            assert 0, str(e)

    def get_bgm_log(self):
        bgm_ssh = BGM_SSH()
        timeout = 600
        log_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
        cmd = 'cd /log;tar -cvf /update/bgm_log.tar.gz ./*'
        bgm_ssh.type_commands(commands=cmd, timeout=timeout)
        file_download(device_name='BGM', remote_path='/update/bgm_log.tar.gz',
                      local_path=f'{self.save_path}/bgm_log_{log_time}.tar.gz',connect_type='obd')
        logger.info(f"bgm_log_{log_time}.tar.gz已经全部取到 {self.save_path} 路径下啦0")

if __name__ == "__main__":
    pytest.main()
    # pytest 00ltg/test_bgm_1181_check_chassiscan1_0x125.py
