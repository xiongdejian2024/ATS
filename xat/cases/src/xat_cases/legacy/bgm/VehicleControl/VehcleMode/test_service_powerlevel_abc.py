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
        self.soa.update(["VehicleModeService_client"])
        time.sleep(5)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.ukwn)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        pass

    def after_each_func(self, ecu):
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw=BattSnsrHwFltRaw.DevErrSts2_NoFlt)
        self.bus_comm.set_fltelecdcdc(fltelecdcdc=BattSnsrHwFltRaw.DevErrSts2_NoFlt)
        self.bus_comm.set_flttdcdc(flttdcdc=BattSnsrHwFltRaw.DevErrSts2_NoFlt)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.ukwn)
        self.bus_comm.set_battiraw(BattIRaw=1.0)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        pass

    def after_class(self, ecu):
        self.soa.send_method_request( 'VehicleModeService_client','SetUsageModeDown',{"mode": 1})
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.INACTIVE)
        self.io.bgm_diag_line_up()
        self.bus_comm.resume_all_bus_send()
        self.io.bgm_power_on()
        self.soa.stop_soa()


    # ---------------------------->powerlevel<---------------------------------------------
    @pytest.mark.smoke
    def test_caseid_1985284(self):
        "PowerLevel发送_LVPwrSplyErrSts=1"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_batturaw(BattURaw=16.0)
        time.sleep(5)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.UhiDurgDrvg)
        self.bus_comm.check_pwrlvlelec(mai=3,subtype=1)
    
    @pytest.mark.sanity
    def test_caseid_1985283(self):
        "PowerLevel发送_LVPwrSplyErrSts=2"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_batturaw(BattURaw=11.0)
        time.sleep(120)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.UloDurgdrvg)
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
    
    # @pytest.mark.full
    # def test_caseid_1985282(self):
    #     "PowerLevel发送_LVPwrSplyErrSts=4"
    #     self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
    #     self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
    #     time.sleep(1)
    #     self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
    #     self.bus_comm.pause_bus_send(bus_name="cem_lin6")
    #     time.sleep(10)
    #     self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.BattSnsrComFlt)
    #     self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
    
    @pytest.mark.sanity
    def test_caseid_1985281(self):
        "PowerLevel发送_LVPwrSplyErrSts=5"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw=BattSnsrHwFltRaw.DevErrSts2_Flt)
        time.sleep(20)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.BattSnsrHwFlt)
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
    
    @pytest.mark.sanity
    def test_caseid_1985280(self):
        "PowerLevel发送_LVPwrSplyErrSts=6"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.NoConversionToLVSide)
        time.sleep(10)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.FltComDcDc)
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
    
    @pytest.mark.sanity
    def test_caseid_1985279(self):
        "PowerLevel发送_LVPwrSplyErrSts=7"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_fltelecdcdc(fltelecdcdc=BattSnsrHwFltRaw.DevErrSts2_Flt)
        time.sleep(10)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.FltElecDcDc)
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
    
    @pytest.mark.sanity
    def test_caseid_1985278(self):
        "PowerLevel发送_LVPwrSplyErrSts=8"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_flttdcdc(flttdcdc=BattSnsrHwFltRaw.DevErrSts2_Flt)
        time.sleep(10)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.FltDcDc)
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
    
    @pytest.mark.full
    @pytest.mark.longtime
    def test_caseid_1985277(self):
        "PowerLevel发送_LVPwrSplyErrSts=15"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_battsoc_less_15()
        self.bus_comm.set_battiraw(BattIRaw=-100.0)
        time.sleep(900)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.LoSOC)
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
    
    @pytest.mark.sanity
    def test_caseid_1985276(self):
        "PowerLevel发送_CllsnThreat1=1"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.threatlo)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=1)
    
    @pytest.mark.sanity
    def test_caseid_1985275(self):
        "PowerLevel发送_CllsnThreat1=2"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.threatmed)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=2)
    
    @pytest.mark.sanity
    def test_caseid_1985274(self):
        "PowerLevel发送_CllsnThreat1=3"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.threathi)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=3)
    
    @pytest.mark.sanity
    def test_caseid_1985461(self):
        "PowerLevel发送优先级PwrLvlElecMai_4_3"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.threathi)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=3)
        self.bus_comm.set_batturaw(BattURaw=16.0)
        time.sleep(5)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.UhiDurgDrvg)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=3)
    
    @pytest.mark.sanity
    def test_caseid_1985460(self):
        "PowerLevel发送优先级PwrLvlElecMai_4_5"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.threathi)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=3)
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw=BattSnsrHwFltRaw.DevErrSts2_Flt)
        time.sleep(20)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.BattSnsrHwFlt)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=3)
    
    @pytest.mark.full
    def test_caseid_1985459(self):
        "PowerLevel发送优先级PwrLvlElecMai_3_4"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_batturaw(BattURaw=16.0)
        time.sleep(5)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.UhiDurgDrvg)
        self.bus_comm.check_pwrlvlelec(mai=3,subtype=1)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.threathi)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=3)
    
    @pytest.mark.full
    def test_caseid_1985458(self):
        "PowerLevel发送优先级PwrLvlElecMai_5_4"
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.ACTIVE)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        time.sleep(1)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw=BattSnsrHwFltRaw.DevErrSts2_Flt)
        time.sleep(20)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts=LVPwrSplyErrSts.BattSnsrHwFlt)
        self.bus_comm.check_pwrlvlelec(mai=5,subtype=1)
        self.bus_comm.set_cllsnthreat(cllsnthreat=CllsnThreat1.threathi)
        self.bus_comm.check_pwrlvlelec(mai=4,subtype=3)