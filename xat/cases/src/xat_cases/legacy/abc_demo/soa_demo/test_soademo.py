# -*- coding: utf-8 -*-
"""
@File        : test_soademo.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2023/10/31 18:00 PM
@Description :  SOA Test Demo
"""

import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.soa_partner.src.partner_const import *


@allure.feature("SOA Demo")
@allure.story("demon")
class TestDoorService(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        self.soa.update(["VehicleModeService_server"])

    def before_each_func(self, ecu):
        logger.info("before_each_func")

    def after_each_func(self, ecu):
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")

    @pytest.mark.soa_demo
    def test_soa_caseid_11111(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        sleep(5)