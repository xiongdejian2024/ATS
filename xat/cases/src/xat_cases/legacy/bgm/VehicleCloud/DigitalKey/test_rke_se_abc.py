#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_pile_open_charge_lid.py
@Time         :2023/1/31 17:54:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ""))
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
PRECHECKTI = 1

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/其他/SE")
class TestDigitalKeyWhiteListConTrol(TestDigitalKeyBase):

    # def before_class(self, ecu):
    #     """测试用例的前处理"""
    #     super().before_class(self, ecu)
    #     self.tsp = DigitalKeyManager(self.tc_config.get('vid'),
    #                                  self.tc_config.get('tel'),
    #                                  "jiduapp/0.9.3 (iOS; 16.0; apple; jdcomiphone; iPhone 12; NULL; BF983636-D3F2-4805-90B4-77C3DC75D433; aVBob25l)",
    #                                  uid = self.tc_config.get('uid'))
    
    # def after_class(self, ecu):
    #     super().after_class(self, ecu)
        

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        # self.dk.nucapp.bgm_diag_line_down()
        self.bus_comm.dk.set_digital_key_connect_info(connect_sts1=1, type1=2, keyid1=bytes([0x01] * 16),
                                             connect_sts2=1, type2=1, keyid2=bytes([0x22] * 16),
                                             connect_sts3=1, type3=3, keyid3=bytes([0x33] * 16),
                                             connect_sts4=1, type4=5, keyid4=bytes([0x44] * 16))
        self.bus_comm.dk.reset_bncm_digital_keyinfo()
        # self.set_usage_mode(0x1)
        # self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        sleep(20)
    
    @allure.title("SE_RESULT_SUCCESS_全部正响应")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/110580?projectId=46')
    @pytest.mark.smoke
    def test_caseid_110580(self):
        result = self.tsp_rke_se_sync('080102030405060708000024000D00A4040008A000000151000000029000000D80503000082FD4AC3C53DB7426029000')
        sleep(10)
        logger.info(f"-------------------->{result}")
        # todo: 查看云端日志err = 0，errMsg=''，CardID=000102030405060708090A0B0C0D0E0F


    # @allure.title("SE_RESULT_FAILED_2次指令与预期不符_Inactive")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/110572?projectId=46')
    # @pytest.mark.full
    # def test_caseid_110572(self):
    #     self.dk.set_chassis_service_gear("GearP")
    #     sleep(1)
    #     self.tsp.tsp_rke_se_sync('080102030405060708000024000D00A4040008A000000151000000029000000D80503000082FD4AC3C53DB7426029000')
    #     sleep(10)
    #     # todo: 查看云端日志err = 0，errMsg=''，CardID=000102030405060708090A0B0C0D0E0F
    
    