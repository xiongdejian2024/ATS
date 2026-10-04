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
        self.io.bgm_diag_line_down()
        self.io.io_reset_bgm()
        time.sleep(20)

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
        self.sd_tester.write_ccp(ccp={973: 0})
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        pass

    def after_class(self, ecu):
        self.io.bgm_diag_line_up()
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.soa.stop_soa()

    
    @pytest.mark.full
    def test_wakeup_caseid_1989397(self):
        '''Full Wakeup function激活逻辑_踩刹车激活超时失活'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_PtInin(OnOff=isOn.On)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        time.sleep(20)
        self.bus_comm.check_PtInin(OnOff=isOn.Off)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestNOTPresent)
    
    @pytest.mark.full
    def test_wakeup_caseid_1989396(self):
        '''Full Wakeup function激活逻辑_失活后可立即激活'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        time.sleep(20)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestNOTPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
    
    @pytest.mark.full
    def test_wakeup_caseid_1989395(self):
        '''Full Wakeup function激活逻辑_踩刹车激活上切active失活'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestNOTPresent)
    
    @pytest.mark.full
    def test_wakeup_caseid_1989394(self):
        '''Full Wakeup function激活逻辑_踩刹车激活超时重置'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        time.sleep(10)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(0.3)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        time.sleep(10)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        time.sleep(10)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestNOTPresent)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_wakeup_caseid_1989393(self):
        '''Full Wakeup function激活逻辑_踩刹车激活最大时长'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        time.sleep(120)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(120)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(120)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(120)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.Yes)
        time.sleep(110)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionActiveANDExternalRequestPresent)
        time.sleep(10)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestNOTPresent)
    
    @pytest.mark.full
    def test_wakeup_caseid_1989392(self):
        '''Partial Wakeup function激活逻辑_主驾门打开超时失活'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_PtInin(OnOff=isOn.On)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestPresent)
        self.io.set_door(Drvr=Door.close)
        time.sleep(10)
        self.bus_comm.check_PtInin(OnOff=isOn.Off)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestNOTPresent)
    
    @pytest.mark.full
    def test_wakeup_caseid_1989391(self):
        '''Partial Wakeup function激活逻辑_主驾门打开RlyPwrDistbnCmd1WdIgnRlyCmd置位失活'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestPresent)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestPresent)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_IgnRlyCmd(OnOff=isOn.On)
        self.bus_comm.check_EngActvnMod1WdReq(EngActvnMod1=EngActvnMod1.WakeupFunctionNOTActiveANDExternalRequestNOTPresent)
    
    @pytest.mark.full
    def test_wakeup_caseid_1989390(self):
        '''PtInin置位逻辑_RlyPwrDistbnCmd1WdIgnRlyCmd'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_IgnRlyCmd(OnOff=isOn.On)
        self.bus_comm.check_PtInin(OnOff=isOn.On)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_IgnRlyCmd(OnOff=isOn.Off)
        self.bus_comm.check_PtInin(OnOff=isOn.Off)
    

    