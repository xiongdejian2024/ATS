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
@allure.story("功能安全/信息伪装")
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

    @allure.title("method伪装_BGM服务端检测method伪装_partner服务端上报故障")
    @pytest.mark.smoke
    def test_caseid_1886109(self):
        self.partner = S2sBaseClass([("VehicleModeService", "client")], domin=self.domin)  # partner服务连接
        sleep(5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {"safetyFault": "fake"})
        # todo: 1.BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetUsageMode
        sleep(6)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {"safetyFault": "fake"})
        sleep(6)
        # todo: 2.BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetUsageMode

    @allure.title("response伪装_BGM客户端检测response伪装_BGM客户端上报故障")
    @pytest.mark.sanity
    def test_caseid_1886108(self):
        self.partner = S2sBaseClass([("RPAAPAService", "server")], domin=self.domin)
        sleep(5)
        self.dk.send_apa_cmd(4, "0000000000000002")
        sleep(2)
        self.partner.ck_s2s_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", {"paReq": 4, "handleUid": 2})
        self.partner.send_method_response(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", {"safetyFault": "fake"})
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPASetResponse", {"paSetResponse": 2})
        # todo: BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Response, name=SetPARemoteStatus
        self.dk.send_apa_cmd(4, "0000000000000002")
        sleep(2)
        self.partner.ck_s2s_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", {"paReq": 4, "handleUid": 2})
        self.partner.send_method_response(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", {"safetyFault": "fake"})
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPASetResponse", {"paSetResponse": 2})
        # todo: BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Response, name=SetPARemoteStatus

    @allure.title("event伪装_客户端检测检测event伪装_客户端上报故障")
    @pytest.mark.smoke
    def test_caseid_1886107(self):
        self.partner = S2sBaseClass([("ANPMRCService", "server")], domin=self.domin)
        sleep(5)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                       {"fault": 1, "safetyFault": "fake"})
        # todo: 1.BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=RecvEvent, name=GetUsageMode
        sleep(6)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                       {"fault": 1, "safetyFault": "fake"})
        # todo: 2.BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=RecvEvent, name=GetUsageMode

    @allure.title("event伪装_CDCQ客户端检测event伪装_CDCQ客户端上报故障")
    @allure.title("event伪装_ACU主板客户端检测event伪装_ACU主板客户端上报故障")
    @allure.title("event伪装_ACU从板客户端检测event伪装_ACU从板客户端上报故障")
    @pytest.mark.sanity
    def test_caseid_1912728_1886062_1886054(self):
        self.partner = S2sBaseClass([("VehicleModeService", "server")], domin=self.domin)
        sleep(5)
        self.partner.send_event_notify("VehicleModeService_server", "UsageModeChanged",
                                       {"mode": 2, "safetyFault": "fake"})
        # todo: CDC、ACU中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=RecvEvent, name=UsageModeChanged
        sleep(6)

    @allure.title("event伪装_CDCA客户端检测检测event伪装_CDCA客户端上报故障")
    @pytest.mark.smoke
    def test_caseid_1886069(self):
        self.partner = S2sBaseClass([("AccountService", "server")], domin=self.domin)
        sleep(5)
        self.partner.send_event_notify("AccountService_server", "NotifyAccountSts",
                                       {"info": {"FunctionName": 1, "Authority": True},
                                        "safetyFault": "fake"})
        sleep(10)
        # todo: cdca中bootes日志打印SafetyFake, type=RecvEvent, name=UsageModeChanged
        # todo: CDC、ACU中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=RecvEvent, name=UsageModeChanged

    @allure.title("method伪装_ACU主板服务端检测method伪装_ACU主板服务端上报故障")
    @pytest.mark.full
    def test_caseid_1886063(self):
        self.partner = S2sBaseClass([("ANPMRCService", "client")], domin=self.domin)
        sleep(5)
        self.partner.send_method_request("ANPMRCService_client", "GetMRCSts", {"safetyFault": "fake"})
        # todo: ACU主板中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetMRCSts
        sleep(6)
        self.partner.send_method_request("ANPMRCService_client", "GetMRCSts", {"safetyFault": "fake"})
        sleep(6)
        # todo: ACU主板中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetMRCSts

    @allure.title("method伪装_ACU从板服务端检测method伪装_ACU从板服务端上报故障")
    @pytest.mark.full
    def test_caseid_1886055(self):
        self.partner = S2sBaseClass(
            [("IMUService", "client")], domin=self.domin)
        sleep(40)
        self.partner.send_method_request("IMUService_client", "GetIMUData", {"safetyFault": "fake"})
        # todo: ACU从板中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetIMUData
        sleep(2)
        self.partner.send_method_request("IMUService_client", "GetIMUData", {"safetyFault": "fake"})
        # todo: ACU从板中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetIMUData

    @allure.title("有新客户端连接_检测推迟30s")
    @pytest.mark.full
    def test_caseid_1886113(self):  # 延迟30s只有通道阻塞故障有，但是没必要了，BGM不检测通道阻塞
        self.partner = S2sBaseClass([("VehicleModeService", "client")], domin=self.domin)
        sleep(5)
        self.partner.send_method_request("VehicleModeService_client", "GetUsageMode", {"safetyFault": 'fake'})
        sleep(1)
        self.partner.send_method_request("VehicleModeService_client", "GetUsageMode",
                                         {"safetyFault": 'fake'})  # todo:当前需要调用两次才可以注入成功
        # todo：BGM中bootes日志未打印SafetyFakeInsertionBrokenAddressInvalid
        sleep(30)
        self.partner.send_method_request("VehicleModeService_client", "GetUsageMode", {"safetyFault": 'fake'})
        sleep(1)
        self.partner.send_method_request("VehicleModeService_client", "GetUsageMode",
                                         {"safetyFault": 'fake'})  # todo:当前需要调用两次才可以注入成功
        # todo：BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetUsageMode
        self.partner.start_single_partner("VehicleModeService", "client_1")
        sleep(5)
        self.partner.send_method_request("VehicleModeService_client", "GetUsageMode", {"safetyFault": 'fake'})
        sleep(1)
        self.partner.send_method_request("VehicleModeService_client", "GetUsageMode",
                                         {"safetyFault": 'fake'})  # todo:当前需要调用两次才可以注入成功
        # todo：BGM中bootes日志未打印SafetyFakeInsertionBrokenAddressInvalid
        sleep(30)
        self.partner.send_method_request("VehicleModeService_client_1", "GetUsageMode", {"safetyFault": 'fake'})
        sleep(1)
        self.partner.send_method_request("VehicleModeService_client_1", "GetUsageMode",
                                         {"safetyFault": 'fake'})  # todo:当前需要调用两次才可以注入成功
        # todo：BGM中bootes日志打印SafetyFakeInsertionBrokenAddressInvalid, type=Request, name=GetUsageMode