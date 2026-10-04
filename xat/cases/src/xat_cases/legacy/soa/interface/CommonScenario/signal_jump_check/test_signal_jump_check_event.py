# -*- coding: utf-8 -*-

"""
@Time    : 2024/06/05 08:55
@Author  : lei.tao
@Email   : lei.tao@jiduauto.com
"""
import time
import pytest
import allure
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.soa_partner.src.partner_const import *


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestACCServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("ACCService", 'client')])
        self.partner_key = "ACCService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("ACCService::SetACCSpeedStep_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986839(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe1SteerWhlTouchSwt1'])
        self.partner.ck_no_req(self.partner_key, "SetACCSpeedStep", timeout=0.2)

    @allure.title("ACCService::SetFollowDistanceLevel_BodyCAN::0x269同帧非相关信号跳变无异常event")
    def test_caseid_1986838(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=617, no_opera_signal=['SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 'SteerWhlScRightButtonLeSteerWhlTouchSwt2'])
        self.partner.ck_no_req(self.partner_key, "SetFollowDistanceLevel", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestBlueToothServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("BlueToothService", 'client')])
        self.partner_key = "BlueToothService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("BlueToothService::ConStsForAVP_ConnectivityCANFD::0x198同帧非相关信号跳变无异常event")
    def test_caseid_1986468(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=408, no_opera_signal=['BLEConStsForAVP'])
        self.partner.ck_no_event(self.partner_key, "ConStsForAVP", timeout=0.2)

    @allure.title("BlueToothService::MobDevSts_ConnectivityCANFD::0x198同帧非相关信号跳变无异常event")
    def test_caseid_1986469(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=408, no_opera_signal=['BLEMobDevSts'])
        self.partner.ck_no_event(self.partner_key, "MobDevSts", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestBonnetServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("BonnetService", 'client')])
        self.partner_key = "BonnetService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("BonnetService::OpenCloseStatus_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986459(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['HoodSts'])
        self.partner.ck_no_event(self.partner_key, "OpenCloseStatus", timeout=0.2)

    @allure.title("BonnetService::OpenCloseStatusValidity_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986458(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['HoodSts'])
        self.partner.ck_no_event(self.partner_key, "OpenCloseStatusValidity", timeout=0.2)

    @allure.title("BonnetService::Status_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986460(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['HoodSts'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestCarConfigServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("CarConfigService", 'client')])
        self.partner_key = "CarConfigService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("CarConfigService::NotifyCarConfigInfo_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986474(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['WhlCircum'])
        self.partner.ck_no_event(self.partner_key, "NotifyCarConfigInfo", timeout=0.2)

    @allure.title("CarConfigService::NotifyCarConfigInfo_BackboneFR::38-0-64同帧非相关信号跳变无异常event")
    def test_caseid_1986476(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2490432, no_opera_signal=['ListOfNodAv1', 'ListOfNodAv2', 'ListOfNodAv3', 'ListOfNodAv4', 'ListOfNodAv5', 'ListOfNodAv6', 'ListOfNodAv7', 'ListOfNodAv8'])
        self.partner.ck_no_event(self.partner_key, "NotifyCarConfigInfo", timeout=0.2)

    @allure.title("CarConfigService::NotifyCarConfigInfo_BackboneFR::39-2-8同帧非相关信号跳变无异常event")
    def test_caseid_1986475(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556424, no_opera_signal=['VinBlockNr', 'VinVINSignalPos1', 'VinVINSignalPos2', 'VinVINSignalPos3', 'VinVINSignalPos4', 'VinVINSignalPos5', 'VinVINSignalPos6', 'VinVINSignalPos7'])
        self.partner.ck_no_event(self.partner_key, "NotifyCarConfigInfo", timeout=0.2)

    @allure.title("CarConfigService::NotifyCarConfigInfo_BackboneFR::39-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986477(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557192, no_opera_signal=['VehCfgPrmExtBlkIDBytePosn1', 'VehCfgPrmExtCCPBytePosn2', 'VehCfgPrmExtCCPBytePosn3', 'VehCfgPrmExtCCPBytePosn4', 'VehCfgPrmExtCCPBytePosn5', 'VehCfgPrmExtCCPBytePosn6', 'VehCfgPrmExtCCPBytePosn7', 'VehCfgPrmExtCCPBytePosn8'])
        self.partner.ck_no_event(self.partner_key, "NotifyCarConfigInfo", timeout=0.2)

    @allure.title("CarConfigService::NotifyCarConfigInfo_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986478(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['VehCfgPrmBlkIDBytePosn1', 'VehCfgPrmCCPBytePosn2', 'VehCfgPrmCCPBytePosn3', 'VehCfgPrmCCPBytePosn4', 'VehCfgPrmCCPBytePosn5', 'VehCfgPrmCCPBytePosn6', 'VehCfgPrmCCPBytePosn7', 'VehCfgPrmCCPBytePosn8'])
        self.partner.ck_no_event(self.partner_key, "NotifyCarConfigInfo", timeout=0.2)

    @allure.title("CarConfigService::NotifyCltcPowerConsumption_BackboneFR::39-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986470(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557192, no_opera_signal=['VehCfgPrmExtBlkIDBytePosn1', 'VehCfgPrmExtCCPBytePosn2', 'VehCfgPrmExtCCPBytePosn3', 'VehCfgPrmExtCCPBytePosn4', 'VehCfgPrmExtCCPBytePosn5', 'VehCfgPrmExtCCPBytePosn6', 'VehCfgPrmExtCCPBytePosn7', 'VehCfgPrmExtCCPBytePosn8'])
        self.partner.ck_no_event(self.partner_key, "NotifyCltcPowerConsumption", timeout=0.2)

    @allure.title("CarConfigService::NotifyCltcPowerConsumption_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986471(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['VehCfgPrmBlkIDBytePosn1', 'VehCfgPrmCCPBytePosn2', 'VehCfgPrmCCPBytePosn3', 'VehCfgPrmCCPBytePosn4', 'VehCfgPrmCCPBytePosn5', 'VehCfgPrmCCPBytePosn6', 'VehCfgPrmCCPBytePosn7', 'VehCfgPrmCCPBytePosn8'])
        self.partner.ck_no_event(self.partner_key, "NotifyCltcPowerConsumption", timeout=0.2)

    @allure.title("CarConfigService::NotifyVIN_BackboneFR::39-2-8同帧非相关信号跳变无异常event")
    def test_caseid_1986473(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556424, no_opera_signal=['VinBlockNr', 'VinVINSignalPos1', 'VinVINSignalPos2', 'VinVINSignalPos3', 'VinVINSignalPos4', 'VinVINSignalPos5', 'VinVINSignalPos6', 'VinVINSignalPos7'])
        self.partner.ck_no_event(self.partner_key, "NotifyVIN", timeout=0.2)

    @allure.title("CarConfigService::NotifyWheelCircumference_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986472(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['WhlCircum'])
        self.partner.ck_no_event(self.partner_key, "NotifyWheelCircumference", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestCentralLockServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("CentralLockService", 'client')])
        self.partner_key = "CentralLockService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("CentralLockService::CenLckUpdEve_BodyCAN::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986453(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=256, no_opera_signal=['LockgCenStsUpdEve'])
        self.partner.ck_no_event(self.partner_key, "CenLckUpdEve", timeout=0.2)

    @allure.title("CentralLockService::CentralLockReminder_InfoCANFD::0x480同帧非相关信号跳变无异常event")
    def test_caseid_1986454(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=1152, no_opera_signal=['LockSysStsPrmt'])
        self.partner.ck_no_event(self.partner_key, "CentralLockReminder", timeout=0.2)

    @allure.title("CentralLockService::LockActTriggerSource_BackboneFR::40-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986455(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2621456, no_opera_signal=['LockgEventTrigsrc'])
        self.partner.ck_no_event(self.partner_key, "LockActTriggerSource", timeout=0.2)

    @allure.title("CentralLockService::LockStatus_BodyCAN::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986457(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=256, no_opera_signal=['LockgCenStsLockSt'])
        self.partner.ck_no_event(self.partner_key, "LockStatus", timeout=0.2)

    @allure.title("CentralLockService::LockSuccessTriggerSource_BodyCAN::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986456(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=256, no_opera_signal=['LockgCenStsTrigSrc'])
        self.partner.ck_no_event(self.partner_key, "LockSuccessTriggerSource", timeout=0.2)

    @allure.title("CentralLockService::NotifyCentralLockSysInfo_BodyCAN::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986452(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=256, no_opera_signal=['LockgCenStsLockSt', 'LockgCenStsTrigSrc', 'LockgCenStsUpdEve'])
        self.partner.ck_no_event(self.partner_key, "NotifyCentralLockSysInfo", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestChargeLidServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("ChargeLidService", 'client')])
        self.partner_key = "ChargeLidService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("ChargeLidService::ChargeLidFault_CEM_LIN2::0x38同帧非相关信号跳变无异常event")
    def test_caseid_1986278(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin2", message=56, no_opera_signal=['ChrgLidManvgDCorAcDcElecErrFb', 'ChrgLidManvgDCorAcDcOverTFb', 'ChrgLidManvgDCorAcDcOverVoltFb', 'ChrgLidManvgDCorAcDcUnderVoltFb'])
        self.partner.ck_no_event(self.partner_key, "ChargeLidFault", timeout=0.2)

    @allure.title("ChargeLidService::ChargeLidLightStatus_InfoCANFD::0x190同帧非相关信号跳变无异常event")
    def test_caseid_1986299(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=400, no_opera_signal=['FCSILEDIndctn'])
        self.partner.ck_no_event(self.partner_key, "ChargeLidLightStatus", timeout=0.2)

    @allure.title("ChargeLidService::ChargeLidPos_CEM_LIN2::0x38同帧非相关信号跳变无异常event")
    def test_caseid_1986300(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin2", message=56, no_opera_signal=['ChrgLidManvgDCorAcDcActPosn2'])
        self.partner.ck_no_event(self.partner_key, "ChargeLidPos", timeout=0.2)

    @allure.title("ChargeLidService::ChargeLidSwitchStatus_BackboneFR::40-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986298(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2621456, no_opera_signal=['ChrgLidDCorAcDctSwtReq'])
        self.partner.ck_no_event(self.partner_key, "ChargeLidSwitchStatus", timeout=0.2)

    @allure.title("ChargeLidService::ChargeLidWarnSts_CEM_LIN2::0x38同帧非相关信号跳变无异常event")
    def test_caseid_1986297(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin2", message=56, no_opera_signal=['ChrgLidManvgDCorAcDcBlkFb', 'ChrgLidManvgDCorAcDcOverTrvlFb'])
        self.partner.ck_no_event(self.partner_key, "ChargeLidWarnSts", timeout=0.2)

    @allure.title("ChargeLidService::Status_BackboneFR::39-3-8同帧非相关信号跳变无异常event")
    def test_caseid_1986301(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556680, no_opera_signal=['ChrgLidRearSts'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestChassisServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("ChassisService", 'client')])
        self.partner_key = "ChassisService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("ChassisService::absActSts_BackboneFR::57-2-4同帧非相关信号跳变无异常event")
    def test_caseid_1986879(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3736068, no_opera_signal=['AbsCtrlActvForWhlFrntLe', 'AbsCtrlActvForWhlFrntRi', 'AbsCtrlActvForWhlReLe', 'AbsCtrlActvForWhlReRi'])
        self.partner.ck_no_event(self.partner_key, "absActSts", timeout=0.2)

    @allure.title("ChassisService::absFailSts_BackboneFR::57-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986878(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3736840, no_opera_signal=['AbsSts'])
        self.partner.ck_no_event(self.partner_key, "absFailSts", timeout=0.2)

    @allure.title("ChassisService::absWarnIndicateReqSts_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986885(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "absWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::absWarnIndicateReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986886(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq'])
        self.partner.ck_no_event(self.partner_key, "absWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::AutoHoldChanged_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986864(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['AutHldSoftSwtEnaSts'])
        self.partner.ck_no_event(self.partner_key, "AutoHoldChanged", timeout=0.2)

    @allure.title("ChassisService::AutoHoldWorkState_BackboneFR::57-7-32同帧非相关信号跳变无异常event")
    def test_caseid_1986875(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3737376, no_opera_signal=['LampReqByVehHld'])
        self.partner.ck_no_event(self.partner_key, "AutoHoldWorkState", timeout=0.2)

    @allure.title("ChassisService::avhDisplayReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986874(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['DispMsgByVehHld'])
        self.partner.ck_no_event(self.partner_key, "avhDisplayReqSts", timeout=0.2)

    @allure.title("ChassisService::BrakeDiscOverHeatSts_ChassisCAN2::0x270同帧非相关信号跳变无异常event")
    def test_caseid_1986843(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=624, no_opera_signal=['WhlBrkOvrheatd'])
        self.partner.ck_no_event(self.partner_key, "BrakeDiscOverHeatSts", timeout=0.2)

    @allure.title("ChassisService::brkRelsWarnReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986877(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['BrkRelsWarnReq'])
        self.partner.ck_no_event(self.partner_key, "brkRelsWarnReqSts", timeout=0.2)

    @allure.title("ChassisService::brkSysWarnIndicateReqSts_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986895(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "brkSysWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::brkSysWarnIndicateReqSts_BackboneFR::57-1-8同帧非相关信号跳变无异常event")
    def test_caseid_1986897(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735816, no_opera_signal=['EpbDrvrDisp'])
        self.partner.ck_no_event(self.partner_key, "brkSysWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::brkSysWarnIndicateReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986898(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['EpbLampReqEpbLampReq', 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 'BrkSysWarnIndcnReq', 'BrkFldLvl'])
        self.partner.ck_no_event(self.partner_key, "brkSysWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::brkSysWarnIndicateReqSts_BackboneFR::7-2-4同帧非相关信号跳变无异常event")
    def test_caseid_1986896(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=459268, no_opera_signal=['EpbDrvrDispSec'])
        self.partner.ck_no_event(self.partner_key, "brkSysWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::brkSysWarnIndicateReqSts_BackboneFR::7-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986899(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=460864, no_opera_signal=['EpbLampReqSecEpbLampReq', 'BrkSysWarnIndcnReqSec'])
        self.partner.ck_no_event(self.partner_key, "brkSysWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::brkSysWarnMsgDisplayReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986880(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['BrkMsgWarnReq'])
        self.partner.ck_no_event(self.partner_key, "brkSysWarnMsgDisplayReqSts", timeout=0.2)

    @allure.title("ChassisService::ChassisFault_BackboneFR::17-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986917(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1114370, no_opera_signal=['VehSpdIndcdVehSpdIndcd', 'VehSpdIndcdVeSpdIndcdUnit'])
        self.partner.ck_no_event(self.partner_key, "ChassisFault", timeout=0.2)

    @allure.title("ChassisService::ChassisFault_BackboneFR::51-0-2同帧非相关信号跳变无异常event")
    def test_caseid_1986920(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3342338, no_opera_signal=['WhlRotToothCntrFrntLe', 'WhlRotToothCntrFrntRi', 'WhlRotToothCntrReLe', 'WhlRotToothCntrReRi', 'WhlSpdCircumlFrntLe', 'WhlSpdCircumlFrntLeQf', 'WhlSpdCircumlFrntRiQf', 'WhlSpdCircumlFrntWhlSpdCircumlFrntRi', 'WhlSpdCircumlReLe', 'WhlSpdCircumlReLeQf', 'WhlSpdCircumlReRi', 'WhlSpdCircumlReRiQf'])
        self.partner.ck_no_event(self.partner_key, "ChassisFault", timeout=0.2)

    @allure.title("ChassisService::ChassisFault_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986919(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['VehMtnStVehMtnSt'])
        self.partner.ck_no_event(self.partner_key, "ChassisFault", timeout=0.2)

    @allure.title("ChassisService::ChassisFault_BackboneFR::57-0-4同帧非相关信号跳变无异常event")
    def test_caseid_1986918(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735556, no_opera_signal=['VehSpdLgtA', 'VehSpdLgtQf'])
        self.partner.ck_no_event(self.partner_key, "ChassisFault", timeout=0.2)

    @allure.title("ChassisService::ChassisFault_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986916(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['AutHldSoftSwtEnaSts'])
        self.partner.ck_no_event(self.partner_key, "ChassisFault", timeout=0.2)

    @allure.title("ChassisService::CreepMode_ChassisCAN1::0x2C4同帧非相关信号跳变无异常event")
    def test_caseid_1986862(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=708, no_opera_signal=['CrpModAct'])
        self.partner.ck_no_event(self.partner_key, "CreepMode", timeout=0.2)

    @allure.title("ChassisService::DisplaySpeedChanged_BackboneFR::17-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986906(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1114370, no_opera_signal=['VehSpdIndcdVehSpdIndcd', 'VehSpdIndcdVeSpdIndcdUnit'])
        self.partner.ck_no_event(self.partner_key, "DisplaySpeedChanged", timeout=0.2)

    @allure.title("ChassisService::DisplaySpeedChanged_BackboneFR::57-0-4同帧非相关信号跳变无异常event")
    def test_caseid_1986907(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735556, no_opera_signal=['VehSpdLgtQf'])
        self.partner.ck_no_event(self.partner_key, "DisplaySpeedChanged", timeout=0.2)

    @allure.title("ChassisService::EGSMVirtualShiftReq_PropulsionCAN::0x135同帧非相关信号跳变无异常event")
    def test_caseid_1986859(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=309, no_opera_signal=['DrvrGearShiftReqInv'])
        self.partner.ck_no_event(self.partner_key, "EGSMVirtualShiftReq", timeout=0.2)

    @allure.title("ChassisService::EmergencySystemState_BackboneFR::57-1-8同帧非相关信号跳变无异常event")
    def test_caseid_1986840(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735816, no_opera_signal=['EmgyBrkLiReqEmgyBrk'])
        self.partner.ck_no_event(self.partner_key, "EmergencySystemState", timeout=0.2)

    @allure.title("ChassisService::epbDisplayReqSts_BackboneFR::57-1-8同帧非相关信号跳变无异常event")
    def test_caseid_1986892(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735816, no_opera_signal=['EpbDrvrDisp'])
        self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts", timeout=0.2)

    @allure.title("ChassisService::epbDisplayReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986893(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['EpbLampReqEpbLampReq', 'BrkSysWarnIndcnReq'])
        self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts", timeout=0.2)

    @allure.title("ChassisService::epbDisplayReqSts_BackboneFR::7-2-4同帧非相关信号跳变无异常event")
    def test_caseid_1986891(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=459268, no_opera_signal=['EpbDrvrDispSec'])
        self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts", timeout=0.2)

    @allure.title("ChassisService::epbDisplayReqSts_BackboneFR::7-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986894(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=460864, no_opera_signal=['EpbLampReqSecEpbLampReq', 'BrkSysWarnIndcnReqSec'])
        self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts", timeout=0.2)

    @allure.title("ChassisService::epbIndicatorLightReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986889(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['EpbLampReqEpbLampReq'])
        self.partner.ck_no_event(self.partner_key, "epbIndicatorLightReqSts", timeout=0.2)

    @allure.title("ChassisService::epbIndicatorLightReqSts_BackboneFR::7-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986890(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=460864, no_opera_signal=['EpbLampReqSecEpbLampReq'])
        self.partner.ck_no_event(self.partner_key, "epbIndicatorLightReqSts", timeout=0.2)

    @allure.title("ChassisService::epbIndicatorLightReqStsValidity_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986853(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['EpbLampReqEpbLampReq'])
        self.partner.ck_no_event(self.partner_key, "epbIndicatorLightReqStsValidity", timeout=0.2)

    @allure.title("ChassisService::epbIndicatorLightReqStsValidity_BackboneFR::7-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986852(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=460864, no_opera_signal=['EpbLampReqSecEpbLampReq'])
        self.partner.ck_no_event(self.partner_key, "epbIndicatorLightReqStsValidity", timeout=0.2)

    @allure.title("ChassisService::EPBOperationStatus_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986866(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['EpbStsEpbSts'])
        self.partner.ck_no_event(self.partner_key, "EPBOperationStatus", timeout=0.2)

    @allure.title("ChassisService::epbWarnChimeReqSts_BackboneFR::57-0-4同帧非相关信号跳变无异常event")
    def test_caseid_1986910(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735556, no_opera_signal=['VehSpdLgtA'])
        self.partner.ck_no_event(self.partner_key, "epbWarnChimeReqSts", timeout=0.2)

    @allure.title("ChassisService::epbWarnChimeReqSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986908(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['EpbLampReqEpbLampReq'])
        self.partner.ck_no_event(self.partner_key, "epbWarnChimeReqSts", timeout=0.2)

    @allure.title("ChassisService::epbWarnChimeReqSts_BackboneFR::7-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986909(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=460864, no_opera_signal=['EpbLampReqSecEpbLampReq'])
        self.partner.ck_no_event(self.partner_key, "epbWarnChimeReqSts", timeout=0.2)

    @allure.title("ChassisService::EPedlModeInfo_ChassisCAN2::0x120同帧非相关信号跳变无异常event")
    def test_caseid_1986846(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=288, no_opera_signal=['EPedlModSts'])
        self.partner.ck_no_event(self.partner_key, "EPedlModeInfo", timeout=0.2)

    @allure.title("ChassisService::EPedlModeInfo_ChassisCAN2::0x200同帧非相关信号跳变无异常event")
    def test_caseid_1986844(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=512, no_opera_signal=['EPedlInhbnSts'])
        self.partner.ck_no_event(self.partner_key, "EPedlModeInfo", timeout=0.2)

    @allure.title("ChassisService::EPedlModeInfo_ChassisCAN2::0x333同帧非相关信号跳变无异常event")
    def test_caseid_1986845(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=819, no_opera_signal=['EPedlDrvrIndcnMsg'])
        self.partner.ck_no_event(self.partner_key, "EPedlModeInfo", timeout=0.2)

    @allure.title("ChassisService::escOffIndicateLightSts_BackboneFR::56-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986887(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3670274, no_opera_signal=['EscStEscSt'])
        self.partner.ck_no_event(self.partner_key, "escOffIndicateLightSts", timeout=0.2)

    @allure.title("ChassisService::escOffIndicateLightSts_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986888(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['DrvModEscOffDrvModEscOff'])
        self.partner.ck_no_event(self.partner_key, "escOffIndicateLightSts", timeout=0.2)

    @allure.title("ChassisService::escWarnIndicateReqSts_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986883(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "escWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::escWarnIndicateReqSts_BackboneFR::57-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986884(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3736840, no_opera_signal=['EscWarnIndcnReqEscWarnIndcnReq'])
        self.partner.ck_no_event(self.partner_key, "escWarnIndicateReqSts", timeout=0.2)

    @allure.title("ChassisService::ESCWorkStatus_BackboneFR::56-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986881(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3670274, no_opera_signal=['EscStEscSt'])
        self.partner.ck_no_event(self.partner_key, "ESCWorkStatus", timeout=0.2)

    @allure.title("ChassisService::Gear_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986912(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "Gear", timeout=0.2)

    @allure.title("ChassisService::Gear_PropulsionCAN::0x04B同帧非相关信号跳变无异常event")
    def test_caseid_1986913(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=75, no_opera_signal=['GearLvrIndcn'])
        self.partner.ck_no_event(self.partner_key, "Gear", timeout=0.2)

    @allure.title("ChassisService::Gear_PropulsionCAN::0x155同帧非相关信号跳变无异常event")
    def test_caseid_1986914(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=341, no_opera_signal=['TrsmParkLockdTrsmParkLockd'])
        self.partner.ck_no_event(self.partner_key, "Gear", timeout=0.2)

    @allure.title("ChassisService::GearFault_ChassisCAN1::0x2C4同帧非相关信号跳变无异常event")
    def test_caseid_1986869(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=708, no_opera_signal=['GearLvrFaultIndcn'])
        self.partner.ck_no_event(self.partner_key, "GearFault", timeout=0.2)

    @allure.title("ChassisService::HDCFunctionAvailableChanged_BackboneFR::57-7-32同帧非相关信号跳变无异常event")
    def test_caseid_1986865(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3737376, no_opera_signal=['SwtStsforHillDwnCtrl'])
        self.partner.ck_no_event(self.partner_key, "HDCFunctionAvailableChanged", timeout=0.2)

    @allure.title("ChassisService::hdcWorkSts_BackboneFR::57-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986876(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3736840, no_opera_signal=['MsgReqByHillDwnCtrl'])
        self.partner.ck_no_event(self.partner_key, "hdcWorkSts", timeout=0.2)

    @allure.title("ChassisService::InterUse_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986900(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['BrkPedlPsdBrkPedlPsd', 'BrkPedlPsdQf'])
        self.partner.ck_no_event(self.partner_key, "InterUse", timeout=0.2)

    @allure.title("ChassisService::LaunchMode_ChassisCAN1::0x24B同帧非相关信号跳变无异常event")
    def test_caseid_1986848(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=587, no_opera_signal=['LnchModSts'])
        self.partner.ck_no_event(self.partner_key, "LaunchMode", timeout=0.2)

    @allure.title("ChassisService::LaunchMode_ChassisCAN1::0x391同帧非相关信号跳变无异常event")
    def test_caseid_1986847(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=913, no_opera_signal=['LnchModIndcnMsg'])
        self.partner.ck_no_event(self.partner_key, "LaunchMode", timeout=0.2)

    @allure.title("ChassisService::NotifyBrkFldLvlWarnMsgStatus_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986872(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['BrkFldLvl'])
        self.partner.ck_no_event(self.partner_key, "NotifyBrkFldLvlWarnMsgStatus", timeout=0.2)

    @allure.title("ChassisService::NotifyShiftRequestInfo_InfoCANFD::0x0C0同帧非相关信号跳变无异常event")
    def test_caseid_1986857(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=192, no_opera_signal=['CDCDrvrGearShiftParkReq1', 'CDCDrvrGearShiftDirReq1DwnRTipAut', 'CDCDrvrGearShiftDirReq1UpDTipAut', 'CDCDrvrGearShiftDirReq2DwnRTipAut', 'CDCDrvrGearShiftDirReq2UpDTipAut'])
        self.partner.ck_no_event(self.partner_key, "NotifyShiftRequestInfo", timeout=0.2)

    @allure.title("ChassisService::NotifyShiftRequestInfo_PropulsionCAN::0x135同帧非相关信号跳变无异常event")
    def test_caseid_1986856(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=309, no_opera_signal=['DrvrGearShiftParkReq1'])
        self.partner.ck_no_event(self.partner_key, "NotifyShiftRequestInfo", timeout=0.2)

    @allure.title("ChassisService::NotifyShiftRequestInfo_PropulsionCAN::0x136同帧非相关信号跳变无异常event")
    def test_caseid_1986855(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=310, no_opera_signal=['DrvrGearShiftDirReq1DwnDwnTipAut', 'DrvrGearShiftDirReq1UpUpTipAut', 'DrvrGearShiftDirReq2DwnDwnTipAut', 'DrvrGearShiftDirReq2UpUpTipAut'])
        self.partner.ck_no_event(self.partner_key, "NotifyShiftRequestInfo", timeout=0.2)

    @allure.title("ChassisService::PropulsionStatus_ChassisCAN2::0x210同帧非相关信号跳变无异常event")
    def test_caseid_1986851(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=528, no_opera_signal=['PTStsForRace'])
        self.partner.ck_no_event(self.partner_key, "PropulsionStatus", timeout=0.2)

    @allure.title("ChassisService::SpeedChanged_BackboneFR::57-0-4同帧非相关信号跳变无异常event")
    def test_caseid_1986905(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735556, no_opera_signal=['VehSpdLgtA', 'VehSpdLgtQf'])
        self.partner.ck_no_event(self.partner_key, "SpeedChanged", timeout=0.2)

    @allure.title("ChassisService::SportModeAvailableStatus_ChassisCAN2::0x2F0同帧非相关信号跳变无异常event")
    def test_caseid_1986861(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=752, no_opera_signal=['PrpsnModSptBlkd'])
        self.partner.ck_no_event(self.partner_key, "SportModeAvailableStatus", timeout=0.2)

    @allure.title("ChassisService::SteerErrorReqStatus_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986867(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "SteerErrorReqStatus", timeout=0.2)

    @allure.title("ChassisService::SteerErrorReqStatus_ChassisCAN1::0x1BC同帧非相关信号跳变无异常event")
    def test_caseid_1986868(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=444, no_opera_signal=['SteerErrReq'])
        self.partner.ck_no_event(self.partner_key, "SteerErrorReqStatus", timeout=0.2)

    @allure.title("ChassisService::SuperEnergySaveMode_ADCANFD::0x121同帧非相关信号跳变无异常event")
    def test_caseid_1986860(self):
        self.ipdu.filter_special_message_send(bus_name="adcanfd", message=289, no_opera_signal=['DrvModSetFbk'])
        self.partner.ck_no_event(self.partner_key, "SuperEnergySaveMode", timeout=0.2)

    @allure.title("ChassisService::SuspensionFailureSts_ChassisCAN2::0x2AF同帧非相关信号跳变无异常event")
    def test_caseid_1986842(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=687, no_opera_signal=['SuspFailrStsSuspFailrSts', 'SuspFailrStsTypQf', 'SuspFailrSts3'])
        self.partner.ck_no_event(self.partner_key, "SuspensionFailureSts", timeout=0.2)

    @allure.title("ChassisService::SuspensionLevel_ChassisCAN2::0x213同帧非相关信号跳变无异常event")
    def test_caseid_1986863(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=531, no_opera_signal=['ActModOfDampr'])
        self.partner.ck_no_event(self.partner_key, "SuspensionLevel", timeout=0.2)

    @allure.title("ChassisService::TorqueMode_ChassisCAN1::0x35B同帧非相关信号跳变无异常event")
    def test_caseid_1986870(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=859, no_opera_signal=['TqModAct'])
        self.partner.ck_no_event(self.partner_key, "TorqueMode", timeout=0.2)

    @allure.title("ChassisService::TouchShiftActiveSts_PropulsionCAN::0x135同帧非相关信号跳变无异常event")
    def test_caseid_1986841(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=309, no_opera_signal=['GearLvrIllmnSts'])
        self.partner.ck_no_event(self.partner_key, "TouchShiftActiveSts", timeout=0.2)

    @allure.title("ChassisService::TraveledDistance_BackboneFR::39-4-8同帧非相关信号跳变无异常event")
    def test_caseid_1986854(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556936, no_opera_signal=['TotDstTrvldHiResl'])
        self.partner.ck_no_event(self.partner_key, "TraveledDistance", timeout=0.2)

    @allure.title("ChassisService::VehicleAcceleration_PassiveSafetyCAN::0x012同帧非相关信号跳变无异常event")
    def test_caseid_1986858(self):
        self.ipdu.filter_special_message_send(bus_name="passivesafetycan", message=18, no_opera_signal=['ADataRawSafeALgt', 'ADataRawSafeALat', 'ADataRawSafeAVert'])
        self.partner.ck_no_event(self.partner_key, "VehicleAcceleration", timeout=0.2)

    @allure.title("ChassisService::VehicleMotionState_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986911(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['VehMtnStVehMtnSt'])
        self.partner.ck_no_event(self.partner_key, "VehicleMotionState", timeout=0.2)

    @allure.title("ChassisService::vehicleReady_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986873(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "vehicleReady", timeout=0.2)

    @allure.title("ChassisService::VehiclestandstillSts_ChassisCAN1::0x1F0同帧非相关信号跳变无异常event")
    def test_caseid_1986849(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=496, no_opera_signal=['StandStillMgrStsForHld1'])
        self.partner.ck_no_event(self.partner_key, "VehiclestandstillSts", timeout=0.2)

    @allure.title("ChassisService::WheelImpluseCounter_BackboneFR::51-0-2同帧非相关信号跳变无异常event")
    def test_caseid_1986915(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3342338, no_opera_signal=['WhlRotToothCntrFrntLe', 'WhlRotToothCntrFrntRi', 'WhlRotToothCntrReLe', 'WhlRotToothCntrReRi'])
        self.partner.ck_no_event(self.partner_key, "WheelImpluseCounter", timeout=0.2)

    @allure.title("ChassisService::WheelSlipRate_ChassisCAN1::0x2F0同帧非相关信号跳变无异常event")
    def test_caseid_1986850(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=752, no_opera_signal=['WhlSlipRateFL', 'WhlSlipRateFR', 'WhlSlipRateRL', 'WhlSlipRateRR'])
        self.partner.ck_no_event(self.partner_key, "WheelSlipRate", timeout=0.2)

    @allure.title("ChassisService::WheelSpeed_BackboneFR::51-0-2同帧非相关信号跳变无异常event")
    def test_caseid_1986882(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3342338, no_opera_signal=['WhlSpdCircumlFrntLe', 'WhlSpdCircumlFrntLeQf', 'WhlSpdCircumlFrntRiQf', 'WhlSpdCircumlFrntWhlSpdCircumlFrntRi', 'WhlSpdCircumlReLe', 'WhlSpdCircumlReLeQf', 'WhlSpdCircumlReRi', 'WhlSpdCircumlReRiQf'])
        self.partner.ck_no_event(self.partner_key, "WheelSpeed", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestClimateControlServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("ClimateControlService", 'client')])
        self.partner_key = "ClimateControlService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("ClimateControlService::AutoBlowMode_BodyCAN::0x40D同帧非相关信号跳变无异常event")
    def test_caseid_1986434(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1037, no_opera_signal=['ResrvdSigForECM4'])
        self.partner.ck_no_event(self.partner_key, "AutoBlowMode", timeout=0.2)

    @allure.title("ClimateControlService::ClimateAirFlow_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986295(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['HvacAirMFlowEstimd'])
        self.partner.ck_no_event(self.partner_key, "ClimateAirFlow", timeout=0.2)

    @allure.title("ClimateControlService::ClimateFault_BodyCAN::0x40D同帧非相关信号跳变无异常event")
    def test_caseid_1986433(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1037, no_opera_signal=['RemClimaWarn'])
        self.partner.ck_no_event(self.partner_key, "ClimateFault", timeout=0.2)

    @allure.title("ClimateControlService::ClimateSystemStatus_BodyCAN::0x419同帧非相关信号跳变无异常event")
    def test_caseid_1986446(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1049, no_opera_signal=['ClimaSts'])
        self.partner.ck_no_event(self.partner_key, "ClimateSystemStatus", timeout=0.2)

    @allure.title("ClimateControlService::CockpitVentStatus_BodyCAN::0x243同帧非相关信号跳变无异常event")
    def test_caseid_1986431(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=579, no_opera_signal=['RemVentReqRspnFb', 'RemVentActvSts', 'RemVentWarnSts'])
        self.partner.ck_no_event(self.partner_key, "CockpitVentStatus", timeout=0.2)

    @allure.title("ClimateControlService::coolantLowWarnInfo_ChassisCAN1::0x46F同帧非相关信号跳变无异常event")
    def test_caseid_1986449(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=1135, no_opera_signal=['BattCooltIndcnReq'])
        self.partner.ck_no_event(self.partner_key, "coolantLowWarnInfo", timeout=0.2)

    @allure.title("ClimateControlService::coolantLowWarnInfo_ChassisCAN2::0x200同帧非相关信号跳变无异常event")
    def test_caseid_1986450(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=512, no_opera_signal=['EmotCooltIndcnReq'])
        self.partner.ck_no_event(self.partner_key, "coolantLowWarnInfo", timeout=0.2)

    @allure.title("ClimateControlService::NotifyACDefrostSts_BodyCAN::0x127同帧非相关信号跳变无异常event")
    def test_caseid_1986432(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=295, no_opera_signal=['RemClimaDefrstSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyACDefrostSts", timeout=0.2)

    @allure.title("ClimateControlService::NotifyAmbientTempRawData_BodyCAN::0x490同帧非相关信号跳变无异常event")
    def test_caseid_1986448(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1168, no_opera_signal=['AmbTEstimdAmbTEstimd', 'AmbTEstimdQf'])
        self.partner.ck_no_event(self.partner_key, "NotifyAmbientTempRawData", timeout=0.2)

    @allure.title("ClimateControlService::NotifyClimateCoolingHeatingStatus_BodyCAN::0x405同帧非相关信号跳变无异常event")
    def test_caseid_1986435(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1029, no_opera_signal=['ClimaCmptSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyClimateCoolingHeatingStatus", timeout=0.2)

    @allure.title("ClimateControlService::NotifyClimateECOSts_BodyCAN::0x127同帧非相关信号跳变无异常event")
    def test_caseid_1986451(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=295, no_opera_signal=['EcoClimaSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyClimateECOSts", timeout=0.2)

    @allure.title("ClimateControlService::PM25_BodyCAN::0x025同帧非相关信号跳变无异常event")
    def test_caseid_1986443(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=37, no_opera_signal=['IntPm25VluFrmClima'])
        self.partner.ck_no_event(self.partner_key, "PM25", timeout=0.2)

    @allure.title("ClimateControlService::PM25_BodyCAN::0x0B1同帧非相关信号跳变无异常event")
    def test_caseid_1986444(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=177, no_opera_signal=['IntPm25LvlFrmClima'])
        self.partner.ck_no_event(self.partner_key, "PM25", timeout=0.2)

    @allure.title("ClimateControlService::PM25_BodyCAN::0x419同帧非相关信号跳变无异常event")
    def test_caseid_1986445(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1049, no_opera_signal=['IntPm25StsFrmClima'])
        self.partner.ck_no_event(self.partner_key, "PM25", timeout=0.2)

    @allure.title("ClimateControlService::PM25_BodyCAN::0x4A0同帧非相关信号跳变无异常event")
    def test_caseid_1986442(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1184, no_opera_signal=['IntPm25HiPopUp'])
        self.partner.ck_no_event(self.partner_key, "PM25", timeout=0.2)

    @allure.title("ClimateControlService::RemoteClimateHVDelayStatus_BodyCAN::0x410同帧非相关信号跳变无异常event")
    def test_caseid_1986437(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1040, no_opera_signal=['RemClimaDelaySts'])
        self.partner.ck_no_event(self.partner_key, "RemoteClimateHVDelayStatus", timeout=0.2)

    @allure.title("ClimateControlService::RemoteClimateHVStatus_BodyCAN::0x410同帧非相关信号跳变无异常event")
    def test_caseid_1986439(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1040, no_opera_signal=['RemClimaHvSts'])
        self.partner.ck_no_event(self.partner_key, "RemoteClimateHVStatus", timeout=0.2)

    @allure.title("ClimateControlService::RemoteClimateSwitchToHVDelayReceiveFeedback_BodyCAN::0x410同帧非相关信号跳变无异常event")
    def test_caseid_1986436(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1040, no_opera_signal=['RemClimaExtnTiRspn'])
        self.partner.ck_no_event(self.partner_key, "RemoteClimateSwitchToHVDelayReceiveFeedback", timeout=0.2)

    @allure.title("ClimateControlService::RemoteClimateSwitchToHVReceiveFeedback_BodyCAN::0x410同帧非相关信号跳变无异常event")
    def test_caseid_1986438(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1040, no_opera_signal=['RemClimaHvRspn'])
        self.partner.ck_no_event(self.partner_key, "RemoteClimateSwitchToHVReceiveFeedback", timeout=0.2)

    @allure.title("ClimateControlService::RemoteOn_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1987164(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "RemoteOn", timeout=0.2)

    @allure.title("ClimateControlService::RemoteOn_BodyCAN::0x200同帧非相关信号跳变无异常event")
    def test_caseid_1987163(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=512, no_opera_signal=['RemClimaActv'])
        self.partner.ck_no_event(self.partner_key, "RemoteOn", timeout=0.2)

    @allure.title("ClimateControlService::RemoteOnOffReceiveFeedback_BodyCAN::0x251同帧非相关信号跳变无异常event")
    def test_caseid_1986440(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=593, no_opera_signal=['RemStrtClimaRspn'])
        self.partner.ck_no_event(self.partner_key, "RemoteOnOffReceiveFeedback", timeout=0.2)

    @allure.title("ClimateControlService::RemotePowerStatus_BodyCAN::0x200同帧非相关信号跳变无异常event")
    def test_caseid_1986441(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=512, no_opera_signal=['RemClimaActv'])
        self.partner.ck_no_event(self.partner_key, "RemotePowerStatus", timeout=0.2)

    @allure.title("ClimateControlService::Temperature_BodyCAN::0x121同帧非相关信号跳变无异常event")
    def test_caseid_1986447(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=289, no_opera_signal=['CmptmtTFrntCmptmtTFrnt', 'CmptmtTFrntQf'])
        self.partner.ck_no_event(self.partner_key, "Temperature", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestCTDServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("CTDService", 'client')])
        self.partner_key = "CTDService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("CTDService::alarmInfo_BackboneFR::38-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986461(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2492480, no_opera_signal=['AlrmStsAlrmFailr', 'AlrmStsAlrmSt', 'AlrmStsAlrmTrgSrc', 'AlrmStsSnsrInclnFailr', 'AlrmStsSnsrIntrScanrFailr'])
        self.partner.ck_no_event(self.partner_key, "alarmInfo", timeout=0.2)

    @allure.title("CTDService::theftDectEnableSts_BackboneFR::38-32-64同帧非相关信号跳变无异常event")
    def test_caseid_1986462(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2498624, no_opera_signal=['PasAlrmSts'])
        self.partner.ck_no_event(self.partner_key, "theftDectEnableSts", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestDoorServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("DoorService", 'client')])
        self.partner_key = "DoorService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("DoorService::DoorActionRequest_BodyCAN::0x0B4同帧非相关信号跳变无异常event")
    def test_caseid_1986405(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=180, no_opera_signal=['DoorOpenerDrvrReqDoorOpenerReq2', 'DoorOpenerLeReReqDoorOpenerReq2', 'DoorOpenerDrvrReqTrigSrc', 'DoorOpenerLeReReqTrigSrc'])
        self.partner.ck_no_event(self.partner_key, "DoorActionRequest", timeout=0.2)

    @allure.title("DoorService::DoorActionRequest_BodyCAN::0x0B8同帧非相关信号跳变无异常event")
    def test_caseid_1986404(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=184, no_opera_signal=['DoorOpenerPassReqDoorOpenerReq2', 'DoorOpenerRiReReqDoorOpenerReq2', 'DoorOpenerPassReqTrigSrc', 'DoorOpenerRiReReqTrigSrc'])
        self.partner.ck_no_event(self.partner_key, "DoorActionRequest", timeout=0.2)

    @allure.title("DoorService::DoorFault_BodyCAN::0x005同帧非相关信号跳变无异常event")
    def test_caseid_1986425(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=5, no_opera_signal=['ChdPrtnLeftFailStsToHmi'])
        self.partner.ck_no_event(self.partner_key, "DoorFault", timeout=0.2)

    @allure.title("DoorService::DoorFault_BodyCAN::0x1E0同帧非相关信号跳变无异常event")
    def test_caseid_1986424(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=480, no_opera_signal=['ChdLockRightFailStsToHmi'])
        self.partner.ck_no_event(self.partner_key, "DoorFault", timeout=0.2)

    @allure.title("DoorService::DoorFault_BodyCAN::0x217同帧非相关信号跳变无异常event")
    def test_caseid_1986429(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=535, no_opera_signal=['DtcInfDoorDrvrBoolean1', 'DtcInfDoorDrvrBoolean10', 'DtcInfDoorDrvrBoolean11', 'DtcInfDoorDrvrBoolean12', 'DtcInfDoorDrvrBoolean13', 'DtcInfDoorDrvrBoolean14', 'DtcInfDoorDrvrBoolean2', 'DtcInfDoorDrvrBoolean3', 'DtcInfDoorDrvrBoolean4', 'DtcInfDoorDrvrBoolean5', 'DtcInfDoorDrvrBoolean6', 'DtcInfDoorDrvrBoolean7', 'DtcInfDoorDrvrBoolean8', 'DtcInfDoorDrvrBoolean9'])
        self.partner.ck_no_event(self.partner_key, "DoorFault", timeout=0.2)

    @allure.title("DoorService::DoorFault_BodyCAN::0x218同帧非相关信号跳变无异常event")
    def test_caseid_1986426(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=536, no_opera_signal=['DtcInfDoorLeReBoolean1', 'DtcInfDoorLeReBoolean10', 'DtcInfDoorLeReBoolean11', 'DtcInfDoorLeReBoolean12', 'DtcInfDoorLeReBoolean13', 'DtcInfDoorLeReBoolean14', 'DtcInfDoorLeReBoolean2', 'DtcInfDoorLeReBoolean3', 'DtcInfDoorLeReBoolean4', 'DtcInfDoorLeReBoolean5', 'DtcInfDoorLeReBoolean6', 'DtcInfDoorLeReBoolean7', 'DtcInfDoorLeReBoolean8', 'DtcInfDoorLeReBoolean9'])
        self.partner.ck_no_event(self.partner_key, "DoorFault", timeout=0.2)

    @allure.title("DoorService::DoorFault_BodyCAN::0x222同帧非相关信号跳变无异常event")
    def test_caseid_1986428(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=546, no_opera_signal=['DtcInfDoorPassBoolean1', 'DtcInfDoorPassBoolean10', 'DtcInfDoorPassBoolean11', 'DtcInfDoorPassBoolean12', 'DtcInfDoorPassBoolean13', 'DtcInfDoorPassBoolean14', 'DtcInfDoorPassBoolean2', 'DtcInfDoorPassBoolean3', 'DtcInfDoorPassBoolean4', 'DtcInfDoorPassBoolean5', 'DtcInfDoorPassBoolean6', 'DtcInfDoorPassBoolean7', 'DtcInfDoorPassBoolean8', 'DtcInfDoorPassBoolean9'])
        self.partner.ck_no_event(self.partner_key, "DoorFault", timeout=0.2)

    @allure.title("DoorService::DoorFault_BodyCAN::0x22A同帧非相关信号跳变无异常event")
    def test_caseid_1986427(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=554, no_opera_signal=['DtcInfDoorRiReBoolean1', 'DtcInfDoorRiReBoolean10', 'DtcInfDoorRiReBoolean11', 'DtcInfDoorRiReBoolean12', 'DtcInfDoorRiReBoolean13', 'DtcInfDoorRiReBoolean14', 'DtcInfDoorRiReBoolean2', 'DtcInfDoorRiReBoolean3', 'DtcInfDoorRiReBoolean4', 'DtcInfDoorRiReBoolean5', 'DtcInfDoorRiReBoolean6', 'DtcInfDoorRiReBoolean7', 'DtcInfDoorRiReBoolean8', 'DtcInfDoorRiReBoolean9'])
        self.partner.ck_no_event(self.partner_key, "DoorFault", timeout=0.2)

    @allure.title("DoorService::DoorIceBreakActiveStatus_BodyCAN::0x010同帧非相关信号跳变无异常event")
    def test_caseid_1986412(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=16, no_opera_signal=['IceBreakDoorPassActv'])
        self.partner.ck_no_event(self.partner_key, "DoorIceBreakActiveStatus", timeout=0.2)

    @allure.title("DoorService::DoorIceBreakActiveStatus_BodyCAN::0x0C0同帧非相关信号跳变无异常event")
    def test_caseid_1986413(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=192, no_opera_signal=['IceBreakDoorDrvrActv'])
        self.partner.ck_no_event(self.partner_key, "DoorIceBreakActiveStatus", timeout=0.2)

    @allure.title("DoorService::DoorIceBreakActiveStatus_BodyCAN::0x203同帧非相关信号跳变无异常event")
    def test_caseid_1986411(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=515, no_opera_signal=['IceBreakDoorLeReActv'])
        self.partner.ck_no_event(self.partner_key, "DoorIceBreakActiveStatus", timeout=0.2)

    @allure.title("DoorService::DoorIceBreakActiveStatus_BodyCAN::0x204同帧非相关信号跳变无异常event")
    def test_caseid_1986410(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=516, no_opera_signal=['IceBreakDoorRiReActv'])
        self.partner.ck_no_event(self.partner_key, "DoorIceBreakActiveStatus", timeout=0.2)

    @allure.title("DoorService::DoorObstacleInfo_ConnectivityCANFD::0x0F0同帧非相关信号跳变无异常event")
    def test_caseid_1986409(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=240, no_opera_signal=['DoorDrvrPosnToObstAngle1'])
        self.partner.ck_no_event(self.partner_key, "DoorObstacleInfo", timeout=0.2)

    @allure.title("DoorService::DoorObstacleInfo_ConnectivityCANFD::0x0F1同帧非相关信号跳变无异常event")
    def test_caseid_1986408(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=241, no_opera_signal=['DoorPassPosnToObstAngle1'])
        self.partner.ck_no_event(self.partner_key, "DoorObstacleInfo", timeout=0.2)

    @allure.title("DoorService::DoorObstacleInfo_ConnectivityCANFD::0x0F2同帧非相关信号跳变无异常event")
    def test_caseid_1986407(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=242, no_opera_signal=['DoorLeRePosnToObstAngle1'])
        self.partner.ck_no_event(self.partner_key, "DoorObstacleInfo", timeout=0.2)

    @allure.title("DoorService::DoorObstacleInfo_ConnectivityCANFD::0x0F3同帧非相关信号跳变无异常event")
    def test_caseid_1986406(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=243, no_opera_signal=['DoorRiRePosnToObstAngle1'])
        self.partner.ck_no_event(self.partner_key, "DoorObstacleInfo", timeout=0.2)

    @allure.title("DoorService::DoorRadarWorkMode_ConnectivityCANFD::0x1F5同帧非相关信号跳变无异常event")
    def test_caseid_1986418(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=501, no_opera_signal=['FLDRMWorkModeFB'])
        self.partner.ck_no_event(self.partner_key, "DoorRadarWorkMode", timeout=0.2)

    @allure.title("DoorService::DoorRadarWorkMode_ConnectivityCANFD::0x1FC同帧非相关信号跳变无异常event")
    def test_caseid_1986417(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=508, no_opera_signal=['FRDRMWorkModeFB'])
        self.partner.ck_no_event(self.partner_key, "DoorRadarWorkMode", timeout=0.2)

    @allure.title("DoorService::DoorRadarWorkMode_ConnectivityCANFD::0x203同帧非相关信号跳变无异常event")
    def test_caseid_1986416(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=515, no_opera_signal=['RLDRMWorkModeFB'])
        self.partner.ck_no_event(self.partner_key, "DoorRadarWorkMode", timeout=0.2)

    @allure.title("DoorService::DoorRadarWorkMode_ConnectivityCANFD::0x209同帧非相关信号跳变无异常event")
    def test_caseid_1986415(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=521, no_opera_signal=['RRDRMWorkModeFB'])
        self.partner.ck_no_event(self.partner_key, "DoorRadarWorkMode", timeout=0.2)

    @allure.title("DoorService::FrntLeftDoorPosition_BodyCAN::0x217同帧非相关信号跳变无异常event")
    def test_caseid_1986393(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=535, no_opera_signal=['DoorDrvrPercPosn', 'DoorDrvrPosn', 'DoorDrvrMInAngleFb', 'TopPercDrvrHmiFeedBack'])
        self.partner.ck_no_event(self.partner_key, "FrntLeftDoorPosition", timeout=0.2)

    @allure.title("DoorService::FrntLeftDoorSts_BodyCAN::0x040同帧非相关信号跳变无异常event")
    def test_caseid_1986401(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=64, no_opera_signal=['DoorDrvrSts'])
        self.partner.ck_no_event(self.partner_key, "FrntLeftDoorSts", timeout=0.2)

    @allure.title("DoorService::FrntLeftDoorSts_BodyCAN::0x217同帧非相关信号跳变无异常event")
    def test_caseid_1986400(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=535, no_opera_signal=['DoorOpenerDrvrSts', 'DoorDrvrAntiPnch'])
        self.partner.ck_no_event(self.partner_key, "FrntLeftDoorSts", timeout=0.2)

    @allure.title("DoorService::FrntRightDoorPosition_BodyCAN::0x222同帧非相关信号跳变无异常event")
    def test_caseid_1986392(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=546, no_opera_signal=['DoorPassPercPosn', 'DoorPassPosn', 'DoorPassMInAngleFb', 'TopPercPassHmiFeedBack'])
        self.partner.ck_no_event(self.partner_key, "FrntRightDoorPosition", timeout=0.2)

    @allure.title("DoorService::FrntRightDoorSts_BodyCAN::0x0E0同帧非相关信号跳变无异常event")
    def test_caseid_1986399(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=224, no_opera_signal=['DoorPassSts'])
        self.partner.ck_no_event(self.partner_key, "FrntRightDoorSts", timeout=0.2)

    @allure.title("DoorService::FrntRightDoorSts_BodyCAN::0x222同帧非相关信号跳变无异常event")
    def test_caseid_1986398(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=546, no_opera_signal=['DoorOpenerPassSts', 'DoorPassAntiPnch'])
        self.partner.ck_no_event(self.partner_key, "FrntRightDoorSts", timeout=0.2)

    @allure.title("DoorService::NotifyDoorRadarSts_ConnectivityCANFD::0x0F0同帧非相关信号跳变无异常event")
    def test_caseid_1986422(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=240, no_opera_signal=['RadarDrvrSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyDoorRadarSts", timeout=0.2)

    @allure.title("DoorService::NotifyDoorRadarSts_ConnectivityCANFD::0x0F1同帧非相关信号跳变无异常event")
    def test_caseid_1986421(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=241, no_opera_signal=['RadarPassSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyDoorRadarSts", timeout=0.2)

    @allure.title("DoorService::NotifyDoorRadarSts_ConnectivityCANFD::0x0F2同帧非相关信号跳变无异常event")
    def test_caseid_1986420(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=242, no_opera_signal=['RadarLeReSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyDoorRadarSts", timeout=0.2)

    @allure.title("DoorService::NotifyDoorRadarSts_ConnectivityCANFD::0x0F3同帧非相关信号跳变无异常event")
    def test_caseid_1986419(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=243, no_opera_signal=['RadarRiReSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyDoorRadarSts", timeout=0.2)

    @allure.title("DoorService::NotifyDoorSwitchSts_BackboneFR::40-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986423(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2621456, no_opera_signal=['DoorDrvrOpenReqInsdLogic', 'DoorPassOpenReqInsdLogic', 'DoorLeReOpenReqInsdLogic', 'DoorRiReOpenReqInsdLogic', 'DoorDrvrOpenReqOutdLogic', 'DoorPassOpenReqOutdLogic', 'DoorLeReOpenReqOutdLogic', 'DoorRiReOpenReqOutdLogic'])
        self.partner.ck_no_event(self.partner_key, "NotifyDoorSwitchSts", timeout=0.2)

    @allure.title("DoorService::NotifyOutDoorSwitchLightSts_InfoCANFD::0x201同帧非相关信号跳变无异常event")
    def test_caseid_1986414(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=513, no_opera_signal=['StatusOfOuterDoorSwLightDrvrSwLight', 'StatusOfOuterDoorSwLightPassSwLight', 'StatusOfOuterDoorSwLightLeReSwLight', 'StatusOfOuterDoorSwLightRiReSwLight'])
        self.partner.ck_no_event(self.partner_key, "NotifyOutDoorSwitchLightSts", timeout=0.2)

    @allure.title("DoorService::OpenWarning_BackboneFR::39-0-8同帧非相关信号跳变无异常event")
    def test_caseid_1986430(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2555912, no_opera_signal=['DoorOpenInteWarn'])
        self.partner.ck_no_event(self.partner_key, "OpenWarning", timeout=0.2)

    @allure.title("DoorService::RearLeftChildLock_BodyCAN::0x005同帧非相关信号跳变无异常event")
    def test_caseid_1986403(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=5, no_opera_signal=['ChdPrtnLeftStsToHmi'])
        self.partner.ck_no_event(self.partner_key, "RearLeftChildLock", timeout=0.2)

    @allure.title("DoorService::RearLeftDoorPosition_BodyCAN::0x218同帧非相关信号跳变无异常event")
    def test_caseid_1986391(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=536, no_opera_signal=['DoorLeRePercPosn', 'DoorLeRePosn', 'DoorLeReMInAngleFb', 'TopPercLeReHmiFeedBack'])
        self.partner.ck_no_event(self.partner_key, "RearLeftDoorPosition", timeout=0.2)

    @allure.title("DoorService::RearLeftDoorSts_BodyCAN::0x040同帧非相关信号跳变无异常event")
    def test_caseid_1986397(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=64, no_opera_signal=['DoorLeReSts'])
        self.partner.ck_no_event(self.partner_key, "RearLeftDoorSts", timeout=0.2)

    @allure.title("DoorService::RearLeftDoorSts_BodyCAN::0x218同帧非相关信号跳变无异常event")
    def test_caseid_1986396(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=536, no_opera_signal=['DoorOpenerLeReSts', 'DoorLeReAntiPnch'])
        self.partner.ck_no_event(self.partner_key, "RearLeftDoorSts", timeout=0.2)

    @allure.title("DoorService::RearRightChildLock_BodyCAN::0x030同帧非相关信号跳变无异常event")
    def test_caseid_1986402(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=48, no_opera_signal=['ChdLockRightStsToHmi'])
        self.partner.ck_no_event(self.partner_key, "RearRightChildLock", timeout=0.2)

    @allure.title("DoorService::RearRightDoorPosition_BodyCAN::0x22A同帧非相关信号跳变无异常event")
    def test_caseid_1986390(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=554, no_opera_signal=['DoorRiRePercPosn', 'DoorRiRePosn', 'DoorRiReMInAngleFb', 'TopPercRiReHmiFeedBack'])
        self.partner.ck_no_event(self.partner_key, "RearRightDoorPosition", timeout=0.2)

    @allure.title("DoorService::RearRightDoorSts_BodyCAN::0x0E0同帧非相关信号跳变无异常event")
    def test_caseid_1986395(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=224, no_opera_signal=['DoorRiReSts'])
        self.partner.ck_no_event(self.partner_key, "RearRightDoorSts", timeout=0.2)

    @allure.title("DoorService::RearRightDoorSts_BodyCAN::0x22A同帧非相关信号跳变无异常event")
    def test_caseid_1986394(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=554, no_opera_signal=['DoorOpenerRiReSts', 'DoorRiReAntiPnch'])
        self.partner.ck_no_event(self.partner_key, "RearRightDoorSts", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestDrivingAssistServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("DrivingAssistService", 'client')])
        self.partner_key = "DrivingAssistService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("DrivingAssistService::handOFFSts_CEM_LIN4::0x18同帧非相关信号跳变无异常event")
    def test_caseid_1986480(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin4", message=24, no_opera_signal=['HandsOnDetectionHandsOnStatus', 'HandsOnDetectionErrorStatus'])
        self.partner.ck_no_event(self.partner_key, "handOFFSts", timeout=0.2)

    @allure.title("DrivingAssistService::NotifyTraveledDistance_BackboneFR::39-4-8同帧非相关信号跳变无异常event")
    def test_caseid_1986479(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556936, no_opera_signal=['TotDstTrvldHiResl'])
        self.partner.ck_no_event(self.partner_key, "NotifyTraveledDistance", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestETCServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("ETCService", 'client')])
        self.partner_key = "ETCService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("ETCService::ETCMFaultEnum_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986463(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "ETCMFaultEnum", timeout=0.2)

    @allure.title("ETCService::ETCMFaultEnum_BodyCAN::0x245同帧非相关信号跳变无异常event")
    def test_caseid_1986464(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=581, no_opera_signal=['ETCSelfChkSts'])
        self.partner.ck_no_event(self.partner_key, "ETCMFaultEnum", timeout=0.2)

    @allure.title("ETCService::NotifyETCStatus_BodyCAN::0x245同帧非相关信号跳变无异常event")
    def test_caseid_1986467(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=581, no_opera_signal=['ETCSelfChkSts', 'ETCOpenSts', 'ETCMWorkSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyETCStatus", timeout=0.2)

    @allure.title("ETCService::NotifyETCTradeRes_BodyCAN::0x236同帧非相关信号跳变无异常event")
    def test_caseid_1986466(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=566, no_opera_signal=['ETCGatePpty', 'ETCSysSts', 'ETCTradeInfo'])
        self.partner.ck_no_event(self.partner_key, "NotifyETCTradeRes", timeout=0.2)

    @allure.title("ETCService::NotifyETCUsableSts_BodyCAN::0x236同帧非相关信号跳变无异常event")
    def test_caseid_1986465(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=566, no_opera_signal=['ETCGatePpty', 'ETCSysSts', 'ETCTradeInfo'])
        self.partner.ck_no_event(self.partner_key, "NotifyETCUsableSts", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestGloveBoxServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("GloveBoxService", 'client')])
        self.partner_key = "GloveBoxService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("GloveBoxService::GloveBoxStatus_BackboneFR::39-2-8同帧非相关信号跳变无异常event")
    def test_caseid_1986389(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556424, no_opera_signal=['LockgPrsnlSts', 'RmnLockgPrsnlReq'])
        self.partner.ck_no_event(self.partner_key, "GloveBoxStatus", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestHighVoltageServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("HighVoltageService", 'client')])
        self.partner_key = "HighVoltageService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("HighVoltageService::AxleTorqueDistribution_ChassisCAN1::0x1C7同帧非相关信号跳变无异常event")
    def test_caseid_1986501(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=455, no_opera_signal=['ActAxleTqDistbn'])
        self.partner.ck_no_event(self.partner_key, "AxleTorqueDistribution", timeout=0.2)

    @allure.title("HighVoltageService::BatteryHeatingInfo_PropulsionCAN::0x175同帧非相关信号跳变无异常event")
    def test_caseid_1986498(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=373, no_opera_signal=['HvBattThermTiEstimd'])
        self.partner.ck_no_event(self.partner_key, "BatteryHeatingInfo", timeout=0.2)

    @allure.title("HighVoltageService::BatteryHeatingInfo_PropulsionCAN::0x188同帧非相关信号跳变无异常event")
    def test_caseid_1986500(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=392, no_opera_signal=['HvBattThermReqFb'])
        self.partner.ck_no_event(self.partner_key, "BatteryHeatingInfo", timeout=0.2)

    @allure.title("HighVoltageService::BatteryHeatingInfo_PropulsionCAN::0x290同帧非相关信号跳变无异常event")
    def test_caseid_1986499(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=656, no_opera_signal=['LocalHvBattThermReqFb'])
        self.partner.ck_no_event(self.partner_key, "BatteryHeatingInfo", timeout=0.2)

    @allure.title("HighVoltageService::BatteryTemperatureInfo_PropulsionCAN::0x315同帧非相关信号跳变无异常event")
    def test_caseid_1986502(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=789, no_opera_signal=['HvBattTMin', 'HvBattTMax', 'HvBattTAvg'])
        self.partner.ck_no_event(self.partner_key, "BatteryTemperatureInfo", timeout=0.2)

    @allure.title("HighVoltageService::BatteryTemperatureLowState_BackboneFR::49-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986508(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3211280, no_opera_signal=['HvBattCellTInfoHvBattTMin'])
        self.partner.ck_no_event(self.partner_key, "BatteryTemperatureLowState", timeout=0.2)

    @allure.title("HighVoltageService::BattMaintReqSts_PropulsionCAN::0x175同帧非相关信号跳变无异常event")
    def test_caseid_1986497(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=373, no_opera_signal=['MaintainBattTReq'])
        self.partner.ck_no_event(self.partner_key, "BattMaintReqSts", timeout=0.2)

    @allure.title("HighVoltageService::BookChargingTime_PropulsionCAN::0x3F0同帧非相关信号跳变无异常event")
    def test_caseid_1986504(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=1008, no_opera_signal=['LocalBookStrtTiChrgnTmrChrgnTmrhour', 'LocalBookStrtTiChrgnTmrChrgnTmrmin', 'LocalBookStopTiChrgnTmrChrgnTmrhour', 'LocalBookStopTiChrgnTmrChrgnTmrmin'])
        self.partner.ck_no_event(self.partner_key, "BookChargingTime", timeout=0.2)

    @allure.title("HighVoltageService::BookChargingTime_PropulsionCAN::0x401同帧非相关信号跳变无异常event")
    def test_caseid_1986505(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=1025, no_opera_signal=['BthBookStrtTiChrgnTmrChrgnTmrhour', 'BthBookStrtTiChrgnTmrChrgnTmrmin', 'BthBookStopTiChrgnTmrChrgnTmrhour', 'BthBookStopTiChrgnTmrChrgnTmrmin'])
        self.partner.ck_no_event(self.partner_key, "BookChargingTime", timeout=0.2)

    @allure.title("HighVoltageService::BookChargingTime_PropulsionCAN::0x402同帧非相关信号跳变无异常event")
    def test_caseid_1986506(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=1026, no_opera_signal=['RemoteBookStrtTiChrgnTmrChrgnTmrhour', 'RemoteBookStrtTiChrgnTmrChrgnTmrmin', 'RemoteBookStopTiChrgnTmrChrgnTmrhour', 'RemoteBookStopTiChrgnTmrChrgnTmrmin'])
        self.partner.ck_no_event(self.partner_key, "BookChargingTime", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_BackboneFR::48-6-8同帧非相关信号跳变无异常event")
    def test_caseid_1986521(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3147272, no_opera_signal=['ChrgnOrDisChrgnStsFb'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_ChassisCAN1::0x278同帧非相关信号跳变无异常event")
    def test_caseid_1986523(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=632, no_opera_signal=['ChrgnSpd'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_ChassisCAN1::0x367同帧非相关信号跳变无异常event")
    def test_caseid_1986516(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=871, no_opera_signal=['BookChrgnTarValFb'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_ChassisCAN2::0x211同帧非相关信号跳变无异常event")
    def test_caseid_1986517(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=529, no_opera_signal=['BookChrgnStsFb'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x143同帧非相关信号跳变无异常event")
    def test_caseid_1986522(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=323, no_opera_signal=['DCChrgnHndlSts'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x178同帧非相关信号跳变无异常event")
    def test_caseid_1986513(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=376, no_opera_signal=['HvBattChrgnCmpl'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x287同帧非相关信号跳变无异常event")
    def test_caseid_1986518(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=647, no_opera_signal=['BookChargeSetResponse'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x288同帧非相关信号跳变无异常event")
    def test_caseid_1986520(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=648, no_opera_signal=['HvBattChrgnTiEstimd'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x298同帧非相关信号跳变无异常event")
    def test_caseid_1986515(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=664, no_opera_signal=['HvBattChrgnPwrCns1', 'HvBattEgyAvlChrg1'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986511(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=769, no_opera_signal=['HvBattChrgnPwrCns800'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x331同帧非相关信号跳变无异常event")
    def test_caseid_1986519(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=817, no_opera_signal=['DCChrgnPosPortT', 'DCChrgnNegPortT'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x341同帧非相关信号跳变无异常event")
    def test_caseid_1986514(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=833, no_opera_signal=['TotChrgEgy'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::ChargingInfo_PropulsionCAN::0x401同帧非相关信号跳变无异常event")
    def test_caseid_1986512(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=1025, no_opera_signal=['ChrgPilBookChrgn'])
        self.partner.ck_no_event(self.partner_key, "ChargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::DischargingInfo_PropulsionCAN::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986491(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=769, no_opera_signal=['HvBattChrgnPwrCns800'])
        self.partner.ck_no_event(self.partner_key, "DischargingInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_ChassisCAN1::0x340同帧非相关信号跳变无异常event")
    def test_caseid_1986288(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=832, no_opera_signal=['HvCabinThermPwrCns'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_ChassisCAN1::0x3DF同帧非相关信号跳变无异常event")
    def test_caseid_1986289(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=991, no_opera_signal=['HvBattThermPwrCns'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_ChassisCAN2::0x370同帧非相关信号跳变无异常event")
    def test_caseid_1986290(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=880, no_opera_signal=['DispBattEgyIn', 'DispBattEgyOut'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_PropulsionCAN::0x04B同帧非相关信号跳变无异常event")
    def test_caseid_1986287(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=75, no_opera_signal=['EngSt1WdStsEngSt1WdSts'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_PropulsionCAN::0x060同帧非相关信号跳变无异常event")
    def test_caseid_1986284(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=96, no_opera_signal=['WhlMotSysUdc'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_PropulsionCAN::0x063同帧非相关信号跳变无异常event")
    def test_caseid_1986283(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=99, no_opera_signal=['WhlMotSysIdc', 'WhlMotSysUDc800'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_PropulsionCAN::0x13A同帧非相关信号跳变无异常event")
    def test_caseid_1986286(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=314, no_opera_signal=['IsgIDc'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyConsumptionInfo_PropulsionCAN::0x156同帧非相关信号跳变无异常event")
    def test_caseid_1986285(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=342, no_opera_signal=['IsgUDc', 'IsgUDc800'])
        self.partner.ck_no_event(self.partner_key, "EnergyConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::EnergyRecoveryLevel_BackboneFR::49-4-16同帧非相关信号跳变无异常event")
    def test_caseid_1986509(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3212304, no_opera_signal=['EgyRgnLvlAct'])
        self.partner.ck_no_event(self.partner_key, "EnergyRecoveryLevel", timeout=0.2)

    @allure.title("HighVoltageService::EnergyRecoveryState_ChassisCAN2::0x233同帧非相关信号跳变无异常event")
    def test_caseid_1986507(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=563, no_opera_signal=['DrvPfmncRedn'])
        self.partner.ck_no_event(self.partner_key, "EnergyRecoveryState", timeout=0.2)

    @allure.title("HighVoltageService::FullChargingRemind_PropulsionCAN::0x178同帧非相关信号跳变无异常event")
    def test_caseid_1986291(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=376, no_opera_signal=['HvBattChrgnCmpl'])
        self.partner.ck_no_event(self.partner_key, "FullChargingRemind", timeout=0.2)

    @allure.title("HighVoltageService::HeatingPrioritySts_PropulsionCAN::0x27C同帧非相关信号跳变无异常event")
    def test_caseid_1986292(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=636, no_opera_signal=['HvBattClimaPrioReq'])
        self.partner.ck_no_event(self.partner_key, "HeatingPrioritySts", timeout=0.2)

    @allure.title("HighVoltageService::HighVoltageFault_BackboneFR::49-13-32同帧非相关信号跳变无异常event")
    def test_caseid_1986528(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3214624, no_opera_signal=['TelltlPwrLoss'])
        self.partner.ck_no_event(self.partner_key, "HighVoltageFault", timeout=0.2)

    @allure.title("HighVoltageService::HighVoltageFault_ChassisCAN2::0x3B0同帧非相关信号跳变无异常event")
    def test_caseid_1986529(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=944, no_opera_signal=['HybErrIndcnReqTelltlSysHybFailr'])
        self.partner.ck_no_event(self.partner_key, "HighVoltageFault", timeout=0.2)

    @allure.title("HighVoltageService::hvActiveSts_PropulsionCAN::0x141同帧非相关信号跳变无异常event")
    def test_caseid_1986547(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=321, no_opera_signal=['HvSysRlyStsHvSysRlySts'])
        self.partner.ck_no_event(self.partner_key, "hvActiveSts", timeout=0.2)

    @allure.title("HighVoltageService::HVBatteryCurrent_PropulsionCAN::0x143同帧非相关信号跳变无异常event")
    def test_caseid_1986525(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=323, no_opera_signal=['HvBattIDc1'])
        self.partner.ck_no_event(self.partner_key, "HVBatteryCurrent", timeout=0.2)

    @allure.title("HighVoltageService::HVBatteryFault_ChassisCAN2::0x3B0同帧非相关信号跳变无异常event")
    def test_caseid_1986533(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=944, no_opera_signal=['HybErrIndcnReqTelltlBattTracCutOff', 'HybErrIndcnReqTelltlBattTracFailr'])
        self.partner.ck_no_event(self.partner_key, "HVBatteryFault", timeout=0.2)

    @allure.title("HighVoltageService::HVBatteryFaultValidity_ChassisCAN2::0x3B0同帧非相关信号跳变无异常event")
    def test_caseid_1986496(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=944, no_opera_signal=['HybErrIndcnReqTelltlBattTracFailr', 'HybErrIndcnReqTelltlBattTracCutOff'])
        self.partner.ck_no_event(self.partner_key, "HVBatteryFaultValidity", timeout=0.2)

    @allure.title("HighVoltageService::HVBatterySOH_PropulsionCAN::0x293同帧非相关信号跳变无异常event")
    def test_caseid_1986510(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=659, no_opera_signal=['HvBattEgyCdn'])
        self.partner.ck_no_event(self.partner_key, "HVBatterySOH", timeout=0.2)

    @allure.title("HighVoltageService::HVBatteryVoltage_PropulsionCAN::0x141同帧非相关信号跳变无异常event")
    def test_caseid_1986526(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=321, no_opera_signal=['HvBattUDc', 'HvBattUDc800'])
        self.partner.ck_no_event(self.partner_key, "HVBatteryVoltage", timeout=0.2)

    @allure.title("HighVoltageService::HVCrash_PropulsionCAN::0x035同帧非相关信号跳变无异常event")
    def test_caseid_1986574(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=53, no_opera_signal=['CrashStsSafeSts'])
        self.partner.ck_no_event(self.partner_key, "HVCrash", timeout=0.2)

    @allure.title("HighVoltageService::HVInsulationFault_PropulsionCAN::0x342同帧非相关信号跳变无异常event")
    def test_caseid_1986555(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=834, no_opera_signal=['HvIsoFlt'])
        self.partner.ck_no_event(self.partner_key, "HVInsulationFault", timeout=0.2)

    @allure.title("HighVoltageService::hvInterLockInfo_PropulsionCAN::0x295同帧非相关信号跳变无异常event")
    def test_caseid_1986540(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=661, no_opera_signal=['HVIL1Sts', 'HVIL2Sts', 'HVIL3Sts'])
        self.partner.ck_no_event(self.partner_key, "hvInterLockInfo", timeout=0.2)

    @allure.title("HighVoltageService::hvInterLockInfo_PropulsionCAN::0x342同帧非相关信号跳变无异常event")
    def test_caseid_1986541(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=834, no_opera_signal=['HvilFlt'])
        self.partner.ck_no_event(self.partner_key, "hvInterLockInfo", timeout=0.2)

    @allure.title("HighVoltageService::HVSOCInfo_PropulsionCAN::0x131同帧非相关信号跳变无异常event")
    def test_caseid_1986531(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=305, no_opera_signal=['DispHvBattLvlOfChrg'])
        self.partner.ck_no_event(self.partner_key, "HVSOCInfo", timeout=0.2)

    @allure.title("HighVoltageService::HVSOCInfo_PropulsionCAN::0x143同帧非相关信号跳变无异常event")
    def test_caseid_1986530(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=323, no_opera_signal=['DCChrgnHndlSts'])
        self.partner.ck_no_event(self.partner_key, "HVSOCInfo", timeout=0.2)

    @allure.title("HighVoltageService::HVSOCInfo_PropulsionCAN::0x178同帧非相关信号跳变无异常event")
    def test_caseid_1986532(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=376, no_opera_signal=['HvBattSoc'])
        self.partner.ck_no_event(self.partner_key, "HVSOCInfo", timeout=0.2)

    @allure.title("HighVoltageService::HVThermalOutOfControl_PropulsionCAN::0x142同帧非相关信号跳变无异常event")
    def test_caseid_1986527(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=322, no_opera_signal=['HvBattLimnIndcn'])
        self.partner.ck_no_event(self.partner_key, "HVThermalOutOfControl", timeout=0.2)

    @allure.title("HighVoltageService::LimitedDischargePower_PropulsionCAN::0x105同帧非相关信号跳变无异常event")
    def test_caseid_1986493(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=261, no_opera_signal=['HvBattPwrLimDcha800'])
        self.partner.ck_no_event(self.partner_key, "LimitedDischargePower", timeout=0.2)

    @allure.title("HighVoltageService::LimitedDischargePower_PropulsionCAN::0x143同帧非相关信号跳变无异常event")
    def test_caseid_1986494(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=323, no_opera_signal=['HvBattPwrLimDcha1'])
        self.partner.ck_no_event(self.partner_key, "LimitedDischargePower", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_ChassisCAN1::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986563(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=256, no_opera_signal=['WhlMotSysSpdActSafe800IsgSpdActSgn800', 'WhlMotSysSpdActSafe800Qf'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x04C同帧非相关信号跳变无异常event")
    def test_caseid_1986573(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=76, no_opera_signal=['WhlMotSysTqEstIsgTqAct', 'WhlMotSysTqEstQualityFactor'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x060同帧非相关信号跳变无异常event")
    def test_caseid_1986565(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=96, no_opera_signal=['WhlMotSysSpdAct', 'WhlMotSysUdc', 'WhlMotSysCooltT'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x063同帧非相关信号跳变无异常event")
    def test_caseid_1986564(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=99, no_opera_signal=['WhlMotSysIdc', 'WhlMotSysSpdAct800', 'WhlMotSysUDc800'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x094同帧非相关信号跳变无异常event")
    def test_caseid_1986562(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=148, no_opera_signal=['IsgSpdActSgn800'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x095同帧非相关信号跳变无异常event")
    def test_caseid_1986572(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=149, no_opera_signal=['IsgTqActIsgTqAct', 'IsgTqActQualityFactor', 'IsgSpdActSgn'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x13A同帧非相关信号跳变无异常event")
    def test_caseid_1986571(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=314, no_opera_signal=['IsgIDc', 'IsgMotT', 'IsgCooltT'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x156同帧非相关信号跳变无异常event")
    def test_caseid_1986569(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=342, no_opera_signal=['IsgUDc', 'IsgUDc800'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x180同帧非相关信号跳变无异常event")
    def test_caseid_1986561(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=384, no_opera_signal=['IsgSpdActSgnSafe800IsgSpdActSgn800', 'IsgSpdActSgnSafe800Qf', 'IsgSpdActSgnSafe800IsgSpdActSgn800', 'IsgSpdActSgnSafe800Qf'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x272同帧非相关信号跳变无异常event")
    def test_caseid_1986567(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=626, no_opera_signal=['IemGenericEMSeqNr', 'IemGenericModStatusRms', 'IemGenericEMQnty'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x273同帧非相关信号跳变无异常event")
    def test_caseid_1986568(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=627, no_opera_signal=['IgmGenericModStatusRms', 'IgmGenericEMSeqNr'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x275同帧非相关信号跳变无异常event")
    def test_caseid_1986570(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=629, no_opera_signal=['IsgInvrT'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorInfo_PropulsionCAN::0x305同帧非相关信号跳变无异常event")
    def test_caseid_1986566(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=773, no_opera_signal=['WhlMotSysInvrT', 'WhlMotSysMotT'])
        self.partner.ck_no_event(self.partner_key, "MotorInfo", timeout=0.2)

    @allure.title("HighVoltageService::MotorPower_PropulsionCAN::0x04C同帧非相关信号跳变无异常event")
    def test_caseid_1986560(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=76, no_opera_signal=['WhlMotSysTqEstIsgTqAct'])
        self.partner.ck_no_event(self.partner_key, "MotorPower", timeout=0.2)

    @allure.title("HighVoltageService::MotorPower_PropulsionCAN::0x063同帧非相关信号跳变无异常event")
    def test_caseid_1986556(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=99, no_opera_signal=['WhlMotSysSpdAct800'])
        self.partner.ck_no_event(self.partner_key, "MotorPower", timeout=0.2)

    @allure.title("HighVoltageService::MotorPower_PropulsionCAN::0x095同帧非相关信号跳变无异常event")
    def test_caseid_1986559(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=149, no_opera_signal=['IsgTqActIsgTqAct'])
        self.partner.ck_no_event(self.partner_key, "MotorPower", timeout=0.2)

    @allure.title("HighVoltageService::MotorPower_PropulsionCAN::0x180同帧非相关信号跳变无异常event")
    def test_caseid_1986558(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=384, no_opera_signal=['IsgSpdActSgnSafeIsgSpdWSgnTyp'])
        self.partner.ck_no_event(self.partner_key, "MotorPower", timeout=0.2)

    @allure.title("HighVoltageService::MotorPower_PropulsionCAN::0x189同帧非相关信号跳变无异常event")
    def test_caseid_1986557(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=393, no_opera_signal=['WhlMotSysSpdActSafeIsgSpdWSgnTyp'])
        self.partner.ck_no_event(self.partner_key, "MotorPower", timeout=0.2)

    @allure.title("HighVoltageService::NotifyChargingEquipmentInformation_ConnectivityCANFD::0x177同帧非相关信号跳变无异常event")
    def test_caseid_1986551(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=375, no_opera_signal=['ChrgrPileInfo'])
        self.partner.ck_no_event(self.partner_key, "NotifyChargingEquipmentInformation", timeout=0.2)

    @allure.title("HighVoltageService::NotifyChargingEquipmentInformation_PropulsionCAN::0x053同帧非相关信号跳变无异常event")
    def test_caseid_1986553(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=83, no_opera_signal=['ChrgEquipIDc'])
        self.partner.ck_no_event(self.partner_key, "NotifyChargingEquipmentInformation", timeout=0.2)

    @allure.title("HighVoltageService::NotifyChargingEquipmentInformation_PropulsionCAN::0x105同帧非相关信号跳变无异常event")
    def test_caseid_1986554(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=261, no_opera_signal=['DCChrgrIMax'])
        self.partner.ck_no_event(self.partner_key, "NotifyChargingEquipmentInformation", timeout=0.2)

    @allure.title("HighVoltageService::NotifyChargingEquipmentInformation_PropulsionCAN::0x141同帧非相关信号跳变无异常event")
    def test_caseid_1986549(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=321, no_opera_signal=['HvBattUDc800', 'HvBattUDc'])
        self.partner.ck_no_event(self.partner_key, "NotifyChargingEquipmentInformation", timeout=0.2)

    @allure.title("HighVoltageService::NotifyChargingEquipmentInformation_PropulsionCAN::0x143同帧非相关信号跳变无异常event")
    def test_caseid_1986550(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=323, no_opera_signal=['DCChrgnHndlSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyChargingEquipmentInformation", timeout=0.2)

    @allure.title("HighVoltageService::NotifyChargingEquipmentInformation_PropulsionCAN::0x175同帧非相关信号跳变无异常event")
    def test_caseid_1986552(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=373, no_opera_signal=['JIDUChgrFlg'])
        self.partner.ck_no_event(self.partner_key, "NotifyChargingEquipmentInformation", timeout=0.2)

    @allure.title("HighVoltageService::NotifyDCDCSts_PropulsionCAN::0x14B同帧非相关信号跳变无异常event")
    def test_caseid_1986548(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=331, no_opera_signal=['DcDcActvd'])
        self.partner.ck_no_event(self.partner_key, "NotifyDCDCSts", timeout=0.2)

    @allure.title("HighVoltageService::NotifyEnergyRecoveryLimitSts_ChassisCAN2::0x233同帧非相关信号跳变无异常event")
    def test_caseid_1986539(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=563, no_opera_signal=['DrvPfmncRedn'])
        self.partner.ck_no_event(self.partner_key, "NotifyEnergyRecoveryLimitSts", timeout=0.2)

    @allure.title("HighVoltageService::NotifyHvBatteryCode_PropulsionCAN::0x342同帧非相关信号跳变无异常event")
    def test_caseid_1986538(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=834, no_opera_signal=['HvBattCodLen'])
        self.partner.ck_no_event(self.partner_key, "NotifyHvBatteryCode", timeout=0.2)

    @allure.title("HighVoltageService::NotifyHvBatteryCode_PropulsionCAN::0x347同帧非相关信号跳变无异常event")
    def test_caseid_1986537(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=839, no_opera_signal=['HvBattCodPackIndex', 'HvBattCodPackCodeX1', 'HvBattCodPackCodeX2', 'HvBattCodPackCodeX3', 'HvBattCodPackCodeX4', 'HvBattCodPackCodeX5', 'HvBattCodPackCodeX6'])
        self.partner.ck_no_event(self.partner_key, "NotifyHvBatteryCode", timeout=0.2)

    @allure.title("HighVoltageService::PowerConsumptionInfo_ChassisCAN1::0x340同帧非相关信号跳变无异常event")
    def test_caseid_1986534(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=832, no_opera_signal=['HvCabinThermPwrCns'])
        self.partner.ck_no_event(self.partner_key, "PowerConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::PowerConsumptionInfo_ChassisCAN1::0x3DF同帧非相关信号跳变无异常event")
    def test_caseid_1986535(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=991, no_opera_signal=['HvBattThermPwrCns'])
        self.partner.ck_no_event(self.partner_key, "PowerConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::PowerConsumptionInfo_ChassisCAN2::0x370同帧非相关信号跳变无异常event")
    def test_caseid_1986536(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=880, no_opera_signal=['DispBattEgyIn', 'DispBattEgyOut'])
        self.partner.ck_no_event(self.partner_key, "PowerConsumptionInfo", timeout=0.2)

    @allure.title("HighVoltageService::powerLimitedSts_BackboneFR::49-13-32同帧非相关信号跳变无异常event")
    def test_caseid_1986544(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3214624, no_opera_signal=['TelltlPwrLoss'])
        self.partner.ck_no_event(self.partner_key, "powerLimitedSts", timeout=0.2)

    @allure.title("HighVoltageService::powertrainFaultMsg_ChassisCAN2::0x233同帧非相关信号跳变无异常event")
    def test_caseid_1986546(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=563, no_opera_signal=['DrvPfmncRedn'])
        self.partner.ck_no_event(self.partner_key, "powertrainFaultMsg", timeout=0.2)

    @allure.title("HighVoltageService::powertrainFaultMsgValidity_ChassisCAN2::0x233同帧非相关信号跳变无异常event")
    def test_caseid_1986492(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=563, no_opera_signal=['DrvPfmncRedn'])
        self.partner.ck_no_event(self.partner_key, "powertrainFaultMsgValidity", timeout=0.2)

    @allure.title("HighVoltageService::powertrainFaultStsSts_ChassisCAN2::0x3B0同帧非相关信号跳变无异常event")
    def test_caseid_1986545(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=944, no_opera_signal=['HybErrIndcnReqTelltlSysHybFailr'])
        self.partner.ck_no_event(self.partner_key, "powertrainFaultStsSts", timeout=0.2)

    @allure.title("HighVoltageService::powertrainFaultStsStsValidity_ChassisCAN2::0x3B0同帧非相关信号跳变无异常event")
    def test_caseid_1986495(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=944, no_opera_signal=['HybErrIndcnReqTelltlSysHybFailr'])
        self.partner.ck_no_event(self.partner_key, "powertrainFaultStsStsValidity", timeout=0.2)

    @allure.title("HighVoltageService::ptSysFaultSts_ChassisCAN2::0x3B0同帧非相关信号跳变无异常event")
    def test_caseid_1986542(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=944, no_opera_signal=['HybErrIndcnReqTelltlSysHybFailr'])
        self.partner.ck_no_event(self.partner_key, "ptSysFaultSts", timeout=0.2)

    @allure.title("HighVoltageService::PulseHeatingInfo_ChassisCAN1::0x24B同帧非相关信号跳变无异常event")
    def test_caseid_1986294(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=587, no_opera_signal=['PlsHeatgSts'])
        self.partner.ck_no_event(self.partner_key, "PulseHeatingInfo", timeout=0.2)

    @allure.title("HighVoltageService::PulseHeatingInfo_PropulsionCAN::0x27A同帧非相关信号跳变无异常event")
    def test_caseid_1986293(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=634, no_opera_signal=['PlsHeatgTarT'])
        self.partner.ck_no_event(self.partner_key, "PulseHeatingInfo", timeout=0.2)

    @allure.title("HighVoltageService::RemainingMileage_BackboneFR::48-6-8同帧非相关信号跳变无异常event")
    def test_caseid_1986524(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3147272, no_opera_signal=['DstEstimdToEmptyForDrvgElec'])
        self.partner.ck_no_event(self.partner_key, "RemainingMileage", timeout=0.2)

    @allure.title("HighVoltageService::TemperatureMaintain_PropulsionCAN::0x175同帧非相关信号跳变无异常event")
    def test_caseid_1986503(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=373, no_opera_signal=['MaintainBattTFb'])
        self.partner.ck_no_event(self.partner_key, "TemperatureMaintain", timeout=0.2)

    @allure.title("HighVoltageService::wdMsgDisplaySts_BackboneFR::49-4-16同帧非相关信号跳变无异常event")
    def test_caseid_1986543(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3212304, no_opera_signal=['DispOfPrpsnModForEv'])
        self.partner.ck_no_event(self.partner_key, "wdMsgDisplaySts", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestKeyServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("KeyService", 'client')])
        self.partner_key = "KeyService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("KeyService::ConnectedZones_ConnectivityCANFD::0x198同帧非相关信号跳变无异常event")
    def test_caseid_1986388(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=408, no_opera_signal=['BLEKeyPrsntStsZone0', 'BLEKeyPrsntStsZone1', 'BLEKeyPrsntStsZone2', 'BLEKeyPrsntStsZone3', 'BLEKeyPrsntStsZone4', 'BLEKeyPrsntStsZone5', 'BLEKeyPrsntStsZone6', 'BLEKeyPrsntStsZone7', 'BLEKeyPrsntStsZone8', 'BLEKeyPrsntStsZone9', 'BLEKeyPrsntStsZone10', 'BLEKeyPrsntStsZone11', 'BLEKeyPrsntStsZone12', 'BLEKeyPrsntStsZone13', 'BLEKeyPrsntStsZone14', 'BLEKeyPrsntStsZone15'])
        self.partner.ck_no_event(self.partner_key, "ConnectedZones", timeout=0.2)

    @allure.title("KeyService::DigitalKeyConnectedStatus_ConnectivityCANFD::0x244同帧非相关信号跳变无异常event")
    def test_caseid_1986387(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=580, no_opera_signal=['DigKeyConnectInfo1KeyConnectSts', 'DigKeyConnectInfo1KeyIdByte0', 'DigKeyConnectInfo1KeyIdByte1', 'DigKeyConnectInfo1KeyIdByte2', 'DigKeyConnectInfo1KeyIdByte3', 'DigKeyConnectInfo1KeyIdByte4', 'DigKeyConnectInfo1KeyIdByte5', 'DigKeyConnectInfo1KeyIdByte6', 'DigKeyConnectInfo1KeyIdByte7', 'DigKeyConnectInfo1KeyIdByte8', 'DigKeyConnectInfo1KeyIdByte9', 'DigKeyConnectInfo1KeyIdByte10', 'DigKeyConnectInfo1KeyIdByte11', 'DigKeyConnectInfo1KeyIdByte12', 'DigKeyConnectInfo1KeyIdByte13', 'DigKeyConnectInfo1KeyIdByte14', 'DigKeyConnectInfo1KeyIdByte15', 'DigKeyConnectInfo1KeyPrsntZone', 'DigKeyConnectInfo1KeyTyp', 'DigKeyConnectInfo1BattWarn', 'DigKeyConnectInfo2KeyConnectSts', 'DigKeyConnectInfo2KeyIdByte0', 'DigKeyConnectInfo2KeyIdByte1', 'DigKeyConnectInfo2KeyIdByte2', 'DigKeyConnectInfo2KeyIdByte3', 'DigKeyConnectInfo2KeyIdByte4', 'DigKeyConnectInfo2KeyIdByte5', 'DigKeyConnectInfo2KeyIdByte6', 'DigKeyConnectInfo2KeyIdByte7', 'DigKeyConnectInfo2KeyIdByte8', 'DigKeyConnectInfo2KeyIdByte9', 'DigKeyConnectInfo2KeyIdByte10', 'DigKeyConnectInfo2KeyIdByte11', 'DigKeyConnectInfo2KeyIdByte12', 'DigKeyConnectInfo2KeyIdByte13', 'DigKeyConnectInfo2KeyIdByte14', 'DigKeyConnectInfo2KeyIdByte15', 'DigKeyConnectInfo2KeyPrsntZone', 'DigKeyConnectInfo2KeyTyp', 'DigKeyConnectInfo2BattWarn'])
        self.partner.ck_no_event(self.partner_key, "DigitalKeyConnectedStatus", timeout=0.2)

    @allure.title("KeyService::DigitalKeyConnectedStatus_ConnectivityCANFD::0x245同帧非相关信号跳变无异常event")
    def test_caseid_1986386(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=581, no_opera_signal=['DigKeyConnectInfo3KeyConnectSts', 'DigKeyConnectInfo3KeyIdByte0', 'DigKeyConnectInfo3KeyIdByte1', 'DigKeyConnectInfo3KeyIdByte2', 'DigKeyConnectInfo3KeyIdByte3', 'DigKeyConnectInfo3KeyIdByte4', 'DigKeyConnectInfo3KeyIdByte5', 'DigKeyConnectInfo3KeyIdByte6', 'DigKeyConnectInfo3KeyIdByte7', 'DigKeyConnectInfo3KeyIdByte8', 'DigKeyConnectInfo3KeyIdByte9', 'DigKeyConnectInfo3KeyIdByte10', 'DigKeyConnectInfo3KeyIdByte11', 'DigKeyConnectInfo3KeyIdByte12', 'DigKeyConnectInfo3KeyIdByte13', 'DigKeyConnectInfo3KeyIdByte14', 'DigKeyConnectInfo3KeyIdByte15', 'DigKeyConnectInfo3KeyPrsntZone', 'DigKeyConnectInfo3KeyTyp', 'DigKeyConnectInfo3BattWarn', 'DigKeyConnectInfo4KeyConnectSts', 'DigKeyConnectInfo4KeyIdByte0', 'DigKeyConnectInfo4KeyIdByte1', 'DigKeyConnectInfo4KeyIdByte2', 'DigKeyConnectInfo4KeyIdByte3', 'DigKeyConnectInfo4KeyIdByte4', 'DigKeyConnectInfo4KeyIdByte5', 'DigKeyConnectInfo4KeyIdByte6', 'DigKeyConnectInfo4KeyIdByte7', 'DigKeyConnectInfo4KeyIdByte8', 'DigKeyConnectInfo4KeyIdByte9', 'DigKeyConnectInfo4KeyIdByte10', 'DigKeyConnectInfo4KeyIdByte11', 'DigKeyConnectInfo4KeyIdByte12', 'DigKeyConnectInfo4KeyIdByte13', 'DigKeyConnectInfo4KeyIdByte14', 'DigKeyConnectInfo4KeyIdByte15', 'DigKeyConnectInfo4KeyPrsntZone', 'DigKeyConnectInfo4KeyTyp', 'DigKeyConnectInfo4BattWarn'])
        self.partner.ck_no_event(self.partner_key, "DigitalKeyConnectedStatus", timeout=0.2)

    @allure.title("KeyService::KeyWhiteListVersion_ConnectivityCANFD::0x3A0同帧非相关信号跳变无异常event")
    def test_caseid_1986384(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=928, no_opera_signal=['EntityKeyWhiteListVers', 'BLESlotKeyWhiteListVers'])
        self.partner.ck_no_event(self.partner_key, "KeyWhiteListVersion", timeout=0.2)

    @allure.title("KeyService::NotifyCarLocalTraceActiveStatus_ConnectivityCANFD::0x380同帧非相关信号跳变无异常event")
    def test_caseid_1986385(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=896, no_opera_signal=['CarLoctrActvnSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyCarLocalTraceActiveStatus", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestLightServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("LightService", 'client')])
        self.partner_key = "LightService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("LightService::AutoHighBeamStatus_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986796(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['ExtrLtgStsHiBeam', 'ExtrLtgStsFlash'])
        self.partner.ck_no_event(self.partner_key, "AutoHighBeamStatus", timeout=0.2)

    @allure.title("LightService::LightControl_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986800(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['ExtrLtgStsReFog'])
        self.partner.ck_no_event(self.partner_key, "LightControl", timeout=0.2)

    @allure.title("LightService::LightFault_BackboneFR::40-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986780(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2621456, no_opera_signal=['SALM1Flt', 'SALM2Flt', 'SALM3Flt', 'SALM4Flt', 'SALM5Flt', 'SALM6Flt', 'ALM9Flt', 'ALM10Flt'])
        self.partner.ck_no_event(self.partner_key, "LightFault", timeout=0.2)

    @allure.title("LightService::LightShowActivateStatus_BodyExposedCANFD::0x09A同帧非相关信号跳变无异常event")
    def test_caseid_1986784(self):
        self.ipdu.filter_special_message_send(bus_name="bodyexposedcanfd", message=154, no_opera_signal=['StaticLightingModeEn'])
        self.partner.ck_no_event(self.partner_key, "LightShowActivateStatus", timeout=0.2)

    @allure.title("LightService::NotifyHazardLightSwitchStatus_BackboneFR::37-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986782(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2425090, no_opera_signal=['SwtLiHzrdWarn'])
        self.partner.ck_no_event(self.partner_key, "NotifyHazardLightSwitchStatus", timeout=0.2)

    @allure.title("LightService::NotifyHighBeamSwitchStatus_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986801(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlTouchSwtLe3'])
        self.partner.ck_no_event(self.partner_key, "NotifyHighBeamSwitchStatus", timeout=0.2)

    @allure.title("LightService::NotifyHighBeamSwitchStatus_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986802(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlTouchSwtRi1SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "NotifyHighBeamSwitchStatus", timeout=0.2)

    @allure.title("LightService::NotifySteerWheelBackLightEnableStatus_BodyCAN::0x230同帧非相关信号跳变无异常event")
    def test_caseid_1986783(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=560, no_opera_signal=['ActvnOfIndcrIllmn'])
        self.partner.ck_no_event(self.partner_key, "NotifySteerWheelBackLightEnableStatus", timeout=0.2)

    @allure.title("LightService::NotifyTurnLampStatus_BodyCAN::0x020同帧非相关信号跳变无异常event")
    def test_caseid_1986781(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=32, no_opera_signal=['IndcrSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyTurnLampStatus", timeout=0.2)

    @allure.title("LightService::Status_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986795(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['ExtrLtgStsLoBeam', 'ExtrLtgStsFrntFogTBD', 'ExtrLtgStsReFog', 'ExtrLtgStsPosLiFrnt', 'ExtrLtgStsPosLiRe', 'ExtrLtgStsAFSTBD', 'ExtrLtgStsAHL', 'ExtrLtgStsFlash', 'ExtrLtgStsDBL', 'ExtrLtgStsReverseLi', 'ExtrLtgStsStopLi', 'ExtrLtgStsDRL', 'ExtrLtgStsWelcomeTBD', 'ExtrLtgStsTurnIndrLe', 'ExtrLtgStsTurnIndrRi'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986788(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['IndcrDisp'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_BodyCAN::0x0E0同帧非相关信号跳变无异常event")
    def test_caseid_1986786(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=224, no_opera_signal=['IntrBriSts'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_BodyExposedCANFD::0x250同帧非相关信号跳变无异常event")
    def test_caseid_1986792(self):
        self.ipdu.filter_special_message_send(bus_name="bodyexposedcanfd", message=592, no_opera_signal=['StsOfLedReWheelLampLe', 'StsOfLedReLampLe2', 'StsOfLedReLampLe1'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_BodyExposedCANFD::0x251同帧非相关信号跳变无异常event")
    def test_caseid_1986794(self):
        self.ipdu.filter_special_message_send(bus_name="bodyexposedcanfd", message=593, no_opera_signal=['StsOfLedFrntWheelLampLe', 'StsOfLedFrntLampLe1', 'StsOfLedFrntLampMid1', 'StsOfLedFrntLampLe2'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_BodyExposedCANFD::0x252同帧非相关信号跳变无异常event")
    def test_caseid_1986793(self):
        self.ipdu.filter_special_message_send(bus_name="bodyexposedcanfd", message=594, no_opera_signal=['StsOfLedFrntWheelLampRi', 'StsOfLedFrntLampRi1', 'StsOfLedFrntLampRi2'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_BodyExposedCANFD::0x254同帧非相关信号跳变无异常event")
    def test_caseid_1986785(self):
        self.ipdu.filter_special_message_send(bus_name="bodyexposedcanfd", message=596, no_opera_signal=['StsOfLedReLampMid1'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_BodyExposedCANFD::0x260同帧非相关信号跳变无异常event")
    def test_caseid_1986791(self):
        self.ipdu.filter_special_message_send(bus_name="bodyexposedcanfd", message=608, no_opera_signal=['StsOfLedReWheelLampRi', 'StsOfLedReLampRi2', 'StsOfLedReLampRi1'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_CEM_LIN2::0x12同帧非相关信号跳变无异常event")
    def test_caseid_1986790(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin2", message=18, no_opera_signal=['StsOfLedLeftAIILY1', 'StsOfLedLeftAIILY2', 'StsOfLedLeftAIILY3', 'StsOfLedLeftAIILY4'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_CEM_LIN2::0x13同帧非相关信号跳变无异常event")
    def test_caseid_1986789(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin2", message=19, no_opera_signal=['StsOfLedRightAIILY1', 'StsOfLedRightAIILY2', 'StsOfLedRightAIILY3', 'StsOfLedRightAIILY4'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("LightService::Status_CEM_LIN3::0x20同帧非相关信号跳变无异常event")
    def test_caseid_1986787(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin3", message=32, no_opera_signal=['ReadLiStsFirstRowLe', 'ReadLiStsFirstRowRi', 'ReadLiStsSecondRowLe', 'ReadLiStsSecondRowRi', 'ReadLiStsThirdRowLe', 'ReadLiStsThirdRowRi'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestLowVoltageServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("LowVoltageService", 'client')])
        self.partner_key = "LowVoltageService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("LowVoltageService::BatteryStatus_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986489(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['VehBattUSysU', 'VehBattUSysUQf', 'ChrgnUReq'])
        self.partner.ck_no_event(self.partner_key, "BatteryStatus", timeout=0.2)

    @allure.title("LowVoltageService::BatteryStatus_CEM_LIN6::0x02同帧非相关信号跳变无异常event")
    def test_caseid_1986487(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=2, no_opera_signal=['BattIRaw'])
        self.partner.ck_no_event(self.partner_key, "BatteryStatus", timeout=0.2)

    @allure.title("LowVoltageService::BatteryStatus_CEM_LIN6::0x04同帧非相关信号跳变无异常event")
    def test_caseid_1986486(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=4, no_opera_signal=['BattTRaw', 'BattCpEstimdRaw', 'BattIQuiscFildLongRaw', 'BattIQuiscAvgRaw'])
        self.partner.ck_no_event(self.partner_key, "BatteryStatus", timeout=0.2)

    @allure.title("LowVoltageService::BatteryStatus_CEM_LIN6::0x06同帧非相关信号跳变无异常event")
    def test_caseid_1986488(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=6, no_opera_signal=['BattSocRaw', 'BattURaw'])
        self.partner.ck_no_event(self.partner_key, "BatteryStatus", timeout=0.2)

    @allure.title("LowVoltageService::BatteryStatus_CEM_LIN6::0x09同帧非相关信号跳变无异常event")
    def test_caseid_1986485(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=9, no_opera_signal=['BattRRaw', 'BattIQuiscFildShoRaw', 'BattCircOpenU', 'BattSnsrCalcnNotVldRaw'])
        self.partner.ck_no_event(self.partner_key, "BatteryStatus", timeout=0.2)

    @allure.title("LowVoltageService::BatteryStatus_PropulsionCAN::0x149同帧非相关信号跳变无异常event")
    def test_caseid_1986484(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=329, no_opera_signal=['IDcDcActLoSideIDcDcActLoSide'])
        self.partner.ck_no_event(self.partner_key, "BatteryStatus", timeout=0.2)

    @allure.title("LowVoltageService::LowWarn_BackboneFR::39-2-8同帧非相关信号跳变无异常event")
    def test_caseid_1986490(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556424, no_opera_signal=['ULoWarnULoWarn'])
        self.partner.ck_no_event(self.partner_key, "LowWarn", timeout=0.2)

    @allure.title("LowVoltageService::LVBatteryRechargeReqSts_InfoCANFD::0x0E1同帧非相关信号跳变无异常event")
    def test_caseid_1986481(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=225, no_opera_signal=['LVBattCnvnReq'])
        self.partner.ck_no_event(self.partner_key, "LVBatteryRechargeReqSts", timeout=0.2)

    @allure.title("LowVoltageService::LVFault_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986483(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['LVPwrSplyErrSts'])
        self.partner.ck_no_event(self.partner_key, "LVFault", timeout=0.2)

    @allure.title("LowVoltageService::LVFaultValidity_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986482(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['LVPwrSplyErrSts'])
        self.partner.ck_no_event(self.partner_key, "LVFaultValidity", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestOuterRearViewServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("OuterRearViewService", 'client')])
        self.partner_key = "OuterRearViewService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("OuterRearViewService::OuterRearViewFoldStatus_BodyCAN::0x010同帧非相关信号跳变无异常event")
    def test_caseid_1986378(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=16, no_opera_signal=['MirrFoldStsAtPass'])
        self.partner.ck_no_event(self.partner_key, "OuterRearViewFoldStatus", timeout=0.2)

    @allure.title("OuterRearViewService::OuterRearViewFoldStatus_BodyCAN::0x030同帧非相关信号跳变无异常event")
    def test_caseid_1986379(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=48, no_opera_signal=['MirrFoldStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "OuterRearViewFoldStatus", timeout=0.2)

    @allure.title("OuterRearViewService::OuterRearViewMirrorAngle_BodyCAN::0x123同帧非相关信号跳变无异常event")
    def test_caseid_1986377(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=291, no_opera_signal=['MirrPosnToCldAtDrvrMirrPosnAdjCldLeRi', 'MirrPosnToCldAtDrvrMirrPosnAdjCldUpDwn'])
        self.partner.ck_no_event(self.partner_key, "OuterRearViewMirrorAngle", timeout=0.2)

    @allure.title("OuterRearViewService::OuterRearViewMirrorAngle_BodyCAN::0x125同帧非相关信号跳变无异常event")
    def test_caseid_1986376(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=293, no_opera_signal=['MirrPosnToCldAtPassMirrPosnAdjCldLeRi', 'MirrPosnToCldAtPassMirrPosnAdjCldUpDwn'])
        self.partner.ck_no_event(self.partner_key, "OuterRearViewMirrorAngle", timeout=0.2)

    @allure.title("OuterRearViewService::ViewFault_BodyCAN::0x123同帧非相关信号跳变无异常event")
    def test_caseid_1986381(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=291, no_opera_signal=['DrvrMirrorFoldErrorFb', 'DrvrMirrorAdjErrorFb'])
        self.partner.ck_no_event(self.partner_key, "ViewFault", timeout=0.2)

    @allure.title("OuterRearViewService::ViewFault_BodyCAN::0x125同帧非相关信号跳变无异常event")
    def test_caseid_1986380(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=293, no_opera_signal=['PassMirrorFoldErrorFb', 'PassMirrorAdjErrorFb'])
        self.partner.ck_no_event(self.partner_key, "ViewFault", timeout=0.2)

    @allure.title("OuterRearViewService::ViewTiltStatus_BodyCAN::0x010同帧非相关信号跳变无异常event")
    def test_caseid_1986382(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=16, no_opera_signal=['MirrDwnStsAtPass'])
        self.partner.ck_no_event(self.partner_key, "ViewTiltStatus", timeout=0.2)

    @allure.title("OuterRearViewService::ViewTiltStatus_BodyCAN::0x123同帧非相关信号跳变无异常event")
    def test_caseid_1986383(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=291, no_opera_signal=['MirrDwnStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "ViewTiltStatus", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestPassiveSafetyServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("PassiveSafetyService", 'client')])
        self.partner_key = "PassiveSafetyService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)
    
    @allure.title("PassiveSafetyService::PedestrianProtectionWarning_BackboneFR::12-6-64同帧非相关信号跳变无异常event")
    def test_caseid_1986373(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=788032, no_opera_signal=['PedProtnMsgReqForFlt', 'PedProtnMsgReqForImpct'])
        self.partner.ck_no_event(self.partner_key, "PedestrianProtectionWarning", timeout=0.2)

    @allure.title("PassiveSafetyService::AirbagWarning_BackboneFR::12-6-64同帧非相关信号跳变无异常event")
    def test_caseid_1986375(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=788032, no_opera_signal=['RestrntSysLampReq', 'RestrntSysMsgReq'])
        self.partner.ck_no_event(self.partner_key, "AirbagWarning", timeout=0.2)

    @allure.title("PassiveSafetyService::AirbagWarning_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986374(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "AirbagWarning", timeout=0.2)

    @allure.title("PassiveSafetyService::NotifyVehicleCrashStatus_BackboneFR::12-6-64同帧非相关信号跳变无异常event")
    def test_caseid_1986372(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=788032, no_opera_signal=['RecOfImpctCrashRollovr', 'RecOfImpctCrashFrnt', 'RecOfImpctCrashRe', 'RecOfImpctCrashSideLe', 'RecOfImpctCrashSideRi'])
        self.partner.ck_no_event(self.partner_key, "NotifyVehicleCrashStatus", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestPedalServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("PedalService", 'client')])
        self.partner_key = "PedalService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("PedalService::AccPedalPosition_PropulsionCAN::0x04A同帧非相关信号跳变无异常event")
    def test_caseid_1986640(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=74, no_opera_signal=['AccrPedlRatAccrPedlRat'])
        self.partner.ck_no_event(self.partner_key, "AccPedalPosition", timeout=0.2)

    @allure.title("PedalService::AccPedalStatus_ChassisCAN2::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986638(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=256, no_opera_signal=['AccrPedlPsdAccrPedlPsd', 'AccrPedlPsdSts'])
        self.partner.ck_no_event(self.partner_key, "AccPedalStatus", timeout=0.2)

    @allure.title("PedalService::BrakePedalPosition_BackboneFR::57-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986639(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3736840, no_opera_signal=['BrkPedlrRatPerc', 'BrkPedlrRatQf'])
        self.partner.ck_no_event(self.partner_key, "BrakePedalPosition", timeout=0.2)

    @allure.title("PedalService::BrakePedalStatus_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986637(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['BrkPedlPsdBrkPedlPsd'])
        self.partner.ck_no_event(self.partner_key, "BrakePedalStatus", timeout=0.2)

    @allure.title("PedalService::BrakePedalTravel_ChassisCAN2::0x102同帧非相关信号跳变无异常event")
    def test_caseid_1986282(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=258, no_opera_signal=['BrkPedlTrvlAct'])
        self.partner.ck_no_event(self.partner_key, "BrakePedalTravel", timeout=0.2)

    @allure.title("PedalService::PedalFault_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986643(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['BrkPedlPsdBrkPedlPsd', 'BrkPedlPsdQf'])
        self.partner.ck_no_event(self.partner_key, "PedalFault", timeout=0.2)

    @allure.title("PedalService::PedalFault_BackboneFR::57-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986641(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3736840, no_opera_signal=['BrkPedlrRatPerc', 'BrkPedlrRatQf'])
        self.partner.ck_no_event(self.partner_key, "PedalFault", timeout=0.2)

    @allure.title("PedalService::PedalFault_ChassisCAN2::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986642(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=256, no_opera_signal=['AccrPedlPsdAccrPedlPsd', 'AccrPedlPsdSts'])
        self.partner.ck_no_event(self.partner_key, "PedalFault", timeout=0.2)

    @allure.title("PedalService::PedalFault_PropulsionCAN::0x04A同帧非相关信号跳变无异常event")
    def test_caseid_1986644(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=74, no_opera_signal=['AccrPedlRatAccrPedlRat'])
        self.partner.ck_no_event(self.partner_key, "PedalFault", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestSeatServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("SeatService", 'client')])
        self.partner_key = "SeatService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("SeatService::BeltEquipStatus_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986598(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['BltLockStAtRowSecLeBltLockEquid', 'BltLockStAtRowSecMidBltLockEquid', 'BltLockStAtRowSecRiBltLockEquid'])
        self.partner.ck_no_event(self.partner_key, "BeltEquipStatus", timeout=0.2)

    @allure.title("SeatService::BeltPretensioningWarning_PassiveSafetyCAN::0x153同帧非相关信号跳变无异常event")
    def test_caseid_1986597(self):
        self.ipdu.filter_special_message_send(bus_name="passivesafetycan", message=339, no_opera_signal=['MsgReqForRtrctrRvsbLe'])
        self.partner.ck_no_event(self.partner_key, "BeltPretensioningWarning", timeout=0.2)

    @allure.title("SeatService::BeltWarning_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986633(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['BltLockStAtPassBltLockSts', 'BltLockStAtRowSecRiBltLockSts', 'BltLockStAtRowSecMidBltLockSts', 'BltLockStAtRowSecLeBltLockSts', 'PassSeatSts', 'SeatOccptAtRowSecLe', 'SeatOccptAtRowSecMid', 'SeatOccptAtRowSecRi', 'BltLockStAtPassBltLockSt1', 'BltLockStAtRowSecLeBltLockSt1', 'BltLockStAtRowSecMidBltLockSt1', 'BltLockStAtRowSecRiBltLockSt1'])
        self.partner.ck_no_event(self.partner_key, "BeltWarning", timeout=0.2)

    @allure.title("SeatService::BeltWarning_BackboneFR::17-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986635(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1114370, no_opera_signal=['VehSpdIndcdVehSpdIndcd'])
        self.partner.ck_no_event(self.partner_key, "BeltWarning", timeout=0.2)

    @allure.title("SeatService::BeltWarning_BackboneFR::20-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986634(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1310721, no_opera_signal=['BltLockStAtDrvrBltLockSts', 'BltLockStAtDrvrBltLockSt1'])
        self.partner.ck_no_event(self.partner_key, "BeltWarning", timeout=0.2)

    @allure.title("SeatService::BeltWarning_BackboneFR::39-4-8同帧非相关信号跳变无异常event")
    def test_caseid_1986632(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556936, no_opera_signal=['TotDstTrvldHiResl'])
        self.partner.ck_no_event(self.partner_key, "BeltWarning", timeout=0.2)

    @allure.title("SeatService::BeltWarning_BackboneFR::57-0-4同帧非相关信号跳变无异常event")
    def test_caseid_1986636(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3735556, no_opera_signal=['VehSpdLgtQf'])
        self.partner.ck_no_event(self.partner_key, "BeltWarning", timeout=0.2)

    @allure.title("SeatService::BeltWarning_BodyCAN::0x040同帧非相关信号跳变无异常event")
    def test_caseid_1986631(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=64, no_opera_signal=['DoorDrvrSts', 'DoorLeReSts'])
        self.partner.ck_no_event(self.partner_key, "BeltWarning", timeout=0.2)

    @allure.title("SeatService::BeltWarning_BodyCAN::0x0E0同帧非相关信号跳变无异常event")
    def test_caseid_1986630(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=224, no_opera_signal=['DoorPassSts', 'DoorRiReSts'])
        self.partner.ck_no_event(self.partner_key, "BeltWarning", timeout=0.2)

    @allure.title("SeatService::FrntLeftBeltSts_BackboneFR::20-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986588(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1310721, no_opera_signal=['BltLockStAtDrvrBltLockSt1', 'BltLockStAtDrvrBltLockSts'])
        self.partner.ck_no_event(self.partner_key, "FrntLeftBeltSts", timeout=0.2)

    @allure.title("SeatService::FrntLeftSeatHeatVentStatus_BodyCAN::0x299同帧非相关信号跳变无异常event")
    def test_caseid_1986580(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=665, no_opera_signal=['DrvrSeatHeatgLvlSts', 'DrvrSeatHeatgAvlSts', 'DrvrSeatVentnLvlSts', 'DrvrSeatVentAvlSts'])
        self.partner.ck_no_event(self.partner_key, "FrntLeftSeatHeatVentStatus", timeout=0.2)

    @allure.title("SeatService::FrntLeftSeatPosition_BodyCAN::0x069同帧非相关信号跳变无异常event")
    def test_caseid_1986582(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=105, no_opera_signal=['SeatBackAngleRowFirstDrvr'])
        self.partner.ck_no_event(self.partner_key, "FrntLeftSeatPosition", timeout=0.2)

    @allure.title("SeatService::FrntLeftSeatPosition_BodyCAN::0x110同帧非相关信号跳变无异常event")
    def test_caseid_1986583(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=272, no_opera_signal=['DrvrSeatPosPercSeatPosFrntHeiPerc', 'DrvrSeatPosPercSeatPosFrntHeiQF', 'DrvrSeatPosPercSeatPosHeiPerc', 'DrvrSeatPosPercSeatPosHeiQF', 'DrvrSeatPosPercSeatPosSldPerc', 'DrvrSeatPosPercSeatPosSldQF'])
        self.partner.ck_no_event(self.partner_key, "FrntLeftSeatPosition", timeout=0.2)

    @allure.title("SeatService::FrntRightBeltSts_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986587(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['BltLockStAtPassBltLockSt1', 'BltLockStAtPassBltLockSts'])
        self.partner.ck_no_event(self.partner_key, "FrntRightBeltSts", timeout=0.2)

    @allure.title("SeatService::FrntRightSeatHeatVentStatus_BodyCAN::0x427同帧非相关信号跳变无异常event")
    def test_caseid_1986579(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1063, no_opera_signal=['PassSeatHeatgLvlSts', 'PassSeatHeatgAvlSts', 'PassSeatVentnLvlSts', 'PassSeatVentAvlSts'])
        self.partner.ck_no_event(self.partner_key, "FrntRightSeatHeatVentStatus", timeout=0.2)

    @allure.title("SeatService::FrntRightSeatPosition_BodyCAN::0x113同帧非相关信号跳变无异常event")
    def test_caseid_1986581(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=275, no_opera_signal=['PassSeatPosPercSeatPosFrntHeiPerc', 'PassSeatPosPercSeatPosFrntHeiQF', 'PassSeatPosPercSeatPosHeiPerc', 'PassSeatPosPercSeatPosHeiQF', 'PassSeatPosPercSeatPosSldPerc', 'PassSeatPosPercSeatPosSldQF', 'SeatBackAngleRowFirstPass'])
        self.partner.ck_no_event(self.partner_key, "FrntRightSeatPosition", timeout=0.2)

    @allure.title("SeatService::MassageConf_BodyCAN::0x299同帧非相关信号跳变无异常event")
    def test_caseid_1986604(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=665, no_opera_signal=['DrvrMassgRunng'])
        self.partner.ck_no_event(self.partner_key, "MassageConf", timeout=0.2)

    @allure.title("SeatService::MassageConf_BodyCAN::0x427同帧非相关信号跳变无异常event")
    def test_caseid_1986603(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1063, no_opera_signal=['PassMassgRunng'])
        self.partner.ck_no_event(self.partner_key, "MassageConf", timeout=0.2)

    @allure.title("SeatService::RearLeftBeltSts_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986586(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['BltLockStAtRowSecLeBltLockSt1', 'BltLockStAtRowSecLeBltLockSts', 'BltLockStAtRowSecLe_UB'], UB_Flag=False)
        self.partner.ck_no_event(self.partner_key, "RearLeftBeltSts", timeout=0.2)

    @allure.title("SeatService::RearLeftSeatHeatVentStatus_BodyCAN::0x385同帧非相关信号跳变无异常event")
    def test_caseid_1986578(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=901, no_opera_signal=['SeatHeatgLvlStsRowSecLe', 'SeatHeatgAvlStsRowSecLe'])
        self.partner.ck_no_event(self.partner_key, "RearLeftSeatHeatVentStatus", timeout=0.2)

    @allure.title("SeatService::RearLeftSeatHeatVentStatus_BodyCAN::0x386同帧非相关信号跳变无异常event")
    def test_caseid_1986577(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=902, no_opera_signal=['SeatVentnLvlStsRowSecLe', 'SeatVentAvlStsRowSecLe'])
        self.partner.ck_no_event(self.partner_key, "RearLeftSeatHeatVentStatus", timeout=0.2)

    @allure.title("SeatService::RearMiddleBeltSts_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986585(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['BltLockStAtRowSecMidBltLockSt1', 'BltLockStAtRowSecMidBltLockSts', 'BltLockStAtRowSecMid_UB'], UB_Flag=False)
        self.partner.ck_no_event(self.partner_key, "RearMiddleBeltSts", timeout=0.2)

    @allure.title("SeatService::RearRightBeltSts_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986584(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['BltLockStAtRowSecRiBltLockSt1', 'BltLockStAtRowSecRiBltLockSts', 'BltLockStAtRowSecRi_UB'], UB_Flag=False)
        self.partner.ck_no_event(self.partner_key, "RearRightBeltSts", timeout=0.2)

    @allure.title("SeatService::RearRightSeatHeatVentStatus_BodyCAN::0x385同帧非相关信号跳变无异常event")
    def test_caseid_1986576(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=901, no_opera_signal=['SeatHeatgLvlStsRowSecRi', 'SeatHeatgAvlStsRowSecRi'])
        self.partner.ck_no_event(self.partner_key, "RearRightSeatHeatVentStatus", timeout=0.2)

    @allure.title("SeatService::RearRightSeatHeatVentStatus_BodyCAN::0x386同帧非相关信号跳变无异常event")
    def test_caseid_1986575(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=902, no_opera_signal=['SeatVentnLvlStsRowSecRi', 'SeatVentAvlStsRowSecRi'])
        self.partner.ck_no_event(self.partner_key, "RearRightSeatHeatVentStatus", timeout=0.2)

    @allure.title("SeatService::SeatFault_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986595(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['BltLockStAtPassBltLockSts', 'BltLockStAtRowSecLeBltLockSts', 'BltLockStAtRowSecMidBltLockSts', 'BltLockStAtRowSecRiBltLockSts', 'BltLockStAtRowSecLe_UB', 'BltLockStAtRowSecMid_UB', 'BltLockStAtRowSecRi_UB'], UB_Flag=False)
        self.partner.ck_no_event(self.partner_key, "SeatFault", timeout=0.2)

    @allure.title("SeatService::SeatFault_BackboneFR::20-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986596(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1310721, no_opera_signal=['BltLockStAtDrvrBltLockSts'])
        self.partner.ck_no_event(self.partner_key, "SeatFault", timeout=0.2)

    @allure.title("SeatService::SeatFault_BodyCAN::0x110同帧非相关信号跳变无异常event")
    def test_caseid_1986594(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=272, no_opera_signal=['DrvrSeatPosPercSeatPosFrntHeiQF', 'DrvrSeatPosPercSeatPosHeiQF', 'DrvrSeatPosPercSeatPosSldQF'])
        self.partner.ck_no_event(self.partner_key, "SeatFault", timeout=0.2)

    @allure.title("SeatService::SeatFault_BodyCAN::0x113同帧非相关信号跳变无异常event")
    def test_caseid_1986593(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=275, no_opera_signal=['PassSeatPosPercSeatPosHeiQF', 'PassSeatPosPercSeatPosSldQF'])
        self.partner.ck_no_event(self.partner_key, "SeatFault", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatus_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986601(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['PassSeatSts', 'SeatOccptAtRowSecLe', 'SeatOccptAtRowSecMid', 'SeatOccptAtRowSecRi', 'BltLockStAtPassBltLockSt1', 'BltLockStAtRowSecLeBltLockSt1', 'BltLockStAtRowSecMidBltLockSt1', 'BltLockStAtRowSecRiBltLockSt1'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatus", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatus_BackboneFR::20-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986599(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1310721, no_opera_signal=['BltLockStAtDrvrBltLockSt1'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatus", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatus_BackboneFR::39-6-16同帧非相关信号跳变无异常event")
    def test_caseid_1986602(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557456, no_opera_signal=['DrvrSeatSts'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatus", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatus_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986600(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['BrkPedlPsdBrkPedlPsd'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatus", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatusValidity_BackboneFR::12-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986591(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=786690, no_opera_signal=['PassSeatSts', 'SeatOccptAtRowSecLe', 'SeatOccptAtRowSecMid', 'SeatOccptAtRowSecRi', 'BltLockStAtPassBltLockSt1', 'BltLockStAtRowSecLeBltLockSt1', 'BltLockStAtRowSecMidBltLockSt1', 'BltLockStAtRowSecRiBltLockSt1'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatusValidity", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatusValidity_BackboneFR::20-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986589(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1310721, no_opera_signal=['BltLockStAtDrvrBltLockSt1'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatusValidity", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatusValidity_BackboneFR::39-6-16同帧非相关信号跳变无异常event")
    def test_caseid_1986592(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557456, no_opera_signal=['DrvrSeatSts'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatusValidity", timeout=0.2)

    @allure.title("SeatService::SeatOccupyStatusValidity_BackboneFR::55-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986590(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3604481, no_opera_signal=['BrkPedlPsdBrkPedlPsd'])
        self.partner.ck_no_event(self.partner_key, "SeatOccupyStatusValidity", timeout=0.2)

    @allure.title("SeatService::SeatSwitchStatus_BodyCAN::0x069同帧非相关信号跳变无异常event")
    def test_caseid_1986612(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=105, no_opera_signal=['DrvrSeatBtnPsd'])
        self.partner.ck_no_event(self.partner_key, "SeatSwitchStatus", timeout=0.2)

    @allure.title("SeatService::SeatSwitchStatus_BodyCAN::0x130同帧非相关信号跳变无异常event")
    def test_caseid_1986610(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=304, no_opera_signal=['PassSeatBtnPsd'])
        self.partner.ck_no_event(self.partner_key, "SeatSwitchStatus", timeout=0.2)

    @allure.title("SeatService::SeatSwitchStatus_BodyCAN::0x299同帧非相关信号跳变无异常event")
    def test_caseid_1986613(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=665, no_opera_signal=['DrvrSeatSwtStsDrvrSeatSwtHeiSts', 'DrvrSeatSwtStsDrvrSeatSwtHeiFrntSts', 'DrvrSeatSwtStsDrvrSeatSwtSldSts', 'DrvrSeatSwtStsDrvrSeatSwtInclSts', 'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctHozlSts', 'DrvrSeatSwtStsDrvrSeatSwtAdjmtOfSpplFctVertSts'])
        self.partner.ck_no_event(self.partner_key, "SeatSwitchStatus", timeout=0.2)

    @allure.title("SeatService::SeatSwitchStatus_BodyCAN::0x427同帧非相关信号跳变无异常event")
    def test_caseid_1986611(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1063, no_opera_signal=['PassSeatSwtSts2PassSeatSwtHeiSts', 'PassSeatSwtSts2PassSeatSwtHeiFrntSts', 'PassSeatSwtSts2PassSeatSwtSldSts', 'PassSeatSwtSts2PassSeatSwtInclSts', 'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctHozlSts', 'PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctVerSts'])
        self.partner.ck_no_event(self.partner_key, "SeatSwitchStatus", timeout=0.2)

    @allure.title("SeatService::SeatSysStatus_BodyCAN::0x069同帧非相关信号跳变无异常event")
    def test_caseid_1986608(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=105, no_opera_signal=['DrvrSeatInAutMovmt'])
        self.partner.ck_no_event(self.partner_key, "SeatSysStatus", timeout=0.2)

    @allure.title("SeatService::SeatSysStatus_BodyCAN::0x110同帧非相关信号跳变无异常event")
    def test_caseid_1986609(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=272, no_opera_signal=['DrvrSeatExtAdjAllowd'])
        self.partner.ck_no_event(self.partner_key, "SeatSysStatus", timeout=0.2)

    @allure.title("SeatService::SeatSysStatus_BodyCAN::0x130同帧非相关信号跳变无异常event")
    def test_caseid_1986606(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=304, no_opera_signal=['PassSeatInAutMovmt'])
        self.partner.ck_no_event(self.partner_key, "SeatSysStatus", timeout=0.2)

    @allure.title("SeatService::SeatSysStatus_BodyCAN::0x299同帧非相关信号跳变无异常event")
    def test_caseid_1986607(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=665, no_opera_signal=['DrvrMassgRunng'])
        self.partner.ck_no_event(self.partner_key, "SeatSysStatus", timeout=0.2)

    @allure.title("SeatService::SeatSysStatus_BodyCAN::0x427同帧非相关信号跳变无异常event")
    def test_caseid_1986605(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1063, no_opera_signal=['PassMassgRunng'])
        self.partner.ck_no_event(self.partner_key, "SeatSysStatus", timeout=0.2)

    @allure.title("SeatService::StartMoveDirection_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986627(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1CarModSts1'])
        self.partner.ck_no_event(self.partner_key, "StartMoveDirection", timeout=0.2)

    @allure.title("SeatService::StartMoveDirection_BodyCAN::0x069同帧非相关信号跳变无异常event")
    def test_caseid_1986629(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=105, no_opera_signal=['DrvrSeatBtnPsd'])
        self.partner.ck_no_event(self.partner_key, "StartMoveDirection", timeout=0.2)

    @allure.title("SeatService::StartMoveDirection_BodyCAN::0x110同帧非相关信号跳变无异常event")
    def test_caseid_1986628(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=272, no_opera_signal=['DrvrSeatExtAdjAllowd'])
        self.partner.ck_no_event(self.partner_key, "StartMoveDirection", timeout=0.2)

    @allure.title("SeatService::StartMoveDirection_BodyCAN::0x130同帧非相关信号跳变无异常event")
    def test_caseid_1986626(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=304, no_opera_signal=['PassSeatBtnPsd'])
        self.partner.ck_no_event(self.partner_key, "StartMoveDirection", timeout=0.2)

    @allure.title("SeatService::StopMoveDirection_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986623(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1CarModSts1'])
        self.partner.ck_no_event(self.partner_key, "StopMoveDirection", timeout=0.2)

    @allure.title("SeatService::StopMoveDirection_BodyCAN::0x069同帧非相关信号跳变无异常event")
    def test_caseid_1986625(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=105, no_opera_signal=['DrvrSeatBtnPsd'])
        self.partner.ck_no_event(self.partner_key, "StopMoveDirection", timeout=0.2)

    @allure.title("SeatService::StopMoveDirection_BodyCAN::0x110同帧非相关信号跳变无异常event")
    def test_caseid_1986624(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=272, no_opera_signal=['DrvrSeatExtAdjAllowd'])
        self.partner.ck_no_event(self.partner_key, "StopMoveDirection", timeout=0.2)

    @allure.title("SeatService::StopMoveDirection_BodyCAN::0x130同帧非相关信号跳变无异常event")
    def test_caseid_1986622(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=304, no_opera_signal=['PassSeatBtnPsd'])
        self.partner.ck_no_event(self.partner_key, "StopMoveDirection", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestSteerWheelServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("SteerWheelService", 'client')])
        self.partner_key = "SteerWheelService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("SteerWheelService::ADASButtonChanged_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986824(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe2SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "ADASButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::ADASButtonChanged_BodyCAN::0x269同帧非相关信号跳变无异常event")
    def test_caseid_1986823(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=617, no_opera_signal=['SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 'SteerWhlScRightButtonLeSteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "ADASButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::ADASButtonChanged_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986822(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlScButtonMidRi2', 'SteerWhlScLeftButtonRi', 'SteerWhlScRightButtonRi'])
        self.partner.ck_no_event(self.partner_key, "ADASButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::ADASComplexButtonChanged_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986837(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe1SteerWhlTouchSwt1'])
        self.partner.ck_no_event(self.partner_key, "ADASComplexButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::ADASComplexButtonChanged_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986836(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlScButtonMidRi1'])
        self.partner.ck_no_event(self.partner_key, "ADASComplexButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::ComplexButtonChanged_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986835(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe1SteerWhlTouchSwt1'])
        self.partner.ck_no_event(self.partner_key, "ComplexButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::ComplexButtonChanged_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986834(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlScButtonMidRi1'])
        self.partner.ck_no_event(self.partner_key, "ComplexButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::Heat_BackboneFR::38-12-64同帧非相关信号跳变无异常event")
    def test_caseid_1986812(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2493504, no_opera_signal=['SteerWhlHeatgLvlSts'])
        self.partner.ck_no_event(self.partner_key, "Heat", timeout=0.2)

    @allure.title("SteerWheelService::NotifyADActivationButttonState_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986825(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe2SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "NotifyADActivationButttonState", timeout=0.2)

    @allure.title("SteerWheelService::NotifySteerWheelHeatTemperature_BackboneFR::40-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986808(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2621456, no_opera_signal=['HSWTRaw'])
        self.partner.ck_no_event(self.partner_key, "NotifySteerWheelHeatTemperature", timeout=0.2)

    @allure.title("SteerWheelService::SimpleButtonChanged_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986821(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe2SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "SimpleButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::SimpleButtonChanged_BodyCAN::0x269同帧非相关信号跳变无异常event")
    def test_caseid_1986820(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=617, no_opera_signal=['SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 'SteerWhlScRightButtonLeSteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "SimpleButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::SimpleButtonChanged_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986819(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlScButtonMidRi1', 'SteerWhlScButtonMidRi2', 'SteerWhlScLeftButtonRi', 'SteerWhlScRightButtonRi'])
        self.partner.ck_no_event(self.partner_key, "SimpleButtonChanged", timeout=0.2)

    @allure.title("SteerWheelService::StalkStatus_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986816(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlTouchSwtLe2SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "StalkStatus", timeout=0.2)

    @allure.title("SteerWheelService::StalkStatus_BodyCAN::0x269同帧非相关信号跳变无异常event")
    def test_caseid_1986818(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=617, no_opera_signal=['SteerWhlTouchSwtLe1SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "StalkStatus", timeout=0.2)

    @allure.title("SteerWheelService::StalkStatus_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986817(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlTouchSwtRi2SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "StalkStatus", timeout=0.2)

    @allure.title("SteerWheelService::SteerHeatAvailiable_ConnectivityCANFD::0x340同帧非相关信号跳变无异常event")
    def test_caseid_1986809(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=832, no_opera_signal=['SteerWhlHeatgAvlSts'])
        self.partner.ck_no_event(self.partner_key, "SteerHeatAvailiable", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986828(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_BackboneFR::47-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986827(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3080193, no_opera_signal=['SteerWhlSnsrQf'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986833(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2', 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_BodyCAN::0x269同帧非相关信号跳变无异常event")
    def test_caseid_1986832(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=617, no_opera_signal=['SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 'SteerWhlScRightButtonLeSteerWhlTouchSwt2', 'SteerWhlTouchSwtLe1SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986831(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlTouchSwtRi2SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_CEM_LIN4::0x1C同帧非相关信号跳变无异常event")
    def test_caseid_1986829(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin4", message=28, no_opera_signal=['WhlFailrSts'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_ChassisCAN1::0x04E同帧非相关信号跳变无异常event")
    def test_caseid_1986830(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=78, no_opera_signal=['PinionSteerAgGroupSteerWhlTq', 'PinionSteerAgGroupSteerWhlTqQf'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelFault_ConnectivityCANFD::0x340同帧非相关信号跳变无异常event")
    def test_caseid_1986826(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=832, no_opera_signal=['SteerWhlHeatgAvlSts'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelFault", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelInfo_BackboneFR::47-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986811(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3080193, no_opera_signal=['SteerWhlSnsrAg', 'SteerWhlSnsrAgSpd', 'SteerWhlSnsrQf'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelInfo", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelL2ButtonSts_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1987162(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlScButtonMidLe1SteerWhlTouchSwt1'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelL2ButtonSts", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelPositionChanged_CEM_LIN4::0x1A同帧非相关信号跳变无异常event")
    def test_caseid_1986813(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin4", message=26, no_opera_signal=['SteerWhlPosnAng', 'SteerWhlPosnX'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelPositionChanged", timeout=0.2)

    @allure.title("SteerWheelService::SteerWheelR2ButtonSts_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1987161(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlScButtonMidRi1'])
        self.partner.ck_no_event(self.partner_key, "SteerWheelR2ButtonSts", timeout=0.2)

    @allure.title("SteerWheelService::StrengthLevel_ChassisCAN1::0x3BB同帧非相关信号跳变无异常event")
    def test_caseid_1986810(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=955, no_opera_signal=['SteerAsscLvlCfmd'])
        self.partner.ck_no_event(self.partner_key, "StrengthLevel", timeout=0.2)

    @allure.title("SteerWheelService::Torque_ChassisCAN1::0x04E同帧非相关信号跳变无异常event")
    def test_caseid_1986815(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=78, no_opera_signal=['PinionSteerAgGroupSteerWhlTq', 'PinionSteerAgGroupSteerWhlTqQf'])
        self.partner.ck_no_event(self.partner_key, "Torque", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestTailGateServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("TailGateService", 'client')])
        self.partner_key = "TailGateService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("TailGateService::NotifyLiftgateSysSts_BodyCAN::0x095同帧非相关信号跳变无异常event")
    def test_caseid_1986363(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=149, no_opera_signal=['TrOpenerSts', 'TrAntiPnch'])
        self.partner.ck_no_event(self.partner_key, "NotifyLiftgateSysSts", timeout=0.2)

    @allure.title("TailGateService::NotifyLiftgateSysSts_BodyCAN::0x242同帧非相关信号跳变无异常event")
    def test_caseid_1986364(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=578, no_opera_signal=['TopPosHmiFeedBack2'])
        self.partner.ck_no_event(self.partner_key, "NotifyLiftgateSysSts", timeout=0.2)

    @allure.title("TailGateService::NotifyTailGateSwitchStatus_BackboneFR::40-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986365(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2621456, no_opera_signal=['TrHndlOutdOpenSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyTailGateSwitchStatus", timeout=0.2)

    @allure.title("TailGateService::NotifyTailGateSwitchStatus_BodyCAN::0x095同帧非相关信号跳变无异常event")
    def test_caseid_1986366(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=149, no_opera_signal=['SwtTrClsSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyTailGateSwitchStatus", timeout=0.2)

    @allure.title("TailGateService::OpenCloseStatus_BodyCAN::0x0E0同帧非相关信号跳变无异常event")
    def test_caseid_1986371(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=224, no_opera_signal=['TrSts'])
        self.partner.ck_no_event(self.partner_key, "OpenCloseStatus", timeout=0.2)

    @allure.title("TailGateService::OpenCloseStatusValidity_BodyCAN::0x0E0同帧非相关信号跳变无异常event")
    def test_caseid_1986362(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=224, no_opera_signal=['TrSts'])
        self.partner.ck_no_event(self.partner_key, "OpenCloseStatusValidity", timeout=0.2)

    @allure.title("TailGateService::Position_BodyCAN::0x242同帧非相关信号跳变无异常event")
    def test_caseid_1986369(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=578, no_opera_signal=['TrOpenPosn'])
        self.partner.ck_no_event(self.partner_key, "Position", timeout=0.2)

    @allure.title("TailGateService::PositionMax_BodyCAN::0x242同帧非相关信号跳变无异常event")
    def test_caseid_1986368(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=578, no_opera_signal=['TopPosHmiFeedBack2'])
        self.partner.ck_no_event(self.partner_key, "PositionMax", timeout=0.2)

    @allure.title("TailGateService::Status_BodyCAN::0x095同帧非相关信号跳变无异常event")
    def test_caseid_1986370(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=149, no_opera_signal=['TrOpenerSts'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("TailGateService::TailGateFault_BodyCAN::0x242同帧非相关信号跳变无异常event")
    def test_caseid_1986367(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=578, no_opera_signal=['TrRelsFailtoHMI'])
        self.partner.ck_no_event(self.partner_key, "TailGateFault", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestTailWingServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("TailWingService", 'client')])
        self.partner_key = "TailWingService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("TailWingService::InitStatus_CEM_LIN6::0x20同帧非相关信号跳变无异常event")
    def test_caseid_1986359(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=32, no_opera_signal=['CalStsAWM'])
        self.partner.ck_no_event(self.partner_key, "InitStatus", timeout=0.2)

    @allure.title("TailWingService::Position_CEM_LIN6::0x20同帧非相关信号跳变无异常event")
    def test_caseid_1986360(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=32, no_opera_signal=['ActvReSplrPosn'])
        self.partner.ck_no_event(self.partner_key, "Position", timeout=0.2)

    @allure.title("TailWingService::Status_CEM_LIN6::0x20同帧非相关信号跳变无异常event")
    def test_caseid_1986361(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=32, no_opera_signal=['ActvReSplrPosn'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestTweeterServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("TweeterService", 'client')])
        self.partner_key = "TweeterService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("TweeterService::SyncStatus_CEM_LIN4::0x0A同帧非相关信号跳变无异常event")
    def test_caseid_1986357(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin4", message=10, no_opera_signal=['RiseorFallSyncStatus'])
        self.partner.ck_no_event(self.partner_key, "SyncStatus", timeout=0.2)

    @allure.title("TweeterService::TweeterStatus_CEM_LIN4::0x0A同帧非相关信号跳变无异常event")
    def test_caseid_1986356(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin4", message=10, no_opera_signal=['LeftElevatorStatus', 'RightElevatorStatus'])
        self.partner.ck_no_event(self.partner_key, "TweeterStatus", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestTyreServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("TyreService", 'client')])
        self.partner_key = "TyreService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("TyreService::AllTyrePressure_BackboneFR::39-3-8同帧非相关信号跳变无异常event")
    def test_caseid_1986354(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556680, no_opera_signal=['LeFrntTireMsgP', 'RiFrntTireMsgP', 'LeReTireMsgP', 'RiReTireMsgP'])
        self.partner.ck_no_event(self.partner_key, "AllTyrePressure", timeout=0.2)

    @allure.title("TyreService::AllTyreTemperature_BackboneFR::39-3-8同帧非相关信号跳变无异常event")
    def test_caseid_1986353(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556680, no_opera_signal=['LeFrntTireMsgT', 'RiFrntTireMsgT', 'LeReTireMsgT', 'RiReTireMsgT'])
        self.partner.ck_no_event(self.partner_key, "AllTyreTemperature", timeout=0.2)

    @allure.title("TyreService::TyreFault_BackboneFR::39-3-8同帧非相关信号跳变无异常event")
    def test_caseid_1986355(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556680, no_opera_signal=['LeFrntTireMsgBattLoSt', 'LeFrntTireMsgFastLoseWarnFlg', 'LeFrntTireMsgMsgOldFlg', 'LeFrntTireMsgPWarnFlg', 'LeFrntTireMsgSysWarnFlg', 'LeFrntTireMsgTWarnFlg', 'RiFrntTireMsgBattLoSt', 'RiFrntTireMsgFastLoseWarnFlg', 'RiFrntTireMsgMsgOldFlg', 'RiFrntTireMsgPWarnFlg', 'RiFrntTireMsgSysWarnFlg', 'RiFrntTireMsgTWarnFlg', 'LeReTireMsgBattLoSt', 'LeReTireMsgFastLoseWarnFlg', 'LeReTireMsgMsgOldFlg', 'LeReTireMsgPWarnFlg', 'LeReTireMsgSysWarnFlg', 'LeReTireMsgTWarnFlg', 'RiReTireMsgBattLoSt', 'RiReTireMsgFastLoseWarnFlg', 'RiReTireMsgMsgOldFlg', 'RiReTireMsgPWarnFlg', 'RiReTireMsgSysWarnFlg', 'RiReTireMsgTWarnFlg'])
        self.partner.ck_no_event(self.partner_key, "TyreFault", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestVehicleModeServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("VehicleModeService", 'client')])
        self.partner_key = "VehicleModeService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("VehicleModeService::CarModeChanged_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986692(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1CarModSts1'])
        self.partner.ck_no_event(self.partner_key, "CarModeChanged", timeout=0.2)

    @allure.title("VehicleModeService::CarModeChangedValidity_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986684(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1CarModSts1'])
        self.partner.ck_no_event(self.partner_key, "CarModeChangedValidity", timeout=0.2)

    @allure.title("VehicleModeService::CarModeDisplayChanged_BackboneFR::39-7-16同帧非相关信号跳变无异常event")
    def test_caseid_1986691(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557712, no_opera_signal=['CarModDispdWdDispd'])
        self.partner.ck_no_event(self.partner_key, "CarModeDisplayChanged", timeout=0.2)

    @allure.title("VehicleModeService::ConvenienceModeDuration_InfoCANFD::0x210同帧非相关信号跳变无异常event")
    def test_caseid_1986680(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=528, no_opera_signal=['PrkgCmftModTiCtrl'])
        self.partner.ck_no_event(self.partner_key, "ConvenienceModeDuration", timeout=0.2)

    @allure.title("VehicleModeService::EnergylevelChanged_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986689(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1EgyLvlElecSubtyp'])
        self.partner.ck_no_event(self.partner_key, "EnergylevelChanged", timeout=0.2)

    @allure.title("VehicleModeService::FastStartStsInfo_ConnectivityCANFD::0x198同帧非相关信号跳变无异常event")
    def test_caseid_1986281(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=408, no_opera_signal=['UsgModChgReqFromBLE'])
        self.partner.ck_no_event(self.partner_key, "FastStartStsInfo", timeout=0.2)

    @allure.title("VehicleModeService::lvRelaySts_BodyCAN::0x430同帧非相关信号跳变无异常event")
    def test_caseid_1986681(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1072, no_opera_signal=['ClimRlyCmd'])
        self.partner.ck_no_event(self.partner_key, "lvRelaySts", timeout=0.2)

    @allure.title("VehicleModeService::lvRelaySts_InfoCANFD::0x190同帧非相关信号跳变无异常event")
    def test_caseid_1986683(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=400, no_opera_signal=['IgnRlyFb'])
        self.partner.ck_no_event(self.partner_key, "lvRelaySts", timeout=0.2)

    @allure.title("VehicleModeService::lvRelaySts_InfoCANFD::0x210同帧非相关信号跳变无异常event")
    def test_caseid_1986682(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=528, no_opera_signal=['FuPmpRlyCmd'])
        self.partner.ck_no_event(self.partner_key, "lvRelaySts", timeout=0.2)

    @allure.title("VehicleModeService::NotifyExhibitionModeSts_PropulsionCAN::0x27C同帧非相关信号跳变无异常event")
    def test_caseid_1986698(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=636, no_opera_signal=['ExhibitionModeStsExhibitionModeSts'])
        self.partner.ck_no_event(self.partner_key, "NotifyExhibitionModeSts", timeout=0.2)

    @allure.title("VehicleModeService::PowerlevelChanged_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986690(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1PwrLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecSubtyp'])
        self.partner.ck_no_event(self.partner_key, "PowerlevelChanged", timeout=0.2)

    @allure.title("VehicleModeService::UsageModeChanged_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986693(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "UsageModeChanged", timeout=0.2)

    @allure.title("VehicleModeService::UsageModeChangedValidity_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986685(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "UsageModeChangedValidity", timeout=0.2)

    @allure.title("VehicleModeService::usageModeRemind_BackboneFR::38-12-64同帧非相关信号跳变无异常event")
    def test_caseid_1986695(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2493504, no_opera_signal=['VehNotParkInfoWarn'])
        self.partner.ck_no_event(self.partner_key, "usageModeRemind", timeout=0.2)

    @allure.title("VehicleModeService::usageModeRemind_BackboneFR::39-1-8同帧非相关信号跳变无异常event")
    def test_caseid_1986696(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556168, no_opera_signal=['StrtMsgToDrvr'])
        self.partner.ck_no_event(self.partner_key, "usageModeRemind", timeout=0.2)

    @allure.title("VehicleModeService::usageModeRemind_BackboneFR::39-7-16同帧非相关信号跳变无异常event")
    def test_caseid_1986697(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557712, no_opera_signal=['KeyNotPrsntMsgToDrvr'])
        self.partner.ck_no_event(self.partner_key, "usageModeRemind", timeout=0.2)

    @allure.title("VehicleModeService::usageModeRemind_BackboneFR::8-2-4同帧非相关信号跳变无异常event")
    def test_caseid_1986694(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524804, no_opera_signal=['AudWarn'])
        self.partner.ck_no_event(self.partner_key, "usageModeRemind", timeout=0.2)

    @allure.title("VehicleModeService::UsageModeRemind_BodyCAN::0x1BF同帧非相关信号跳变无异常event")
    def test_caseid_1986686(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=447, no_opera_signal=['StrtInProgs'])
        self.partner.ck_no_event(self.partner_key, "UsageModeRemind", timeout=0.2)

    @allure.title("VehicleModeService::vehicleModeInfo_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986688(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp', 'VehModMngtGlbSafe1CarModSts1', 'VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 'VehModMngtGlbSafe1FltEgyCnsWdSts', 'VehModMngtGlbSafe1PwrLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecSubtyp'])
        self.partner.ck_no_event(self.partner_key, "vehicleModeInfo", timeout=0.2)

    @allure.title("VehicleModeService::vehicleModeInfo_BackboneFR::39-7-16同帧非相关信号跳变无异常event")
    def test_caseid_1986687(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557712, no_opera_signal=['CarModDispdWdDispd'])
        self.partner.ck_no_event(self.partner_key, "vehicleModeInfo", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestWindowServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("WindowService", 'client')])
        self.partner_key = "WindowService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("WindowService::NotifyRainWinAutoCloseReqSts_InfoCANFD::0x201同帧非相关信号跳变无异常event")
    def test_caseid_1986339(self):
        self.ipdu.filter_special_message_send(bus_name="infocanfd", message=513, no_opera_signal=['WinGlbCmd1'])
        self.partner.ck_no_event(self.partner_key, "NotifyRainWinAutoCloseReqSts", timeout=0.2)

    @allure.title("WindowService::NotifyWindowSwitchStatus_BodyCAN::0x010同帧非相关信号跳变无异常event")
    def test_caseid_1986337(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=16, no_opera_signal=['WinSwtStsAtPass'])
        self.partner.ck_no_event(self.partner_key, "NotifyWindowSwitchStatus", timeout=0.2)

    @allure.title("WindowService::NotifyWindowSwitchStatus_BodyCAN::0x0C0同帧非相关信号跳变无异常event")
    def test_caseid_1986338(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=192, no_opera_signal=['WinSwtReqFrntLe', 'WinSwtReqFrntRi', 'WinSwtReqReLe', 'WinSwtReqReRi'])
        self.partner.ck_no_event(self.partner_key, "NotifyWindowSwitchStatus", timeout=0.2)

    @allure.title("WindowService::NotifyWindowSwitchStatus_BodyCAN::0x203同帧非相关信号跳变无异常event")
    def test_caseid_1986336(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=515, no_opera_signal=['WinSwtStsAtReLe'])
        self.partner.ck_no_event(self.partner_key, "NotifyWindowSwitchStatus", timeout=0.2)

    @allure.title("WindowService::NotifyWindowSwitchStatus_BodyCAN::0x204同帧非相关信号跳变无异常event")
    def test_caseid_1986335(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=516, no_opera_signal=['WinSwtStsAtReRi'])
        self.partner.ck_no_event(self.partner_key, "NotifyWindowSwitchStatus", timeout=0.2)

    @allure.title("WindowService::Status_BodyCAN::0x005同帧非相关信号跳变无异常event")
    def test_caseid_1986352(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=5, no_opera_signal=['WinPosnStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("WindowService::Status_BodyCAN::0x010同帧非相关信号跳变无异常event")
    def test_caseid_1986351(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=16, no_opera_signal=['WinPosnStsAtPass', 'WinSwtStsAtPass'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("WindowService::Status_BodyCAN::0x070同帧非相关信号跳变无异常event")
    def test_caseid_1986350(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=112, no_opera_signal=['WinPosnStsAtReLe'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("WindowService::Status_BodyCAN::0x075同帧非相关信号跳变无异常event")
    def test_caseid_1986349(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=117, no_opera_signal=['WinPosnStsAtReRi'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("WindowService::Status_BodyCAN::0x203同帧非相关信号跳变无异常event")
    def test_caseid_1986348(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=515, no_opera_signal=['WinSwtStsAtReLe'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("WindowService::Status_BodyCAN::0x204同帧非相关信号跳变无异常event")
    def test_caseid_1986347(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=516, no_opera_signal=['WinSwtStsAtReRi'])
        self.partner.ck_no_event(self.partner_key, "Status", timeout=0.2)

    @allure.title("WindowService::WindowFault_BodyCAN::0x030同帧非相关信号跳变无异常event")
    def test_caseid_1986346(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=48, no_opera_signal=['WinFailrStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "WindowFault", timeout=0.2)

    @allure.title("WindowService::WindowFault_BodyCAN::0x070同帧非相关信号跳变无异常event")
    def test_caseid_1986344(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=112, no_opera_signal=['WinFailrStsAtReLe'])
        self.partner.ck_no_event(self.partner_key, "WindowFault", timeout=0.2)

    @allure.title("WindowService::WindowFault_BodyCAN::0x075同帧非相关信号跳变无异常event")
    def test_caseid_1986343(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=117, no_opera_signal=['WinFailrStsAtReRi'])
        self.partner.ck_no_event(self.partner_key, "WindowFault", timeout=0.2)

    @allure.title("WindowService::WindowFault_BodyCAN::0x123同帧非相关信号跳变无异常event")
    def test_caseid_1986342(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=291, no_opera_signal=['WinThermlStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "WindowFault", timeout=0.2)

    @allure.title("WindowService::WindowFault_BodyCAN::0x125同帧非相关信号跳变无异常event")
    def test_caseid_1986345(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=293, no_opera_signal=['WinFailrStsAtPass', 'WinThermlStsAtPass'])
        self.partner.ck_no_event(self.partner_key, "WindowFault", timeout=0.2)

    @allure.title("WindowService::WindowFault_BodyCAN::0x203同帧非相关信号跳变无异常event")
    def test_caseid_1986341(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=515, no_opera_signal=['WinThermlStsAtReLe'])
        self.partner.ck_no_event(self.partner_key, "WindowFault", timeout=0.2)

    @allure.title("WindowService::WindowFault_BodyCAN::0x204同帧非相关信号跳变无异常event")
    def test_caseid_1986340(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=516, no_opera_signal=['WinThermlStsAtReRi'])
        self.partner.ck_no_event(self.partner_key, "WindowFault", timeout=0.2)

    @allure.title("WindowService::WindowPosition_BodyCAN::0x005同帧非相关信号跳变无异常event")
    def test_caseid_1986334(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=5, no_opera_signal=['WinPosnStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "WindowPosition", timeout=0.2)

    @allure.title("WindowService::WindowPosition_BodyCAN::0x010同帧非相关信号跳变无异常event")
    def test_caseid_1986333(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=16, no_opera_signal=['WinPosnStsAtPass'])
        self.partner.ck_no_event(self.partner_key, "WindowPosition", timeout=0.2)

    @allure.title("WindowService::WindowPosition_BodyCAN::0x070同帧非相关信号跳变无异常event")
    def test_caseid_1986332(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=112, no_opera_signal=['WinPosnStsAtReLe'])
        self.partner.ck_no_event(self.partner_key, "WindowPosition", timeout=0.2)

    @allure.title("WindowService::WindowPosition_BodyCAN::0x075同帧非相关信号跳变无异常event")
    def test_caseid_1986331(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=117, no_opera_signal=['WinPosnStsAtReRi'])
        self.partner.ck_no_event(self.partner_key, "WindowPosition", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestWiperServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("WiperService", 'client')])
        self.partner_key = "WiperService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("WiperService::DayNightStatus_BodyCAN::0x040同帧非相关信号跳变无异常event")
    def test_caseid_1986312(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=64, no_opera_signal=['TwliBriSts'])
        self.partner.ck_no_event(self.partner_key, "DayNightStatus", timeout=0.2)

    @allure.title("WiperService::HumidityInfo_BodyCAN::0x100同帧非相关信号跳变无异常event")
    def test_caseid_1986318(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=256, no_opera_signal=['RelHumSnsrQf'])
        self.partner.ck_no_event(self.partner_key, "HumidityInfo", timeout=0.2)

    @allure.title("WiperService::HumidityInfo_BodyCAN::0x12C同帧非相关信号跳变无异常event")
    def test_caseid_1986319(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=300, no_opera_signal=['CmptmtRelHum'])
        self.partner.ck_no_event(self.partner_key, "HumidityInfo", timeout=0.2)

    @allure.title("WiperService::LightLux_CEM_LIN1::0x15同帧非相关信号跳变无异常event")
    def test_caseid_1986324(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=21, no_opera_signal=['TwliBriRawTwliBriRaw', 'TwliBriRawQf'])
        self.partner.ck_no_event(self.partner_key, "LightLux", timeout=0.2)

    @allure.title("WiperService::MaintainceMode_BackboneFR::39-15-32同帧非相关信号跳变无异常event")
    def test_caseid_1986325(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2559776, no_opera_signal=['WiprInPosnForSrv'])
        self.partner.ck_no_event(self.partner_key, "MaintainceMode", timeout=0.2)

    @allure.title("WiperService::Mode_BackboneFR::39-1-8同帧非相关信号跳变无异常event")
    def test_caseid_1986329(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556168, no_opera_signal=['WipgInfoWipgSpdInfo', 'RainSensActvn'])
        self.partner.ck_no_event(self.partner_key, "Mode", timeout=0.2)

    @allure.title("WiperService::Mode_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986328(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlTouchSwtRi3'])
        self.partner.ck_no_event(self.partner_key, "Mode", timeout=0.2)

    @allure.title("WiperService::Mode_CEM_LIN1::0x05同帧非相关信号跳变无异常event")
    def test_caseid_1986327(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=5, no_opera_signal=['WiprMotFrntLvrCmdSafeLvrInSnglStrokePos'])
        self.partner.ck_no_event(self.partner_key, "Mode", timeout=0.2)

    @allure.title("WiperService::NotifyWiperAutoMode_BackboneFR::39-1-8同帧非相关信号跳变无异常event")
    def test_caseid_1986316(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556168, no_opera_signal=['RainSensActvn'])
        self.partner.ck_no_event(self.partner_key, "NotifyWiperAutoMode", timeout=0.2)

    @allure.title("WiperService::NotifyWiperAutoMode_CEM_LIN1::0x15同帧非相关信号跳变无异常event")
    def test_caseid_1986315(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=21, no_opera_signal=['WipgAutFrntMod'])
        self.partner.ck_no_event(self.partner_key, "NotifyWiperAutoMode", timeout=0.2)

    @allure.title("WiperService::NotifyWiperPosition_CEM_LIN1::0x27同帧非相关信号跳变无异常event")
    def test_caseid_1986314(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=39, no_opera_signal=['WiprInPrkgPosnLo', 'WiprInWipgAr'])
        self.partner.ck_no_event(self.partner_key, "NotifyWiperPosition", timeout=0.2)

    @allure.title("WiperService::Rainlevel_CEM_LIN1::0x02同帧非相关信号跳变无异常event")
    def test_caseid_1986323(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=2, no_opera_signal=['RainfallAmnt'])
        self.partner.ck_no_event(self.partner_key, "Rainlevel", timeout=0.2)

    @allure.title("WiperService::RainStatusRestricted_CEM_LIN1::0x02同帧非相关信号跳变无异常event")
    def test_caseid_1986311(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=2, no_opera_signal=['RainDetected'])
        self.partner.ck_no_event(self.partner_key, "RainStatusRestricted", timeout=0.2)

    @allure.title("WiperService::SolarValue_CEM_LIN1::0x02同帧非相关信号跳变无异常event")
    def test_caseid_1986310(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=2, no_opera_signal=['SolarSnsrLeValue', 'SolarSnsrRiValue'])
        self.partner.ck_no_event(self.partner_key, "SolarValue", timeout=0.2)

    @allure.title("WiperService::SparyWashing_CEM_LIN1::0x05同帧非相关信号跳变无异常event")
    def test_caseid_1986326(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=5, no_opera_signal=['WshrLvrPosnSafe'])
        self.partner.ck_no_event(self.partner_key, "SparyWashing", timeout=0.2)

    @allure.title("WiperService::SwitchStatus_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986317(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlTouchSwtRi3'])
        self.partner.ck_no_event(self.partner_key, "SwitchStatus", timeout=0.2)

    @allure.title("WiperService::WiperFault_BackboneFR::38-12-64同帧非相关信号跳变无异常event")
    def test_caseid_1986322(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2493504, no_opera_signal=['RainSnsrActvnErrToHmi'])
        self.partner.ck_no_event(self.partner_key, "WiperFault", timeout=0.2)

    @allure.title("WiperService::WiperFault_BackboneFR::38-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986321(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2492480, no_opera_signal=['WiprSysFailrDetdSafe', 'WiprSysFailrDetdSafe', 'WshrFldTankStsToHMI'])
        self.partner.ck_no_event(self.partner_key, "WiperFault", timeout=0.2)

    @allure.title("WiperService::WiperFault_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986320(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlTouchSwtRi3'])
        self.partner.ck_no_event(self.partner_key, "WiperFault", timeout=0.2)

    @allure.title("WiperService::WiperOneshotSts_CEM_LIN1::0x05同帧非相关信号跳变无异常event")
    def test_caseid_1986330(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin1", message=5, no_opera_signal=['WiprMotFrntLvrCmdSafeLvrInSnglStrokePos'])
        self.partner.ck_no_event(self.partner_key, "WiperOneshotSts", timeout=0.2)

    @allure.title("WiperService::WiperWashFluidLowStatus_BackboneFR::38-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986313(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2492480, no_opera_signal=['WshrFldTankStsToHMI'])
        self.partner.ck_no_event(self.partner_key, "WiperWashFluidLowStatus", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestWirelessPhoneChargingServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("WirelessPhoneChargingService", 'client')])
        self.partner_key = "WirelessPhoneChargingService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("WirelessPhoneChargingService::ChargingFault_ConnectivityCANFD::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986305(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=769, no_opera_signal=['WPCModuleSts'])
        self.partner.ck_no_event(self.partner_key, "ChargingFault", timeout=0.2)

    @allure.title("WirelessPhoneChargingService::ChargingStatus_ConnectivityCANFD::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986307(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=769, no_opera_signal=['WPCModuleSts'])
        self.partner.ck_no_event(self.partner_key, "ChargingStatus", timeout=0.2)

    @allure.title("WirelessPhoneChargingService::PhoneForgottenRemindInfo_ConnectivityCANFD::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986306(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=769, no_opera_signal=['PhoneForgottenRmn'])
        self.partner.ck_no_event(self.partner_key, "PhoneForgottenRemindInfo", timeout=0.2)

    @allure.title("WirelessPhoneChargingService::WirelessChargingInfo_ConnectivityCANFD::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986304(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=769, no_opera_signal=['PhoneForgottenRmn', 'WPCCtrlRes', 'WPCModuleSts', 'WPCFailureSts'])
        self.partner.ck_no_event(self.partner_key, "WirelessChargingInfo", timeout=0.2)

    @allure.title("WirelessPhoneChargingService::WirelessChargingInfo_ConnectivityCANFD::0x303同帧非相关信号跳变无异常event")
    def test_caseid_1986303(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=771, no_opera_signal=['PhoneForgottenRmnPass', 'WPCCtrlResPass', 'WPCModuleStsPass', 'WPCFailureStsPass'])
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=769, no_opera_signal=['PhoneForgottenRmn', 'WPCCtrlRes', 'WPCModuleSts', 'WPCFailureSts'])
        self.partner.ck_no_event(self.partner_key, "WirelessChargingInfo", timeout=0.2)

    @allure.title("WirelessPhoneChargingService::WirelessPhoneCharging_ConnectivityCANFD::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986308(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=769, no_opera_signal=['WPCCtrlRes'])
        self.partner.ck_no_event(self.partner_key, "WirelessPhoneCharging", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestWTIAutoDriveServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("WTIAutoDriveService", 'client')])
        self.partner_key = "WTIAutoDriveService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("WTIAutoDriveService::WarningMsgList_ADCANFD::0x185同帧非相关信号跳变无异常event")
    def test_caseid_1986296(self):
        self.ipdu.filter_special_message_send(bus_name="adcanfd", message=389, no_opera_signal=['InsdSnsrFltFrntShoLe', 'InsdSnsrFltFrntShoRi', 'InsdSnsrFltReShoLe', 'InsdSnsrFltReShoRi', 'OutdSnsrFltFrntShoLe', 'OutdSnsrFltFrntShoRi', 'OutdSnsrFltReShoLe', 'OutdSnsrFltReShoRi', 'SnsrFltFrntShoSideLe', 'SnsrFltFrntShoSideRi', 'SnsrFltReShoSideLe', 'SnsrFltReShoSideRi'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/信号跳变校验event事件场景")
class TestWTIServiceSignalJumpMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip='172.16.5.21')
        self.partner = S2sBaseClass([("WTIService", 'client')])
        self.partner_key = "WTIService" + '_client'
        time.sleep(8)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.stop_special_message_send()
        super().after_each_func(ecu)

    @allure.title("WTIService::TelltaleList_BackboneFR::12-6-64同帧非相关信号跳变无异常event")
    def test_caseid_1986711(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=788032, no_opera_signal=['RestrntSysLampReq'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::20-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986700(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1310721, no_opera_signal=['BltLockStAtDrvrBltLockSt1'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::32-3-8同帧非相关信号跳变无异常event")
    def test_caseid_1986699(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2097928, no_opera_signal=['SmartAutoHldCtrlSts'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986708(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['ExtrLtgStsLoBeam', 'ExtrLtgStsHiBeam', 'ExtrLtgStsPosLiFrnt', 'ExtrLtgStsPosLiRe', 'ExtrLtgStsReFog', 'ExtrLtgStsFlash', 'VehModMngtGlbSafe1UsgModSts'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::39-15-32同帧非相关信号跳变无异常event")
    def test_caseid_1986701(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2559776, no_opera_signal=['RlyPwrDistbnCmd1WdIgnRlyExtCmd'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::39-2-8同帧非相关信号跳变无异常event")
    def test_caseid_1986715(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556424, no_opera_signal=['ULoWarnULoWarn'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::39-3-8同帧非相关信号跳变无异常event")
    def test_caseid_1986706(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556680, no_opera_signal=['LeFrntTireMsgPWarnFlg', 'LeFrntTireMsgSysWarnFlg', 'RiFrntTireMsgPWarnFlg', 'RiFrntTireMsgSysWarnFlg', 'LeReTireMsgPWarnFlg', 'LeReTireMsgSysWarnFlg', 'RiReTireMsgPWarnFlg', 'RiReTireMsgSysWarnFlg'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::49-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986705(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3211280, no_opera_signal=['HvBattCellTInfoHvBattTMin'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::56-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986712(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3670274, no_opera_signal=['EscStEscSt'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986714(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['DrvModEscOffDrvModEscOff', 'BrkAndAbsWarnIndcnReqAbsWarnIndcnReq', 'BrkAndAbsWarnIndcnReqBrkWarnIndcnReq', 'AutHldSoftSwtEnaSts'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::57-5-8同帧非相关信号跳变无异常event")
    def test_caseid_1986713(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3736840, no_opera_signal=['EscWarnIndcnReqEscWarnIndcnReq', 'MsgReqByHillDwnCtrl'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::57-7-32同帧非相关信号跳变无异常event")
    def test_caseid_1986704(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3737376, no_opera_signal=['LampReqByVehHld'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986707(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['IndcrDisp', 'LVPwrSplyErrSts', 'DoorDrvrStsWithFacQlyDoorSts', 'DoorDrvrStsWithFacQlyFacQly'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_ChassisCAN1::0x1BC同帧非相关信号跳变无异常event")
    def test_caseid_1986710(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=444, no_opera_signal=['SteerErrReq'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_ChassisCAN1::0x2C4同帧非相关信号跳变无异常event")
    def test_caseid_1986709(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=708, no_opera_signal=['CrpModAct'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_PropulsionCAN::0x04B同帧非相关信号跳变无异常event")
    def test_caseid_1986703(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=75, no_opera_signal=['GearLvrIndcn'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::TelltaleList_PropulsionCAN::0x143同帧非相关信号跳变无异常event")
    def test_caseid_1986702(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=323, no_opera_signal=['DCChrgnHndlSts'])
        self.partner.ck_no_event(self.partner_key, "TelltaleList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::12-6-64同帧非相关信号跳变无异常event")
    def test_caseid_1986773(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=788032, no_opera_signal=['RestrntSysMsgReq', 'PedProtnMsgReqForFlt', 'PedProtnMsgReqForImpct'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::17-1-2同帧非相关信号跳变无异常event")
    def test_caseid_1986755(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=1114370, no_opera_signal=['VehSpdIndcdVehSpdIndcd', 'VehSpdIndcdVeSpdIndcdUnit'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::36-0-1同帧非相关信号跳变无异常event")
    def test_caseid_1986774(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2359297, no_opera_signal=['ExtrLtgStsAHL', 'ExtrLtgStsLoBeam', 'ExtrLtgStsHiBeam', 'ExtrLtgStsFlash', 'ExtrLtgStsReverseLi', 'ExtrLtgStsPosLiFrnt', 'ExtrLtgStsPosLiRe', 'ExtrLtgStsReFog', 'ExtrLtgStsTurnIndrLe', 'ExtrLtgStsTurnIndrRi', 'VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecMai'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::38-12-64同帧非相关信号跳变无异常event")
    def test_caseid_1986767(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2493504, no_opera_signal=['ChrgLidRearFltSts', 'VehNotParkInfoWarn', 'RainSnsrActvnErrToHmi'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::38-8-64同帧非相关信号跳变无异常event")
    def test_caseid_1986759(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2492480, no_opera_signal=['AlrmStsAlrmSt', 'WshrFldTankStsToHMI', 'WiprSysFailrDetdSafe'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::39-15-32同帧非相关信号跳变无异常event")
    def test_caseid_1986754(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2559776, no_opera_signal=['WiprInPosnForSrv'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::39-1-8同帧非相关信号跳变无异常event")
    def test_caseid_1986761(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556168, no_opera_signal=['StrtMsgToDrvr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::39-2-8同帧非相关信号跳变无异常event")
    def test_caseid_1986777(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556424, no_opera_signal=['ULoWarnULoWarn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::39-3-8同帧非相关信号跳变无异常event")
    def test_caseid_1986772(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2556680, no_opera_signal=['LeFrntTireMsgPWarnFlg', 'RiFrntTireMsgPWarnFlg', 'LeReTireMsgPWarnFlg', 'RiReTireMsgPWarnFlg', 'LeFrntTireMsgTWarnFlg', 'RiFrntTireMsgTWarnFlg', 'LeReTireMsgTWarnFlg', 'RiReTireMsgTWarnFlg', 'LeFrntTireMsgFastLoseWarnFlg', 'RiFrntTireMsgFastLoseWarnFlg', 'LeReTireMsgFastLoseWarnFlg', 'RiReTireMsgFastLoseWarnFlg', 'LeFrntTireMsgBattLoSt', 'RiFrntTireMsgBattLoSt', 'LeReTireMsgBattLoSt', 'RiReTireMsgBattLoSt', 'LeFrntTireMsgSysWarnFlg', 'RiFrntTireMsgSysWarnFlg', 'LeReTireMsgSysWarnFlg', 'RiReTireMsgSysWarnFlg', 'ChrgLidRearSts', 'LeFrntTireMsgP', 'RiFrntTireMsgP', 'LeReTireMsgP', 'RiReTireMsgP'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::39-7-16同帧非相关信号跳变无异常event")
    def test_caseid_1986762(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2557712, no_opera_signal=['KeyNotPrsntMsgToDrvr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::40-0-16同帧非相关信号跳变无异常event")
    def test_caseid_1986740(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=2621456, no_opera_signal=['Flash2HighBeamFailFlag', 'DoorDrvrOpenReqInsdLogic', 'DoorLeReOpenReqInsdLogic', 'DoorPassOpenReqInsdLogic', 'DoorRiReOpenReqInsdLogic'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::49-4-16同帧非相关信号跳变无异常event")
    def test_caseid_1986764(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3212304, no_opera_signal=['EgyRgnLvlAct'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BackboneFR::57-23-64同帧非相关信号跳变无异常event")
    def test_caseid_1986763(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=3741504, no_opera_signal=['BrkFldLvl', 'BrkMsgWarnReq', 'DispMsgByVehHld', 'BrkRelsWarnReq', 'EpbLampReqEpbLampReq'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)
        
    @allure.title("WTIService::WarningMsgList_BackboneFR::8-1-4同帧非相关信号跳变无异常event")
    def test_caseid_1986775(self):
        self.ipdu.filter_special_message_send(bus_name="backbonefr", message=524548, no_opera_signal=['LVPwrSplyErrSts', 'HoodSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x030同帧非相关信号跳变无异常event")
    def test_caseid_1986753(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=48, no_opera_signal=['WinFailrStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x040同帧非相关信号跳变无异常event")
    def test_caseid_1986757(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=64, no_opera_signal=['DoorDrvrSts', 'DoorLeReSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x070同帧非相关信号跳变无异常event")
    def test_caseid_1986751(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=112, no_opera_signal=['WinFailrStsAtReLe'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x075同帧非相关信号跳变无异常event")
    def test_caseid_1986750(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=117, no_opera_signal=['WinFailrStsAtReRi'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x0E0同帧非相关信号跳变无异常event")
    def test_caseid_1986756(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=224, no_opera_signal=['DoorPassSts', 'DoorRiReSts', 'TrSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x123同帧非相关信号跳变无异常event")
    def test_caseid_1986733(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=291, no_opera_signal=['DrvrMirrorFoldErrorFb', 'DrvrMirrorAdjErrorFb', 'WinThermlStsAtDrvr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x125同帧非相关信号跳变无异常event")
    def test_caseid_1986752(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=293, no_opera_signal=['WinThermlStsAtPass', 'WinFailrStsAtPass', 'PassMirrorFoldErrorFb', 'PassMirrorAdjErrorFb'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x140同帧非相关信号跳变无异常event")
    def test_caseid_1986724(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=320, no_opera_signal=['HmiHvacFanLvlFrnt'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x1BF同帧非相关信号跳变无异常event")
    def test_caseid_1986760(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=447, no_opera_signal=['StrtInProgs'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x217同帧非相关信号跳变无异常event")
    def test_caseid_1986744(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=535, no_opera_signal=['DtcInfDoorDrvrBoolean1','DtcInfDoorDrvrBoolean2','DtcInfDoorDrvrBoolean3','DtcInfDoorDrvrBoolean4','DtcInfDoorDrvrBoolean5'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x218同帧非相关信号跳变无异常event")
    def test_caseid_1986742(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=536, no_opera_signal=['DtcInfDoorLeReBoolean1','DtcInfDoorLeReBoolean2','DtcInfDoorLeReBoolean3','DtcInfDoorLeReBoolean4','DtcInfDoorLeReBoolean5'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x222同帧非相关信号跳变无异常event")
    def test_caseid_1986743(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=546, no_opera_signal=['DtcInfDoorPassBoolean1','DtcInfDoorPassBoolean2','DtcInfDoorPassBoolean3','DtcInfDoorPassBoolean4','DtcInfDoorPassBoolean5'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x22A同帧非相关信号跳变无异常event")
    def test_caseid_1986741(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=554, no_opera_signal=['DtcInfDoorRiReBoolean1','DtcInfDoorRiReBoolean2','DtcInfDoorRiReBoolean3','DtcInfDoorRiReBoolean4','DtcInfDoorRiReBoolean5'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x242同帧非相关信号跳变无异常event")
    def test_caseid_1986738(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=578, no_opera_signal=['TrRelsFailtoHMI'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x268同帧非相关信号跳变无异常event")
    def test_caseid_1986739(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=616, no_opera_signal=['SteerWhlTouchSwtLe3'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x271同帧非相关信号跳变无异常event")
    def test_caseid_1986779(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=625, no_opera_signal=['SteerWhlTouchSwtRi1SteerWhlTouchSwt2'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x299同帧非相关信号跳变无异常event")
    def test_caseid_1986746(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=665, no_opera_signal=['DrvrSeatHeatgAvlSts', 'DrvrSeatVentAvlSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986727(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=769, no_opera_signal=['HvacRecFlapActrErr', 'HvacModFlapActrErrFrstRowLe', 'HvacModFlapActrErrFrstRowRi'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x302同帧非相关信号跳变无异常event")
    def test_caseid_1986732(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=770, no_opera_signal=['VentnActr01BlckSts', 'VentnActr01ElecErr', 'VentnActr02BlckSts', 'VentnActr02ElecErr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x303同帧非相关信号跳变无异常event")
    def test_caseid_1986731(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=771, no_opera_signal=['VentnActr03BlckSts', 'VentnActr03ElecErr', 'VentnActr04BlckSts', 'VentnActr04ElecErr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x304同帧非相关信号跳变无异常event")
    def test_caseid_1986730(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=772, no_opera_signal=['VentnActr05BlckSts', 'VentnActr05ElecErr', 'VentnActr06BlckSts', 'VentnActr06ElecErr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x305同帧非相关信号跳变无异常event")
    def test_caseid_1986729(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=773, no_opera_signal=['VentnActr07BlckSts', 'VentnActr07ElecErr', 'VentnActr08BlckSts', 'VentnActr08ElecErr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x306同帧非相关信号跳变无异常event")
    def test_caseid_1986728(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=774, no_opera_signal=['VentnActr09BlckSts', 'VentnActr09ElecErr', 'VentnActr10BlckSts', 'VentnActr10ElecErr'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x320同帧非相关信号跳变无异常event")
    def test_caseid_1986719(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=800, no_opera_signal=['IPMLVPwrSplyErrSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x385同帧非相关信号跳变无异常event")
    def test_caseid_1986717(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=901, no_opera_signal=['SeatHeatgAvlStsRowSecLe', 'SeatHeatgAvlStsRowSecRi'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x386同帧非相关信号跳变无异常event")
    def test_caseid_1986716(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=902, no_opera_signal=['SeatVentAvlStsRowSecLe', 'SeatVentAvlStsRowSecRi'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x419同帧非相关信号跳变无异常event")
    def test_caseid_1986726(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1049, no_opera_signal=['IntPm25StsFrmClima', 'FragStsFrmClima'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x427同帧非相关信号跳变无异常event")
    def test_caseid_1986745(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1063, no_opera_signal=['PassSeatHeatgAvlSts', 'PassSeatVentAvlSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_BodyCAN::0x4A0同帧非相关信号跳变无异常event")
    def test_caseid_1986725(self):
        self.ipdu.filter_special_message_send(bus_name="bodycan", message=1184, no_opera_signal=['OutdAirQlyQf'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_CEM_LIN6::0x20同帧非相关信号跳变无异常event")
    def test_caseid_1986749(self):
        self.ipdu.filter_special_message_send(bus_name="cem_lin6", message=32, no_opera_signal=['ActvReSplrPosn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN1::0x1BC同帧非相关信号跳变无异常event")
    def test_caseid_1986776(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=444, no_opera_signal=['SteerErrReq'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN1::0x22A同帧非相关信号跳变无异常event")
    def test_caseid_1986722(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=554, no_opera_signal=['CmprFbCmprSts2'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN1::0x278同帧非相关信号跳变无异常event")
    def test_caseid_1986718(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=632, no_opera_signal=['GrlShttrStsShttrBlkd'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN1::0x2C4同帧非相关信号跳变无异常event")
    def test_caseid_1986765(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=708, no_opera_signal=['GearLvrLockIndcn', 'GearLvrFaultIndcn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN1::0x367同帧非相关信号跳变无异常event")
    def test_caseid_1986723(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=871, no_opera_signal=['HvCooltHeatrWarnSigFltInCom', 'HvCooltHeatrWarnSigFltPrsnt'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN1::0x46F同帧非相关信号跳变无异常event")
    def test_caseid_1986720(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan1", message=1135, no_opera_signal=['BattCooltIndcnReq'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN2::0x102同帧非相关信号跳变无异常event")
    def test_caseid_1986280(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=258, no_opera_signal=['BrkPedlTrvlAct'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN2::0x1E0同帧非相关信号跳变无异常event")
    def test_caseid_1986279(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=480, no_opera_signal=['RoadInclnRoadIncln'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN2::0x200同帧非相关信号跳变无异常event")
    def test_caseid_1986721(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=512, no_opera_signal=['EmotCooltIndcnReq', 'DchaStopByTarDrvrIndcn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ChassisCAN2::0x233同帧非相关信号跳变无异常event")
    def test_caseid_1986766(self):
        self.ipdu.filter_special_message_send(bus_name="chassiscan2", message=563, no_opera_signal=['DrvPfmncRedn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ConnectivityCANFD::0x244同帧非相关信号跳变无异常event")
    def test_caseid_1986737(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=580, no_opera_signal=['DigKeyConnectInfo1KeyConnectSts', 'DigKeyConnectInfo1KeyIdByte0', 'DigKeyConnectInfo1KeyIdByte1', 'DigKeyConnectInfo1KeyIdByte2', 'DigKeyConnectInfo1KeyIdByte3', 'DigKeyConnectInfo1KeyIdByte4', 'DigKeyConnectInfo1KeyIdByte5', 'DigKeyConnectInfo1KeyIdByte6', 'DigKeyConnectInfo1KeyIdByte7', 'DigKeyConnectInfo1KeyIdByte8', 'DigKeyConnectInfo1KeyIdByte9', 'DigKeyConnectInfo1KeyIdByte10', 'DigKeyConnectInfo1KeyIdByte11', 'DigKeyConnectInfo1KeyIdByte12', 'DigKeyConnectInfo1KeyIdByte13', 'DigKeyConnectInfo1KeyIdByte14', 'DigKeyConnectInfo1KeyIdByte15', 'DigKeyConnectInfo1KeyPrsntZone', 'DigKeyConnectInfo1KeyTyp', 'DigKeyConnectInfo1BattWarn', 'DigKeyConnectInfo2KeyConnectSts', 'DigKeyConnectInfo2KeyIdByte0', 'DigKeyConnectInfo2KeyIdByte1', 'DigKeyConnectInfo2KeyIdByte2', 'DigKeyConnectInfo2KeyIdByte3', 'DigKeyConnectInfo2KeyIdByte4', 'DigKeyConnectInfo2KeyIdByte5', 'DigKeyConnectInfo2KeyIdByte6', 'DigKeyConnectInfo2KeyIdByte7', 'DigKeyConnectInfo2KeyIdByte8', 'DigKeyConnectInfo2KeyIdByte9', 'DigKeyConnectInfo2KeyIdByte10', 'DigKeyConnectInfo2KeyIdByte11', 'DigKeyConnectInfo2KeyIdByte12', 'DigKeyConnectInfo2KeyIdByte13', 'DigKeyConnectInfo2KeyIdByte14', 'DigKeyConnectInfo2KeyIdByte15', 'DigKeyConnectInfo2KeyPrsntZone', 'DigKeyConnectInfo2KeyTyp', 'DigKeyConnectInfo2BattWarn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ConnectivityCANFD::0x245同帧非相关信号跳变无异常event")
    def test_caseid_1986734(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=581, no_opera_signal=['DigKeyConnectInfo3KeyConnectSts', 'DigKeyConnectInfo3KeyIdByte0', 'DigKeyConnectInfo3KeyIdByte1', 'DigKeyConnectInfo3KeyIdByte2', 'DigKeyConnectInfo3KeyIdByte3', 'DigKeyConnectInfo3KeyIdByte4', 'DigKeyConnectInfo3KeyIdByte5', 'DigKeyConnectInfo3KeyIdByte6', 'DigKeyConnectInfo3KeyIdByte7', 'DigKeyConnectInfo3KeyIdByte8', 'DigKeyConnectInfo3KeyIdByte9', 'DigKeyConnectInfo3KeyIdByte10', 'DigKeyConnectInfo3KeyIdByte11', 'DigKeyConnectInfo3KeyIdByte12', 'DigKeyConnectInfo3KeyIdByte13', 'DigKeyConnectInfo3KeyIdByte14', 'DigKeyConnectInfo3KeyIdByte15', 'DigKeyConnectInfo3KeyPrsntZone', 'DigKeyConnectInfo3KeyTyp', 'DigKeyConnectInfo3BattWarn', 'DigKeyConnectInfo4KeyConnectSts', 'DigKeyConnectInfo4KeyIdByte0', 'DigKeyConnectInfo4KeyIdByte1', 'DigKeyConnectInfo4KeyIdByte2', 'DigKeyConnectInfo4KeyIdByte3', 'DigKeyConnectInfo4KeyIdByte4', 'DigKeyConnectInfo4KeyIdByte5', 'DigKeyConnectInfo4KeyIdByte6', 'DigKeyConnectInfo4KeyIdByte7', 'DigKeyConnectInfo4KeyIdByte8', 'DigKeyConnectInfo4KeyIdByte9', 'DigKeyConnectInfo4KeyIdByte10', 'DigKeyConnectInfo4KeyIdByte11', 'DigKeyConnectInfo4KeyIdByte12', 'DigKeyConnectInfo4KeyIdByte13', 'DigKeyConnectInfo4KeyIdByte14', 'DigKeyConnectInfo4KeyIdByte15', 'DigKeyConnectInfo4KeyPrsntZone', 'DigKeyConnectInfo4KeyTyp', 'DigKeyConnectInfo4BattWarn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ConnectivityCANFD::0x301同帧非相关信号跳变无异常event")
    def test_caseid_1986748(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=769, no_opera_signal=['WPCModuleSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ConnectivityCANFD::0x340同帧非相关信号跳变无异常event")
    def test_caseid_1986747(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=832, no_opera_signal=['SteerWhlHeatgAvlSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_ConnectivityCANFD::0x3A0同帧非相关信号跳变无异常event")
    def test_caseid_1986735(self):
        self.ipdu.filter_special_message_send(bus_name="connectivitycanfd", message=928, no_opera_signal=['WPCWarnSts', 'BNCMWarnSts', 'NKRWarnSts', 'BKAWarnSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_PropulsionCAN::0x04B同帧非相关信号跳变无异常event")
    def test_caseid_1986758(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=75, no_opera_signal=['GearLvrIndcn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_PropulsionCAN::0x135同帧非相关信号跳变无异常event")
    def test_caseid_1986736(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=309, no_opera_signal=['GearLvrIllmnSts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_PropulsionCAN::0x142同帧非相关信号跳变无异常event")
    def test_caseid_1986770(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=322, no_opera_signal=['HvBattLimnIndcn'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_PropulsionCAN::0x155同帧非相关信号跳变无异常event")
    def test_caseid_1986778(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=341, no_opera_signal=['TrsmParkLockdTrsmParkLockd'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_PropulsionCAN::0x295同帧非相关信号跳变无异常event")
    def test_caseid_1986768(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=661, no_opera_signal=['HVIL1Sts', 'HVIL2Sts', 'HVIL3Sts'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_PropulsionCAN::0x331同帧非相关信号跳变无异常event")
    def test_caseid_1986771(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=817, no_opera_signal=['DCChrgnPosPortT', 'DCChrgnNegPortT'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)

    @allure.title("WTIService::WarningMsgList_PropulsionCAN::0x342同帧非相关信号跳变无异常event")
    def test_caseid_1986769(self):
        self.ipdu.filter_special_message_send(bus_name="propulsioncan", message=834, no_opera_signal=['HvilFlt', 'HvIsoFlt'])
        self.partner.ck_no_event(self.partner_key, "WarningMsgList", timeout=0.2)
