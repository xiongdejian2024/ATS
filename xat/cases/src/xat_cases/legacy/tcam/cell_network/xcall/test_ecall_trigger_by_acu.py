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
class TestXcallAcu(TestABCBase):

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


    @pytest.mark.join_smoke
    @allure.title("Ecall_send_call_status_passivecall_ACU_success")
    def test_ecall_caseid_1898388(self):
        with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
                                                      keywords=[
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 2",  # 正在拨号
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 3, Type = 2",  # 正在响铃
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 2",  # 已挂断
        ], timeout=30):
            with allure.step('1.通过SOA接口发送[API:SetECallWorkStatus].eCallOperationCmd==START_ECALL触发Ecall话'):
                self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kACU, type=eCallType.kPASSIVE, status=eCallSts.kDIALING)
                self.soa.confirm_call_sos()
            # 接通后20s挂断
            sleep(20)
            with allure.step('2.通话30s后，模拟acu发送挂断消息'):
                self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kACU, type=eCallType.kPASSIVE,status=eCallSts.kHANG_UP)


if __name__ == '__main__':
    pytest.main()

# pytest -sv xcall/test_xcall_abc.py -k test_ecall_caseid_1898378
