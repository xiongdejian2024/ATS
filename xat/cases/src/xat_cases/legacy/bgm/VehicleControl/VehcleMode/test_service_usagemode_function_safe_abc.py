#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_service_usagemode_function_safe_abc.py
@Author      : heng.wang@jiduauto.com
@Time        : 2024/4/15 13:35
@Description: BGMusagmode功能安全相关抽象接口用例
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
        self.soa.set_hv_off_sts(is_off=False)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_strt_msg_to_mod_mngt(StrtMsgToModMngt=StrtMsgToModMngt.NoInhb)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.trigger_gear_by_auto(gear_status=False)
        self.bus_comm.trigger_gear_by_manual(gear_status=False)
        self.bus_comm.trigger_gear_by_cdc(gear_status=False)
        self.bus_comm.set_brake_pedal_function_safe(sts=YesOrNo.No)
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
        self.soa.stop_soa()


    # ---------------------------->功能安全<---------------------------------------------
    @pytest.mark.full
    def test_usage_mode_caseid_1986091(self):
        ''' VMM功能安全信号UsgModDeactvnQly_触发异常状态'''
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehspd_and_qf(vehspd=7.2)
        time.sleep(1.5)
        self.soa.send_method_request( 'VehicleModeService_client', "SetUsageModeDown", {"mode": UsageMode.INACTIVE.value})
        self.bus_comm.check_usgmode_deactvn_qly(usgmoddeactvnqly=UsgModDeactvnQly.QlyOkHighConfidence)
        time.sleep(0.4)
        self.bus_comm.check_usgmode_deactvn_qly(usgmoddeactvnqly=UsgModDeactvnQly.QlyNotOkLowConfidence)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    def test_usage_mode_caseid_1986090(self):
        ''' VMM功能安全信号UsgModDeactvnQly_默认值'''
        self.io.bgm_power_off()
        time.sleep(1)
        self.io.bgm_power_on()
        self.bus_comm.check_usgmode_deactvn_qly(usgmoddeactvnqly=UsgModDeactvnQly.QlyOkHighConfidence)
        time.sleep(20)
    
    @pytest.mark.full
    def test_usage_mode_caseid_1986094(self):
        ''' BrkPedlPsd功能安全_E2E失效'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal_function_safe(sts=YesOrNo.No, crc_sts=False)
        time.sleep(0.2)
        self.bus_comm.set_brake_pedal_function_safe(sts=YesOrNo.Yes, crc_sts=False)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)

    @pytest.mark.full
    def test_usage_mode_caseid_1986093(self):
        ''' BrkPedlPsd功能安全_UB异常'''
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_brake_pedal_function_safe(sts=YesOrNo.No, ub_flag=False)
        time.sleep(0.2)
        self.bus_comm.set_brake_pedal_function_safe(sts=YesOrNo.Yes, ub_flag=False)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)