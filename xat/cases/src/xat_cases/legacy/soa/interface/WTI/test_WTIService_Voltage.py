#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIService_Voltage.py
@Time         :2023/04/08 17:20:31
@Author       :tao.cheng_ext@jiduauto.com
@Description : Test SOA for WTIService_Voltage
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
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *


@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIServiceVoltage")
class TestWTIServiceVoltage(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("ClimateControlService", "client"),
                                     ("HighVoltageService", "client"),])
        self.partner.method_default_timeout = 2
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
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu, start=False)

    def BGM_down_up(self,X,Y,Z):
        """X代表总线停后等待时间 Y代表下电后电等待时间 Z代表上电后电等待时间"""
        self.ipdu.pause_all_bus_send()
        sleep(X)
        self.nucapp.bgm_power_off()
        sleep(Y)
        self.nucapp.bgm_power_on()
        sleep(Z)

    def airvent_no_fault(self):
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01BlckSts_1_CcmBodySignalIPdu62',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr01ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr62, 'VentnActr02ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr03BlckSts_1_CcmBodySignalIPdu63',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr03ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr63, 'VentnActr04ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05BlckSts_1_CcmBodySignalIPdu64',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr05ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06BlckSts',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr64, 'VentnActr06ElecErr',0)
        self.ipdu.set(self.ipdu.bodycan.CcmBodyFr65, 'VentnActr07BlckSts_1_CcmBodySignalIPdu65',0)
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
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', X)
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
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts_0_SRSBackBoneSignalIPdu04', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe_0_SRSBackBoneSignalIPdu04', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid_0_SRSBackBoneSignalIPdu04', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi_0_SRSBackBoneSignalIPdu04', D)
        sleep(1)

    def seat_belt_status(self,A,B,C,D,E):
        """主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts_0_SRSBackBoneSignalIPdu04', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1_0_SRSBackBoneSignalIPdu04', B)
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
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06', X)
        sleep(1)

    @allure.title("动力系统故障信息_遍历chargingState中的Value_参数不为'5") 
    @pytest.mark.full
    def test_caseid_1989287(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(random.choice([2, 11,13]))
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', random.choice([8,11]))
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb',18)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)

    @allure.title("动力系统故障信息_遍历UsageModeChanged中的Value从2或11或13跳1时_参数不为'5") 
    @pytest.mark.full
    def test_caseid_1989291(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(random.choice([2, 11,13]))
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', random.choice([8,11]))
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(1)
        self.partner.ck_wti_warning_and_resp(hint, 0, timeout=0.5)

    @allure.title("动力系统故障信息_遍历UsageModeChanged中的Value从2跳11或13时_延时上报参数为'9") 
    @pytest.mark.full
    def test_caseid_1989292(self):
        hint="Power System Failure"
        for usagemode in [11,13]:
            self.sd_tester.change_usage_mode(2)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
            logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', random.choice([8,11]))
            self.partner.empty_all(1.5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                                "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "5"}]})
            self.sd_tester.change_usage_mode(usagemode)
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)
            self.partner.ck_wti_no_warning_and_ck_resp(hint,"5",timeout=0.7)
            self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.7)

    @allure.title("动力系统故障信息_ powertrainFaultMsgValidity的Validity=4时其他条件满足") 
    @pytest.mark.full
    def test_caseid_1989302(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.ipdu.pause_bus_send("chassiscan2")
        self.partner.empty_all(2.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_wti_warning_and_resp(hint, 9, timeout=0.5)
        self.partner.empty_all()
        self.ipdu.resume_bus_send("chassiscan2")
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":hint, "info": "9"}]}, timeout=2)
        self.partner.empty_all()
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":hint, "info": "9"}]}, timeout=2)
        self.partner.empty_all()    
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)    
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)    
        self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.5)
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.empty_all(1)   
        self.ipdu.pause_bus_send("chassiscan2")
        self.partner.empty_all(2.5)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"9",timeout=0.7)    
        self.partner.ck_wti_coming_warning_and_resp(hint, 4, timeout=0.7)
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"4",timeout=0.7)

    @allure.title("动力系统故障信息_ value满足情况下从0 跳11时的1S内变化value，1S后不上报9") 
    @pytest.mark.sanity
    def test_caseid_1989301(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.partner.empty_all()
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=1)    
        self.partner.empty_all()    
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=1)    
        self.partner.empty_all() 
        self.sd_tester.change_usage_mode(13) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.5)    
        self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.7)

    @allure.title("动力系统故障信息_ value为9但不满足使用者模式") 
    @pytest.mark.sanity
    def test_caseid_1989300(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.sd_tester.change_usage_mode(1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=1)
        self.sd_tester.change_usage_mode(0)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=1)
        for usagemode1 in [0,1]:
            for usagemode2 in [11,13]:
                self.sd_tester.change_usage_mode(usagemode1)
                self.partner.empty_all(1.5)
                self.sd_tester.change_usage_mode(usagemode2)
                logger.info(f"从使用者模式{usagemode1}切换到使用者模式{usagemode2}")
                self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.5)
                self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.7)

    @allure.title("动力系统故障信息_ value非9 （信号0-15，非1）不满足参数为9") 
    @pytest.mark.full
    def test_caseid_1989299(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(random.choice([2, 11,13]))
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)
        self.partner.empty_all(1.5)
        for fault in range(2,16):
            logger.info(f"故障状态{fault}")
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', fault)
            self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":hint, "info": "9"}]}, timeout=0.5)
        self.partner.empty_all(1.5)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)
        self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.5)

    @allure.title("动力系统故障信息_ UsageModeChanged保持2或11和13，但是Validity不是有效，其他条件满足，上报5") 
    @pytest.mark.full
    def test_caseid_1989298(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.ipdu.pause_bus_send("backbonefr")
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 8)
        self.partner.ck_wti_coming_warning_and_resp(hint, 5, timeout=0.5)

    @allure.title("动力系统故障信息_ 重启前满足重启后也上报5") 
    @pytest.mark.full
    def test_caseid_1989297(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 8)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "5"}]})
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "5"}]},timeout=5)

    @allure.title("动力系统故障信息_ chargingState重启丢失保持默认值即！=18，其他条件满足，上报5") 
    @pytest.mark.full
    def test_caseid_1989296(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 8)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        sleep(2)
        self.ipdu.resume_bus_send("chassiscan2")
        self.ipdu.resume_bus_send("backbonefr")
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.7)
        self.partner.ck_wti_coming_warning_and_resp(hint, 5, timeout=0.7)


    @allure.title("动力系统故障信息_ powertrainFaultMsgValidity的value保持5，但是Validity为4，其他条件满足，上报5") 
    @pytest.mark.full
    def test_caseid_1989295(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 18)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 8)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.ipdu.pause_bus_send("chassiscan2")
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 0)
        self.partner.ck_wti_coming_warning_and_resp(hint, 5, timeout=0.7)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(11)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,5,timeout=0.7)
        self.partner.ck_wti_coming_warning_and_resp(hint, 4, timeout=0.7)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(2)
        self.partner.ck_wti_warning_and_resp(hint, 5, timeout=0.5)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(13)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,5,timeout=0.7)
        self.partner.ck_wti_coming_warning_and_resp(hint, 4, timeout=0.7)

    @allure.title("动力系统故障信息_遍历UsageModeChanged中的Value从0跳11时改变变量_延时上报参数不为'5") 
    @pytest.mark.full
    def test_caseid_1989293(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', random.choice([8,11]))
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.7)
        self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.7)
        self.sd_tester.change_usage_mode(0)
        self.partner.empty_all(1.5)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb',18)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.7)
        self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.7)

    @allure.title("动力系统故障信息_使用者模式从0跳11的1S内满足条件_延时上报参数为'9") 
    @pytest.mark.smoke
    def test_caseid_1989294(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 18)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)
        self.partner.empty_all(1.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                            "GetWarningMsgList", {}, {"out":[{"name":hint, "info": "0"}]})
        self.sd_tester.change_usage_mode(11)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 8)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.5)
        self.partner.ck_wti_coming_warning_and_resp(hint, 5, timeout=0.7)
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all(1.5)
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', 18)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"5",timeout=0.5)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.7)


    @allure.title("动力系统故障信息_遍历UsageModeChanged中的Value_参数为'5") 
    @pytest.mark.full
    def test_caseid_1989290(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', random.choice([8,11]))
        self.partner.empty_all(1)
        for usagemode1 in [0,1]:
            for usagemode2 in [11,13]:
                self.sd_tester.change_usage_mode(usagemode1)
                self.partner.empty_all(1.5)
                logger.info(f"使用者模式从{usagemode1}切换到{usagemode2}")
                self.sd_tester.change_usage_mode(usagemode2)
                self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.7)
                self.partner.ck_wti_coming_warning_and_resp(hint, 5, timeout=0.7)
        self.partner.empty_all(1)
        for usagemode3 in [0,1]:
            self.sd_tester.change_usage_mode(usagemode3)
            self.partner.empty_all(1.5)
            logger.info(f"使用者模式从{usagemode3}切换到convenience")
            self.sd_tester.change_usage_mode(2)
            self.partner.ck_wti_warning_and_resp(hint, 5, timeout=0.5)
        for usagemode4 in [11,13]:
            self.sd_tester.change_usage_mode(2)
            self.partner.empty_all(1.5)
            logger.info(f"使用者模式从convenience切换到{usagemode3}")
            self.sd_tester.change_usage_mode(usagemode4)
            self.partner.ck_wti_no_warning_and_ck_resp(hint,"5",timeout=1.5)

    @allure.title("动力系统故障信息_遍历UsageModeChanged中的Value_参数不为'5") 
    @pytest.mark.full
    def test_caseid_1989289(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(random.choice([2, 11,13]))
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', random.choice([8,11]))
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(0)
        self.partner.ck_wti_warning_and_resp(hint, 0, timeout=0.5)
        self.partner.empty_all(1)
        self.sd_tester.change_usage_mode(1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"0",timeout=0.5)

    @allure.title("动力系统故障信息_遍历chargingState中的Value_参数为'5") 
    @pytest.mark.smoke
    def test_caseid_1989288(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(random.choice([2, 11,13]))
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb',0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', random.choice([8,11]))
        self.partner.empty_all(1)
        for chargingsts in list(range(13))+[14,15]+list(range(19,31)):
            logger.info(f"充电状态为{chargingsts}")
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb',chargingsts)
            self.partner.ck_wti_no_warning_and_ck_resp(hint,"5")
            self.partner.empty_all(0.5)

    @allure.title("动力系统故障信息_遍历powertrainFaultMsgValidity中的Value_参数为'5") 
    @pytest.mark.sanity
    def test_caseid_1989286(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(random.choice([2, 11,13]))
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 8)
        self.partner.ck_wti_coming_warning_and_resp(hint, 5, timeout=0.5)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 11)
        self.partner.ck_wti_no_warning_and_ck_resp(hint,"5")

    @allure.title("动力系统故障信息_遍历powertrainFaultMsgValidity中的Value_参数不为'5") 
    @pytest.mark.full
    def test_caseid_1989285(self):
        hint="Power System Failure"
        self.sd_tester.change_usage_mode(random.choice([2, 11,13]))
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', random.choice(list(range(13))+[14,15]+list(range(19,31))))
        logger.info(f"充电状态{random.choice(list(range(13))+[14,15]+list(range(18,31)))}")
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)
        self.partner.empty_all(1)
        for fault in list(range(8))+[9,10]+list(range(12,16)):
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', fault)
            logger.info(f"故障信号发送值为{fault}")
            if fault ==1:
                self.partner.ck_wti_coming_warning_and_resp(hint, 9, timeout=0.5)
            elif fault ==2:
                self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=0.5)
            elif fault ==3:
                self.partner.ck_wti_coming_warning_and_resp(hint, 2, timeout=0.5)
            elif fault ==4:
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
            elif fault ==5:
                self.partner.ck_wti_coming_warning_and_resp(hint, 3, timeout=0.5)
            elif fault ==6:
                self.partner.ck_wti_coming_warning_and_resp(hint, 4, timeout=0.5)
            elif fault ==7:
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
            elif fault ==10:
                self.partner.ck_wti_coming_warning_and_resp(hint, 8, timeout=0.5)
            elif fault ==12:
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint,"0")


    @allure.title("快充充电桩使用提示_ 仅直流CCP_通过插入直流枪触发") 
    @pytest.mark.smoke
    def test_caseid_1989311(self):
        hint="DCChargePileUsagePrompt"
        self.sd_tester.write_single_ccp(973,0) #仅支持直流
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
        sleep(3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "0"}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=0.5)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)

    @allure.title("快充充电桩使用提示_ 交直流CCP_通过插入直流枪触发") 
    @pytest.mark.sanity
    def test_caseid_1989312(self):
        hint="DCChargePileUsagePrompt"
        self.sd_tester.write_single_ccp(973,2) #支持交直流
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
        sleep(3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "0"}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=0.5)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)

    @allure.title("快充充电桩使用提示_ 仅直流CCP_通过升压原因触发") 
    @pytest.mark.sanity
    def test_caseid_1989314(self):
        hint="DCChargePileUsagePrompt"
        self.sd_tester.write_single_ccp(973,2) #支持交直流
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 0)
        sleep(3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "0"}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        sleep(0.1)
        for BOOST in [0,1,2]:
            logger.info(f"发送升压从3到{BOOST}")
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
            self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=0.5)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', BOOST)
            self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
        self.partner.empty_all(0.5)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
        self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=0.5)
        self.partner.empty_all(0.5) 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)

    @allure.title("快充充电桩使用提示_ 交直流CCP_重启前后都保持") 
    @pytest.mark.full
    def test_caseid_1989315(self):
        hint="DCChargePileUsagePrompt"
        self.sd_tester.write_single_ccp(973,2) #支持交直流
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
        sleep(3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "1"}]})
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "1"}]},timeout=5)

    @allure.title("快充充电桩使用提示_ 交直流CCP_休眠后拔枪") 
    @pytest.mark.full
    def test_caseid_1989316(self):
        hint="DCChargePileUsagePrompt"
        self.sd_tester.write_single_ccp(973,2) #支持交直流
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
        sleep(3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "1"}]})
        self.nucapp.bgm_power_off()
        sleep(2)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(WTI_SERVICE_CLIENT)
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "0"}]},timeout=5)

    @allure.title("快充充电桩使用提示_ 交直流CCP_通过升压原因触发") 
    @pytest.mark.sanity
    def test_caseid_1989313(self):
        hint="DCChargePileUsagePrompt"
        self.sd_tester.write_single_ccp(973,2) #支持交直流
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 0)
        sleep(3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, 
                                              "GetWarningMsgList", {}, {"out":[{"name":"DCChargePileUsagePrompt", "info": "0"}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1)
        sleep(0.1)
        for BOOST in [0,1,2]:
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
            self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=0.5)
            self.partner.empty_all()
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', BOOST)
            self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)
        self.partner.empty_all(0.5)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3)
        self.partner.ck_wti_coming_warning_and_resp(hint, 1, timeout=0.5)
        self.partner.empty_all(0.5) 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=0.5)

    def set_DCChargePileUsagePrompt(self, ccp973 = 2):
        '''设置高压直流快充充电桩使用提示的前置条件'''
        self.sd_tester.write_single_ccp(973, ccp973) 
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 0)
        sleep(3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(2)        
    
    @allure.title("高压直流快充充电桩使用提示_isInhibitByHVBoost条件判断") 
    @pytest.mark.sanity
    def test_caseid_1989618(self): # isconnect=False,acdcType=1,改变isInhibitByHVBoost
        hint="DCChargePileUsagePrompt"
        self.set_DCChargePileUsagePrompt()
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"acdcType": 0, "isConnect": False}}, timeout=3)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3) # pluggerStatus=3 枪插着才能上报acdcTyoe
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"acdcType": 1, "isConnect": True}}, timeout=5)
        self.partner.empty_all()
        for i in [1, 3, 0, 2]:
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', i)
            value = 1 if i == 3 else 0
            if i in [3, 0]:
                self.partner.ck_wti_warning_and_resp(hint, value, timeout=2)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value, timeout=2)   

    @allure.title("高压直流快充充电桩使用提示_acdcType条件判断") 
    @pytest.mark.sanity
    def test_caseid_1989619(self): # ChargingInfo,acdcType|DCChargePileUsagePrompt|isInhibitByHVBoost|ChargingInfo,isconnect
        hint="DCChargePileUsagePrompt"
        self.set_DCChargePileUsagePrompt()
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'HVChrgnStopReq', 3) # isInhibitByHVBoost=True
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"acdcType": 0, "isConnect": False}}, timeout=3)
        for i in [1, 0]: # acdcType=1,0
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', i)
            self.partner.ck_wti_warning_and_resp(hint, i, timeout=2) # OnBdChrgrHndlSts1=0，DCChrgnHndlSts=1时，acdcType=DC 
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) # acdcType=2  
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)   
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # acdcType=3
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)     
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0) # acdcType=1
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=2)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1) # acdcType=3
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=2)     
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) # acdcType=2
        self.partner.ck_wti_warning_and_resp(hint, 0, timeout=2)     

    @allure.title("遍历_备用低压电池系统异常") 
    @pytest.mark.sanity
    def test_caseid_1980110(self):
        def info(input):
            return "1" if input == 1 else "0"
        self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLVPwrSplyErrSts', 1)
        self.partner.empty_all(0.5)
        for item in range(8):
            logger.info(f"-----发送信号值{item}")
            self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, 'IPMLVPwrSplyErrSts', item)
            if item in [0,1,2]:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"IPM Battery Fault Waring", "info": info(item)}]})
            else:
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT, "WarningMsgList", "IPM Battery Fault Waring")
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"IPM Battery Fault Waring", "info": info(item)}]})

    @allure.title("遍历_低电量报警灯和低电量报警信息") 
    @pytest.mark.sanity
    def test_caseid_1979959(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.partner.empty_all(1)
        #低电量2级报警
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 10.5)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Battery Low Warning", "info": "2"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"High Voltage Battery Low Telltale", "state": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Battery Low Warning", "info": "2"}]})
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"High Voltage Battery Low Telltale", "state": "2"}]})
        ##低电量1级报警
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.6)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Battery Low Warning", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"High Voltage Battery Low Telltale", "state": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Battery Low Warning", "info": "1"}]})
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"High Voltage Battery Low Telltale", "state": "1"}]})
        ##低电量无报警
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Battery Low Warning", "info": "0"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"High Voltage Battery Low Telltale", "state": "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Battery Low Warning", "info": "0"}]})
        sleep(1)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"High Voltage Battery Low Telltale", "state": "0"}]})
        
    @allure.title("遍历_功率受限故障灯") 
    @pytest.mark.sanity
    def test_caseid_1983336(self):
        for usagemode in [1,0]:
            logger.info(f"---切换使用者模式{usagemode}")
            self.sd_tester.change_usage_mode(usagemode)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',1)
            sleep(1)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Power Limited", "state": "0"}]})
        for usagemode in [2,11,13]:
            logger.info(f"---切换使用者模式{usagemode}")
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',0)
            sleep(1)
            self.sd_tester.change_usage_mode(usagemode)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',1)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Power Limited", "state": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Power Limited", "state": "1"}]})
            self.sd_tester.change_usage_mode(1)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Power Limited", "state": "0"}]})
        for usagemode in [2,11,13]:
            logger.info(f"---切换使用者模式{usagemode}")
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',0)
            sleep(1)
            self.sd_tester.change_usage_mode(usagemode)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',1)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Power Limited", "state": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Power Limited", "state": "1"}]})
            self.sd_tester.change_usage_mode(0)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Power Limited", "state": "0"}]})
        for usagemode in [2,11,13]:
            logger.info(f"---切换使用者模式{usagemode}")
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',0)
            sleep(1)
            self.sd_tester.change_usage_mode(usagemode)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',1)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Power Limited", "state": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Power Limited", "state": "1"}]})
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr27, 'TelltlPwrLoss',0)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Power Limited", "state": "0"}]})

    @allure.title("遍历_高压电池热管理状态提示") 
    @pytest.mark.sanity
    def test_caseid_1983435(self):
        def info(input):
            if input == 0:
                return "0"
            if input == 1:
                return "1"
            if input == 2:
                return "2"
            if input == 3:
                return "3"
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr24, 'LocalHvBattThermReqFb', 1)
        sleep(1)
        for X in range(4):
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr24, 'LocalHvBattThermReqFb', X)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                    {"list":[{"name":"HV Battery Thermal Status", "info": info(X)}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out":[{"name":"HV Battery Thermal Status", "info":info(X)}]})

    @allure.title("遍历_电池低温指示灯") 
    @pytest.mark.sanity
    def test_caseid_1979960(self):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',100.0)
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',-10.0)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Battery Temp Low", "state": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Battery Temp Low", "state": "1"}]})
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',-5.0)
            self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Battery Temp Low", "state": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Battery Temp Low", "state": "1"}]})
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',0.0)
            sleep(1)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Battery Temp Low", "state": "0"}]})
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',-5.0)
            sleep(1)
            self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Battery Temp Low", "state": "0"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Battery Temp Low", "state": "0"}]})
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin', -10.0)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Battery Temp Low", "state": "1"}]})
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',-6.0)
            self.partner.empty_all(1)
            self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Battery Temp Low", "state": "0"}]},timeout=5)
            
    @allure.title("遍历_热失控报警信息") 
    @pytest.mark.sanity
    def test_caseid_1979962(self):
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattLimnIndcn', 0)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattLimnIndcn', 128)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "1"}]})
        A = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList", {})["out"][0]['sequenceTime']['timestamp']
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Thermal Out of Control", "info": "1"}]})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattLimnIndcn', 127)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "0"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "0"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"Thermal Out of Control", "info": "0"}]})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattLimnIndcn', 129)
        sleep(0.1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "1"}]})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattLimnIndcn', 127)
        sleep(0.1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "0"}]})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattLimnIndcn', 128)
        sleep(0.1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "1"}]})
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"Thermal Out of Control", "info": "1"}]})
        B = self.partner.send_request_and_return_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList", {})["out"][0]['sequenceTime']['timestamp']
        assert B > A
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr23, 'HvBattLimnIndcn', 127)
        C = self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {})["list"][0]["sequenceTime"]["timestamp"]
        D = self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {})["list"][0]["sequenceTime"]["timestamp"]
        E = self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {})["list"][0]["sequenceTime"]["timestamp"]
        assert 330000 > D -C > 270000
        assert 330000 > E -D > 270000

    @allure.title("遍历_高压互锁状态信息") 
    @pytest.mark.sanity
    def test_caseid_1979964(self):
        info = {1:"1",0:"0"}
        self.Voltage_Inter_Lock_nofault(0,1,1,1)
        for key,value in info.items():
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvilFlt', key)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Inter Lock", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Inter Lock", "info": value}]})
        #信号1/2/3遍历
        info2 = {0:"1",1:"0"}
        for X in ["HVIL1Sts","HVIL2Sts","HVIL2Sts"]:
            for key,value in info2.items():
                logger.info(f"---发送信号{X}--发送信号值{key}")
                self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr05, X, key)
                sleep(1)
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Inter Lock", "info": value}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Inter Lock", "info": value}]})
        #同时造故障
        self.Voltage_Inter_Lock_nofault(1,0,0,0)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Inter Lock", "info": "1"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Inter Lock", "info": "1"}]})
        #同时恢复故障
        self.Voltage_Inter_Lock_nofault(0,1,1,1)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Inter Lock", "info": "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Inter Lock", "info": "0"}]})

    @allure.title("遍历_高压绝缘信息") 
    @pytest.mark.sanity
    def test_caseid_1979965(self):
        info = {1:"1",0:"0"}
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvIsoFlt', 0)
        sleep(1)
        for key,value in info.items():
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr08, 'HvIsoFlt', key)
            sleep(1)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",{"list":[{"name":"High Voltage Isolation", "info": value}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, {"out":[{"name":"High Voltage Isolation", "info": value}]})

    @allure.title("遍历_电池低温指示灯_默认值") 
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_1980144(self):
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',-5.0)
        sleep(1)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.nucapp.bgm_power_off()
        sleep(3)
        self.nucapp.bgm_power_on()
        sleep(10)
        self.ipdu.resume_bus_send("backbonefr")
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr19, 'HvBattCellTInfoHvBattTMin',-5.0)
        self.sd_tester.change_usage_mode(13)
        try: 
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, {"out":[{"name":"Battery Temp Low", "state": "0"}]})
        except Exception as error:
            self.ipdu.resume_bus_send("backbonefr")
            assert False
        else:
            self.ipdu.resume_bus_send("backbonefr")

    @allure.title("WTI重启event")
    @pytest.mark.full
    def test_caseid_1984247(self):
        # self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr19, 'HybErrIndcnReqTelltlBattTracCutOff', 0)
        # self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr19, 'HybErrIndcnReqTelltlBattTracFailr', 0)
        # self.partner.empty_all(1)
        # self.BGM_down_up(2,3,10)
        # self.ipdu.resume_all_bus_send()
        # # self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", {"list":[{"name":"High Voltage Battery Failed", "state":"0"}]})
        # self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr19, 'HybErrIndcnReqTelltlBattTracCutOff', 1)
        # self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr19, 'HybErrIndcnReqTelltlBattTracFailr', 1)
        # self.partner.ck_s2s_event(WTI_SERVICE_CLIENT, "TelltaleList", {"list":[{"name":"High Voltage Battery Failed", "state":"1"}]})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15,'DCChrgnHndlSts', 0)
        self.partner.empty_all(0.5)
        self.BGM_down_up(2,3,10)
        self.ipdu.resume_all_bus_send()
        # self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Charging Gun Connected", "state": "0"}]})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15,'DCChrgnHndlSts', 1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",{"list":[{"name":"Charging Gun Connected", "state": "1"}]})

    '''放电提醒'''
    @allure.title("放电提醒_DchaStopByTarDrvrIndcn=1_HVSOCInfo.info.displaySoc遍历") 
    @pytest.mark.full
    def test_caseid_1987923(self): # HVSOCInfo.info.displaySoc 映射后只有整数
        hint = "Discharge Reminder" 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'DchaStopByTarDrvrIndcn', 1)  
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.9) 
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '2'}]}, timeout=3)
        self.partner.empty_all()
        last_value=2
        for displaySOC in [0.9, 20.4, 21.0, 99.9]: 
            self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', displaySOC) 
            value = 1 if displaySOC  < 21.0 else 2
            if last_value== value:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)
            else:
                self.partner.ck_wti_warning_and_resp(hint, value)       
            last_value=value
        
    @allure.title("放电提醒_HVSOCInfo.info.displaySoc满足条件后_DchaStopByTarDrvrIndcn遍历") 
    @pytest.mark.sanity
    def test_caseid_1987924(self): # HVSOCInfo,displaySoc|DchaStopByTarDrvrIndcn|Discharge Reminder
        hint = "Discharge Reminder"  
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'DchaStopByTarDrvrIndcn', 1) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0) # HVSOCInfo.info.displaySoc ≤ 20.4
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {"out":{"displaySoc":0}}, timeout=2)        
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '1'}]}, timeout=2)
        self.partner.empty_all()
        dict1={0:[0, 1], 1:[0, 2]}
        for i in range(2):
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'DchaStopByTarDrvrIndcn', i) 
            self.partner.ck_wti_warning_and_resp(hint, dict1[0][i])   
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 80.0) # HVSOCInfo.info.displaySoc ＞20.4
        self.partner.ck_wti_warning_and_resp(hint, 2)
        for i in range(2):
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'DchaStopByTarDrvrIndcn', i) 
            self.partner.ck_wti_warning_and_resp(hint, dict1[1][i]) 
        
    @allure.title("放电提醒_重启场景_未收到HVSOCInfo.info.displaySoc的总线信号") 
    @pytest.mark.full
    def test_caseid_1987925(self): # 停发propulsioncan
        hint = "Discharge Reminder"    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 30.0) 
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'DchaStopByTarDrvrIndcn', 1) 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 30}}, timeout=2)
        self.ipdu.pause_bus_send("propulsioncan")     
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': -1}}, timeout=2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=3)
        self.ipdu.resume_bus_send("propulsioncan")  
        self.partner.ck_wti_warning_and_resp(hint, 2, timeout=2.5)

    @allure.title("放电提醒_重启场景_未收到DchaStopByTarDrvrIndcn的总线信号") 
    @pytest.mark.full
    def test_caseid_1987947(self): # 停发propulsioncan
        hint = "Discharge Reminder"    
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 0.0) # 当收到信号DispHvBattLvlOfChrg值为0时，需要做1.5s的Delay
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr09, 'DchaStopByTarDrvrIndcn', 1) 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 0}}, timeout=3)
        self.ipdu.pause_bus_send("chassiscan2")     
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 0}}, timeout=2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=3)
        self.ipdu.resume_bus_send("chassiscan2")  
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=2.5)
        
    '''充电提醒'''
    def deafault_charge_reminder(self):
        '''充电提醒 前置info=0'''
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)   
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) # pluggerStatus=0, isConnect=0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": False, "pluggerStatus": 0}}, timeout=3) 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 90.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 80.0) # HVSOCInfo.info.displaySoc ＞ chargeTargetSoc
        sleep(0.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":"Charge Reminder" , "info": '0'}]}, timeout=4) # 计时器4s结束
        self.partner.empty_all()
        
    @allure.title("充电提醒_info=1/2_先触发pluggerStatus从0跳1/2/3_再满足前置条件") 
    @pytest.mark.full
    def test_caseid_1987934(self): # info=1的场景也包含了：仅满足chargeTargetSoc<100_不满足displaySoc小于chargeTargetSoc_pluggerStatus从0跳1/2/3后不触发info=1
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', random.choice([1, 2, 3])) # pluggerStatus 从0跳1/2/3
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 0.0) # displaySoc=80.0, chargeTargetSoc=0.0
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # HVSOCInfo.info.displaySoc 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0)
        
    @allure.title("充电提醒_info=1_chargeTargetSoc<100_displaySoc=chargeTargetSoc_pluggerStatus从0跳1/2/3后不触发info=1") 
    @pytest.mark.full
    def test_caseid_1987935(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 90.0) # displaySoc= 90.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 90}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', random.choice([1, 2, 3])) # pluggerStatus 从0跳1/2/3
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)
        
    @allure.title("充电提醒_info=1_触发info=1后_再次满足pluggerStatus从0跳1/2/3") # 此场景偏差接收：info=1后，再次触发后会上报info=1，重新计时4s
    @pytest.mark.sanity
    def test_caseid_1987936(self): # HVSOCInfo,displaySoc|Charge Reminder|ChargingInfo,isConnected|ChargingInfo,chargeTargetSoc
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0        
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 0.0) # chargeTargetSoc=0.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 0.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 2) # pluggerStatus 从0跳2
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 2}})
        self.partner.ck_wti_warning_and_resp(hint, 1)
        for i in range(2):            
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', i) # pluggerStatus 从2跳0再跳1
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": i}})
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=2) # 触发info=1后，pluggerStatus变化不会退出或再次触发
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=2.5) # 触发info=1后，4s计时器结束触发info=0
        
    @allure.title("充电提醒_info=1_触发info=1后_再不满足前置条件") 
    @pytest.mark.sanity
    def test_caseid_1987937(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0        
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 0.0) # chargeTargetSoc=0.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 0.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', random.choice([1, 2, 3])) # pluggerStatus 从0跳1/2/3
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=2)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 91.0) # ChargingInfo.info.chargeTargetSoc
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 91.0}})
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=2)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=2.5)        
        
    @allure.title("充电提醒_info=1_触发info=1后_通过超时恢复") 
    @pytest.mark.sanity
    def test_caseid_1987938(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 50.0) # chargeTargetSoc=0.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 50.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', random.choice([1, 2, 3])) # pluggerStatus 从0跳1/2/3
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=2)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5)
        
    @allure.title("充电提醒_info=1_触发info=1后_通过满足info=2退出计时") 
    @pytest.mark.sanity
    def test_caseid_1987939(self): # 包含了info=2的场景：仅满足displaySoc=100_不满足chargeTargetSoc=100_isConnect从0跳1后不触发info=2
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0   
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # displaySoc= 100.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # pluggerStatus 从0跳1/2/3
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 1}})  
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        for i in range(2):            
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', i) # pluggerStatus 从1跳0再跳1
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": i}})
        self.partner.ck_wti_warning_and_resp(hint, 2)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2, timeout=3)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5) # 关注第一个计时器停止时间 

    @allure.title("充电提醒_info=2_仅满足chargeTargetSoc=100_不满足displaySoc=100_pluggerStatus从0跳1/2/3后不触发info=2") 
    @pytest.mark.sanity
    def test_caseid_1987940(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # chargeTargetSoc=100
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', random.choice([1, 2, 3])) # pluggerStatus 从0跳1/2/3
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)

    @allure.title("充电提醒_info=2_触发info=2后_再次满足pluggerStatus从0跳1/2/3") # 此场景偏差接收：info=2后，再次触发后会上报info=2，重新计时4s
    @pytest.mark.sanity
    def test_caseid_1987941(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # HVSOCInfo.info.displaySoc         
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 2) # pluggerStatus 从0跳2
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 2}})
        self.partner.ck_wti_warning_and_resp(hint, 2)
        for i in range(2):            
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', i) # pluggerStatus 从2跳0再跳1
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": i}})
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2, timeout=2) # 触发info=2后，pluggerStatus变化不会退出或再次触发
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=2.5) # 触发info=2后，4s计时器结束触发info=0
        
    @allure.title("充电提醒_info=2_触发info=2后_再不满足前置条件") 
    @pytest.mark.sanity
    def test_caseid_1987942(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # HVSOCInfo.info.displaySoc         
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # pluggerStatus 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 1}})
        self.partner.ck_wti_warning_and_resp(hint, 2)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 80.0) 
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 80}})
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 80.0) 
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2, timeout=2)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=2.5)
    
    @allure.title("充电提醒_info=2_触发info=2后_通过超时恢复") 
    @pytest.mark.sanity
    def test_caseid_1987943(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # HVSOCInfo.info.displaySoc         
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # pluggerStatus 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 1}})
        self.partner.ck_wti_warning_and_resp(hint, 2)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 2, timeout=3)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5)
                        
    @allure.title("充电提醒_info=2_触发info=2后_通过满足info=1退出计时") 
    @pytest.mark.sanity
    def test_caseid_1987944(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0    
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # HVSOCInfo.info.displaySoc         
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # pluggerStatus 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 1}})
        self.partner.ck_wti_warning_and_resp(hint, 2)    
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 0.0) # ChargingInfo.info.chargeTargetSoc
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 0.0}})
        for i in range(2):            
            self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', i) # pluggerStatus 从1跳0再跳1
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": i}})
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1, timeout=3)
        self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=1.5) # 关注第一个计时器停止时间              

    @allure.title("充电提醒_info=1_pluggerStatus触发条件检查") 
    @pytest.mark.smoke
    def test_caseid_1989620(self): # ChargingInfo,pluggerStatus,from|updateMsg name:Charge Reminder|jetlogd start|HVSOCInfo,displaySoc|ChargingInfo,isConnected|ChargingInfo,chargeTargetSoc
        hint = "Charge Reminder" 
        self.set_DCChargePileUsagePrompt() # 支持交直流
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0        
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 0.0) # chargeTargetSoc=0.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 0.0}})
        self.partner.empty_all()
        for i in range(11):
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 0}}, timeout=2)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', i)   
            if i in [1, 2, 3, 10]:
                self.partner.ck_wti_warning_and_resp(hint, 1, timeout=2)
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=4.5) # 计时器=4s
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)
        
    @allure.title("充电提醒_info=2_pluggerStatus触发条件检查") 
    @pytest.mark.smoke
    def test_caseid_1989621(self): 
        hint = "Charge Reminder" 
        self.set_DCChargePileUsagePrompt() # 支持交直流
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0        
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # HVSOCInfo.info.displaySoc         
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        self.partner.empty_all()
        for i in range(11):
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)  
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 0}}, timeout=2)
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', i)   
            if i in [1, 2, 3, 10]:
                self.partner.ck_wti_warning_and_resp(hint, 2, timeout=2)
                self.partner.ck_wti_coming_warning_and_resp(hint, 0, timeout=4.5) # 计时器=4s
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, 0, timeout=2)                 
        
    @allure.title("充电提醒_重启场景_启动后displaySoc未上报") 
    @pytest.mark.full
    def test_caseid_1987945(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0    
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 0.0) 
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # displaySoc= 100.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # pluggerStatus 从0跳1
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=2)
        self.ipdu.pause_bus_send("propulsioncan")
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 6, "chargeTargetSoc": 0.0}}, timeout=2)
        self.ipdu.resume_bus_send("propulsioncan")  
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=3)

    @allure.title("充电提醒_重启场景_启动后chargeTargetSoc未上报") 
    @pytest.mark.full
    def test_caseid_1987946(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0    
        self.ipdu.pause_bus_send("chassiscan1")
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=3)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"isConnect": False, "chargeTargetSoc": 255.0}}, timeout=2)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 1) # pluggerStatus 从0跳1
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 1}})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=2)
        self.ipdu.resume_bus_send("chassiscan1")  
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=3)

    @allure.title("充电提醒_重启场景_重启前info=1") 
    @pytest.mark.full
    def test_caseid_1988065(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0        
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 0.0) # chargeTargetSoc=0.0
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 0.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3) # isConnect 从0跳3
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 3}})
        self.partner.ck_wti_warning_and_resp(hint, 1)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":hint, "info": '0'}]}, timeout=4) 
        
    @allure.title("充电提醒_重启场景_重启前info=2") 
    @pytest.mark.full
    def test_caseid_1988067(self): 
        hint = "Charge Reminder" 
        self.deafault_charge_reminder() # 前置info=0, displaySoc=80.0, chargeTargetSoc=90.0 
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr13, 'BookChrgnTarValFb', 100.0) # ChargingInfo.info.chargeTargetSoc
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 100.0) # HVSOCInfo.info.displaySoc         
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetHVSOCInfo", {}, {'out': {'displaySoc': 100}})
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"chargeTargetSoc": 100.0}})
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 2) # pluggerStatus 从0跳2
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, {"out": {"pluggerStatus": 2}})
        self.partner.ck_wti_warning_and_resp(hint, 2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, {"out":[{"name":"Charge Reminder" , "info": '0'}]}, timeout=4) 
                                                
@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIServiceVoltage")
class TestLowVoltageServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("LowVoltageService", "client"),("WTIService", "client"),("VehicleModeService", "client")])

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

    @allure.title("遍历_通知和获取低压蓄电池指示灯") 
    @pytest.mark.full
    def test_caseid_1984305(self):
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',0)
        self.partner.empty_all(0.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "1"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',2)
        sleep(0.5)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "1"}]})
        self.partner.empty_all()
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(0.5)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "0"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',0)
        sleep(0.5)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "0"}]})
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "0"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "0"}]})
        
    @allure.title("遍历_通知和获取低压蓄电池指示灯") 
    @pytest.mark.full
    def test_caseid_1984304(self):
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',1)
        sleep(0.5)
        for usagemode in [0,1,2,11]:#使用者模式不满足时不能上报
            logger.info(f"切换使用者模式为{usagemode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",usagemode)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "0"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        sleep(0.5)
        for sigin1 in list(range(9,15))+[0,3,4,5]: #信号不满足时不能上报
            logger.info(f"切换LVPwrSplyErrSts为{sigin1}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',sigin1)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "0"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",0)
        sleep(0.5)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn') #E2E失败时&使用者模式不满足
        sleep(1)
        for usagemode in [0,1,2,11]:
            logger.info(f"切换使用者模式为{usagemode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",usagemode)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "0"}]})
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        sleep(0.5)
        for sigin2 in [1,2,6,7,8,15]: #信号切换LVPwrSplyErrSts为满足时上报
            logger.info(f"切换LVPwrSplyErrSts为{sigin2}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',sigin2)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "1"}]})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',0)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "0"}]})
        for sigin3 in [1,2]: #信号切换ULoWarnULoWarn为满足时上报
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',sigin3)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "1"}]})
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetTelltaleList",{},
                                          {"out":[{"name":"Low Voltage Battery", "state": "1"}]})
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',0)
            sleep(0.5)
            self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"TelltaleList",
                                          {"list":[{"name":"Low Voltage Battery", "state": "0"}]})

    @allure.title("WTI高压筛查validity") 
    @pytest.mark.full
    def test_caseid_1989366(self):
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',0)
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai',0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts")
        self.partner.empty_all(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',1)#低压电池1
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Low Battery Warning1", "info": "1"}]})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',4) #低压电池2
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Low Battery Warning2", "info": "4"}]})
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 1) #动力系统故障
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Power System Failure", "info": "9"}]})
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', 13) 
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Power System Failure", "info": "0"}]},timeout=2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr20, 'EgyRgnLvlAct', 1)#能量回收限制
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Energy Regen Limit", "info": "1"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai',1) #低压系统故障信息3
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Low Battery Warning3", "info": "1"}]})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",1)
        # self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Low Battery Warning2", "info": "0"}]},timeout=2)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList", {"list":[{"name":"Energy Regen Limit", "info": "0"},{"name":"Low Battery Warning3", "info": "0"}]},timeout=2)
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts")
            
    @allure.title("遍历_通知和获取低压系统故障信息1_E2E失败时信号改变") 
    @pytest.mark.full
    def test_caseid_1984306(self):
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',0)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',1)
        sleep(1)
        self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "1"}]})
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "1"}]})
        
    @allure.title("遍历_通知和获取低压系统故障信息1_E2E失败时处理") 
    @pytest.mark.full
    def test_caseid_1984002(self):
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',0)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "1"}]})
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "2"}]})
        for usagemode in [0,1,2,11]:
            logger.info(f"--切换使用者模式为{usagemode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",usagemode)
            sleep(0.5)
            self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "0"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn')
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "1"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',1)#两个信号同时满足上报2
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',0)
        sleep(1)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "1"}]})
        
    @allure.title("遍历_获取和通知低压系统故障信息2_4跳F") 
    @pytest.mark.sanity
    def test_caseid_1989615(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",13)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',4)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning2", "info": "4"}]})
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',15)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning2", "info": "F"}]})

    @allure.title("遍历_获取和通知低压系统故障信息2") 
    @pytest.mark.smoke
    def test_caseid_1983972(self):
        sleep(2)
        def info (usagemode,value):
            if usagemode == 13 and value == 4:
                return "4"
            elif usagemode == 13 and value == 5:
                return "4"
            elif usagemode == 13 and value == 15:
                return "F"
            else:
                return "0"
        for usagemode1 in [0,1,2,11,13]:
            for sigin in range (16):
                logger.info(f"--切换使用者模式为{usagemode1}且信号发送{sigin}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",usagemode1)
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',sigin)
                self.partner.empty_all(1)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning2", "info": info(usagemode1,sigin)}]})

    @allure.title("遍历_获取和通知低压系统故障信息3") 
    @pytest.mark.smoke
    def test_caseid_1983970(self):
        sleep(2)
        for usagemode1 in [0,1,2,11,13]:
            for sigin in range (16):
                logger.info(f"--切换使用者模式为{usagemode1}且信号发送{sigin}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",usagemode1)
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai',sigin)
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecMai',sigin)
                sleep(1)
                if usagemode1 in [2,11,13]:
                    if sigin in [1,3,5]:
                        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                            {"list":[{"name":"Low Battery Warning3", "info": "1"}]})
                        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                            {"out":[{"name":"Low Battery Warning3", "info": "1"}]})
                    else: 
                        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning3", "info": "0"}]})
                else: 
                    self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning3", "info": "0"}]})

    @allure.title("遍历_通知和获取低压系统故障信息1") 
    @pytest.mark.smoke
    def test_caseid_1983971(self):
        sleep(2)
        def info (usagemode,value):
            if usagemode == 13 and value == 1:
                return "2"
            elif usagemode == 13 and value == 2:
                return "2"
            elif usagemode == 13 and value == 6:
                return "2"
            elif usagemode == 13 and value == 7:
                return "2"
            elif usagemode == 13 and value == 8:
                return "2"
            else:
                return "0"
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',1)
        self.partner.empty_all(0.5)
        for usagemode in [0,1,2,11,13]:
            logger.info(f"--切换使用者模式为{usagemode}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",usagemode)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',1)
            sleep(0.5)
            if usagemode == 13:
                self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "1"}]})
            else:
                self.partner.ck_no_specific_event(WTI_SERVICE_CLIENT,"WarningMsgList","Low Battery Warning1")
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "0"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',2)
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": "2"}]})
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr08, 'ULoWarnULoWarn',0)
        sleep(0.5)
        self.partner.ck_s2s_event(WTI_SERVICE_CLIENT,"WarningMsgList",
                                          {"list":[{"name":"Low Battery Warning1", "info": "0"}]})
        self.partner.empty_all(0.5)
        for usagemode1 in [0,1,2,11,13]:
            for sigin in range(16):
                logger.info(f"--切换使用者模式为{usagemode1}并且信号发送{sigin}")
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,"VehModMngtGlbSafe1UsgModSts",usagemode1)
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr06, 'LVPwrSplyErrSts',sigin)
                self.partner.empty_all(1)
                self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{},
                                          {"out":[{"name":"Low Battery Warning1", "info": info(usagemode1,sigin)}]})                
                      
######################################################################################################################################################## 

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIServiceVoltage")
class TestWTIServiceVoltage800V(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("HighVoltageService", "client"),
                                     ("WTIService", "client"),
                                     ("ChassisService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()
        self.sd_tester.write_single_ccp(962, 2) #800V
        self.sd_tester.write_single_ccp(973, 2) #支持交直流
        sleep(3)
        self.nucapp.bgm_power_off()
        self.nucapp.bgm_power_on()
        self.partner.wait_for_service_reconnect(HIGHVOLTAGE_SERVICE_CLIENT)
        sleep(5)#防止诊断超时报list index out of range
        
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
        self.ipdu.set_vehspd(0)
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 0)        
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0) 
        sleep(0.5)
        self.io.set_four_door_close()
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)
    def set_Energy_Regen_Limit(self, UsgMod=13, egy=1, drv=13, resv=1, info=1, timeout=2):
        '''能量回收限制信息'''
        self.sd_tester.change_usage_mode(UsgMod)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1', resv) # EnergyRecoveryInfo.info.value=0%
        self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', drv)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr20, 'EgyRgnLvlAct', egy)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {}, 
                                              {"out":[{"name":"Energy Regen Limit", "info": str(info)}]}, timeout=timeout)
        self.partner.empty_all()
         
    @allure.title("能量回收限制信息_其他条件满足_遍历DrvPfmncRedn") 
    @pytest.mark.full
    def test_caseid_1988410(self): # DrvPfmncRedn|Energy Regen Limit|EgyRgnLvlAct|EnergyRecoveryInfo,value:|wti current mode
        hint = "Energy Regen Limit" 
        self.set_Energy_Regen_Limit()
        for drv in range(16):
            self.ipdu.set(self.ipdu.chassiscan2.EcmChas2Fr31, 'DrvPfmncRedn', drv)
            value = 1 if drv == 13 else 0
            if drv in [0, 13, 14]:
                self.partner.ck_wti_warning_and_resp(hint, value)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)
                
    @allure.title("能量回收限制信息_其他条件满足_遍历EgyRgnLvlAct") 
    @pytest.mark.sanity
    def test_caseid_1989617(self): 
        hint = "Energy Regen Limit" 
        self.set_Energy_Regen_Limit()
        for egy in range(4):
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr20, 'EgyRgnLvlAct', egy)
            value = 1 if egy in [1, 2] else 0
            if egy in [0, 1, 3]:
                self.partner.ck_wti_warning_and_resp(hint, value)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)
                
    @allure.title("能量回收限制信息_其他条件满足_遍历EnergyRecoveryInfo.info.value") 
    @pytest.mark.sanity
    def test_caseid_1988412(self): 
        hint = "Energy Regen Limit"                 
        self.set_Energy_Regen_Limit(egy=0, resv=2)
        for resv in range(1, 12):
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1', resv)
            value = 0 if resv == 1 else 1
            if resv in [1, 2]:
                self.partner.ck_wti_warning_and_resp(hint, value)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)
        for resv in [0, 12, 13, 14, 15]:
            self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1', resv)
            self.partner.ck_wti_no_warning_and_ck_resp(hint, 1)

    @allure.title("能量回收限制信息_其他条件满足_遍历UsgMod") 
    @pytest.mark.full
    def test_caseid_1988413(self): 
        hint = "Energy Regen Limit"                 
        self.set_Energy_Regen_Limit(egy=0, resv=2)
        for UsgMod in [0, 1, 2, 11, 13]:                
            self.sd_tester.change_usage_mode(UsgMod)
            value = 1 if UsgMod == 13 else 0
            if UsgMod in [0, 13]:
                self.partner.ck_wti_warning_and_resp(hint, value)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, value)

    @allure.title("能量回收限制信息_EgyRgnLvlAct和EnergyRecoveryInfo.info.value均满足条件后单个恢复") 
    @pytest.mark.full
    def test_caseid_1988442(self): 
        hint = "Energy Regen Limit"   
        self.set_Energy_Regen_Limit(egy=0, resv=2)        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr20, 'EgyRgnLvlAct', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.chassiscan1.EcmChas1Fr27, 'ResvFb1', 1)
        self.partner.ck_wti_no_warning_and_ck_resp(hint, 1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr20, 'EgyRgnLvlAct', 0)
        self.partner.ck_wti_warning_and_resp(hint, 0)
                        
    @allure.title("能量回收限制信息_重启场景_启动后EnergyRecoveryInfo.info.value未上报") 
    @pytest.mark.full
    def test_caseid_1988414(self): # DrvPfmncRedn|Energy Regen Limit|EgyRgnLvlAct|EnergyRecoveryInfo,value:|wti current mode
        hint = "Energy Regen Limit"   
        self.set_Energy_Regen_Limit(egy=0, resv=2)
        self.ipdu.pause_bus_send("chassiscan1")
        sleep(2)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetEnergyRecoveryInfo", {},
                                              {"out":{"value":255}},timeout=3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT,"GetWarningMsgList",{}, 
                                              {"out":[{"name":hint, "info": '0'}]})
        self.ipdu.resume_bus_send("chassiscan1")  
        self.partner.ck_wti_warning_and_resp(hint, 1, timeout=3)

    @allure.title("充电枪连接指示_遍历ChargingInfo.info.isConnect") 
    @pytest.mark.sanity
    def test_caseid_1988415(self): # ChargingInfo,isConnected|Charging Gun Connected
        hint = "Charging Gun Connected" 
        last_value=0
        dict1={0:0, 1:1, 2:2, 3:3, 8:4, 9:5, 10:7, 4:8, 5:9, 6:10, 7:11}
        for signal,pluggerStatus in dict1.items():
            self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', signal)       
            if pluggerStatus == 0:
                value=0
            elif pluggerStatus not in [0, 4, 6, 8, 10]:
                value=1
            self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, 
                                                  {"out": {"isConnect": bool(value)}})
            if value != last_value:
                self.partner.ck_wti_telltale_and_resp(hint, value)
            else:
                self.partner.ck_wti_no_telltale_and_ck_resp(hint, value)
            last_value=value
            
    @allure.title("充电枪连接指示_重启场景_所有总线未恢复") 
    @pytest.mark.full
    def test_caseid_1988416(self): 
        hint = "Charging Gun Connected"  
        self.ipdu.set(self.ipdu.propulsioncan.CddObcPropFr01, 'OnBdChrgrHndlSts1', 1)     
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                              {"out":[{"name":"Charging Gun Connected", "state": "1"}]}, timeout=3)
        self.restart_bgm_and_connect_service(WTI_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)         
        self.partner.send_request_and_ck_resp(HIGHVOLTAGE_SERVICE_CLIENT, "GetChargingInfo", {}, 
                                                  {"out": {"isConnect": True}}, timeout=3)
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                              {"out":[{"name":"Charging Gun Connected", "state": "1"}]})
        
        self.ipdu.resume_all_bus_send()
        self.partner.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetTelltaleList", {}, 
                                              {"out":[{"name":"Charging Gun Connected", "state": "1"}]})