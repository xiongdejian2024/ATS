# -*- coding: utf-8 -*-
"""
@File        : test_soa_horn.py
@Author      : jishu.duan_ext
@Time        : 2023/05/10 15:00 PM
@Description : Test s2s interface about tailwing function
"""

import os
import sys
from time import sleep
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))

import pytest
import allure
from time import sleep
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.sdk.Internal_ETH.tools.bgm_eth_internal import *

@allure.feature("SOA服务接口")
@allure.story("整车控制/HornService")
@pytest.mark.jishu
class TestHornService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("HornService", "client")])
        self.partner.method_default_timeout = 0.1
        self.io_obj = self.io.io_obj
        sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        sleep(0.5)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        
    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    @allure.title("通知/获取喇叭鸣笛状态_开")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1751673?projectId=46')
    @pytest.mark.sanity
    def test_caseid_109414(self):
        self.io_obj.set_do_level("horn_switch", False)
        sleep(1)
        self.io_obj.set_do_level("horn_switch", True)
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0}) 
        self.partner.send_request_and_ck_resp('HornService_client','GetStatus', {},
                                                                       {'out': 0})
        self.io_obj.set_do_level("horn_switch", False)
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1}) 
        self.partner.send_request_and_ck_resp('HornService_client','GetStatus', {},
                                                                       {'out': 1})

            
    @allure.title("通知/获取喇叭鸣笛状态_关")
    @pytest.mark.smoke
    def test_caseid_109413(self):
        self.io_obj.set_do_level("horn_switch", True)
        sleep(0.5)
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0})
        self.partner.send_request_and_ck_resp('HornService_client','GetStatus', {},
                                                                       {'out': 0})
        sleep(1)
        self.io_obj.set_do_level("horn_switch", False)
        sleep(0.5)
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
        self.partner.send_request_and_ck_resp('HornService_client','GetStatus', {},
                                                                       {'out': 1})
        self.partner.empty_all(1)
        self.io_obj.set_do_level("horn_switch", False)
        sleep(0.5)
        self.partner.ck_no_event("HornService_client", "Status")
        self.partner.send_request_and_ck_resp('HornService_client','GetStatus', {},
                                                                       {'out': 1})

    @allure.title("设置喇叭周期性鸣笛_2S开1S关共0次")
    @pytest.mark.full
    def test_caseid_110778(self):
        self.io_obj.set_do_level("horn_switch", False)    
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.io_obj.set_do_level("horn_switch", True)
        sleep(1)
        self.partner.send_method_request("HornService_client", "CyclicActivation", {"onTime": 2000, "offTime": 1000, "actNum": 0})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOnTi", [20])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOffTi", [10])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlNrOfHornActvn", [0])
 
    @allure.title("设置喇叭周期性鸣笛_默认值开默认值关共0次")
    @pytest.mark.full
    def test_caseid_1985985(self):
        self.io_obj.set_do_level("horn_switch", False)    
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.io_obj.set_do_level("horn_switch", True)
        sleep(1)
        self.partner.send_method_request("HornService_client", "CyclicActivation", {"onTime": 25500, "offTime": 25500, "actNum": 255})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOnTi", [255])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOffTi", [255])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlNrOfHornActvn", [255]) 
 
    @allure.title("设置喇叭周期性鸣笛_1S开1S关共5次")
    @pytest.mark.full
    def test_caseid_109431(self):
        self.io_obj.set_do_level("horn_switch", False)    
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.io_obj.set_do_level("horn_switch", True)
        sleep(1)
        self.partner.send_method_request("HornService_client", "CyclicActivation", {"onTime": 1000, "offTime": 1000, "actNum": 5})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOnTi", [10])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOffTi", [10])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlNrOfHornActvn", [5])
                     
    @allure.title("设置喇叭周期性鸣笛_1S开0S关共5次")
    @pytest.mark.sanity
    def test_caseid_110780(self):
        self.io_obj.set_do_level("horn_switch", False)    
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.io_obj.set_do_level("horn_switch", True)
        sleep(1)
        self.partner.send_method_request("HornService_client", "CyclicActivation", {"onTime": 1000, "offTime": 0, "actNum": 5})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOnTi", [10])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlHornOffTi", [0])
        self.bgm_eth_inter.ck_signal_values("HornAdvCtrlNrOfHornActvn", [5])
 
    @allure.title("通知/获取喇叭鸣笛状态_默认值")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1751673?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1984000(self):
        self.io_obj.set_do_level("horn_switch", True)
        sleep(1)
        self.restart_bgm_and_connect_service(HORN_SERVICE_CLIENT)  
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0})
        self.partner.send_request_and_ck_resp('HornService_client','GetStatus', {},
                                                                       {'out': 0})
        self.partner.empty_all(0.5)
        self.io_obj.set_do_level("horn_switch", False)
        sleep(1)
        self.restart_bgm_and_connect_service(HORN_SERVICE_CLIENT)  
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
        self.partner.send_request_and_ck_resp('HornService_client','GetStatus', {},
                                                                       {'out': 1})
