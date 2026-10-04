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
@allure.story("RelayControl功能")
@pytest.mark.sam
class TestRelayCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([
                        "TailGateService_client", 
                        "CentralLockService_client",
                        "KeyService_client",
                        "VehicleModeService_client",

        ])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.io.set_five_door_sts(sts=Door.close)
        sleep(2)

    def after_each_func(self, ecu):
        sleep(3)

    def after_class(self, ecu):
        try:
            self.mix.restore_poweroutlet_relay_simulation_environment()
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
            self.bus_comm.set_relay_control_proxy_req(proxy_req=OnOff1.Off)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("534738 inactive_LidarPowerReq=on_KL153:On")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1898832(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.Off)

    @allure.title("534738 inactive_LidarPowerReq=on_KL153:On")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_118371(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.Off)

    @allure.title("inactive_DiagcComActv_on")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_118376(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.bgm_diag_line_up()
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("DiagcComActv_Usagemode_Convenience")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118377(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off, check_time=2)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.bgm_diag_line_up()
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("UM=Abandoned&&诊断激活线连接KL15-3断开上切UM到ActiveKL15-3闭合")
    @pytest.mark.full
    def test_caseid_118379(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.io.bgm_diag_line_up()
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("KL15-3继电器控制_Abandoned&&诊断激活线连接KL15-3断开_UM上切到DrivingKL15-3闭合")
    @pytest.mark.full
    def test_caseid_118381(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.io.bgm_diag_line_up()
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("KL15-3继电器控制 Abandonedz&&诊断激活线连接KL15-3断开上切ConvenienceKL15-3闭合")
    @pytest.mark.full
    def test_caseid_118388(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.io.bgm_diag_line_up()
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("DiagcComActv_Usagemode_Convenience")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118396(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.bgm_diag_line_up()
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("KL15-3继电器控制_inactive_LidarPowerReq_计时200msKL15-3断开")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118400(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.Off)
        sleep(.2)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)

    @allure.title("534738_inactive_DiagcComActv_off")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118401(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.bgm_diag_line_up()
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("534738_inactive_DiagcComActv_off")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1988726(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)
        self.sd_tester.reset_bgm()
        sleep(5)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)

    @allure.title(" Crash继电器_无Crash触发&&UM=Drving_Crash继电器闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1988725(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff )
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)

    @allure.title("Fuel pump Relay功能安全_Drving&&CarMode！=Crash_FuPmpRlyCmd=：On")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1985019(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)

    @allure.title("Crash继电器_无Crash触发&&UM=Active_Crash继电器闭合")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1986864(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)

    # @allure.title("Abdnd&&RlyCrashForHvsysReq= on_300s燃油泵继电器断开")
    # @pytest.mark.restart
    # @pytest.mark.update
    # @pytest.mark.longtime
    # @pytest.mark.full
    # def test_caseid_118406(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(30)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", 1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)
    #     sleep(300.5)
    #     self.io.set_door(Drvr=Door.open)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", 0)

    # @allure.title("RlyCrashForHvsysReq_on_Usagemode_Active-Abondoned")
    # @pytest.mark.restart
    # @pytest.mark.update1
    # @pytest.mark.longtime
    # @pytest.mark.full
    # def test_caseid_118405(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(30)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", 1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
    #     sleep(300)
    #     self.io.set_door(Drvr=Door.open)  # Abandoned 总线数据None
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff, time_wait=1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", 0)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)

    # @allure.title("RlyCrashForHvsysReq_on_Usagemode_CONVENIENCE-Abondoned")
    # @pytest.mark.restart
    # @pytest.mark.update1
    # @pytest.mark.longtime
    # @pytest.mark.full
    # def test_caseid_118404(self):
    #     self.io.bgm_diag_line_down()
    #     logger.info(f'断开诊断激活线')
    #     sleep(30)
    #     self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
    #     self.sd_tester.send_data([0x11, 0x01])
    #     sleep(30)
    #     self.io.set_door(Drvr=Door.open)  # 开门上Convenience
    #     self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
    #     self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", 1)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)
    #     sleep(300.5)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff, time_wait=1)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr00", "RlyCrashForHvsysReq", 0)

    @allure.title("inactive诊断激活线连接_CrashRelay On")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_118403(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        sleep(.5)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOff)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes     
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay,OnOff=OnOffSafe1.OnOffSafeOn)

    @allure.title("KL15-3继电器控制_LidarPowerReq=On&&UM=AbandonedKL15-3断开_UM上切Driving_KL15-3闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118373(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        sleep(.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.Off)

    @allure.title("电源逻辑预警节电继电器禁用RlyPwrDistbnCmd1WdBattSaveCmd == OFF")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1988577(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_batter_saver_connect(battersaver=True)
        self.bus_comm.check_battery_save_prxy_req(battery_save=OnOff1.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
        self.bus_comm.check_battery_save_prxy_req(battery_save=OnOff1.Off)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(60.5)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)

    @allure.title("节电继电器控制 usagemode _上切Convenience")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_113174(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        sleep(.5)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("power outlet relay控制_inactive上切Active_power outlet On")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_113170(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.poweroutlet, relaysts=RelaySts.On)

    @allure.title("节电继电器控制_中控锁继电器断开_后背门开继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_113155(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("节电继电器控制_中控锁继电器断开_后背门开继电器闭合")
    @pytest.mark.smoke
    def test_caseid_113140(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)

    @allure.title("Power Saver 继电器控制_解锁节电继电器闭合_外部闭锁节电继电器60s断开")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_113139(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)

    @allure.title("电源逻辑预警节电继电器禁用RlyPwrDistbnCmd1WdBattSaveCmd == OFF")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_113138(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_batter_saver_connect(battersaver=True)
        self.bus_comm.check_battery_save_prxy_req(battery_save=OnOff1.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
        self.bus_comm.check_battery_save_prxy_req(battery_save=OnOff1.Off)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(60.5)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)

    @allure.title("节电继电器控制_节电继电器闭合_外部NFC锁车1min节电继电器off")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_113137(self):
        self.io.set_hood_sts(sts=HoodSts.Open)
        self.io.set_hood_sts(sts=HoodSts.Close)  # 防止重锁触发
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_batter_saver_connect(battersaver=True)
        self.bus_comm.check_battery_save_prxy_req(battery_save=OnOff1.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
        self.bus_comm.check_battery_save_prxy_req(battery_save=OnOff1.Off)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(60.5)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)

    @allure.title("KL15-2继电器断开_左后门Open继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_1987984(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)
        self.io.set_door(LeRe=Door.close)

    @allure.title("KL152继电器控制_inactive 门开右后门开继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_1987985(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)
        self.io.set_door(RiRe=Door.close)

    @allure.title("Inactive&&诊断激活线断开KL15-1断开_诊断激活线连接KL15-1闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118334(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.Off)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)

    @allure.title("KL151特殊case_Driving=>convenience&&诊断激活线连接_KL15-1断开1s后闭合")
    @pytest.mark.smoke
    def test_caseid_118345(self):
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_signal_thread_start('backbonefr', 'CemBackBoneFr14', 'RlyPwrDistbnCmd1WdIgnRlyCmd', timeout=1)  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        result_ori = self.bus_comm.check_signal_thread_stop('RlyPwrDistbnCmd1WdIgnRlyCmd')  
        logger.info(f'获取到的原始数据RlyPwrDistbnCmd1WdIgnRlyCmd为{result_ori}')
        result = get_signal_times_interval(result_ori, 0)  # 几点 会断开1s后闭合
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] != 1
        self.bus_comm.ipdu.reset_check_results()
        sleep(1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL151, relaysts=RelaySts.On)

    @allure.title("KL15-3继电器控制_LidarPowerReq=On&&UM=AbandonedKL15-3断开_UM上切Inactive_KL15-3闭合")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_118367(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE,down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)
        self.bus_comm.set_lidar_req(Lidar=RelaySts.Off)

    @allure.title("Abandoned&&诊断激活线连接KL15-3断开_上切UM至InactiveKL15-3闭合")
    @pytest.mark.smoke
    def test_caseid_118375(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)

    @allure.title("KL15-3继电器控制_Inctive&&诊断激活线连接KL15-3闭合_UM下切到AbaondonedKL15-3断开")
    @pytest.mark.full
    def test_caseid_118399(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL153, relaysts=RelaySts.Off)

    @allure.title("Usagemode_abandoned_RlyCrashForHvsysReq")
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_118408(self):
        self.bus_comm.set_crash_proxy_req(crash_proxy=OnOff1.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay, OnOff=OnOffSafe1.OnOffSafeOff)
        self.bus_comm.set_crash_proxy_req(crash_proxy=OnOff1.On)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay, OnOff=OnOffSafe1.OnOffSafeOn)
        sleep(300)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.crashrelay, OnOff=OnOffSafe1.OnOffSafeOff)
        self.bus_comm.set_crash_proxy_req(crash_proxy=OnOff1.Off)

    @allure.title("Climate relay控制_CRASH-Dyno_Climate relay on")
    @pytest.mark.sanity
    @pytest.mark.update
    def test_caseid_118465(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.CRASH)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.DYNO)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.DYNO)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.NORMAL)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        sleep(15)  # 恢复Crash 15s 安全状态影响解闭锁

    @allure.title("usagemode_abandoned上切driving_DiagcComActv")
    @pytest.mark.full
    @pytest.mark.update
    def test_caseid_118473(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)

    @allure.title("usagemode_abandoned上切active_DiagcComActv")
    @pytest.mark.full
    @pytest.mark.update
    def test_caseid_118472(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)

    @allure.title("Abandoned诊断激活线连接鼓风机继电器断开_UsageMode上切到Convenience继电器闭合")
    @pytest.mark.full
    @pytest.mark.update
    def test_caseid_118471(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)

    @allure.title("carmode_Crash上切Dyno_RlyCrashForClimaReq")
    @pytest.mark.full
    @pytest.mark.restart
    @pytest.mark.update
    def test_caseid_118469(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_clima_proxy_req(clima_proxy=OnOff1.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.CRASH)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.DYNO)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.DYNO)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.NORMAL)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        sleep(15)  # 恢复Crash安全状态

    @allure.title("Climate relay控制_CRASH-Dyno_Climate relay on")
    @pytest.mark.sanity
    @pytest.mark.update
    def test_caseid_118468(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.CRASH)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.FACTORY)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.FACTORY)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.NORMAL)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        sleep(15)  # 恢复Crash 15s 安全状态影响解闭锁

    @allure.title("Climate relay控制_CRASH-Dyno_Climate relay on")
    @pytest.mark.sanity
    def test_caseid_118467(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.CRASH)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.TRANSPORT)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.TRANSPORT)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.NORMAL)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        sleep(15)  # 恢复Crash 15s 安全状态影响解闭锁

    @allure.title("usagemode_abandoned上切driving")
    @pytest.mark.full
    def test_caseid_118464(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)

    @allure.title("usagemode_abandoned上切active")
    @pytest.mark.sanity
    def test_caseid_118463(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)

    @allure.title("usagemode_abandoned上切active")
    @pytest.mark.sanity
    def test_caseid_118462(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)

    @allure.title("Inactive ClimaReq On Climate relay On_Crash Climate relay Off")
    @pytest.mark.full
    @pytest.mark.restart
    @pytest.mark.update
    def test_caseid_118460(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_clima_proxy_req(clima_proxy=OnOff1.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.CRASH)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.NORMAL)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        sleep(15)  # 恢复Crash安全状态

    @allure.title("Climate relay控制_服务请求_Crash下切Fectory")
    @pytest.mark.full
    @pytest.mark.restart
    @pytest.mark.update
    def test_caseid_118459(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_clima_proxy_req(clima_proxy=OnOff1.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.CRASH)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.FACTORY)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.FACTORY)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.NORMAL)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        sleep(15)  # 恢复Crash安全状态

    @allure.title("Climate relay控制_服务请求_Crash下切Transport")
    @pytest.mark.full
    @pytest.mark.restart
    @pytest.mark.update
    def test_caseid_118458(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.Off)
        self.bus_comm.set_clima_proxy_req(clima_proxy=OnOff1.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.CRASH)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate, relaysts= RelaySts.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.TRANSPORT)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.TRANSPORT)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.climate,relaysts= RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode= CarMode.NORMAL)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        sleep(15)  # 恢复Crash安全状态