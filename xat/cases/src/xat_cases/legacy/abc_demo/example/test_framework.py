#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_framework.py
@time         : 2024/02/27 14:19
@author       : quan.sun@jiduauto.com
@description  : 框架相关的一些cases
'''


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


    @pytest.mark.xfail(reason="https://jira.jiduauto.com/browse/SOA-21010")
    def test_caseid_001(self):
        sleep(5)
        assert False

    def test_caseid_002(self):
        sleep(5)
