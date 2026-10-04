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
class TestXcallCdc(TestABCBase):

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
    @allure.title("Ecall_send_call_status_activecall_CDC_success & Ecall_send_call_status_activecall_CDC_cancel")
    def test_ecall_caseid_1898410_and_caseid_101330(self):
        with allure.step('1.通过SOS触发Ecall'):
            self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kCDC)
        # 7.5s以内有两个按钮（取消或者挂断）
        # 7.5s以后只有挂断
        sleep(5)
        with allure.step('2.在eCallCountTi_TCAM(7.5s)时间内，再次按压SOS按键挂断Ecall'):
            self.soa.cancel_call_sos(ReqSrc=eCallReqSource.kCDC)

    @pytest.mark.join_smoke
    @allure.title("Ecall_Active_triggered_by_ecalldown & Ecall_Active_triggered_by_CDC")
    def test_ecall_caseid_1898337_and_caseid_101320(self):
        with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
                                                      keywords=[
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 1",  # 正在拨号
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 2, Type = 1",  # 正在响铃
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 1",  # 已挂断
        ], timeout=30):
            self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kCDC)
            # 接通后20s挂断
            sleep(20)
            self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kCDC)
    
    @pytest.mark.join_smoke
    @allure.title("Ecall_Active_triggered_by_CDC_and_Confirm")
    def test_ecall_caseid_101319(self):
        with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
                                                      keywords=[
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 1",  # 正在拨号
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 2, Type = 1",  # 正在响铃
            "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 1",  # 已挂断
        ], timeout=30):
            self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kCDC)
            sleep(4)
            self.soa.confirm_call_sos()
            # 接通后15s挂断
            sleep(15)
            self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kCDC)


if __name__ == '__main__':
    pytest.main()

# pytest -sv xcall/test_xcall_abc.py -k test_ecall_caseid_1898378