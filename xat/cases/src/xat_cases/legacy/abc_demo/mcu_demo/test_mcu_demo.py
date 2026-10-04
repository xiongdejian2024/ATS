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
from xat_ecu.legacy.common.logger import logger


@allure.feature("SOA Demo")
@allure.story("demon")
class TestDoorService(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")

    def before_each_func(self, ecu):
        logger.info("before_each_func")
        self.excel_path = r"../mcu/config_data/signal_routing_communication"

    def after_each_func(self, ecu):
        logger.info("after_each_func")

    def after_class(self, ecu):
        logger.info("after_class")


    # def test_cycle_True(self):
    #     self.mix.check_signal_route_items(excel_path=self.excel_path, select_cond='cycle')

    def test_cycle_False(self):
        self.mix.check_signal_route_items(excel_path=self.excel_path, select_cond='event')

    # def test_ub_flag(self):
    #     self.mix.check_signal_route_items(excel_path=self.excel_path, select_cond='ub')


# pytest mcu_demo/test_mcu_demo.py