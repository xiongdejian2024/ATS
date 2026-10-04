#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_usagemode_abc.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/1/9 13:20
@Description: BGMusagmode服务相关抽象接口用例
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
from framework.automotive.utils.data_type import EcuInfo
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("车控车设")
@allure.story("整车模式/使用模式")
class TestUsageMode(TestABCBase):
    @staticmethod
    def change_bench_config(ecu:EcuInfo) -> EcuInfo:
        ecu.domain.single_bgm = True
        ecu.domain.two_domain = False
        ecu.tc_config["dut_ecu"] = ["BGM"]
        return ecu
    def before_class(self, ecu):
        self.io.tcam_power_off()
        self.soa.update(["VehicleModeService_client", "TailGateService_client", "VehicleSetStatusService_client"])
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40E8, SESSION.EXTENDED, UnLock.L5, '00', '6e40e8', check_method=Check_Method.response, recover=False)
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.set_BrkSysSts_BrkSys_Capability(BrkSysCap=BrkSysCap.TestPending)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        pass

    def after_each_func(self, ecu):
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.set_epbsts_function_safe(sts=EpbSts.Resd0, ub_flag=True)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.soa.set_hv_off_sts(is_off=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.NoInhb)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.bus_comm.trigger_gear_by_manual(gear_status=False)
        self.bus_comm.trigger_gear_by_cdc(gear_status=False)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        pass

    def after_class(self, ecu):
        self.io.tcam_power_on()
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.stop_soa()


    # ---------------------------->雨刮模式设置<---------------------------------------------
    @allure.title("inactive存储与恢复")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    @pytest.mark.nvm
    def test_service_usagemode_caseid_109942(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        time.sleep(.7)
        self.io.io_reset_bgm()
        time.sleep(15)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @allure.title("convenience存储与恢复")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_service_usagemode_caseid_109979(self):
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.io.io_reset_bgm()
        time.sleep(15)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @allure.title("convenience存储与恢复")
    @pytest.mark.sanity
    @pytest.mark.nvm    
    def test_service_usagemode_caseid_1943277(self):
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.io.io_reset_bgm()
        time.sleep(15)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @allure.title("active存储与恢复")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    @pytest.mark.nvm
    def test_service_usagemode_caseid_110014(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        time.sleep(1)
        self.io.io_reset_bgm()
        time.sleep(15)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
    
    @pytest.mark.smoke
    @pytest.mark.App
    def test_usage_mode_caseid_1984577(self):
        "SetConvenienceForAppAction_1分钟"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        self.mix.wait_time_exit_usagemde_a_to_b(num=1, usagemode1=UsageMode.CONVENIENCE, usagemode2=UsageMode.INACTIVE)
    
    @pytest.mark.sanity
    @pytest.mark.App
    def test_usage_mode_caseid_1984574(self):
        "SetConvenienceForAppAction_上切满足条件不会下切_主驾门打开"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.io.set_door(Drvr=Door.open, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.sanity
    @pytest.mark.App
    @pytest.mark.longtime
    def test_usage_mode_caseid_1984576(self):
        "SetConvenienceForAppAction_0分钟"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience, time1= 0)
        self.mix.wait_time_exit_usagemde_a_to_b(num=15, usagemode1=UsageMode.CONVENIENCE, usagemode2=UsageMode.INACTIVE)
    
    @pytest.mark.sanity
    @pytest.mark.App
    @pytest.mark.longtime
    def test_usage_mode_caseid_1984575(self):
        "SetConvenienceForAppAction_0分钟_后排有占位"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience, time1= 0)
        self.bus_comm.set_secle_seat_present()
        self.mix.wait_time_in_usagemde(num=20, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    @pytest.mark.App
    def test_usage_mode_caseid_1984573(self):
        "SetConvenienceForAppAction_上切满足条件不会下切_副驾门打开"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.io.set_door(Drvr=Door.close, Pass=Door.open, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    @pytest.mark.App
    def test_usage_mode_caseid_1984572(self):
        "SetConvenienceForAppAction_上切满足条件不会下切_左后门打开"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.open, Trunk=Door.close)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    @pytest.mark.App
    def test_usage_mode_caseid_1984571(self):
        "SetConvenienceForAppAction_上切满足条件不会下切_右后门打开"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.open, LeRe=Door.close, Trunk=Door.close)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.sanity
    @pytest.mark.App
    def test_usage_mode_caseid_1984570(self):
        "SetConvenienceForAppAction_上切满足条件不会下切—_主驾有占位"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.io.driver_seat_present()
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.sanity
    @pytest.mark.App
    def test_usage_mode_caseid_1984569(self):
        "SetConvenienceForAppAction_上切满足条件不会下切—_踩刹车"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.bus_comm.set_brake_pedal()
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    @pytest.mark.App
    @pytest.mark.testfail
    def test_usage_mode_caseid_1984568(self):
        "SetConvenienceForAppAction_上切满足条件不会下切—_下切inactive再上切convenience"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_1984567(self):
        "SetConvenienceForAppAction_上切满足条件不会下切—_上切driving再下切convenience"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.DRIVING)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.smoke
    @pytest.mark.App
    def test_usage_mode_caseid_1984565(self):
        "SetConvenienceForAppAction_非inactive功能无效_Convenience"
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.SetConvenienceForAppAction_and_check_usagemode(time1=1, usagemode=UsageMode.CONVENIENCE)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    @pytest.mark.App
    def test_usage_mode_caseid_1984564(self):
        "SetConvenienceForAppAction_非inactive功能无效_Active"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.SetConvenienceForAppAction_and_check_usagemode(time1=1, usagemode=UsageMode.ACTIVE)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.ACTIVE)
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_1984563(self):
        "SetConvenienceForAppAction_非inactive功能无效_Driving"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.DRIVING)
        self.mix.SetConvenienceForAppAction_and_check_usagemode(time1=1, usagemode=UsageMode.DRIVING)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.DRIVING)
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_1984562(self):
        "SetConvenienceForAppAction_2s后上切convenience不会下切"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.SetConvenienceForAppAction_and_check_usagemode(time1=1, usagemode=UsageMode.INACTIVE)
        time.sleep(2)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    @pytest.mark.App
    def test_usage_mode_caseid_1984561(self):
        "SetConvenienceForAppAction_2s后上切Active不会下切"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.SetConvenienceForAppAction_and_check_usagemode(time1=1, usagemode=UsageMode.INACTIVE)
        time.sleep(2)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.wait_time_in_usagemde(num=1, usagemode=UsageMode.ACTIVE)        
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_1984560(self):
        "SetConvenienceForAppAction_上切后定时内上切active再下切"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(10)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 11})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        time.sleep(20)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
        time.sleep(30)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_usage_mode_caseid_1984559(self):
        "SetConvenienceForAppAction_上切后再上切active后超时"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(10)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 11})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        time.sleep(50)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.App
    def test_usage_mode_caseid_1984558(self):
        "SetConvenienceForAppAction_上切后满足条件会下切_副驾占位"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        time.sleep(30)
        self.bus_comm.set_pass_seat_present()
        time.sleep(30)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985774(self):
        "服务仲裁_up_abandon_down_abandon"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ABANDONED,down_usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985773(self):
        "服务仲裁_up_abandon_down_inactive"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ABANDONED,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985772(self):
        "服务仲裁_up_abandon_down_convenience"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ABANDONED,down_usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985771(self):
        "服务仲裁_up_abandon_down_active"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ABANDONED,down_usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985770(self):
        "服务仲裁_up_abandon_down_driving"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ABANDONED,down_usagemode=UsageMode.DRIVING)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985769(self):
        "服务仲裁_up_inactive_down_abandon"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985768(self):
        "服务仲裁_up_inactive_down_inactive"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985767(self):
        "服务仲裁_up_inactive_down_convenience"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985766(self):
        "服务仲裁_up_inactive_down_active"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985765(self):
        "服务仲裁_up_inactive_down_driving"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.DRIVING)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985764(self):
        "服务仲裁_up_convenience_down_abandon"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.CONVENIENCE,down_usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985763(self):
        "服务仲裁_up_convenience_down_inactive"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.CONVENIENCE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985762(self):
        "服务仲裁_up_convenience_down_convenience"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.CONVENIENCE,down_usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985761(self):
        "服务仲裁_up_convenience_down_active"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.CONVENIENCE,down_usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985760(self):
        "服务仲裁_up_convenience_down_driving"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.CONVENIENCE,down_usagemode=UsageMode.DRIVING)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985759(self):
        "服务仲裁_up_active_down_abandon"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ACTIVE,down_usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985758(self):
        "服务仲裁_up_active_down_inactive"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985757(self):
        "服务仲裁_up_active_down_convenience"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ACTIVE,down_usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985756(self):
        "服务仲裁_up_active_down_active"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ACTIVE,down_usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985755(self):
        "服务仲裁_up_active_down_driving"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.ACTIVE,down_usagemode=UsageMode.DRIVING)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985754(self):
        "服务仲裁_up_driving_down_abandon"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.DRIVING,down_usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.DRIVING)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985753(self):
        "服务仲裁_up_driving_down_inactive"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.DRIVING,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985752(self):
        "服务仲裁_up_driving_down_convenience"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.DRIVING,down_usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985751(self):
        "服务仲裁_up_driving_down_active"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.DRIVING,down_usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985750(self):
        "服务仲裁_up_driving_down_driving"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.DRIVING,down_usagemode=UsageMode.DRIVING)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.DRIVING)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985749(self):
        "服务仲裁_fail机制"
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.DRIVING,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ABANDONED)
        time.sleep(1)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985675(self):
        "踩刹车保持寻钥状态"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_key_nfc_vmm_prsnt_in_time(keyprsnt_old=Keyprsntsts.KeyPrsntStsInProgs, keyprsnt_new=Keyprsntsts.KeyPrsntStsIdle, time=60, is_change=False)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.check_key_nfc_vmm_prsnt(keyprsnt=Keyprsntsts.KeyPrsntStsIdle)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985674(self):
        "StrtInProgs_状态变化"
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_strtinprogs(StrtInProgs=StrtInProgs.StrtStsImminent)
        self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
        self.bus_comm.check_strtinprogs(StrtInProgs=StrtInProgs.StrtStsStrtng)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_strtinprogs(StrtInProgs=StrtInProgs.StrtStsRunng)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.check_strtinprogs(StrtInProgs=StrtInProgs.StrtStsImminent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.check_strtinprogs(StrtInProgs=StrtInProgs.StrtStsOff)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985673(self):
        " StrtMsgToDrvr上报_MSG7"
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.PwrUpDly)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.SetUsageModeUp)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg7)
        self.bus_comm.check_strt_msg_to_drvrr_in_time(StrtMsgToDrvrg_old=StrtMsgToDrvrg.Msg7, StrtMsgToDrvrg_new=StrtMsgToDrvrg.NoMsg, time=100, is_change=True)
        self.mix.set_strt_req(up_type=UpType.SetUsageModeUp)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg7)
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.NoInhb)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985672(self):
        '''StrtMsgToDrvr上报_MSG10'''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr_in_time(StrtMsgToDrvrg_old=StrtMsgToDrvrg.Msg10, StrtMsgToDrvrg_new=StrtMsgToDrvrg.NoMsg, time=5, is_change=True)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985671(self):
        '''StrtMsgToDrvr上报_MSG1'''
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.SelnOfParkOrNeut)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg1)
        self.bus_comm.check_strt_msg_to_drvrr_in_time(StrtMsgToDrvrg_old=StrtMsgToDrvrg.Msg1, StrtMsgToDrvrg_new=StrtMsgToDrvrg.NoMsg, time=5, is_change=True)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985670(self):
        '''KeyNotPrsntMsgToDrvr状态变化_置位计时'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp", {"mode": UsageMode.DRIVING.value})
        self.bus_comm.check_key_not_prsnt_msg_to_drvr(flag=1)
        self.bus_comm.check_key_not_prsnt_msg_to_drvr_in_time(flag_old=True, flag_new=False, time=4, is_change=True)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985669(self):
        '''KeyNotPrsntMsgToDrvr状态变化_置位计时重置'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp", {"mode": UsageMode.DRIVING.value})
        self.bus_comm.check_key_not_prsnt_msg_to_drvr_in_time(flag_old=True, flag_new=False, time=2, is_change=False)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp", {"mode": UsageMode.DRIVING.value})
        self.bus_comm.check_key_not_prsnt_msg_to_drvr_in_time(flag_old=True, flag_new=False, time=2, is_change=False)
        self.bus_comm.check_key_not_prsnt_msg_to_drvr_in_time(flag_old=True, flag_new=False, time=2, is_change=True)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985668(self):
        '''KeyNotPrsntMsgToDrvr状态变化_置位取消'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp", {"mode": UsageMode.DRIVING.value})
        self.bus_comm.check_key_not_prsnt_msg_to_drvr(flag=True)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_key_not_prsnt_msg_to_drvr(flag=False)
    
    @pytest.mark.full
    @pytest.mark.mcu_test
    def test_usage_mode_caseid_1985667(self):
        '''usagemode切换限制_lowspeed_driving_to_conveniecne'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehspd_and_qf(vehspd=7.2)
        self.io.set_door(Drvr=Door.open, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985666(self):
        '''usagemode切换限制_lowspeed_active_to_conveniecne'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_vehspd_and_qf(vehspd=7.2)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeDown", {"mode": UsageMode.CONVENIENCE.value})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985665(self):
        ''' DrivingCycleOffTime_计时机制'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=0)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=16, wait_time=1)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=32, wait_time=3)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=256, wait_time=252)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1985664(self):
        ''' DrivingCycleOffTime_冻结和重置机制'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=0)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=16, wait_time=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=16, wait_time=3)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=0)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985957(self):
        ''' usagemode统计信息_430E_abandon'''
        count1 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Abandon_0h)
        self.mix.trigger_usage_mode_to_abandoned()
        count2 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Abandon_0h)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985956(self):
        ''' usagemode统计信息_430E_inactive'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        count1 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Inactive_1min)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        time.sleep(60)
        count2 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Inactive_1min)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985955(self):
        ''' usagemode统计信息_430E_convenience_10min内'''
        count1 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Convenience_10s)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(10)
        count2 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Convenience_10s)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1)

    @pytest.mark.full
    @pytest.mark.longtime
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985954(self):
        ''' usagemode统计信息_430E_convenience_10min外'''
        count1,count3 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Convenience_10s, usagemode_size2=UsagemodeSize.Convenience_10min, is_flag=True)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(10)
        count2, count4 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Convenience_10s, usagemode_size2=UsagemodeSize.Convenience_10min, is_flag=True)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1, count_c=count3, count_d=count4, num_2=0, is_flag=True)
        time.sleep(590)
        count5, count6 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Convenience_10s, usagemode_size2=UsagemodeSize.Convenience_10min, is_flag=True)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count5, num=0, count_c=count3, count_d=count6, num_2=1, is_flag=True)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985953(self):
        ''' usagemode统计信息_430E_Active_10min内'''
        count1 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Active_10s)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        time.sleep(10)
        count2 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Active_10s)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1)

    @pytest.mark.full
    @pytest.mark.longtime
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985952(self):
        ''' usagemode统计信息_430E_Avtive_10min外'''
        count1,count3 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Active_10s, usagemode_size2=UsagemodeSize.Active_10min, is_flag=True)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        time.sleep(10)
        count2, count4 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Active_10s, usagemode_size2=UsagemodeSize.Active_10min, is_flag=True)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1, count_c=count3, count_d=count4, num_2=0, is_flag=True)
        time.sleep(590)
        count5, count6 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Active_10s, usagemode_size2=UsagemodeSize.Active_10min, is_flag=True)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count5, num=0, count_c=count3, count_d=count6, num_2=1, is_flag=True)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985951(self):
        ''' usagemode统计信息_430E_Driving_10min内'''
        count1 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Driving_0min)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        count2 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Driving_0min)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1)

    @pytest.mark.full
    @pytest.mark.longtime
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985950(self):
        ''' usagemode统计信息_430E_Driving_10min外'''
        count1,count3 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Driving_0min, usagemode_size2=UsagemodeSize.Driving_10min, is_flag=True)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        count2, count4 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Driving_0min, usagemode_size2=UsagemodeSize.Driving_10min, is_flag=True)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count2, num=1, count_c=count3, count_d=count4, num_2=0, is_flag=True)
        time.sleep(600)
        count5, count6 = self.sd_tester.send_usagemode_statistics_times_request_and_return_check_value(usagemode_size=UsagemodeSize.Driving_0min, usagemode_size2=UsagemodeSize.Driving_10min, is_flag=True)
        self.sd_tester.compare_a_and_b(count_a=count1, count_b=count5, num=0, count_c=count3, count_d=count6, num_2=1, is_flag=True)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985949(self):
        ''' usagemode统计信息_430F_abandon'''
        self.mix.trigger_usage_mode_to_abandoned()
        time1 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Abandon)
        time.sleep(60)
        time2 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Abandon)
        self.sd_tester.compare_a_and_b(count_a=time1, count_b=time2, num=1)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985948(self):
        ''' usagemode统计信息_430F_inactive'''
        time1 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Inactive)
        time.sleep(60)
        time2 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Inactive)
        self.sd_tester.compare_a_and_b(count_a=time1, count_b=time2, num=1)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985947(self):
        ''' usagemode统计信息_430F_convenience'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time1 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Convenience)
        time.sleep(60)
        time2 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Convenience)
        self.sd_tester.compare_a_and_b(count_a=time1, count_b=time2, num=1)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985946(self):
        ''' usagemode统计信息_430F_active'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        time1 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Active)
        time.sleep(60)
        time2 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Active)
        self.sd_tester.compare_a_and_b(count_a=time1, count_b=time2, num=1)

    @pytest.mark.full
    @pytest.mark.v110only
    def test_usage_mode_caseid_1985945(self):
        ''' usagemode统计信息_430F_driving'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time1 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Driving)
        time.sleep(60)
        time2 = self.sd_tester.send_usagemode_statistics_time_request_and_return_check_value(usagemode_value=UsagemodeValue.Driving)
        self.sd_tester.compare_a_and_b(count_a=time1, count_b=time2, num=1)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1986075(self):
        ''' HvActvForVehModReq状态_convenience'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=True)

    @pytest.mark.full
    def test_usage_mode_caseid_1986074(self):
        ''' HvActvForVehModReq状态_active'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=True)

    @pytest.mark.full
    def test_usage_mode_caseid_1986073(self):
        ''' HvActvForVehModReq状态_driving'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=True)

    @pytest.mark.full
    def test_usage_mode_caseid_1986072(self):
        ''' HvActvForVehModReq状态_Convenience_to_inactive_120s'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_hv_actv_for_vehmod_req_in_time(onoff_old=True, onoff_new=False, time=120, is_change=True)

    @pytest.mark.full
    @pytest.mark.ST
    def test_usage_mode_caseid_1986071(self):
        ''' HvActvForVehModReq状态_Convenience_to_inactive_主动下高压'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=True)
        self.soa.set_hv_off_sts(is_off=True)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=False)

    @pytest.mark.full
    @pytest.mark.ST
    def test_usage_mode_caseid_1986070(self):
        ''' HvActvForVehModReq状态_Active_to_inactive_主动下高压'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=True)
        self.soa.set_hv_off_sts(is_off=True)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=False)

    @pytest.mark.full
    @pytest.mark.ST
    def test_usage_mode_caseid_1986069(self):
        ''' HvActvForVehModReq状态_Driving_to_inactive_主动下高压'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(2)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeDown", {"mode": UsageMode.INACTIVE.value})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=True)
        self.soa.set_hv_off_sts(is_off=True)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=False)

    @pytest.mark.full
    @pytest.mark.testfail
    def test_usage_mode_caseid_1986068(self):
        ''' HvActvForVehModReq状态_Abandon_to_inactive'''
        self.mix.trigger_usage_mode_to_abandoned()
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp", {"mode": UsageMode.INACTIVE.value})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=False)

    @pytest.mark.full
    def test_usage_mode_caseid_1986067(self):
        ''' HvActvForVehModReq状态_Inactive_上下电'''
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_hv_actv_for_vehmod_req_in_time(onoff_old=False, onoff_new=True, time=20, is_change=False)

    @pytest.mark.full
    def test_usage_mode_caseid_1986066(self):
        ''' HvActvForVehModReq状态_Convenience_上下电'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience)
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_hv_actv_for_vehmod_req_in_time(onoff_old=True, onoff_new=False, time=20, is_change=False)
        time.sleep(20)
    
    @pytest.mark.sanity
    def test_usage_mode_caseid_1986701(self):
        ''' 踩刹车上切convenience_先踩刹车后解锁'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.sanity
    def test_usage_mode_caseid_1986700(self):
        ''' 踩刹车无法上切convenience_先踩刹车150s后解锁'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal()
        time.sleep(150)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    #BGM自检相关
    @pytest.mark.smoke
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989590(self):
        '''VMM主动上车自检_主驾门打开'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.open_fl_door, check_selftest_flag=True)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989589(self):
        '''VMM主动上车自检_副驾门打开'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.open_fr_door, check_selftest_flag=True)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989588(self):
        '''VMM主动上车自检_左后门打开'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.open_rl_door, check_selftest_flag=True)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989587(self):
        '''VMM主动上车自检_右后门打开'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.open_rr_door, check_selftest_flag=True)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    @pytest.mark.test1
    def test_usage_mode_caseid_1989586(self):
        '''VMM主动上车自检_主驾占位'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.occupy_drvr_seat, check_selftest_flag=True)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    @pytest.mark.test1
    def test_usage_mode_caseid_1989585(self):
        '''VMM主动上车自检_踩刹车'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.hit_brake, check_selftest_flag=True)

    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989584(self):
        '''VMM主动上车自检_服务上切convenience'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service, check_selftest_flag=True)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989583(self):
        '''VMM主动上车自检_调用应用设置convenience接口'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.app_set_convenience, check_selftest_flag=True)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989582(self):
        '''VMM主动上车自检_上切active后BrkSysSts满足'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.open_fl_door, check_selftest_flag=True, selftest_fail2_flg=True)
        time.sleep(2.5)
        self.bus_comm.set_BrkSysSts_BrkSys_Capability(BrkSysCap=BrkSysCap.Full)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
    
    @pytest.mark.full
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989581(self):
        '''VMM主动上车自检失效_300ms内convenience上切active'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.io.set_door(Drvr=Door.open)
        self.soa.send_method_request( 'VehicleModeService_client', 'SetUsageModeUp', {"mode": UsageMode.ACTIVE.value})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.Reqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=True)
        time.sleep(5.5)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
    
    @pytest.mark.full
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989580(self):
        '''VMM主动上车自检失效_300ms内convenience下切inactive'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.io.set_door(Drvr=Door.open)
        self.soa.send_method_request( 'VehicleModeService_client', 'SetUsageModeDown', {"mode": UsageMode.INACTIVE.value})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
        time.sleep(6)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)  
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989579(self):
        ''' VMM主动上车自检失效_5.5s内active下切inactive'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service, check_selftest_flag=True, selftest_fail2_flg=True)
        self.soa.send_method_request( 'VehicleModeService_client', 'SetUsageModeDown', {"mode": UsageMode.INACTIVE.value})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
        time.sleep(6)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
    
    @pytest.mark.full
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989578(self):
        ''' VMM主动上车自检失效_5.5s内active下切Convenience'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service, check_selftest_flag=True, selftest_fail2_flg=True)
        self.soa.send_method_request( 'VehicleModeService_client', 'SetUsageModeDown', {"mode": UsageMode.CONVENIENCE.value})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
        time.sleep(6)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
    
    @pytest.mark.full
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989577(self):
        '''VMM主动上车自检失效_5.5s内active上切driving'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service, check_selftest_flag=True, selftest_fail2_flg=True)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.Reqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=True)
        time.sleep(5.5)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.Reqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=True)
        time.sleep(4.5)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989576(self):
        '''VMM主动上车自检失效_5.5s内收到服务上切active'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service, check_selftest_flag=True, selftest_fail2_flg=True)
        self.soa.send_method_request( 'VehicleModeService_client', 'SetUsageModeUp', {"mode": UsageMode.ACTIVE.value})
        self.bus_comm.check_keeperreq_act(usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.Reqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=True)
        time.sleep(5.5)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
    
    @pytest.mark.sanity
    @pytest.mark.selftest
    def test_usage_mode_caseid_1989575(self):
        '''VMM主动上车自检失效_BrkSysSts非TestPending'''
        self.bus_comm.set_BrkSysSts_BrkSys_Capability(BrkSysCap=BrkSysCap.NotInitialized)
        time.sleep(0.3)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.open_fl_door, check_selftest_flag=True, selftest_fail1_flg=True)
        time.sleep(0.3)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=True)
        time.sleep(5.5)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_PrkgFctTestPndReq_From_VMM(ReqSts2=ReqSts2.NotReqd)
        self.bus_comm.check_VMM_BrkgSys_SelfTestFlg(SelfTestFlg=False)
    
    
    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993234(self):
        '''EPB丢失处理'''
        self.bus_comm.set_trsm_park_lockd(TrsmParkLockd=TrsmParkLockd.Undefd)
        self.bus_comm.set_epb_sts(sts=3)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_VehParkNotActvd(Flg1=Flg1.Rst)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.set_epbsts_function_safe(sts=EpbSts.AllAppld, ub_flag=False)
        time.sleep(3)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_VehParkNotActvd(Flg1=Flg1.Set)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993233(self):
        '''TrsmParkLockd丢失处理'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_trsm_park_lockd(TrsmParkLockd=TrsmParkLockd.ParkNotEngd)
        time.sleep(1)
        self.bus_comm.set_trsmparklockd_function_safe(TrsmParkLockd=TrsmParkLockd.ParkNotEngd, ub_flag=False)
        time.sleep(5)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_trsm_park_lockd(TrsmParkLockd=TrsmParkLockd.ParkEngd)
        time.sleep(1)
        self.bus_comm.set_trsmparklockd_function_safe(TrsmParkLockd=TrsmParkLockd.ParkEngd, ub_flag=False)
        time.sleep(5)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993231(self):
        '''服务下切_Idle_inactive'''
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 0})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 2})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 13})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993230(self):
        '''服务下切_Idle_convenience'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 0})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 2})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 13})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993229(self):
        '''服务下切_Idle_active'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 0})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 13})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993228(self):
        '''服务下切_Idle_driving'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 0})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 13})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993227(self):
        '''服务下切_convenience_to_inactive'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993226(self):
        '''服务下切_Active_to_inactive'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993225(self):
        '''服务下切_Driving_to_inactive'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993224(self):
        '''服务下切_Active_to_convenience'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 2})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993223(self):
        '''服务下切_Driving_to_convenience'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 2})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993222(self):
        '''服务下切_Driving_to_active'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(1.5)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993220(self):
        '''发动机信号丢失'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_sts_function_safe(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng, ub_flag=False)
        time.sleep(0.7)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993219(self):
        '''DrivingCycleOffTime_计时机制_发动机信号丢失'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_engine_sts_function_safe(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng, ub_flag=False)
        time.sleep(3)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=0)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=16, wait_time=1)
        self.bus_comm.check_drvgcycoff_time(TiDrvgCycOff=32, wait_time=3)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993217(self):
        '''Usagemode_远程泊车场景，触发动力系统启动_immo超时_Rdy'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Rdy, imobengsts1=ImobSts.ImobImobn)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        self.bus_comm.check_RemPrkgSts(RemPrkgSts=RemPrkgSts.PrkgAssiSysRemPrkgSts_Remoteparkactive)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993216(self):
        '''Usagemode_远程泊车场景，触发动力系统启动_immo超时_PreStrtg'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_PreStrtg, imobengsts1=ImobSts.ImobImobn)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        self.bus_comm.check_RemPrkgSts(RemPrkgSts=RemPrkgSts.PrkgAssiSysRemPrkgSts_Remoteparkactive)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993215(self):
        '''Usagemode_远程泊车场景，触发动力系统启动_immo超时_RunngRemStrtd'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, imobengsts1=ImobSts.ImobImobn)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        self.bus_comm.check_RemPrkgSts(RemPrkgSts=RemPrkgSts.PrkgAssiSysRemPrkgSts_Remoteparkactive)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993214(self):
        '''Usagemode_远程泊车场景，触发动力系统启动_immo超时_AftRun'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_AftRun, imobengsts1=ImobSts.ImobImobn)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        self.bus_comm.check_RemPrkgSts(RemPrkgSts=RemPrkgSts.PrkgAssiSysRemPrkgSts_Remoteparkactive)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(1)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993213(self):
        '''Usagemode_远程泊车场景，触发动力系统启动_WakeupTimeout'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini, imobengsts1=ImobSts.ImobImobn)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeWithoutKey",{"mode": 2})
        self.bus_comm.check_RemPrkgSts(RemPrkgSts=RemPrkgSts.PrkgAssiSysRemPrkgSts_Remoteparkactive)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.PtActvnReq)
        time.sleep(0.3)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993210(self):
        '''EPB夹紧非P档开门下车不提醒'''
        self.bus_comm.set_trsm_park_lockd(TrsmParkLockd=TrsmParkLockd.ParkNotEngd)
        self.bus_comm.check_veh_not_park_info_warn(VehNotParkInfoWarn=VehNotParkInfoWarn.OutofP)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_veh_not_park_info_warn(VehNotParkInfoWarn=VehNotParkInfoWarn.ShifttoP)
        self.bus_comm.check_AudWarn(AudWarn=True)
        self.bus_comm.set_epb_sts(sts=3)
        self.bus_comm.check_veh_not_park_info_warn(VehNotParkInfoWarn=VehNotParkInfoWarn.NoTxt)
        self.bus_comm.check_AudWarn(AudWarn=False)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993208(self):
        '''长时间踩刹车无效'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake, imobengsts1=ImobSts.ImobMtn)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(150)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993207(self):
        '''Ub异常踩刹车无效'''
        self.bus_comm.set_driving_preconditions(engSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake, imobengsts1=ImobSts.ImobMtn)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(1)
        self.bus_comm.set_brake_pedal_function_safe(sts=YesOrNo.Yes, ub_flag=False)
        time.sleep(1.5)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_PtActvnReq(PtActvnReq=PtActvnReq1.NoPtActvnReq)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993206(self):
        '''convenience下切inactive_下高压'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.soa.send_method_request('VehicleModeService_client', "setHVOffSts", {"isOff":True})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993205(self):
        '''服务上切_Inactive_to_Convenience'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993204(self):
        '''服务上切_Inactive_to_Active'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993203(self):
        '''服务上切_Convenience_to_Active'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993202(self):
        '''服务上切_Prevent_decrease_fromDriving'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 13})
        self.bus_comm.check_ProxyKeepLow(usage_mode=UsageMode.DRIVING)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        self.bus_comm.check_ProxyKeepLow(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    @pytest.mark.new
    def test_usage_mode_caseid_1993201(self):
        '''服务触发Start_inhibit'''
        self.soa.send_method_request( 'VehicleModeService_client','SetStartInhibit',{"isInhibit": True})
        self.bus_comm.check_StartInhibitReq(StartInhibitReq=isOn.On)
        time.sleep(1)
        self.bus_comm.check_StartInhibitReq(StartInhibitReq=isOn.Off)

    @allure.title("Usagemode_本地存储和恢复_Inactive_诊断重启")
    @pytest.mark.full
    @pytest.mark.diagrest
    @pytest.mark.new
    @pytest.mark.nvm
    def test_service_usagemode_caseid_1994575(self):
        self.sd_tester.reset_bgm()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @allure.title("Usagemode_本地存储和恢复_Driving_Run_诊断重启")
    @pytest.mark.full
    @pytest.mark.diagrest
    @pytest.mark.new
    @pytest.mark.nvm
    def test_service_usagemode_caseid_1994574(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)

    @allure.title("Usagemode_本地存储和恢复_Active_No_Run_诊断重启")
    @pytest.mark.full
    @pytest.mark.diagrest
    @pytest.mark.new
    @pytest.mark.nvm
    def test_service_usagemode_caseid_1994573(self):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)

    @allure.title("Usagemode_本地存储和恢复_Convenience_诊断重启")
    @pytest.mark.full
    @pytest.mark.diagrest
    @pytest.mark.new
    @pytest.mark.nvm
    def test_service_usagemode_caseid_1994572(self):
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    

    
    