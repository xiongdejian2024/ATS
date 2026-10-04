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
@allure.story("RelayControl_IGN2功能")
@pytest.mark.sam
class TestRelayCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([
                        "TailGateService_client", "CentralLockService_client", "VehicleModeService_client",
        ])
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(2)

    def after_each_func(self, ecu):
        # self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)
        sleep(3)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
            self.mix.restore_poweroutlet_relay_simulation_environment()
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("476442 KL15-2继电器断开_左后门Open继电器闭合")
    @pytest.mark.kl152
    @pytest.mark.smoke
    def test_caseid_118350(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 Inactive KL15-2断开_诊断激活线连接KL152闭合")
    @pytest.mark.kl152
    @pytest.mark.full
    def test_caseid_118360(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接') 
        self.bus_comm.check_DiagcComActv_sts(OnOff.On,300)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)
        self.mix.set_common_precontion(UsageMode.ABANDONED)
        self.bus_comm.check_usage_mode_status(UsageMode.ABANDONED) 
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)

    @allure.title("476442 Inactive KL15-2断开_诊断激活线连接KL152闭合")
    @pytest.mark.kl152
    @pytest.mark.smoke
    def test_caseid_118359(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接') 
        self.bus_comm.check_DiagcComActv_sts(OnOff.On,300)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 KL15-2继电器断开_尾门Open继电器闭合")
    @pytest.mark.kl152
    @pytest.mark.smoke
    def test_caseid_118354(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 KL15-2继电器断开_主驾门Open继电器闭合")
    @pytest.mark.kl152
    @pytest.mark.smoke
    def test_caseid_118353(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 KL15-2继电器断开_副驾门Open继电器闭合")
    @pytest.mark.kl152
    @pytest.mark.smoke
    def test_caseid_118352(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 KL15-2继电器断开_右后门Open继电器闭合")
    @pytest.mark.kl152
    @pytest.mark.smoke
    def test_caseid_118351(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 Inactive继电器KL152断开_UsageMode上切到Active继电器闭合")
    @pytest.mark.restart
    @pytest.mark.kl152
    @pytest.mark.full
    def test_caseid_118349(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.ACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.ACTIVE) 
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 Inactive继电器KL152断开_UsageMode上切到Convenience继电器闭合")
    @pytest.mark.restart
    @pytest.mark.kl152
    @pytest.mark.smoke
    def test_caseid_118348(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.bus_comm.check_usage_mode_status(UsageMode.CONVENIENCE) 
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("476442 Inactive继电器KL152断开_UsageMode上切到Driving继电器闭合")
    @pytest.mark.restart
    @pytest.mark.kl152
    @pytest.mark.full
    def test_caseid_118347(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_usage_mode_status(UsageMode.INACTIVE) 
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_usage_mode_status(UsageMode.DRIVING)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("IGN2继电器控制_Inactive&& 车速低于2km/h_IGN2计时3分钟断开")
    @pytest.mark.restart
    @pytest.mark.sanity
    @pytest.mark.longtime
    def test_caseid_1998910(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(10)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        sleep(1)  # 蓝牙远控又1s仲裁逻辑
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.55,veh_qf=VehSpdQf.AccurData)
        sleep(180.2)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0,veh_qf=VehSpdQf.AccurData)

    @allure.title("476442 Inactive继电器KL152闭合_外部闭锁1min_KL15-2断开")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118364(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)  # 蓝牙远控又1s仲裁逻辑
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(60)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)

    @allure.title("476442 Inactive继电器KL152断开_NFC解锁继电器闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118365(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("KL15-2Relay Control_Inactive模式下Telm解锁_KL15-2 ON")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118362(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("KL15-2Relay Control_Inactive模式下Telm解锁_KL15-2 ON")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118361(self):
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_DiagcComActv_sts(OnOff.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)

    @allure.title("Inactive诊断激活线连接KL152闭合_UsageMode下切到AbandonedKL15-2断开")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_118366(self):
        self.io.bgm_diag_line_up()
        logger.info(f'诊断激活线连接')
        self.bus_comm.check_DiagcComActv_sts(sts=OnOff.On, check_time=5)  # 诊断激活线上线要几分钟才能获取到Yes 
        self.soa.set_usagemode_up_and_down(up_usagemode=UsageMode.INACTIVE, down_usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.KL152, relaysts=RelaySts.Off)
