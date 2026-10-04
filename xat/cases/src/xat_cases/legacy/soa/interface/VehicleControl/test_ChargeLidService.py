#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_ChargeLidService.py
@Time         :2023/06/6 19:07:31
@Author       :peipei.yang_ext@jiduauto.com
@Description  :
"""
import os
import sys

from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase


@allure.feature("SOA服务接口")
@allure.story("整车控制/ChargeLidService")
class TestChargeLidService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("ChargeLidService", "client"),
                                     ("VehicleSetStatusService", "client")])
        self.partner.method_default_timeout = 0.1
        self.ipdu.lin1_wakeup()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 0)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 0)
        #全部无故障
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', 0)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', 0)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', 0)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', 0)
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)        
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()  # 恢复所有总线
        super().after_each_func(ecu, start=False)

    @allure.title("打开充电口盖")
    @pytest.mark.smoke
    def test_caseid_1903601(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Open", {})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChrgLidReCtrlHmiReq", [1, 0])
        self.bgm_eth_inter.ck_period_time('ChrgLidReCtrlHmiReq', 0.5)
        
    @allure.title("关闭充电口盖")
    @pytest.mark.sanity
    def test_caseid_1983176(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Close", {})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChrgLidReCtrlHmiReq", [2, 0])
        self.bgm_eth_inter.ck_period_time('ChrgLidReCtrlHmiReq', 0.5)

    @allure.title("打开充电口盖_打断机制")
    @pytest.mark.full
    def test_caseid_1981073(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Open", {})
        sleep(0.1)
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Open", {})
        sleep(2)
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Open", {})
        sleep(0.1)
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Close", {})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChrgLidReCtrlHmiReq", [1, 0, 1, 0])

    @allure.title("关闭充电口盖_打断机制")
    @pytest.mark.full
    def test_caseid_1981074(self):
        # todo 开始抓包
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Close", {})
        sleep(0.1)
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Close", {})
        sleep(2)
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Close", {})
        sleep(0.1)
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "Open", {})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChrgLidReCtrlHmiReq", [2, 0, 2, 0])

    @allure.title("获取充电口盖异常状态&通知充电口盖异常状态")
    @pytest.mark.full
    def test_caseid_1981081(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 0)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [1]}, timeout=2)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [1]}, timeout=2)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [1, 2]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [1, 2]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [2]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [2]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [0]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [0]})

    @allure.title("获取充电口盖异常状态&通知充电口盖异常状态_默认值")
    @pytest.mark.full
    def test_caseid_1981083(self):
        self.partner.empty_all(0.5)
        for AcDcBlkFb in [1, 0]:
            self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcBlkFb', AcDcBlkFb)
            for AcDcOverTrvlFb in [1, 0]:
                self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTrvlFb', AcDcOverTrvlFb)
                self.restart_bgm_and_connect_service(CHARGELID_SERVICE_CLIENT, resume_all_bus=False)
                self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                                    {"out": [0]})
                self.ipdu.resume_all_bus_send()
                if AcDcBlkFb ==1 and AcDcOverTrvlFb==1:
                    self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [1, 2]})
                    self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [1, 2]})
                elif AcDcBlkFb ==1 and AcDcOverTrvlFb==0:
                    self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [1]})
                    self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [1]})
                elif AcDcBlkFb ==0 and AcDcOverTrvlFb==1:
                    self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [2]})
                    self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [2]})
                elif AcDcBlkFb ==0 and AcDcOverTrvlFb==0:
                    self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidWarnSts", {"warnsts": [0]})
                    self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetWarnStatus", {},
                                              {"out": [0]})

    @allure.title("获取充电口盖位置百分比&通知充电口盖位置百分比")
    @pytest.mark.sanity
    def test_caseid_1981106(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', 0)
        self.partner.empty_all(0.5)
        for posn2 in [1, 5, 6, 100, 101, 0]:
            logger.info(f"打印{posn2}")
            if posn2 in [1, 5, 6, 100, 0]:
                posn2 = posn2
            else:
                posn2 = 255
            self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', posn2)
            self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidPos", {"pos": posn2})
            self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetChargeLidPos", {},
                                                  {"out": posn2})

    @allure.title("获取充电口盖位置百分比&通知充电口盖位置百分比_默认值")
    @pytest.mark.full
    def test_caseid_1981109(self):
        for posn2 in [1, 100, 0]:
            logger.info(f"打印{posn2}")
            self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcActPosn2', posn2)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(CHARGELID_SERVICE_CLIENT, resume_all_bus=False)
            self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetChargeLidPos", {},
                                                {"out": 255})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidPos", {"pos": posn2})
            self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetChargeLidPos", {},
                                                {"out": posn2})
    
    @allure.title("获取充电口盖故障状态&通知充电口盖故障状态_全部故障")
    @pytest.mark.smoke
    def test_caseid_1985117(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 6, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 6, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 2, "faultMsg": ""},{"fault": 6, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 2, "faultMsg": ""},{"fault": 6, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 6, "faultMsg": ""},{"fault": 2, "faultMsg": ""},{"fault": 7, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 6, "faultMsg": ""},{"fault": 2, "faultMsg": ""},{"fault": 7, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 6, "faultMsg": ""},{"fault": 2, "faultMsg": ""}, {"fault": 7, "faultMsg": ""},{"fault": 8, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 6, "faultMsg": ""},{"fault": 2, "faultMsg": ""},{"fault": 7, "faultMsg": ""},{"fault": 8, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 2, "faultMsg": ""},{"fault": 7, "faultMsg": ""},{"fault": 8, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 2, "faultMsg": ""},{"fault": 7, "faultMsg": ""}, {"fault": 8, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 7, "faultMsg": ""},{"fault": 8, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 7, "faultMsg": ""},{"fault": 8, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 8, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 8, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 0, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
    
    @allure.title("获取充电口盖故障状态&通知充电口盖故障状态_内部故障")
    @pytest.mark.sanity
    def test_caseid_1985118(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 6, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 6, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 0, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
    
    @allure.title("获取充电口盖故障状态&通知充电口盖故障状态_过温故障(130°以上)故障")
    @pytest.mark.sanity
    def test_caseid_1985119(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 2, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 2, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 0, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
    
    @allure.title("获取充电口盖故障状态&通知充电口盖故障状态_过压故障(17V以上)故障")
    @pytest.mark.sanity
    def test_caseid_1985120(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 7, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 7, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 0, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
    
    @allure.title("获取充电口盖故障状态&通知充电口盖故障状态_电压过低故障(小于7.5V)故障")
    @pytest.mark.full
    def test_caseid_1985121(self):
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 8, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 8, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 0, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
    
    @allure.title("获取充电口盖故障状态&通知充电口盖故障状态_默认值")
    @pytest.mark.full
    def test_caseid_1985122(self):
        self.restart_bgm_and_connect_service(CHARGELID_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 0, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcElecErrFb', 1)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverTFb', 1)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcOverVoltFb', 1)
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcUnderVoltFb', 1)
        self.restart_bgm_and_connect_service(CHARGELID_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 0, "faultMsg": ""}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "ChargeLidFault",
                                  {"faults": [{"fault": 6, "faultMsg": ""},
                                              {"fault": 2, "faultMsg": ""}, 
                                              {"fault": 7, "faultMsg": ""}, 
                                              {"fault": 8, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetFaultInfo", {},
                                              {"out": [{"fault": 6, "faultMsg": ""},
                                                       {"fault": 2, "faultMsg": ""}, 
                                                       {"fault": 7, "faultMsg": ""}, 
                                                       {"fault": 8, "faultMsg": ""}]})

    @allure.title("设置拔枪充电口盖自动关闭充电口盖时间_前置判断&信号发送逻辑")
    @pytest.mark.smoke
    def test_caseid_1988980(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for cmd in [0, 120, 120, 255]: # 存在两次参数值相同的调用。且无打断的情况下，都需响应
            # self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, 'SetGunPullOutChargeLidCloseTimeConfig', 
            #                                 {"configCmd":{"closeTimeCmd": cmd}})  
            if cmd <= 120:
                self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, 'SetGunPullOutChargeLidCloseTimeConfig', 
                                                    {"configCmd":{"closeTimeCmd": cmd}}, 
                                                    {"out": 0}) # 可执行
            else:
                self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, 'SetGunPullOutChargeLidCloseTimeConfig', 
                                                    {"configCmd":{"closeTimeCmd": cmd}}, 
                                                    {"out": 1}) # 参数超出范围  
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetClsChargeLidTi", [0, 0, 0, 120, 120, 120, 120, 120, 120]) 
        self.bgm_eth_inter.ck_period_time('SetClsChargeLidTi', 0.1, deviation=0.5, permit_fail_times=3)
            
    @allure.title("设置拔枪充电口盖自动关闭充电口盖时间_打断逻辑")
    @pytest.mark.full
    def test_caseid_1988981(self):  
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)  
        for cmd in [100, 0, 121]:
            self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, 'SetGunPullOutChargeLidCloseTimeConfig', 
                                            {"configCmd":{"closeTimeCmd": 0}})  
            sleep(0.1)
            self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, 'SetGunPullOutChargeLidCloseTimeConfig', 
                                            {"configCmd":{"closeTimeCmd": cmd}})   
            sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        counter=self.bgm_eth_inter.get_signal_values("SetClsChargeLidTi")
        assert len(counter) in range(10, 13), "打断逻辑有误"            
        
@allure.feature("SOA服务接口")
@allure.story("整车控制/ChargeLidService")
class TestChargeLidServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("ChargeLidService", "client")])
        self.partner.wait_for_service_reconnect(CHARGELID_SERVICE_CLIENT) 
        sleep(10)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def set_usage_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入usage mode给到S2S"""
        logger.info(f"设置usage mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)

    def set_car_mode(self, mode):
        """通过模拟mcu cdd打包总线数据来输入carmode给到S2S"""
        logger.info(f"设置car mode: {mode}")
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', mode)

    @allure.title("获取&通知拔枪充电口盖自动关闭充电口盖时间信息")
    @pytest.mark.sanity
    def test_caseid_1988979(self):
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'SetClsChargeLidTiSts', 200)
        sleep(2)
        self.restart_bgm_and_connect_service(CHARGELID_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetGunPullOutChargeLidCloseTimeInfo", {},
                                              {"out": {"closeTimeValue": 65535}}, timeout=3) 
        self.ipdu.resume_all_bus_send()
        sleep(2)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetGunPullOutChargeLidCloseTimeInfo", {},
                                              {"out": {"closeTimeValue": 65535}}, timeout=3) # 偏差接受 信号上来后映射默认值无event
        self.partner.empty_all()
        for sts in [0, 1, 120, 121, 255]:
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'SetClsChargeLidTiSts', sts)
            if sts <= 120:
                self.partner.ck_event_and_resp(CHARGELID_SERVICE_CLIENT, "GunPullOutChargeLidCloseTimeInfo",
                                            {"closeTimeInfo": {"closeTimeValue": sts}})  
            else:
                self.partner.ck_no_event_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GunPullOutChargeLidCloseTimeInfo",
                                            {"closeTimeInfo": {"closeTimeValue": sts}})            
        
    @allure.title("获取充电口盖当前状态&通知充电口盖当前状态")
    @pytest.mark.sanity
    def test_caseid_1981079(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 1)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "Status",
                                  {"sts": 0})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                              {"out": 0})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 2)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "Status",
                                  {"sts": 2})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                              {"out": 2})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 0)
        self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "Status",
                                  {"sts": 7})
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                              {"out": 7})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 3)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                              {"out": 7})

    @allure.title("获取充电口盖当前状态&通知充电口盖当前状态_默认值")  #重启后信号恢复拿不到event
    @pytest.mark.full
    def test_caseid_1981080(self):
        self.partner.send_method_request(CHARGELID_SERVICE_CLIENT, "GetStatus", {})
        sleep(1)
        for sts in [1, 0]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', sts)
            self.partner.empty_all(0.5)
            self.restart_bgm_and_connect_service(CHARGELID_SERVICE_CLIENT, resume_all_bus=False)
            sleep(15)
            self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                                    {"out": 7})
            self.ipdu.resume_all_bus_send()
            if sts in [1]:
                self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "Status",
                                            {"sts": 0})
                self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                                        {"out": 0})
            else:
                self.partner.ck_s2s_event(CHARGELID_SERVICE_CLIENT, "Status",
                                            {"sts": 7})
                self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                                        {"out": 7})

    @allure.title("获取充电口盖当前状态_默认值无Last Value")
    @pytest.mark.full
    def test_caseid_1981120(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 2)
        self.partner.ck_coming_event(CHARGELID_SERVICE_CLIENT, "Status",
                                            {"sts": 2})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr09, 'ChrgLidRearSts', 3)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                              {"out": 2})
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(CHARGELID_SERVICE_CLIENT)
        sleep(5)
        self.partner.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "GetStatus", {},
                                              {"out": 7})
