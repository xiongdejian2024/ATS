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
        self.soa.update(["VehicleModeService_client"])
        self.bus_comm.set_battcp_estimd(80)
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.ukwn)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        time.sleep(1)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd.NoConversionToLVSide)
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.check_egylvlelec(mai=0, subtype=0)
        pass

    def after_each_func(self, ecu):
        self.bus_comm.set_battcp_estimd(80)
        self.bus_comm.set_battiraw(BattIRaw=0)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        pass

    def after_class(self, ecu):
        self.io.tcam_power_on()
        self.mix.exit_crash()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        self.io.bgm_diag_line_up()
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.resume_all_bus_send()
        self.io.bgm_power_on()
        self.soa.stop_soa()


    # ---------------------------->powerlevel<---------------------------------------------
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1985346(self):
        "低能耗下EnergryLevel发送_inactive_nomal"
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=360)
        self.bus_comm.check_egylvlelec_drvinfo(info=1)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=1, mai_old=1, subtype_old=2, time=120)
        self.bus_comm.check_egylvlelec_drvinfo(info=2)
        
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1985345(self):
        "低能耗下EnergryLevel发送_convenience_nomal"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=360)
        self.bus_comm.check_egylvlelec_drvinfo(info=1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=1, mai_old=1, subtype_old=2, time=120)
        self.bus_comm.check_egylvlelec_drvinfo(info=2)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1985344(self):
        "低能耗下EnergryLevel发送_active_nomal"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=360)
        self.bus_comm.check_egylvlelec_drvinfo(info=1)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=1, mai_old=1, subtype_old=2, time=120)
        self.bus_comm.check_egylvlelec_drvinfo(info=2)
    
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1985343(self):
        "低能耗下EnergryLevel发送_driving_nomal_1"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=0, subtype_new=0, mai_old=0, subtype_old=0, time=480)
        self.bus_comm.check_egylvlelec_drvinfo(info=0)
    
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1985342(self):
        "低能耗下EnergryLevel发送_active_factory"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.FACTORY, car_mode_sub=0)
        self.bus_comm.set_battsocraw2_less_value(battsocraw2=65)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=60)
        self.bus_comm.check_egylvlelec_drvinfo(info=1)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1985341(self):
        "低能耗下EnergryLevel发送_active_transport"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.TRANSPORT, car_mode_sub=0)
        self.bus_comm.set_battsocraw2_less_value(battsocraw2=70)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=60)
        self.bus_comm.check_egylvlelec_drvinfo(info=1)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1985340(self):
        "低能耗下EnergryLevel发送_inactive_dyno_1"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=1, mai_old=0, subtype_old=0, time=300)
        self.bus_comm.check_egylvlelec_drvinfo(info=2)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1985376(self):
        "低能耗下EnergryLevel发送_inactive_dyno_2"
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.DYNO, car_mode_sub=0)
        self.bus_comm.set_battsocraw2_more_value(battsocraw2=100)
        self.bus_comm.set_battcp_estimd(1)
        self.bus_comm.check_egyavldelta(1)
        self.bus_comm.check_egyavlwarn(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=300)
        self.bus_comm.check_egylvlelec_drvinfo(info=1)
    
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1985338(self):
        "低能耗下EnergryLevel发送_ConversionToLVSide"
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd.ConversionToLVSide)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=0, subtype_new=0, mai_old=0, subtype_old=0, time=480)
        self.bus_comm.check_egylvlelec_drvinfo(info=0)
    
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1985405(self):
        "低能耗下EnergryLevel发送_RunngRemStrtd"
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=0, subtype_new=0, mai_old=0, subtype_old=0, time=480)
        self.bus_comm.check_egylvlelec_drvinfo(info=0)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1985339(self):
        "低能耗下EnergryLevel发送_inactive_crash"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.bus_comm.set_crashsts_safests(CrashSts=crashsts.Crash)
        self.bus_comm.check_carmode_dispd_in_time(carmode=CarMode.CRASH, subtype=0, carmoddisp1_old=CarModDisp1.CarModDisp1_Crash, carmoddisp1_new=CarModDisp1.CarModDisp1_NoDisp)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=360)
        self.bus_comm.check_egylvlelec_drvinfo(info=1)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=1, mai_old=1, subtype_old=2, time=120)
        self.bus_comm.check_egylvlelec_drvinfo(info=2)
        self.mix.exit_crash()
    
    @pytest.mark.full
    @pytest.mark.abandon
    def test_usage_mode_caseid_1985337(self):
        '''低能耗下inactive下切abandon'''
        self.mix.trigger_usage_mode_to_abandoned(wait_time=70)
        self.bus_comm.set_singal("infocanfd", "CdcInfoCanFdFr03", "MmedHdPwrMod", 3)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_battcp_estimd(0)
        self.bus_comm.check_egyavldelta(0)
        self.bus_comm.wait_time_and_check_egylvlelec(mai_new=1, subtype_new=2, mai_old=0, subtype_old=0, time=360)
        self.bus_comm.check_usage_mode_status_in_time(usagemode_old=UsageMode.INACTIVE, usagemode_new=UsageMode.ABANDONED, time=120, is_change=True)
        
    
    