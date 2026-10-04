# -*- coding: utf-8 -*-
"""
@File        : 离线刷写台
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/11/27 13:11
@Description :

"""
import threading
import time
import pytest
import allure
import sys, os
import json

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'soa_lib', 'interface')
sys.path.append(work_path_2)

from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase

import os
import sys
import time
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.bgm.mcu.case_helper.test_base import TestBase
import pytest
import allure
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.driver.ssh_interface import command_send, file_download, file_upload

sniff_count = 0


@allure.feature("架构基础/网络架构")
@allure.story("诊断/诊断刷写")
class Test_Flash_BGM(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        path = os.path.dirname(__file__)
        self.save_path = os.path.join(path, f'BGM_{otherStyleTime}_pcap_file')
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
        self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        # 设置车速为 0
        self.ipdu.set_vehspd(0)
        time.sleep(5)

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

        self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
        self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文

    def tcp_dump(self):
        global sniff_count
        sniff_count += 1
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
        bord = self.tc_config.get("bus", {}).get("eth_obd", "any")
        logger.info(f"bord={bord}")
        # path = os.path.dirname(__file__)

        # save_path = os.path.join(path, 'pcap_file')
        # if not os.path.exists(save_path):
        #     os.mkdir(save_path)

        file_path = f"{self.save_path}/{sniff_count}_update_bgm_{otherStyleTime}.pcap"
        logger.info(f"第{sniff_count} tcpdump 抓包保存路径为={file_path}")
        cmd = f"sudo tcpdump -i {bord}  -w {file_path}"
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
        self.tc_config["sd_tester_cfg"]["ecu_name"] = "BGM"
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.diagnostic_client_sim_start()
        sleep(0.5)
        # 进行升级
        self.sd_test.upgrade_ecu(keyinfo, file_url, standard=standard, check_data=check_data)

        self.sd_test.stop_tester_present()
        self.sd_test.diagnostic_client_sim_close()

    def update_bgm_offline(self, bin_dic, new_bgm=False):
        with allure.step(f"****************BGM 离线刷写开始***当前版子为{'新板子' if new_bgm else '旧板子'}**************"):
            logger.info("离线刷写开始")
        self.tc_config["sd_tester_cfg"]["ecu_name"] = "BGM"
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.diagnostic_client_sim_start()
        self.sd_test.tester_present()

        with allure.step('ECU信息读取'):
            self.sd_test.update_serverdoipid(0x1001)
            with allure.step('- step1:给MPU(1001)发送 10 01 ----> 回复正响应：50 01 xx xx yy yy '):
                self.sd_test.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

            with allure.step('- step2: 给MPU(1001)发送 22 F1AE ---> 回复正响应：62 F1 AE xx xx ... xx'):
                self.sd_test.send_request_and_recv_response(
                    [0x22, 0xF1, 0XAE],
                    recv=[0x62, 0xF1,
                          0XAE])

            with allure.step('- step3: 给MPU(1001)发送 22 F1AA ---> 回复正响应：62 F1 AA xx xx ... xx'):
                err_code, send_22f1aa_recv_data_before_update = self.sd_test.send_request_and_recv_response(
                    [0x22, 0xF1, 0XAA],
                    recv=[0x62, 0xF1, 0XAA])

            with allure.step('- step4: 给MPU(1001)发送 22 F18C ---> 回复正响应：62 F1 8C xx xx ... xx'):
                err_code, send_22f18c_recv_data_before_update = self.sd_test.send_request_and_recv_response(
                    [0x22, 0xF1, 0X8C],
                    recv=[0x62, 0xF1, 0X8C])

        with allure.step('来料检查'):
            with allure.step('- MPU(0x1001) 信息检查'):
                self.sd_test.update_serverdoipid(0x1001)
                with allure.step('- 检查前提条件：10 03 ---> 回复正响应：50 03 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])

                with allure.step('- 0E 80 ---> 1002 发送 27 05 ---> 回复：67 05 S1 S2 S3'):
                    self.sd_test.security_access_level_l3()

                with allure.step('- 检查防火墙状态：22 B1 65 ---> 回复正响应：62 B1 65 02'):
                    self.sd_test.send_request_and_recv_response([0x22, 0xB1, 0X65], recv=[0x62, 0xB1, 0X65, 0X02])

                with allure.step(
                        '- 检车证书状态：22 B1 63 ---> 回复正响应：62 B1 63 xx xx ... xx(16 bytes 全0x00 or 全 0xFF)'):
                    err_code, recv_data_list = self.sd_test.send_request_and_recv_response([0x22, 0xB1, 0X63],
                                                                                           recv=[0x62, 0xB1, 0X63])
                    check_data_list = [
                        [0x00] * 16,
                        [0xFF] * 16,
                    ]
                    rcv_data = recv_data_list[3:]
                    if new_bgm:
                        if rcv_data not in check_data_list:
                            assert 0, f"发送22 B1 63 获取的值应该为全0 或者全ff 实际为{rcv_data}"

                with allure.step('- 检查public key写入状态：22 D0 3A ---> 回复负响应：NRC22'):
                    # self.sd_test.send_data([0x22, 0xD0, 0X3A])
                    # recv_data_list = self.sd_test.return_udsdata_and_check_and_print_response_result(
                    #     f" 发送{bytes([0x22, 0xD0, 0X3A]).hex()}")
                    self.sd_test.send_request_and_recv_response([0x22, 0xD0, 0X3A], recv=[0x7F, 0x22])

                with allure.step('- 检查FOTA Status状态：22 F1 54 ---> 回复正响应：62 F1 54 xx xx ... xx(124byts 00)'):
                    err_code, recv_data_list = self.sd_test.send_request_and_recv_response([0x22, 0xF1, 0X54],
                                                                                           recv=[0x62, 0xF1, 0X54])
                    check_data_list = [
                        [0x00] * 124,
                        # [0xFF] * 16,
                    ]
                    rcv_data = recv_data_list[3:127]

                    if new_bgm and rcv_data not in check_data_list:
                        assert 0, f"发送22 B1 63 获取的值应该为全0  实际为{rcv_data}"

            with allure.step('- MCU(0x1002)信息检查'):
                self.sd_test.update_serverdoipid(0x1002)
                with allure.step('- 检查前提条件：10 03 ---> 回复正响应：50 03 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])

                with allure.step('- 检查VIN状态：22 F1 90 ---> 回复正响应：62 F1 90 xx xx ... xx(17bytes全0x00)'):
                    err_code, recv_data_list = self.sd_test.send_request_and_recv_response([0x22, 0xf1, 0x90],
                                                                                           recv=[0x62, 0xf1, 0x90])
                    check_data_list = [
                        [0x00] * 17,
                    ]
                    rcv_data = recv_data_list[3:20]
                    if new_bgm and rcv_data not in check_data_list:
                        assert 0, f"发送22 F1 90 获取的值应该为全0 实际为{rcv_data}"

                with allure.step('- 检查CCP状态：22 F1 06 ---> 回复正响应：62 F1 06 xx xx ... xx(1558bytes 全FF)'):
                    err_code, recv_data_list = self.sd_test.send_request_and_recv_response([0x22, 0xF1, 0x06],
                                                                                           recv=[0x62, 0xF1, 0x06])
                    check_data_list = [
                        [0xFF] * 1558,
                    ]
                    rcv_data = recv_data_list[3:1558 + 3]
                    if new_bgm and rcv_data not in check_data_list:
                        assert 0, f"发送22 F1 06 获取的值应该为全FF 实际为{rcv_data}"

                with allure.step('- 检查Usagemode状态：22 DD 0A ---> 回复正响应：62 DD 0A xx(xx != (0xB || 0xD))'):
                    err_code, recv_data_list = self.sd_test.send_request_and_recv_response([0x22, 0xDD, 0x0A],
                                                                                           recv=[0x62, 0xDD, 0x0A])
                    check_data_list = [
                        [0x0B],
                        [0x0D],
                    ]
                    rcv_data = recv_data_list[3:4]
                    if rcv_data in check_data_list:
                        assert 0, f"发送22 DD 0A 回复正响应：62 DD 0A xx(xx != (0xB || 0xD)) 实际为{rcv_data}"

                with allure.step('- 检查BGM-BNCM key状态：22 D9 04 ---> 回复正响应：62 D9 04 00'):
                    self.sd_test.send_request_and_recv_response([0x22, 0xD9, 0X04], recv=[0x62, 0xD9, 0X04, 0x00])

                with allure.step(
                        '    - 检查L11常数状态：27 11 ---> 回复 67 11 S1 S2 S3   27 12 K1 K2 K3 ---> 回复 67 12'):
                    self.sd_test.security_access_level_l6()

        # return
        with allure.step('刷写过程中'):
            self.sd_test.update_serverdoipid(0x1001)
            # 刷写boot
            update_boot_ver = None
            boot_url = bin_dic.get('boot_url')
            boot_key_info = bin_dic.get('boot_key_info')
            if boot_url:
                with allure.step('刷写boot'):
                    update_boot_ver = boot_url[-16:-4]
            with allure.step(f'刷写 boot 版本号为》》{update_boot_ver}'):
                self.sd_test.upgrade_ecu(boot_key_info, boot_url)

            app_url = bin_dic.get('app_url')
            app_key_info = bin_dic.get('app_key_info')
            update_app_ver = None
            if app_url:
                with allure.step('刷写 app'):
                    update_app_ver = app_url[-16:-4]  # self.sd_test.get_version_by_url(app_url)
            with allure.step(f'刷写 app 版本号为》》{update_app_ver}'):
                self.sd_test.upgrade_ecu(app_key_info, app_url, )

        # 开启 3E80
        self.sd_test.tester_present()

        with allure.step('刷写后'):

            with allure.step('- Step1:检查F1 AE/F1 AA/F18C 信息'):
                self.sd_test.update_serverdoipid(0x1001)
                time.sleep(1)
                with allure.step('- 0E 80 ---> 1001 发送 10 01 ---> 回复：50 01 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])

                with allure.step(
                        '- 0E 80 ---> 1001 发送 22 F1 AE ---> 回复：62 F1 AE xx xx ... xx（软件版本需要版本与刷写的版本一致）'):
                    mcu_ver, boot_ver = self.sd_test.get_soft_version()
                    if update_boot_ver and str(update_boot_ver).upper() != str(boot_ver).upper().replace(" ", ''):
                        assert 0, f"升级的boot 版本为{update_boot_ver} 实际读出来的版本为{boot_ver}"

                    if update_app_ver and str(update_app_ver).upper() != str(mcu_ver).upper().replace(" ", ''):
                        assert 0, f"升级的 app 版本为{update_app_ver} 实际读出来的版本为{boot_ver}"

                with allure.step(
                        '    - 0E 80 ---> 1001 发送 22 F1 AA ---> 回复：62 F1 AA xx xx ... xx (需要与刷写前保持一致)'):
                    err_code, send_22f1aa_recv_data_after_update = self.sd_test.send_request_and_recv_response(
                        [0x22, 0xF1, 0XAA], recv=[0x62, 0xF1, 0XAA])
                    if send_22f1aa_recv_data_after_update != send_22f1aa_recv_data_before_update:
                        assert 0, "刷写前后22 F1 AA 读取的值不同 "

                with allure.step(
                        '- 0E 80 ---> 1001 发送 22 F1 8C ---> 回复：62 F1 8C xx xx ... xx (需要与刷写前保持一致) '):
                    err_code, send_22f18c_recv_data_after_update = self.sd_test.send_request_and_recv_response(
                        [0x22, 0xF1, 0X8C], recv=[0x62, 0xF1, 0X8C])
                    if send_22f18c_recv_data_after_update != send_22f18c_recv_data_before_update:
                        assert 0, "刷写前后22 F1 8c 读取的值不同 "

            with allure.step('- Step2:写入预置CCP'):
                self.sd_test.update_serverdoipid(0x1002)
                with allure.step('- 0E 80 ---> 1002 发送 10 03 ---> 回复：50 03 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
                with allure.step('- 0E 80 ---> 1002 发送 27 05 ---> 回复：67 05 S1 S2 S3'):
                    self.sd_test.security_access_level_l3()
                if not new_bgm:
                    pass
                    ccp_data='A3 01 80 06 FD 03 02 01 A3 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 02 04 8C 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 04 01 02 02 85 89 02 02 01 02 09 02 7B 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 01 00 81 80 11 80 03 04 01 01 01 01 02 01 03 01 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 81 01 02 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 02 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 02 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 82 01 02 02 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 02 02 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 04 01 02 01 01 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 02 02 01 01 03 01 04 01 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 02 01 02 01 01 01 02 01 01 02 01 01 01 01 01 01 01 01 01 01 02 02 01 01 02 01 01 01 01 00 00 01 04 00 00 00 02 01 00 02 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 02 05 08 08 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 02 01 01 01 01 01 01 02 02 01 02 02 01 01 02 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 01 01 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01 60 33'
                    ccp_data=ccp_data.replace(' ','')
                    write_ccp_data =[int(ccp_data[i:i + 2], 16) for i in range(0, len(ccp_data), 2)]
                    with allure.step('- 0E 80 ---> 1002 发送 2E F1 06 xx xx ... xx ---> 回复：2E F1 06'):

                        self.sd_test.write_ccp(write_ccp_data)


                    with allure.step('- 0E 80 ---> 1002 发送 22 F1 06 ---> 62 F1 06 xx xx ... xx(xx非default ccp值)'):
                        err_code, recv_data_list = self.sd_test.send_request_and_recv_response([0x22, 0xF1, 0x06],
                                                                                               recv=[0x62, 0xF1, 0x06])
                        rcv_data = recv_data_list[3:1558+3]
                        if rcv_data != write_ccp_data:
                            assert 0, f"发送写入的ccp 和读取的ccp不一致  实际为{rcv_data}"

            with allure.step('- Step3:写入智能补电阀值'):
                self.sd_test.update_serverdoipid(0x1002)
                with allure.step('- 0E 80 ---> 1001 发送 10 03 ---> 回复：50 03 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
                with allure.step('- 0E 80 ---> 1001 发送 27 05 ---> 回复：67 05 S1 S2 S3'):
                    self.sd_test.security_access_level_l3()

                with allure.step('- 0E 80 ---> 1001 发送 2E 45 34 76 ---> 回复：6E 45 34'):
                    self.sd_test.send_request_and_recv_response([0x2E, 0x45, 0X34, 0X76], recv=[0x6E, 0x45, 0X34])
                time.sleep(1)
                with allure.step('- 0E 80 ---> 1001 发送 22 45 34 ---> 回复：62 45 34 76'):
                    self.sd_test.send_request_and_recv_response([0x22, 0x45, 0X34], recv=[0x62, 0x45, 0X34, 0X76])

            with allure.step('- Step4:切换Carmode进入Factory'):
                self.sd_test.update_serverdoipid(0x1002)
                self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()

                with allure.step('- 0E 80 ---> 1002 发送 10 03 ---> 回复：50 03 xx xx yy yy'):
                    self.sd_test.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])

                with allure.step('- 0E 80 ---> 1002 发送 27 03 ---> 回复：67 03 S1 S2 S3'):
                    self.sd_test.security_access_level_l2()

                with allure.step('- 0E 80 ---> 1002 发送 2F D1 34 03 02 ---> 回复：6F D1 34 xx'):
                    self.sd_test.send_request_and_recv_response([0x2F, 0XD1, 0X34, 0X03, 0X02], recv=[0x6F, 0XD1, 0X34])
                    time.sleep(1)
                    self.sd_test.send_request_and_recv_response([0x22, 0XD1, 0X34], recv=[0x62, 0XD1, 0X34, 0X02])

        try:
            self.sd_test.stop_tester_present()
            self.sd_test.diagnostic_client_sim_close()

        except Exception as e:
            logger.error(f">>>>error>>>{str(e)}")
            pass
        with allure.step('**********************************离线刷写结束***********************************'):
            logger.info("离线刷写结束")

    @pytest.mark.repeat(1)
    @pytest.mark.update_bgm_offline
    def test_update_bgm_offline(self):

        bin_dic_list = [
            {
                # 版本 1
                'boot_url': "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.1.0/6160110110EA/2960110110AG.bin",
                'boot_key_info': __import__("os").environ['XAT_CREDENTIAL_SCAN_65DAA3DDEB33D38764E5'],
                'app_url': "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.1.0/6160110110EA/6160110110EA.bin",
                'app_key_info': __import__("os").environ.get('XAT_CREDENTIAL____BGM_MCU_PRESSURE_TEST_FLASH_BGM_PY_APP_KEY_INFO', ""),

            },
            {
                # 版本2
            
                'boot_url': "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.3.0/6160110130BN/2960110130AD.bin",
                'boot_key_info': __import__("os").environ['XAT_CREDENTIAL_SCAN_44A73F7DE1FF5B9B822E'],
                'app_url': "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.3.0/6160110130BN/6160110130BN.bin",
                'app_key_info': __import__("os").environ.get('XAT_CREDENTIAL____BGM_MCU_PRESSURE_TEST_FLASH_BGM_PY_APP_KEY_INFO', ""),
            
            },
            # {
            #     # 版本2
            #
            #     'boot_url': "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.4.0/6160110140AA/2960110130AD.bin",
            #     'boot_key_info': "${XAT_CREDENTIAL_SCAN_CCD9D9C1E77F7B787737}",
            #     'app_url': "https://repo.jidudev.com/artifactory/BGMSoftware/Release/v1.4.0/6160110140AA/6160110140AA.bin",
            #     'app_key_info': "${XAT_CREDENTIAL_SCAN_0E297E12E4AF19906B86}"
            # },
        ]

        for bin_dic in bin_dic_list:
            if not bin_dic:
                continue
            try:
                # todo 如果是新板子 new_bgm =True
                # todo 如果是旧板子 new_bgm =False
                self.update_bgm_offline(bin_dic, new_bgm=False)
            except Exception as e:
                logger.error(f"离线刷写失败》》{str(e)}")
                self.get_bgm_log()
                assert 0, str(e)

        # 只升级
        # 升级boot
        # keyinfo = bin_dic_list[0]['boot_key_info']
        # boot_url = bin_dic_list[0]['boot_url']
        # self.flash_func(keyinfo=keyinfo, file_url=boot_url)
        # # 升级app
        # app_key_info = bin_dic_list[0]['app_key_info']
        # app_url = bin_dic_list[0]['app_url']
        # self.flash_func(keyinfo=app_key_info, file_url=app_url)

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
    # pytest pressure/test_flash_bgm.py

    #  需求来源  https://jiduauto.feishu.cn/wiki/K29Gwx9OHio5fFkbxcqcOTvUnMK
