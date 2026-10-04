#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_batterysaver_ctrl_abc.py
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
@allure.story("BatterySaverControl功能")
@pytest.mark.sam
class TestBatterySaverRelayCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([
                        "TailGateService_client", 
                        "CentralLockService_client", 
                        "LightService_client",

        ])
        sleep(2)

    def before_each_func(self, ecu):
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(2)
        self.io.bgm_diag_line_down()
        logger.info(f'断开诊断激活线')
        sleep(30)
        self.sd_tester.update_serverdoipid(0x1002)# 重启BGM清除诊断激活线连接状态
        self.sd_tester.send_data([0x11, 0x01])
        sleep(30)
  
    def after_each_func(self, ecu):
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)

        
    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title(" 461687 节电继电器控制_Inactive&&激活灯光秀_节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_1986122(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "ExtrLtgStsStaticLtgShow", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.soa.hmi_set_light_show_active(status=True)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "ExtrLtgStsStaticLtgShow", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("461687 Power Saver 继电器控制_节电继电器断开_诊断激活线连接_节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_113160(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "ExtrLtgStsStaticLtgShow", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.bgm_diag_line_up()  # 诊断激活线连接
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
    
    @allure.title("461687 Power Saver 继电器控制_节电继电器断开_主驾门开启节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_113153(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "ExtrLtgStsStaticLtgShow", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
    
    @allure.title("461687 Power Saver 继电器控制_节电继电器断开_副驾门开启节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_113151(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("461687 Power Saver 继电器控制_节电继电器断开_左后门开启节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.santy
    def test_caseid_113148(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("461687 Power Saver 继电器控制_节电继电器断开_右后门开启节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_113149(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("461687 Power Saver 继电器控制_节电继电器断开_尾门门开启节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.smoke
    def test_caseid_113147(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("461687 Power Saver 继电器控制_节电继电器断开_舒适继电器闭合节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_113141(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1) 
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr34", "RlyCmftForClimaReq", 1)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    @allure.title("461687 Power Saver 继电器控制_闭锁节电继电器断开_解锁节电继电器闭合")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_113156(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        time.sleep(60)  # 闭锁后1min节电继电器断开
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)
        sleep(.5)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)

    # @allure.title("461687 Power Saver 继电器控制_解锁节电继电器闭合_外部闭锁节电继电器60s断开")
    # @pytest.mark.restart
    # @pytest.mark.smoke
    # def test_caseid_113138(self):
    #     self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr20", "DiagcComActv", 0)
    #     self.mix.set_common_precontion(UsageMode.INACTIVE)
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1) 
    #     self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.On)
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
    #     time.sleep(60)  # 闭锁后1min节电继电器断开
    #     self.bus_comm.check_relay_cmd(relaytype=RelayType.batterysaver, relaysts=RelaySts.Off)

