#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : test_pwm.py

**********************

------------------------------------------------------------------
@Time    : 2024/8/7 16:01
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
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

@allure.feature("Demon")
@allure.story("example Demo")
class TestExampleAbstract(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu):
        super().after_class(self, ecu)
        logger.info("after_class")

    @allure.title("测试io的pwm设置")
    def test_caseid_001(self):
        self.io.set_pwm(io_signal="pwm_test", freq=250, duty=50)
        sleep(2)
        self.io.get_pwm(io_signal="pwm_test")
