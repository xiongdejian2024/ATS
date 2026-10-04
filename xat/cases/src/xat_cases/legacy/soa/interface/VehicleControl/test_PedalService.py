#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_PedalService.py
@Time         :2023/11/10 10:07:39
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import os
import sys
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *


@allure.feature("SOA服务接口")
@allure.story("整车控制/PedalService")
@pytest.mark.ypp
class TestPedalService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("PedalService", "client")])
        self.partner.method_default_timeout = 0.1

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)#加速踏板未踩下
        self.ipdu.set_vehspd(0)  # 车速
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        super().after_each_func(ecu, start=False)

    @allure.title("获取&通知加速踏板位置状态(带功能安全参数)_信号丢失")
    @pytest.mark.full
    def test_caseid_1985292(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 12800)
        self.partner.empty_all(0.5)
        self.ipdu.pause_all_bus_send()
        self.partner.ck_coming_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":50.0,"statusValidity":4}}, timeout=2, deviation=0.2)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 50, "statusValidity": 4}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":50,"statusValidity":0}}, timeout=1)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 50, "statusValidity": 0}]})

    @allure.title("获取&通知加速踏板位置状态(带功能安全参数)_100%-50%-0%")  
    @pytest.mark.sanity
    def test_caseid_1985294(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 25600)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":100,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 100, "statusValidity": 0}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 12800)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":50,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 50, "statusValidity": 0}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":0,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 0, "statusValidity": 0}]})

    @allure.title("获取&通知加速踏板位置状态(带功能安全参数)_E2E校验失败")  
    @pytest.mark.full
    def test_caseid_1985293(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set_no_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 25600)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":100,"statusValidity":7}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 100, "statusValidity": 7}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', 12800)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":50,"statusValidity":7}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 50, "statusValidity": 7}]})
        self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":50,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 50, "statusValidity": 0}]})

    @allure.title("获取&通知加速踏板位置状态(带功能安全参数)_默认值")
    @pytest.mark.full
    def test_caseid_1985296(self):
        for Rat in [12800, 0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat', Rat)
            sleep(0.5)
            self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 0, "statusValidity": 0}]},timeout=1)
            self.ipdu.resume_all_bus_send()
            sleep(1)
            if Rat in [12800]:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":50,"statusValidity":0}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 50, "statusValidity": 0}]})
            else:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalPosition",
                                  {"position":{"position":0,"statusValidity":0}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [0]},
                                              {"out": [{"id": 0, "position": 0, "statusValidity": 0}]})

    @allure.title("获取&通知制动踏板位置状态(带功能安全参数)_100%-50%-0%")  
    @pytest.mark.sanity
    def test_caseid_1985298(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 25600)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":100.0,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 100, "statusValidity": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 12800)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":50,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":0,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 0, "statusValidity": 0}]})

    @allure.title("获取&通知制动踏板的位置状态(带功能安全参数)_信号丢失") 
    @pytest.mark.full
    def test_caseid_1985301(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 12800)
        self.partner.empty_all(0.5)
        self.ipdu.pause_all_bus_send()
        self.partner.ck_coming_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                 {"position":{"position":50,"statusValidity":4}}, timeout=2, deviation=0.2)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 4}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":50,"statusValidity":0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 0}]})

    @allure.title("获取&通知制动踏板位置状态(带功能安全参数)_BrkPedlrRatQf != 3") 
    @pytest.mark.full
    def test_caseid_1985308(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 0)
        self.partner.empty_all(0.5)
        for sts in [3, 2, 1, 0]:
            logger.info(f"打印{sts}")
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', sts)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 12800)
            if sts in [3]:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":50,"statusValidity":0}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 0}]})
            elif sts in [2]:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":50,"statusValidity":2}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 2}]})
            elif sts in [1]:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":50,"statusValidity":6}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 6}]})
            elif sts in [0]:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":50,"statusValidity":8}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 8}]})

    @allure.title("获取&通知制动踏板位置状态(带功能安全参数)_默认值")
    @pytest.mark.full
    def test_caseid_1985309(self):
        for Perc in [12800, 0]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', Perc)
            sleep(0.2)
            self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 0, "statusValidity": 0}]})
            self.ipdu.resume_all_bus_send()
            if Perc in [12800]:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":50,"statusValidity":0}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 50, "statusValidity": 0}]})
            else:
                self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalPosition",
                                  {"position":{"position":0,"statusValidity":0}})
                self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalPosition", {"pedals": [1]},
                                              {"out": [{"id": 1, "position": 0, "statusValidity": 0}]})

    @allure.title("获取&通知踏板故障_制动踏板踩下")  # pass
    @pytest.mark.sanity
    def test_caseid_1980058(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        sleep(1)
        for qf in [0, 3, 1, 3, 2, 3]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', qf)
            if qf == 3:
                info = {"faultId": 0, "faultMsg": "", "id": 2}
            else:
                info = {"faultId": 1, "faultMsg": "", "id": 1}
            self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                      {"faults": [info]})
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                                  {"out": [info]})

    @allure.title("获取&通知踏板故障_制动踏板踩下(E2E校验失败)")#
    @pytest.mark.full
    def test_caseid_1980060(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 1, "faultMsg": "", "id": 1}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 1, "faultMsg": "", "id": 1}]})
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})
    
    @allure.title("获取&通知踏板故障_制动踏板踩下(重启event)")  
    @pytest.mark.full
    def test_caseid_1984604(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]},timeout = 1)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})

    @allure.title("获取&通知踏板故障_加速踏板位置(E2E校验失败)")
    @pytest.mark.full
    def test05_caseid_1980062(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        self.ipdu.set_no_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 2, "faultMsg": "", "id": 0}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 2, "faultMsg": "", "id": 0}]})
        self.ipdu.restore_crc(self.ipdu.propulsioncan.EcmPropFr00, 'AccrPedlRatAccrPedlRat')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})

    @allure.title("获取&通知踏板故障_加速踏板位置(信号丢失)")
    @pytest.mark.sanity
    def test_caseid_1980063(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        sleep(0.5)
        self.ipdu.pause_all_bus_send()
        self.partner.ck_coming_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 2, "faultMsg": "", "id": 0}]}, timeout=2, deviation=0.2)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 2, "faultMsg": "", "id": 0}]})
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]}, timeout=1)

    @allure.title("获取&通知踏板故障_制动踏板位置(BrkPedlrRatQf = 3!=3)")
    @pytest.mark.sanity
    def test_caseid_1980064(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 0)  # 制动踏板位置
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 2, "faultMsg": "", "id": 1}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 2, "faultMsg": "", "id": 1}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 1)  # 制动踏板位置
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 2, "faultMsg": "", "id": 1}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 2)  # 制动踏板位置
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 2, "faultMsg": "", "id": 1}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})

    @allure.title("获取&通知踏板故障_制动踏板位置(信号丢失)")
    @pytest.mark.full
    def test_caseid_1980065(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        self.ipdu.pause_all_bus_send()
        self.partner.ck_coming_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 2, "faultMsg": "", "id": 1}]}, timeout=2, deviation=0.2)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 2, "faultMsg": "", "id": 1}]})
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})

    @allure.title("获取加速踏板踩下状态(不带功能安全参数)")
    @pytest.mark.sanity
    def test_caseid_1985310(self):
        for sts in [1, 0]:
            logger.info(f"打印{sts}")
            sleep(0.2)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', sts)
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [0]},
                                                {"out": [{"id": 0, "status": sts}]})

    @allure.title("获取加速踏板踩下状态(不带功能安全参数)E2E校验失败")
    @pytest.mark.smoke
    def test_caseid_1985311(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        sleep(0.2)
        self.ipdu.set_no_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [0]},
                                              {"out": [{"id": 0, "status": 0}]})
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [0]},
                                              {"out": [{"id": 0, "status": 0}]})
    
    @allure.title("获取加速踏板踩下状态(不带功能安全参数)_(信号丢失)")
    @pytest.mark.sanity
    def test_caseid_1985312(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)  # 加速踏板
        self.partner.empty_all(0.5)
        self.ipdu.pause_bus_send("chassiscan2")
        sleep(1)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [0]},
                                              {"out": [{"id": 0, "status": 0}]})
        self.ipdu.resume_bus_send("chassiscan2")
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [0]},
                                              {"out": [{"id": 0, "status": 0}]})
    
    @allure.title("获取加速踏板踩下状态(带功能安全参数)")
    @pytest.mark.sanity
    def test_caseid_1985021(self):
        for sts in [1, 0]:
            logger.info(f"打印{sts}")
            sleep(0.2)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', sts)  # 加速踏板
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                                {"out": [{"value": {"id": 0, "status": sts}, "statusValidity": 0}]})

    @allure.title("获取加速踏板踩下状态(带功能安全参数)信号丢失")  
    @pytest.mark.full
    def test_caseid_1985023(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)  # 加速踏板
        sleep(1)
        self.ipdu.pause_bus_send("chassiscan2")
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                              {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 4}]}, timeout=2)
        self.ipdu.resume_bus_send("chassiscan2")
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                              {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0}]},
                                              timeout=2)

    @allure.title("获取加速踏板踩下状态(带功能安全参数)E2E校验失败")
    @pytest.mark.full
    def test_caseid_1985022(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)  # 加速踏板
        sleep(1)
        self.ipdu.set_no_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                              {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 7}]})
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                              {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0}]})  

    @allure.title("获取加速踏板踩下状态(带功能安全参数)_(E2E校验失败+信号丢失)")
    @pytest.mark.full
    def test_caseid_1985024(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)  # 加速踏板
        sleep(1)
        self.ipdu.set_no_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                              {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 7}]})  
        self.ipdu.pause_bus_send("chassiscan2")
        sleep(1)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                              {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 7}]}) 
        self.ipdu.resume_bus_send("chassiscan2")
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd') 
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0]},
                                              {"out": [{"value": {"id": 0, "status": 1}, "statusValidity": 0}]})  
    
    @allure.title("获取&通知踏板踩下状态(带功能安全参数)_增加时间戳")#在s2s进程生命周期内，同一个数据（比如安全带状态）的get/event接口的id值相同，不同数据的id值不同；如果s2s重启后，id值会重新生成
    @pytest.mark.full
    def test_caseid_1985074(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)  # 加速踏板
        acc1 = self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 0}}) 
        acc1_timestamp = acc1["status"]['sequenceTime']['timestamp']
        acc1_id = acc1["status"]['sequenceTime']['id']
        logger.info(f"--acc1_id: {acc1_id}--acc1_timestamp: {acc1_timestamp}")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
        brk1 = self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": 1, "validity": 0}})
        brk1_timestamp = brk1["status"]['sequenceTime']['timestamp']
        brk1_id = brk1["status"]['sequenceTime']['id']
        logger.info(f"--brk1_id: {brk1_id}--brk1_timestamp: {brk1_timestamp}")
        resp1 = self.partner.send_request_and_return_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0, 1]})["out"]
        for data in resp1:
            if data["value"]["id"] == 0:
                resp1_acc_timestamp = data["sequenceTime"]["timestamp"]
                resp1_acc_id = data["sequenceTime"]["id"]
            else:
                resp1_brk_timestamp = data["sequenceTime"]["timestamp"]
                resp1_brk_id = data["sequenceTime"]["id"]
        assert resp1_acc_id == acc1_id
        assert resp1_brk_id == brk1_id
        assert resp1_acc_timestamp == acc1_timestamp 
        assert resp1_brk_timestamp == brk1_timestamp#get和event应该拿到相同的id和timestamp
        self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT)#重启后拿到不同的id和timestamp,且timestamp越来越小
        sleep(1)
        acc2 = self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 0}})
        acc2_timestamp = acc2["status"]['sequenceTime']['timestamp']
        acc2_id = acc2["status"]['sequenceTime']['id']
        logger.info(f"--acc2_id: {acc2_id}--acc2_timestamp: {acc2_timestamp}")
        brk2 = self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": 1, "validity": 0}})
        brk2_timestamp = brk2["status"]['sequenceTime']['timestamp']
        brk2_id = brk2["status"]['sequenceTime']['id']
        logger.info(f"--brk2_id: {brk2_id}--brk2_timestamp: {brk2_timestamp}")
        resp2 = self.partner.send_request_and_return_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [0, 1]}, timeout = 2)["out"]
        for data in resp2:
            if data["value"]["id"] == 0:
                resp2_acc_timestamp = data["sequenceTime"]["timestamp"]
                resp2_acc_id = data["sequenceTime"]["id"]
            else:
                resp2_brk_timestamp = data["sequenceTime"]["timestamp"]
                resp2_brk_id = data["sequenceTime"]["id"]
        assert resp2_acc_id != resp1_acc_id
        assert resp2_brk_id != resp1_brk_id
        assert resp2_acc_timestamp < resp1_acc_timestamp 
        assert resp2_brk_timestamp < resp1_brk_timestamp
        assert acc2_timestamp == resp2_acc_timestamp
        assert brk2_timestamp == resp2_brk_timestamp
    
    @allure.title("通知加速踏板踩下状态")  #  2.0
    @pytest.mark.sanity
    def test_caseid_1985009(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', sts)  # 加速踏板
            self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                    {"status": {"value": sts, "validity": 0}})
        
    @allure.title("通知加速踏板踩下状态_(信号丢失1000ms)")  #  2.0
    @pytest.mark.full
    def test_caseid_1985010(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)  # 加速踏板
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 0}})
        sleep(0.5)
        self.ipdu.pause_all_bus_send()
        self.partner.ck_coming_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 4}}, timeout=1, deviation=0.2)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 0}})
    
    @allure.title("通知加速踏板踩下状态_(E2E校验失败)")  #  v2.0
    @pytest.mark.full
    def test_caseid_1985011(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)  # 加速踏板
        sleep(0.5)
        self.ipdu.set_no_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 7}})
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 0}})
    
    @allure.title("通知加速踏板踩下状态_(重启event)")  #  v2.0
    @pytest.mark.full
    def test_caseid_1985012(self):
        self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 0, "validity": 0}})
    
    @allure.title("通知加速踏板踩下状态_(E2E校验失败+信号丢失)")
    @pytest.mark.smoke
    def test_caseid_1985016(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 1)  # 加速踏板
        sleep(1)
        self.ipdu.set_no_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 7}}) 
        self.partner.empty_all()
        self.ipdu.pause_all_bus_send()
        sleep(1)
        self.partner.ck_no_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus")
        self.ipdu.resume_all_bus_send()
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd') 
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "AccPedalStatus",
                                  {"status": {"value": 1, "validity": 0}}) 
        
    @allure.title("获取制动踏板踩下状态(不带功能安全参数)")
    @pytest.mark.smoke
    def test_caseid_1985318(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [1]},
                                              {"out": [{"id": 1, "status": 1}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [1]},
                                              {"out": [{"id": 1, "status": 0}]})

    @allure.title("获取制动踏板踩下状态(不带功能安全参数)_(默认值)")
    @pytest.mark.full
    def test_caseid_1985319(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        sleep(0.5)
        self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [1]},
                                              {"out": [{"id": 1, "status": 0}]},timeout=2)
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [1]},
                                              {"out": [{"id": 1, "status": 1}]},timeout=2)

    @allure.title("获取制动踏板踩下状态(不带功能安全参数)_(E2E校验失败)")
    @pytest.mark.full
    def test_caseid_1985320(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [1]},
                                              {"out": [{"id": 1, "status": 1}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [1]},
                                              {"out": [{"id": 1, "status": 0}]})
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatus", {"pedals": [1]},
                                              {"out": [{"id": 1, "status": 0}]})
    
    @allure.title("获取制动踏板踩下状态(带功能安全参数)")
    @pytest.mark.sanity
    def test_caseid_1980106(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [1]},
                                              {"out": [{"value": {"id": 1, "status": 1}, "statusValidity": 0}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [1]},
                                              {"out": [{"value": {"id": 1, "status": 0}, "statusValidity": 0}]})
    
    # @allure.title("获取制动踏板踩下状态(带功能安全参数)")
    # def test_caseid_eeeee(self):
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
    #     self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
    #                               {"status": {"value": 1, "validity": 0}})
    #     self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 1)
    #     self.partner.ck_no_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus")
    
    @allure.title("加速踏板踩下(E2E校验失败+信号丢失)")#
    @pytest.mark.smoke
    def test_caseid_1987103(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdSts', 0)
        self.ipdu.set_no_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        sleep(1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 1, "faultMsg": "", "id": 0}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]})
        self.ipdu.pause_all_bus_send()
        self.partner.ck_no_event(PEDAL_SERVICE_CLIENT, "PedalFault", timeout=1)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]})
        self.ipdu.resume_all_bus_send()
        sleep(2)
        self.partner.ck_no_event(PEDAL_SERVICE_CLIENT, "PedalFault")
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]})
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        
    @allure.title("获取制动踏板踩下状态(带功能安全参数)_(E2E校验失败)")
    @pytest.mark.full
    def test_caseid_1980107(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [1]},
                                              {"out": [{"value": {"id": 1, "status": 1}, "statusValidity": 7}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [1]},
                                              {"out": [{"value": {"id": 1, "status": 0}, "statusValidity": 7}]})
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetStatusValidity", {"pedals": [1]},
                                              {"out": [{"value": {"id": 1, "status": 0}, "statusValidity": 0}]})
    
    @allure.title("通知制动踏板踩下状态 ")  #  v1.4 
    @pytest.mark.sanity
    def test_caseid_1983622(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": 1, "validity": 0}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": 0, "validity": 0}})
    
    @allure.title("通知制动踏板踩下状态_(E2E校验失败)")  #  v1.4   
    @pytest.mark.full
    def test_caseid_1983623(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        sleep(0.5)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": 1, "validity": 7}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": 0, "validity": 7}})
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": 0, "validity": 0}})
    
    @allure.title("通知制动踏板踩下状态_(重启event)")  #  v1.4 
    @pytest.mark.full
    def test_caseid_1984618(self):
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', sts)
            self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT, resume_all_bus=False)
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus",
                                  {"status": {"value": sts, "validity": 0}})
    
    @allure.title("获取&通知制动踏板行程状态")  # 2.0
    @pytest.mark.sanity
    def test_caseid_1984909(self):
        for sts in [400, 1500, 5200, 8191, 0]:
            logger.info(f"发送信号: {sts}")
            self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', sts)
            self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalTravel",
                                  {"travel": {"travel": sts* 0.01-5, "travelValidity": 0}})
            self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetBrakePedalTravel", {"pedals": [1]},
                                              {"out": {"travel": sts* 0.01-5, "travelValidity": 0}})
    
    @allure.title("获取&通知制动踏板行程状态_默认值")  # 2.0
    @pytest.mark.full
    def test_caseid_1984910(self):
        self.ipdu.set(self.ipdu.chassiscan2.BbmChas2Fr01, 'BrkPedlTrvlAct', 0)
        sleep(0.2)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetBrakePedalTravel", {"pedals": [1]},
                                            {"out": {"travel": 0* 0.01-5, "travelValidity": 0}})
        self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetBrakePedalTravel", {"pedals": [1]},
                                            {"out": {"travel": 255, "travelValidity": 0}},timeout = 2)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalTravel",
                                {"travel": {"travel": 0* 0.01-5, "travelValidity": 0}})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetBrakePedalTravel", {"pedals": [1]},
                                            {"out": {"travel": 0* 0.01-5, "travelValidity": 0}},timeout = 2)
    
    @allure.title("获取&通知踏板故障_加速踏板踩下(信号丢失)")  # 2.0
    @pytest.mark.full
    def test_caseid_1985026(self):
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.ipdu.pause_bus_send("chassiscan2")
        self.partner.ck_coming_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 1, "faultMsg": "", "id": 0}]}, timeout=1.5)
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]})
        self.ipdu.resume_bus_send("chassiscan2")
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})
    
    @allure.title("获取&通知踏板故障_加速踏板踩下(E2E校验失败)")  # 2.0
    @pytest.mark.sanity
    def test_caseid_1985027(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        sleep(0.2)
        self.ipdu.set_no_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 1, "faultMsg": "", "id": 0}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]})
        self.ipdu.restore_crc(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd')
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                  {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                              {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]})
    
    @allure.title("获取&通知踏板故障_加速踏板踩下(重启event)") # 2.0
    @pytest.mark.full
    def test_caseid_1985028(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr04, 'AccrPedlPsdAccrPedlPsd', 0)
        self.restart_bgm_and_connect_service(PEDAL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "PedalFault",
                                {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]})
        self.partner.send_request_and_ck_resp(PEDAL_SERVICE_CLIENT, "GetPedalFault", {},
                                            {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]},timeout = 1)
    
    