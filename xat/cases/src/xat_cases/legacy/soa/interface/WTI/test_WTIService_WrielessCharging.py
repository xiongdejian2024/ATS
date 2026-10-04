#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import allure
import pytest
import random
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.soa.case_helper.utils import *

@allure.feature("SOA服务接口")
@allure.story("WTI/WTIService_Door")
@pytest.mark.jishu
class TestDoorWTIService(TestBase):
    
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("WTIService", "client")
                                ])
        self.partner.method_default_timeout = 0.1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,'VehMtnStVehMtnSt','VehMtnSt2_StandStillVal3') # 切UsageMode的前置条件
        time.sleep(5)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    #####################新增2.1删除主副驾无线充电故障状态提示#####################
    @allure.title("副驾无线充电故障状态提示_取消")
    @pytest.mark.sanity
    def test_caseid_1988445(self): 
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', 0)  
        self.partner.empty_all(0.5)
        for usage in [2,11,0,13,1]:
            logger.info(f"当前usage为.{usage}")
            self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', random.choice(range(1, 16)))
            self.sd_tester.change_usage_mode(usage)
            self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", "Driver Wireless Charging Remind", 5)    
            data = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
            logger.info(f"返回值：{data}")
            for i in data:
                assert "Driver Wireless Charging Remind" not in i 
    
    @allure.title("主驾无线充电故障状态提示_取消")
    @pytest.mark.sanity
    def test_caseid_1988444(self): 
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', 0)  
        self.partner.empty_all(0.5)
        for usage in [2,11,0,13,1]:
            logger.info(f"当前usage为.{usage}")
            self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', random.choice(range(1, 16)))
            self.sd_tester.change_usage_mode(usage)
            self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", "Driver Wireless Charging Remind", 5)    
            data = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {})['out']
            logger.info(f"返回值：{data}")
            for i in data:
                assert "Driver Wireless Charging Remind" not in i 
