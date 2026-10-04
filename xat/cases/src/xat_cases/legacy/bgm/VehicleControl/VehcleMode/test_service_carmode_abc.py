#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_carmode_abc.py
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
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("车控车设")
@allure.story("整车模式/车辆模式")
class TestUsageMode(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "VehicleSetStatusService_client"])
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        pass

    def after_each_func(self, ecu):
        self.mix.exit_crash()
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        pass

    def after_class(self, ecu):
        self.mix.exit_crash()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)


    # ---------------------------->carmode<---------------------------------------------
    @pytest.mark.full
    def test_caseid_1985725(self):
        "carmode_text_message_inactive_factory"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.FACTORY, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Facy, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Norm, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
    
    @pytest.mark.full
    def test_caseid_1985724(self):
        "carmode_text_message_inactive_transport"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.TRANSPORT, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.TRANSPORT, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Trnsp, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Norm, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
    
    @pytest.mark.full
    def test_caseid_1985723(self):
        "carmode_text_message_inactive_dyno"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.DYNO, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Dyno, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Norm, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)

    
    @pytest.mark.full
    def test_caseid_1985722(self):
        "carmode_text_message_inactive_crash"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.CRASH, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Crash, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
        self.mix.exit_crash()
    
    @pytest.mark.full
    def test_caseid_1985721(self):
        "carmode_text_message_inactive_factory_pause"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.FACTORY, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Facy, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        time.sleep(1)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=1, carmoddisp1_old=CarModDisp1.CarModDisp1_FacyStop, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
    
    @pytest.mark.full
    def test_caseid_1985720(self):
        "carmode_text_message_active_factory"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.FACTORY, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Facy, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Norm, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
    
    @pytest.mark.full
    def test_caseid_1985719(self):
        "carmode_text_message_active_transport"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.TRANSPORT, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.TRANSPORT, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Trnsp, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Norm, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
    
    @pytest.mark.full
    def test_caseid_1985718(self):
        "carmode_text_message_active_dyno"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.DYNO, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Dyno, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Norm, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
    
    @pytest.mark.full
    def test_caseid_1985717(self):
        "carmode_text_message_active_crash"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.CRASH, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Crash, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
        self.mix.exit_crash()
    
    @pytest.mark.full
    def test_caseid_1985716(self):
        "carmode_text_message_active_factory_pause"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.FACTORY, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Facy, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        time.sleep(1)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=1, carmoddisp1_old=CarModDisp1.CarModDisp1_FacyStop, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
    
    @pytest.mark.full
    def test_caseid_1985715(self):
        " carmode_text_message_factory_driving"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.soa.set_carmode_by_serivice(carmod=CarMode.FACTORY)
        time.sleep(1)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=2, carmoddisp1_old=CarModDisp1.CarModDisp1_FacyStop, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
    
    @pytest.mark.full
    def test_caseid_1985714(self):
        " carmode_text_message_transport_driving"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.soa.set_carmode_by_serivice(carmod=CarMode.TRANSPORT)
        time.sleep(1)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.NORMAL, subtype=3, carmoddisp1_old=CarModDisp1.CarModDisp1_TrnspStop, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp, is_change=False)
    
    @pytest.mark.full
    def test_caseid_1985713(self):
        " 诊断切换dyno子模式"
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0, '02', '6e4313', check_method=Check_Method.response, recover=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=1)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0, '01', '6e4313', check_method=Check_Method.response, recover=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
    
    #crash相关
    @pytest.mark.sanity
    @pytest.mark.crash
    @pytest.mark.nvm
    def test_caseid_1959794(self):
        "crash 存储"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        time.sleep(1)
        self.io.io_reset_bgm()
        time.sleep(20)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.mix.exit_crash()
        
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_110101(self):
        "Carmode_SRS检测到碰撞进入Crash"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.mix.exit_crash()
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_110140(self):
        "Carmode_退出Crash mode_Inactive上切Convenience"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        time.sleep(1)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_110139(self):
        "Carmode_退出Crash mode_Abandoned上切Active"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        self.sd_tester.quit_usage_mode()
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_110130(self):
        "Carmode_退出Crash mode_inactive上切driving"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        time.sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        self.sd_tester.quit_usage_mode()
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_110079(self):
        "Carmode_退出Crash mode_Abandoned上切Driving"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        self.sd_tester.quit_usage_mode()
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_110031(self):
        "Carmode_退出Crash mode_Abandoned上切Convenience"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        self.sd_tester.quit_usage_mode()
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_109987(self):
        "Carmode_退出Crash mode_Inactive上切Active"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        time.sleep(1)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_110094(self):
        "Carmode_退出Crash mode_Inactive上切Active"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        time.sleep(1)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_109968(self):
        "Carmode_退出Crash mode_Inactive1上切Driving"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.NORMAL, car_mode_sub=0)
        self.sd_tester.quit_usage_mode()
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_109898(self):
        "Carmode_退出Crash mode_Inactive1上切Convenience"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.mix.exit_crash()
    
    @pytest.mark.full
    @pytest.mark.crash
    def test_caseid_109953(self):
        "Carmode_退出Crash mode_Inactive1上切Driving"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.NoCrash)
        self.bus_comm.set_singal(bus="backbonefr", msg="SrsBackBoneFr02", signal="SafetyCrashFb", value=3)
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr26", signal="HvSysCrashFb", value=3)
        time.sleep(1)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeUp',{"mode": 13})
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        time.sleep(15)
    
    @pytest.mark.full
    @pytest.mark.crash
    @pytest.mark.nvm
    def test_caseid_1994571(self):
        "Carmode_车辆模式的本地存储和恢复_CarModCrash_诊断重启"
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.mix.exit_crash()

    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994570(self):
        "Carmode_车辆模式的本地存储和恢复_CarModDyno_诊断重启"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.DYNO, car_mode_sub=0)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.DYNO, car_mode_sub=0)

    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994569(self):
        "Carmode_车辆模式的本地存储和恢复_CarModTransport_诊断重启"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.TRANSPORT, car_mode_sub=0)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.TRANSPORT, car_mode_sub=0)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.TRANSPORT, car_mode_sub=0)

    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994568(self):
        "Carmode_车辆模式的本地存储和恢复_CarModFactory_诊断重启"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.FACTORY, car_mode_sub=0)
        time.sleep(1)
        self.sd_tester.reset_bgm()
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.FACTORY, car_mode_sub=0)
        
   


    