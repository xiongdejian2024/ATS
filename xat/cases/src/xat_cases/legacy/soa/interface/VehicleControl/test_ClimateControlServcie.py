# -*- coding: utf-8 -*-
"""
@File        : test_ClimateControlService.py
@Author      : tao.cheng_ext@jiduatuo.com
@Time        : 2023/10/30 23:00 PM
@Description : Test SOA for ClimateControlService
"""

import os
import sys
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger


@allure.feature("SOA服务接口")
@allure.story("整车控制/ClimateControlServcie")
class TestClimateControlService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([
            ("ClimateControlService", "client"), 
            ("VehicleModeService", "client"), ("SeatService", "client")])
        self.partner.method_default_timeout = 3
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('propulsioncan', 0x516, [0x16, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.sd_tester.tester_present()
        self.sd_tester.write_single_ccp(502, 2)
        sleep(3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        sleep(1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                             {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False}, timeout=1)
        sleep(0.1)

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.seat_belt_status(1, 1, 1, 1, 1)
        self.io.set_four_door_close()
        sleep(1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.state_manual()
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                             {"isOpen": False}, timeout=1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False}, timeout=1)
        sleep(1)
        super().after_each_func(ecu, start=False)
  
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def five_door_open(self):
        self.io.drvr_door_open()
        self.io.pass_door_open()
        self.io.rire_door_open()
        self.io.lere_door_open()
        self.io.trunk_door_open()

    def state_manual(self):
        """设置manual状态机"""
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 3})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 22})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":1})
        sleep(1)

    def state_off_withAuto(self):
        """带auto记忆的auto，实际状态为off"""
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                             {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        # self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": 22.0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 22})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        sleep(1)

    def state_off_withoutAuto(self):
        """没有记忆的auto状态"""
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                             {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 3})
        # self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": 22.0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 22})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        sleep(1)

    def state_Auto(self):
        """设置状态机auto"""
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                             {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        # self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": 22.0})
        
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
        sleep(1)

    def state_Defrost(self):
        """除霜除雾打开"""
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                             {"isOpen": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 22})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":6})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})#设置除霜除雾的接口
        sleep(1)

    def set_four_seat_occupt(self, A, B, C, D, sleeptime=0.5):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        sleep(sleeptime)

    def seat_belt_status(self, A, B, C, D, E):
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
    
    @allure.title("设置空调温度（可以不联动空调）_校验abonded/inactive下的tcpdump")
    @pytest.mark.sanity
    def test_caseid_1979762(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in [0, 1]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": req})
            sleep(1)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmClimaTSetSPHmiCmptmtTSpSpcl", [1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
        self.bgm_eth_inter.ck_signal_values("TelmClimaTSetSPTempRange", [0, 0, 0, 0, 0, 26, 26, 26, 26, 26])
        self.bgm_eth_inter.ck_period_time("TelmClimaTSetSPHmiCmptmtTSpSpcl", 0.1, permit_fail_times=1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in [0, 1]: #打断
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": req})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmClimaTSetSPHmiCmptmtTSpSpcl", [1, 2, 2, 2, 2, 2])
        self.bgm_eth_inter.ck_signal_values("TelmClimaTSetSPTempRange", [0, 26, 26, 26, 26, 26])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("TelmClimaTSetSPTempRange", 0.1, permit_fail_times=1)
        
    @allure.title("200版本_设置座舱通风开启关闭_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1984907(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": req}})
            sleep(1)
        sleep(1)    
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemVentReq", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump() #打断
        for req in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": req}})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemVentReq", [1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump() #500-1000内打断
        for req in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": req}})
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemVentReq", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump() #500ms内发送相同的
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": True}})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": True}})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemVentReq", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("RemVentReq", 0.1)
        
    @allure.title("设置座舱通风开启关闭_下行PDU校验_相同值")
    @pytest.mark.sanity
    def test_caseid_1985262(self):
        self.bgm_eth_inter.start_bgm_tcpdump() #500ms内发送相同的
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": False}})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": False}})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemVentReq", [2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump() #500ms内发送相同的但是type不相同
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": True}})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":1, "isOn": True}})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemVentReq", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])

    @allure.title("设置远程空调上高压_校验下行tcpdump")
    @pytest.mark.sanity
    def test_caseid_1979835(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHV", {"isOn": req, "time": 20})
            sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemStrtHvCtrlReqErsCmd", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHV", {"isOn": req, "time": 20})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemStrtHvCtrlReqErsCmd", [1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("RemStrtHvCtrlReqErsCmd", 0.1)

    @pytest.mark.sanity
    @allure.title("设置空调节能模式_abonded和inactive下的情况")
    def test_caseid_1979767(self):
        def info2(input2):
            return True if input2 == 1 else False
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'EcoClimaSts', 0)
            sleep(0.5)
            for Z in [1, 0]:
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'EcoClimaSts', Z)
                sleep(0.1)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateECOSts", {"sts": info2(Z)})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetEcoMode", {}, {"out": info2(Z)})
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetEcoMode', {"on": req})
            sleep(0.5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("HMIClimaEgySaveReq", [1, 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("HMIClimaEgySaveReq", 0.5)
        
    @pytest.mark.full
    @pytest.mark.jishu3
    @allure.title("v2.2设置空调节能模式_初始化状态重启")
    def test_caseid_1989123(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetEcoMode', {"on": True})
        sleep(3)
        self.del_s2s_db()
        self.kill_s2s_and_reconnect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_ordered_array("HMIClimaEgySaveReq", [1, 0])
        
    @pytest.mark.sanity
    @pytest.mark.jishu3
    @allure.title("v2.2设置空调节能模式_节能模式开启时重启bgm加载记忆值")
    def test_caseid_1989124(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetEcoMode', {"on": True})
        sleep(3)
        self.kill_s2s_and_reconnect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_ordered_array("HMIClimaEgySaveReq", [1])
        
    @pytest.mark.full
    @pytest.mark.jishu3
    @allure.title("v2.2设置空调节能模式_节能模式关闭时重启bgm加载记忆值")
    def test_caseid_1989125(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetEcoMode', {"on": True})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetEcoMode', {"on": False})
        sleep(3)
        self.kill_s2s_and_reconnect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_ordered_array("HMIClimaEgySaveReq", [1,0])       

    @allure.title("设置远程开启空调_下行tcupdump")
    @pytest.mark.sanity
    def test_caseid_1979836(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in ["RemoteOn", "RemoteOff"]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, req, {})
            sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmClimaReqSP", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in ["RemoteOn", "RemoteOff"]: #打断
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, req, {})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmClimaReqSP", [1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("TelmClimaReqSP", 0.1)

    @allure.title("设置远程空调上高压延长时长_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1979838(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHVDelay", {"extendtime": 10})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHVDelay", {"extendtime": 10})
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHVDelay", {"extendtime": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHVDelay", {"extendtime": 30})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemStrtExtnTiReq", [10, 10, 10, 10, 10, 20, 30, 30, 30, 30, 30])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("RemStrtExtnTiReq", 0.1)

    @allure.title("设置远程除霜_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1960053(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmDefrostReq", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time("TelmDefrostReq", 0.1)

    @pytest.mark.sanity
    @allure.title("设置A/C开或关_SetACInhibit打开/关闭的情况")
    def test_caseid_1983206(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":False, "acInhibitSts": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out": {"acStatus":False, "acInhibitSts": True}})
        sleep(3)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out": {"acStatus":True, "acInhibitSts": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        sleep(0.1)
        
    @pytest.mark.sanity
    @allure.title("设置座舱通风开启关闭")
    def test_caseid_1984906(self):
        def info2(input2):
            return 1 if input2 == True else 2
        for input in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": input}})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'RemVentReq', info2(input), timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'RemVentReq', 0, timeout=0.5)
            sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCockpitVent', {"ctrl":{"triggerSrc":0, "isOn": True}})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'RemVentReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'RemVentReq', 0, timeout=0.5)

    @pytest.mark.sanity
    @allure.title("设置空调节能模式_遍历压测10次")
    def test_caseid_1984663(self):
        def info2(input2):
            return 1 if input2 == True else 0
        for times in range(10):
            logger.info(f"第{times}次压测")
            for input in [True, False]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetEcoMode', {"on": input})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'HMIClimaEgySaveReq', info2(input), timeout=0.5)

    @pytest.mark.full
    @allure.title("空调起雾优化_OFF状态机下开关信号=0湿度信号大于85时不会下发循环模式切换")
    def test_caseid_1984088(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 0)
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        
    @pytest.mark.full
    @allure.title("空调起雾优化_启动场景")
    def test_caseid_1987586(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 75) 
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 80)
        sleep(10)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 70) 
        for i in range(5):
            sleep(100)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        sleep(101)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)

    @pytest.mark.full
    @allure.title("空调起雾优化_OFF状态机下湿度信号大于85时下发循环模式自动信号但状态机不变化")
    def test_caseid_1983990(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 1})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)

    @pytest.mark.full
    @allure.title("空调起雾优化_湿度信号大于85时打开了除雾除霜然后再退出除霜除雾的情况")
    @pytest.mark.failed
    def test_caseid_1983991(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 3, timeout=0.5)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        sleep(1)# 退出除霜除雾模式后湿度仍然满足应该置1
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        #开始计时10min
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 86)
        sleep(3)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 71)
        sleep(300)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        sleep(302)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        #再次湿度大于85
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 86)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 74)#再次启动10min计时器
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        sleep(300)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 90)
        sleep(30)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 70)
        sleep(30)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        sleep(241)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)

    @pytest.mark.full
    @allure.title("空调起雾优化_湿度信号大于85时设置Auto然后再退出设置Auto的情况")
    def test_caseid_1983993(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 3, timeout=0.5)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        sleep(1)# 退出Auto后湿度仍然满足应该置1
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        #开始计时10min
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 86)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 74)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 0)
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        
    @pytest.mark.sanity
    @allure.title("获取和通知座舱通风状态")
    def test_caseid_1985217(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentReqRspnFb', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentActvSts', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', 0)
        self.partner.empty_all()
        for sts1 in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentReqRspnFb', sts1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":sts1}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCockpitVentStatus", {}, {"out": {"feedback":sts1}})
        for sts2 in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentActvSts', sts2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"ventSts":sts2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCockpitVentStatus", {}, {"out": {"ventSts":sts2}})
        for sts3 in [1, 0, 2, 3]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', sts3)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"ventWarnSts":sts3}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCockpitVentStatus", {}, {"out": {"ventWarnSts":sts3}})
  
    @pytest.mark.full
    @allure.title("获取和通知座舱通风状态_单个参数触发event")
    def test_caseid_1988784(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentReqRspnFb', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentActvSts', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', 3)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":0,"ventSts":0,"ventWarnSts":3}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', 2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":0,"ventSts":0,"ventWarnSts":2}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":0,"ventSts":0,"ventWarnSts":1}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', 0)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":0,"ventSts":0,"ventWarnSts":0}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentReqRspnFb', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":1,"ventSts":0,"ventWarnSts":0}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentActvSts', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":1,"ventSts":1,"ventWarnSts":0}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentReqRspnFb', 0)  
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":0,"ventSts":1,"ventWarnSts":0}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentActvSts', 0)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", {"vent":{"feedback":0,"ventSts":0,"ventWarnSts":0}})
          
          
          
    @pytest.mark.full
    @allure.title("空调起雾优化_manual状态机下湿度信号大于85时下发循环模式自动信号但状态机不变化")
    def test_caseid_1983999(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 3, timeout=0.5)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 3})
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 3, timeout=0.5)
        sleep(1)# 循环模式设置为2时应该置1
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 1})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 80)
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)

    @pytest.mark.full
    @allure.title("空调起雾优化_发送自动循环模式的过程中ResrvdSigForECM2在70和80之间来回跳变的情况")
    @pytest.mark.failed
    def test_caseid_1983996(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 3, timeout=0.5)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 74)#启动计时器
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        sleep(300)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)#跳变
        sleep(30)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 74)#不会再启动计时器
        sleep(30)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        sleep(242)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)

    @pytest.mark.full
    @allure.title("空调起雾优化_湿度信号大于85时设置主开关OFF然后再设置主开关On情况")
    @pytest.mark.failed
    def test_caseid_1983995(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 3, timeout=0.5)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 0)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        sleep(1)# 主开关打开后湿度仍然满足应该置1
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        #开始计时10min
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 86)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 74)
        sleep(300)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 70) #跳变
        sleep(250)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(55) #10min过后继续保持
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 30) #计时器过后再次触发计时器
        sleep(300)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 90) #跳变
        sleep(250)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 79)
        sleep(55) #10min过后继续保持
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 2, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机除霜除雾换到manual_设置主驾吹风模式为自动下的吹面触发的所有现象")
    def test_caseid_1980081(self):
        for X in [2, 11, 13]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            info ={273:1, 0:0, 546:2, 819:3, 1092:4, 1365:5, 1638:6}
            for key, value in info.items():
                logger.info(f"---信号发送{key}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":7})
                sleep(0.1)
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":7})
                sleep(0.1)
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":7})
                sleep(0.5)
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', key)
                sleep(0.2)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":value, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":value, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":value, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到auto_设置auto打开触发的现象")
    def test_caseid_1980088(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到auto_后排未开启时设置auto打开触发的现象")
    def test_caseid_1980089(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.smoke
    @allure.title("状态机除霜除雾换到auto_设置除雾除霜关闭触发的现象")
    def test_caseid_1980090(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到auto_设置后排温度触发的现象")
    def test_caseid_1980091(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            for Y in [0, 1, 16, 28]:
                logger.info(f"--设置后排温度{Y}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": Y})
                sleep(0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                        "tempDriver": 22, "tempPassenger": 22, "tempSecRow": Y, "windSpeedFirRow": 12, 
                                                        "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                        "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                        "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_打开主开关触发的所有现象")
    def test_caseid_1979984(self):
        self.state_off_withAuto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_打开auto触发的所有现象")
    def test_caseid_1979985(self):
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_inactive下设置主驾温度触发的所有现象")
    def test_caseid_1979986(self):
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 23})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 23, "tempPassenger": 23, "tempSecRow": 23, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_inactive下设置副驾温度触发的所有现象")
    def test_caseid_1979987(self):
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":4, "value": 23})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 23, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_inactive下设置后排温度触发的所有现象")
    def test_caseid_1979988(self):
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": 23})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 23, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.smoke
    @allure.title("状态机除霜除雾换到auto_设置后排On触发的现象")
    def test_caseid_1980092(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 2})
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    # @pytest.mark.sanity
    # @allure.title("逆向测试_状态机除霜除雾换到auto_前排风速为12auto触发的现象")
    # def test_caseid_1980093(self):
    #     for X in [2, 11, 13]:
    #         self.sd_tester.change_usage_mode(X)
    #         self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
    #         sleep(0.5)
    #         self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
    #         sleep(0.5)
    #         self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
    #         sleep(0.5)
    #         self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
    #         sleep(0.5)
    #         self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 12})
    #         sleep(0.5)
    #         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
    #                                                 "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
    #                                                 "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
    #                                                 "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
    #                                                 "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
    #         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
    #         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
    #         self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机除霜除雾换到auto_设置AC关闭触发的现象")
    def test_caseid_1980094(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAC", {}, {"out":True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机除霜除雾换到auto_设置副驾吹面触发的现象")
    def test_caseid_1980095(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":3})
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":3, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机auto换到manual_改变循环模式为0-1触发的所有现象")
    def test_caseid_1980040(self):
        for X in [0, 1]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.2)
            logger.info(f"--循环模式设置为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": X})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_设置后排OFF触发的所有现象")
    def test_caseid_1984903(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 2})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("OFF带auto记忆下_SetACInhibit打开/关闭的情况")
    def test_caseid_1983211(self):
        self.state_off_withAuto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": False, "acInhibitSts":True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        sleep(3)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": False, "acInhibitSts": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": True, "acInhibitSts": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机manual且AC打开切换到auto再到manual__SetACInhibit打开/关闭的情况")
    def test_caseid_1983332(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": False, "acInhibitSts":True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        sleep(3)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": False, "acInhibitSts": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": False, "acInhibitSts": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾到manual再到除霜除雾再到manual_SetACInhibit打开/关闭的情况")
    def test_caseid_1983210(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, "acInhibitSts":True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":
                                                 {"acStatus": False, "acInhibitSts":True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        sleep(3)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":
                                                 {"acStatus": False, "acInhibitSts":False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":
                                                 {"acStatus": True, "acInhibitSts":False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow":6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        

    @pytest.mark.sanity
    @allure.title("状态机auto换到manual再到auto再到manual_由设置AC禁用_触发的所有现象")
    def test_caseid_1984947(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, "acInhibitSts":True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, "acInhibitSts":True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        sleep(3)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, "acInhibitSts":False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, "acInhibitSts":False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})

    @pytest.mark.sanity
    @allure.title("状态机auto换到manual再到auto再到manual_由设置AC禁用_触发的所有现象")
    def test_caseid_1985815(self):
        self.partner.empty_all()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, "acInhibitSts":True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, "acInhibitSts":True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

        
    @pytest.mark.sanity
    @allure.title("验证JBS-23646 短按一下雨刮按键，雨刮刮了两次")
    def test_caseid_1984020(self):
        for i in range (10):
            logger.info(f"第{i}次压测")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntCmptmtTFrnt', 0.0)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntQf', 0)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', 1)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr01, 'IntPm25LvlFrmClima', 1)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdAmbTEstimd', 1)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'IntPm25HiPopUp', 1)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdQf', 1)
            self.partner.send_request_and_return_resp(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                                {"outlets": [{"id": 0, "side": 0, "horizontal": 20, "vertical":100}, 
                                                            {"id": 1, "side": 0, "horizontal": 100, "vertical":60}, 
                                                            {"id": 2, "side": 0, "horizontal": 30, "vertical":100}, 
                                                            {"id": 3, "side": 0, "horizontal": 100, "vertical":40}, 
                                                            {"id": 4, "side": 0, "horizontal": 40, "vertical":100}, 
                                                            {"id": 5, "side": 0, "horizontal": 100, "vertical":100}, 
                                                            {"id": 6, "side": 0, "horizontal": 20, "vertical":30}, 
                                                            {"id": 7, "side": 0, "horizontal": 20, "vertical":100}, 
                                                            {"id": 0, "side": 1, "horizontal": 100, "vertical":100}, 
                                                            {"id": 1, "side": 1, "horizontal": 20, "vertical":100}, 
                                                            {"id": 2, "side": 1, "horizontal": 100, "vertical":70}, 
                                                            {"id": 3, "side": 1, "horizontal": 100, "vertical":100}, 
                                                            {"id": 4, "side": 1, "horizontal": 20, "vertical":100}, 
                                                            {"id": 5, "side": 1, "horizontal": 100, "vertical":90}, 
                                                            {"id": 6, "side": 1, "horizontal": 20, "vertical":100}, 
                                                            {"id": 7, "side": 1, "horizontal": 100, "vertical":100}]})
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', 2)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr01, 'IntPm25LvlFrmClima', 2)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdAmbTEstimd', 2)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'IntPm25HiPopUp', 2)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdQf', 3)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntCmptmtTFrnt', 10.0)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntQf', 0)
            self.state_manual()
            time1=time.time()
            date=self.partner._send_request_and_return_resp_atom(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                                {"outlets": [{"id": 0, "side": 0, "horizontal": 10, "vertical":10}, 
                                                            {"id": 1, "side": 0, "horizontal": 10, "vertical":20}, 
                                                            {"id": 2, "side": 0, "horizontal": 10, "vertical":30}, 
                                                            {"id": 3, "side": 0, "horizontal": 10, "vertical":40}, 
                                                            {"id": 4, "side": 0, "horizontal": 10, "vertical":50}, 
                                                            {"id": 5, "side": 0, "horizontal": 10, "vertical":50}, 
                                                            {"id": 6, "side": 0, "horizontal": 100, "vertical":50}, 
                                                            {"id": 7, "side": 0, "horizontal": 90, "vertical":50}, 
                                                            {"id": 0, "side": 1, "horizontal": 80, "vertical":50}, 
                                                            {"id": 1, "side": 1, "horizontal": 70, "vertical":50}, 
                                                            {"id": 2, "side": 1, "horizontal": 60, "vertical":50}, 
                                                            {"id": 3, "side": 1, "horizontal": 50, "vertical":50}, 
                                                            {"id": 4, "side": 1, "horizontal": 40, "vertical":50}, 
                                                            {"id": 5, "side": 1, "horizontal": 30, "vertical":50}, 
                                                            {"id": 6, "side": 1, "horizontal": 20, "vertical":50}, 
                                                            {"id": 7, "side": 1, "horizontal": 10, "vertical":50}]})['timestamp']
            logger.info(f"差值为{date-time1}")
            if date-time1 >0.05:
                assert False
                assert date-time1
                break
            else:
                assert date-time1

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机auto换到manual_改变出风口角度触发的所有现象")
    def test_caseid_1980042(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 8, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 9, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 10, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 11, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 12, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 100, "vertical":100}, 
                                                          {"id": 3, "side": 0, "horizontal": 100, "vertical":100}, {"id": 4, "side": 0, "horizontal": 100, "vertical":100}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机auto换到manual_设置温度触发的所有现象")
    def test_caseid_1980059(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":12})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": 23.0})
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 23, "tempPassenger": 23, "tempSecRow": 23, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机auto换到manual_convenience设置温度触发的所有现象")
    def test_caseid_1980061(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.state_Auto()
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": 23.0})
            sleep(0.2)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 23, "tempPassenger": 23, "tempSecRow": 23, "windSpeedFirRow": 12, 
                                                    "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机manual换到auto_设置AUto为on触发的所有现象")
    def test_caseid_1980067(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机manual换到auto_设置后排开关off后，设置Auto为On触发的所有现象")
    def test_caseid_1980068(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 2})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})


    @pytest.mark.sanity
    @allure.title("状态机auto换到除雾除霜_打开除霜触发的所有现象")
    def test_caseid_1980030(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.state_Auto()
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机auto换到除雾除霜_远程打开除霜触发的所有现象")
    def test_caseid_1980031(self):
        self.state_Auto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_设置auto关闭触发的所有现象")
    def test_caseid_1980032(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        
    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_设置AC关闭触发的所有现象")
    def test_caseid_1984948(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_改变主驾循环模式触发的所有现象")
    def test_caseid_1984949(self):
        for X in range(2, 7):
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.2)
            logger.info(f"--循环模式设置为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":X})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":X, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
            
    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_改变副驾循环模式触发的所有现象")
    def test_caseid_1984950(self):
        for X in range(2, 7):
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.2)
            logger.info(f"--循环模式设置为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":X})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":X, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
            
    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_改变后排循环模式触发的所有现象")
    def test_caseid_1984951(self):
        for X in range(2, 7):
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.2)
            logger.info(f"--循环模式设置为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":X})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":X, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机auto换到manual_真实吹风模式改变触发的所有现象")
    def test_caseid_1980035(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})


    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_改变循环模式触发的所有现象")
    def test_caseid_1980039(self):
        for X in [2, 3]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.2)
            logger.info(f"--循环模式设置为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": X})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": X})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_改变循环模式触发的所有现象")
    def test_caseid_1984952(self):
        for X in [2, 3]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.2)
            logger.info(f"--循环模式设置为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": X})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": X})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_设置AC打开触发的所有现象")
    def test_caseid_1979992(self):
        self.state_off_withAuto()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_后排开关打开触发的所有现象")
    def test_caseid_1979993(self):
        self.state_off_withAuto()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF带auto记忆切换到Auto_改变循环模式触发的所有现象")
    def test_caseid_1979994(self):
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode":2})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF带auto记忆切换到Auto_改变出风口角度触发的所有现象")
    def test_caseid_1979995(self):
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 8, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 9, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 10, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 11, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 12, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 100, "vertical":100}, 
                                                          {"id": 3, "side": 0, "horizontal": 100, "vertical":100}, {"id": 4, "side": 0, "horizontal": 100, "vertical":100}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF带auto记忆切换到Auto_设置座椅通风触发的所有现象")
    def test_caseid_1979996(self):
        self.state_off_withAuto()
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel", 
                                             {"params": [{"id": 0, "uint8Info": 3}, {"id": 1, "uint8Info": 3}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到除雾除霜_convenience及以上下设置除雾除霜触发的所有现象")
    def test_caseid_1979997(self):
        for usagemode in [2, 11, 13]:
            self.sd_tester.change_usage_mode(usagemode)
            self.state_off_withAuto()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF带auto记忆切换到除雾除霜-inactive下设置除雾除霜触发的所有现象")
    def test_caseid_1979998(self):
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("通知和获取远程空调上高压状态-遍历")
    def test_caseid_1979839(self):
        for X in [0, 1]:
            self.sd_tester.change_usage_mode(X)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', 0)
            self.partner.empty_all(1)
            for Y in [1, 0]:
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', Y)
                sleep(1)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateHVStatus", {"sts": Y})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateHVStatus", {}, {"out": Y})

    @pytest.mark.full
    @allure.title("通知和获取远程空调上高压状态-校验默认值")
    def test_caseid_1988652(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', 1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT,resume_all_bus=False)
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateHVStatus", {}, {"out": 255})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateHVStatus", {"sts": 1})
        
    @pytest.mark.sanity
    @allure.title("通知和获取远程空调延长高压状态-遍历")
    def test_caseid_1979840(self):
        for X in [0, 1]:
            self.sd_tester.change_usage_mode(X)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaDelaySts', 0)
            self.partner.empty_all(1)
            for Y in [1, 0]:
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaDelaySts', Y)
                sleep(1)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateHVDelayStatus", {"extendSts": Y})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateHVDelayStatus", {}, {"out": Y})
   
    @pytest.mark.full
    @allure.title("通知和获取远程空调延长高压状态-校验默认值")
    def test_caseid_1988653(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaDelaySts', 0)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT,resume_all_bus=False)
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateHVDelayStatus", {}, {"out": 255})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateHVDelayStatus", {"extendSts": 0})
    
    @pytest.mark.sanity
    @allure.title("通知和获取远程空调开启关闭反馈-遍历")
    def test_caseid_1988656(self):   
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr44, 'RemStrtClimaRspn', 1) 
        for sts in range(2):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr44, 'RemStrtClimaRspn', sts) 
            self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOnOffReceiveFeedback", {"sts": sts})  
            
    @pytest.mark.full
    @allure.title("通知和获取远程空调开启关闭反馈-校验默认值(事件帧)")
    def test_caseid_1988657(self): 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr44, 'RemStrtClimaRspn', 1)  
        for sts in range(2):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr44, 'RemStrtClimaRspn', sts) 
            self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT,resume_all_bus=False)
            sleep(1)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteOnOffReceiveFeedback", {}, {"out": 255})
          
    @pytest.mark.smoke
    @allure.title("通知和获取远程空调延长高压反馈-遍历")
    def test_caseid_1979841(self):
        for X in [0, 1]:
            self.sd_tester.change_usage_mode(X)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaExtnTiRspn', 0)
            self.partner.empty_all(1)
            for Y in [1, 0]:
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaExtnTiRspn', Y)
                sleep(1)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateSwitchToHVDelayReceiveFeedback", {"sts": Y})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateSwitchToHVDelayReceiveFeedback", {}, {"out": Y})

    @pytest.mark.sanity
    @allure.title("通知和获取远程空调开启关闭状态-遍历")
    def test_caseid_1979842(self):
        for X in [0, 1]:
            self.sd_tester.change_usage_mode(X)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
            self.partner.empty_all(1)
            for Y in [1, 0]:
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', Y)
                sleep(1)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemotePowerStatus", {"status": Y})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemotePowerStatus", {}, {"out": Y})
   
    @pytest.mark.full
    @allure.title("通知远程空调开启关闭状态-校验默认值")
    def test_caseid_1988655(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT,resume_all_bus=False)
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemotePowerStatus", {}, {"out": 255})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "RemotePowerStatus", {"status": 1})

    @pytest.mark.full
    @allure.title("通知远程空调延长高压反馈-校验默认值")
    def test_caseid_1988654(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaExtnTiRspn', 1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT,resume_all_bus=False)
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateSwitchToHVDelayReceiveFeedback", {}, {"out": 255})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateSwitchToHVDelayReceiveFeedback", {"sts": 1})
    
    @pytest.mark.sanity
    @allure.title("设置除霜模式开启关闭_遍历使用者模式为0，1的情况")
    @pytest.mark.failed
    def test_caseid_1979763(self):
        for X in [0, 1]:
            self.sd_tester.change_usage_mode(X)
            sleep(2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmDefrostReq', 1, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmDefrostReq', 0, timeout=0.5)
            self.partner.empty_all(2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmDefrostReq', 2, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmDefrostReq', 0, timeout=0.5)
            
    @pytest.mark.sanity
    @allure.title("设置空调自动模式开启关闭_后排空调Off_状态机从Auto切回之前状态的情况")
    def test_caseid_1979732(self):
        #状态机为OFF时
        self.state_manual()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId":1}, {"out":{"zoneId":1, "speed":6}})
        sleep(0.1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId":2}, {"out":{"zoneId":2, "speed":0}})
        
    @pytest.mark.sanity
    @allure.title("设置A/C开或关_遍历展车模式打开/关闭的情况")
    def test_caseid_1979743(self):
        self.sd_tester.write_single_ccp(502, 2)
        sleep(3)
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            #展车模式打开时
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
            sleep(1)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                            {"isOpen": True})
            # sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": False}})
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", 
                                            {"isOpen": False})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAC", {}, {"out": False})
            #展车模式关闭时
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                  {"status":{"acStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAC", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": True}})
        
    @pytest.mark.sanity
    @allure.title("设置内外循环模式_无效值")
    def test_caseid_1985972(self):
        for mode in range(4):
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCycleMode', {"mode": mode})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": mode})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCycleMode', {"mode": 4})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("设置空调温度（可以不联动空调）_不同使用者模式的情况")
    @pytest.mark.failed
    def test_caseid_1979761(self):
        info1 = ["HmiCmptmtTSpForRowFirstLe", "HmiCmptmtTSpForRowFirstRi", "HmiCmptmtTSpForRowSecLe", "HmiCmptmtTSpForRowSecRi"]
        info2 = ["HmiCmptmtTSpSpclForRowFirstLe", "HmiCmptmtTSpSpclForRowFirstRi", "HmiCmptmtTSpSpclForRowSecLe", "HmiCmptmtTSpSpclForRowSecRi"]
        def results1(input1):
            if input1 ==0:
                return 1
            if input1 ==1:
                return 2
            else:
                return 0
        def results2(input2):
            if input2 ==0 or input2 ==1:
                return 14
            else:
                return (input2-15)*2
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            for Y in [0, 1, 16, 28]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
                sleep(0.1)
                logger.info(f"--设置使用者模式{X}--温度设置{Y}--")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": Y})
                sleep(0.2)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                    {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow": Y, "tempSecLeft": Y, "tempSecRight": Y}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "value": Y, "isValid": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 3}, 
                                                {"out": {"zoneId":3, "value": Y, "isValid": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetTargetTemperature", {"zoneId": 4}, 
                                                {"out": {"zoneId":4, "value": Y, "isValid": True}})
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            for Y in [0, 1, 16, 28]:
                logger.info(f"--设置使用者模式{X}--温度设置{Y}--")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": Y})
                sleep(0.2)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                    {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow": Y, "tempSecLeft": Y, "tempSecRight": Y}})
                for Z in info1:
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, Z, results2(Y))
                for Q in info2:
                    self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, Q, results1(Y))

    @pytest.mark.sanity
    @allure.title("设置除霜模式开启关闭_遍历使用者模式为2，11，13且不同状态机的情况")
    @pytest.mark.failed
    def test_caseid_1979764(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            sleep(1)
            #状态机为OFF时，切为除霜除雾
            self.state_off_withoutAuto()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.2)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiDefrstMaxReq', 1, timeout=0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                    {"status":{"windSpeedFirRow": 9, "windSpeedSecRow": 0, "airModeDriver": {"mode": 2}, 
                                               "airModePassenger": {"mode": 1}, "airModeSecRow": {"mode": 1}}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 2}, {"out": {"zoneId": 2, "mode": 1}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 3}, {"out": {"zoneId": 3, "mode": 2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 4}, {"out": {"zoneId": 4, "mode": 1}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, {"out": {"zoneId": 1, "speed": 9}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, {"out": {"zoneId": 2, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            #状态机为manual时，切为除霜除雾
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.2)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiDefrstMaxReq', 1, timeout=0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                    {"status":{"windSpeedFirRow": 9, "windSpeedSecRow": 0, "airModeDriver": {"mode": 2}, 
                                               "airModePassenger": {"mode": 1}, "airModeSecRow": {"mode": 1}}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 2}, {"out": {"zoneId": 2, "mode": 1}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 3}, {"out": {"zoneId": 3, "mode": 2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 4}, {"out": {"zoneId": 4, "mode": 1}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, {"out": {"zoneId": 1, "speed": 9}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, {"out": {"zoneId": 2, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            #除雾除霜退回auto时
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 2}, {"out": {"zoneId": 2, "mode": 2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 3}, {"out": {"zoneId": 3, "mode": 2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 4}, {"out": {"zoneId": 4, "mode": 2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, {"out": {"zoneId": 1, "speed": 12}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, {"out": {"zoneId": 2, "speed": 12}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.2)
            #auto切为除霜除霜时
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                    {"status":{"windSpeedFirRow": 9, "windSpeedSecRow": 0, "airModeDriver": {"mode": 2, "isWindModeAuto": False}, 
                                               "airModePassenger": {"mode": 2, "isWindModeAuto": True}, "airModeSecRow": {"mode": 2, "isWindModeAuto": True}}})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiDefrstMaxReq', 1, timeout=0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 2}, {"out": {"zoneId": 2, "mode": 2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 3}, {"out": {"zoneId": 3, "mode": 2}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId": 4}, {"out": {"zoneId": 4, "mode": 2}})
    
    @pytest.mark.sanity
    @allure.title("设置自动同步分区温度_改变副或后，再改变主驾的现象")
    def test_caseid_1980113(self):
        for Y in [0, 1, 16, 28]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperatureAndOn', {"zoneId": 3, "value": 22})
            sleep(0.1)
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperatureAndOn', {"zoneId": 2, "value": Y})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": 22, "tempPassenger": 22, "tempSecRow":Y}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperatureAndOn', {"zoneId": 3, "value": 20})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": False}})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow":Y}})
        for Z in [0, 1, 16, 28]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperatureAndOn', {"zoneId": 3, "value": 22})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperatureAndOn', {"zoneId": 4, "value": Z})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": 22, "tempPassenger": Z, "tempSecRow":22}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperatureAndOn', {"zoneId": 3, "value": 20})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": False}})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": 20, "tempPassenger": Z, "tempSecRow":20}})
            
    @pytest.mark.sanity
    @allure.title("设置自动同步分区温度_遍历不同状态机的情况")
    def test_caseid_1979765(self):
        self.sd_tester.change_usage_mode(2)
        sleep(1)
        #状态机为OFF时
        self.state_off_withoutAuto()
        for Y in [0, 1, 16, 28]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": Y})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow":Y}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 2, "value": 20})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": False}})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow":20}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": 21})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": 21, "tempPassenger": 21, "tempSecRow":20}})
        #状态机为manaual时
        self.state_manual()
        for Y in [0, 1, 16, 28]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": Y})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow":Y}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 4, "value": 20})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": False}})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": 20, "tempSecRow":Y}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": 21})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": 21, "tempPassenger": 20, "tempSecRow":21}})
        #状态机为Auto时
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        for Y in [0, 1, 16, 28]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": True}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": Y})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow":Y}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 2, "value": 18})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": False}})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow":18}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        #状态机为除雾除霜时
        for Y in [0, 1, 16, 28]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": True}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 3, "value": Y})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": Y, "tempSecRow":Y}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId": 4, "value": 26})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "AutoSyncStatus", {"status": {"zoneId": 0, "isOn": False}})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                {"status":{"tempDriver": Y, "tempPassenger": 26, "tempSecRow":Y}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})

    @pytest.mark.sanity
    @allure.title("设置电动出风口开启关闭_abonded和inactive下的情况")
    @pytest.mark.failed
    def test_caseid_1979768(self):
        def info1(input1):
            return 1 if input1 == True else 0
        info2= {8:"HmiAirVentDrvrLeSwtReq", 9:"HmiAirVentDrvrRiSwtReq", 10:"HmiAirVentPassLeSwtReq", 11:"HmiAirVentPassRiSwtReq", 12:"HmiAirVentSecLeLeSwtReq"}
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            for key, value in info2.items():
                for Z in [True, False]:
                    self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": key, "on": Z})
                    self.ipdu.check(self.ipdu.bodycan.BgmBodyFr13, value, info1(Z))
                    self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId": key}, {"out": Z})

    @pytest.mark.sanity
    @allure.title("设置AC-校验总线信号")
    @pytest.mark.failed
    def test_caseid_1980115(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAC', {"on": True})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtCoolgReq', 1, timeout=0.5)
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtCoolgReq', 1, timeout=0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAC', {"on": False})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtCoolgReq', 0, timeout=0.5)
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, 'HmiCmptmtCoolgReq', 0, timeout=0.5)

    @pytest.mark.sanity
    @allure.title("设置内外循环模式_校验总线信号")
    @pytest.mark.failed
    def test_caseid_1980118(self):
        for X in range(4):
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetCycleMode', {"mode": X})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', X, timeout=0.5)

    @pytest.mark.sanity
    @allure.title("设置远程开启空调_校验总线信号")
    @pytest.mark.failed
    def test_caseid_1980119(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 0)
        self.partner.empty_all(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOff', {})
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 0)

    @pytest.mark.sanity
    @allure.title("设置空调吹风模式_校验总线信号")
    @pytest.mark.failed
    def test_caseid_1980117(self):
        info = {2:"HmiCmptmtAirDistbnRe", 3:"HmiCmptmtAirDistbnFrntLe", 4:"HmiCmptmtAirDistbnFrntRi"}
        for key, value in info.items():
            for Y in range(8):
                logger.info(f"---设置区域{key}--发送信号{Y}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetWindMode', {"zoneId": key, "mode":Y})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, value, Y)
                sleep(1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, value, Y)

    @pytest.mark.sanity
    @allure.title("设置电动出风口模式_abonded和inactive下的情况")
    @pytest.mark.failed
    def test_caseid_1979769(self):
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            for Z in [0, 1, 2, 3]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 2, "mode": Z})
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirModReqReLeElecAirDirModReq', Z, timeout=0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVentMode", {"zoneId": 2}, {"out": Z})
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 3, "mode": Z})
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiElecAirDirModReqDrvrMod', Z, timeout=0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVentMode", {"zoneId": 3}, {"out": Z})
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 4, "mode": Z})
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiElecAirDirModReqPassMod', Z, timeout=0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVentMode", {"zoneId": 4}, {"out": Z})

    @pytest.mark.sanity
    @allure.title("设置电动出风口出风角度_abonded和inactive下的情况")
    @pytest.mark.failed
    def test_caseid_1979770(self):
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 0, "vertical":0}, 
                                                          {"id": 3, "side": 0, "horizontal": 0, "vertical":0}, {"id": 4, "side": 0, "horizontal": 0, "vertical":0}]})
            sleep(0.1)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosX', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosY', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrLePosX', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrLePosY', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassLePosX', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassLePosY', 0, timeout=0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletAngle", {"zoneId": [2, 3, 4]}, 
                                                  {"out": [{"id": 2, "side": 0, "horizontal": 0, "vertical":0}, 
                                                          {"id": 3, "side": 0, "horizontal": 0, "vertical":0}, 
                                                          {"id": 4, "side": 0, "horizontal": 0, "vertical":0}]})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 100, "vertical":100}, 
                                                          {"id": 3, "side": 0, "horizontal": 100, "vertical":100}, {"id": 4, "side": 0, "horizontal": 100, "vertical":100}]})
            sleep(0.1)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosX', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosY', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrLePosX', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrLePosY', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassLePosX', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassLePosY', 200, timeout=0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletAngle", {"zoneId": [2, 3, 4]}, 
                                                  {"out": [{"id": 2, "side": 0, "horizontal": 100, "vertical":100}, 
                                                          {"id": 3, "side": 0, "horizontal": 100, "vertical":100}, 
                                                          {"id": 4, "side": 0, "horizontal": 100, "vertical":100}]})
            #外测
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 1, "horizontal": 0, "vertical":0}, 
                                                          {"id": 3, "side": 1, "horizontal": 0, "vertical":0}, {"id": 4, "side": 1, "horizontal": 0, "vertical":0}]})
            sleep(0.1)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosX', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosY', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrRiPosX', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrRiPosY', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassRiPosX', 0, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassRiPosY', 0, timeout=0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletAngle", {"zoneId": [2, 3, 4]}, 
                                                  {"out": [{"id": 2, "side": 1, "horizontal": 0, "vertical":0}, 
                                                          {"id": 3, "side": 1, "horizontal": 0, "vertical":0}, 
                                                          {"id": 4, "side": 1, "horizontal": 0, "vertical":0}]})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 1, "horizontal": 100, "vertical":100}, 
                                                          {"id": 3, "side": 1, "horizontal": 100, "vertical":100}, {"id": 4, "side": 1, "horizontal": 100, "vertical":100}]})
            sleep(0.1)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosX', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'HmiReElecAirDirCrtlReqSecRowLePosY', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrRiPosX', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqDrvrRiPosY', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassRiPosX', 200, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr49, 'HmiElecAirDirCrtlReqPassRiPosY', 200, timeout=0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletAngle", {"zoneId": [2, 3, 4]}, 
                                                  {"out": [{"id": 2, "side": 1, "horizontal": 100, "vertical":100}, 
                                                          {"id": 3, "side": 1, "horizontal": 100, "vertical":100}, 
                                                          {"id": 4, "side": 1, "horizontal": 100, "vertical":100}]})
            
    @pytest.mark.sanity
    @allure.title("设置香氛类型_abonded和inactive下的情况")
    @pytest.mark.failed
    def test_caseid_1979775(self):
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            for Y in [0, 100]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType', {"fragrance": [{"channel": 1, "ratio": Y}]})
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 1, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', Y, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5)
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType', {"fragrance": [{"channel": 2, "ratio": Y}]})
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 2, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', Y, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5)
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType', {"fragrance": [{"channel": 3, "ratio": Y}]})
                sleep(0.1)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 3, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', Y, timeout=0.5)

    @pytest.mark.sanity
    @allure.title("设置香氛等级_abonded和inactive下的情况")
    @pytest.mark.failed
    def test_caseid_1979786(self):
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            for Y in [0, 1, 2, 3]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceLevel', {"level": Y})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiFragraLvlReq', Y, timeout=0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceLevel", {}, {"out": Y})

    @pytest.mark.sanity
    @allure.title("通知和获取除霜状态（包含最大除霜工作状态和除霜工作状态）_不同使用者模式的情况")
    def test_caseid_1979788(self):
        def info(input):
            return True if input == 1 else False
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        sleep(0.2)
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            for Y in [1, 0]:
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', Y)
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr11, 'ClimaDefrstSts', Y)
                sleep(0.2)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyACDefrostSts", {"sts":{"defrostMax": info(Y), "climateDefrost": info(Y)}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetDefrostSts", {}, 
                                                      {"out":{"defrostMax": info(Y), "climateDefrost": info(Y)}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFastDefrostMode", {}, {"out":info(Y)})
        for X in[2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            for Y in [1, 0]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
                sleep(0.1)
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr11, 'ClimaDefrstSts', Y)
                sleep(0.2)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyACDefrostSts", {"sts":{"defrostMax": True, "climateDefrost": info(Y)}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetDefrostSts", {}, 
                                                      {"out":{"defrostMax": True, "climateDefrost": info(Y)}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFastDefrostMode", {}, {"out":True})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyACDefrostSts", {"sts":{"defrostMax": False, "climateDefrost": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetDefrostSts", {}, 
                                                      {"out":{"defrostMax": False, "climateDefrost": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFastDefrostMode", {}, {"out":False})

    @pytest.mark.sanity
    @allure.title("通知和获取通知电动出风口系统状态_遍历")
    def test_caseid_1979793(self):
        for X in [8, 9, 10, 11, 12]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": X, "on": True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "OutletStatus", {"status":{"driverVentStatus":{"isLeftOpen":True, "isRightOpen":True}, 
                                                                                                  "passVentStatus":{"isLeftOpen":True, "isRightOpen":True}, 
                                                                                                  "secRowVentStatus":{"isLeftOpen":True}}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"isLeftOpen":True, "isRightOpen":True}, 
                                                                                                  "passVentStatus":{"isLeftOpen":True, "isRightOpen":True}, 
                                                                                                  "secRowVentStatus":{"isLeftOpen":True}}})
        for X in [8, 9, 10, 11, 12]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": X, "on": False})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "OutletStatus", {"status":{"driverVentStatus":{"isLeftOpen":False, "isRightOpen":False}, 
                                                                                                  "passVentStatus":{"isLeftOpen":False, "isRightOpen":False}, 
                                                                                                  "secRowVentStatus":{"isLeftOpen":False}}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"isLeftOpen":False, "isRightOpen":False}, 
                                                                                                  "passVentStatus":{"isLeftOpen":False, "isRightOpen":False}, 
                                                                                                  "secRowVentStatus":{"isLeftOpen":False}}})
        for Y in range(4):
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 2, "mode": Y})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 3, "mode": Y})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 4, "mode": Y})
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "OutletStatus", {"status":{"driverVentStatus":{"mode":Y}, 
                                                                                                  "passVentStatus":{"mode":Y}, 
                                                                                                  "secRowVentStatus":{"mode":Y}}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"mode":Y}, 
                                                                                                  "passVentStatus":{"mode":Y}, 
                                                                                                  "secRowVentStatus":{"mode":Y}}})
        for Q in [0, 100]:
            for A in [0, 1]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', {"outlets":[{"id":2, "side": A, "horizontal":Q, "vertical":Q}, 
                                                                                                        {"id":3, "side": A, "horizontal":Q, "vertical":Q}, 
                                                                                                        {"id":4, "side": A, "horizontal":Q, "vertical":Q}]})
                sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "OutletStatus", {"status":{"driverVentStatus":{"leftHorizontal":Q, "leftVertical":Q, 
                                                                                                                        "rightHorizontal":Q, "rightVertical":Q}, 
                                                                                            "passVentStatus": {"leftHorizontal":Q, "leftVertical":Q, 
                                                                                                            "rightHorizontal":Q, "rightVertical":Q}, 
                                                                                            "secRowVentStatus":{"leftHorizontal":Q, "leftVertical":Q, 
                                                                                                                "rightHorizontal":Q, "rightVertical":Q}}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"leftHorizontal":Q, "leftVertical":Q, 
                                                                                                                        "rightHorizontal":Q, "rightVertical":Q}, 
                                                                                            "passVentStatus": {"leftHorizontal":Q, "leftVertical":Q, 
                                                                                                            "rightHorizontal":Q, "rightVertical":Q}, 
                                                                                            "secRowVentStatus":{"leftHorizontal":Q, "leftVertical":Q, 
                                                                                                                "rightHorizontal":Q, "rightVertical":Q}}})  
  
    @pytest.mark.full
    @allure.title("通知/获取远程空调上高压反馈_停发总线校验默认值")
    def test_caseid_1987202(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvRspn', 1)
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, 
                                                  "GetRemoteClimateSwitchToHVReceiveFeedback", {},  {"out": 255})    
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateSwitchToHVReceiveFeedback", {"sts": 1})
        
    @pytest.mark.smoke
    @allure.title("获取远程空调上高压反馈")
    def test_caseid_1983333(self):
        for X in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvRspn', X)
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateSwitchToHVReceiveFeedback", {},  {"out": X})

    @pytest.mark.smoke
    @allure.title("通知和获取舱内温度_遍历")
    def test_caseid_1979794(self):
        def info(input):
            return True if input ==3 else False
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntCmptmtTFrnt', 0.0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntQf', 0)
        sleep(0.2)
        for X in [-60.0, 125.0]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntCmptmtTFrnt', X)
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "Temperature", {"info":{"zoneId":0, "value": X}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCurrentTemperature", {"zoneId": 0},  {"out":{"zoneId":0, "value": X}})
        for Y in [3, 0, 3, 1, 3, 2]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntQf', Y)
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "Temperature", {"info":{"isValid": info(Y)}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCurrentTemperature", {"zoneId": 0},  {"out": {"isValid": info(Y)}})

    @pytest.mark.sanity
    @allure.title("设置香氛类型_拔掉使用中的香氛的情况")
    @pytest.mark.failed
    def test_caseid_1979776(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 100)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 100)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id', 100)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType', {"fragrance": [{"channel": 1, "ratio": 100}]})
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 100, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5)
        #通道1拔掉
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 0)
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5)
        #通道2拔掉
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 100)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType', {"fragrance": [{"channel": 2, "ratio": 100}]})
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 2, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 100, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 0)
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5)
        #通道3拔掉
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 100)
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetFragranceType', {"fragrance": [{"channel": 3, "ratio": 100}]})
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 3, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 100, timeout=0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id', 0)
        sleep(0.2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5)

    @pytest.mark.sanity
    @allure.title("通知和获取环境温度_遍历")
    def test_caseid_1979796(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdQf', 1)
        sleep(0.5)
        for X in [-70.0, 134.7]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdAmbTEstimd', X)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyAmbientTempRawData", {"data":{"temp": X, "unit":0, "isValid": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "getAmbientTempRawData", {}, {"out":{"temp": X, "unit":0, "isValid": True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdQf', 0)
        sleep(0.2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdAmbTEstimd', 100.0)
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "getAmbientTempRawData", {}, {"out":{"temp": 100, "unit":0, "isValid": False}})

    @pytest.mark.sanity
    @allure.title("通知和获取冷却液液位信息_遍历")
    def test_caseid_1979812(self):
        def info(input):
            return False if input ==0 else True
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'EmotCooltIndcnReq', 1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 1)
        sleep(0.5)
        for X in [0, 1]:
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'EmotCooltIndcnReq', X)
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', X)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "coolantLowWarnInfo", {"info":{"eMotion":info(X), "battery":info(X)}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "getCoolantLowWarnInfo", {}, {"out":{"eMotion":info(X), "battery":info(X)}})

    @pytest.mark.full
    @allure.title("香氛胶囊拔出时大屏剩余含量显示_遍历非180时正常不延时通知")
    def test_caseid_1985138(self):
        for A in range(1, 6):
                logger.info(f"信号AirFragCh{A}发送10")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", 10)
        self.partner.empty_all(0.5)
        for B in [0, 100, 360]:
            for A in range(1, 6):
                logger.info(f"信号AirFragCh{A}发送{B}")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", B)
                sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[B, B, B, B, B]}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[B, B, B, B, B]}})

    @pytest.mark.full
    @allure.title("香氛胶囊拔出时大屏剩余含量显示_遍历非180到180再到非180时正常不延时通知")
    def test_caseid_1985145(self):
        for A in range(1, 6):
                logger.info(f"信号AirFragCh{A}发送10")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", 10)
        self.partner.empty_all(0.5)
        for B in range(1, 6):
                logger.info(f"信号AirFragCh{B}发送180")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{B}AvlTi", 180)
                sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 360)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[360, 180, 10, 10, 10]}},timeout=2.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 360)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[360, 360, 180, 10, 10]}}, timeout=1.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 360)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[360, 360, 360, 180, 10]}}, timeout=1.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 360)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[360, 360, 360, 360, 180]}}, timeout=1.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 360)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[360, 360, 360, 360, 360]}}, timeout=1.5)
        sleep(2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[360, 360, 360, 360, 360]}}, timeout=1.5)
          
    @pytest.mark.full
    @allure.title("香氛胶囊拔出时大屏剩余含量显示_遍历180跳变时正常延时通知")
    def test_caseid_1985144(self):
        for A in range(1, 6):
                logger.info(f"信号AirFragCh{A}发送10")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", 10)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 180) #第一个信号
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 20)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 180)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        sleep(3)#第一次发180的7S内
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[10, 10, 10, 10, 10]}})
        sleep(3)#第二次发180的7S后
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 10, 10, 10, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 10, 10, 10, 10]}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 180)#第二个信号
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 20)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 180)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        sleep(3)#第一次发180的7S内
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 10, 10, 10, 10]}})
        sleep(3)#第二次发180的7S后
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 10, 10, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 10, 10, 10]}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 180)#第3个信号
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 20)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 180)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        sleep(3)#第一次发180的7S内
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 10, 10, 10]}})
        sleep(3)#第二次发180的7S后
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 10, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 10, 10]}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 180)#第4个信号
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 20)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 180)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        sleep(3)#第一次发180的7S内
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 10, 10]}})
        sleep(3)#第二次发180的7S后
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 180, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 180, 10]}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 180)#第5个信号
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 20)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 180)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        sleep(3)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 180, 10]}})
        sleep(3)#第二次发180的7S后
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 180, 180]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 180, 180]}})

    @pytest.mark.full
    @allure.title("香氛胶囊拔出时大屏剩余含量显示_遍历180时正常延时通知")
    def test_caseid_1985143(self):
        for A in range(1, 6):
                logger.info(f"信号AirFragCh{A}发送10")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", 10)
        self.partner.empty_all(0.5)
        for B in range(1, 6):
            logger.info(f"信号AirFragCh{B}发送{180}")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{B}AvlTi", 180)
            sleep(1)
        self.partner.empty_all(1) #第一个信号发送之后的6s
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[10, 10, 10, 10, 10]}})
        sleep(1)#第7S
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 10, 10, 10, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 10, 10, 10, 10]}})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 10, 10, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 10, 10, 10]}})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 10, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 10, 10]}})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 180, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 180, 10]}})
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 180, 180]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[180, 180, 180, 180, 180]}})
        self.partner.empty_all(0.5)
        for A in range(1, 6):
                logger.info(f"信号AirFragCh{A}发送0")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", 0)
                sleep(0.1)
        sleep(1)      
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 180)
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 360)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[0, 0, 0, 0, 0]}})
        sleep(5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[360, 0, 0, 0, 0]}})

    @pytest.mark.sanity
    @allure.title("香通知/获取香氛信息原子能力_单个信号调用触发")
    def test_caseid_1987580(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', 1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[False, False, False], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[False, False, False], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh1UseUpWrn', 1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, False, False], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, False, False], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh2UseUpWrn', 1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, False], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, False], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh3UseUpWrn', 1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[0, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 255)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 10)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id', 255)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 359)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 0, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 180)
        sleep(7)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 180, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 180, 0, 0, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 0)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 180)
        sleep(7)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 180, 0, 180, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 180, 0, 180, 0]}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 10)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 180, 0, 180, 10]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 10, 255], "leftTime":[359, 180, 0, 180, 10]}})

    @pytest.mark.full
    @allure.title("通知/获取香氛信息原子能力_停发0x300单帧总线校验事件")
    def test_caseid_1987582(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh1UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh2UseUpWrn', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh3UseUpWrn', 0)       
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 255)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh4Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh5Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 10)
        self.ipdu.stop_send_pdu('bodycan', 0x300)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, False, False], "channelId":[255, 0, 0], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":True, "isUseup":[True, False, False], "channelId":[255, 0, 0], "leftTime":[ 0, 0, 0, 0, 0]}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, False, False], "channelId":[255, 0, 0], "leftTime":[0, 0, 0, 10, 0]}})

    @pytest.mark.full
    @allure.title("通知/获取香氛信息原子能力_停发0x4A0单帧总线校验事件")
    def test_caseid_1987584(self):  
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh1UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh2UseUpWrn', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh3UseUpWrn', 0)       
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 255)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 10)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 0)
        self.ipdu.stop_send_pdu('bodycan', 0x4A0)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":False, "isUseup":[True, False, False], "channelId":[255, 255, 255], "leftTime":[0, 0, 0, 10, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":False, "isUseup":[True, False, False], "channelId":[255, 255, 255], "leftTime":[ 0, 0, 0, 10, 0]}},timeout=0.3)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, False, False], "channelId":[255, 0, 0], "leftTime":[0, 0, 0, 10, 0]}})

    @pytest.mark.full
    @allure.title("通知/获取香氛信息原子能力_启动场景")
    def test_caseid_1987583(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh1UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh2UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh3UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 255)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 180)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 180)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 181)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 179)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 360)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 0, 0], "leftTime":[180, 180, 181, 179, 360]}})
       
    @pytest.mark.full
    @allure.title("通知/获取香氛信息原子能力_启动场景")
    def test_caseid_1987731(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh1UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh2UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh3UseUpWrn', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id', 255)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 180)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 180)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 180)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 181)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 179)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                              {"out":{"isRefreshOn":False, "isUseup":[False, False, False], "channelId":[255, 255, 255], "leftTime":[ 0, 0, 0, 0, 0]}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", 
                                              {"info":{"isRefreshOn":True, "isUseup":[True, True, True], "channelId":[255, 0, 0], "leftTime":[180, 180, 180, 181, 179]}})
        
    @pytest.mark.full
    @allure.title("通知/获取香氛信息原子能力_leftTime多个通道不同时间开启计时器后停发总线")
    def test_caseid_1987585(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 90)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 90)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 90)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 90)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 90)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh1AvlTi", 180)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh2AvlTi", 180)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh3AvlTi", 180)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh4AvlTi", 180)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 180)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, "AirFragCh5AvlTi", 10)
        sleep(1)
        self.ipdu.pause_all_bus_send()
        sleep(2)
        self.partner.ck_coming_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 90, 90, 90, 10]}},timeout=1.5)
        self.partner.ck_coming_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 90, 90, 10]}},timeout=1.5)
        self.partner.ck_coming_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 90, 10]}},timeout=1.5)
        self.partner.ck_coming_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[180, 180, 180, 180, 10]}},timeout=1.5) 
        self.partner.empty_all(1)       
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo")
    
    @pytest.mark.sanity
    @allure.title("通知和获取香氛信息_遍历")
    def test_caseid_1979813(self):
        def info(input):
            return False if input ==0 else True
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh1UseUpWrn',  0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh2UseUpWrn',  0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh3UseUpWrn',  0)
        for A in range(1, 6):
            logger.info(f"信号AirFragCh{A}发送")
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", 20)
        self.partner.empty_all(0.5)
        for X in [0, 1]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', X)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"isRefreshOn":info(X)}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"isRefreshOn":info(X)}})
        for Y in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh1UseUpWrn',  Y)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh2UseUpWrn',  Y)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FragCh3UseUpWrn',  Y)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"isUseup":[info(Y), info(Y), info(Y)]}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"isUseup":[info(Y), info(Y), info(Y)]}})
        for Z in [1, 0]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id',  Z)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id',  Z)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id',  Z)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"channelId":[Z, Z, Z]}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"channelId":[Z, Z, Z]}})
        for B in [0, 60]:
            for A in range(1, 6):
                logger.info(f"信号AirFragCh{A}发送{B}")
                self.ipdu.set(self.ipdu.bodycan.CcmBodyFr60, f"AirFragCh{A}AvlTi", B)
                sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "FragranceInfo", {"info":{"leftTime":[B, B, B, B, B]}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, {"out":{"leftTime":[B, B, B, B, B]}})

    @pytest.mark.sanity
    @allure.title("通知和获取PM25信息_遍历")
    def test_caseid_1979817(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr01, 'IntPm25LvlFrmClima', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'IntPm25HiPopUp', 1)
        self.partner.empty_all(0.5)
        for X in range(4):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', X)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "PM25", {"info":{"status":X}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Info", {}, {"out":{"status":X}})
        for Y in range(8):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr01, 'IntPm25LvlFrmClima', Y)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "PM25", {"info":{"level":Y}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Info", {}, {"out":{"level":Y}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Level", {}, {"out": Y})
        for Z in range(4):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'IntPm25HiPopUp', Z)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "PM25", {"info":{"warning":Z}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Info", {}, {"out":{"warning":Z}})
        for A in [1000, 100]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr02, 'IntPm25VluFrmClima', A)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "PM25", {"info":{"value":A}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Info", {}, {"out":{"value":A}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Value", {}, {"out": A})

    @pytest.mark.sanity
    @allure.title("通知和获取AQS信息_遍历")
    def test_caseid_1979820(self):
        def info(input):
            return False if input ==0 else True
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyOutdAirQly', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'LvlOfClimaCmft', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 1)
        self.partner.empty_all(0.5)
        for X in range(4):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyOutdAirQly', X)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyAQSInfo", {"info":{"level":X}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAQSLevel", {}, {"out": X})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAQSInfo", {}, {"out":{"level":X}})
        for Y in range(8):
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'LvlOfClimaCmft', Y)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyAQSInfo", {"info":{"zone":Y}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAQSInfo", {}, {"out":{"zone":Y}})
        for Z in [0, 1]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', Z)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyAQSInfo", {"info":{"isValid":info(Z)}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAQSInfo", {}, {"out":{"isValid":info(Z)}})

    @pytest.mark.sanity
    @allure.title("设置远程空调上高压")
    @pytest.mark.failed
    def test_caseid_1979834(self):
        for X in [0, 1]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHV", {"isOn": False, "time": 20})
            self.partner.empty_all(2)
            for Y in [0, 60]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHV", {"isOn": True, "time": Y})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 1, timeout=0.5)
                sleep(0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsRunTime', Y, timeout=0.5)
                self.partner.empty_all(2)
            for Z in [0, 60]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHV", {"isOn": False, "time": Z})
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 2, timeout=0.5)
                sleep(0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsCmd', 0, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr84, 'RemStrtHvCtrlReqErsRunTime', Z, timeout=0.5)
                self.partner.empty_all(2)
                
    @allure.title("设置远程空调上高压_校验下行tcpdump")
    @pytest.mark.full
    def test_caseid_1987195(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHV", {"isOn": True, "time": 59})
        sleep(0.15)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHV", {"isOn": True, "time": 10})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemStrtHvCtrlReqErsCmd", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.bgm_eth_inter.ck_signal_values("RemStrtHvCtrlReqErsRunTime", [59, 59, 10, 10, 10, 10, 10, 10, 10, 10])

    @pytest.mark.smoke
    @allure.title("通知和获取空调系统故障_遍历")
    def test_caseid_1979822(self):
        info = {0:0, 1:6, 2:7, 3:8, 4:9, 5:10, 6:11, 7:12, 8:13}
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'RemClimaWarn', 2)
        self.partner.empty_all(0.5)
        for key, value in info.items():
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'RemClimaWarn', key)
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateFault", {"faults":[{"faultId":value, "faultMsg":""}]})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateFault", {}, {"out":[{"faultId":value, "faultMsg":""}]})

    @pytest.mark.sanity
    @allure.title("通知和获取空调状态机当前模式_切换到OFF的情况")
    def test_caseid_1979824(self):
        #状态机为Manual时
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        #状态机为Auto时
        self.state_Auto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        #状态机为除霜除霜时
        self.state_Defrost()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为auto时打开车门风速改变回到10档")
    def test_caseid_1985963(self):
        self.io.set_four_door_close()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        sleep(0.1)
        self.five_door_open()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":10})
        sleep(0.1)
        self.io.set_four_door_close()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为Manual时打开车门后改变风速关门风速不变")
    def test_caseid_1987159(self):
        self.io.set_four_door_close()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.1)
        self.five_door_open()
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":5})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":4})
        sleep(2)
        self.io.set_four_door_close()
        sleep(2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为除霜除雾时打开车门风速改变回到10档")
    def test_caseid_1985964(self):
        self.io.set_four_door_close()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.five_door_open()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":1})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":4})
        sleep(0.1)
        self.io.set_four_door_close()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": False}})
 
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为除霜除雾且后排开关未开启时打开车门")
    def test_caseid_1985874(self):
        self.sd_tester.change_usage_mode(2)
        self.io.set_four_door_close()
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":4})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.1)
        self.five_door_open()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(1)
        self.io.set_four_door_close()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": False}})

    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为除霜除雾且后排开关未开启时打开车门")
    def test_caseid_1984408(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.1)
        self.io.set_four_door_close()
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.five_door_open()
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 4}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 9}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为manual降风速后关闭空调再关车门")
    def test_caseid_1985490(self):
        self.io.set_four_door_close()
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.five_door_open()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":6})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":4})
        sleep(1)
        self.io.set_four_door_close()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为manual且后排开关开启时风速小于4档打开车门")
    def test_caseid_1984390(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":3})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":3})
        sleep(0.1)
        self.io.set_four_door_close()
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.five_door_open()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 3, 
                                                "windSpeedSecRow":3, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 3}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 3}})
        
    @pytest.mark.full
    @pytest.mark.restart
    @allure.title("开门降空调风量功能_状态机为除霜除雾BGM重启时打开车门")
    def test_caseid_1984411(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.1)
        self.io.set_four_door_close()
        sleep(0.2)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.five_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 4}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 4}})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 6}})

    @pytest.mark.full
    @pytest.mark.restart
    @allure.title("开门降空调风量功能_状态机为manual且后排开关开启时在BGM重启后打开车门")
    def test_caseid_1984386(self):
        self.io.set_four_door_close()
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.five_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 4}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 4}})
        
    @pytest.mark.full
    @pytest.mark.restart
    @allure.title("开门降空调风量功能_状态机为auto时BGM重启打开车门")
    @pytest.mark.failed
    def test_caseid_1985071(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        sleep(0.1)
        self.io.set_four_door_close()
        sleep(1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.five_door_open()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 10, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 10, timeout=0.5)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 10, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 10, timeout=0.5)
        self.io.set_four_door_close()
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})

    @pytest.mark.full
    @allure.title("开门降空调风量功能_除霜除雾状态机时Flag=1时改变风速")
    @pytest.mark.failed
    def test_caseid_1984426(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.1)
        self.io.set_four_door_close()
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.five_door_open()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 5})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 5, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 5, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": False}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 5, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 5}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_auto状态机时Flag=1时改变风速")
    @pytest.mark.failed
    def test_caseid_1985072(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.io.set_four_door_close()
        self.five_door_open()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 10, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 10, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 11})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed": 11})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 11, 
                                                "windSpeedSecRow":11, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.io.set_four_door_close()
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 11, 
                                                "windSpeedSecRow":11, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 11, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 11, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 11}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 11}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        
    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_改变循环模式=7触发的所有现象")
    def test_caseid_1985767(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 2, "mode": 7})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 3, "mode": 7})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 4, "mode": 7})
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.partner.empty_all(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.full
    @allure.title("JBS-30222_打开AUTO后, 开门降低风量后, 空调面板内的吹风图标全置灰")
    def test_caseid_1985068(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.io.set_four_door_close()
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.io.rire_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.io.rire_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为auto时且后排开关开启时打开车门")
    @pytest.mark.failed
    def test_caseid_1985075(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 12})
        sleep(0.1)
        self.io.set_four_door_close()
        self.five_door_open()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 10, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 10, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 10}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 10}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 12, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 12, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 12}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 12}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为auto打开车门后调整风速")
    @pytest.mark.failed
    def test_caseid_1985371(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 13})
        sleep(0.1)
        self.io.set_four_door_close()
        self.five_door_open()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 10, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 10, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 14})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                "windSpeedSecRow":14, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                "windSpeedSecRow":14, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                "windSpeedSecRow":14, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 14, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 14, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 14}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 14}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            
    @pytest.mark.full
    @allure.title("开门降空调风量功能_OFF状态机三门关一门开，开启空调四门开")
    def test_caseid_1987587(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.five_door_open()
        self.io.drvr_door_close()
        sleep(3)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})    
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.io.drvr_door_open()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}) 
        self.io.set_four_door_close()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})            
                 
 
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为auto且风速=13时打开车门")
    @pytest.mark.failed
    def test_caseid_1985370(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 13})
        sleep(0.1)
        self.io.set_four_door_close()
        sleep(1)
        self.five_door_open()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 10, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 10, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 10}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 10}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                                "windSpeedSecRow":13, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 13, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 13, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 13}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 13}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        
    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为auto且风速=11时打开车门")
    @pytest.mark.failed
    def test_caseid_1985369(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 11})
        sleep(0.1)
        self.io.set_four_door_close()
        self.five_door_open()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 10, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 10, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 10}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 10}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 11, 
                                                "windSpeedSecRow":11, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus":
                                                  True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 11, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 11, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 11}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 11}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为manual且后排开关未开启时打开车门")
    def test_caseid_1984383(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.io.set_four_door_close()
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.five_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 4}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})

    @pytest.mark.full
    @allure.title("开门降空调风量功能_状态机为manual且后排开关开启时打开车门")
    def test_caseid_1984370(self):
        self.io.set_four_door_close()
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.io.drvr_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 4}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 4}})
        self.io.drvr_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 6}})
        self.io.pass_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.io.pass_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 6}})
        self.io.rire_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.io.rire_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 6}})
        self.io.lere_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.io.lere_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 6}})
        self.five_door_open()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 4, 
                                                "windSpeedSecRow":4, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.io.set_four_door_close()
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 6}})

    @pytest.mark.sanity
    @allure.title("通知和获取空调状态机当前模式_除雾除霜切换到manual的情况")
    def test_caseid_1979827(self):
        self.sd_tester.change_usage_mode(2)
        #状态机为除雾除霜时，设置吹风模式
        for X in [0, 1, 3, 4, 5, 6, 7]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 3, "mode": X})
            sleep(1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为除雾除霜时，关闭除雾除霜
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为除雾除霜时，打开后排空调
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 2})
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为除雾除霜时，设置后排温度
        for X in [16, 28, 1, 0]:
            logger.info(f"-------设置后排温度为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": X})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为除雾除霜时，设置后排温度
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":2, "value": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})

    @pytest.mark.sanity
    @allure.title("通知和获取空调状态机当前模式_manual切到Auto的情况")
    def test_caseid_1979830(self):
        for X in [1, 0]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
            sleep(0.5)

    @pytest.mark.sanity
    @allure.title("通知和获取空调状态机当前模式_除雾除霜切到Auto的情况")
    def test_caseid_1979831(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            #auto切为除雾除霜时，再关闭除霜
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            #auto切为除雾除霜时，再设置自动打开
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            #auto切为除雾除霜时，再设置后排打开
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 2})
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            #auto切为除雾除霜时，再设置温度SetTemperatureAndOn
            for Y in [1, 0, 16, 28]:
                logger.info(f"-------设置温度为{Y}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
                sleep(0.5)
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId": 2, "value": Y})
                sleep(0.5)
                self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            #auto切为除雾除霜时，再设置温度SetTemperature
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId": 2, "value": 22})
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})

    @pytest.mark.sanity
    @allure.title("通知和获取空调状态机当前模式_除雾除霜的情况")
    def test_caseid_1979832(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.state_off_withoutAuto()
            sleep(0.5)
            #OFF到打开除霜
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 5})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
            #manual到打开除霜
            self.state_manual()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 5})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
            #AUTO到打开除霜
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 5})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})

    @pytest.mark.smoke
    @allure.title("设置远程空调上高压延长时长")
    @pytest.mark.failed
    def test_caseid_1979837(self):
        for X in [0, 1]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHVDelay", {"extendtime": 20})
            self.partner.empty_all(0.1)
            for Y in [0, 59]:
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetRemoteClimateSwitchToHVDelay", {"extendtime": Y})
                sleep(0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr63, 'RemStrtExtnTiReq', Y, timeout=0.5)
                sleep(1)

    @pytest.mark.sanity
    @allure.title("设置空调自动模式开启关闭_设置无效区域")
    def test_caseid_1979860(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 2, "on": True})
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        for state in [True, False]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": state})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAuto", 
                                                  {"zoneId":0}, {"out": {"zoneId":0, "isOn": state}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAuto", 
                                                {"zoneId":2}, {"out": {"zoneId":0, "isOn": state}})

    @pytest.mark.sanity
    @allure.title("设置空调OFF_设置无效区域")
    def test_caseid_1979861(self):
        for zone in [1, 3, 4, 5, 6, 7]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId": zone})
            sleep(0.1)
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
            
    @pytest.mark.sanity
    @allure.title("设置空调ON_设置无效区域")
    def test_caseid_1985967(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 0})
        self.partner.empty_all(0.5)
        for zone in [1, 3, 4, 5, 6, 7]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": zone})
            sleep(0.1)
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")

    @pytest.mark.sanity
    @allure.title("设置空调风速SetWindSpeed_设置无效值的情况")
    def test_caseid_1979862(self):
        self.set_four_seat_occupt(0, 1, 0, 0)
        for speed1 in range(1, 10): #manual下设置风速1-9
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": speed1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                  {"out": {"zoneId":1, "speed": speed1}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                  {"out": {"zoneId":2, "speed": speed1}})
        for speed2 in [10, 11, 12, 13, 14]:#manual下设置风速10-14
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": speed2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                  {"out": {"zoneId":1, "speed": 9}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                  {"out": {"zoneId":2, "speed": 9}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        for speed3 in [10, 11, 12, 13, 14]: #auto下设置风速10-14
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": speed3})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                  {"out": {"zoneId":1, "speed": speed3}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                  {"out": {"zoneId":2, "speed": speed3}})
        for speed4 in range(1, 10): #auto下设置风速1-9
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": speed4})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                  {"out": {"zoneId":1, "speed": 14}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                  {"out": {"zoneId":2, "speed": 14}})
        for zone in range(1): #无效区域
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":zone, "speed": 11})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                  {"out": {"zoneId":1, "speed": 14}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                  {"out": {"zoneId":2, "speed": 14}})

    @pytest.mark.sanity
    @allure.title("设置空调吹风模式_设置无效值的情况")
    def test_caseid_1979865(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        for mode in range(7):
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode": mode})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode": mode})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode": mode})
            sleep(0.1)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":2}, {"out": {"zoneId":2, "mode": mode}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":3}, {"out": {"zoneId":3, "mode": mode}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":4}, {"out": {"zoneId":4, "mode": mode}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode": 7}) #manual下设置小auto
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode": 7}) #manual下设置小auto
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode": 7}) #manual下设置小auto
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":2}, {"out": {"zoneId":2, "mode": 1}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":3}, {"out": {"zoneId":3, "mode": 1}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":4}, {"out": {"zoneId":4, "mode": 1}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":0, "mode": 1}) #区域无效
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":2}, {"out": {"zoneId":2, "mode": 1}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":3}, {"out": {"zoneId":3, "mode": 1}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindMode", {"zoneId":4}, {"out": {"zoneId":4, "mode": 1}})

    @pytest.mark.sanity
    @allure.title("设置空调温度(主/副/后排且联动空调开启)_无效值的情况")
    @pytest.mark.failed
    def test_caseid_1979866(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 23})
        sleep(0.1)
        info1 = ["HmiCmptmtTSpForRowFirstLe", "HmiCmptmtTSpForRowFirstRi", "HmiCmptmtTSpForRowSecLe", "HmiCmptmtTSpForRowSecRi"]
        info2 = ["HmiCmptmtTSpSpclForRowFirstLe", "HmiCmptmtTSpSpclForRowFirstRi", "HmiCmptmtTSpSpclForRowSecLe", "HmiCmptmtTSpSpclForRowSecRi"]
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":0, "value": 24})
        sleep(0.5)
        for Z in info1:
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, Z, 16)
        for Q in info2:
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, Q, 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": 10})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 10})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":4, "value": 10})
        sleep(0.1)
        for Z in info1:
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, Z, 16, timeout=0.5)
        for Q in info2:
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr15, Q, 0, timeout=0.5)
 
    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_convenience下设置主驾温度触发的所有现象")
    def test_caseid_1979989(self):
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(2)
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 23})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 23, "tempPassenger": 23, "tempSecRow": 23, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_convenience下设置副驾温度触发的所有现象")
    def test_caseid_1979990(self):
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(2)
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":4, "value": 23})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 23, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("状态机OFF带auto记忆切换到Auto_convenience下设置后排温度触发的所有现象")
    def test_caseid_1979991(self):
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(2)
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":2, "value": 23})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 23, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_打开主开关触发的所有现象")
    def test_caseid_1980007(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 0})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_打开后排开关触发的所有现象")
    def test_caseid_1980009(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 2})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_设置主驾温度触发的所有现象")
    def test_caseid_1980010(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 23})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 23, "tempPassenger": 23, "tempSecRow": 23, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_设置副驾温度触发的所有现象")
    def test_caseid_1980011(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":4, "value": 23})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 23, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_设置后排温度触发的所有现象")
    def test_caseid_1980012(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": 23})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 23, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_设置AC打开触发的所有现象")
    def test_caseid_1980013(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_改变前排风量触发的所有现象")
    def test_caseid_1980014(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":9})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow":9, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_改变主驾吹风模式触发的所有现象")
    def test_caseid_1980015(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":3})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":3, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_改变副驾吹风模式触发的所有现象")
    def test_caseid_1980016(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":3})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":3, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机OFF不带auto记忆切换到manual_改变后排吹风模式触发的所有现象")
    def test_caseid_1980018(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":3})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":3, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF不带auto记忆切换到manual_改变后排吹风模式触发的所有现象")
    def test_caseid_1980019(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
        sleep(0.2)
        self.state_off_withoutAuto()
        for X in[819, 1092, 1365]:
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', X)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF不带auto记忆切换到manual_改变出风口角度触发的所有现象")
    def test_caseid_1980022(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 8, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 9, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 10, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 11, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVent', {"zoneId": 12, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 100, "vertical":100}, 
                                                          {"id": 3, "side": 0, "horizontal": 100, "vertical":100}, {"id": 4, "side": 0, "horizontal": 100, "vertical":100}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("状态机auto换到OFF_关闭主开关触发的所有现象")
    def test_caseid_1980028(self):
        #此case1.4需要修改off下的吹风模式，应该为当前值，实际为记忆值
        self.state_Auto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId": 0})
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":True}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF不带auto记忆切换到manual_convenience下设置主驾温度触发的所有现象")
    def test_caseid_1980026(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetTemperature', {"zoneId":3, "value": 23})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 23, "tempPassenger": 23, "tempSecRow": 23, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机OFF带auto记忆切换到manual_设置座椅通风触发的所有现象")
    def test_caseid_1980027(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
        sleep(0.2)
        self.state_off_withoutAuto()
        self.partner.send_method_request(SEAT_SERVICE_CLIENT, "SetVentingLevel", 
                                             {"params": [{"id": 0, "uint8Info": 3}, {"id": 1, "uint8Info": 3}]})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 546)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机manual换到auto_设置循环模式为1auto触发的所有现象")
    def test_caseid_1980069(self):
        for X in [1, 0]:
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": X})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": X})

    @pytest.mark.sanity
    @allure.title("状态机manual换到除霜除雾_设置除霜除雾打开触发的所有现象")
    def test_caseid_1980071(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.state_manual()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机manual换到除霜除雾_convenience下设置空调吹窗触发的所有现象")
    def test_caseid_1980073(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.state_manual()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机manual换到除霜除雾_inactive下设置除霜除雾打开触发的所有现象")
    def test_caseid_1980072(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("状态机manual换到OFF_设置主开关OFF触发的所有现象")
    def test_caseid_1980074(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机manual换到OFF_设置后排OFF触发的所有现象")
    def test_caseid_1980075(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到OFF_设置主开关OFF触发的所有现象")
    def test_caseid_1980077(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        sleep(0.2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("状态机由auto到除霜除雾再换到OFF_设置主开关OFF触发的所有现象")
    def test_caseid_1980078(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机由除霜除雾换到OFF_切换使用者模式为1触发的所有现象")
    def test_caseid_1980079(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.sd_tester.change_usage_mode(1)
            sleep(0.2)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到manual_设置主驾吹风模式触发的所有现象")
    def test_caseid_1980080(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            for Y in [0, 1, 3, 4, 5, 6]:
                logger.info(f"----循环模式切换为{Y}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":Y})
                sleep(0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":Y, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机除霜除雾换到manual_设置副驾吹风模式触发的所有现象")
    def test_caseid_1980083(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            for Y in range(7):
                logger.info(f"----吹风模式切换为{Y}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":Y})
                sleep(0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                        "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                        "windSpeedSecRow":6, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                        "airModePassenger":{"mode":Y, "isWindModeAuto":False}, 
                                                        "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("逆向测试_状态机除霜除雾换到manual_设置后排吹风模式触发的所有现象")
    def test_caseid_1980084(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            for Y in range(7):
                logger.info(f"----吹风模式切换为{Y}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":Y})
                sleep(0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                        "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                        "windSpeedSecRow":6, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                        "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                        "airModeSecRow":{"mode":Y, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到manual_设置除雾除霜关闭触发的所有现象")
    def test_caseid_1980085(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":False})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到manual_设置后排开关打开触发的所有现象")
    def test_caseid_1980086(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 2})
            sleep(0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @allure.title("状态机除霜除雾换到manual_设置后排温度打开触发的所有现象")
    def test_caseid_1980087(self):
        for X in [2, 11, 13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on":True})
            sleep(0.2)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":3, "mode":2})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":4, "mode":2})
            sleep(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
            sleep(0.5)
            for Y in [0, 1, 16, 28]:
                logger.info(f"--设置后排温度{Y}")
                self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": Y})
                sleep(0.5)
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                        "tempDriver": 22, "tempPassenger": 22, "tempSecRow": Y, "windSpeedFirRow": 6, 
                                                        "windSpeedSecRow":6, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                        "airModePassenger":{"mode":2, "isWindModeAuto":False}, 
                                                        "airModeSecRow":{"mode":2, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": False})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
                self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 3})

    @pytest.mark.sanity
    @pytest.mark.restart
    @allure.title("状态机Auto时，记忆重启前的所有空调设置")
    def test_caseid_1979931(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 3})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 2, "mode": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 3, "mode": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 4, "mode": 1})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 50, "vertical":50}, 
                                                          {"id": 3, "side": 0, "horizontal": 50, "vertical":50}, {"id": 4, "side": 0, "horizontal": 50, "vertical":50}]})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 1, "horizontal": 50, "vertical":50}, 
                                                          {"id": 3, "side": 1, "horizontal": 50, "vertical":50}, {"id": 4, "side": 1, "horizontal": 50, "vertical":50}]})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        sleep(1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 0)
        sleep(1)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":0, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":0, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":0, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"mode":1, "leftHorizontal":50, 
                                                                                "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                               "passVentStatus": {"mode":1, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                        "secRowVentStatus":{"mode": 1, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out":2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out":1})

    @pytest.mark.sanity
    @pytest.mark.restart
    @allure.title("状态机manual时，记忆重启前的所有空调设置")
    def test_caseid_1980006(self):
        self.sd_tester.change_usage_mode(2)
        self.state_manual()
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out":1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 3})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 2, "mode": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 3, "mode": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 4, "mode": 1})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 50, "vertical":50}, 
                                                          {"id": 3, "side": 0, "horizontal": 50, "vertical":50}, {"id": 4, "side": 0, "horizontal": 50, "vertical":50}]})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 1, "horizontal": 50, "vertical":50}, 
                                                          {"id": 3, "side": 1, "horizontal": 50, "vertical":50}, {"id": 4, "side": 1, "horizontal": 50, "vertical":50}]})
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"mode":1, "leftHorizontal":50, 
                                                                                "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                            "passVentStatus": {"mode":1, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                        "secRowVentStatus":{"mode": 1, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out":1})

    @pytest.mark.sanity
    @pytest.mark.restart
    @allure.title("状态机除雾除霜时，记忆重启前的所有空调设置")
    def test_caseid_1979935(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 3})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 2, "mode": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 3, "mode": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetAirVentMode', {"zoneId": 4, "mode": 1})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 0, "horizontal": 50, "vertical":50}, 
                                                          {"id": 3, "side": 0, "horizontal": 50, "vertical":50}, {"id": 4, "side": 0, "horizontal": 50, "vertical":50}]})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'SetOutletAngle', 
                                             {"outlets": [{"id": 2, "side": 1, "horizontal": 50, "vertical":50}, 
                                                          {"id": 3, "side": 1, "horizontal": 50, "vertical":50}, {"id": 4, "side": 1, "horizontal": 50, "vertical":50}]})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"mode":1, "leftHorizontal":50, 
                                                                                "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                               "passVentStatus": {"mode":1, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                        "secRowVentStatus":{"mode": 1, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out":1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out":3})

    @pytest.mark.full
    @pytest.mark.restart
    @allure.title("设置A/C禁止开启_遍历_默认值及get和notify")
    def test_caseid_1981118(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out": {"acStatus":False, "acInhibitSts": False}})
        self.ipdu.resume_all_bus_send()
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":False, "acInhibitSts": True}})
        sleep(2)#140AB存在bug
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out": {"acInhibitSts": True}})
        sleep(2)#3S后禁用主动关闭
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":False, "acInhibitSts": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":True, "acInhibitSts": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetACInhibit", {"isOn": True})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":False, "acInhibitSts": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out": {"acStatus":False, "acInhibitSts": True}})
        
    @pytest.mark.full
    @pytest.mark.restart
    @allure.title("空调服务重启上电event")
    def test_caseid_1984308(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr02, 'IntPm25VluFrmClima', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh1Id',  0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh2Id',  0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragRefreshPopUp', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'FragCh3Id',  0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr11, 'ClimaDefrstSts', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'EcoClimaSts', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntCmptmtTFrnt', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr08, 'CmptmtTFrntQf', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdQf', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr28, 'AmbTEstimdAmbTEstimd', 0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'EmotCooltIndcnReq', 0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr22, 'BattCooltIndcnReq', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'IntPm25StsFrmClima', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr01, 'IntPm25LvlFrmClima', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'IntPm25HiPopUp', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyOutdAirQly', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'LvlOfClimaCmft', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'RemClimaWarn', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr29, 'OutdAirQlyQf', 0)
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyAQSInfo", {"info":{"level":0, "isValid":False, "zone":0}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "PM25", {"info": {"status":0, "level":0, "value": 0, "warning":0}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "coolantLowWarnInfo", {"info":{"eMotion":False, "battery":False}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyAmbientTempRawData", {"data":{"temp": -70, "unit":0, "isValid": False}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "Temperature", {"info":{"zoneId":0, "value": -60, "isValid":False}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateECOSts", {"sts": 0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyACDefrostSts", 
                                  {"sts":{"defrostMax": False, "climateDefrost": False}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateHVStatus", {"sts": 0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemoteClimateHVDelayStatus", {"extendSts": 0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, "isOn":False, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "RemotePowerStatus", {"status": 0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateFault", {"faults":[{"faultId":0, "faultMsg":""}]})

    @pytest.mark.sanity
    @pytest.mark.restart
    @allure.title("空调服务所有获取接口的上电默认值")
    def test_caseid_1979843(self):
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetDefrostSts", {}, {"out": {"defrostMax": False, "climateDefrost": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetEcoMode", {}, {"out": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCurrentTemperature", {"zoneId": 0}, {"out": {"value": 255, "isValid": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "getAmbientTempRawData", {}, {"out": {"temp": 0, "unit": 0, "isValid": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "getCoolantLowWarnInfo", {}, {"out": {"eMotion": False, "battery": False}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetFragranceInfo", {}, 
                                                {"out":{"isRefreshOn":False, "isUseup":[False, False, False], "channelId":[255, 255, 255], "leftTime":[0, 0, 0, 0, 0]}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Value", {}, {"out": 65535})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Level", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAQSLevel", {}, {"out": 0})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetPM25Info", {}, {"out": {"status":0, "level":0, "value": 65535, "warning":0}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAQSInfo", {}, {"out": {"level":0, "isValid":False, "zone": 0}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out": {"status": 255}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateFault", {}, {"out": [{"faultId": 0, "faultMsg": ""}]})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateSwitchToHVReceiveFeedback", {}, {"out": 255})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateHVStatus", {}, {"out": 255})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateHVDelayStatus", {}, {"out": 255})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteClimateSwitchToHVDelayReceiveFeedback", {}, {"out": 255})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemotePowerStatus", {}, {"out": 255})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetRemoteOnOffReceiveFeedback", {}, {"out": 255})
        self.ipdu.resume_all_bus_send()

    @pytest.mark.sanity
    @pytest.mark.restart
    @allure.title("通知和获取空调状态机当前模式_OFF切换到manual的情况")
    def test_caseid_1979825(self):
        #状态机为manual且重启时
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为OFF且Auto无记忆时
        self.state_off_withoutAuto()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0}, timeout=1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为OFF且Auto无记忆时
        self.state_off_withoutAuto()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为OFF且Auto无记忆时
        for X in [2, 3, 4]:
            self.state_off_withoutAuto()
            sleep(1)
            logger.info(f"------设置温度区域为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":X, "value": 16}, timeout=1)
            sleep(1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        #状态机为OFF且AUto无记忆时，展车模式未打开时
        self.state_off_withoutAuto()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True}, timeout=1)
        sleep(1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        ##当状态机为OFF且AUto无记忆时，
        for X in range(1, 10):
            self.state_off_withoutAuto()
            sleep(1)
            logger.info(f"------设置前排风速为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": X}, timeout=0.5)
            sleep(1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
        ##当状态机为OFF且AUto无记忆时，
        for X in [2, 3, 4]:
            self.state_off_withoutAuto()
            sleep(1)
            logger.info(f"------设置吹风模式为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":X, "mode": 7}, timeout=0.6)
            sleep(1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1}, timeout=0.5)

    @pytest.mark.sanity
    @pytest.mark.restart
    @allure.title("通知和获取空调状态机当前模式_OFF切到Auto的情况")
    def test_caseid_1979828(self):
        #状态机Auto情况下重启
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(1)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        #状态机off带auto时，调用接口on
        self.state_off_withAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 0})
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        #状态机off不带auto时，设置空调自动打开
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        #状态机为OFFd带auto时，设置后排温度
        for X in [2, 3, 4]:
            self.state_off_withAuto()
            sleep(0.5)
            logger.info(f"-------设置温度为{X}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":X, "value": 1})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        #状态机为OFFd带auto时，设置前排温度
        self.state_off_withAuto()
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        #状态机为OFFd带auto时，设置AC
        self.state_off_withAuto()
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        #状态机为OFFd带auto时，打开后排开关
        self.state_off_withAuto()
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId": 2})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})

    @pytest.mark.full
    @allure.title("空调起雾优化_湿度信号大于85下发自动循环模式重启BGM的表现")
    @pytest.mark.failed
    def test_caseid_1984101(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        sleep(0.1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr25, 'FrntHvacBlowerSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM2', 85)
        sleep(0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 3, timeout=0.5)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetCycleMode", {"mode": 2})
        sleep(1)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(2)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacRecircCmd', 1, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                    "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "CycleMode", {"mode": 2})

    @pytest.mark.full
    @pytest.mark.restart
    @allure.title("BGM出厂空调默认设置项")
    def test_caseid_1979951(self):
        # 删除数据库
        self.del_s2s_db()
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)#auto，除霜除雾吹风模式=1
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(1)
        #获取空调首次下线设置
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": True, "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, 
                                                       "windSpeedFirRow": 12, "windSpeedSecRow":12, 
                                                       "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                       "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out":1}) #内外循环
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":8}, {"out":True}) #风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":9}, {"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":10}, {"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":11}, {"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAirVent", {"zoneId":12}, {"out":True})#风口
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetOutletStatus", {}, {"out":{"driverVentStatus":{"mode":0, "leftHorizontal":50, 
                                                                                "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                               "passVentStatus": {"mode":0, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}, 
                                                                               "secRowVentStatus":{"mode": 0, "leftHorizontal":50, "leftVertical":50, "rightHorizontal":50, "rightVertical":50}}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out":2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetAutoSyncMode", {}, {"out": True}) #温度同步
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'HMIClimaEgySaveReq', 0, timeout=0.5) #节能模式关闭
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr46, 'HmiFragraLvlReq', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr48, 'TelmAirFragTasteReq', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh1', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh2', 0, timeout=0.5) #香氛
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr51, 'HmiFragraChRatReqFragRatForCh3', 0, timeout=0.5) #香氛

    @pytest.mark.smoke
    @pytest.mark.restart
    @allure.title("出厂默认值_auto到Manual")
    def test_caseid_1987248(self):
        # 删除数据库
        self.del_s2s_db()
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)#auto，除霜除雾吹风模式=1
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(1)
        #获取空调首次下线设置
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": True, "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, 
                                                       "windSpeedFirRow": 12, "windSpeedSecRow":12, 
                                                       "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                       "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, 
                                              {"out":{"acStatus": True, "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, 
                                                       "windSpeedFirRow": 4, "windSpeedSecRow":4, 
                                                       "airModeDriver":{"mode":6, "isWindModeAuto":False}, 
                                                       "airModePassenger":{"mode":4, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":4, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})  
        
    @allure.title("AUTO模式支持5挡风调节策略_auto下设置10-14档保持auto")
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1984923(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        for level in [10, 11, 12, 13, 14]:
            self.state_Auto()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":level})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":level})
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                "windSpeedSecRow":level, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                    "windSpeedSecRow":level, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": level}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": level}})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', level, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', level, timeout=0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
            sleep(0.1)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                "windSpeedSecRow":level, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
    
    @allure.title("AUTO模式支持5挡风调节策略_manual下设置前排风速为10-14")
    @pytest.mark.full
    def test_caseid_1984932(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.partner.empty_all(1)
        for level in [10, 11, 12, 13, 14]:
            logger.info(f"发送风速{level}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":level})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":level})
            sleep(0.2)
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 6}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 6}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 1})
            
    @allure.title("AUTO模式支持5挡风调节策略_off带不auto记忆设置前后排风速为10-14")
    @pytest.mark.full
    def test_caseid_1984936(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_off_withoutAuto()
        self.partner.empty_all(0.5)
        for level in range(1, 10):
            logger.info(f"发送风速{level}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":level})
            sleep(0.2)
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        for level in [10, 11, 12, 13, 14]:
            logger.info(f"发送风速{level}")
            self.state_off_withoutAuto()
            self.partner.empty_all(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":level})
            sleep(0.2)
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
            
    @allure.title("AUTO模式支持5挡风调节策略_off到manual到auto到除霜除雾到auto")
    @pytest.mark.full
    def test_caseid_1984944(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_off_withoutAuto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":2})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 2, 
                                                "windSpeedSecRow":2, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":13})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                                "windSpeedSecRow":13, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                                "windSpeedSecRow":13, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            
    @allure.title("AUTO模式支持5挡风调节策略_off带auto记忆分别设置前后排风速为10-14")
    @pytest.mark.full
    def test_caseid_1984933(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_off_withAuto()
        self.partner.empty_all(0.5)
        for level in [10, 11, 12, 13, 14]:
            logger.info(f"发送风速{level}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":level})
            sleep(0.2)
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        for level in [10, 11, 12, 13, 14]:
            logger.info(f"发送风速{level}")
            self.state_off_withAuto()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":level})
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                "windSpeedSecRow":level, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": level}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": level}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            
    @allure.title("AUTO模式支持5挡风调节策略_auto下设置前排风速为0-9")
    @pytest.mark.full
    def test_caseid_1984926(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_Auto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":14})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":14})
        self.partner.empty_all(1)
        for level in range(10):
            logger.info(f"发送风速{level}")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":level})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":level})
            sleep(0.2)
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": 14}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 14}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            
    @allure.title("AUTO模式支持5挡风调节策略_auto5挡风断电重启保持")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1984929(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_Auto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":14})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                "windSpeedSecRow":14, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                "windSpeedSecRow":14, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                    "windSpeedSecRow":14, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})

    @allure.title("AUTO模式支持5挡风调节策略_auto切换到OFF再到Auto")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984931(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_Auto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":14})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 0, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":10})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 10, 
                                                "windSpeedSecRow":10, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})

    @allure.title("AUTO模式支持5挡风调节策略_auto切换到manual再到Auto")
    @pytest.mark.full
    def test_caseid_1985495(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":14})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                "windSpeedSecRow":14, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            
    @allure.title("AUTO模式支持5挡风调节策略_auto切换到除霜除雾再到auto")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984928(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_Auto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":14})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":2, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 9, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 0, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 5})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(0.2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 14, 
                                                "windSpeedSecRow":14, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', 14, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 14, timeout=0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            
    @allure.title("AUTO模式支持5挡风调节策略_auto下后排开关OFF再打开保持auto")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984927(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        for level in [10, 11, 12, 13, 14]:
            logger.info(f"发送风速{level}")
            self.state_Auto()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":level})
            self.partner.empty_all(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
            self.partner.empty_all(0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":level})
            self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                "windSpeedSecRow":level, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": level}})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', level, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', level, timeout=0.5)
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            
    @allure.title("AUTO模式支持5挡风调节策略_auto下后排开关OFF设置10-14档保持auto")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984924(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        for level in [10, 11, 12, 13, 14]:
            logger.info(f"发送风速{level}")
            self.state_Auto()
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":level})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":level})
            sleep(0.2)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True, 
                                                    "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                    "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                    "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": level}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": 0}})
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlFrnt', level, timeout=0.5)
            self.ipdu.check(self.ipdu.bodycan.CEMBodyFr14, 'HmiHvacFanLvlRe', 0, timeout=0.5)
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
            sleep(0.1)
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":0, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
            self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
            self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": level, 
                                                "windSpeedSecRow":level, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 1}, 
                                                {"out": {"zoneId":1, "speed": level}})
            self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetWindSpeed", {"zoneId": 2}, 
                                                {"out": {"zoneId":2, "speed": level}})
            
    @allure.title("AUTO模式支持5挡风调节策略_auto下后排开关因占位不会导致OFF的情况")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984925(self):
        self.set_four_seat_occupt(0, 1, 1, 1) #其余四座不占位
        self.seat_belt_status(1, 0, 0, 0, 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.2)
        self.state_Auto()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":13})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":2, "speed":13})
        sleep(0.2)
        self.set_four_seat_occupt(0, 0, 0, 0)
        self.seat_belt_status(0, 0, 0, 0, 0)
        sleep(5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                                "windSpeedSecRow":13, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": False})
        sleep(0.1)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                            "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                            "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                            "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                            "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                            "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                            "windSpeedSecRow":13, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                            "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                            "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True,
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 13, 
                                                "windSpeedSecRow": 13, "airModeDriver": {"mode":1, "isWindModeAuto": True},
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True},
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        
    @pytest.mark.full
    @allure.title("后排无人关闭后排空调策略_auto下&temp1_设置后排吹风模式进入Maunal下座椅占位")
    def test_caseid_1988213(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_off_withAuto()
        self.set_four_seat_occupt(0, 0, 0, 0)#全部未占位
        self.seat_belt_status(0, 0, 0, 0, 0)#全部安全带未系
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,"SetWindMode",{"zoneId": 2, "mode": 1})
        self.partner.ck_coming_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow": 6, "airModeDriver": {"mode":1, "isWindModeAuto": False},
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False},
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        self.partner.empty_all(0.5)
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False,
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow": 6, "airModeDriver": {"mode":1, "isWindModeAuto": False},
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False},
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        self.partner.empty_all(0.5)
        self.set_four_seat_occupt(0, 0, 1, 0, sleeptime=0)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": False,
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow": 6, "airModeDriver": {"mode":1, "isWindModeAuto": False},
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False},
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
      
    @pytest.mark.full
    @allure.title("后排无人关闭后排空调策略_OFF到AUTO后排离坐5s再占位")
    def test_caseid_1988214(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_off_withAuto()
        self.set_four_seat_occupt(0, 0, 0, 0)#全部未占位
        self.seat_belt_status(0, 0, 0, 0, 0)#全部安全带未系
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed":12})
        self.partner.ck_coming_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True},
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True},
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        self.partner.empty_all(0.5)
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True,
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True},
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True},
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        self.partner.empty_all(0.5)
        self.set_four_seat_occupt(0, 0, 1, 0, sleeptime=0)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateSystemStatus", {}, {"out":{"acStatus": True,
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow":12, 
                                                "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True},
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True},
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        
    @allure.title("Manual状态机下后排开关因无占位不会导致OFF的情况")
    @pytest.mark.full
    def test_caseid_1988181(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.set_four_seat_occupt(0, 1, 1, 1) #其余四座不占位
        self.seat_belt_status(1, 0, 0, 0, 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.set_four_seat_occupt(0, 0, 0, 0)
        self.seat_belt_status(0, 0, 0, 0, 0)
        self.partner.empty_all(0.5)
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
   
    @allure.title("Manual切auto状态机下后排开关不会因为无占位导致OFF的情况")
    @pytest.mark.full
    def test_caseid_1988183(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.set_four_seat_occupt(0, 1, 1, 1) #其余四座不占位
        self.seat_belt_status(1, 0, 0, 0, 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow":6, "airModeDriver":{"mode":1, "isWindModeAuto":False}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":False}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.set_four_seat_occupt(0, 0, 0, 0)
        self.seat_belt_status(0, 0, 0, 0, 0)
        self.partner.empty_all(0.5)
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.set_four_seat_occupt(0, 1, 1, 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow":12, "airModeDriver":{"mode":1, "isWindModeAuto":True}, 
                                                "airModePassenger":{"mode":1, "isWindModeAuto":True}, 
                                                "airModeSecRow":{"mode":1, "isWindModeAuto":True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(1)
        self.set_four_seat_occupt(0, 0, 0, 0)
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @allure.title("获取和通知座舱通风状态_默认值")
    def test_caseid_1985218(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentReqRspnFb', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentActvSts', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr58, 'RemVentWarnSts', 0)
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCockpitVentStatus", {}, 
                                              {"out": {"feedback":255, "ventSts":255, "ventWarnSts":255}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "CockpitVentStatus", 
                                            {"vent": {"feedback":0, "ventSts":0, "ventWarnSts":0}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCockpitVentStatus", {}, 
                                              {"out": {"feedback":0, "ventSts":0, "ventWarnSts":0}})
        
    @pytest.mark.sanity
    @allure.title("状态机auto换到manual_改变循环模式=7触发的所有现象")
    def test_caseid_1985767(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(0.1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 2, "mode": 7})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 3, "mode": 7})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId": 4, "mode": 7})
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.partner.empty_all(0.5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateMode", {}, {"out": 2})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetCycleMode", {}, {"out": 1})
 
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _请求下发后重启bgm")
    def test_caseid_1987138(self):  
        self.state_manual()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})      
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 1})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow": 6, "airModeDriver": {"mode":1, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)   
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "NotifyClimateMode", {"mode": 5})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)

    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭_auto下进入除雾除霜，退出除雾除霜回auto")
    def test_caseid_1986138(self): 
        self.state_off_withAuto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        sleep(1)
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _状态机为除雾除霜&uasge上切")
    def test_caseid_1986150(self): 
        self.sd_tester.change_usage_mode(1) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(1)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(1) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.sd_tester.change_usage_mode(11)
        sleep(1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _状态机为OFF记忆值auto&uasge上切")
    def test_caseid_1986142(self): 
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(1) 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 1)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmDefrostReq', 2,timeout=1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr92, 'TelmDefrostReq', 0, timeout=0.5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _状态机为OFF&uasge上切")
    def test_caseid_1986147(self): 
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _状态机为manual&uasge上切")
    def test_caseid_1986149(self): 
        self.state_manual()
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        
    @pytest.mark.sanity
    @allure.title("设置除霜模式开启关闭 _状态机为auto&uasge上切")
    def test_caseid_1986148(self): 
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(1) 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 1)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus") 
 
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _未满足接口调用_信号置0触发除霜除雾")
    def test_caseid_1986136(self): 
        self.state_off_withAuto()
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 1)
        self.sd_tester.change_usage_mode(1) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        sleep(2)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _状态机为manual&uasge上切")
    def test_caseid_1987166(self): 
        self.state_manual()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})    
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")  
        self.sd_tester.change_usage_mode(0)    
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus") 
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})        
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)      
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus") 
                                
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭_除雾除霜关闭开启")
    def test_caseid_1986137(self): 
        self.state_manual()
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})    
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False}) 
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow": 6, "airModeDriver": {"mode":1, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})  
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _重复下发除雾除霜开启请求")
    def test_caseid_1987157(self): 
        self.state_manual()
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})    
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})   
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @allure.title("设置除霜模式开启关闭 _500ms信号时延内从off到on")
    def test_caseid_1986139(self): 
        self.state_manual()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 1)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True}) 
        sleep(1)   
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31, 'RemClimaDefrstSts', 0)
        sleep(0.1)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 9, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)

    @pytest.mark.full
    @allure.title("设置远程开启空调 _请求下发后重启bgm")
    def test_caseid_1987137(self): 
        self.state_off_withAuto()
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(1) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.sd_tester.change_usage_mode(11) 
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 0, 
                                                "windSpeedSecRow": 0, "airModeDriver": {"mode":1, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": False, "secondRowPowerStatus": False}}, timeout=3)       

    @pytest.mark.full
    @allure.title("设置远程开启空调 _远控请求后卡500ms重置信号再切usage")
    def test_caseid_1987158(self):
        self.state_off_withAuto() 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {}) 
        sleep(0.5) 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0) 
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {}) 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0) 
        sleep(2)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
    
    @pytest.mark.full
    @allure.title("设置远程开启空调 _记忆值为Manual下调用")
    def test_caseid_1987134(self): 
        self.set_four_seat_occupt(0, 0, 0, 0)
        self.seat_belt_status(0, 0, 0, 0, 0)
        self.state_manual()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 16})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.sd_tester.change_usage_mode(2) 
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 16, "tempPassenger": 16, "tempSecRow": 16, "windSpeedFirRow": 6, 
                                                "windSpeedSecRow": 6, "airModeDriver": {"mode":1, "isWindModeAuto": False}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        self.partner.empty_all(1)   
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOff', {})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmClimaReqSP", [2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
    
    @pytest.mark.smoke
    @allure.title("设置远程开启空调 _记忆值为auto下调用")
    def test_caseid_1987133(self): 
        self.state_off_withAuto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.sd_tester.change_usage_mode(1) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.sd_tester.change_usage_mode(2) 
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                                "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                                "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                                "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                                "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
        self.partner.empty_all(1)        
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @allure.title("设置远程开启空调 _状态机为auto下调用")
    def test_caseid_1987136(self): 
        self.state_off_withAuto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.sd_tester.change_usage_mode(2) 
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmClimaReqSP", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
     
    @pytest.mark.full
    @allure.title("设置远程开启空调 _状态为除雾除霜下调用")
    def test_caseid_1987135(self): 
        self.state_off_withAuto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.sd_tester.change_usage_mode(2) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 25})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                            "tempDriver": 25, "tempPassenger": 25, "tempSecRow": 25, "windSpeedFirRow": 9, 
                                            "windSpeedSecRow": 0, "airModeDriver": {"mode":2, "isWindModeAuto": False}, 
                                            "airModePassenger": {"mode": 1, "isWindModeAuto": False}, 
                                            "airModeSecRow": {"mode": 1, "isWindModeAuto": False}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": False}}, timeout=3)
        self.sd_tester.change_usage_mode(2) 
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        sleep(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                            "tempDriver": 25, "tempPassenger": 25, "tempSecRow": 25, "windSpeedFirRow":12, 
                                            "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                            "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                            "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
       
    @pytest.mark.full
    @allure.title("设置远程开启空调 _inactive下设置除雾除霜关闭除雾除霜下发远控开启上切usage")
    def test_caseid_1987203(self): 
        self.state_off_withAuto()
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        sleep(0.4)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.sd_tester.change_usage_mode(2) 
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                            "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow": 12, 
                                            "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                            "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                            "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)     
       
    @pytest.mark.full   
    @allure.title("设置远程开启空调 _报文发0时切变信号")
    def test_caseid_1987132(self): 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                            "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow":12, 
                                            "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                            "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                            "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)

    @pytest.mark.full
    @allure.title("设置远程开启空调 _下发远控开启后关闭空调上切usage")
    def test_caseid_1987165(self):
        self.sd_tester.change_usage_mode(11) 
        self.io.set_four_door_close()
        self.del_s2s_db()
        self.kill_s2s_and_reconnect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        sleep(3)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
      
    @pytest.mark.full
    @allure.title("设置远程开启空调_重置信号时延内改变信号")
    def test_caseid_1986132(self): 
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                            "tempDriver": 22, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow":12, 
                                            "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                            "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                            "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)
    
    @pytest.mark.full
    @allure.title("设置远程开启空调_不改变温度同步")
    def test_caseid_1987167(self): 
        self.state_off_withAuto()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr21, 'ResrvdSigForECM4', 273)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": False}) 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 25})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOn', {})
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True, 
                                            "tempDriver": 25, "tempPassenger": 22, "tempSecRow": 22, "windSpeedFirRow":12, 
                                            "windSpeedSecRow": 12, "airModeDriver": {"mode":1, "isWindModeAuto": True}, 
                                            "airModePassenger": {"mode": 1, "isWindModeAuto": True}, 
                                            "airModeSecRow": {"mode": 1, "isWindModeAuto": True}, 
                                            "firstRowPowerStatus": True, "secondRowPowerStatus": True}}, timeout=3)

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_服务初始化")
    def test_caseid_1988351(self): 
        self.kill_s2s_and_reconnect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制热后设置极速制冷温度")
    def test_caseid_1988389(self): 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":True}})
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        
    @pytest.mark.smoke
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制热")
    def test_caseid_1988353(self):    
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":True}})
               
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷，调用RemoteOff后300ms内调用On")
    def test_caseid_1988359(self):   
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOff', {})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, 'RemoteOff', {}, timeout=0.3)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetMaxCoolingHeatingInfo", {},{"out": {"maxCoolingSts" :False,"maxHeatingSts":False}})
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷，RemClimaActv10s内跳变")
    def test_caseid_1988357(self):   
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(3)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})
        self.partner.empty_all(0.5) 
        sleep(4)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetMaxCoolingHeatingInfo", {},{"out": {"maxCoolingSts" :False,"maxHeatingSts":False}})      

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷，10s后RemClimaAct为1")
    def test_caseid_1988355(self):  
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(10)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetMaxCoolingHeatingInfo", {},{"out": {"maxCoolingSts" :False,"maxHeatingSts":False}})      
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷后调用远程除雾除霜开启")
    def test_caseid_1988367(self):  
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷后调用RemoteOn")
    def test_caseid_1988364(self):  
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOn", {})
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo")
        
    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制热后设置相同温度&不同温度")
    def test_caseid_1988369(self):  
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":True}})    
        self.partner.empty_all(0.5)
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value":1})
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetMaxCoolingHeatingInfo", {},{"out": {"maxCoolingSts" :False,"maxHeatingSts":True}})         
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 20})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})    
    
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷后设置极速制热温度")
    def test_caseid_1988388(self):  
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})    
        sleep(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 1})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})   
 
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷后在开启极速制热")
    def test_caseid_1988363(self):    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})    
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})    
        sleep(2)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetMaxCoolingHeatingInfo",{},{"out":{"maxCoolingSts" :False,"maxHeatingSts":False}})  
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷，2s后上切usage")
    def test_caseid_1988356(self):  
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})    
        sleep(2) 
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})    
        
    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制冷")
    def test_caseid_1988352(self):  
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})  
  
    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_关闭极速制冷")
    def test_caseid_1988354(self):   
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":False}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetMaxCoolingHeatingInfo",{},{"out":{"maxCoolingSts" :False,"maxHeatingSts":False}})  
  
    @pytest.mark.smoke
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭inactive下调用")
    def test_caseid_1988313(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                       {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}})  

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_重启后1温度不做记忆")
    def test_caseid_1988331(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后远程关闭空调")
    def test_caseid_1988321(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOff", {})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )
   
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后调用除雾除霜开启再关闭")
    def test_caseid_1988322(self):    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on":True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on":False})
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后调用除雾除霜开启")
    def test_caseid_1988323(self):     
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on":True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后调用RemoteOff，上切usage")
    def test_caseid_1988257(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOff", {})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后调用RemoteOff后调RemoteOn")
    def test_caseid_1988326(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOff", {})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOn", {})
        sleep(0.2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )    
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  ) 
      
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后设置温度等于记忆值")
    def test_caseid_1988324(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 20})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后设置温度等于1")
    def test_caseid_1988329(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 1})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )
        
    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后关闭极速制热")
    def test_caseid_1988332(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":False}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后上切usage后关闭极速制热")
    def test_caseid_1988312(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 1})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":False}})
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制热后上切convenience再下切inactive")
    def test_caseid_1988333(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
       
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_温度不同步进入极速制热后温度")
    def test_caseid_1988318(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  ) 
        self.sd_tester.change_usage_mode(1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  ) 
    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_RemClimaActv信号跳变,上切usage")
    def test_caseid_1988315(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv',0)
        self.partner.empty_all(0.5)  
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)   
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )  
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)   
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  ) 
        sleep(2)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)  
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_convenience下调用极速制热然后下切inactive")
    def test_caseid_1988305(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)  
        sleep(0.5) 
        self.sd_tester.change_usage_mode(1)  
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )  
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_convenience下调用")
    def test_caseid_1988339(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.sd_tester.change_usage_mode(2)    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )  
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_10s内RemClimaActv未置为1")
    def test_caseid_1988316(self): 
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})   
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow":0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )  
        sleep(10)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", 
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                   "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                    ) 
        self.partner.empty_all(0.5)  
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus") 

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_重启后0温度不做记忆")
    def test_caseid_1988225(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_进入极速制冷后远程关闭空调")
    def test_caseid_1988277(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOff", {})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_进入极速制冷后调用除雾除霜开启再关闭")
    def test_caseid_1988276(self):    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on":True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on":False})
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_进入极速制冷后调用除雾除霜开启")
    def test_caseid_1988266(self):    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on":True})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                    {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                    "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                    "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                     )
    
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制冷后调用RemoteOff后调RemoteOn")
    def test_caseid_1988258(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.empty_all(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOff", {})
        sleep(0.2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "RemoteOn", {})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )    
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  ) 
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_记忆值1调用极速制热上切usage")
    def test_caseid_1988314(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 1})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)   
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow": 1, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制冷后设置温度等于记忆值")
    def test_caseid_1988262(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 20})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_进入极速制冷后设置温度等于0")
    def test_caseid_1988261(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperature", {"zoneId":3, "value": 0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )

    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制冷后关闭极速制冷")
    def test_caseid_1988224(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":False}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制热开启关闭_进入极速制冷后上切convenience再下切inactive")
    def test_caseid_1988223(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_记忆值0调用极速制冷上切usage")
    def test_caseid_1988229(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)   
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  )
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )
 
    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_温度不同步进入极速制冷后温度")
    def test_caseid_1988282(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  ) 
        self.sd_tester.change_usage_mode(1)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  ) 
    @pytest.mark.smoke
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_inactive下调用")
    def test_caseid_1988202(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  ) 

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_convenience下调用极速制冷然后下切inactive")
    def test_caseid_1988217(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)  
        sleep(1)  
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [])    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  ) 
    
    @pytest.mark.full
    @pytest.mark.jishu2  
    @allure.title("设置极速制冷开启关闭_convenience下调用")
    def test_caseid_1988204(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [])    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )  

    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_active下调用")
    def test_caseid_1988206(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(11)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [])    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 12, "windSpeedSecRow": 12, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  ) 
       
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_RemClimaActv信号跳变，上切usage")
    def test_caseid_1988302(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)    
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [1, 1, 1, 1, 1, 0, 0, 0, 0, 0])    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  ) 
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0) 
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                   "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                    ) 
        self.partner.empty_all(0.5)
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1) 
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
  
    @pytest.mark.full
    @pytest.mark.jishu2      
    @allure.title("设置极速制冷开启关闭_driving下调用")
    def test_caseid_1988206(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('TelmClimaReqSP', [])    
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20, 
                                                                   "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
                                                                 "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
                                                                  )         

    @pytest.mark.sanity
    @pytest.mark.jishu2
    @allure.title("设置极速制冷开启关闭_10s内RemClimaActv未置为1")
    def test_caseid_1988296(self): 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(10)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
                                                                   {"status":{"tempDriver": 0, "tempPassenger": 0, "tempSecRow": 0, 
                                                                   "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
                                                                 "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
                                                                  ) 
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)       
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus")
        
    @pytest.mark.full
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_调用极速制冷后调用极速制热10s触发远控信号")
    def test_caseid_1988424(self): 
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 0)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        sleep(9)  
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1) 
        sleep(3)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})    
 
    # @pytest.mark.full
    # @pytest.mark.jishu2
    # @allure.title("设置极速制热开启关闭_开启极速制热/制冷后调用SetTemperatureAndOn")
    # def test_caseid_1988450(self): 
    #     self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
    #     self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAutoSyncMode", {"on": True})
    #     self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
    #     self.sd_tester.change_usage_mode(1)
    #     self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)  
    #     sleep(1)
    #     self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})   
    #     self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 23})
    #     self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
    #                                                                {"status":{"tempDriver": 1, "tempPassenger": 1, "tempSecRow":1, 
    #                                                                "windSpeedFirRow": 6, "windSpeedSecRow": 6, 
    #                                                              "firstRowPowerStatus":True, "secondRowPowerStatus":True}},
    #                                                               ) 
        
    #     self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
    #     self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}})  
    #     self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":4, "value": 25})
    #     self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})  
    #     self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
    #                                                                {"status":{"tempDriver": 0, "tempPassenger": 25, "tempSecRow":0, 
    #                                                                "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
    #                                                              "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
    #                                                               ) 
    #     self.sd_tester.change_usage_mode(2)
    #     sleep(2)
    #     self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus",
    #                                                                {"status":{"tempDriver": 0, "tempPassenger": 25, "tempSecRow":0, 
    #                                                                "windSpeedFirRow": 0, "windSpeedSecRow": 0, 
    #                                                              "firstRowPowerStatus":False, "secondRowPowerStatus":False}},
    #                                                               ) 
 
    @pytest.mark.full       
    @pytest.mark.jishu2
    @allure.title("通知/获取极速制冷制热状态_开启极速制热/制冷后调用SetTemperatureAndOn")
    def test_caseid_1988425(self): 
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr03, 'RemClimaActv', 1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxHeatingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":True}}) 
        sleep(1)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}}) 
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetMaxCoolingCtrl", {"cmd":{"onOffCmd":True}})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :True,"maxHeatingSts":False}}) 
        self.partner.empty_all(0.5)        
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 0})
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT,"MaxCoolingHeatingInfo")
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 1})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "MaxCoolingHeatingInfo",{"info":{"maxCoolingSts" :False,"maxHeatingSts":False}})    
              

    @allure.title("v2.2除霜除雾-AUTO_后排开关记忆值为on-打开后排开关-关闭后排开关-打开除雾除霜-关闭除雾除霜")
    @pytest.mark.jishu3
    @pytest.mark.sanity    
    def test_caseid_1989149(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        
        
    @allure.title("v2.2除霜除雾-AUTO_后排开关记忆值为off-关闭除雾除霜-设置后排温度-关闭总开关-设置风速")  
    @pytest.mark.full      
    @pytest.mark.jishu3
    def test_caseid_1989147(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": 25})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False,
                                                "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 11})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        
    @allure.title("v2.2除霜除雾-AUTO_后排开关记忆值为off-设置auto开-手动关闭后排-手动开启后排-关闭总开关-设置风速")
    @pytest.mark.smoke    
    @pytest.mark.jishu3
    def test_caseid_1989146(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False,
                                                "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 11})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})   
                                
        
    @allure.title("v2.2OFF-AUTO_后排开关记忆值为off-打开auto-设置后排温度-关闭总开关-AC为开")
    @pytest.mark.sanity    
    @pytest.mark.jishu3
    def test_caseid_1989145(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": 23})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False,
                                                "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5) 
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        
    @allure.title("v2.2OFF-AUTO_后排开关记忆值为off-设置副驾驶温度-设置后排温度-关闭总开关-AC为开")
    @pytest.mark.full    
    @pytest.mark.jishu3
    def test_caseid_1989144(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 23})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":2, "value": 23})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                False, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        
    @allure.title("v2.2OFF-AUTO_后排开关记忆值为on-AC为开-关闭后排开关-关闭总开关-开启auto-关闭总开关-设置主驾驶温度")
    @pytest.mark.full    
    @pytest.mark.jishu3
    def test_caseid_1989139(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False,
                                                    "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": False,
                                                    "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 24})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus": True,
                                                    "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        
    @allure.title("v2.2OFF-AUTO_后排开关记忆值为OFF-设置AC为on-关闭总开关-设置风量为12")
    @pytest.mark.full    
    @pytest.mark.jishu3
    def test_caseid_1989138(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                False, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 12})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        
    @allure.title("v2.2OFF-AUTO_后排开关记忆值为on-设置副驾驶温度-关闭总开关-AC为开")
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989137(self):
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":4, "value": 23})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                False, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        
    @allure.title("v2.2OFF-AUTO_恢复出厂设置&关闭总开关&设置主驾驶温度")
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989136(self):
        self.del_s2s_db()
        self.kill_s2s_and_reconnect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(3)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                False, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 24})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})

    @allure.title("v2.2OFF-AUTO_恢复出厂设置&关闭总开关&打开总开关")
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989135(self):
        self.del_s2s_db()
        self.kill_s2s_and_reconnect_service(CLIMATECONTROL_SERVICE_CLIENT)
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                False, "firstRowPowerStatus": False, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":0})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})

    @allure.title("v2.2OFF-AUTO_后排开关记忆值为on&打开auto开关&打开除雾除霜&关闭除雾除霜")
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989134(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        
    @allure.title("v2.2OFF-AUTO_后排开关记忆值为off&打开auto开关&打开除雾除霜&关闭除雾除霜")
    @pytest.mark.full
    @pytest.mark.jishu3
    def test_caseid_1989133(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":2})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": True}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{"acStatus":
                                                True, "firstRowPowerStatus": True, "secondRowPowerStatus": False}})
        
    @allure.title("v2.2除霜除雾Aciton-除雾除霜状态机设置风速7-跳转manual")
    @pytest.mark.full
    def test_caseid_1989178(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 8})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 9, "windSpeedSecRow":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 7})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 7, "windSpeedSecRow":7}})
        
    @allure.title("v2.2除霜除雾Aciton-除雾除霜状态机设置风速13档同时退出进入Manual-auto")
    @pytest.mark.full
    def test_caseid_1989173(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 7})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 9, "windSpeedSecRow":0}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 13})
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindMode", {"zoneId":2, "mode":2})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 7, "windSpeedSecRow":7}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 12, "windSpeedSecRow":12}})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "Off", {"zoneId":0})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 13})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 13, "windSpeedSecRow":13}})
        
        
    @allure.title("v2.2除霜除雾Aciton-除雾除霜状态机设置auto风量13-关闭除雾除霜")
    @pytest.mark.full
    def test_caseid_1989171(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetAC", {"on": False})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT,  "SetClimateAuto", {"zoneId": 0, "on": True})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "On", {"zoneId":2})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 12})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetTemperatureAndOn", {"zoneId":3, "value": 20})
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": True})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 9, "windSpeedSecRow":0}})
        self.partner.empty_all(0.5)
        self.five_door_open()
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetWindSpeed", {"zoneId":1, "speed": 13})
        sleep(1)
        # self.io.set_four_door_close()
        # self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT,"ClimateSystemStatus")
        sleep(0.5)
        self.partner.send_method_request(CLIMATECONTROL_SERVICE_CLIENT, "SetFastDefrostMode", {"on": False})
        self.partner.ck_event_and_resp(CLIMATECONTROL_SERVICE_CLIENT, "ClimateSystemStatus", {"status":{
                                                            "tempDriver": 20, "tempPassenger": 20, "tempSecRow": 20,
                                                                "windSpeedFirRow": 12, "windSpeedSecRow":12}})
        
@allure.feature("SOA服务接口")
@allure.story("整车控制/ClimateControlServcie")
@pytest.mark.mockmcu
class TestClimateControlServcieMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("ClimateControlService", "client")])
        sleep(5)

    def after_class(self, ecu):
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu)            

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    @pytest.mark.full
    @allure.title("通知/获取空调的空气流量_0")
    def test_caseid_1985174(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 50)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 0)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateAirFlow", 
                                            {"airFlow": {"flow":0}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":0}})

    @pytest.mark.smoke
    @allure.title("通知/获取空调的空气流量_100")
    def test_caseid_1985175(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 50)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 100)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateAirFlow", 
                                            {"airFlow": {"flow":100}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":100}})
                                    
    @pytest.mark.sanity
    @allure.title("通知/获取空调的空气流量_1000")
    def test_caseid_1985181(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 50)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 1000)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateAirFlow", 
                                            {"airFlow": {"flow":1000}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":1000}})

    @pytest.mark.full
    @allure.title("通知/获取空调的空气流量_500")
    def test_caseid_1985176(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 50)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 500)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateAirFlow", 
                                            {"airFlow": {"flow":500}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":500}})

    @pytest.mark.full
    @allure.title("通知/获取空调的空气流量_无效信号保持lastvlaue&重启默认值")
    def test_caseid_1985182(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 50)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 1023)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":50}})
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(5)
        self.partner.ck_no_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateAirFlow")
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":0}})
                                            
    @pytest.mark.full
    @allure.title("通知/获取空调的空气流量_有效信号重启event")
    def test_caseid_1985185(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 50)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT)
        sleep(5)
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateAirFlow", 
                                            {"airFlow": {"flow":50}})
                                            
    @pytest.mark.full
    @allure.title("通知/获取空调的空气流量_默认值")
    def test_caseid_1985173(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'HvacAirMFlowEstimd', 50)
        self.restart_bgm_and_connect_service(CLIMATECONTROL_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":0}})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(CLIMATECONTROL_SERVICE_CLIENT, "ClimateAirFlow", 
                                            {"airFlow": {"flow":50}})
        self.partner.send_request_and_ck_resp(CLIMATECONTROL_SERVICE_CLIENT, "GetClimateAirFlow", {}, 
                                              {"out": {"flow":50}})


