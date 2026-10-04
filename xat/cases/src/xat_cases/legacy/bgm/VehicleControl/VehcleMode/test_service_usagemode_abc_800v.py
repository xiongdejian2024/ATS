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
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("车控车设")
@allure.story("整车模式/使用模式")
class TestUsageMode(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "TailGateService_client", "VehicleSetStatusService_client"])
        self.sd_tester.write_ccp(ccp={962: 2})
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
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.stop_soa()

    
    @pytest.mark.full
    def test_usage_mode_caseid_1990944(self):
        '''Usagemode_交流充电_插枪状态禁止启动'''
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)

    @pytest.mark.full
    @pytest.mark.test2
    def test_usage_mode_caseid_1990943(self):
        '''Usagemode_交流充电_不插枪状态不禁止启动'''
        self.sd_tester.write_ccp(ccp={973: 1})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpEna)
    
    @pytest.mark.full
    @pytest.mark.test2
    def test_usage_mode_caseid_1990942(self):
        '''Usagemode_交流充电_插枪状态信号丢失1s禁止启动'''
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1_function_safe(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected, ub_flag=False)
        time.sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990941(self):
        '''Usagemode_交流充电_从Driving进入Convenience（用户插枪）'''
        self.sd_tester.write_ccp(ccp={973: 1})
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990940(self):
        '''StrtMsgToDrvr上报_MSG10_交流充电'''
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr_in_time(StrtMsgToDrvrg_old=StrtMsgToDrvrg.Msg10, StrtMsgToDrvrg_new=StrtMsgToDrvrg.NoMsg, time=5, is_change=True)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990939(self):
        '''Usagemode_交流或直流充电_插枪状态禁止启动_插交流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990938(self):
        '''Usagemode_交流或直流充电_插枪状态禁止启动_插直流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990937(self):
        '''Usagemode_交流或直流充电_插枪状态禁止启动_插直流枪和交流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990936(self):
        '''Usagemode_交流或直流充电_插枪状态信号丢失1s禁止启动_交流枪ub丢失'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1_function_safe(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected, ub_flag=False)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        time.sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990935(self):
        '''Usagemode_交流或直流充电_插枪状态信号丢失1s禁止启动_直流枪ub丢失'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts_function_safe(sts=DCChrgnHndlSts.Disconnected, ub_flag=False)
        time.sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990934(self):
        '''Usagemode_交流或直流充电_插枪状态信号丢失1s禁止启动_直流枪和交流枪都丢失'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1_function_safe(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected, ub_flag=False)
        self.bus_comm.set_dc_chrg_handle_sts_function_safe(sts=DCChrgnHndlSts.Disconnected, ub_flag=False)
        time.sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpNotEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990933(self):
        '''Usagemode_交流或直流充电_不插枪状态不禁止启动'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.GeatAuto)
        self.bus_comm.check_ChrgHndlStrtEna(ChrgHndlStrtEna=ChrgHndlStrtEna.PwrUpEna)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990932(self):
        '''Usagemode_交流或直流充电_从Driving进入Convenience(用户插枪)_插交流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990931(self):
        '''Usagemode_交流或直流充电_从Driving进入Convenience(用户插枪)_插直流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990930(self):
        '''Usagemode_交流或直流充电_从Driving进入Convenience(用户插枪)_插直流枪和交流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990929(self):
        '''StrtMsgToDrvr上报_MSG10_交流或直流充电_插交流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr_in_time(StrtMsgToDrvrg_old=StrtMsgToDrvrg.Msg10, StrtMsgToDrvrg_new=StrtMsgToDrvrg.NoMsg, time=5, is_change=True)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990928(self):
        '''StrtMsgToDrvr上报_MSG10_交流或直流充电_插直流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr_in_time(StrtMsgToDrvrg_old=StrtMsgToDrvrg.Msg10, StrtMsgToDrvrg_new=StrtMsgToDrvrg.NoMsg, time=5, is_change=True)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1990927(self):
        '''StrtMsgToDrvr上报_MSG10_交流或直流充电_插直流和交流枪'''
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr_in_time(StrtMsgToDrvrg_old=StrtMsgToDrvrg.Msg10, StrtMsgToDrvrg_new=StrtMsgToDrvrg.NoMsg, time=5, is_change=True)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)

    
    