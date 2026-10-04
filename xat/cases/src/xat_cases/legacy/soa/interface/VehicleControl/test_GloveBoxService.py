#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_GloveBoxService.py
@Time         :2023/06/14 09:07:49
@Author       :jishu.duan_ext
@Description  :
"""
import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.utils import *

NotifyTi = 1


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("整车控制/GloveBoxService")
@pytest.mark.jishu
class TestGloveBoxService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("GloveBoxService", "client")])
        self.partner.method_default_timeout = 0.1

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.partner.empty_all()

    def after_each_func(self, ecu):
        if ecu.get("testresult") != "Pass":
            logger.error("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            logger.info("case成功，需等待3s让环境恢复")
            sleep(3)
        super().after_each_func(ecu, start=False)

    @allure.title("打开手套箱_开")
    @pytest.mark.sanity
    def test_caseid_109430(self):
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "RmnLockgPrsnlReq", 1)
        sleep(0.1)
        self.partner.ck_s2s_event(GLOVEBOX_SERVICE_CLIENT, "GloveBoxStatus",
                                    {'status': {'isLocked': True, 'needAuthentication': True}})


    @allure.title("打开手套箱_二次调用")
    @pytest.mark.full
    def test_caseid_109429(self):
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        sleep(1)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Open", {})
        sleep(0.05)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "RmnLockgPrsnlReq", 1)


    @allure.title("设置手套箱上隐私锁_上锁并通知状态")
    @pytest.mark.sanity
    def test_caseid_109428(self):
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'LockgPrsnlSts', 'OnOff1_Off')
        sleep(1)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgPrsnlSts", 1)
        self.partner.ck_s2s_event(GLOVEBOX_SERVICE_CLIENT, "GloveBoxStatus",
                                    {'status': {'isLocked': True, 'needAuthentication': False}})
        self.partner.send_request_and_ck_resp(GLOVEBOX_SERVICE_CLIENT, "GetGloveBoxStatus", {},
                                                {'out': {'isLocked': True, 'needAuthentication': False}})

    @allure.title("上锁手套箱_二次调用")
    @pytest.mark.full
    def test_caseid_109427(self):
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'LockgPrsnlSts', 'OnOff1_Off')
        sleep(1)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        sleep(0.015)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgPrsnlSts", 1)


    @pytest.mark.smoke
    @allure.title("设置手套箱上隐私锁_解锁并通知状态")
    def test_caseid_109426(self):
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgPrsnlSts", 1)
        sleep(0.5)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgPrsnlSts", 0)
        self.partner.ck_s2s_event(GLOVEBOX_SERVICE_CLIENT, "GloveBoxStatus",
                                    {'status': {'isLocked': False, 'needAuthentication': False}})
        self.partner.send_request_and_ck_resp(GLOVEBOX_SERVICE_CLIENT, "GetGloveBoxStatus", {},
                                                {'out': {'isLocked': False, 'needAuthentication': False}})

    @allure.title("启动场景event_GloveBox")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_1988828(self): # LockgPrsnlSts|RmnLockgPrsnlReq
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})        
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgPrsnlSts", 0)
        self.partner.send_request_and_ck_resp(GLOVEBOX_SERVICE_CLIENT, "GetGloveBoxStatus", {},
                                                {'out': {'isLocked': False, 'needAuthentication': False}})
        self.restart_bgm_and_connect_service(GLOVEBOX_SERVICE_CLIENT)
        # 通知手套箱状态
        self.partner.ck_event_and_resp(GLOVEBOX_SERVICE_CLIENT, "GloveBoxStatus", 
                                       {'status': {'isLocked': False, 'needAuthentication': False}})    

    @allure.title("解锁手套箱_二次调用")
    @pytest.mark.full
    def test_caseid_109425(self):
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'LockgPrsnlSts', 'OnOff1_On')
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})
        sleep(0.015)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "LockgPrsnlSts", 0)

    @allure.title("打开手套箱_碰撞模式下15s后打开")
    @pytest.mark.full
    def test_caseid_1985087(self):
        self.sd_tester.change_car_mode(3, do_assert=1)
        sleep(17)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Open", {})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr08, "RmnLockgPrsnlReq", 1)
        sleep(0.1)
        self.partner.ck_s2s_event(GLOVEBOX_SERVICE_CLIENT, "GloveBoxStatus",
                                      {'status': {'isLocked': False, 'needAuthentication': True}})

    @allure.title("打开手套箱_校验PDU打断逻辑")
    @pytest.mark.full
    def test_caseid_1984268(self):
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Open", {})
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Open", {})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("GlvBoxOpenReqFromUI", [1, 1, 0])

    @pytest.mark.full
    @allure.title("设置手套箱上隐私锁_校验报文打断逻辑")
    def test_caseid_1984282(self):
        self.bgm_eth_inter.start_bgm_tcpdump()  
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Lock", {})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("LockgPrsnlReqFromHmi", [1, 1, 0])
        
    @pytest.mark.full
    @allure.title("设置手套箱解隐私锁_校验报文打断逻辑")
    def test_caseid_1984283(self):
        self.bgm_eth_inter.start_bgm_tcpdump()  
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})
        self.partner.send_method_request(GLOVEBOX_SERVICE_CLIENT, "Unlock", {})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("LockgPrsnlReqFromHmi", [2, 2, 0])











