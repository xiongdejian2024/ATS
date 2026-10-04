#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_diag.py
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

    def test_diag_caseid_111(self):
        logger.info(f"test diag")
        with allure.step('step1'):
            self.sd_tester.send_data([0x10, 0x01])
            return_data = self.sd_tester.return_udsdata_and_check_and_print_response_result()
            logger.info(f"return_data:{return_data}")
            
            assert [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4] == return_data

        # with allure.step('step2'):
        #     self.assertTrue(False)
