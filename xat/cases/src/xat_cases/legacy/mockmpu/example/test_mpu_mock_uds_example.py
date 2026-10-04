#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_mpu_mock_uds_example.py
@time         : 2023/11/23 14:19
@author       : quan.sun@jiduauto.com
@description  : 
'''


import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.mockmpu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *
import time


@allure.feature("Demon")
@allure.story("MockMpu")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        super().before_class(self, ecu)
        self.sd_tester.update_serverdoipid(0x1002, ecu="MCU")
        self.mockmpu.start_heart_beat()
        time.sleep(5)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        super().after_class(self, ecu)
        logger.info("after_class")

    @allure.title("测试test_mock_mpu_uds")
    def test_mock_mpu_uds_0001(self):
        self.diag_mock.update_0x22_data(ecu_name="ACU", did="F1AE", data_info_update=[0xFF, 0xFF, 0x00, 0xFF])
        self.sd_tester.send_data([0x22, 0xF1, 0xAE])
        sleep(5)
