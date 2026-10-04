#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Door.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
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
@allure.story("WTI通知/WTIService_Seat")
class TestWTIService_Seat(TestBase):
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
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        sleep(1)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(0.5)

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def airvent_no_fault(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr03BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr03ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr07BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr07ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr08ElecErr',0)
        sleep(1)

    def Voltage_Inter_Lock_nofault(self,A,B,C,D):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvilFlt', A)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr05, 'HVIL1Sts', B)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr05, 'HVIL2Sts', C)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr05, 'HVIL3Sts', D)
        sleep(1)

    def Shift_Gear(self, X):
        """0代表P挡 2代表N挡 3代表D挡 1代表R挡"""
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', X)
        sleep(1)
    
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

    def seat_occupt(self,A,B,C,D):
        """副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        sleep(1)

    def seat_belt_status(self,A,B,C,D,E):
        """主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSt1_0_SRSBackBoneSignalIPdu04', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSt1_0_SRSBackBoneSignalIPdu04', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSt1_0_SRSBackBoneSignalIPdu04', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
        sleep(1)

    def set_vehicle_speed(self,X):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', X)
        sleep(1)

    @allure.title("遍历_后排右座椅通风故障报警") 
    @pytest.mark.full
    def test_caseid_1980181(self):
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',3)
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Right Seat Vent Warning","info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Right Seat Vent Warning","info": "1"}]})
        for value in [0,1,2,4,6,7]:
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',value)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Right Seat Vent Warning","info": "0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Right Seat Vent Warning","info": "0"}]})
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',5)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Right Seat Vent Warning","info": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Right Seat Vent Warning","info": "1"}]})

    @allure.title("遍历_后排左座椅通风故障报警") 
    @pytest.mark.full
    def test_caseid_1980179(self):
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',3)
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Vent Warning","info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Vent Warning","info": "1"}]})
        for value in [0,1,2,4,6,7]:
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',value)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Vent Warning","info": "0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Vent Warning","info": "0"}]})
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',5)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Vent Warning","info": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Vent Warning","info": "1"}]})
        
    @allure.title("遍历_后排左座椅加热故障报警") 
    @pytest.mark.full
    def test_caseid_1980175(self):
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',3)
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Heat Warning","info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Heat Warning","info": "1"}]})
        for value in [0,1,2,4,6,7]:
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',value)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Heat Warning","info": "0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Heat Warning","info": "0"}]})
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecLe',5)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Heat Warning","info": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Heat Warning","info": "1"}]})

    @allure.title("遍历_后排右座椅加热故障报警") 
    @pytest.mark.full
    def test_caseid_1987884	(self):
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',3)
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Right Seat Heat Warning","info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Right Seat Heat Warning","info": "1"}]})
        for value in [0,1,2,4,6,7]:
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',value)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Right Seat Heat Warning","info": "0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Right Seat Heat Warning","info": "0"}]})
            self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',5)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Right Seat Heat Warning","info": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Right Seat Heat Warning","info": "1"}]})
        
    @allure.title("遍历_主驾驶座椅加热故障报警") 
    @pytest.mark.sanity
    def test_caseid_1979970(self):
        info = [(3,"1"),(0,"0"),(5,"1"), (1,"0"), (3,"1"), (2,"0"),(3,"1"), (4,"0"),(5,"1"), (6,"0"),(3,"1"), (7,"0")]
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts', 0)
        self.partner.empty_all(0.5)
        for item in info:
            logger.info(f"-----发送信号值{item[0]}")
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatHeatgAvlSts', item[0])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Driver Seat Heat Warning", "info": item[1]}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Driver Seat Heat Warning", "info": item[1]}]})

    @allure.title("安全带指示灯/报警信息_遍历")
    @pytest.mark.smoke
    def test_caseid_1980141(self):
        def info1(input1):
            return "1" if input1 == 0 else "0"
        def info3(input3):
            return "2" if input3 == 0 else "0"
        def info4(input4):
            return "3" if input4 == 0 else "0"
        info2 =["BltLockStAtPassBltLockSt1","BltLockStAtRowSecLeBltLockSt1","BltLockStAtRowSecMidBltLockSt1","BltLockStAtRowSecRiBltLockSt1"]
        self.sd_tester.change_usage_mode(13)
        self.Shift_Gear(3)
        self.seat_occupt(0,0,0,0)
        self.io.driver_seat_notpresent()
        self.seat_belt_status(1,1,1,1,1)
        self.set_vehicle_speed(0.0)
        self.partner.empty_all(0.5)
        #主驾触发一级报警
        self.seat_occupt(1,1,1,1)
        self.io.driver_seat_present()
        for X in [0,1]:
            logger.info(f"-----发送主驾安全带{X}")
            self.seat_belt_status(X,1,1,1,1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Seat Belt", "state": info1(X)}]})
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Driver Seat Belt Warning", "info": info1(X)}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Seat Belt", "state": info1(X)}]})
        for X in info2: #其余四个座位触发一级报警
            for Y in [0,1]:
                logger.info(f"-----发送座位{X}信号值--{Y}")
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, X, Y)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Seat Belt", "state": info1(Y)}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Seat Belt", "state": info1(Y)}]})
        self.set_vehicle_speed(8.0)
        #主驾触发二级报警
        for X in [0,1]:
            logger.info(f"-----发送主驾安全带{X}")
            self.seat_belt_status(X,1,1,1,1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Seat Belt", "state": info3(X)}]})
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Driver Seat Belt Warning", "info": info3(X)}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Seat Belt", "state": info3(X)}]})
        for Y in [0,1]:
                logger.info(f"-----发送四个座位信号值--{Y}")
                self.seat_belt_status(1,Y,Y,Y,Y)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Seat Belt", "state": info3(Y)}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Passenger Seat Belt Warning", "info": info3(Y)},
                                                              {"name":"Second Row Left Seat Belt Warning", "info": info3(Y)},
                                                              {"name":"Second Row Middle Seat Belt Warning", "info": info3(Y)},
                                                              {"name":"Second Row Right Seat Belt Warning", "info": info3(Y)}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Seat Belt", "state": info3(Y)}]})
        self.set_vehicle_speed(15.0)
        #主驾触发三级报警
        for X in [0,1]:
            logger.info(f"-----发送主驾安全带{X}")
            self.seat_belt_status(X,1,1,1,1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Seat Belt", "state": info4(X)}]})
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Driver Seat Belt Warning", "info": info4(X)}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Seat Belt", "state": info4(X)}]})
        for Y in [0,1]:
                logger.info(f"-----发送四个座位信号值--{Y}")
                self.seat_belt_status(1,Y,Y,Y,Y)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Seat Belt", "state": info4(Y)}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, 
                                                      {"out":[{"name":"Passenger Seat Belt Warning", "info": info4(Y)},
                                                              {"name":"Second Row Left Seat Belt Warning", "info": info3(Y)},
                                                              {"name":"Second Row Middle Seat Belt Warning", "info": info3(Y)},
                                                              {"name":"Second Row Right Seat Belt Warning", "info": info3(Y)}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Seat Belt", "state": info4(Y)}]})
        self.set_vehicle_speed(0.0)

    @allure.title("遍历_副驾驶座椅加热故障报警") 
    @pytest.mark.sanity
    def test_caseid_1979971(self):
        info = [(3,"1"),(0,"0"),(5,"1"), (1,"0"), (3,"1"), (2,"0"),(3,"1"), (4,"0"),(5,"1"), (6,"0"),(3,"1"), (7,"0")]
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts', 0)
        self.partner.empty_all(0.5)
        for item in info:
            logger.info(f"-----发送信号值{item[0]}")
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatHeatgAvlSts', item[0])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Passenger Seat Heat Warning", "info": item[1]}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Passenger Seat Heat Warning", "info": item[1]}]})

    @allure.title("遍历_主驾座椅通风故障报警") 
    @pytest.mark.sanity
    def test_caseid_1979972(self):
        info = [(3,"1"),(0,"0"),(5,"1"), (1,"0"), (3,"1"), (2,"0"),(3,"1"), (4,"0"),(5,"1"), (6,"0"),(3,"1"), (7,"0")]
        self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts', 0)
        self.partner.empty_all(0.5)
        for item in info:
            logger.info(f"-----发送信号值{item[0]}")
            self.ipdu.set(self.ipdu.bodycan.SmdBodyFr04, 'DrvrSeatVentAvlSts', item[0])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Driver Seat Wind Warning", "info": item[1]}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Driver Seat Wind Warning", "info": item[1]}]})

    @allure.title("遍历_副驾座椅通风故障报警") 
    @pytest.mark.sanity
    def test_caseid_1979973(self):
        info = [(3,"1"),(0,"0"),(5,"1"), (1,"0"), (3,"1"), (2,"0"),(3,"1"), (4,"0"),(5,"1"), (6,"0"),(3,"1"), (7,"0")]
        self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts', 0)
        self.partner.empty_all(0.5)
        for item in info:
            logger.info(f"-----发送信号值{item[0]}")
            self.ipdu.set(self.ipdu.bodycan.SmpBodyFr03, 'PassSeatVentAvlSts', item[0])
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Passenger Seat Wind Warning", "info": item[1]}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Passenger Seat Wind Warning", "info": item[1]}]})

    @allure.title("座椅故障报警交叉测试") 
    @pytest.mark.full
    def test_caseid_1980176(self):
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',0)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',3)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',3)
        
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Vent Warning","info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Right Seat Heat Warning","info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Vent Warning","info": "1"},
                                                           {"name": "Rear Right Seat Heat Warning","info": "1"}]})
        
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecLe',0)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list": [{"name": "Rear Left Seat Vent Warning","info": "0"},
                                                                                ]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Vent Warning","info": "0"},
                                                           {"name": "Rear Right Seat Heat Warning","info": "1"}]})
        
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr00, 'SeatHeatgAvlStsRowSecRi',0)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                   {"out":[{"name": "Rear Left Seat Vent Warning","info": "0"},
                                                           {"name": "Rear Right Seat Heat Warning","info": "0"}]})