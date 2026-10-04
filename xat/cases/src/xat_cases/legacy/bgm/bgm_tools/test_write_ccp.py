# -*- coding: utf-8 -*-
"""
@File        : test_can_lin_fr_signal_route.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/11/22 11:36
@Description :

"""
import copy
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
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("MCU 基础平台/诊断路由")
@allure.story("功能用例")
class TestDiagRouteApp(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)


    def before_each_func(self, ecu):
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x06])

    def after_each_func(self, ecu):
        time.sleep(3)
        super().after_each_func(self, )
        logger.info("after_each_func")

    def after_class(self, ecu):
        super().after_class(self, ecu)
        logger.info("after_class")

    def test_write_mars_400_ccp(self):
        '''
        目前所有版本都支持 mars_400的，直接写入
        @return:
        '''
        self.mix.write_vehicle_model_ccp(vehicle_model = VehicleType.Mars, vehicle_mca = VehicleMca.Mca_400v)

    def test_write_mars_800_ccp(self):
        '''
        在 2.0 以后才有 800
        @return:
        '''
        self.mix.write_vehicle_model_ccp(vehicle_model = VehicleType.Mars, vehicle_mca = VehicleMca.Mca_800v)

    def test_write_venus_400_ccp(self):
        '''
       目前所有版本都支持 mars_400的，直接写入
       @return:
       '''
        self.mix.write_vehicle_model_ccp(vehicle_model=VehicleType.Venus, vehicle_mca=VehicleMca.Mca_400v)

    def test_write_venus_800_ccp(self):
        '''
        在 2.0 以后才有 800
        @return:
        '''
        self.mix.write_vehicle_model_ccp(vehicle_model = VehicleType.Venus, vehicle_mca = VehicleMca.Mca_800v)


# pytest bgm_tools/00ltg/test_write_ccp.py
