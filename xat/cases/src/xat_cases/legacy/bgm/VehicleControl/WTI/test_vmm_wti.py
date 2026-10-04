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
@allure.story("WTI功能/TPMS and VMM")
class TestUsageMode(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["VehicleModeService_client", "VehicleSetStatusService_client", "WTIService_client"])
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40E8, SESSION.EXTENDED, UnLock.L5, '00', '6e40e8', check_method=Check_Method.response, recover=False)
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
        pass

    def after_each_func(self, ecu):
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.NoInhb)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.bus_comm.trigger_gear_by_manual(gear_status=False)
        self.bus_comm.trigger_gear_by_cdc(gear_status=False)
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
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.io.bgm_diag_line_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.stop_soa()


    # ---------------------------->vmm_wti<---------------------------------------------
    @pytest.mark.sanity
    def test_caseid_1981936(self):
        '''无钥匙提示告警'''
        hint = "No Key"
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeUp", {"mode": UsageMode.CONVENIENCE.value})
        self.bus_comm.check_key_not_prsnt_msg_to_drvr(flag=1)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        time.sleep(4)
        self.bus_comm.check_key_not_prsnt_msg_to_drvr(flag=0)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
        
    
    @pytest.mark.sanity
    @pytest.mark.test
    def test_caseid_1981935(self):
        '''启动相关提示报警msg1'''
        hint = "Starting"
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.SelnOfParkOrNeut)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg1)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        time.sleep(5)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")

    
    @pytest.mark.sanity
    def test_caseid_1981934(self):
        '''启动相关提示报警msg7'''
        hint = "Starting"
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.PwrUpDly)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.SetUsageModeUp)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg7)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="7")
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.NoInhb)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
        
    @pytest.mark.sanity
    @pytest.mark.test
    def test_caseid_1981933(self):
        '''启动相关提示报警msg10'''
        hint = "Starting"
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_strt_req(up_type=UpType.GeatAuto)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.Msg10)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="A")
        time.sleep(5)
        self.bus_comm.check_strt_msg_to_drvrr(StrtMsgToDrvrg=StrtMsgToDrvrg.NoMsg)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.sanity
    def test_caseid_1981932(self): 
        '''车辆工作提示报警'''
        hint = "Vehicle Working"
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.PwrUpDly)
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
        self.bus_comm.check_strtinprogs(StrtInProgs=StrtInProgs.StrtStsStrtng)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="2")
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_strtinprogs(StrtInProgs=StrtInProgs.StrtStsRunng)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
    @pytest.mark.sanity
    def test_caseid_1981931(self): 
        '''未驻车提示告警'''
        hint = "Not Parked"
        self.bus_comm.set_trsm_park_lockd(TrsmParkLockd=TrsmParkLockd.ParkNotEngd)
        self.bus_comm.check_veh_not_park_info_warn(VehNotParkInfoWarn=VehNotParkInfoWarn.OutofP)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="2")
        self.io.set_door(Drvr=Door.open, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.bus_comm.check_veh_not_park_info_warn(VehNotParkInfoWarn=VehNotParkInfoWarn.ShifttoP)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.io.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)
        self.bus_comm.check_veh_not_park_info_warn(VehNotParkInfoWarn=VehNotParkInfoWarn.OutofP)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="2")
        
    @pytest.mark.sanity
    def test_caseid_1981930(self): 
        '''触摸换挡器告警'''
        hint = "Touch Shift Activated"
        self.bus_comm.set_gearlvrillmnSts(GearLvrIllmnSts=isOn.On)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_gearlvrillmnSts(GearLvrIllmnSts=isOn.Off)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
    
   
    


   


    