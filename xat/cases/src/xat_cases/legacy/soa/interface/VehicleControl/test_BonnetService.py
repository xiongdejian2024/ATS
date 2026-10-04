# -*- coding: utf-8 -*-
"""
@File        : test_soa_bonnet.py
@Author      : jishu.duan_ext
@Time        : 2023/05/10 15:00 PM
@Description : Test s2s interface about bonnet function
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

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *

@allure.feature("SOA服务接口")
@allure.story("整车控制/BonnetService")
@pytest.mark.jishu
class TestBonnetService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_tester.tester_present()
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        # 启动partner operator
        self.partner = S2sBaseClass([("BonnetService", "client")])
        self.partner.method_default_timeout = 0.1
        sleep(2)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def boon_all_open_close(self, swith):
        if swith == 0:
            self.io.hood_door1_open()
            self.io.hood_door2_open()
        else:
            self.io.hood_door1_close()
            self.io.hood_door2_open()
        sleep(1)
              
    @allure.title("通知/获取前舱盖状态_一开一开")
    @pytest.mark.smoke
    def test_caseid_1983186(self):
        self.boon_all_open_close(1)
        self.partner.empty_all(1)
        self.boon_all_open_close(0)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'Status',{"sts":0})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 0})
        
    @allure.title("通知/获取前舱盖状态_一开一关")
    @pytest.mark.full
    def test_caseid_1983187(self):
        self.io.hood_door1_close()
        self.io.hood_door2_close()
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'Status',{"sts":0})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 0})
        
    @allure.title("通知/获取前舱盖状态_一关一关")
    @pytest.mark.sanity
    def test_caseid_1983188(self):
        self.boon_all_open_close(0)
        self.partner.empty_all(1)
        self.boon_all_open_close(1)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'Status',{"sts":1})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})
        
    @allure.title("通知/获取前舱盖状态_校验默认值")
    @pytest.mark.full
    def test_caseid_1983190(self): 
        self.boon_all_open_close(1)
        self.partner.empty_all(1)
        self.boon_all_open_close(0)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'Status',{"sts":0})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 0})
        self.restart_bgm_and_connect_service(BOONET_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)  
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 65535})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'Status',{"sts":0})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 0})
        
    @allure.title("通知/获取前舱盖开关状态_一开一开")
    @pytest.mark.smoke
    def test_caseid_1983197(self):
        self.boon_all_open_close(1)
        self.partner.empty_all(1)
        self.boon_all_open_close(0)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus', {"sts": True})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatus', {}, {"out": True})
        
    @allure.title("通知/获取前舱盖开关状态_一开一关")
    @pytest.mark.full
    def test_caseid_1983196(self):
        self.io.hood_door1_close()
        self.io.hood_door2_close()
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus',{"sts": True})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatus', {}, {"out": True})
        
    @allure.title("通知/获取前舱盖开关状态_一关一关")
    @pytest.mark.sanity
    def test_caseid_1983195(self):
        self.boon_all_open_close(0)
        self.partner.empty_all(1)
        self.boon_all_open_close(1)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus', {"sts": False})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatus', {}, {"out": False})
        
    @allure.title("通知/获取前舱盖开关状态_校验默认值")
    @pytest.mark.full
    def test_caseid_1983198(self): 
        self.boon_all_open_close(1)
        self.partner.empty_all(1)
        self.boon_all_open_close(0)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus',{"sts":True})
        self.restart_bgm_and_connect_service(BOONET_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)  
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatus', {}, {"out": False})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus',{"sts":True})
        
    @allure.title("通知/获取前舱盖开关状态(带功能安全)_信号超时或丢失")
    @pytest.mark.full
    def test_caseid_1983201(self):    
        self.boon_all_open_close(1)
        self.partner.empty_all(1)
        self.boon_all_open_close(0)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": True, "validity": 0}})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"value": True, "validity": 0}})
        self.ipdu.pause_bus_send("backbonefr")
        sleep(0.5)
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"value": True, "validity": 0}})
        sleep(1)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": True, "validity": 4}})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"value": True, "validity": 4}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": True, "validity": 0}})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"value": True, "validity": 0}})
           
    @allure.title("通知/获取前舱盖开关状态(带功能安全)_有效")
    @pytest.mark.smoke
    def test_caseid_1983200(self): 
        self.boon_all_open_close(1)
        self.partner.empty_all(1)
        self.boon_all_open_close(0)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": True, "validity": 0}})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"value": True, "validity": 0}})
        sleep(2)  
        
    @allure.title("通知前舱盖开关状态/(带功能安全)_上下电校验event")
    @pytest.mark.sanity
    def test_caseid_1984269(self):
        self.boon_all_open_close(1)
        self.restart_bgm_and_connect_service(BOONET_SERVICE_CLIENT)  
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus',{"sts":False})   
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": False, "validity": 0}}) 
        self.partner.empty_all(1)
        self.boon_all_open_close(0)
        self.restart_bgm_and_connect_service(BOONET_SERVICE_CLIENT)  
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus',{"sts":True})
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": True, "validity": 0}})

@allure.feature("SOA服务接口")    
@allure.story("整车控制/BonnetService")         
class TestDoorServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("BonnetService", "client")])
        sleep(5)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu)            
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)
        sleep(10)
    
    @allure.title("通知/获取前舱盖状态_遍历信号0~3")
    @pytest.mark.full
    def test_caseid_1983194(self):     
        dic = {1 : 0, 0 : 65535, 2 : 1, 3 : 65535}
        for sig, sts in dic.items():
            logger.info(f"当前信号.{sig},当前值.{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', sig)
            sleep(0.5)
            self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'Status',{"sts": sts})
            self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": sts})
            
    @allure.title("通知/获取前舱盖开关状态_遍历信号")
    @pytest.mark.full
    def test_caseid_1983199(self): 
        dic = {1 : True, 0 : "", 2 : False, 3 : ""}
        last = ""
        for sig, sts in dic.items():
            logger.info(f"当前信号.{sig},当前值.{sts}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', sig)
            if sig in [1, 2]:
               self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatus',{"sts": sts})
               self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatus', {}, {"out": sts})
               last = sts
            else:
               self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatus', {}, {"out": last})
                
        
    @allure.title("通知/获取前舱盖开关状态_信号未定义")
    @pytest.mark.full
    def test_caseid_1983202(self):  
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', 2)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', 3)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": False, "validity": 1}})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"value": False, "validity": 1}})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', 2)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HoodSts', 0)
        self.partner.ck_s2s_event(BOONET_SERVICE_CLIENT, 'OpenCloseStatusValidity', {"sts": {"value": False, "validity": 1}})
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetOpenCloseStatusValidity', {}, {"out": {"value": False, "validity": 1}})
        
  