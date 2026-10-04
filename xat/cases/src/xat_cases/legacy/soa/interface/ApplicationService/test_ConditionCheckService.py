# -*- coding: utf-8 -*-
"""
@File        : test_service.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/06/5 18:00 PM
@Description : Test SOA for ConditionCheckService
"""

import random
import os
import sys
import allure
import pytest
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
sys.path.append(os.path.join(os.getcwd(), "../../../.."))
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.driver.ssh_interface import command_send

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger

partner = None
sd_test = None
COCKPITPERCEPTION_SERVICE_CLIENT = "cockpit_perception_service_server"

@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("BGM应用/ConditionCheckService")
class TestConditionCheckService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("ConditionCheckService", "client"),
            ("cockpit_perception_service","server"),
            ("InteractiveService","server"),
            ("HighVoltageService", "client"),
            ("VehicleModeService", "client"),
            ("SeatService", "client"),
            ("ChassisService", "client")])
        self.partner.method_default_timeout = 3
        self.sd_tester.tester_present()
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        sleep(1)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                             {"isOpen": False},timeout=3)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)
    
    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', X)
        sleep(1)

    def set_gear_P_speed_0(self):
        '''P档 车速为0'''
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd',  0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',  0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)

    def five_door_open(self):
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.io.rire_door_open()
        self.io.lere_door_open()
        self.io.trunk_door_open()

    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()

    def set_four_seat_occupt(self,A,B,C,D):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        sleep(1)
    
    def seat_belt_status(self,A,B,C,D,E):
        """设置主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSt1', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSt1', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSt1', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)

    @allure.title("获取和通知功能可用状态列表_遍历_退出低压延时状态条件判断_计时器内跳变")
    @pytest.mark.sanity
    def test_caseid_1985190(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        sleep(5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        sleep(4)
        self.partner.ck_no_specific_event(HIGHVOLTAGE_SERVICE_CLIENT,"FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','DCDCSts']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        sleep(5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','DCDCSts']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': False,
                                                                'failedKeys': ['','DCDCSts']}]})
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})
        self.sd_tester.change_usage_mode(0)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        sleep(5)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        sleep(1)
        self.sd_tester.change_usage_mode(0)
        sleep(4)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        sleep(5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','LVRelaySts']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': False,
                                                                'failedKeys': ['','LVRelaySts']}]})
        sleep(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})

    @allure.title("获取和通知功能可用状态列表_遍历_退出低压延时状态条件判断")
    @pytest.mark.smoke
    def test_caseid_1985080(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr15, 'RlyPwrDistbnCmd1WdIgnRlyExtCmd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)#需要改回10
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.empty_all(1)
        for HVSOC in [0.0,9.0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', HVSOC) #只能有一个failkey
            sleep(2)#0时有延迟
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','HVSocDisplay']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': False,
                                                                'failedKeys': ['','HVSocDisplay']}]})
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)#需要改回10
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        for usagemode in [0,1,2,11]: #01时可能会上报继电器的failkey
            self.sd_tester.change_usage_mode(13)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','UsageMode']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': False,
                                                                'failedKeys': ['','UsageMode']}]})
            self.sd_tester.change_usage_mode(usagemode)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 5.0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','HVSocDisplay']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': False,
                                                                'failedKeys': ['','HVSocDisplay']}]})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        sleep(5)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})
        sleep(5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','DCDCSts']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': False,
                                                                'failedKeys': ['','DCDCSts']}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        self.sd_tester.change_usage_mode(0)
        sleep(5)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})
        sleep(5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': False,'failedKeys': ['','LVRelaySts']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': False,
                                                                'failedKeys': ['','LVRelaySts']}]})
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 41, 'state': True,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 41, 'state': True,
                                                                'failedKeys': ['']}]})

    @allure.title("获取和通知功能可用状态列表_遍历_进入低压延时状态条件判断")
    @pytest.mark.sanity
    def test_caseid_1985079(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 11.0)#需要还原10
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.empty_all(0.5)
        for HVSOC in [0.0,9.0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', HVSOC)
            sleep(2)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 40, 'state': False,'failedKeys': ['','HVSocDisplay']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 40, 'state': False,
                                                                'failedKeys': ['','HVSocDisplay']}]})
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 11.0)#需要还原10
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 40, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 40, 'state': True,
                                                                'failedKeys': ['']}]})
        self.partner.empty_all(0.5)
        for usagemode in [0,2,11,13]:
            self.sd_tester.change_usage_mode(usagemode)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 40, 'state': False,'failedKeys': ['','UsageMode']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 40, 'state': False,
                                                                'failedKeys': ['','UsageMode']}]})
            self.partner.empty_all(0.5)
            self.sd_tester.change_usage_mode(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 40, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 40, 'state': True,
                                                                'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 40, 'state': True,'failedKeys': ['']}]})
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 40, 'state': False,'failedKeys': ['','UsageMode','HVSocDisplay']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 40, 'state': False,
                                                                'failedKeys': ['','UsageMode','HVSocDisplay']}]})#不能有其他的failkey
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.sd_tester.change_usage_mode(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 40, 'state': True,'failedKeys': ['']}]})
        
    @allure.title("获取和通知功能可用状态列表_维持上电模式条件判断_定时器不可受其他failkey打断")
    @pytest.mark.full
    def test_caseid_1988650(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.set_gear_P_speed_0()
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.0)
        self.sd_tester.change_car_mode(1)
        self.partner.empty_all(1)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','DCDCSts']}]}, timeout=8)
        
    @allure.title("获取和通知功能可用状态列表_维持上电模式条件判断_新增条件2")
    @pytest.mark.sanity
    def test_caseid_1985828(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.set_gear_P_speed_0()
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','DCDCSts']}]}, timeout=11)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]}, timeout=1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        sleep(5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        sleep(2)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        sleep(3)
        self.partner.ck_no_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged")
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','DCDCSts']}]}, timeout=8)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.sd_tester.change_car_mode(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd',  1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',  2)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,
                                                'failedKeys': ['','DCDCSts','CarMode','HVSocDisplay','Gear']}]}, timeout=11)
        
    @allure.title("获取和通知功能可用状态列表_维持上电模式条件判断_新增条件")
    @pytest.mark.sanity
    def test_caseid_1985827(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.set_gear_P_speed_0()
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 19.4)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay']}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.5)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]}, timeout=1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay']}]},timeout=2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]}, timeout=1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.ck_coming_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay']}]}, timeout=1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(3)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})

    @allure.title("否定条件有时间判断的_重启前后直接否定的表现")
    @pytest.mark.sanity
    def test_caseid_1987653(self):
        self.set_gear_P_speed_0()
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_usage_mode(0)
        self.partner.empty_all(0.5)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)#需要延时10s
        sleep(1)
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','DCDCSts']}]},timeout=5)
        
    @allure.title("获取和通知功能可用状态列表_遍历_维持上电模式条件判断")
    @pytest.mark.smoke
    def test_caseid_1985078(self):
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.set_gear_P_speed_0()
        self.partner.empty_all(0.5)
        for HVSOC in [0.0,19.0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', HVSOC)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay']}]},timeout=3) #信号为0时有1.5S延时
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','HVSocDisplay']}]})
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 20.0)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 24)
        sleep(1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                    {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay']}]})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 15)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})
        for gear in [1,2,3]:
            self.Shift_Gear(gear)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','Gear']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','Gear']}]})
            self.Shift_Gear(0)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
        for carmode in [1,2,3,5]:
            self.sd_tester.change_car_mode(carmode)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','CarMode']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','CarMode']}]})
            self.sd_tester.change_car_mode(0)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
        for dcdc in [0,1]:
            self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
            self.partner.empty_all(8)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','DCDCSts']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','DCDCSts']}]})
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0)
        self.sd_tester.change_car_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.Shift_Gear(2)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','CarMode','Gear','HVSocDisplay']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','CarMode','Gear','HVSocDisplay']}]})
        sleep(10)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': False,'failedKeys': ['','DCDCSts','CarMode','Gear','HVSocDisplay']}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        self.sd_tester.change_car_mode(0)
        self.Shift_Gear(0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                       {"infos": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 35, 'state': True,'failedKeys': ['']}]})

    @allure.title("获取和通知功能可用状态列表_遍历_退出维持上电模式后上锁条件判断")
    @pytest.mark.sanity
    def test_caseid_1983205(self):
        self.five_door_open()
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                        {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.set_gear_P_speed_0()
        self.partner.empty_all(3)#3S后判断无人
        #5座占位
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': False,
                                                            'failedKeys': ['','SeatOccupied']}]})
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)##5座不占位
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=3)#座椅服务需求改动
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': True,
                                                            'failedKeys': ['']}]})
        for carmode1 in [0,1,2,5]:
            self.sd_tester.change_car_mode(3)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['CarMode']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': False,
                                                            'failedKeys': ['','CarMode']}]})
            self.sd_tester.change_car_mode(carmode1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]})
        self.sd_tester.change_usage_mode(13)
        for gear in [1,2,3]:
            self.Shift_Gear(gear)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','Gear']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': False,
                                                            'failedKeys': ['','Gear']}]})
            self.Shift_Gear(0)
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]})

    @allure.title("获取和通知功能可用状态列表_仅视觉有人_退出维持上电模式后上锁条件判断")
    @pytest.mark.full
    def test_caseid_1988985(self):
        self.five_door_open()  
        self.io.driver_seat_notpresent()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                        {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.set_gear_P_speed_0()
        self.seat_belt_status(0,0,0,0,0)
        self.partner.empty_all(3)#3S后判断无人
        #5座占位
        self.io.driver_seat_present()
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True,"userInVehicleStatusWithCam":True}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': False,
                                                            'failedKeys': ['','SeatOccupied']}]})
        self.io.driver_seat_notpresent()
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=4)#融合感知需要3S校验时间
        self.partner.empty_all(1)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                        {"firstLeftExist":True,"firstRightExist":False,"errorCode":0}})

        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":True}})
        self.partner.ck_no_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged")
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': True,'failedKeys': ['']}]})
        self.partner.empty_all(1)
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                        {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.partner.empty_all()
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":False,"userInVehicleStatusWithCam":False}})
        self.partner.ck_no_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged")
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': True,'failedKeys': ['']}]})

    @allure.title("获取和通知功能可用状态列表_儿童座有人_退出维持上电模式后上锁条件判断")
    @pytest.mark.sanity
    def test_caseid_1988898(self):
        self.five_door_open()  
        self.io.driver_seat_notpresent()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.partner.send_event_notify(COCKPITPERCEPTION_SERVICE_CLIENT, "VehicleInsidePersonExistSts", {"existSts":
                                        {"firstLeftExist":False,"firstRightExist":False,"errorCode":0}})
        self.set_four_seat_occupt(0,0,0,0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.0)
        self.set_gear_P_speed_0()
        self.seat_belt_status(0,0,0,0,0)
        self.partner.empty_all(3)#3S后判断无人
        #5座占位
        self.io.driver_seat_present()
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "VehicleInsidePersonSts",
                                    {"personSts":{"userInVehicleStatus":True,"userInVehicleStatusWithCam":True}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': False,
                                                            'failedKeys': ['','SeatOccupied']}]})
        self.io.driver_seat_notpresent()
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=4)#融合感知需要3S校验时间
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 39, 'state': True,
                                                            'failedKeys': ['']}]})
        self.partner.empty_all()
        self.set_four_seat_occupt(1,0,0,0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.empty_all()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=4)#融合感知需要3S校验时间
        self.partner.empty_all()
        self.set_four_seat_occupt(0,1,0,0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.empty_all()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=4)#融合感知需要3S校验时间
        self.partner.empty_all()
        self.set_four_seat_occupt(0,0,1,0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.empty_all()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=4)#融合感知需要3S校验时间
        self.partner.empty_all()
        self.set_four_seat_occupt(0,0,0,1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.empty_all()
        self.set_four_seat_occupt(0,0,0,0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=4)#融合感知需要3S校验时间
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":True,"occupySts":True}}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': False,
                                                                'failedKeys': ['','SeatOccupied']}]})
        self.partner.empty_all()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "ChildSeatSts",
                                        {"seatSts":{"seatStsSecondLeft":{"installSts":False,"occupySts":False},
                                                    "seatStsSecondRight":{"installSts":False,"occupySts":False}}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 39, 'state': True,
                                                                'failedKeys': ['']}]},timeout=4)#融合感知需要3S校验时间

    @allure.title("获取和通知功能可用状态列表_遍历_舒享模式条件判断")
    @pytest.mark.sanity
    def test_caseid_1980581(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        #表显soc大于20%
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.Shift_Gear(0) #P档
        self.partner.empty_all(0.5)
        for SOC in [10.0,0.0,19.0]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', SOC)
            sleep(0.5) #表显SOC小于20
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','HVSocDisplay']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': False,
                                                            'failedKeys': ['','HVSocDisplay']}]})
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
            sleep(0.5)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
        for carmode1 in [1,2,3,5]:
            logger.info(f"切换车辆模式为{carmode1}")
            self.sd_tester.change_car_mode(carmode1)
            sleep(0.5) #车辆模式不为narmal
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','CarMode']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': False,
                                                            'failedKeys': ['','CarMode']}]})
            self.sd_tester.change_car_mode(0)
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': True,
                                                            'failedKeys': ['']}]})
        self.sd_tester.change_usage_mode(13)
        for gear in [1,2,3]:
            logger.info(f"切换档位为{gear}")
            self.Shift_Gear(gear)
            sleep(0.5) #车辆模式不为narmal
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','Gear']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': False,
                                                            'failedKeys': ['','Gear']}]})
            self.Shift_Gear(0)
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': True,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': True,
                                                            'failedKeys': ['']}]})
        
    @allure.title("获取功能可用状态列表_运动模式功能不可用条件判断_所有信号不满足")
    @pytest.mark.sanity
    def test_caseid_1980290(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 1)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        sleep(0.5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 23, 'state': True,
                                                                'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 23, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', 2)

    @allure.title("获取功能可用状态列表_运动模式功能不可用条件判断_SteerErrReq信号不满足")
    @pytest.mark.full
    def test_caseid_106987(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        sleep(0.5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 23, 'state': True,
                                                                'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 23, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', 2)

    @allure.title("获取功能可用状态列表_牵引模式功能退出条件判断（按键置灰条件）_车速不满足_1703490")
    @pytest.mark.sanity
    def test_caseid_107033(self):
        DISPLAYSOC1=4/(1.05*3.06)
        DISPLAYSOC2=2/(1.05*3.6)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.Shift_Gear(2)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 6, 'state': True,
                                                        'failedKeys': ['']}]})
        logger.info(f"表显车速理论大于3km实际{DISPLAYSOC1}")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', DISPLAYSOC1)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 6, 'state': False,'failedKeys': ['', 'Speed']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 6, 'state': False,'failedKeys': ['', 'Speed']}]})
        self.partner.empty_all(0.5)
        logger.info(f"表显车速理论3km实际{DISPLAYSOC2}")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', DISPLAYSOC2)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 6, 'state': True,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 6, 'state': True,'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        sleep(1)
        
    @allure.title("单踏板模式故障退出条件判断_条件满足_800v")
    @pytest.mark.sanity
    def test_caseid_1987950(self):
        self.sd_tester.write_single_ccp(962,2) #800V
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'CrpVehSpdAct', 0)  
        sleep(3)
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        sleep(1)
        for  guzhang in [0,1,3]:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1',11)
            sleep(1)
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEPedalConfig", {"ePedalconfig": 1},timeout=3)
            self.partner.empty_all(2)
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetEPedalConfig", {}, {"out": 1}) #打开踏板模式
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', 2) 
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1',3)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'CrpVehSpdAct', 7)  
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 30, 'state': True,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 30, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetEPedalConfig", {}, {"out": 0})
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', guzhang)
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 30, 'state': False,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 30, 'state': False,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetEPedalConfig", {}, {"out": 0})

    @allure.title("单踏板模式故障退出条件判断_条件满足_400v")
    @pytest.mark.sanity
    def test_caseid_1987949(self):
        self.sd_tester.write_single_ccp(962,0) #400V
        sleep(3)
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        sleep(1)
        for  guzhang in [0,1,3]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr20, 'EgyRgnLvlAct', 2)
            sleep(1)
            self.partner.send_method_request(HIGHVOLTAGE_SERVICE_CLIENT, "SetEPedalConfig", {"ePedalconfig": 1},timeout=3)
            self.partner.empty_all(2)
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetEPedalConfig", {}, {"out": 1}) #打开踏板模式
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', 2) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr20, 'EgyRgnLvlAct', 0) #回一个能量等级
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 30, 'state': True,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 30, 'state': True,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetEPedalConfig", {}, {"out": 0})
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', guzhang)
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 30, 'state': False,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 30, 'state': False,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetEPedalConfig", {}, {"out": 0})

    @allure.title("获取功能可用状态列表_滑行模式开关不可用条件判断_使用者模式错误_Inactive")
    @pytest.mark.full
    def test_caseid_107019(self):
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 9, 'state': False,
                                                        'failedKeys': ['', "UsageMode"]}]})
        
    @allure.title("获取功能可用状态列表_滑行模式开关不可用条件判断_车辆模式错误")
    @pytest.mark.full
    def test_caseid_1988795(self):
        self.sd_tester.change_usage_mode(2)
        for carmode1 in [0,3,5]:
            self.sd_tester.change_car_mode(carmode1)
            self.partner.empty_all(1)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 9, 'state': True,'failedKeys': ['']}]})
            for carmode2 in [1,2]:
                self.sd_tester.change_car_mode(carmode2)
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                            {"infos": [{'functionId': 9, 'state': False,'failedKeys': ['','Carmode']}]})
                self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                        {"out": [{'functionId': 9, 'state': False,
                                                                'failedKeys': ['', "Carmode"]}]})

    @allure.title("功能删除_获取功能可用状态列表_ESC退出条件判断_当条件不满足的情况下不能上报事件及下发信号")
    @pytest.mark.sanity
    def test_caseid_1984051(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEscSportMode", {"mode": {"id": 1, "isOpen": False}})
        sleep(1)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrEscSptModReqdByDrvr', 0)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrPen', 1)
        try:
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 17, 'state': False,
                                                            'failedKeys': ['']}]})
        except Exception :
            assert  True
        else:
            assert  False
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrEscSptModReqdByDrvr', 0)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrPen', 1)

    @allure.title("功能删除_获取功能可用状态列表_ESC退出条件判断_当条件满足的情况下不能上报事件及下发信号")
    @pytest.mark.sanity
    def test_caseid_1984049(self):
        for usagemode in [11,2,1,0]:
            self.sd_tester.change_usage_mode(13)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetEscSportMode", {"mode": {"id": 1, "isOpen": False}})
            sleep(1)
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrEscSptModReqdByDrvr', 0)
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrPen', 1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 3)
            sleep(1)
            self.sd_tester.change_usage_mode(usagemode)
            try:
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 17, 'state': True,'failedKeys': ['']}]})
                self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 17, 'state': True,
                                                                'failedKeys': ['']}]})
            except Exception :
                assert  True
            else:
                assert  False
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrEscSptModReqdByDrvr', 0)
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr14, 'EscSptModReqdByDrvrPen', 1)
        
    @allure.title("运动/标准模式退出到ECO模式条件判断_信号1满足")
    @pytest.mark.full
    def test_caseid_1959627(self):
        def info (Y):
            return 1 if Y ==0  or Y ==1 else 2
        for X in [0,1,2,11,13]:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 1})
            sleep(1)
            self.sd_tester.change_usage_mode(X)
            logger.info(f"---切换模式为{X}")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
            sleep(0.5)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 1)
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 23, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 23, 'state': True,'failedKeys': ['']}]})
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', info(X))

    @allure.title("陡坡缓降退出（kHDCOff）条件判断_HDC使能开关不满足")
    @pytest.mark.full
    def test_caseid_1988798(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0.0)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                        {"out": [{'functionId': 0, 'state': True,'failedKeys': ['']},
                                                {'functionId': 1, 'state': False,'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 0)#开关不满足
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 0, 'state': False,'failedKeys': ['','SwtStsforHillDwnCtrl']},
                                                                {'functionId': 1, 'state': True,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 0, 'state': False,'failedKeys': ['','SwtStsforHillDwnCtrl']},
                                                {'functionId': 1, 'state': True,'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 0, 'state': True,'failedKeys': ['']},
                                                {'functionId': 1, 'state': False,'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("陡坡缓降退出（kHDCOff）条件判断_车辆模式不满足")
    @pytest.mark.full
    def test_caseid_1988823(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0.0)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.empty_all(1)
        for carmode in [0,3,5]:
            for carmode1 in [1,2]:
                self.sd_tester.change_car_mode(carmode)
                self.sd_tester.change_usage_mode(13)
                self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 0, 'state': True,'failedKeys': ['']},
                                                        {'functionId': 1, 'state': False,'failedKeys': ['']}]})
                self.sd_tester.change_usage_mode(1)
                self.sd_tester.change_car_mode(carmode1)
                logger.info(f"---切换模式从{carmode}到{carmode1}")
                sleep(1)
                self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                            {"infos": [{'functionId': 0, 'state': False,'failedKeys': ['','CarMode']},
                                                                        {'functionId': 1, 'state': True,'failedKeys': ['']}]})
                self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
                self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)

    @allure.title("陡坡缓降退出（kHDCOff）条件判断_使用者模式不满足")
    @pytest.mark.full
    def test_caseid_1988797(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0.0)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.empty_all(1)
        for usagemode2 in [13]:
            self.sd_tester.change_usage_mode(usagemode2)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                            {"out": [{'functionId': 0, 'state': True,'failedKeys': ['']},
                                                    {'functionId': 1, 'state': False,'failedKeys': ['']}]})
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
            self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
            sleep(1)
            for usagemode1 in [0,1,2,11]:
                self.sd_tester.change_usage_mode(usagemode1)
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                            {"infos": [{'functionId': 0, 'state': False,'failedKeys': ['','UsageMode']},
                                                                        {'functionId': 1, 'state': True,'failedKeys': ['']}]})
                self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                        {"out": [{'functionId': 0, 'state': False,'failedKeys': ['','UsageMode']},
                                                        {'functionId': 1, 'state': True,'failedKeys': ['']}]})
                self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("陡坡缓降功能（HDC）可用条件判断_车速不满足时不影响HDCOFF条件判断")
    @pytest.mark.full
    def test_caseid_1988796(self):
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetHDC", {"on": True})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 0, 'state': True,'failedKeys': ['']},
                                                       {'functionId': 1, 'state': False,'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 9.0)#使表显车速=35km/h
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 0, 'state': False,'failedKeys': ['','Speed']},
                                                            {'functionId': 1, 'state': False,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 0, 'state': False,'failedKeys': ['','Speed']},
                                                       {'functionId': 1, 'state': False,'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 8.9)#使表显车速刚刚小于35km/h
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 0, 'state': True,'failedKeys': ['']},
                                                            {'functionId': 1, 'state': False,'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 1,timeout=0.5)

    @allure.title("运动/标准模式退出到ECO模式条件判断_信号2满足")
    @pytest.mark.full
    def test_caseid_1959620(self):
        def info (Y):
            return 1 if Y ==0  or Y ==1 else 2
        for X in [0,1,2,11,13]:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 1})
            sleep(1)
            self.sd_tester.change_usage_mode(X)
            logger.info(f"---切换模式为{X}")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
            sleep(0.5)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 23, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 23, 'state': True,'failedKeys': ['']}]})
            self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', info(X))

    @allure.title("运动/标准模式退出到ECO模式条件判断_信号3满足")
    @pytest.mark.full
    def test_caseid_1959630(self):
        def info (Y):
            return 1 if Y ==0  or Y ==1 else 2
        for X in [0,1,2,11,13]:
            self.partner.send_method_request(CHASSIS_SERVICE_CLIENT, "SetTorqueMode", {"mode": 1})
            sleep(1)
            self.sd_tester.change_usage_mode(X)
            logger.info(f"---切换模式为{X}")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
            sleep(0.5)
            for Y in [2,3]:
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
                sleep(0.5)
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', Y)
                sleep(1)
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 23, 'state': True,'failedKeys': ['']}]})
                self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                    {"out": [{'functionId': 23, 'state': True,'failedKeys': ['']}]})
                self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', info(X))

    @allure.title("Conditioncheck服务所有满足false的重启默检查")
    @pytest.mark.sanity
    def test_caseid_1988777(self):
        self.sd_tester.write_single_ccp(502,1) #避免下面futionid为3报false
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)#退出低压延时状态条件判断
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', 1)#单踏板模式故障退出条件判断
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 15)#牵引模式不可用
        self.sd_tester.change_car_mode(1)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)#座椅不可调
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 0)#陡坡缓降功能HDC条件不可用
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 1)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)#运动/标准模式退出到Comfort模式条件判断_可用
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2) #运动模式不可用条件
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 10.0)#滑行模式不可用条件
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1)        
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)#牵引模式进入二次确认条件不满足
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 7)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 1) #赛道模式不满足
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 9.0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0) 
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 0) #维持上电模式条件判断
        self.io.driver_seat_present() #退出维持上电模式后上锁条件判断
        sleep(1)
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                    {"infos": [{'functionId': 20, 'state': False,'failedKeys': ['','PrpsnModSptBlkd','ESCWorkStatus','SteerErrReq']},
                               {'functionId': 9, 'state': False,'failedKeys': ['','UsageMode','Speed','CarMode']},
                               {'functionId': 3, 'state': False,'failedKeys': ['','EPBOperationStatus','CarConfig_501']},
                               {'functionId': 5, 'state': False,'failedKeys': ['','EPBOperationStatus','ChargingIsConnect','BrakerPedalNoFault']},
                               {'functionId': 37, 'state': True,'failedKeys': ['']},#牵引模式功能退出成功条件判断
                               {'functionId': 4, 'state': False,'failedKeys': ['','EPBOperationStatus','UsageMode']},#允许进入牵引模式条件判断
                               {'functionId': 1, 'state': True,'failedKeys': ['']},
                               {'functionId': 7, 'state': True,'failedKeys': ['']},
                               {'functionId': 29, 'state': False,'failedKeys': ['', "DrvrSeatExtAdjAllowd"]},
                               {'functionId': 30, 'state': False,'failedKeys': ['']},#需求没说需要failkey
                               {'functionId': 23, 'state': True,'failedKeys': ['']},#运动/标准模式退出到Comfort模式条件判断
                               {'functionId': 6, 'state': False,'failedKeys': ['','BrakerPedalNoFault','Gear','Speed']},#牵引模式功能退出条件判断（按键置灰条件）
                               {'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay','CarMode','DCDCSts']},
                               {'functionId': 0, 'state': False,'failedKeys': ['','UsageMode','CarMode','SwtStsforHillDwnCtrl','Speed']},
                               {'functionId': 38, 'state': False,'failedKeys': ['','EPBOperationStatus','UsageMode','RestartEntryTowMode']},
                               {'functionId': 39, 'state': False,'failedKeys': ['','SeatOccupied']},
                               {'functionId': 23, 'state': True,'failedKeys': ['']},
                               {'functionId': 41, 'state': False,'failedKeys': ['','DCDCSts','HVSocDisplay']},#低压延时
                               {'functionId': 40, 'state': False,'failedKeys': ['','HVSocDisplay']},#低压延时
                               {'functionId': 26, 'state': False,'failedKeys': ['','ThermalSystemDeviceFault','CarMode','UsageMode','PropulsionStatus','SteerErrReq']}
                                                               ]},timeout=15)#其中有一个dcdc的10S判断

    @allure.title("Conditioncheck服务重启默认值")
    @pytest.mark.sanity
    def test_caseid_1984567(self):
        self.sd_tester.write_single_ccp(502,2) #避免下面futionid为3报false
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr38, 'EPedlDrvrIndcnMsg', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        sleep(1)
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 6, 'state': False,'failedKeys': ['']},
                                                               {'functionId': 1, 'state': True,'failedKeys': ['']},
                                                               {'functionId': 9, 'state': False,'failedKeys': ['','UsageMode']}]},timeout=10)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 20, 'state': True,'failedKeys': ['']}]},timeout=3)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 30, 'state': False,'failedKeys': ['']}]},timeout=3)
        sleep(3)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                            {"infos": [{'functionId': 23, 'state': False,'failedKeys': ['']}]},timeout=3)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 29, 'state': False,'failedKeys': ['',"DrvrSeatExtAdjAllowd"]},
                                                               {'functionId': 37, 'state': True,'failedKeys': ['']},
                                                               {'functionId': 4, 'state': False,'failedKeys': ['']},
                                                               {'functionId': 3, 'state': True,'failedKeys': ['']},
                                                               {'functionId': 35, 'state': False,'failedKeys': ['','HVSocDisplay']}]},timeout=3)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("赛道模式可操作条件判断_情况满足")
    @pytest.mark.smoke
    def test_caseid_1959507(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 1)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)#防止V2.1的需求导致V2.0测试不过
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                            {"infos": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                            {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})

    @allure.title("赛道模式保持条件判断_情况满足")
    @pytest.mark.sanity
    def test_caseid_1988887(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',3)#D档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                            {"out": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        
    @allure.title("赛道模式保持条件判断_重启后WhlBrkOvrheatd信号未到")
    @pytest.mark.full
    def test_caseid_1988936(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',3)#D档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                            {"out": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        self.ipdu.pause_bus_send("chassiscan2")
        sleep(1)
        self.nucapp.bgm_power_off()
        self.partner.empty_all(2)
        self.nucapp.bgm_power_on()
        sleep(10)   
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','ESCWorkStatusTempError']}]})
        self.ipdu.resume_all_bus_send()
        sleep(1)    
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True ,'failedKeys': ['']}]})

    @allure.title("赛道模式保持条件判断_ESC的遍历情况2")
    @pytest.mark.sanity
    def test_caseid_1988892(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',3)#D档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.empty_all(1)
        for ESC in range(5):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', ESC)
            sleep(0.2)
            for BRK in [1,0]: 
                logger.info(f"发送底盘Esc信号为{ESC}且制动盘信号为{BRK}")
                self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', BRK)
                sleep(0.2)
                if ESC== 2 and BRK ==0:
                    self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','ESCWorkStatusTempError']}]})
                elif ESC== 3 :
                    self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','ESCWorkStatusPermError']}]})
                else:
                    self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 42, 'state': True   ,'failedKeys': ['']}]})
        
    @allure.title("赛道模式保持条件判断_ESC的遍历")
    @pytest.mark.sanity
    def test_caseid_1988891(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',3)#D档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 3)#仅有一个故障
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','ESCWorkStatusPermError']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 42, 'state': False,'failedKeys': ['','ESCWorkStatusPermError']}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','ESCWorkStatusTempError']}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 3)#仅有一个故障
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','ESCWorkStatusPermError']}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 4)
        sleep(0.5)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})

    @allure.title("赛道模式保持条件判断_除开ESC的遍历")
    @pytest.mark.sanity
    def test_caseid_1988890(self):
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn',3)#D档
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.empty_all(1)
        for PT in [7,3,1]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', PT)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','PropulsionStatus']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 42, 'state': False,'failedKeys': ['','PropulsionStatus']}]})
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        for steer in range(1,8):
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', steer)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','SteerErrReq']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 42, 'state': False,'failedKeys': ['','SteerErrReq']}]})
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})
        for THEM in [1,10000,65535]:
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', THEM)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': False,'failedKeys': ['','ThermalSystemDeviceFault']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 42, 'state': False,'failedKeys': ['','ThermalSystemDeviceFault']}]})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 42, 'state': True,'failedKeys': ['']}]})

    @allure.title("赛道模式可操作条件判断_情况不满足_热管理系统故障")
    @pytest.mark.sanity
    def test_caseid_1988460(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                            {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','SteerErrReq','ThermalSystemDeviceFault']}]})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 2)
        self.partner.ck_no_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged")
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','SteerErrReq']}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                        {"infos": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
                
    @allure.title("赛道模式可操作条件判断_任一条件不满足")
    @pytest.mark.sanity
    def test_caseid_1959552(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        sleep(0.5)
        for CARMODE in [1,2,3,5]:
            logger.info(f"--车辆模式切为{CARMODE}")
            self.sd_tester.change_car_mode(0)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
            self.sd_tester.change_car_mode(CARMODE)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','CarMode']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','CarMode']}]})
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()
        for USGMODE in [0,1]:
            logger.info(f"--使用者模式切为{USGMODE}")
            self.sd_tester.change_usage_mode(2)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
            self.sd_tester.change_usage_mode(USGMODE)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','UsageMode']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','UsageMode']}]})
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(11)
        for Gear in [1,2,3]:
            logger.info(f"--档位切为{Gear}")
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', Gear)
            sleep(0.5)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','Gear']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','Gear']}]})
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.partner.empty_all(1)
        for ESCESC in [2,3]:
            logger.info(f"--ESCESC切为{ESCESC}")
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', ESCESC)
            sleep(0.5)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','ESCWorkStatus']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','ESCWorkStatus']}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1)
        self.partner.empty_all(1)
        for QUDONG in [7,3,1]:
            logger.info(f"--QUDONG切为{QUDONG}")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', QUDONG)
            sleep(0.5)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','PropulsionStatus']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','PropulsionStatus']}]})
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr10, 'PTStsForRace', 8)
        self.partner.empty_all(1)
        for zhuanxiang in range(1,8):
            logger.info(f"--STEER切为{zhuanxiang}")
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
            self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', zhuanxiang)
            sleep(0.5)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','SteerErrReq']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','SteerErrReq']}]})
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 1)
        sleep(0.5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','BrakeDiscOverheat']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','BrakeDiscOverheat']}]})
        self.ipdu.set(self.ipdu.chassiscan2.VddmChas2Fr26, 'WhlBrkOvrheatd', 0)
        self.partner.empty_all(1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                            {"out": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3',  random.choice([1, 10000,65535]))
        sleep(0.5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                            {"infos": [{'functionId': 26, 'state': False,'failedKeys': ['','ThermalSystemDeviceFault']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                            {"out": [{'functionId': 26, 'state': False,'failedKeys': ['','ThermalSystemDeviceFault']}]})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr30, 'ResrvdSigForCCM3', 0)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                            {"infos": [{'functionId': 26, 'state': True,'failedKeys': ['']}]})

    @allure.title("获取和通知牵引模式状态_case5_1703537")
    @pytest.mark.sanity
    def test_caseid_106986(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetTowModeStatus", {},
                                              {"out": {'modeExitEnable': {"condition": False}}})

    @allure.title("获取功能可用状态列表_滑行模式开关不可用条件判断_E2E影响_1703531")
    @pytest.mark.full
    def test_caseid_106992(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 9, 'state': True,
                                                        'failedKeys': ['']}]})

    @allure.title("滑行模式开关可用条件判断_遍历")
    @pytest.mark.full
    def test_caseid_107017(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 9, 'state': True,
                                                        'failedKeys': ['']}]})
        for usagemode1 in [0,1]:
            for usagemode2 in [2,11,13]:
                self.sd_tester.change_usage_mode(usagemode1)
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 9, 'state': False,'failedKeys': ['']}]})
                self.partner.empty_all()
                self.sd_tester.change_usage_mode(usagemode2)
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 9, 'state': True,'failedKeys': ['']}]})
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all()
        for CARmode1 in [1,2]:
            for CARmode2 in [0,3,5]:
                self.sd_tester.change_car_mode(CARmode1)
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 9, 'state': False,'failedKeys': ['']}]})
                self.partner.empty_all()
                self.sd_tester.change_car_mode(CARmode2)
                logger.info(f"车辆模式从{CARmode1}切换为{CARmode2}")
                self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 9, 'state': True,'failedKeys': ['']}]})
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all(1)
        for SPEED1 in [0.5,10.0]:
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', SPEED1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                            {"infos": [{'functionId': 9, 'state': False,'failedKeys': ['']}]})
            self.partner.empty_all()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0.0)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                            {"infos": [{'functionId': 9, 'state': True,'failedKeys': ['']}]})

    @allure.title("牵引模式进入二次确认_EPB未夹紧")
    @pytest.mark.full
    def test_caseid_107035(self):
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.write_single_ccp(502, 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'EPBOperationStatus']}]})

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）条件判断_Dyno_1703513")
    def test_caseid_107010(self):
        self.sd_tester.change_car_mode(5)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                          {"out": [{'functionId': 0, 'state': True,
                                                    'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）条件判断_CRASH_1703515")
    @pytest.mark.full
    def test_caseid_107008(self):
        self.sd_tester.change_car_mode(3)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 0, 'state': True,
                                                        'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）条件满足判断")
    @pytest.mark.smoke
    def test_caseid_107040(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 0, 'state': True,
                                                        'failedKeys': ['']}]})

    @allure.title("牵引模式进入二次确认_充电枪不满足")
    @pytest.mark.full
    def test_caseid_106993(self):
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.write_single_ccp(502, 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})

        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'ChargingIsConnect']}]})

        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'ChargingIsConnect']}]})

        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'ChargingIsConnect']}]})

        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 4)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'ChargingIsConnect']}]})

        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 5)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'ChargingIsConnect']}]})

    @allure.title("牵引模式进入二次确认_展车模式已打开")
    @pytest.mark.full
    def test_caseid_107048(self):
        self.sd_tester.write_single_ccp(502, 2)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": True})
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01,
                        'ExhibitionModeStsExhibitionModeSts', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)

        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'ExhibitionMode']}]})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})

    @allure.title("遍历所有使用者模式下打开关闭展车模式")
    @pytest.mark.full
    def test_caseid_1913721(self):
        self.sd_tester.write_single_ccp(502, 2)
        def return_info(value):
            return 1 if value in [0, 1, 2, 11] else 0
        for usgmode in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usgmode)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
            sleep(2)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 0)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                             {"isOpen": True})
            self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01,
                            'ExhibitionModeStsExhibitionModeSts', return_info(usgmode))
            sleep(1)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                             {"isOpen": False})

    @allure.title("展车模式打开后动力禁用")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1703473?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1913725(self):
        self.sd_tester.write_single_ccp(502, 2)
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(2)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": True})
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01,
                        'ExhibitionModeStsExhibitionModeSts', 1)
        sleep(1)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'StartInhibitSts', 1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})

    @allure.title("牵引模式进入二次确认_触发条件")
    @pytest.mark.full
    def test_caseid_107030(self):
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.write_single_ccp(502, 2)
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': True,
                                                        'failedKeys': ['']}]})

    @allure.title("牵引模式进入二次确认_踏板未踩下")
    @pytest.mark.full
    def test_caseid_106988(self):
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.write_single_ccp(502, 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'BrakerPedalStatus']}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 5, 'state': False,
                                                        'failedKeys': ['', 'BrakerPedalNoFault']}]})

    @allure.title("获取功能可用状态列表_允许进入牵引模式条件都不满足判断")
    @pytest.mark.full
    def test_caseid_107014(self):
        for X in [0, 1, 2, 13]:
                self.sd_tester.change_usage_mode(X)
                for Y in list(range(9)) + list(range(10, 15)):
                        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', Y)
                        logger.info(f"{Y}")
                        sleep(1)
                        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                              {"out": [{'functionId': 4, 'state': False,
                                                                        'failedKeys': ['', 'EPBOperationStatus', 'UsageMode']}]})

    @allure.title("获取功能可用状态列表_允许进入牵引模式条件判断_满足")
    @pytest.mark.full
    def test_caseid_107005(self):
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)

        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 4, 'state': True,
                                                        'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_座椅调节前提条件信号不满足判断")
    @pytest.mark.full
    def test_caseid_107036(self):
        #需求有误
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd', 0)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSysStatus", {"seats": [0]},
                                              {"out": [{'id': 0, 'status': {"isExtAdjAllowed": False}}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 29, 'state': False,
                                                        'failedKeys': ['', "DrvrSeatExtAdjAllowd"]}]})

    @allure.title("获取功能可用状态列表_座椅调节前提条件信号满足判断")
    @pytest.mark.full
    def test_caseid_107009(self):
        for X in [1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            logger.info(f"{X}")
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd_0_SmdBodySignalIPdu05', 1)
            sleep(1)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                  {"out": [{'functionId': 29, 'state': True,
                                                            'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_座椅调节前提条件信号使用者模式判断")
    @pytest.mark.full
    def test_caseid_107007(self):
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr05, 'DrvrSeatExtAdjAllowd_0_SmdBodySignalIPdu05', 1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetSeatSysStatus", {"seats": [0]},
                                              {"out": [{'id': 0, 'status': {"isExtAdjAllowed": True}}]})

        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 29, 'state': False,
                                                        'failedKeys': ['', "UsageMode"]}]})

    @allure.title("获取功能可用状态列表_滑行模式开关不可用条件判断_使用者模式错误_abdonded")
    @pytest.mark.full
    def test_caseid_106999(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.sd_tester.change_usage_mode(0)

        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 9, 'state': False,
                                                        'failedKeys': ['', "UsageMode"]}]})

    @allure.title("获取功能可用状态列表_滑行模式开关不可用条件判断_车速影响")
    @pytest.mark.full
    def test_caseid_107042(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 1000)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 9, 'state': False,
                                                        'failedKeys': ['', "Speed"]}]})

    @allure.title("获取功能可用状态列表_牵引模式功能退出成功条件判断_a不满足")#140
    @pytest.mark.full
    def test_caseid_1983353(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                    {"infos": [{'functionId': 37, 'state': False,'failedKeys': ['','EPBOperationStatus']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 37, 'state': False,
                                                        'failedKeys': ['', 'EPBOperationStatus']}]})

    @allure.title("获取功能可用状态列表_牵引模式功能退出成功条件判断_信号遍历满足")
    @pytest.mark.full
    def test_caseid_106996(self):
        self.sd_tester.change_usage_mode(2)
        for X in list(range(9)) + list(range(10, 16)):
                self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', X)
                logger.info(f"{X}")
                sleep(1)
                self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                      {"out": [{'functionId': 37, 'state': True,
                                                                'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_牵引模式功能退出条件判断（按键置灰条件）_踏板未踩下")
    @pytest.mark.full
    def test_caseid_107038(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 6, 'state': False,
                                                        'failedKeys': ['', "BrakerPedalStatus"]}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 1)

        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 6, 'state': False,
                                                        'failedKeys': ['', "BrakerPedalNoFault"]}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 6, 'state': False,
                                                        'failedKeys': ['', "BrakerPedalNoFault"]}]})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 0)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 6, 'state': False,
                                                        'failedKeys': ['', "BrakerPedalNoFault"]}]})
        
    @allure.title("获取功能可用状态列表_牵引模式功能退出条件判断（按键置灰条件）_档位不满足")
    @pytest.mark.smoke
    def test_caseid_1959792_1959648(self):
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        sleep(0.5)
        for Gear in [0,1,3]:
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 6, 'state': True,
                                                            'failedKeys': ['']}]})
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', Gear)
            sleep(0.5)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged",
                                                {"infos": [{'functionId': 6, 'state': False,
                                                            'failedKeys': ['']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 6, 'state': False,
                                                            'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_运动模式功能不可用条件判断_多信号不满足")
    @pytest.mark.full
    def test_caseid_107013(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 23, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.chassiscan1.BgmChas1Fr02, 'TqModReq', 2)

    @allure.title("获取功能可用状态列表_运动模式功能可用条件判断")
    @pytest.mark.full
    def test_caseid_107020(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 20, 'state': True,
                                                        'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）不可用条件判断_使用者模式为11active")
    @pytest.mark.full
    def test_caseid_107043(self):
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 1, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("获取功能可用状态列表_牵引模式可用条件判断-EpbStsEpbSts=15不满足")
    @pytest.mark.full
    def test_caseid_107022(self):
        self.sd_tester.write_single_ccp(502, 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 15)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 3, 'state': False,
                                                        'failedKeys': ['', "EPBOperationStatus"]}]})

    @allure.title("获取功能可用状态列表_牵引模式可用条件判断-信号值遍历")
    @pytest.mark.full
    def test_caseid_107006(self):
        self.sd_tester.write_single_ccp(502, 2)
        for X in range(15):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', X)
            logger.info(f"{X}")
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                  {"out": [{'functionId': 3, 'state': True,
                                                            'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_设置牵引模式确认case1")
    @pytest.mark.smoke
    def test_caseid_107000(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.sd_tester.enter_default_session()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        sleep(1)
        # self.dk.set_cenlock_sts(3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        sleep(1)
        # self.dk.reset_bncm_digital_keyinfo()
        # self.dk.set_internal_has_key()
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True}, timeout=0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 11)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'EpbSoftSwtCtrlSt', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 3}})

    @allure.title("获取功能可用状态列表_设置牵引模式确认case2")
    @pytest.mark.sanity
    def test_caseid_107031(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.sd_tester.enter_default_session()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.five_door_close()  # 设置bodycan上五个电动门均关闭
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeUp", {"mode": 11})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 13)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(1)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True}, timeout=1)
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'EpbSoftSwtCtrlSt', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 3}})

    @allure.title("获取功能可用状态列表_设置牵引模式确认case3")
    @pytest.mark.smoke
    def test_caseid_107045(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 2)
        self.sd_tester.enter_default_session()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.five_door_close()  # 设置bodycan上五个电动门均关闭
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeUp", {"mode": 11})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 11)

        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'EpbSoftSwtCtrlSt', 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)

        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 3}})
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": False})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'EpbSoftSwtCtrlSt', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)

    @allure.title("获取功能可用状态列表_设置牵引模式确认关闭_case1&case6&case8&case9")
    @pytest.mark.sanity
    def test_caseid_107025(self):
        self.sd_tester.enter_default_session()
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.five_door_close()  # 设置bodycan上五个电动门均关闭
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 3)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 2})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 4)
        sleep(0.5)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'EpbSoftSwtCtrlSt', 2) #放前面先校验epb释放
        sleep(0.5)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02,
                        'VehModMngtGlbSafe1UsgModSts', 11)

        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(2)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": False})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'EpbSoftSwtCtrlSt', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)

        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 6}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 1}})


    @allure.title("获取功能可用状态列表_运动模式功能不可用条件判断_EscStEscSt信号不满足")
    @pytest.mark.full
    def test_caseid_107047(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 3)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 20, 'state': False,
                                                        'failedKeys': ['', 'ESCWorkStatus']}]})

    @allure.title("获取功能可用状态列表_运动模式功能不可用条件判断_EscStEscSt信号不满足")
    @pytest.mark.full
    def test_caseid_107041(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 20, 'state': False,
                                                        'failedKeys': ['', 'ESCWorkStatus']}]})

    @allure.title("获取功能可用状态列表_运动模式功能不可用条件判断_PrpsnModSptBlkd信号不满足")
    @pytest.mark.full
    def test_caseid_107028(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 1)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 20, 'state': False,
                                                        'failedKeys': ['', 'PrpsnModSptBlkd']}]})

    @allure.title("获取和通知牵引模式状态_case4")
    @pytest.mark.sanity
    def test_caseid_106989(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True})
        sleep(3)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT,
                                              "GetTowModeStatus", {},  {"out": {"sts": 1}})

    @allure.title("运动/标准模式退出到ECO模式条件判断_全部不满足")
    @pytest.mark.full
    def test_caseid_107018(self):
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr18, 'PrpsnModSptBlkd', 0)
        self.ipdu.set(self.ipdu.chassiscan1.PscmChas1Fr03, 'SteerErrReq', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, 'EscStEscSt', 0)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 23, 'state': False,
                                                        'failedKeys': ['']}]})

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）不可用条件判断_使用者模式为2convenience")
    @pytest.mark.full
    def test_caseid_107016(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 1, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）不可用条件判断_车辆模式和使用者模式不满足")
    @pytest.mark.full
    def test_caseid_107003(self):
        self.sd_tester.change_car_mode(2)
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 1, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）不可用条件判断_车辆模式为FACTORY")
    @pytest.mark.full
    def test_caseid_107029(self):
        self.sd_tester.change_car_mode(2)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 1, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("获取功能可用状态列表_陡坡缓降功能（HDC）不可用条件判断_车辆模式为TRSOPRT")
    @pytest.mark.full
    def test_caseid_107001(self):
        self.sd_tester.change_car_mode(1)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr04, 'SwtStsforHillDwnCtrl', 1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                              {"out": [{'functionId': 1, 'state': True,
                                                        'failedKeys': ['']}]})
        self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr05, 'HillDwnCtrlSt', 0,timeout=0.5)

    @allure.title("获取和通知牵引模式状态_case2")
    @pytest.mark.full
    def test_caseid_107012(self):
        self.sd_tester.write_single_ccp(502, 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})

        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetTowModeStatus", {},
                                              {"out": {'modeConfirmEnable': {"condition": True}}})

    @allure.title("获取和通知牵引模式状态_case3")
    @pytest.mark.full
    def test_caseid_107002(self):
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetTowModeStatus", {},
                                              {"out": {'sts': 2}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetTowModeStatus", {},
                                              {"out": {'sts': 3}})

    @allure.title("获取和通知牵引模式状态_case4")
    @pytest.mark.full
    def test_caseid_106985(self):
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        sleep(2)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetTowModeStatus", {},
                                              {"out": {'sts': 1}})

    @allure.title("获取和通知牵引模式状态_case1")
    @pytest.mark.full
    def test_caseid_107015(self):
        self.sd_tester.write_single_ccp(502, 2)
        for X in range(15):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 15)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', X)
            logger.info(f"{X}")
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus",
                                                  {"info": {"modeEntryEnable": {"condition": True},
                                                           "sts": 1}})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetTowModeStatus", {},
                                                  {"out": {"modeEntryEnable": {"condition": True},
                                                           "sts": 1}})
            
    @allure.title("展车模式打开后重启记忆")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1918678(self):
        self.sd_tester.write_single_ccp(502, 2)
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(2)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": True})
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01,
                        'ExhibitionModeStsExhibitionModeSts', 1)
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        sleep(1)
        self.ipdu.check(self.ipdu.propulsioncan.BgmPropulsionFr01,
                        'ExhibitionModeStsExhibitionModeSts', 1)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetExhibitionModeSts", {},
                                              {"out": {"isOpen": True, "isValid": True}})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False})
        
    @allure.title("获取和通知牵引模式状态_否定赋值")
    @pytest.mark.sanity
    def test_caseid_1960023(self):
        self.sd_tester.write_single_ccp(502, 2)#满足牵引模式可用
        sleep(2)
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": False}, timeout=2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(1)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        sleep(1)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True}, timeout=1)
        logger.info(f"2222222")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 3}})
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 0)
        sleep(0.5)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 0}},timeout=5)#采用event校验
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetTowModeStatus", {},{"out": {"sts": 1}})#牵引模式可用会进入到1的状态
        
    @allure.title("获取和通知牵引模式状态_case10")
    @pytest.mark.sanity
    def test_caseid_1959793(self):
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": False}, timeout=3)#上一个case重启导致超时2S
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(1)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        sleep(1)
        self.partner.send_method_request(CONDITIONCHECK_SERVICE_CLIENT, "SetTowModeConfirm", {"isOn": True}, timeout=3)
        logger.info(f"2222222")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 2}})
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 3}})
        self.restart_bgm_and_connect_service(CONDITIONCHECK_SERVICE_CLIENT)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 9)
        sleep(1)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,"GetEPBOperationStatus",{},{"out":9})
        sleep(1)
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT,
                                              "GetTowModeStatus", {},  {"out": {"sts": 3}})
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "TowModeStatus", {"info": {"sts": 6}})
        
########################################################################################################

@allure.feature("SOA服务接口")
@allure.story("BGM应用/ConditionCheckService")
class TestConditionCheckServiceFota(TestBase):
    
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu, enable_inter_service=True)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        for process_name in ["monitor_em2.sh", "em2", "fota/fota", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(2)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=15)
        self.partner = S2sBaseClass([
            ("ConditionCheckService", "client"),
            ("HighVoltageService", "client"),
            ("VehicleModeService", "client"),
            ("SeatService", "client"),
            ("ChassisService", "client"),
            ("FotaMasterService", "server")])
        self.partner.wait_for_service_reconnect(FOTAMASTER_SERVICE_SERVER)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        self.nucapp.tcam_power_off()
        sleep(2)
        self.nucapp.tcam_power_on()
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        sleep(10)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        
    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', X)
        sleep(1)
        
    def five_door_close(self):
        self.io.pass_door_close()
        self.io.drvr_door_close()
        self.io.lere_door_close()
        self.io.rire_door_close()
        self.io.trunk_door_close()
           
    @allure.title("获取和通知功能可用状态列表_遍历_舒享模式条件判断fota不满足")
    @pytest.mark.sanity
    def test_caseid_1984159(self):
        self.five_door_close()
        self.dk.set_cenlock_sts(1)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)
        #表显soc大于20%
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.Shift_Gear(0) #P档
        self.partner.empty_all(0.5)
        for state in list(range(5)) +list(range(6,11)) +list(range(20,24)):
            logger.info(f"切换master为{state}")
            self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER, "Status",{"status": {"taskId":0, "state":5, "errorCode":0}})
            sleep(0.5) #fotamaster等于update
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': False,
                                                                'failedKeys': ['','FotaStatus']}]})
            self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': False,
                                                            'failedKeys': ['','FotaStatus']}]})
            self.partner.send_event_notify(FOTAMASTER_SERVICE_SERVER, "Status",{"status": {"taskId":0, "state":state, "errorCode":0}})
            sleep(1)
            self.partner.ck_s2s_event(CONDITIONCHECK_SERVICE_CLIENT, "FunctionAvailableChanged", {"infos": [{'functionId': 35, 'state': True,
                                                                'failedKeys': ['']}]})
        self.partner.send_request_and_ck_resp(CONDITIONCHECK_SERVICE_CLIENT, "GetFunctionAvailable", {},
                                                {"out": [{'functionId': 35, 'state': True,
                                                            'failedKeys': ['']}]})



