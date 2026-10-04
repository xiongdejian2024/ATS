#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_npc_vfc.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设VFC
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.common.data_handle import *


@allure.feature("车控车设")
@allure.story("VFC")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_client","CentralLockService_client","SteerWheelService_client",
                         "LightService_client",'ClimateControlService_client',"VehicleModeService_client",
                         "WiperService_client","ChargeLidService_client","TailWingService_client",
                         "KeyService_client","WindowAppService_client","GloveBoxService_client",
                         "OuterRearViewService_client","DoorService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    @allure.title("刹车灯1_PNC18置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC18
    def test_caseid_1985681(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        sleep(60)
        self.io.brake_light_close()
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 2.0)
        self.io.brake_light_open()

    @allure.title("刹车灯2_PNC18置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC18
    def test_caseid_1986152(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 5.0, 2.0)
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","BrkPedlPsdBrkPedlPsd", 0)

    @allure.title("近光灯故障_PNC18置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC18
    def test_caseid_1986151(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.mix.set_and_check_low_beam(sts=isOn.Off)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0,1.5)

    @allure.title("远光灯故障_PNC18置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC18
    def test_caseid_1985662(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.Off,hbid_value=6)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 2.0,1.5)
        self.mix.set_and_check_low_beam(sts=isOn.Off)

    @allure.title("灯光秀_PNC18置位1s")
    @pytest.mark.smoke
    @pytest.mark.PNC18
    def test_caseid_1985682(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        # self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, NMSts.no_valid)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 2.8)
        self.soa.hmi_set_light_show_active(status=False)

    @allure.title("主驾门_PNC18置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC18
    def test_caseid_1985680_1990959(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)
        self.io.set_door(Drvr=Door.close)

    @allure.title("LockgFbToExtLi锁车灯光提示_PNC18置位3s")
    @pytest.mark.smoke
    @pytest.mark.test1021
    @pytest.mark.PNC18
    def test_caseid_1990958(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 5.0, 1.5)

    @allure.title("车控车设_VFCPNC18_DoorLeReSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1021
    @pytest.mark.PNC18
    def test_vfc_caseid_1990961(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC18_DoorPassSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1021
    @pytest.mark.PNC18
    def test_vfc_caseid_1990960(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC18_DoorRiReSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1021
    @pytest.mark.PNC18
    def test_vfc_caseid_1990962(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)
        self.io.set_door(RiRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 3.0, 1.5)


    @allure.title("车控车设_VFCPNC18_AlrmToExtrLiVisReq触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1021
    @pytest.mark.PNC18
    def test_vfc_caseid_1989862(self):
        self.mix.clear_pnc(BGMPNC.PNC18)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, 20.0, 5.0)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, NMSts.valid, 3.0)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC18, NMSts.no_valid, 3.0)

    @allure.title("车控车设_VFCPNC38_AlrmToExtrLiVisReq触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1021
    @pytest.mark.PNC38
    def test_vfc_caseid_1989866(self):
        self.mix.clear_pnc(BGMPNC.PNC38)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(2)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=47)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC38, 20.0, 5.0)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC38, 3.0, 2.0)

    @allure.title("车控车设_VFCPNC38_hazard灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC38
    def test_vfc_caseid_1985683(self):
        self.mix.clear_pnc(BGMPNC.PNC38)
        self.io.hazard_light_open()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC38, NMSts.valid)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC38, 20.0, 5.0)
        self.io.hazard_light_close()
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC38, 20.0, 5.0)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC26, NMSts.no_valid, 3.0)

    
    

    

    

    

    