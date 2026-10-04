# -*- coding: utf-8 -*-
"""
@File        : test_RemoteLogManagerService.py
@Author      : lei.tao@jiduatuo.com
@Time        : 2024/08/11 15:00 PM
@Description : Test SOA for test_RemoteLogManagerService
"""

import os
import sys
import pytest
import allure
import time
sys.path.append(os.path.join(os.getcwd().split("sat")[0], "sat"))

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass


@allure.feature("SOA服务接口")
@allure.story("架构基础/RemoteLogManagerService")
class TestRemoteLogManagerService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("RemoteLogManagerService", "client", "BGM_RemoteLogManagerService"),
                                     #("RemoteLogManagerService", "client")
                                     ])
        self.partner.method_default_timeout = 0.1
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.tester_present()

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
 
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)
    
    @allure.title("请求域控上传日志")
    @pytest.mark.smoke
    def test_caseid_1988528(self):
        for id in range(6):
            self.partner.send_request_and_ck_resp("RemoteLogManagerService_client_BGM_RemoteLogManagerService", 
                                                  "ReqUploadLog", {"triggerSourceInfo":{"source":id, "event":"err_log", "request_id":"123", "ctrlParam":"123"}}, 
                                                  {'out': 0})
            time.sleep(1)