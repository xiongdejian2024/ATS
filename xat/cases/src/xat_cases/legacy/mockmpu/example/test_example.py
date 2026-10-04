#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     : test_basetechdemo.py
@time         : 2024/05/14 14:19
@author       : quan.sun@jiduauto.com
@description  : 
"""

from xat_cases.legacy.mockmpu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *
import time


@allure.feature("Demon")
@allure.story("MockMpu")
class TestExampleMockMpu(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        super().before_class(self, ecu)
        self.mockmpu.start_heart_beat()
        time.sleep(5)

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)

    def test_caseid_0001(self):
        self.mockmpu.send_all_cycle_pdu()
        time.sleep(10)
        self.mockmpu.change_signal("DoorPassOpenHmiReqDoorOpenerReq1", 3, 1)
        time.sleep(10)
        self.mockmpu.change_signal("DoorPassOpenHmiReqChks", 6, 0)
        time.sleep(10)
        pass
