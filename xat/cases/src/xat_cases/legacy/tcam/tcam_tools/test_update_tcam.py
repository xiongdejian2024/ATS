# -*- coding: utf-8 -*-
"""
@File        : test_update_tcam.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/5/31 14:03
@Description : 升级 tcam

"""

import sys, os

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)

import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
import threading


class Test_Flash_TCAM(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # Code Location
        self.sdb_version = ecu.get('sdb_version')
        self.domain = ecu.domain
        if not self.sdb_version:
            raise Exception('缺少--sdb_version=版本号，无法升级')
        self.release_version = ecu.get('release_version')
        if not self.release_version:
            raise Exception('缺少--release_version=版本号，无法升级')
        if self.domain.single_tcam:
            self.tcam_ssh = TCAM_SSH(connect_type='vlan')
        elif self.domain.single_bgm:
            raise Exception("单域BGM无法升级TCAM")
        elif self.domain.two_domain:
            self.tc_config['sd_tester_cfg']['ecu_name'] = "TCAM"
            self.tc_config['gateway_ip'] = "169.254.19.1"
            self.tc_config['server_doip_id'] = 0x1001
            self.tc_config['server_ip'] = ""
            self.tcam_ssh = TCAM_SSH(connect_type='obd')
        elif self.domain.four_domain:
            self.tc_config['sd_tester_cfg']['ecu_name'] = "TCAM"
            self.tc_config['gateway_ip'] = "169.254.19.1"
            self.tc_config['server_doip_id'] = 0x1001
            self.tc_config['server_ip'] = ""
            self.tcam_ssh = TCAM_SSH(connect_type='obd')
        self.tcam_ssh.clear_coredump(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location
        # 开启tcpdump 抓包
        t = threading.Thread(target=self.tcp_dump)
        t.setDaemon(True)
        t.start()
        time.sleep(2)

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)
        # 停止抓包
        time.sleep(10)
        cmd = "ps -ef | grep tcpdump| awk '{print $2}' | xargs kill -9"
        os.system(cmd)

    def after_class(self, ecu):
        # Code Location
        super().after_class(self, ecu)

    def tcp_dump(self):
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        bord = self.tc_config.get("bus", {}).get("eth_obd", "any")
        logger.info(f"bord={bord}")
        path = os.path.dirname(__file__)
        logger.info(f"tcpdump 抓包保存路径为={path}")
        cmd = f"sudo tcpdump -i {bord}  -w {path}/update_tcam{otherStyleTime}.cap"
        os.system(cmd)

    def flash_func(self, keyinfo, file_url, standard=True, check_data=None):
        '''
        升级
        @param keyinfo:
        @param file_url:
        @param standard:
        @param check_data:
        @return:
        '''
        self.tcam_ssh.type_commands('reboot -f')
        sleep(300)
        self.sd_test = Sd_Tester(**self.tc_config)
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.5)
        # 进行升级
        if self.domain.single_tcam:
            self.sd_test.upgrade_ecu_tcam(keyinfo, file_url, standard=standard, check_data=check_data)
        else:
            self.sd_test.upgrade_ecu(keyinfo, file_url, standard=standard, check_data=check_data)

        self.sd_test.stop_tester_present()
        sleep(0.5)
        self.sd_test.diagnostic_client_sim_close()
        sleep(5)

    def test_flash_tcam_caseid_0000(self):
        with allure.step('設置车速为0'):
            try:
                self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
                self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
                # 设置车速为 0
                self.ipdu.set_vehspd(0)
                time.sleep(5)
                self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
                self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
            except Exception as e:
                logger.warning(f"修改车速失败：{str(e)}")
        """
        pytest bgm_tools/test_update_bgm.py --sdb_version=1.3.0 --release_version=AU
        release_version参数直接指定版本 例如AU
        """
        logger.info(f"升级 tcam app ")
        self.flash_func(self.sdb_version, self.release_version)


# class falsh_tcam():
#     def flash_func(self, keyinfo, file_url, standard=True, check_data=None):
#         '''
#         升级
#         @param keyinfo:
#         @param file_url:
#         @param standard:
#         @param check_data:
#         @return:
#         '''
#         cfg = {'dut_ecu': ['TCAM'], 'com_mock_ecu': [], 'gateway_ip': '169.254.19.1', 'bus': {'eth_obd': 'enx000ec658349a', 'eth_vlan5': 'eth0.5', 'eth_vlan9': 'eth0.9', 'connectivitycanfd': 'can0'}, 'veh_type': 'mars1', 'veh_gen': '', 'bl_ver': 'v_2_0_0', 'ecu_mock_cfg': {'ecu_name': 'ALL', 'p_n_res': True, 'nrc_code': 34, 'diag_mode': 'doip', 'server_doip_id': 5121, 'server_ip': '172.16.9.222'}, 'sd_tester_cfg': {'diag_mode': 'doip', 'is_via_gateway': False, 'ecu_name': 'TCAM', 'dig_bus': 'connectivitycanfd', 'server_ip': '172.16.9.31'}, 'eth_vlan': 'enp89s0', 'eth_obd': '172.16.9.222', 'wifi_localhost': '172.23.21.11', 'domain': ['TCAM'], 'usbrelay': {'TCAM_P': '/dev/hidraw0_2', 'TCAM_KL15': '/dev/hidraw0_5'}, 'adbdevice': {'tcam': 'a3e41149'}, 'vid': 'f3f6c5dfe8a70077d60d8ef2bc974703', 'vin': 'LSTEST6R9F2086668', 'tel': '15926230758', 'sec_con': {'TCAM': [1099511627775, 110464654498, 1054071901578, '9c121c16bca957c759701493b409853c', 1099511627775], 'BGM': [1099511627775, 110464654498, 110464654498, '9c121c16bca957c759701493b409853c', 1099511627775], 'CDC': [1099511627775, 110464654498, 110464654498, '9c121c16bca957c759701493b409853c', 1099511627775], 'ACU': [1099511627775, 110464654498, 110464654498, '9c121c16bca957c759701493b409853c', 1099511627775]}}
#         self.sd_test = Sd_Tester(**cfg)
#         sleep(0.5)
#         self.sd_test.diagnostic_client_sim_start()
#         sleep(0.5)
#         # 进行升级
#         self.sd_test.upgrade_ecu_tcam(keyinfo, file_url, standard=standard, check_data=check_data)
#         self.sd_test.stop_tester_present()
#         sleep(0.5)
#         self.sd_test.diagnostic_client_sim_close()
#         sleep(5)

#     def test_flash_tcam_caseid_0000(self):
#         with allure.step('設置车速为0'):
#             try:
#                 self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
#                 self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
#                 # 设置车速为 0
#                 self.ipdu.set_vehspd(0)
#                 time.sleep(5)
#                 self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
#                 self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
#             except Exception as e:
#                 logger.warning(f"修改车速失败：{str(e)}")
#         """
#         pytest bgm_tools/test_update_bgm.py --sdb_version=1.3.0 --release_version=AU
#         release_version参数直接指定版本 例如AU
#         """
#         logger.info(f"升级 tcam app ")
#         self.flash_func('2.0.0','AQ')

if __name__ == "__main__":
    s = falsh_tcam()
    s.test_flash_tcam_caseid_0000()
    # pytest.main()
    # pytest tcam_tools/test_update_tcam.py --sdb_version=1.3.0 --release_version=AU

