#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_demo.py
@Time         :2024/10/23 13:57
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
from xat_cases.dp2.lcu.case_helper.test_abc_base import *


class TestDemo(CommonSILTestBase):
    def before_class(self, ecu: EcuInfo):
        super().before_class(self, ecu)
        logger.info("before_class")

    def before_each_func(self, ecu: EcuInfo):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu: EcuInfo):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu: EcuInfo):
        super().after_class(self, ecu)
        logger.info("after_class")

    def test_demo(self):
        logger.info(f"test demo")
