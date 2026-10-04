#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Tailgate.py
@Time         :2023/04/08 17:20:31
@Author       :tao.cheng_ext@jiduauto.com
@Description : Test SOA for WTIService_Tailgate
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
@allure.story("WTI通知/WTIService_Tailgate")
class TestWTIService_Tailgate(TestBase):
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

    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', X)
        sleep(1)
           
    @allure.title("遍历_尾门开报警信息") 
    @pytest.mark.sanity
    def test_caseid_1979968(self):
        self.io.trunk_door_close()
        self.partner.empty_all(0.5)
        #P挡下开尾门
        self.io.trunk_door_open()
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Tail", "info": "4"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Tail", "info": "4"}]})
        #N挡下开尾门
        self.Shift_Gear(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Tail", "info": "4"}]})
        #先开尾门再挂D挡
        self.sd_tester.change_usage_mode(13)
        self.Shift_Gear(3)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Tail", "info": "5"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Tail", "info": "5"}]})
        #先挂D挡再关尾门
        self.io.trunk_door_close()
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Tail", "info": "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Tail", "info": "0"}]})
        #先挂D挡再开尾门
        self.io.trunk_door_open()
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Tail", "info": "5"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Tail", "info": "5"}]})
        #尾门打开下切N挡
        self.Shift_Gear(2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Tail", "info": "4"}]})
        #尾门打开下切R挡
        self.Shift_Gear(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Tail", "info": "5"}]})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Tail", "info": "5"}]})