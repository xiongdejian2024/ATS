#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_safety.py
@Time         :2023/08/08 14:37:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import allure
import pytest
from time import sleep


from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *


@allure.feature("SOA中间件测试")
@allure.story("功能安全/信息丢失")
@pytest.mark.wjj
class TestSafety(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.domin = self.tc_config.get('partner_domin', 'acu')

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        super().after_class(self, ecu)
        os.system("ps -ef | grep tcpreplay| awk '{print $2}' | xargs kill -9")

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')

    def after_each_func(self, ecu):
        try:
            self.sd_tester.stop_tester_present()
            self.partner.stop_operators()
        except Exception:
            pass
        super().after_each_func(ecu, start=False)

    @allure.title("event丢失_partner服务端检测event丢失_BGM客户端上报故障")
    @pytest.mark.smoke
    def test_caseid_1886111(self):
        self.partner = S2sBaseClass([("ANPMRCService", "server")], domin=self.domin)
        sleep(5)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                       {"fault": 1, "safetyFault": "loss"})
        # todo: 1.BGM中bootes日志打印SafetyLoss, type=Request, name=GetUsageMode
        sleep(6)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                       {"fault": 1, "safetyFault": "loss"})
        sleep(6)
        # todo: 2.BGM中bootes日志打印SafetyLoss, type=Request, name=GetUsageMode

    @allure.title("event丢失_partner服务端检测event丢失_CDCQ客户端上报故障")
    @allure.title("event丢失_partner服务端检测event丢失_ACU主板客户端上报故障")
    @allure.title("event丢失_partner服务端检测event丢失_ACU从板客户端上报故障")
    @pytest.mark.sanity
    def test_caseid_1886074_1886065_1892961(self):
        self.partner = S2sBaseClass([("VehicleModeService", "server"), ("ChassisService", "server")], domin=self.domin)
        sleep(5)
        self.partner.send_event_notify("VehicleModeService_server", "UsageModeChanged",
                                       {"mode": 2, "safetyFault": "loss"})
        sleep(10)
        # todo: BGM/CDCQ/CDCA/ACU主从板中bootes日志打印[SafetyLoss][RecvEvent][csInfo:VehicleModeService][UsageModeChanged]
        # sleep(6)

    @allure.title("event丢失_partner服务端检测event丢失_CDCA客户端上报故障")
    @pytest.mark.sanity
    def test_caseid_1886070(self):
        self.partner = S2sBaseClass([("AccountService", "server")], domin=self.domin)
        sleep(5)
        self.partner.send_event_notify("AccountService_server", "NotifyAccountSts",
                                       {"sts": {"uid": 1, "token": 1},
                                        "logInSts": 0,
                                        "safetyFault": "loss"})
        sleep(10)
        # todo: CDCA中bootes日志打印[SafetyLoss][RecvEvent][csInfo:AccountService][NotifyAccountSts]

    