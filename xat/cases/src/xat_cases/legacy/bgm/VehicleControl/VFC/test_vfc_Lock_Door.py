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
                         "OuterRearViewService_client","DoorService_client","TailGateService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        pass

    def after_each_func(self, ecu):
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=False)
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    @allure.title("车控车设_VFCPNC16_DoorDrvrSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1988580(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("车控车设_VFCPNC16_DoorLeReSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1990953(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("车控车设_VFCPNC16_DoorPassSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1990952(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("车控车设_VFCPNC16_DoorRiReSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1990954(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.io.set_door(RiRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("车控车设_VFCPNC16_HoodSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1990955(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.io.set_hood_sts(HoodSts.Close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("车控车设_VFCPNC16_TrSts触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1990956(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0) 

    @allure.title("车控车设_VFCPNC16_充电口盖状态ChrgLidRearFltSts")
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_caseid_1990957(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.ipdu.lin2_wakeup()
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.ElecErr,sts=False)
        sleep(1)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.ElecErr,sts=True)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.ElecErr,sts=False)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("车控车设_VFCPNC16_四门状态_DoorOpenerPassSts")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1991423(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)

    @allure.title("车控车设_VFCPNC16_四门状态_DoorOpenerRiReSts")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1991424(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)

    @allure.title("车控车设_VFCPNC16_四门状态_DoorOpenerDrvrSts")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1988573(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)

    @allure.title("车控车设_VFCPNC16_四门状态_DoorOpenerLeReSts")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1988574(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
 
    @allure.title("车控车设_VFCPNC16_充电口盖故障ChrgLidManvgFailWarnDCorACDCSts")
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_caseid_1995669(self):
        self.sd_tester.write_single_ccp(578,0x04)
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcOverTrvlFb",0)
        sleep(1)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcOverTrvlFb",0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcOverTrvlFb",1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0)

    @allure.title("充电口盖故障ChrgLidManvgFailWarnDCorACDCSts_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1986095(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcOverTrvlFb",0)
        sleep(1)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",0)

    @allure.title("DoorXXIntrSwtLedLockgCmd外部开关状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1987562(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        # self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        # self.bus_comm.check_singal("bodycan","CemBodyFr02","DoorDrvrIntrSwtLedLockgCmd",1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        # self.bus_comm.check_singal("bodycan","CemBodyFr02","DoorDrvrIntrSwtLedLockgCmd",0)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("TrSts尾门状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1979888(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("DoorXXSts主驾门状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1987571(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "DoorDrvrSts", 1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_singal("bodycan", "CemBodyFr02", "DoorDrvrSts", 2)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("DoorXXSts副驾门状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1995825(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DoorPassSts", 2)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("DoorXXSts右后门状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1995826(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.io.set_door(RiRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("DoorXXSts左后门状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1995827(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("四门锁请求DoorDrvrLockCmd_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1979887(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("ChrgLidManvgFailWarnDCorACDCSts充电口盖_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1987563(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.bus_comm.set_singal("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcOverTFb", 1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.bus_comm.set_singal("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcOverTFb", 0)

    @allure.title("DoorXXSts四门状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1987561(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("HoodSts引擎盖状态_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC17
    def test_caseid_1987560(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.io.set_hood_sts(HoodSts.Close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("LockgCenStsForUsrFb中控锁状态_PNC17置位3s")
    @pytest.mark.sanity
    @pytest.mark.PNC17
    def test_caseid_1987559(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 3.0)

    @allure.title("LockgPrsnlSts手套箱私锁状态_PNC17置位3s")
    @pytest.mark.sanity
    @pytest.mark.PNC17
    def test_caseid_1987558(self):
        self.mix.clear_pnc(BGMPNC.PNC17)
        self.soa.hmi_set_glove_box_active_req(SetType.Lock)
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.PrivatetLockSts, GloveBoxStatus.On)
        sleep(1)
        self.soa.hmi_set_glove_box_active_req(SetType.Unlock)
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.PrivatetLockSts, GloveBoxStatus.Off)
        # self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, NMSts.valid)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 5.0, 2.5)
        self.soa.hmi_set_glove_box_active_req(SetType.Lock)
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.PrivatetLockSts, GloveBoxStatus.On)
        # self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, NMSts.valid)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, 5.0, 2.5)
        self.soa.hmi_set_glove_box_active_req(SetType.Unlock)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC17, NMSts.no_valid,timeout=10.0)

    @allure.title("车控车设_VFCPNC19_DoorXXOpenAutoReq 门打开请求")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1990966(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)
    
    # @allure.title("车控车设_VFCPNC19_DoorOpenerXXReq 门打开请求")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    # )
    # @pytest.mark.smoke
    # @pytest.mark.PNC19
    # def test_vfc_caseid_1988575(self):
    #     self.mix.clear_pnc(BGMPNC.PNC19)
    #     self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
    #     self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
    #     self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC19_四门状态_DoorOpenerDrvrSts")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1988579(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)

    @allure.title("车控车设_VFCPNC19_DoorDrvrOpenReqOutdSwt1触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1986089(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval= 0.1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC19_DoorPassOpenOutdSwtIf1触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1986096(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval= 0.1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)   

    @allure.title("车控车设_VFCPNC19_DoorLeReOpenOutdSwtIf1触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1986097(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval= 0.1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC19_DoorRiReOpenOutdSwtIf1触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1986098(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval= 0.1)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC19_ActvReSplrMgr 尾翼")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1986105(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_tailwing_pos(TailWingPos.P0)
        sleep(.5)
        self.io.set_door(Trunk=Door.close)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Auto)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 10.0)
        self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)

    @allure.title("尾门动作请求TrOpenerReq_PNC19置位3s")
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_caseid_1988570(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 2.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 2.5)

    @allure.title("车控车设_VFCPNC19_DoorOpenerXXReq触发")
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_caseid_1988575(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 2.5)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 2.5)

    @allure.title("车控车设_VFCPNC19_TrPosnUpprProgmReq 尾门学习")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC19
    def test_vfc_caseid_1990965(self):
        self.mix.clear_pnc(BGMPNC.PNC19)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_tailgate_switch_sts(sts=FoldHmiReq.Psd)
        self.bus_comm.check_tailgate_upper_req(req=isOn.On)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC19, 3.0, 1.5)
        self.bus_comm.check_tailgate_upper_req(req=isOn.Off)

    @allure.title("车控车设_PNC32_VFC Alarm -DoorDrvrSts")
    @pytest.mark.smoke
    @pytest.mark.PNC32
    def test_caseid_1991416(self):
        self.mix.clear_pnc(BGMPNC.PNC32)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)

    @allure.title("车控车设_PNC32_VFC Alarm -DoorLeReSts")
    @pytest.mark.smoke
    @pytest.mark.PNC32
    def test_caseid_1991417(self):
        self.mix.clear_pnc(BGMPNC.PNC32)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)

    @allure.title("车控车设_PNC32_VFC Alarm -DoorPassSts")
    @pytest.mark.smoke
    @pytest.mark.PNC32
    def test_caseid_1991418(self):
        self.mix.clear_pnc(BGMPNC.PNC32)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)

    @allure.title("车控车设_PNC32_VFC Alarm -DoorRiReSts")
    @pytest.mark.smoke
    @pytest.mark.PNC32
    def test_caseid_1991419(self):
        self.mix.clear_pnc(BGMPNC.PNC32)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
        self.io.set_door(RiRe=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)

    @allure.title("车控车设_PNC32_VFC Alarm -TrSts")
    @pytest.mark.smoke
    @pytest.mark.PNC32
    def test_caseid_1991420(self):
        self.mix.clear_pnc(BGMPNC.PNC32)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)

    @allure.title("车控车设_PNC32_VFC Alarm -HoodSts")
    @pytest.mark.smoke
    @pytest.mark.PNC32
    def test_caseid_1991421(self):
        self.mix.clear_pnc(BGMPNC.PNC32)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
        self.io.set_hood_sts(HoodSts.Close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)

    @allure.title("车控车设_PNC32_VFC Alarm -LockgCenSts")
    @pytest.mark.smoke
    @pytest.mark.PNC32
    def test_caseid_1991414_1991415(self):
        self.mix.clear_pnc(BGMPNC.PNC32)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC32, 3.0, 1.5)
    
