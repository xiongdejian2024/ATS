#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_buscomm.py
@Time         :2024/11/04 18:45
@Author       :quan.sun@jiduauto.com
@Description  :
"""
from xat_cases.dp2.cd_mcu.case_helper.test_abc_base import *


class TestDemo(CommonABCTestBase):
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

    def test_buscomm_caseid_112(self):
        logger.info(f"test buscomm")
        with allure.step('step1'):
            self.bus_comm.check("chassis2canfd", "CCUMCUCDChassis2CANFDFr01", "EpbCoornPrimPrimarySystemAvailable", 0)
 