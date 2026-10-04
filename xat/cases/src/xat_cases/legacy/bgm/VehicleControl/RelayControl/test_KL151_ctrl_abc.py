#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_relaycontrol_ctrl.py
@Author      : qian.feng@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车设RelayControl
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


@allure.feature("车控车设")
@allure.story("RelayControl_IGN1功能")
@pytest.mark.sam
class TestRelayCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([
                        "TailGateService_client", "CentralLockService_client", "VehicleModeService_client",
        ])
        sleep(2)

    def before_each_func(self, ecu):
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(2)

    def after_each_func(self, ecu):
        sleep(3)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
            self.io.bgm_diag_line_up()  # 恢复诊断激活线连接状态
            self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
            self.io.set_five_door_sts(sts=Door.close)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    @allure.title("476445_无钥匙进入启用后禁用_KL15_OFF")
    @pytest.mark.samoke
    @pytest.mark.kl151
    def test_caseid_118329(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_RemPrkgSts(RemPrkgSts.PrkgAssiSysRemPrkgSts_OFF)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        self.soa.set_usagemode_withoutkey(TargetUsageMode.DRIVING)
        self.bus_comm.check_RemPrkgSts(RemPrkgSts.PrkgAssiSysRemPrkgSts_Remoteparkactive)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)
        self.soa.set_usagemode_withoutkey(TargetUsageMode.OFF)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_RemPrkgSts(RemPrkgSts.PrkgAssiSysRemPrkgSts_OFF)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)

    @allure.title("476445 诊断激活线断开&&InactiveKL15-1断开模式上切Active_KL15-1闭合")
    @pytest.mark.full
    @pytest.mark.kl151
    def test_caseid_118326(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)

    @allure.title("476445 诊断激活线断开&&InactiveKL15-1断开模式上切Drving_KL15-1闭合")
    @pytest.mark.samoke
    @pytest.mark.kl151
    def test_caseid_118325(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)

    @allure.title("476445_触发动力系统启动_KL15_1 On")
    @pytest.mark.sanity
    @pytest.mark.kl151
    def test_caseid_118324(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_PtActvnReq(PtActvnReq1.NoPtActvnReq)
        self.mix.service_change_usage_mode_and_check_result(UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off) 
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_Rdy)
        self.bus_comm.set_driving_preconditions()
        self.soa.set_usagemode_withoutkey(TargetUsageMode.DRIVING)
        self.bus_comm.check_PtActvnReq(PtActvnReq1.PtActvnReq)
        self.bus_comm.check_RemPrkgSts(RemPrkgSts.PrkgAssiSysRemPrkgSts_OFF)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_StrtgInProgs)
        time.sleep(5)
        self.bus_comm.check_PtActvnReq(PtActvnReq1.PtActvnReq)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)

    @allure.title("UM=Active下切到Inactive_KL151:Off")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118328(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)

    @allure.title("KL151继电器控制_Abandoned：KL151=OFF_UM上切Drving：KL151=On")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118340(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)

    @allure.title("Abandoned&&诊断激活线连接：KL151=OFF_UM上切Convenience：KL151=On")
    @pytest.mark.full
    def test_caseid_118341(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.io.bgm_diag_line_up()  # 恢复诊断激活线连接状态
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)

    @allure.title("IGN1继电器控制_UM=Drving下切到Inactive_IGN1= Off")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1898625(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)

    @allure.title("Ignition Power_Kl15-1继电器控制_IgnRlyCmdActr")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1986934(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        self.bus_comm.check_ignition_state(sts=OnOffSafe1.OnOffSafeOff)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_ignition_state(sts=OnOffSafe1.OnOffSafeOn)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        self.bus_comm.check_ignition_state(sts=OnOffSafe1.OnOffSafeOff)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_ignition_state(sts=OnOffSafe1.OnOffSafeOn)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)