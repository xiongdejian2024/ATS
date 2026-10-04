#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_xcall.py
@Time         :2023/12/11 10:04
@Author       :yunpeng.zhou@jiduauto.com
@Description  :
"""

import time
import allure
import pytest

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务")
@allure.story("呼叫服务")
class TestBcall(TestABCBase):

    def before_class(self, ecu):
        self.soa.update(["CallService_client"])
        sleep(2)
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.ssh.set_airplane_mode(isOn.Off)
        # self.soa.hang_up_call_sos()
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        

    @pytest.mark.join_full
    @allure.title("Bcall_MSD_staging")
    def test_ecall_caseid_1898402(self):
        # 设置BCALL触发前置条件
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.trigger_bcall_sos(bCallOperCmd.kSTART_BCALL)
        # 接通后20s挂断
        sleep(20)
        self.soa.trigger_bcall_sos(bCallOperCmd.kHANG_UP_BCALL)

    

if __name__ == '__main__':
    pytest.main()

# pytest -sv xcall/test_xcall_abc.py -k test_ecall_caseid_1898378
