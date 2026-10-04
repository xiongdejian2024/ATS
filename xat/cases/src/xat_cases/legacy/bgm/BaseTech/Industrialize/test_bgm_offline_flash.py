# -*- coding: utf-8 -*-
"""
@File        : test_bgm_offline_flash.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2024/1/30 9:45
@Description :

"""
import os
import random
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


@allure.feature("BGM BaseTech/工业化")
@allure.story("离线刷写")
class TestBgmOffLineFlash(TestABCBase):
    def before_class(self, ecu):
        self.iface = self.tc_config['bus']['eth_obd']  # 'enp114s0'

        # 连接诊断激活线

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    @pytest.mark.sanity
    @pytest.mark.full
    def test_read_mpu_info_caseid_1985046(self):
        '''
        - step1:给MPU(1001)发送 10 01 ----> 回复正响应：50 01 xx xx yy yy
        - step2: 给MPU(1001)发送 22 F1AE ---> 回复正响应：62 F1 AE xx xx ... xx
        - step3: 给MPU(1001)发送 22 F1AA ---> 回复正响应：62 F1 AA xx xx ... xx
        - step4: 给MPU(1001)发送 22 F18C ---> 回复正响应：62 F1 8C xx xx ... xx
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
        self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0XAE], recv=[0x62, 0xF1, 0XAE])
        self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0XAA], recv=[0x62, 0xF1, 0XAA])
        self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0X8C], recv=[0x62, 0xF1, 0X8C])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_mpu_info_inspection_caseid_1985047(self):
        '''
        - 检查前提条件：10 03 ---> 回复正响应：50 03 xx xx yy yy
        - 0E 80 ---> 1001 发送 27 05 ---> 回复：67 05 S1 S2 S3
        - 检查防火墙状态：22 B1 65 ---> 回复正响应：62 B1 65 02

        需要是新板子，
        - 检车证书状态：22 B1 63 ---> 回复正响应：62 B1 63 xx xx ... xx(16 bytes 全0x00 or 全 0xFF)
        - 检查public key写入状态：22 D0 3A ---> 回复负响应：NRC22
        - 检查FOTA Status状态：22 F1 54 ---> 回复正响应：62 F1 54 xx xx ... xx(124byts 00)
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x22, 0xB1, 0X65], recv=[0x62, 0xB1, 0X65])
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xB1, 0X63],
                                                                                 recv=[0x62, 0xB1, 0X63])
        # # 新板子
        # self.sd_tester.send_request_and_recv_response([0x22, 0xD0, 0X3A], recv=[0x7F, 0x22])
        # 旧板子
        self.sd_tester.send_request_and_recv_response([0x22, 0xD0, 0X3A], recv=[0x62, 0xD0, 0X3A])
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0X54],
                                                                                 recv=[0x62, 0xF1, 0X54])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_mcu_info_inspection_caseid_1985048(self):
        '''
        - 检查前提条件：10 03 ---> 回复正响应：50 03 xx xx yy yy
        - 检查VIN状态：22 F1 90 ---> 回复正响应：62 F1 90 xx xx ... xx(17bytes全0x00)
        - 检查CCP状态：22 F1 06 ---> 回复正响应：62 F1 06 xx xx ... xx(1558bytes 全FF)
        - 检查Usagemode状态：22 DD 0A ---> 回复正响应：62 DD 0A xx(xx != (0xB || 0xD))
        - 检查BGM-BNCM key状态：22 D9 04 ---> 回复正响应：62 D9 04 00
        - 检查L11常数状态：27 11 ---> 回复 67 11 S1 S2 S3   27 12 K1 K2 K3 ---> 回复 67 12
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x90],
                                                                                 recv=[0x62, 0xf1, 0x90])
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xF1, 0x06],
                                                                                 recv=[0x62, 0xF1, 0x06])
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xDD, 0x0A],
                                                                                 recv=[0x62, 0xDD, 0x0A])
        # # 新板子
        # self.sd_tester.send_request_and_recv_response([0x22, 0xD9, 0X04], recv=[0x62, 0xD9, 0X04, 0x00])
        # 旧板子
        self.sd_tester.send_request_and_recv_response([0x22, 0xD9, 0X04], recv=[0x62, 0xD9, 0X04, 0x00])
        self.sd_tester.security_access_level(UnLock.L11)

    @pytest.mark.sanity
    @pytest.mark.full
    def test_write_ccp_caseid_1985049(self):
        '''

        @return:
        '''

        ccp_data = 'A3 01 80 06 FD 03 02 01 A3 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 02 04 8C 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 04 01 02 02 85 89 02 02 01 02 09 02 7B 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 01 00 81 80 11 80 03 04 01 01 01 01 02 01 03 01 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 81 01 02 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 02 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 02 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 82 01 02 02 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 02 02 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 04 01 02 01 01 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 02 02 01 01 03 01 04 01 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 02 01 02 01 01 01 02 01 01 02 01 01 01 01 01 01 01 01 01 01 02 02 01 01 02 01 01 01 01 00 00 01 04 00 00 00 02 01 00 02 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 02 05 08 08 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 02 01 01 01 01 01 01 02 02 01 02 02 01 01 02 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 01 01 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01'
        ret = self.sd_tester.write_ccp_and_check(ccp_data)


    @pytest.mark.sanity
    @pytest.mark.full
    def test_write_intelligent_power_replenishment_caseid_1985050(self):
        '''
        写入智能补电阀值
        - 0E 80 ---> 1002 发送 10 03 ---> 回复：50 03 xx xx yy yy
        - 0E 80 ---> 1002 发送 27 05 ---> 回复：67 05 S1 S2 S3
        - 0E 80 ---> 1002 发送 2E 45 34 76 ---> 回复：6E 45 34
        - 0E 80 ---> 1002 发送 22 45 34 ---> 回复：62 45 34 76
        @return:
        '''
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.sd_tester.security_access_level(UnLock.L5)
        self.sd_tester.send_request_and_recv_response([0x2E, 0x45, 0X34, 0X76], recv=[0x6E, 0x45, 0X34])
        time.sleep(1)
        self.sd_tester.send_request_and_recv_response([0x22, 0x45, 0X34], recv=[0x62, 0x45, 0X34, 0X76])

    @pytest.mark.sanity
    @pytest.mark.full
    def test_change_car_mode_to_factory_caseid_1985051(self):
        '''
        切换Carmode进入Factory
        @return:
        '''

        self.sd_tester.change_car_mode(CarMode.FACTORY)
        # 恢复
        self.sd_tester.change_car_mode(CarMode.NORMAL)
