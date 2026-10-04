#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Window.py
@Time         :2023/04/08 17:20:31
@Author       :tao.cheng_ext@jiduauto.com
@Description : Test SOA for WTIService_Window
"""

import random
import allure
import pytest
import copy
from time import sleep
from random import randint
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.test_base import TestBase


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIService_Window")
class TestWTIService_Window(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("WTIService", "client"),("ClimateControlService", "client"),])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        sleep(1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
    
    def window_fault(self,A,B,C,D):
        """主驾 副驾 后左 后右  1代表有故障 0代表无故障"""
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'WinFailrStsAtDrvr', A)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinFailrStsAtPass', B)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinFailrStsAtReLe', C)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinFailrStsAtReRi', D)
        sleep(1)

    def window_heat(self,A,B,C,D):
        """主驾 副驾 后左 后右  1代表电机过热 0代表正常"""
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'WinThermlStsAtDrvr', A)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinThermlStsAtPass', B)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinThermlStsAtReLe', C)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinThermlStsAtReRi', D)
        sleep(1)
        
    @allure.title("遍历_主/副/后排左/后排右车窗故障信息") 
    @pytest.mark.sanity
    def test_caseid_1979969(self):
        info = {1:"1", 0:"0"}
        self.window_fault(0,0,0,0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Right Window Failure", "info": "0"},
                                                        {"name":"Rear Left Window Failure", "info": "0"},{"name":"Driver Window Failure", "info": "0"},
                                                        {"name":"Passenger Window Failure", "info": "0"}]})
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'WinFailrStsAtDrvr', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Driver Window Failure", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Driver Window Failure", "info": value}]})
        #副驾
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinFailrStsAtPass', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Passenger Window Failure", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Passenger Window Failure", "info": value}]})
        #左后
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, 'WinFailrStsAtReLe', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Rear Left Window Failure", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Left Window Failure", "info": value}]})
        #右后
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, 'WinFailrStsAtReRi', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Rear Right Window Failure", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Right Window Failure", "info": value}]})
        #全部有故障
        self.window_fault(1,1,1,1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Right Window Failure", "info": "1"},
                                                        {"name":"Rear Left Window Failure", "info": "1"},{"name":"Driver Window Failure", "info": "1"},
                                                        {"name":"Passenger Window Failure", "info": "1"}]})
        
    @allure.title("遍历_主/副/后排左/后排右车窗电机过热") 
    @pytest.mark.sanity
    def test_caseid_1979975(self):
        info = {1:"1", 0:"0"}
        self.window_fault(1,1,1,1)
        self.window_heat(0,0,0,0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Right Window Motor Overheating", "info": "0"},
                                                        {"name":"Rear Left Window Motor Overheating", "info": "0"},{"name":"Driver Window Motor Overheating", "info": "0"},
                                                        {"name":"Passenger Window Motor Overheating", "info": "0"}]})
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr03, 'WinThermlStsAtDrvr', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Driver Window Motor Overheating", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Driver Window Motor Overheating", "info": value}]})
        #副驾
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.PdmBodyFr03, 'WinThermlStsAtPass', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Passenger Window Motor Overheating", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Passenger Window Motor Overheating", "info": value}]})
        #左后
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'WinThermlStsAtReLe', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Rear Left Window Motor Overheating", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Left Window Motor Overheating", "info": value}]})
        #右后
        for key,value in info.items():
            self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'WinThermlStsAtReRi', key)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Rear Right Window Motor Overheating", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Right Window Motor Overheating", "info": value}]})
        #全部有故障
        self.window_heat(1,1,1,1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Rear Right Window Motor Overheating", "info": "1"},
                                                        {"name":"Rear Left Window Motor Overheating", "info": "1"},{"name":"Driver Window Motor Overheating", "info": "1"},
                                                        {"name":"Passenger Window Motor Overheating", "info": "1"}]})
