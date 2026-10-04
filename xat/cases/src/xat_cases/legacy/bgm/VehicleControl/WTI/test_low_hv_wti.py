#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_OuterRearView_ctrl.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设高低压WTI
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
@allure.story("智能补电")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_client","CentralLockService_client",'WTIService_client'])
        sleep(2)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=15")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1982542(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=200,low_soc=20)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
        sleep(10)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.LoSOC)
        self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning2",info="F")
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=10,low_soc=10)

    # @allure.title("智能补电_低压故障_LVPwrSplyErrSts=2")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    # )
    # @pytest.mark.sanity
    # def test_HvActive_caseid_1982543(self):
    #     self.mix.set_usage_mode(UsageMode.DRIVING)
    #     self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
    #     self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=200,low_soc=20)
    #     self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UloDurgdrvg)
    #     self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
    #     self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=10,low_soc=10)

    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=5")
    @allure.testcase(
         'https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46'
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109440(self):
        self.bus_comm.set_low_volt_power_supply()
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw.DevErrSts2_Flt)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw.DevErrSts2_Flt)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(25)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.BattSnsrHwFlt)
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw.DevErrSts2_NoFlt)
        sleep(10)
    
    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=4")
    @allure.testcase(
         'https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46'
    )
    @pytest.mark.sanity
    def test_HvActive_caseid_1982540(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
        self.bus_comm.pause_bus_send("cem_lin6")
        sleep(20)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.BattSnsrComFlt)
        self.bus_comm.resume_bus_send("cem_lin6")
        sleep(10)

    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=6")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    )
    @pytest.mark.sanity
    def test_HvActive_caseid_1985296(self):
        self.bus_comm.set_low_volt_power_supply()
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw.DevErrSts2_Flt)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.NoConversionToLVSide)
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw.DevErrSts2_Flt)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(5)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.FltComDcDc)
        self.bus_comm.set_batter_sensor_hw_failure(BattSnsrHwFltRaw.DevErrSts2_NoFlt)   

    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=8")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    )
    @pytest.mark.sanity
    def test_HvActive_caseid_1985903(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_flttdcdc(BattSnsrHwFltRaw.DevErrSts2_Flt)
        sleep(10)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.FltDcDc)
        self.bus_comm.set_flttdcdc(BattSnsrHwFltRaw.DevErrSts2_NoFlt)
        sleep(10)

    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=7")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    )
    @pytest.mark.sanity
    def test_HvActive_caseid_1985904(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_fltelecdcdc(BattSnsrHwFltRaw.DevErrSts2_Flt)
        sleep(10)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.FltElecDcDc)
        self.bus_comm.set_fltelecdcdc(BattSnsrHwFltRaw.DevErrSts2_NoFlt)
        sleep(10)

    @allure.title("智能补电_低压故障_LVPwrSplyErrSts=1")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    )
    @pytest.mark.sanity
    def test_HvActive_caseid_1982539(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xFA, 0xFF, 0xFF, 0xFF, 0xFF])
        sleep(5)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.UhiDurgDrvg)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.send_pdu("cem_lin6", 0x06, [0x0, 0x7C, 0xC8, 0xFF, 0xFF, 0xFF, 0xFF])

    @allure.title("智能补电_低压故障_ULoWarn = ULoPrmnt")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1982532?projectId=46"
    )
    @pytest.mark.sanity
    @pytest.mark.ULoWarn
    def test_HvActive_caseid_1982532(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_low_volt_power_supply()
        self.bus_comm.set_sys_safty_battery_current(0.0)
        self.bus_comm.set_sys_safty_battery_voltage(11.0)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng
        )
        sleep(65)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.ULoPrmnt)
        self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning1",info="2")
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini
        )
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)

    @allure.title("智能补电_低压故障_ULoWarn = ULoPrmnt")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1987989?projectId=46"
    )
    @pytest.mark.sanity
    @pytest.mark.ULoWarn
    def test_HvActive_caseid_1987989(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_low_volt_power_supply()
        self.bus_comm.set_sys_safty_battery_current(0.0)
        self.bus_comm.set_sys_safty_battery_voltage(11.0)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng
        )
        sleep(65)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.ULoPrmnt)
        # self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning1",info="2")
        self.bus_comm.set_sys_safty_battery_voltage(13.4)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini
        )

    @allure.title("智能补电_低压故障_ULoWarn = ULoPrmnt")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1987990?projectId=46"
    )
    @pytest.mark.sanity
    @pytest.mark.ULoWarn
    def test_HvActive_caseid_1987990(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_low_volt_power_supply()
        self.bus_comm.set_sys_safty_battery_current(-2.0)
        self.bus_comm.set_sys_safty_battery_voltage(13.4)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng
        )
        sleep(65)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.ULoPrmnt)
        # self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning1",info="2")
        self.bus_comm.set_sys_safty_battery_current(0.1)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini
        )
    
    @allure.title("智能补电_低压故障_ULoWarn = ULoPrmnt")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1987991?projectId=46"
    )
    @pytest.mark.sanity
    @pytest.mark.ULoWarn
    def test_HvActive_caseid_1987991(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_low_volt_power_supply()
        self.bus_comm.set_sys_safty_battery_current(-2.0)
        self.bus_comm.set_sys_safty_battery_voltage(13.4)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng
        )
        sleep(65)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.ULoPrmnt)
        # self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning1",info="2")
        self.bus_comm.set_sys_safty_battery_current(0.1)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattSftySigSysSaftyBattU')
        sleep(65)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.ULoPrmnt)
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattSftySigSysSaftyBattU')
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini
        )

    @allure.title("智能补电_低压故障_ULoWarn = ULoPrmnt")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1987992?projectId=46"
    )
    @pytest.mark.sanity
    @pytest.mark.ULoWarn
    def test_HvActive_caseid_1987992(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_low_volt_power_supply()
        self.bus_comm.set_sys_safty_battery_current(-2.0)
        self.bus_comm.set_sys_safty_battery_voltage(13.4)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng
        )
        sleep(65)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.ULoPrmnt)
        # self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning1",info="2")
        self.bus_comm.set_sys_safty_battery_current(0.1)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.ipdu.set_no_cntr(self.bus_comm.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattSftySigSysSaftyBattI')
        sleep(65)
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.ULoPrmnt)
        self.bus_comm.ipdu.restore_cntr(self.bus_comm.ipdu.cem_lin6.BmsCem_Lin6Fr01, 'BattSftySigSysSaftyBattI')
        self.bus_comm.check_low_sys_volt_warning(ULoWarnULoWarn.Uon)
        self.bus_comm.set_engine_sts(
            EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini
        )

    @allure.title("智能补电_低压系统故障信息2_LVPwrSplyErrSts=15")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    )
    @pytest.mark.sanity
    def test_HvActive_caseid_1982545(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=200,low_soc=20)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
        sleep(10)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.LoSOC)
        self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning2",info="F")
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=10,low_soc=10)
    
    @allure.title("智能补电_低压系统故障信息2_LVPwrSplyErrSts=4")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109440?projectId=46"
    )
    @pytest.mark.sanity
    def test_HvActive_caseid_1986407(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_dcdc_battary_act_sts(DcDcActvd=DcDcActvd.ConversionToLVSide)
        self.bus_comm.pause_bus_send("cem_lin6")
        sleep(20)
        self.bus_comm.check_lv_power_supply_error_sts(LVPwrSplyErrSts.BattSnsrComFlt)
        self.soa.get_and_event_check_warning_info_list(name="Low Battery Warning2",info="4")
        self.bus_comm.resume_bus_send("cem_lin6")
        sleep(10)

    @allure.title("获取和通知高压电池电量低报警信息_反向用例")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982555(self):
        self.bus_comm.set_SOC_display_value(soc_value=0.0)
        sleep(1)
        self.bus_comm.set_SOC_display_value(soc_value=10.0)
        self.soa.get_battery_low_warn_info(
            BatteryLowTelltale=BatteryLowTelltale.TELLTALE_FLASH,
            isFirstWarn=False,
            isSecondWarn=True,
        )
        self.bus_comm.set_SOC_display_value(soc_value=13.0)
        self.soa.get_battery_low_warn_info(
            BatteryLowTelltale=BatteryLowTelltale.TELLTALE_FLASH,
            isFirstWarn=False,
            isSecondWarn=True,
        )
        self.bus_comm.set_SOC_display_value(soc_value=20.0)
        self.soa.get_battery_low_warn_info(
            BatteryLowTelltale=BatteryLowTelltale.TELLTALE_ON,
            isFirstWarn=True,
            isSecondWarn=False,
        )
        self.bus_comm.set_SOC_display_value(soc_value=21.0)
        self.soa.get_battery_low_warn_info(
            BatteryLowTelltale=BatteryLowTelltale.TELLTALE_ON,
            isFirstWarn=True,
            isSecondWarn=False,
        )
        self.bus_comm.set_SOC_display_value(soc_value=22.0)
        self.soa.get_batterylow_mode(
            BatteryLowTelltale=BatteryLowTelltale.TELLTALE_OFF,
            isFirstWarn=False,
            isSecondWarn=False,
        )

    @allure.title("充电口温度过高提示")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735395?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_105999(self):
        self.bus_comm.set_DC_charge_port_tmp(DCChrgnPort.Pos, 0)
        self.bus_comm.set_DC_charge_port_tmp(DCChrgnPort.Neg, 0)
        sleep(1)
        self.bus_comm.set_DC_charge_port_tmp(DCChrgnPort.Pos, 120.0)
        self.soa.get_charging_info(isTempHigh=True)
        self.bus_comm.set_DC_charge_port_tmp(DCChrgnPort.Pos, 0.0)
        self.soa.get_charging_info(isTempHigh=False)
        self.bus_comm.set_DC_charge_port_tmp(DCChrgnPort.Neg, 120.0)
        self.soa.get_charging_info(isTempHigh=True)
        self.bus_comm.set_DC_charge_port_tmp(DCChrgnPort.Neg, 0.0)
        self.soa.get_charging_info(isTempHigh=False)

    @allure.title("WTI_高压电池低点亮告警信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1981886_1981885_1981884_1980966(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVolBattLow,value=100.0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.HighVolBattLow,sig_value=15.0,prom_name="High Voltage Battery Low Warning",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.HighVolBattLow,sig_value=9.0,prom_name="High Voltage Battery Low Warning",prom_state="2")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.HighVolBattLow,sig_value=100.0,prom_name="High Voltage Battery Low Warning",prom_state="0")
    
    @allure.title("WTI_动力电池故障灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981883(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVoltBattFailed_1,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HighVoltBattFailed_1,sig_value=1,prom_name="High Voltage Battery Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HighVoltBattFailed_1,sig_value=0,prom_name="High Voltage Battery Failed",prom_state="0")
        self.bus_comm.stop_send_pdu("chassiscan2", "EcmChas2Fr19")
        sleep(5)
        self.soa.get_and_event_check_warning_light_list(name="High Voltage Battery Failed",state="1")
        self.bus_comm.resume_send_pdu("chassiscan2", "EcmChas2Fr19")
        sleep(5)    
    
    @allure.title("WTI_动力系统故障灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981880_1981879(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailed,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.PowerSysFailed,sig_value=1,prom_name="Power System Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.PowerSysFailed,sig_value=0,prom_name="Power System Failed",prom_state="0")
        self.bus_comm.stop_send_pdu("chassiscan2", "EcmChas2Fr19")
        sleep(5)
        self.soa.get_and_event_check_warning_light_list(name="Power System Failed",state="1")
        self.bus_comm.resume_send_pdu("chassiscan2", "EcmChas2Fr19")
        sleep(5)

    @allure.title("WTI_动力电池故障灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981882_1982550(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVoltBattFailed_2,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HighVoltBattFailed_2,sig_value=1,prom_name="High Voltage Battery Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HighVoltBattFailed_2,sig_value=0,prom_name="High Voltage Battery Failed",prom_state="0")
        self.bus_comm.stop_send_pdu("chassiscan2", "EcmChas2Fr19")
        sleep(5)
        self.soa.get_and_event_check_warning_light_list(name="High Voltage Battery Failed",state="1")
        self.bus_comm.resume_send_pdu("chassiscan2", "EcmChas2Fr19")
        sleep(5)

    @allure.title("WTI_动力系统故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981881_1981887_1981888(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailure,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.PowerSysFailure,sig_value=2,prom_name="Power System Failure",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.PowerSysFailure,sig_value=3,prom_name="Power System Failure",prom_state="2")
        self.bus_comm.stop_send_pdu("chassiscan2", "EcmChas2Fr31")
        sleep(5)
        self.soa.get_and_event_check_warning_info_list(name="Power System Failure",info="4")
        self.bus_comm.resume_send_pdu("chassiscan2", "EcmChas2Fr31")

    @allure.title("WTI_充电故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982562(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        logger.info(f"模拟系统故障信息:powertrainFaultMsg.msg=5 or 7 8-5 11-7")
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailure,value=8)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingFailedWarning,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargingFailedWarning,sig_value=18,prom_name="Charging Failed Warning",prom_state="1")
        sleep(1)
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailure,value=3)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargingFailedWarning,sig_value=1,prom_name="Charging Failed Warning",prom_state="0")

    @allure.title("WTI_充电故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981890(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        logger.info(f"模拟系统故障信息:powertrainFaultMsg.msg=5 or 7 8-5 11-7")
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailure,value=11)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingFailedWarning,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargingFailedWarning,sig_value=18,prom_name="Charging Failed Warning",prom_state="1")
        sleep(1)
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailure,value=3)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargingFailedWarning,sig_value=1,prom_name="Charging Failed Warning",prom_state="0")

    @allure.title("WTI_充电故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981889(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        logger.info(f"模拟系统故障信息:powertrainFaultMsg.msg=5 or 7 8-5 11-7")
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailure,value=11)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingFailedWarning,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargingFailedWarning,sig_value=18,prom_name="Charging Failed Warning",prom_state="1")
        sleep(1)
        self.bus_comm.set_wti_signal(func=WTI_Func.PowerSysFailure,value=3)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargingFailedWarning,sig_value=2,prom_name="Charging Failed Warning",prom_state="0")
          

    @allure.title("WTI_电池低温指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982553(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.BatteryTempLow,value=50)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BatteryTempLow,sig_value=10,prom_name="Battery Temp Low",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BatteryTempLow,sig_value=60,prom_name="Battery Temp Low",prom_state="0")
        
    @allure.title("WTI_热失控报警信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982554(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.ThermalOutOfControl,value=64)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ThermalOutOfControl,sig_value=128,prom_name="Thermal Out of Control",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ThermalOutOfControl,sig_value=127,prom_name="Thermal Out of Control",prom_state="0")

    @allure.title("WTI_高压互锁状态信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982556(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVolInterLock_0,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVolInterLock_1,value=1)
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVolInterLock_2,value=1)
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVolInterLock_3,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.HighVolInterLock_0,sig_value=1,prom_name="High Voltage Inter Lock",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.HighVolInterLock_0,sig_value=0,prom_name="High Voltage Inter Lock",prom_state="0")

    @allure.title("WTI_高压绝缘信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982557(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.HighVolIsolation,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.HighVolIsolation,sig_value=1,prom_name="High Voltage Isolation",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.HighVolIsolation,sig_value=0,prom_name="High Voltage Isolation",prom_state="0")

    @allure.title("WTI_能量回收限制信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982558(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.EnergyRegenLimit_1,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.EnergyRegenLimit_2,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EnergyRegenLimit_1,sig_value=13,prom_name="Energy Regen Limit",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EnergyRegenLimit_1,sig_value=0,prom_name="Energy Regen Limit",prom_state="0")
  
    @allure.title("WTI_换挡失败信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982559(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.ShiftGear,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ShiftGear,sig_value=1,prom_name="Shift Gear",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ShiftGear,sig_value=2,prom_name="Shift Gear",prom_state="2")
        # self.bus_comm.stop_send_pdu("chassiscan1", "EcmChas1Fr09",)
        # sleep(3)
        # self.soa.get_and_event_check_warning_light_list(name="Shift Gear",state="1")
        # self.bus_comm.resume_send_pdu("chassiscan1", "EcmChas1Fr09",)

    @allure.title("WTI_换挡器故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982560(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.GearFailure,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.GearFailure,sig_value=1,prom_name="Gear Failure",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.GearFailure,sig_value=2,prom_name="Gear Failure",prom_state="2")
        # self.bus_comm.stop_send_pdu("chassiscan1", "EcmChas1Fr09",)
        # sleep(2)
        # self.soa.get_and_event_check_warning_light_list(name="Gear Failure",state="5")
        # self.bus_comm.resume_send_pdu("chassiscan1", "EcmChas1Fr09",)

    @allure.title("WTI_无动力输出")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982561(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.set_vehspd_gear(vehspd=7.0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.NoPowerOutput,sig_value=2,prom_name="No Power Output",prom_state="1")
        sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.NoPowerOutput,sig_value=2,prom_name="No Power Output",prom_state="0")

    @allure.title("WTI_弹射起步提示信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982563(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.LaunchModePrompt_1,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.LaunchModePrompt_2,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.LaunchModePrompt_1,sig_value=1,prom_name="Launch Mode Prompt",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.LaunchModePrompt_1,sig_value=2,prom_name="Launch Mode Prompt",prom_state="2")

    @allure.title("WTI_EPB指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982599(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWork_1,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWork_2,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.EPBWork_1,sig_value=1,prom_name="EPB Working",prom_state="2")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.EPBWork_2,sig_value=1,prom_name="EPB Working",prom_state="0")

    @allure.title("WTI_EPB制动故障灯红色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982601(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.BrakingSysFailedRed_1,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BrakingSysFailedRed_1,sig_value=1,prom_name="Red Braking System Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BrakingSysFailedRed_1,sig_value=0,prom_name="Red Braking System Failed",prom_state="0")

    @allure.title("WTI_EPB制动故障灯红色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1985387(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.BrakingSysFailedRed_1,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BrakingSysFailedRed_1,sig_value=1,prom_name="Red Braking System Failed",prom_state="1")
        sleep(1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BrakingSysFailedRed_1,sig_value=1,prom_name="Red Braking System Failed",prom_state="0")
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BrakingSysFailedRed_2,sig_value=1,prom_name="Red Braking System Failed",prom_state="1")

    @allure.title("WTI_EPB制动故障灯黄色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982600(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.BrakingSysFailedRed_1,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.BrakingSysFailedRed_2,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.BrakingSysFailedYellow,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BrakingSysFailedYellow,sig_value=1,prom_name="Yellow Braking System Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.BrakingSysFailedYellow,sig_value=2,prom_name="Yellow Braking System Failed",prom_state="0")

    @allure.title("WTI_HDC陡坡缓降指示灯黄色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982604(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.HDCGrey,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HDCGrey,sig_value=3,prom_name="HDC Yellow",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HDCGrey,sig_value=0,prom_name="HDC Yellow",prom_state="0")
        
    @allure.title("WTI_HDC陡坡缓降指示灯灰色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982603(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.HDCGrey,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HDCGrey,sig_value=1,prom_name="HDC Grey",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HDCGrey,sig_value=0,prom_name="HDC Grey",prom_state="0")
        
    @allure.title("WTI_HDC陡坡缓降指示灯绿色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982602(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.HDCGrey,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HDCGrey,sig_value=2,prom_name="HDC Green",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.HDCGrey,sig_value=0,prom_name="HDC Green",prom_state="0")
        
    @allure.title("WTI_ABS故障指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982605(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_wti_signal(func=WTI_Func.ABSFailed,value=0)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ABSFailed,sig_value=0,prom_name="ABS Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ABSFailed,sig_value=1,prom_name="ABS Failed",prom_state="2")
        
    @allure.title("WTI_ESC故障指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982606(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.ESCFailed,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ESCFailed,sig_value=0,prom_name="ESC Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ESCFailed,sig_value=1,prom_name="ESC Failed",prom_state="2")
        
    @allure.title("WTI_ESC关闭指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982607(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.ESCOff_1,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ESCOff_1,sig_value=1,prom_name="ESC Off",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ESCOff_1,sig_value=0,prom_name="ESC Off",prom_state="0")

    @allure.title("WTI_转向系统故障指示灯黄色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982699(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.SteeringSysFailedYellow,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SteeringSysFailedYellow,sig_value=1,prom_name="Yellow Steering Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SteeringSysFailedYellow,sig_value=2,prom_name="Yellow Steering Failed",prom_state="0")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SteeringSysFailedYellow,sig_value=3,prom_name="Yellow Steering Failed",prom_state="1")
        

    @allure.title("WTI_转向系统故障指示灯红色")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982700(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.SteeringSysFailedYellow,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SteeringSysFailedYellow,sig_value=2,prom_name="Red Steering Failed",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SteeringSysFailedYellow,sig_value=1,prom_name="Red Steering Failed",prom_state="0")
        
    @allure.title("WTI_悬架故障指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982703(self):
        self.sd_tester.write_single_ccp(58,0x02)
        self.sd_tester.write_single_ccp(950,0x01)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.SuspensionFailed_1,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SuspensionFailed_1,sig_value=3,prom_name="Suspension Failed Telltale",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SuspensionFailed_1,sig_value=2,prom_name="Suspension Failed Telltale",prom_state="0")

    @allure.title("WTI_悬架故障指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982704(self):
        self.sd_tester.write_single_ccp(58,0x02)
        self.sd_tester.write_single_ccp(950,0x02)
        self.sd_tester.reset_bgm()
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.SuspensionFailed_2,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SuspensionFailed_2,sig_value=2,prom_name="Suspension Failed Telltale",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.SuspensionFailed_2,sig_value=0,prom_name="Suspension Failed Telltale",prom_state="0")

    @allure.title("WTI_Autohold激活指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982704(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.AutoholdActiveGreen,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.AutoholStandbyGrey,value=1)
        self.bus_comm.set_gear_pos(Gear.Drv)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.AutoholdActiveGreen,sig_value=1,prom_name="Autohold Active Green",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.AutoholdActiveGreen,sig_value=0,prom_name="Autohold Active Green",prom_state="0")
        
    @allure.title("WTI_Autohold待命指示灯")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982705(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.AutoholdActiveGreen,value=0)
        self.bus_comm.set_wti_signal(func=WTI_Func.AutoholStandbyGrey,value=0)
        self.bus_comm.set_gear_pos(Gear.Drv)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.AutoholdActiveGreen,sig_value=1,prom_name="Autohold Standby Grey",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.AutoholdActiveGreen,sig_value=0,prom_name="Autohold Standby Grey",prom_state="0")
       
    @allure.title("WTI_转向故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982707(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.SteeringSysWarning,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteeringSysWarning,sig_value=1,prom_name="Steering Warning",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteeringSysWarning,sig_value=2,prom_name="Steering Warning",prom_state="2")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteeringSysWarning,sig_value=3,prom_name="Steering Warning",prom_state="3")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteeringSysWarning,sig_value=4,prom_name="Steering Warning",prom_state="4")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteeringSysWarning,sig_value=0,prom_name="Steering Warning",prom_state="0")

    @allure.title("WTI_转向故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1986150(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.SteeringSysWarning,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteeringSysWarning,sig_value=1,prom_name="Steering Warning",prom_state="1")
        self.bus_comm.stop_send_pdu("chassiscan1", "PscmChas1Fr03",)
        sleep(5)
        self.soa.get_and_event_check_warning_info_list(name="Steering Warning",info="4")
        self.bus_comm.resume_send_pdu("chassiscan1", "PscmChas1Fr03",)
    
    @allure.title("WTI_悬架故障信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982708(self):
        self.sd_tester.write_single_ccp(59,0x02)
        self.sd_tester.write_single_ccp(950,0x02)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.SuspensionFailed_2,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SuspensionFailed_2,sig_value=1,prom_name="Suspension Failed Warning",prom_state="2")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SuspensionFailed_2,sig_value=3,prom_name="Suspension Failed Warning",prom_state="3")

    @allure.title("WTI_制动液位信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982709_1982715(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.BrakingFluid,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.BrakingFluid,sig_value=1,prom_name="Braking Fluid",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.BrakingFluid,sig_value=0,prom_name="Braking Fluid",prom_state="0")

    @allure.title("WTI_EPB警告信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982710(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarning1,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBWarning1,sig_value=3,prom_name="EPB Warning1",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBWarning1,sig_value=0,prom_name="EPB Warning1",prom_state="0")

    @allure.title("WTI_EPB警告信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982713(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarning1,value=3)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarning2,value=3)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBWarning2,sig_value=1,prom_name="EPB Warning2",prom_state="2")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBWarning2,sig_value=4,prom_name="EPB Warning2",prom_state="3")
    
    @allure.title("WTI_释放EPB报警音")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982711(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime,value=1)
        self.bus_comm.set_vehspd(1000)
        sleep(1)
        self.bus_comm.set_vehspd(3836)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBWarningChime,sig_value=0,prom_name="EPB Chime Warning",prom_state="2")
        sleep(1)
        self.bus_comm.set_vehspd(1000)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBWarningChime,sig_value=0,prom_name="EPB Chime Warning",prom_state="1")
    
    @allure.title("WTI_EPB故障信息/驻车系统故障")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982714_1982712(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBFailure,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBFailure,sig_value=1,prom_name="EPB Sys Failure",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EPBFailure,sig_value=0,prom_name="EPB Sys Failure",prom_state="0")

    @allure.title("WTI_EBD警告信息")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1735845?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1982714(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_wti_signal(func=WTI_Func.EBDWaring,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=1,prom_name="EBD Warning",prom_state="1")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=2,prom_name="EBD Warning",prom_state="2")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=3,prom_name="EBD Warning",prom_state="3")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=4,prom_name="EBD Warning",prom_state="4")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=5,prom_name="EBD Warning",prom_state="5")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=6,prom_name="EBD Warning",prom_state="6")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=7,prom_name="EBD Warning",prom_state="7")
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.EBDWaring,sig_value=0,prom_name="EBD Warning",prom_state="0")


