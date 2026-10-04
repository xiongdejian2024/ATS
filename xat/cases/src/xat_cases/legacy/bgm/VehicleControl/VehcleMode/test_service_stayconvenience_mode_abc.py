#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_stayconvenience_mode_abc.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/1/26 13:20
@Description: BGMusagmode驻车舒享服务相关抽象接口用例
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
        self.soa.update(["VehicleModeService_client", "TailGateService_client", "VehicleSetStatusService_client","KeyService_client"])
        self.sd_tester.write_ccp(ccp={3: 129, 566: 25, 950: 2})
        self.sd_tester.reset_0x1181()
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
        self.bus_comm.set_charging_sts(ChargingSts.Default)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.ConversionToLVSide)
        self.bus_comm.set_dispbattegyout(DispBattEgyOut=40.0)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        sleep(1)
        pass

    def after_each_func(self, ecu):
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.mix.exit_vehicle_inside_person()
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
        pass

    def after_class(self, ecu):
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)


    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_service_usagemode_caseid_1980936(self):
        '''驻车舒享时间到达后自动下切 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        self.mix.wait_time_exit_usagemde_a_to_b(num=30, usagemode1=UsageMode.CONVENIENCE, usagemode2=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.test
    def test_service_usagemode_caseid_1980935(self):
        '''驻车舒享中外部闭锁 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        time.sleep(10)
        self.bus_comm.send_nfc_cmd()
        self.mix.check_convenience_mode_duration(duration=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_service_usagemode_caseid_1980933(self):
        '''上下电后退出驻车舒享 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        self.mix.check_convenience_mode_duration(duration=1)
        self.io.bgm_power_off()
        time.sleep(10)
        self.io.bgm_power_on()
        time.sleep(25)
        self.mix.check_convenience_mode_duration(duration=0)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_service_usagemode_caseid_1980932(self):
        '''convenience外设置驻车舒享维持时间_driving '''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(UsageMode.DRIVING)
        self.soa.set_convenience_duration(time=1)
        time.sleep(300)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
        self.mix.wait_time_exit_usagemde_a_to_b(num=30, usagemode1=UsageMode.CONVENIENCE, usagemode2=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_service_usagemode_caseid_1980931(self):
        '''convenience外设置驻车舒享维持时间_active '''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        time.sleep(300)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
        self.mix.wait_time_exit_usagemde_a_to_b(num=30, usagemode1=UsageMode.CONVENIENCE, usagemode2=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_service_usagemode_caseid_1980930(self):
        '''convenience中修改驻车舒享维持时间_修改成1小时 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        self.mix.wait_time_in_usagemde(num=20, usagemode=UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=2)
        self.mix.wait_time_exit_usagemde_a_to_b(num=40, usagemode1=UsageMode.CONVENIENCE, usagemode2=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_service_usagemode_caseid_1980929(self):
        '''convenience中修改驻车舒享维持时间_修改成0 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        self.mix.wait_time_in_usagemde(num=20, usagemode=UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_service_usagemode_caseid_1980928(self):
        '''convenience中驻车舒享然后上切active再下切convenience '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        time.sleep(1)
        self.soa.send_method_request('VehicleModeService_client', "SetUsageModeUp", {"mode": 11})
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.ACTIVE)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
        self.mix.wait_time_exit_usagemde_a_to_b(num=30, usagemode1=UsageMode.CONVENIENCE, usagemode2=UsageMode.INACTIVE)
    
    # ###以下为V1.4新增维持上电

    @pytest.mark.smoke
    def test_caseid_1982830(self):
        '''维持上电模式进入 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
    
    @pytest.mark.smoke
    @pytest.mark.test
    def test_caseid_1982829(self):
        '''维持上电模式退出_服务 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_service)
        self.mix.check_convenience_mode_duration(0)
    
    @pytest.mark.sanity
    def test_caseid_1982828(self):
        '''维持上电模式退出_电量低 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(0)
    
    @pytest.mark.sanity
    def test_caseid_1982827(self):
        '''维持上电模式退出_挡位 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_gear)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_gear)
        self.mix.check_convenience_mode_duration(0)
    
    @pytest.mark.sanity
    def test_caseid_1982826(self):
        '''维持上电模式退出_carmode '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_carmode)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_carmode)
        self.mix.check_convenience_mode_duration(0)
    
    @pytest.mark.sanity
    def test_caseid_1982824(self):
        '''维持上电模式退出_carmode_其他 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_other)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_other)
        self.mix.check_convenience_mode_duration(0)
    
    @pytest.mark.sanity
    def test_caseid_1982823(self):
        '''维持上电模式退出触发闭锁请求 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.mix.check_convenience_mode_duration(duration=255)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @pytest.mark.sanity
    def test_caseid_1982822(self):
        '''维持上电模式存储_上下电 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(25)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(duration=0)
    
    @pytest.mark.full
    def test_caseid_1982820(self):
        '''维持上电模式退出_多个条件退出 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
    
    @pytest.mark.full
    def test_caseid_1982819(self):
        '''维持上电模式退出不触发闭锁请求_reason为1 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_service)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_caseid_1982818(self):
        '''维持上电模式退出不触发闭锁请求_LockStatus ！= 3_kAllLocked '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.full
    def test_caseid_1982817(self):
        '''维持上电模式退出不触发闭锁请求_占位有人 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.io.driver_seat_present()
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    
    @pytest.mark.sanity
    def test_service_usagemode_caseid_1982816(self):
        '''无法进入驻车舒享模式_Inactive '''
        self.mix.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        time.sleep(1)
        self.mix.check_convenience_mode_duration(duration=0)
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_service_usagemode_caseid_1982815(self):
        '''无法进入驻车舒享模式_Abandon '''
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        time.sleep(1)
        self.mix.check_convenience_mode_duration(duration=0)
        self.sd_tester.quit_usage_mode()
    
    @pytest.mark.sanity
    @pytest.mark.fail
    def test_service_usagemode_caseid_1982814(self):
        '''设置驻车舒享模式后下切Inactive '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_convenience_duration(time=1)
        self.mix.check_convenience_mode_duration(duration=1)
        self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 1})
        time.sleep(1)
        self.mix.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        self.mix.check_convenience_mode_duration(duration=0)
    
    @pytest.mark.full
    @pytest.mark.fail
    def test_service_usagemode_caseid_1982813(self):
        '''设置驻车舒享模式后下切Inactive '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.soa.set_convenience_duration(time=1)
        self.mix.check_convenience_mode_duration(duration=1)
        self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 1})
        time.sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.soa.chk_notify('VehicleModeService_client', "ConvenienceModeDuration", {"duration": 0})
        self.mix.check_convenience_mode_duration(duration=0)
        self.sd_tester.quit_usage_mode()
    
    # ###以下为V2.0新增宠物模式设置维持上电

    @pytest.mark.smoke
    def test_caseid_1986434(self):
        '''宠物模式设置维持上电模式进入 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)

    @pytest.mark.smoke
    @pytest.mark.test
    def test_caseid_1986433(self):
        '''宠物模式设置维持上电模式退出_服务 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.2)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_service)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_service)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.sanity
    def test_caseid_1986432(self):
        '''宠物模式设置维持上电模式退出_电量低 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.2)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.sanity
    def test_caseid_1986431(self):
        '''宠物模式设置维持上电模式退出_挡位 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.2)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_gear)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_gear)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.sanity
    def test_caseid_1986430(self):
        '''宠物模式设置维持上电模式退出_carmode '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_carmode)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_carmode)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.sanity
    def test_caseid_1986428(self):
        '''宠物模式设置维持上电模式退出_carmode_其他 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_other)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_other)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.sanity
    def test_caseid_1986427(self):
        '''宠物模式设置维持上电模式退出触发闭锁请求 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.mix.check_convenience_mode_duration(duration=255)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @pytest.mark.sanity
    def test_caseid_1986426(self):
        '''宠物模式设置维持上电模式存储_上下电 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        time.sleep(25)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(duration=0)

    @pytest.mark.full
    def test_caseid_1986425(self):
        '''宠物模式设置维持上电模式退出_多个条件退出 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)

    @pytest.mark.full
    def test_caseid_1986424(self):
        '''宠物模式设置维持上电模式退出不触发闭锁请求_reason为1 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_service)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_service)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    def test_caseid_1986423(self):
        '''宠物模式设置维持上电模式退出不触发闭锁请求_LockStatus ！= 3_kAllLocked '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    def test_caseid_1986422(self):
        '''维持上电模式退出不触发闭锁请求_占位有人 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.io.driver_seat_present()
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    def test_caseid_1986421(self):
        '''维持上电模式退出不触发闭锁请求_crash '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        time.sleep(1)
        self.bus_comm.check_car_mode_status(car_mode_main=CarMode.CRASH, car_mode_sub=0)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_carmode)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(15)
        self.mix.exit_crash()

    @pytest.mark.full
    def test_caseid_1986420(self):
        '''维持上电模式退出不触发闭锁请求_非P档 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_gear)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_gear)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    def test_caseid_1986418(self):
        '''维持上电模式优先级_宠物模式设置维持上电模式先打开_维持上电模式设置关闭 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.2)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_other)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.full
    def test_caseid_1986417(self):
        '''维持上电模式优先级_维持上电模式先打开_宠物模式设置维持上电模式关闭 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.soa.set_keep_power_mode_by_source(modeSts=False)
        time.sleep(1)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)

    @pytest.mark.full
    def test_caseid_1986416(self):
        '''宠物模式设置维持上电模式_source非petmode '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.soa.set_keep_power_mode_by_source(modeSts=True, source="Mode")
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_other)
        self.mix.check_convenience_mode_duration(0)
    
    # ###以下为V2.0新增维持上电体验优化用例
    @pytest.mark.sanity
    @pytest.mark.test1
    def test_caseid_1987411(self):
        '''维持上电模式退出_电量低且非充电中 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(0.3)
        self.bus_comm.set_charging_sts(ChargingSts.Default)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.sanity
    @pytest.mark.test1
    def test_caseid_1987410(self):
        '''维持上电模式退出_DCDC未激活10s '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.NoConversionToLVSide)
        time.sleep(11)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_other)
        self.mix.check_convenience_mode_duration(0)

    @pytest.mark.full
    @pytest.mark.test1
    def test_caseid_1987409(self):
        '''维持上电模式不退出_电量低且且充电中 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.set_charging_sts(ChargingSts.ACCharging)
        time.sleep(1)
        self.bus_comm.set_SOC_display_value(soc_value=19.0)
        time.sleep(1)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)

    @pytest.mark.full
    @pytest.mark.test1
    def test_caseid_1987408(self):
        '''维持上电模式不退出_DCDC未激活9s '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.NoConversionToLVSide)
        time.sleep(9)
        self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.ConversionToLVSide)
        time.sleep(2)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)

    @pytest.mark.sanity
    @pytest.mark.test1
    def test_caseid_1987407(self):
        '''维持上电模式剩余时间显示_Charging '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.set_charging_sts(ChargingSts.ACCharging)
        time.sleep(30)
        self.soa.check_keep_power_mode_and_time(True, exit_reason=KeepPowerFlag.open, displaytime=DisplayLeftTime.kCharging)
        self.mix.check_convenience_mode_duration(255)

    @pytest.mark.sanity
    @pytest.mark.test2
    def test_caseid_1987406(self):
        '''维持上电模式剩余时间显示_Calulating '''
        self.bus_comm.set_SOC_display_value(soc_value=19.7)
        self.mix.restart_bgm_and_connect_service("VehicleSetStatusService_client")
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.mix.set_soc_and_wait_tme_check_keep_power_mode_time(displaytime=DisplayLeftTime.kCalulating)
        self.mix.set_soc_and_wait_tme_check_keep_power_mode_time(wait_time=30, displaytime=DisplayLeftTime.kCalulating)
        self.mix.set_soc_and_wait_tme_check_keep_power_mode_time(wait_time=30, displaytime=DisplayLeftTime.kWithin15Min)

    @pytest.mark.sanity
    @pytest.mark.longtime
    @pytest.mark.test2
    def test_caseid_1987405(self):
        '''维持上电模式剩余时间显示_连续上升 '''
        soc_up_sz = [0, 19.9, 20.3, 21.1, 22.6, 24.0, 25.5, 26.9, 28.4, 30.1, 31.5, 33.0, 34.5, 35.9, 37.4, 39.1, 40.5, 42.0, 43.4, 44.9, 46.3, 47.8, 49.2, 50.7, 52.1, 53.6, 55.0]
        displaytime_up_sz = [ 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        self.mix.restart_bgm_and_connect_service("VehicleSetStatusService_client")
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_SOC_display_value(soc_value=19.7)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        time.sleep(30)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        self.mix.times_set_soc_and_wait_tme_check_keep_power_mode_time(soc_sz=soc_up_sz, displaytimesz=displaytime_up_sz)

    @pytest.mark.full
    @pytest.mark.longtime
    @pytest.mark.test2
    def test_caseid_1987404(self):
        '''维持上电模式剩余时间显示_连续下降 '''
        soc_down_sz = [0, 53.5, 52.0, 50.6, 49.1, 47.7, 46.2, 44.8, 43.3, 41.9, 40.4, 39.0, 37.5, 36.1, 34.8, 33.4, 31.9, 30.5, 29.0, 27.6, 26.4, 24.9, 23.5, 22.0, 20.6, 20.0, 19.6]
        displaytime_down_sz = [ 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3]
        self.mix.restart_bgm_and_connect_service("VehicleSetStatusService_client")
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_SOC_display_value(soc_value=54.3)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        time.sleep(30)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        self.mix.times_set_soc_and_wait_tme_check_keep_power_mode_time(soc_sz=soc_down_sz, displaytimesz=displaytime_down_sz)

    @pytest.mark.sanity
    @pytest.mark.test2
    def test_caseid_1987403(self):
        '''维持上电模式剩余时间显示_上升跃迁 '''
        soc_yq_sz=[0, 25.3]
        displaytime_yq_sz=[6, 9]
        self.mix.restart_bgm_and_connect_service("VehicleSetStatusService_client")
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_SOC_display_value(soc_value=21.8)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        time.sleep(30)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        self.mix.times_set_soc_and_wait_tme_check_keep_power_mode_time(soc_sz=soc_yq_sz, displaytimesz=displaytime_yq_sz)

    @pytest.mark.full
    @pytest.mark.test2
    def test_caseid_1987402(self):
        '''维持上电模式剩余时间显示_下降跃迁 '''
        soc_yq_sz=[0, 22.2]
        displaytime_yq_sz=[9, 6]
        self.mix.restart_bgm_and_connect_service("VehicleSetStatusService_client")
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.bus_comm.set_SOC_display_value(soc_value=26.4)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(1)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        time.sleep(30)
        self.soa.check_keep_power_mode(True, exit_reason=KeepPowerFlag.open)
        self.mix.check_convenience_mode_duration(255)
        self.mix.times_set_soc_and_wait_tme_check_keep_power_mode_time(soc_sz=soc_yq_sz, displaytimesz=displaytime_yq_sz)

    @pytest.mark.sanity
    @pytest.mark.test1
    def test_caseid_1987401(self):
        '''维持上电模式闭锁触发车控功能_已设置闭锁自动关窗 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All, mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        self.bus_comm.send_nfc_cmd()
        self.mix.check_convenience_mode_duration(duration=255)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_keep_power_car_config(indcr_sts=IndcrSts.LeAndRiOn, req=MirrFoldCmdTyp.FoldIn, pos=WinPos.close)
        time.sleep(0.5)
        self.bus_comm.check_keep_power_car_config(indcr_sts=IndcrSts.Off, req=MirrFoldCmdTyp.Idle, pos=WinPos.ukwn)

    @pytest.mark.full
    @pytest.mark.test1
    def test_caseid_1987434(self):
        '''维持上电模式闭锁触发车控功能_未设置闭锁自动关窗 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.set_rear_view_mode(pos=ViewPos.All, mode=MirrStsTyp.Unfold)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.bus_comm.send_nfc_cmd()
        self.mix.check_convenience_mode_duration(duration=255)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_keep_power_car_config(indcr_sts=IndcrSts.LeAndRiOn, req=MirrFoldCmdTyp.FoldIn, pos=WinPos.ukwn)
        time.sleep(0.5)
        self.bus_comm.check_keep_power_car_config(indcr_sts=IndcrSts.Off, req=MirrFoldCmdTyp.Idle, pos=WinPos.ukwn)
    
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_1994892(self):
        '''宠物模式设置维持上电模式退出触发闭锁请求_reason为1'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.mix.check_convenience_mode_duration(duration=255)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_service)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_service)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_1994891(self):
        '''宠物模式设置维持上电模式退出不触发闭锁请求_占位有人后占位无人 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.io.driver_seat_present()
        self.io.driver_seat_notpresent()
        time.sleep(3)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_1994890(self):
        '''宠物模式设置维持上电模式退出不触发闭锁请求_占位有人后开门占位无人时长不足3s  '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.open)
        self.io.driver_seat_notpresent()
        time.sleep(1)
        self.io.set_door(Drvr=Door.close)
        self.mix.set_keep_power_by_source_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode_by_source(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_1994889(self):
        '''维持上电模式退出触发闭锁请求_reason为1'''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        time.sleep(1)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.mix.check_convenience_mode_duration(duration=255)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_service)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_1994888(self):
        '''维持上电模式退出不触发闭锁请求_占位有人后占位无人 '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.io.driver_seat_present()
        self.io.driver_seat_notpresent()
        time.sleep(3)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)

    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_1994887(self):
        '''维持上电模式退出不触发闭锁请求_占位有人后开门占位无人时长不足3s  '''
        self.mix.set_usagemode_inactive_to_convenience(set_usagemode_type=set_usagemode_type.service)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.open)
        self.io.driver_seat_notpresent()
        time.sleep(1)
        self.io.set_door(Drvr=Door.close)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        time.sleep(1)
        self.soa.check_keep_power_mode(False, exit_reason=KeepPowerFlag.close_hvsoc)
        self.mix.check_convenience_mode_duration(duration=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.CONVENIENCE)
    


    