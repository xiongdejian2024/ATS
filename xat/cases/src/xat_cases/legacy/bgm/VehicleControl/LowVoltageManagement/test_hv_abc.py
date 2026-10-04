#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_OuterRearView_ctrl.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设智能补电
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
        self.soa.update(["HighVoltageService_client","CentralLockService_client","LightService_client"])
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

    @allure.title("智能补电_IPM_abonedone触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919295(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(
            cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5
        )
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=5)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()

    @allure.title("智能补电_IPM_补电补电次数4次触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919303?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919303_1919296(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)
        self.bus_comm.check_low_volt_servse_sts(
            cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5
        )
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(ipm=True, time_wait=5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.valid)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter(10)
        self.mix.set_low_volt_servse_mode(ipm=False, time_wait=5)
    
    @allure.title("智能补电_ChargingLVInit PNC25_低压补电ok")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919303?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109480(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=0.5)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, 3.0)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)

    @allure.title("智能补电_ChargingLVInit PNC25_低压补电Nok")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919303?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109482(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk)
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=0.5)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, 15.0, 4.0)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)

    @allure.title("智能补电_优先级_低压and系统故障补电")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919303?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_109492(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=5)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.mix.set_low_volt_servse_mode(sys_falt=True, time_wait=20)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=13.5)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)

    @allure.title("智能补电_优先级_低压and系统故障补电")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919303?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_110414(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=5)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=5)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)    
    
    @allure.title("智能补电_优先级_IPM补电and系统故障补电")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919303?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919310(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(ipm=True, time_wait=5)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.mix.set_low_volt_servse_mode(sys_falt=True, time_wait=20)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=13.5)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
    

    @allure.title("智能补电_IPM_abonedone触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1983080(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=5)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.valid, timeout=60)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)

    
    @allure.title("智能补电_RTC_定时唤醒触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke_1
    def test_HvActive_caseid_1983064(self):
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.sd_tester.write_bms_did_value(0xBB09, write_data="0010", check_resp="6ebb09", wait_time=1)
        self.mix.network_sleep()
        sleep(2)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN6, sts=BusSendSts.Sleep)
        self.io.bgm_diag_line_up()
        self.io.tcam_kl15_up()

    @allure.title("智能补电_BMS_低电量触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982906(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.LoSOC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电压触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982961(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.LoVoltage)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电流动态")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982962(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.ChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电流静态")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982963(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.DisChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电量判别类型")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1984942(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.LoSOC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电压判别类型")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1984943(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.LoVoltage)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电流判别类型")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1984944(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.ChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电流判别类型")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1984945(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.DisChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    # @allure.title("智能补电_IPM_判别BMS")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46"
    # )
    # @pytest.mark.smoke
    # def test_HvActive_caseid_1983080(self):
    #     self.mix.set_usage_mode(UsageMode.INACTIVE)
    #     self.bus_comm.set_battery_stop_intelligent_charge(time_wait=3)
    #     self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
    #     self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
    #     self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
    #     self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
    #     self.mix.set_low_volt_servse_mode(ipm=True, time_wait=5)
    #     self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
    #     self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
    #     self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn)
    #     self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk)
    #     self.bus_comm.check_intelligent_charge_wakeup_counter(10)

    @allure.title("电源管理_DTC_F0 00 00")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/109491?projectId=46"
    )
    @pytest.mark.debug
    def test_HvActive_caseid_1919306(self):
        self.mix.set_dtc_precontion()
        # self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L0, '54')
        self.mix.generate_dtc_fault(dtc_fault=DTCFault.HeartBeatFail,last_time=6)
        # self.sd_tester.dtc_read_and_check(dtc=DTCFault.HeartBeatFail,dtc_sts=DTCSts.CurrentFailed)
        self.mix.set_dtc_precontion()
        # self.sd_tester.dtc_read_and_check(dtc=DTCFault.HeartBeatFail,dtc_sts=DTCSts.WithHistoryWithoutCurrent)
        # self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L0, '54')
        self.sd_tester.dtc_read_and_check(dtc=DTCFault.HeartBeatFail,dtc_sts=DTCSts.WithHistoryWithoutCurrent,fault_sts=False)

    @allure.title("智能补电_BMS_低压触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982965(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.DisChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.DisChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)


    @allure.title("智能补电_BMS_低压触发")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1986209(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.DisChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)


    @allure.title("智能补电_BMS_低电流补电停止")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982966(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.DisChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=10,low_soc=10)

    @allure.title("智能补电_BMS_低电流补电停止")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1988837(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.DisChrgnCurrent)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=20.0,low_soc=100.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soc=100.0)
        sleep(1)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.LoVoltage)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=20.0,low_soc=100.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=10.0,low_soc=10.0)

    @allure.title("智能补电_BMS_BGM低压")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1983137(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=1)
        self.mix.set_low_volt_servse_mode(low_volt=False,time_wait=1)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        # self.bus_comm.set_BMS_stop_req(low_sts=SocSts.LessOrEqual10Per,low_soh=1000,low_soc=1000)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=10,low_soc=10)

    @allure.title("智能补电_BMS_低电压触发Nok")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1983050(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.LoSOC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)


    @allure.title("智能补电_BMS_低电压PNC25")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1983140(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.LoSOC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.valid)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid,timeout=5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_RTC14天")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982903(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_HV_SOC_value(0)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_RTC_time(20160)

    @allure.title("智能补电_BMS_RTC2天")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982902(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_HV_SOC_value(1000)
        self.bus_comm.check_RTC_time(720)

    @allure.title("智能补电_BMS_低压告警IPM")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919312(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.mix.set_low_volt_servse_mode(ipm=True,time_wait=1)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
    
    @allure.title("智能补电_IPM_触发PNC25")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1919307(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.mix.set_low_volt_servse_mode(ipm=True,time_wait=1)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.valid)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter(10)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC25, NMSts.no_valid)

    @allure.title("智能补电_BMS_低压告警IPM")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_118736(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.mix.set_low_volt_servse_mode(ipm=True,time_wait=1)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)


    @allure.title("智能补电_BMS_低压告警OK清除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1983128_1983127(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
    
    @allure.title("智能补电_BMS_低压告告警导致配置项置位1")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1986123(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrEna, value=GeneralSts.Disable)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrEna, value=GeneralSts.Disable)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocEna, value=GeneralSts.Disable)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolEna, value=GeneralSts.Disable)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.ChrgnCurrEna, value=GeneralSts.Enable)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.DisChrgnCurrEna, value=GeneralSts.Enable)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.SocEna, value=GeneralSts.Enable)
        self.bus_comm.check_bms_related_signal(type=BMSWakeUpSetType.VolEna, value=GeneralSts.Enable)

    @allure.title("智能补电_BMS_低压告警NVM记忆")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.nvm
    def test_HvActive_caseid_1983130(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)

    @allure.title("智能补电_BMS_低压告警ug清除")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1983129(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)

    @allure.title("智能补电_BMS_低压告警重新计数")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1983133(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_intelligent_charge_wakeup_counter(4)
        # self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)

    @allure.title("智能补电_BMS_BattSocRaw")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1987452(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",0.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSocRaw2",0.0)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",50.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSocRaw2",50.0)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",100.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSocRaw2",100.0)

    @allure.title("智能补电_BMS_BattSocSts")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1987453(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSocSts",0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSoc2Sts",0)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSocSts",1)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSoc2Sts",1)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSocSts",2)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSoc2Sts",2)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSocSts",3)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSoc2Sts",3)    

    @allure.title("智能补电_BMS_BattSohRaw2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1987454(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSocSts",1)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSoc2Sts",1)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",100.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSocRaw2",100.0)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSOHLAMRaw",25.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSohRaw2",50.0)

    @allure.title("智能补电_BMS_BattSohRaw2")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1982905(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSocSts",1)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSoc2Sts",1)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",100.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSocRaw2",100.0)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSOHLAMRaw",25.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSohRaw2",50.0)

    @allure.title("智能补电_BMS_BattSnsrType")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    def test_HvActive_caseid_1982904(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSocSts",1)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSoc2Sts",0)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr05","BattSocRaw",100.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSocRaw2",70.0)
        self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr07","BattSOHLAMRaw",25.0)
        self.bus_comm.check_singal("connectivitycanfd","BgmConnectivityFr06","BattSohRaw2",100.0)

    @allure.title("智能补电_上电默认值_720分钟")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919278?projectId=46'
    )
    @pytest.mark.full
    def test_HvActive_caseid_1919278(self): 
        with allure.step(f"Step:设置inactive"):
            self.mix.set_usage_mode(UsageMode.INACTIVE)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为11.8 BattURaw
            self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        with allure.step(f"Step:重启BGM"):
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_HV_SOC_value(1000)
            self.bus_comm.set_batturaw(BattURaw=15)
            self.bus_comm.set_battiraw(BattIRaw=1)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscAvgRaw",-50.0)
            self.bus_comm.check_RTC_time(720)
            self.sd_tester.reboot_bgm_by_diag_hardreset()
            self.bus_comm.check_RTC_time(10)

    @allure.title("智能补电_RTC时间计算_持续增加")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919286?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919286(self): 
        with allure.step(f"Step:设置inactive"):
            self.mix.set_usage_mode(UsageMode.INACTIVE)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为12.7 BattURaw
            self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_HV_SOC_value(1000)
            self.bus_comm.set_batturaw(BattURaw=12.7)
            self.bus_comm.set_battiraw(BattIRaw=1.0)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscAvgRaw",-2500.0)
        with allure.step(f"Step:重启BGM"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step(f"检测是否TiLVBattChrgn=142"):
            self.bus_comm.check_RTC_time(142)
        with allure.step(f"补电1分钟 检测是否TiLVBattChrgn=261"):
            self.bus_comm.set_battiraw(BattIRaw=100.0)
            sleep(30)
            self.bus_comm.check_RTC_time(193)

    @allure.title("智能补电_RTC时间计算_持续减少")
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1919286?projectId=46'
    )
    @pytest.mark.full 
    def test_HvActive_caseid_1919285(self): 
        with allure.step(f"Step:设置inactive"):
            self.mix.set_usage_mode(UsageMode.INACTIVE)
        with allure.step(f"Step:设置BattURaw"):
            # LIN6信号 设置为12.7 BattURaw
            self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
            self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
            self.bus_comm.set_HV_SOC_value(1000)
            self.bus_comm.set_batturaw(BattURaw=12.7)
            self.bus_comm.set_battiraw(BattIRaw=1.0)
            self.bus_comm.set_singal("cem_lin6","BmsCem_Lin6Fr03","BattIQuiscAvgRaw",-2500.0)
        with allure.step(f"Step:重启BGM"):
            self.sd_tester.reboot_bgm_by_diag_hardreset()
        with allure.step(f"检测是否TiLVBattChrgn=142"):
            self.bus_comm.check_RTC_time(142)
        with allure.step(f"补电1分钟 检测是否TiLVBattChrgn=261"):
            self.bus_comm.set_battiraw(BattIRaw=-100.0)
            sleep(10)
            self.bus_comm.check_RTC_time(119)

    @allure.title("智能补电_BMS_低电压触发Nok")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1987715(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soc=100.0)
        sleep(1)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.LoSOC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("智能补电_BMS_低电压触发Nok")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1987716(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.OK)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Invalid,low_soc=100.0)
        sleep(1)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.LoSOC)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn,charg_vol_req=14.4)
        self.bus_comm.set_intelligent_charge_allow_sts(CnvnAllwd.NotOk, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)

    @allure.title("707302_门模块通讯检测_FLDoorComFltFlg")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987612(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_door_lock_sts(drv_lock=LockSts.Unlocked)
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Rst)
        self.bus_comm.stop_send_pdu("bodycan","DdmBodyFr04")
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Set)

    @allure.title("707302_门模块通讯检测_FRDoorComFltFlg")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987630(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_door_lock_sts(pass_lock=LockSts.Unlocked)
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Rst)
        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)
        self.bus_comm.set_door_lock_sts(pass_lock=LockSts.AllLocked)
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Rst)
        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Rst)

    @allure.title("707302_门模块通讯检测_RLDoorComFltFlg")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987631(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_door_lock_sts(lere_lock=LockSts.Unlocked)
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Rst)
        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)
        self.bus_comm.set_door_lock_sts(lere_lock=LockSts.AllLocked)  
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Rst)
        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Rst)

    @allure.title("707302_门模块通讯检测_RRDoorComFltFlg")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987632(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_door_lock_sts(rire_lock=LockSts.Unlocked)
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Rst)
        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)
        self.bus_comm.set_door_lock_sts(rire_lock=LockSts.AllLocked)  
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Rst)
        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Rst)

    @allure.title("707303_冗余电路控制_ER16RlySts_Close")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987633(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        self.sd_tester.write_bms_did_value(0xBB0A, write_data="96", check_resp="6eBB0A", wait_time=1)

        self.bus_comm.stop_send_pdu("bodycan","DdmBodyFr04")
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)

        self.bus_comm.set_singal("bodycan","IpmBodyFr01","IPMBattURaw", 7.5)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.sd_tester.recover_bms_did_to_default_value("0xBB02", "73")

    @allure.title("707303_冗余电路控制_ER16RlySts_open")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987634(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        self.sd_tester.write_bms_did_value(0xBB0A, write_data="96", check_resp="6eBB0A", wait_time=1)

        self.bus_comm.stop_send_pdu("bodycan","DdmBodyFr04")
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)

        self.bus_comm.set_singal("bodycan","IpmBodyFr01","IPMBattURaw", 7.5)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.bus_comm.set_singal("bodycan","IpmBodyFr01","IPMBattURaw", 12.5)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 0,timeout=5.0)
        self.sd_tester.recover_bms_did_to_default_value("0xBB0A", "5A")

    @allure.title("707303_冗余电路控制_ER16RlySts_open条件不满足FLDoorSysU")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987635(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        self.sd_tester.write_bms_did_value(0xBB0A, write_data="96", check_resp="6eBB0A", wait_time=1)

        self.bus_comm.stop_send_pdu("bodycan","DdmBodyFr04")
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)

        self.bus_comm.set_singal("bodycan","IpmBodyFr01","IPMBattURaw", 7.5)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.sd_tester.recover_bms_did_to_default_value("0xBB0A", "5A") 
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB0A, "5A")
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 0,timeout=5.0)   
    
    @allure.title("707303_冗余电路控制_ER16RlySts_open条件不满足FLDoorComFltFlg")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987636(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        self.sd_tester.write_bms_did_value(0xBB0A, write_data="96", check_resp="6eBB0A", wait_time=1)

        self.bus_comm.stop_send_pdu("bodycan","DdmBodyFr04")
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)

        self.bus_comm.set_singal("bodycan","IpmBodyFr01","IPMBattURaw", 7.5)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.bus_comm.set_singal("bodycan","DdmBodyFr04", "DoorDrvrLockSts", 1)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","FLDoorComFltFlg", 0)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB0A, "96")
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 0,timeout=5.0) 
        self.sd_tester.recover_bms_did_to_default_value("0xBB0A", "5A")

    @allure.title("707303_冗余电路控制_ER16RlySts_open条件不满足CarMod")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987637(self):
        self.sd_tester.write_ccp({965 : 0x1})
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        self.sd_tester.write_bms_did_value(0xBB0A, write_data="96", check_resp="6eBB0A", wait_time=1)

        self.bus_comm.stop_send_pdu("bodycan","DdmBodyFr04")
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)

        self.bus_comm.set_singal("bodycan","IpmBodyFr01","IPMBattURaw", 7.5)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB0A, "96")
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 0,timeout=5.0) 
        self.sd_tester.recover_bms_did_to_default_value("0xBB0A", "5A")
        self.mix.set_car_mode(CarMode.NORMAL)

    @allure.title("707303_冗余电路控制_ER16RlySts_open条件不满足UsgMod")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1985414?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.v210
    def test_HvActive_caseid_1987638(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        U1 = self.bus_comm.ipdu.get_recent_signal_raw_value(self.bus_comm.ipdu.infocanfd.BgmInfoCanFdFr18, 'FLDoorSysU')
        logger.info("门模块电压检测: FLDoorSysU {}".format(U1))
        self.sd_tester.write_bms_did_value(0xBB0A, write_data="96", check_resp="6eBB0A", wait_time=1)

        self.bus_comm.stop_send_pdu("bodycan","DdmBodyFr04")
        self.bus_comm.check_door_tx(drv_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","PdmBodyFr01")
        self.bus_comm.check_door_tx(pass_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RldmBodyFr01")
        self.bus_comm.check_door_tx(lere_tx=Flgsts.Flg1_Set)

        self.bus_comm.stop_send_pdu("bodycan","RrdmBodyFr01")
        self.bus_comm.check_door_tx(rire_tx=Flgsts.Flg1_Set)

        self.bus_comm.set_singal("bodycan","IpmBodyFr01","IPMBattURaw", 7.5)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 1,timeout=5.0)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.sd_tester.read_bms_did_value(0xBB0A, "96")
        self.bus_comm.check_singal("infocanfd","BgmInfoCanFdFr18","ER16RlySts", 0,timeout=5.0) 
        self.sd_tester.recover_bms_did_to_default_value("0xBB0A", "5A")
        
    @allure.title("智能补电_BMS_低压告警NVM记忆休眠唤醒")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.nvm
    def test_HvActive_caseid_1994466(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)

    @allure.title("智能补电_BMS_低压告警NVM记忆上下电")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.nvm
    def test_HvActive_caseid_1994467(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.NoWarning)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=5)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.NotOk)
        self.bus_comm.check_intelligent_charge_wakeup_counter()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_hv_volt_warning(LVChrgnFailWarn=Motorola.Warning)
        
    @allure.title("639618_ChrgnUReqMax_温度变化降低_411D读取")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1112
    def test_HvActive_caseid_1994871(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_battTraw(40.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.sd_tester.read_bms_did_value(0x411D, "74")
        self.bus_comm.set_battTraw(-8.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.sd_tester.read_bms_did_value(0x411D, "74")
        self.bus_comm.set_battTraw(-12.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")

    @allure.title("639618_ChrgnUReqMax_温度变化升高_411D读取")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1112
    def test_HvActive_caseid_1994872(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_battTraw(-20.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        self.bus_comm.set_battTraw(-8.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        self.bus_comm.set_battTraw(0.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.sd_tester.read_bms_did_value(0x411D, "74")

    @allure.title("639618_ChrgnUReqMax_重启默认值_411D读取")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1112
    def test_HvActive_caseid_1994873(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_battTraw(-20.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        self.bus_comm.set_battTraw(-8.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.bus_comm.set_battTraw(-8.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.sd_tester.read_bms_did_value(0x411D, "74")

    @allure.title("639618_ChrgnUReqMax_通讯故障_411D读取")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1112
    def test_HvActive_caseid_1994874(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_battTraw(-20.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        self.mix.set_low_volt_servse_mode(sys_falt=True, time_wait=20)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=13.5)
        self.sd_tester.read_bms_did_value(0x411D, "74")
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=20)
        self.bus_comm.set_battTraw(-20.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")

    @allure.title("639618_ChrgnUReqMax_低压触发恢复_411D读取")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1112
    def test_HvActive_caseid_1994875(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_battTraw(0.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.sd_tester.read_bms_did_value(0x411D, "74")
        self.mix.set_low_volt_servse_mode(low_volt=True, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_battTraw(-20.0)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.sd_tester.read_bms_did_value(0x411D, "74")

    @allure.title("477973_低压系统补电电压验证_ChrgnCurve1")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.test1202
    def test_HvActive_caseid_1985502(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.AWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.mix.set_low_volt_servse_mode(low_volt=True,time_wait=1)
        self.bus_comm.set_BMS_stop_req(low_sts=SocSts.Larger15Per,low_soh=50,low_soc=50.0)
        self.bus_comm.set_battTraw(-40)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        self.bus_comm.set_battTraw(70)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.Chrgn, charg_vol_req=14.4)
        self.sd_tester.read_bms_did_value(0x411D, "98")
        
    @allure.title("智能补电_BMS_RTC14天")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    def test_HvActive_caseid_1982903_1919284(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.set_battery_stop_intelligent_charge(time_wait=10)
        self.bus_comm.set_intelligent_charge_allow_sts(sts=CnvnAllwd.OK, time_wait=3)
        self.bus_comm.check_low_volt_servse_sts(cnv_req=CnvnReq.NotReqd, charg_vol_req=13.5)
        self.bus_comm.set_HV_SOC_value(0)
        self.bus_comm.set_BMS_wukeup_mode(bms_type=BattSnsrType.NAWC,wakeup_src=BMSWakeUpTrgSrc.NotReqd)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.bus_comm.check_RTC_time(20160)

    @allure.title("477973_电池传感器复位_BattSnsrRstReq")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1203
    def test_HvActive_caseid_1985505(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_singal("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        for i in range(5):   
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
            sleep(1)
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
            sleep(1)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        for i in range(3): 
            self.io.hazard_light_open()
            sleep(1)
            self.io.hazard_light_close()
            sleep(1)
        self.io.hazard_light_open()
        sleep(0.5)
        self.bus_comm.check_signal_always_is("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 1,timeout=5.0)
        sleep(20)

    @allure.title("477973_电池传感器复位_BattSnsrRstReq(手动)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1203
    def test_HvActive_caseid_1992545(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_singal("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        for i in range(5):   
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
            sleep(1)
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
            sleep(1)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        for i in range(2): 
            self.io.hazard_light_open()
            sleep(1)
            self.io.hazard_light_close()
            sleep(1)
        self.io.hazard_light_open()
        self.bus_comm.check_signal_always_is("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        sleep(20)

    @allure.title("477973_电池传感器复位_BattSnsrRstReq(反向用例)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1203
    def test_HvActive_caseid_1992546(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_singal("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        for i in range(5):   
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
            sleep(1)
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
            sleep(1)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        for i in range(3): 
            self.io.hazard_light_open()
            sleep(1)
            self.io.hazard_light_close()
            sleep(1)
        self.io.hazard_light_open()
        sleep(0.5)
        self.bus_comm.check_signal_always_is("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 1,timeout=5.0)
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_singal("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        sleep(20)

    @allure.title("477973_电池传感器复位_BattSnsrRstReq(反向用例)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1203
    def test_HvActive_caseid_1992547(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_singal("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        for i in range(5):   
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
            sleep(1)
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
            sleep(1)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        for i in range(3): 
            self.io.hazard_light_open()
            sleep(1)
            self.io.hazard_light_close()
            sleep(1)
        self.io.hazard_light_open()
        sleep(0.5)
        self.bus_comm.check_signal_always_is("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 1,timeout=5.0)
        self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.check_singal("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        sleep(20)

    @allure.title("477973_电池传感器复位_BattSnsrRstReq(反向用例)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.full
    @pytest.mark.test1203
    def test_HvActive_caseid_1992548(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.check_singal("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        for i in range(5):   
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
            sleep(1)
            self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
            sleep(1)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        sleep(30)
        for i in range(3): 
            self.io.hazard_light_open()
            sleep(1)
            self.io.hazard_light_close()
            sleep(1)
        self.io.hazard_light_open()
        self.bus_comm.check_signal_always_is("cem_lin6","CemCem_Lin6Fr02","BattSnsrRstReq", 0,timeout=5.0)

        
       