#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_lock_ctrl_abc.py
@Author      : qian.feng@jiduauto.com
@Time        : 2023/12/7 11:30
@Description: BGM车控车设中控锁
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
@allure.story("中控锁")
class TestLockCtrlAbc(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            [
                "CentralLockService_client",
                "DoorService_client",
                "TailGateService_client",
                "KeyService_client",
                "VehicleModeService_client",
                "GloveBoxService_client"
            ]
        )
        sleep(2)

    def before_each_func(self, ecu):
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83, 10: 0x2})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.io.set_five_door_sts(Door.close)        
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE, time_wait=1)  # 延时1s避免打断逻辑异常
        self.bus_comm.set_brake_pedal_sts(YesOrNo.No)
        self.mix.set_lock_unlock_visible_feedback_precondition(lockstate=LockState.UnLock)
        sleep(1) # 防止触发仲裁逻辑
        
    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
            self.mix.set_lock_unlock_visible_feedback_precondition(lockstate=LockState.UnLock)
            self.mix.set_seat_occpt_sts(OccupySts.NotOccupied)
            self.soa.set_convenience_duration(time=0)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def check_door_lock_ignored(self):
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorDrvrLockCmd", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorPassLockCmd", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorLeReLockCmd", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorRiReLockCmd", 0)

    @allure.title("540308 v9 HMI闭锁_内部方式开门解锁")
    @pytest.mark.smoke
    def test_caseid_114611(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.soa.hmi_set_door_opener_sts(
            door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open
        )
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt
        )

    @allure.title("498410 v20_中央锁状态_NFC闭锁")
    @pytest.mark.smoke
    def test_caseid_115520(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_event_sts(
            evn_update_sts=True, evn_trigsrc=LockTrigerSource.NFC
        )
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC
        )

    @allure.title("540308 v9 HMI闭锁_尾门解锁")
    @pytest.mark.smoke
    def test_caseid_114601(self):
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 0)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.soa.hmi_set_door_postion(DoorPos.Dirver, 10)
        self.bus_comm.set_singal("bodycan", "BgmBodyFr05", "DoorDrvrTargPercReqFromHmi", 10)
        sleep(.2)  # 3帧恢复默认值
        self.bus_comm.set_singal("bodycan", "BgmBodyFr05", "DoorDrvrTargPercReqFromHmi", 101)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("498410 v20_中央锁状态_NFC解锁")
    @pytest.mark.smoke
    def test_caseid_114308(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_event_sts(evn_update_sts=True, evn_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title(" 499022 v7 手动控制尾门解闭锁_外部方式闭锁-Trunlock钥匙无遗留_硬线关闭后尾箱中控Lock")
    @pytest.mark.full
    def test_caseid_1983486(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        sleep(3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0xB)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("499022 v7 手动控制尾门解闭锁_内部方式上锁-Trunlock-HMI关闭后尾箱重上锁")
    @pytest.mark.full
    def test_caseid_1983485(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(3)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("499022 v7 手动控制尾门解闭锁_Unlock关闭后备箱:后尾箱关闭中控不上锁")
    @pytest.mark.full
    def test_caseid_1983484(self):
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(3)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone5", 1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    # @allure.title("498409 v13 门锁联动_四门及尾门开启_NFC闭锁")
    # @pytest.mark.full
    # def test_caseid_110338(self):
    #     self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
    #     self.io.set_door(Drvr=Door.open)
    #     sleep(1)
    #     self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
    #     self.bus_comm.send_nfc_cmd()
    #     sleep(2.5)  # 长刷
    #     self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
    #     self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
    #     self.io.set_door(Drvr=Door.close)
    #     sleep(3)  # 关门落锁超时10s
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("498409 v13 门锁联动_四门及尾门开启_NFC短刷不闭锁")
    @pytest.mark.sanity
    def test_caseid_114722(self):
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.send_nfc_cmd()
        sleep(1.5)  # 长刷
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Close)
        self.io.set_five_door_sts(Door.close)
        sleep(2)  # 关门落锁超时10s
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title(" 497859 v16 离车落锁设置项关闭_离车中央不上锁")
    @pytest.mark.full
    def test_caseid_110353(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(3)  # 等待NVM存储
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_walk_away_lock_cmd()
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  # 上一次是蓝牙解锁

    @allure.title("494582 v13 车辆驻车状态RKE中央锁定可见反馈")
    @pytest.mark.full
    def test_caseid_115505(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("494582 v13 中央闭锁_右前门开RKE仅闭锁_整车不闭锁")
    @pytest.mark.full
    def test_caseid_119273(self):
        self.io.set_door(Pass=Door.open)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("497859 v16 离车落锁_HMI禁用离车落锁功能")
    @pytest.mark.full
    def test_caseid_110352(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)
        sleep(.2)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        
    @allure.title("498408 v14 有效钥匙在Zone 7近车解锁开门")
    @pytest.mark.full
    def test_caseid_1959943(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 1)
        # sleep(.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("498408 v14 近车解锁_主驾半锁位置2段请求前关门指令打断open")
    @pytest.mark.full
    def test_caseid_1985326(self):
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.soa.get_and_check_door_action_req(checktype= CheckInterfaceType.CheckNotify, 
                                               doorid= DoorId.kDoorFrontLeft, 
                                               dooraction=DoorAction.OpenMinAngle, 
                                               triggerId=DoorActionTriggerId.RemoteKey,
                                               time_wait=1)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.HalfClsd)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)  
        # self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
        #                                     trigger_src=LockTrigerSource.KeyRem)  # Open中断不发
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close,
                                            trigger_src=LockSource.HMI)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("466341 v11 Crash解锁失败同步HMI_仅副驾门锁处于Unlock_Crash解锁失败状态监测为On")
    @pytest.mark.smoke
    def test_caseid_1985295(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE,CarMode.CRASH)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        sleep(.5)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOff)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd, pass_lock=Locksts.Ukwn,
                          lere_lock=Locksts.Lockd, rire_lock=Locksts.SafeLockd)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOn)
    
    @allure.title("466341 v11 Crash解锁失败同步HMI_任意门锁信号跳变_Crash解锁失败状态监测")
    @pytest.mark.smoke
    def test_caseid_1985294(self):
        self.mix.set_common_precontion(UsageMode.INACTIVE,CarMode.CRASH)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        sleep(.5)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOff)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOn)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Ukwn, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOn)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Lockd, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOn)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.SafeLockd, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOn)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Unlckd, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOff)
        
    @allure.title("498408 v14 近车解锁_1段开门800ms计时内延时0.5s&&钥匙置位_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1985328(self):
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 0)
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        sleep(.5)  # 等待配置生效
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        # self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
        #                                     trigger_src=LockTrigerSource.KeyRem)
        sleep(.5)
        # self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 1)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)


    @allure.title("498408 v14 近车解锁_钥匙不在Zone7_主驾开门仅一次")
    @pytest.mark.full
    def test_caseid_1985329(self):
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 0)
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=LockTrigerSource.KeyRem)
        sleep(.5)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,
                                            trigger_src=LockTrigerSource.NoTrigSrc)


    @allure.title("498408 v14 近车解锁_1段开门800ms计时超时钥匙置位&7主驾门Clsd状态_2段开门请求Open不发")
    @pytest.mark.full
    def test_caseid_1985330(self):
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 0)
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=LockTrigerSource.KeyRem)
        sleep(1)
        # self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 1)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,
                                            trigger_src=LockTrigerSource.NoTrigSrc)

    @allure.title("498408 v14 近车解锁_小角度开门800ms计时超时_有有效钥匙&&主驾门Open状态_2段开门请求open")
    @pytest.mark.full
    def test_caseid_1985331(self):
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 0)
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=LockTrigerSource.KeyRem)
        self.io.set_door(Drvr=Door.open)
        sleep(1)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 1)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=LockTrigerSource.KeyRem)

    @allure.title("498408 v14 近车解锁_800ms<T<30s_有有效钥匙&&主驾门Open状态_2段开门请求open")
    @pytest.mark.full
    def test_caseid_1985332(self):
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 0)
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=LockTrigerSource.KeyRem)
        self.io.set_door(Drvr=Door.open)
        sleep(20)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone7", 1)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("497859 v16 离车落锁_尾门开关闭中MoveDowBrkg&&10s内尾门关闭中央落锁")
    @pytest.mark.full
    def test_caseid_1985325(self):
        # self.io.set_door(Trunk=Door.open)        
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 7)  # MoveDowBrkg
        self.soa.hmi_event_check_tailgate_movests(MoveSts.ClosingBreak)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3) # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        sleep(5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1) 
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.io.set_door(Trunk=Door.close) 
        sleep(2) # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("497859 v16 离车落锁_尾门开关闭中MoveDow&&10s超时尾门关闭中央不落锁")
    @pytest.mark.v200only
    @pytest.mark.full
    def test_caseid_1985542(self):
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)  # MoveDown
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closing)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(10)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁_尾门全开&&10s内尾门关闭中央不落锁")
    @pytest.mark.full
    def test_caseid_1985619(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 5)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Opened)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(8)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        
    @allure.title("497859 v16 离车落锁_尾门Ukwn&&10s内尾门关闭中央不落锁")
    @pytest.mark.full
    def test_caseid_1985621(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 0) 
        self.soa.hmi_event_check_tailgate_movests(MoveSts.NA) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(1)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(9)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁_尾门MovgUp&&10s内尾门关闭中央不落锁")
    @pytest.mark.full
    def test_caseid_1985620(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Opening)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(9)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁_497859 v16 离车落锁_尾门MovgUpBrkg&&10s内尾门关闭中央不落锁")
    @pytest.mark.full
    def test_caseid_1985624(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3) 
        self.soa.hmi_event_check_tailgate_movests(MoveSts.OpeningBreak) 
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(9)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁_尾门StopDurgOpen&&10s内尾门关闭中央不落锁")
    @pytest.mark.full
    def test_caseid_1985626(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 4)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Hover)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(9)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁_尾门StopDurgClsd&&10s内尾门关闭中央不落锁")
    @pytest.mark.full
    def test_caseid_1985627(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 8)  
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(9)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁_尾门StopMinPntForCls&&10s内尾门关闭中央不落锁")
    @pytest.mark.full
    def test_caseid_1985628(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 10)  
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(8)
        self.io.set_door(Trunk=Door.close) 
        sleep(2)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁_尾门FullClsd&&尾门关闭中央落锁")
    @pytest.mark.full
    def test_caseid_1985629(self):
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("497859 v16 离车落锁_四门全开&&10s超时关闭_中央不落锁")
    @pytest.mark.full
    def test_caseid_1985632(self):
        self.io.set_door(Drvr=Door.open,Pass=Door.open, LeRe=Door.open, RiRe=Door.open)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(11)
        self.io.set_door(Drvr=Door.close,Pass=Door.close, LeRe=Door.close, RiRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title(" 499022 v7 手动控制尾门解闭锁_外部方式闭锁-Trunlock钥匙遗留_硬线关闭后尾箱中控TrLock")
    @pytest.mark.full
    def test_caseid_1983488(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        sleep(3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Close)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("462992 v9 尾门解锁_重启记忆原状态_TrUnLock")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_110359(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(1)  # 等待NVM存储
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        sleep(2)  # 等待NVM存储
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.io.io_reset_bgm()
        sleep(5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("474633 v6 中央锁定_HMI开启尾门解锁")
    @pytest.mark.sanity
    def test_caseid_114600(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("497859 v16 离车落锁成功_中控锁状态+闭锁源信号监测")
    @pytest.mark.full
    def test_caseid_110349(self):
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_walk_away_lock_cmd()
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        
    @allure.title("462997 v22 Driving模式下远控闭锁")
    @pytest.mark.sanity
    def test_caseid_114353(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.check_door_lock_ignored()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        
    @allure.title("657337 v1 门锁联动仲裁逻辑_车门处于关闭状态")
    @pytest.mark.sanity
    def test_caseid_1919345(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={94: 0x02})
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.io.set_five_door_sts(Door.close)
        self.io.set_hood_sts(HoodSts.Close)
        self.bus_comm.set_singal("infocanfd", "BgmInfoCanFdDevFr03", "KeyReadStsToLockgBLEKey0", 2)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        # self.bus_comm.set_singal("infocanfd", "BgmInfoCanFdDevFr03", "KeyReadStsToLockgBLEKey0", 2)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498583 v26 车速自动落锁_主驾门开启车速不落锁")
    @pytest.mark.full
    def test_caseid_115513(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_vehspd(3.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("[Convenience]模式下主驾无占座远控闭锁_1.5内模式未下切闭锁Fail+")
    @pytest.mark.full
    def test_caseid_114357(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("462997 v22 远控闭锁_[Active]模式下+主驾有占座闭锁请求1s内模式下切到Inactive_中控上锁")
    @pytest.mark.full
    def test_caseid_1892750(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)  # 远控占位逻辑在Tcam
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("526238 v8 Driving模式下远控解锁禁用")
    @pytest.mark.full
    def test_caseid_114350(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        
    @allure.title("645007 v4 kv闭锁钥匙遗留车内可闭锁")
    @pytest.mark.full
    def test_caseid_115510(self):
        self.mix.set_common_precontion(ccp={94: 0x02})
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone6", 1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("645007 v4 KV 闭锁寻车内外所有区域钥匙")
    @pytest.mark.full
    def test_caseid_114309(self):
        self.mix.set_common_precontion(ccp={94: 0x02})
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone2", 1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        
    @allure.title("645007 v4 KV 闭锁寻车内外所有区域钥匙")
    @pytest.mark.full
    def test_caseid_114306(self):
        self.mix.set_common_precontion(ccp={94: 0x02})
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullOpend)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone2", 1)
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498410_v20_中央锁状态_解闭锁失败event监测检测")
    @pytest.mark.full
    def test_caseid_110342(self):
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 7)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("RKE关门上锁DelayCloseDoor计时期间Telm关门上锁_远控关门上锁忽略")
    @pytest.mark.full
    def test_caseid_1919327(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgIn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closing, isopen=True, antipinch=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem)
        sleep(1)  # 远控和RKE 1s内会 忽略
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=1)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("462858_v26 relocking_RKE解锁_钥匙遗留车内重锁不执行")
    @pytest.mark.full
    def test_caseid_1985926(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr17", "BLEKeyPrsntStsZone6", 1)  
        sleep(30)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        
    @allure.title("466243 v5 避免意外KV行为的机制_闭锁计时1s内解锁请求忽略")
    @pytest.mark.full
    def test_caseid_1943258(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("466243 v5 避免意外KV 行为的机制_解锁计时1s内上锁请求忽略")
    @pytest.mark.sanity
    def test_caseid_1943269(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("540308 v9 HMI闭锁_尾门解锁")
    @pytest.mark.sanity
    def test_caseid_1983327(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.soa.hmi_set_tailgate_mode(cmd=TailGateMode.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt
        )

    @allure.title("498582 v18 kv解锁_HMI闭锁_KV解锁禁用")
    @pytest.mark.sanity
    def test_caseid_1987141(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("498582 kv解锁_RKE闭锁PE解锁_中央解锁")
    @pytest.mark.sanity
    def test_caseid_1987142(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498582 KV解锁_远控闭锁PE解锁_中央解锁")
    @pytest.mark.full
    def test_caseid_1987143(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498582 KV解锁_NFC闭锁PE解锁_中央解锁")
    @pytest.mark.full
    def test_caseid_1987144(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498582 KV解锁_PE闭锁PE解锁_中央解锁")
    @pytest.mark.full
    def test_caseid_1987145(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        time.sleep(2)  # 避免防玩
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498582 KV解锁_重锁PE解锁_中央解锁")
    @pytest.mark.full
    def test_caseid_1987146(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1) # 蓝牙和远控有1s仲裁逻辑
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut, timeout=2)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        
        
    @allure.title("498582 KV解锁_驻车舒享模式下PE解锁_PE解锁可用")
    @pytest.mark.full
    def test_caseid_1987147(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        time.sleep(3)  # 等待3s关闭维持上电恢复环境
        self.soa.set_convenience_duration(time=0)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)

    @allure.title("498582 KV解锁_内部其它方式闭锁&&维持上电模式关PrkgCmftModTiCtrl=0_PE解锁禁用")
    @pytest.mark.full
    def test_caseid_1987155(self):
        self.mix.set_common_precontion(ccp={94: 0x80, 142:0x83})
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        time.sleep(2)  # 避免防玩触发
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        time.sleep(3) # 延时3s获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("498582 KV解锁_外部其它方式闭锁PE解锁_中央解锁")
    @pytest.mark.full
    def test_caseid_1987156(self):
        self.mix.set_common_precontion(ccp={94: 0x80, 142:0x83})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        time.sleep(2)  # 避免防玩触发
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498582 KV解锁_车速落锁PE解锁_PE解锁禁用")
    @pytest.mark.full
    def test_caseid_1987157(self):
        self.mix.set_common_precontion(UsageMode.DRIVING)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)

    @allure.title("KV解锁_内部开关闭锁&&Trunlock_PE可解锁")
    @pytest.mark.full    
    def test_caseid_1987162(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)
        self.soa.hmi_set_tailgate_mode(cmd=TailGateMode.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        time.sleep(2)  #避免防玩
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
 
    @allure.title("494881 尾门kv解锁_HMI闭锁_尾门KV解锁禁用")
    @pytest.mark.v200
    @pytest.mark.sanity
    def test_caseid_1987163(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("494881 尾门kv解锁_RKE闭锁尾门KV解锁_尾门锁可解TrUnlock")
    @pytest.mark.sanity
    def test_caseid_1987187(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("494881 尾门kv解锁_远控闭锁尾门kv解锁_尾门锁可解TrUnlock")
    @pytest.mark.full
    def test_caseid_1987190(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("494881 尾门kv解锁_NFC闭锁尾门kv解锁_尾门锁可解TrUnlock")
    @pytest.mark.full
    def test_caseid_1987191(self):
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("494881 尾门kv解锁_PE闭锁尾门kv解锁_尾门锁可解TrUnlock")
    @pytest.mark.full
    def test_caseid_1987192(self):
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        time.sleep(2)  # 避免防玩
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("494881 尾门kv解锁_重锁尾门kv解锁_尾门锁可解TrUnlock")
    @pytest.mark.full
    def test_caseid_1987193(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("494881 尾门kv解锁_PrkgCmftModTiCtrl!=0&PE解锁_尾门锁可解TrUnlock")
    @pytest.mark.full
    def test_caseid_1987194(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.set_convenience_duration(time=0)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)

    @allure.title("494881 尾门kv解锁_内部其它方式闭锁&&维持上电模式关PrkgCmftModTiCtrl=0_尾门解锁禁用")
    @pytest.mark.v200
    @pytest.mark.full
    def test_caseid_1987195(self):
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3) # 延时3s获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("494881 尾门kv解锁_外部其它方式闭锁尾门kv解锁_尾门锁可解TrUnlock")
    @pytest.mark.full
    def test_caseid_1987196(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        time.sleep(2)  # 避免防玩触发
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("494881 尾门kv解锁_车速落锁尾门kv解锁_尾门kv锁禁用")
    @pytest.mark.full
    def test_caseid_1987197(self):
        self.mix.set_common_precontion(UsageMode.DRIVING)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3) # 延时3s获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
 
    @allure.title("449494 外开关解锁开启尾门_离车落锁外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def  test_caseid_1987212(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("498582 KV解锁_离车落锁PE解锁_中央解锁")
    @pytest.mark.full
    def test_caseid_1987213(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)

    @allure.title("498582 KV解锁_LockTrigerSource=InsOthPE解锁禁用_维持上电后开后PE解锁解禁用")
    @pytest.mark.full
    def test_caseid_1987286(self):
        self.mix.set_common_precontion(ccp={94: 0x02})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3)
        sleep(.5)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)     
        self.soa.set_convenience_duration(time=0)

    @allure.title("498582 LockTrigerSource=InsSwt&&维持上电后开_PE解锁禁用")
    @pytest.mark.full
    def test_caseid_1987287(self):
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)
        self.soa.set_convenience_duration(time=0)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)

    @allure.title("449494 外开关解锁开启尾门_仅LockTrigerSource=InsOth尾门外按键不可用_内部其它方式&&PrkgCmftModTiCtrl=0外开关开尾门尾门Open可释放")
    @pytest.mark.full
    def test_caseid_1987285(self):
        self.mix.set_common_precontion(ccp={94: 0x80, 142:0x83})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        time.sleep(2)  # 避免防玩触发
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        time.sleep(3) # 延时3s获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        self.mix.set_common_precontion(UsageMode.CONVENIENCE)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_四门及尾门关HMI关门上锁_success")
    @pytest.mark.smoke
    def test_caseid_1987570(self):  
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.All, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False) 
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_主驾门开10s内关闭_success")
    @pytest.mark.smoke
    def test_caseid_1987704(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=False, antipinch=False)   
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(8)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)   
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_尾门开10s内关闭_success")
    @pytest.mark.sanity
    def test_caseid_1987705(self):
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.FullOpend)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Opened)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(8)
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.FullClsd)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_副驾门开10s超时关闭_Fail")
    @pytest.mark.sanity
    def test_caseid_1987706(self):
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=False, antipinch=False) 
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(10.1)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_尾门开10s超时关闭_Fail")
    @pytest.mark.sanity
    def test_caseid_1987707(self):
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.FullOpend)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Opened)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req=DoorOpenerReq.Close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(10.1)
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.FullClsd)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_左后门开10s内尾门触发防夹_Fail")
    @pytest.mark.full
    def test_caseid_1987708(self):
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=False, antipinch=False) 
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 1)
        time.sleep(2)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearLeftDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False) 
        time.sleep(8)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 0)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_右后门开10s内右后门触发防夹_Fail")
    @pytest.mark.full
    def test_caseid_1987709(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=False, antipinch=False)   
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiReAntiPnch", 1)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=False, antipinch=True)   
        time.sleep(2)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=True)  
        time.sleep(8)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiReAntiPnch", 0)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_计时期间触发RKE闭锁_RKE闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1987819(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opened,isopen=False, antipinch=False)   
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Hmi)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Close, trigger_src=DoorOpenSource.HMI)      
        time.sleep(3)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        time.sleep(.5)
        # self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kClosed) 
        self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullClsd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_10s内右后门closing change to opening_计时中断")
    @pytest.mark.full
    def test_caseid_1987711(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgIn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closing,isopen=False, antipinch=False)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opening,isopen=False, antipinch=False)  
        time.sleep(7)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_10s主驾门opening to Hover 10s内对应侧门关闭_Fail")
    @pytest.mark.full
    def test_caseid_1987712(self):
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opening,isopen=False, antipinch=False)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close)
        time.sleep(3) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopDurgOpen)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Hover,isopen=False, antipinch=False)  
        time.sleep(3) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("MSO-SVRIF-655 HMI关门上锁_10s右后门Hover change to opening_计时中断")
    @pytest.mark.full
    def test_caseid_1987713(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.StopDurgOpen)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Hover,isopen=False, antipinch=False)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close)
        time.sleep(3)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opening,isopen=False, antipinch=False)
        time.sleep(3)  
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("P档自动解锁激活_挡位未切换")
    @pytest.mark.sanity
    def test_caseid_1982365(self):
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)
        sleep(.2)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr03", "GearLvrIndcn", 0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=3)

    @allure.title("P档自动解锁激活_驾驶员在DrvrPrsnt=Yes_P档自动解锁")
    @pytest.mark.sanity
    def test_caseid_119082(self):
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.bus_comm.set_seat_occpt_sts(SeatId.All, SeatPresSts.NoPres)
        self.bus_comm.set_blt_sts(SeatId.FrontLeft, BltFltSts.NoFault, BltLockSts.Unlock)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.No)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)       
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.Yes)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.set_gear_pos(Gear.Drv)
        time.sleep(.2)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3)       
        
    @allure.title("644937 v2 P档自动解锁激活_主驾安全带上锁中控解锁")
    @pytest.mark.sanity
    def test_caseid_119084(self):
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.bus_comm.set_seat_occpt_sts(SeatId.All, SeatPresSts.NoPres)
        self.bus_comm.set_blt_sts(SeatId.FrontLeft, BltFltSts.NoFault, BltLockSts.Lock)
        time.sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)       
        self.bus_comm.set_gear_pos(Gear.Drv)
        sleep(.5)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3)   

    @allure.title("P档自动解锁激活_车内无占座主驾安全带未上锁&&DrvrPrsnt!=Yes中控不解锁")
    @pytest.mark.sanity
    def test_caseid_119086(self):
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.bus_comm.set_seat_occpt_sts(SeatId.All, SeatPresSts.NoPres)
        self.bus_comm.set_blt_sts(SeatId.FrontLeft, BltFltSts.NoFault, BltLockSts.Unlock)
        time.sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)       
        self.bus_comm.set_gear_pos(Gear.Drv)
        sleep(.5)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=3)    

    @allure.title("494582 v13 中央闭锁_InActive模式RKE闭锁成功")
    @pytest.mark.sanity
    def test_caseid_119271(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("backbonefr", "BbmBackBoneFr04", "EpbLampReqSecEpbLampReq", 0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=2)

    @allure.title("MSO-SREQ-21365 蓝牙闭锁踩刹车解锁")
    @pytest.mark.sanity
    def test_caseid_1987356(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=2)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 Telm闭锁踩刹车解锁")
    @pytest.mark.sanity
    def test_caseid_1987383(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 PE闭锁踩刹车解锁")
    @pytest.mark.sanity
    def test_caseid_1987384(self):
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheThirdKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.TempBleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.Temp_BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheThirdKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)
        
    @allure.title("MSO-SREQ-21365 离车落锁踩刹车解锁")
    @pytest.mark.full
    def test_caseid_1987385(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheFourthKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.IcceBleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.ICCE_BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheFourthKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 外部其它方式闭锁踩刹车解锁")
    @pytest.mark.sanity
    def test_caseid_1987386(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth, timeout=2)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.CccNfcBleUwbKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.CCC_NFC_BLE_UWB_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 NFC闭锁踩刹车解锁")
    @pytest.mark.sanity
    def test_caseid_1987387(self):
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheFourthKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.CccNfcBleKey, time_wait=5)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.CCC_NFC_BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=5)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheFourthKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 Relocking闭锁踩刹车解锁")
    @pytest.mark.full
    def test_caseid_1987388(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=2)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut, timeout=2)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheFourthKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=5)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.TheFourthKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 Hmi闭锁踩刹车不解锁")
    @pytest.mark.sanity
    def test_caseid_1987390(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.SecondKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=5)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.SecondKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 内部其它方式闭锁踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987391(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth, timeout=2)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.SecondKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.SecondKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 车速落锁踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987392(self):
        self.mix.set_common_precontion(UsageMode.DRIVING)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.BleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 蓝牙闭锁钥匙未连接踩刹车不解锁")
    @pytest.mark.sanity
    def test_caseid_1987393(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=3)
        
    @allure.title("MSO-SREQ-21365 远控闭锁钥匙未连接踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987394(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm, timeout=3)

    @allure.title("MSO-SREQ-21365 PE闭锁钥匙未连接踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987395(self):
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        time.sleep(2)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)
 
    @allure.title("MSO-SREQ-21365 离车落锁无钥匙连接踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987396(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)

    @allure.title("MSO-SREQ-21365 NFC闭锁无钥匙连接踩刹车不解锁")
    @pytest.mark.sanity
    def test_caseid_1987397(self):
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC, timeout=3)

    @allure.title("MSO-SREQ-21365 外部其它方式闭锁无钥匙连接踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987398(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth, timeout=3)

    @allure.title("MSO-SREQ-21365 Relocking闭锁无钥匙连接踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987399(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut, timeout=3)
        
    @allure.title("474640 NFC解锁_尾门解锁NFC刷卡中控锁解锁")
    @pytest.mark.sanity
    def test_caseid_1987566(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC, timeout=3)

    @allure.title("MSO-SREQ-21365 远控解锁状态下踩刹车不解锁")
    @pytest.mark.sanity
    def test_caseid_1987414(self):
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 TrUnlock状态下踩刹车不解锁")
    @pytest.mark.full
    def test_caseid_1987415(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm, timeout=2)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("MSO-SREQ-21365 远控闭锁状态钥匙类型不符合_踩刹车不解锁")
    @pytest.mark.sanity
    def test_caseid_1987416(self):
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyConnectSts", 1)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyTyp", 3)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm, timeout=3)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo1KeyConnectSts", 0)
        self.bus_comm.set_singal("connectivitycanfd", "BncmConnectivityFr18", "DigKeyConnectInfo2KeyTyp", 0)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)
      
    @allure.title("MSO-SREQ-21365 蓝牙闭锁状态钥匙类型不符合_踩刹车不解锁")
    @pytest.mark.sanity
    def test_caseid_1987417(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.NfcCard)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NFC_Card, isconnect=True)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=3)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("449507 手套箱隐私锁上锁解锁")
    @pytest.mark.sanity
    def test_caseid_1988671(self):
        self.sd_tester.write_ccp(ccp={88: 0x02})
        self.soa.hmi_set_glove_box_active_req(SetType.Unlock)  
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.PrivatetLockSts, GloveBoxStatus.Off)
        self.soa.hmi_set_glove_box_active_req(SetType.Lock)
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.PrivatetLockSts, GloveBoxStatus.On)
        self.soa.hmi_set_glove_box_active_req(SetType.Unlock)  

    @allure.title("463007 手套箱私锁提示")
    @pytest.mark.sanity
    def test_caseid_1988672(self):
        self.sd_tester.write_ccp(ccp={88: 0x02})
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.GloveBoxReq, GloveBoxStatus.Off)
        self.soa.hmi_set_glove_box_active_req(SetType.Open, time_wait=0.2)  
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.GloveBoxReq, GloveBoxStatus.On, time_wait=0.9)
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.GloveBoxReq, GloveBoxStatus.Off, time_wait=0.2)

    @allure.title("463007 手套箱私锁提示_CCP不满足")
    @pytest.mark.full
    def test_caseid_1988693(self):
        self.sd_tester.write_ccp(ccp={88: 0x00})
        time.sleep(1)
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.GloveBoxReq, GloveBoxStatus.Off)
        self.soa.hmi_set_glove_box_active_req(SetType.Open, time_wait=0.2)  
        self.bus_comm.check_glove_box_req(GloveBoxStatus.Off)
        self.sd_tester.write_ccp(ccp={88: 0x02})

    @allure.title("449507 手套箱隐私锁上锁解锁_CCP不满足")
    @pytest.mark.full
    def test_caseid_1988694(self):
        self.soa.hmi_set_glove_box_active_req(SetType.Unlock)  
        self.bus_comm.check_glove_box_req_and_lock_sts(ActionType.PrivatetLockSts, GloveBoxStatus.Off)
        self.sd_tester.write_ccp(ccp={88: 0x00})
        self.soa.hmi_set_glove_box_active_req(SetType.Lock)
        self.bus_comm.check_glove_box_private_lock_sts(GloveBoxStatus.Off)
        self.sd_tester.write_ccp(ccp={88: 0x02})
        self.soa.hmi_set_glove_box_active_req(SetType.Unlock)  

    @allure.title("462845 闭锁可见反馈_重锁")
    @pytest.mark.full
    def test_caseid_1989204(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.On, act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.Off, act_sts_ri=PosnLampSts.Off)
        self.bus_comm.check_lock_status_for_user(StsForUsrFb.Lockd)
        
    @allure.title("462845 闭锁可见反馈_Keyls")
    @pytest.mark.full
    def test_caseid_1989205(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_turn_indicate_lamp_req(IndcrSts.LeAndRiOn)
        sleep(.4)
        self.bus_comm.check_turn_indicate_lamp_req(IndcrSts.Off)
        self.bus_comm.check_lock_status_for_user(StsForUsrFb.Lockd)

    @allure.title("462845 闭锁可见反馈_OutsOth")
    @pytest.mark.full
    def test_caseid_1989207(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.On, act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.Off, act_sts_ri=PosnLampSts.Off)
        self.bus_comm.check_lock_status_for_user(StsForUsrFb.Lockd)

    @allure.title("462845 闭锁可见反馈_RKE且SafeLock灯效反馈")
    @pytest.mark.full
    def test_caseid_1989208(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.SafeLock)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.On, act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.Off, act_sts_ri=PosnLampSts.Off)
        self.bus_comm.check_lock_status_for_user(StsForUsrFb.safe)

    @allure.title("462845 闭锁可见反馈_IntrSwt无灯效")
    @pytest.mark.full
    def test_caseid_1989209(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.Off, act_sts_ri=PosnLampSts.Off)
        self.bus_comm.check_lock_status_for_user(StsForUsrFb.Lockd)

    @allure.title(" 497753 尾门解锁可见反馈_Keyls")
    @pytest.mark.sanity
    def test_caseid_114598(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.UnLock)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls, timeout=2)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open) # 发送开启尾门请求
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.On, act_sts_ri=PosnLampSts.On)
        sleep(.4)  # 解锁灯效循环2次，IndcrSts置位2s恢复
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.Off, act_sts_ri=PosnLampSts.Off)

    @allure.title("497753 解锁可见反馈_Approch")
    @pytest.mark.full
    def test_caseid_1989257(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.UnLock)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.On, act_sts_ri=PosnLampSts.On)
        sleep(.4)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.Off, act_sts_ri=PosnLampSts.Off)

    @allure.title("497753 解锁可见反馈_InsOth解锁无灯效")
    @pytest.mark.full
    def test_caseid_1989258(self):
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.UnLock)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All, act_sts_le=PosnLampSts.Off, act_sts_ri=PosnLampSts.Off)

    @allure.title("中央锁状态_解闭锁成功LockgEventTrigsrc&LockSt锁状态&锁源TrigSrc信号监测")
    @pytest.mark.full
    def test_caseid_110362(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("中央锁状态_解闭锁UpdEve信号计时监测SigChgTiGen")
    @pytest.mark.full
    def test_caseid_1989260(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_lock_unlock_event(event=True)
        self.bus_comm.check_lock_unlock_event(event=False)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_lock_unlock_event(event=True)
        self.bus_comm.check_lock_unlock_event(event=False)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("498410 中央锁状态_LockgCenSts(NVM存储校验)")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1989263(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        time.sleep(5)  # 等待NVM存储
        self.io.io_reset_bgm()
        time.sleep(5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("462846 中央锁定状态反馈给用户_Safe")
    @pytest.mark.full
    def test_caseid_1989264(self):
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.SafeLock)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_lock_status_for_user(StsForUsrFb.safe)

    @allure.title("526235 中央锁定和解锁_闭锁使能监测")
    @pytest.mark.full
    def test_caseid_115517(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_door_lock_req(DoorPos.All, DoorLockCmd.Lock, timeout=2)
        time.sleep(0.8)
        self.bus_comm.check_door_lock_req(DoorPos.All, DoorLockCmd.Off)

    @allure.title("526235 中央锁定和解锁_解锁使能监测")
    @pytest.mark.full
    def test_caseid_1989275(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_door_lock_req(DoorPos.All, DoorLockCmd.Unlck, timeout=2)
        time.sleep(0.8)
        self.bus_comm.check_door_lock_req(DoorPos.All, DoorLockCmd.Off)

    @allure.title("526235 中央锁定和解锁_解锁使能监测UnlckByCrash0")
    @pytest.mark.sanity
    def test_caseid_1989276(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.check_door_lock_req(DoorPos.All, DoorLockCmd.UnlckByCrash0)
        time.sleep(1)
        self.bus_comm.check_door_lock_req(DoorPos.All, DoorLockCmd.UnlckByCrash0)
        time.sleep(9)
        self.bus_comm.check_door_lock_req(DoorPos.All, DoorLockCmd.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)

    @allure.title("462992 v9中控锁定状态下后尾箱外部解锁可见反馈")
    @pytest.mark.sanity
    def test_caseid_114341(self):
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr08", "TrLockSts", 1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr08", "TrLockSts", 2)
        time.sleep(5)  # NVM存储要等至少5s
        self.io.io_reset_bgm()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr08", "TrLockSts", 2)

    @allure.title("474722 热失控解锁_车速低于3km/h边界值")
    @pytest.mark.full
    def test_caseid_1989306(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.83)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr18", "HvBattLimnIndcn", 128)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("热失控解锁_车速低于3km/h & HvBattLimnIndcn 第7个Bit不等于1中央不解锁")
    @pytest.mark.full
    def test_caseid_1989307(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.83)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr18", "HvBattLimnIndcn", 127)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        
    @allure.title("462858 Relocking_TmrAut闭锁Telm解锁重锁再触发")
    @pytest.mark.full
    def test_caseid_1989318(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        sleep(.5)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("ReLockTi执行期间钥匙遗留车内重锁不执行")
    @pytest.mark.full
    def test_caseid_1989321(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(20)  
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=10)

    @allure.title("TmrAut闭锁Telm解锁LockgEventTrigsrc校验")
    @pytest.mark.full
    def test_caseid_1989349(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(29)  
        self.bus_comm.set_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 5)

    @allure.title("462858_v26 relocking_RKE解锁_重锁计时期间UsageMode上切Driving_重锁不执行")
    @pytest.mark.full
    def test_caseid_1989350(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(25)  
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=5)
        
    @allure.title("462858_v26 relocking_RKE解锁_重锁计时期间UsageMode上切Convenience_重锁不执行")
    @pytest.mark.full
    def test_caseid_1988362(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(25)  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=5)

    @allure.title("462858_v26 relocking_RKE解锁_重锁计时期间UsageMode上切Active_重锁不执行")
    @pytest.mark.full
    def test_caseid_1989352(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=5)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(25)  
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        sleep(5) # 重锁计时30s
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("462858  relocking_重锁计时期间UsageMode下切到Abandoned_重锁正常执行")
    @pytest.mark.full
    def test_caseid_1989353(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(25)  
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        sleep(5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)  # 重锁计时30s

    @allure.title("relocking计时期间开启引擎盖_重锁不执行")
    @pytest.mark.full
    def test_caseid_1988361(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(25)  
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=5)
        self.io.set_hood_sts(HoodSts.Close)

    @allure.title("relocking计时期间开启尾门_重锁不执行")
    @pytest.mark.full
    def test_caseid_1988360(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])  # 更新钥匙在车外区域
        time.sleep(25)  
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=5)

    @allure.title("relocking计时期间开启主驾门_重锁不执行")
    @pytest.mark.sanity
    def test_caseid_1988358(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=1)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        time.sleep(25)  
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm, timeout=5)

    @allure.title("relocking计时期间开启右后门_重锁不执行")
    @pytest.mark.full
    def test_caseid_1989354(self):  
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=1)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        time.sleep(25)  
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm, timeout=5)

    @allure.title("HMI关门上锁_10s右后门Hover change to opening_计时中断")
    @pytest.mark.full
    def test_caseid_1987714(self):
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.StopDurgOpen)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Hover,isopen=False, antipinch=False)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockReqSource.Hmi)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opening,isopen=False, antipinch=False)  
        time.sleep(7)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closed,isopen=False, antipinch=False)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("P档自动解锁激活_符合解锁条件触发源校验")
    @pytest.mark.sanity
    def test_caseid_1991618(self):
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.bus_comm.set_seat_occpt_sts(SeatId.All, SeatPresSts.NoPres)
        self.bus_comm.set_blt_sts(SeatId.FrontLeft, BltFltSts.NoFault, BltLockSts.Unlock)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.No)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)       
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.Yes)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.set_gear_pos(Gear.Drv)
        sleep(.2)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3) 

    @allure.title("P档自动解锁激活_CCP10不满足P档解锁不触发")
    @pytest.mark.full
    def test_caseid_1991617(self):
        self.sd_tester.write_ccp(ccp={10: 0x00})
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.bus_comm.set_seat_occpt_sts(SeatId.All, SeatPresSts.NoPres)
        self.bus_comm.set_blt_sts(SeatId.FrontLeft, BltFltSts.NoFault, BltLockSts.Unlock)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.No)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)      
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.Yes)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.set_gear_pos(Gear.Drv)
        sleep(.2)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem) 
        self.sd_tester.write_ccp(ccp={10: 0x02})

    @allure.title("P档自动解锁激活_P档未跳变_P档不解锁")
    @pytest.mark.full
    def test_caseid_1991616(self):
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.bus_comm.set_seat_occpt_sts(SeatId.All, SeatPresSts.NoPres)
        self.bus_comm.set_blt_sts(SeatId.FrontLeft, BltFltSts.NoFault, BltLockSts.Unlock)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.No)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)      
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.Yes)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        
    @allure.title("RKE门锁联动_INACTIVE模式下副驾门及右后门开启")
    @pytest.mark.sanity
    def test_caseid_115419(self):
        self.io.set_door(Pass=Door.open, RiRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=5) 
        self.io.set_door(Pass=Door.close, RiRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("尾门关闭动作请求及触发源校验")
    @pytest.mark.sanity
    def test_caseid_1991659(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)  

    @allure.title("远控闭锁_左后门开仅闭锁_闭锁不执行")
    @pytest.mark.sanity
    def test_caseid_1991658(self):
        self.io.set_door(LeRe=Door.open)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=1)
        self.io.set_door(LeRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("远控闭锁_车辆配备自动驻车_驻车锁P档EPB处于Off")
    @pytest.mark.full
    def test_caseid_1991657(self):  
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.ParkEngd)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=1)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)

    @allure.title("远控闭锁_车辆配备自动驻车_驻车锁不处于P档EPB处于On")
    @pytest.mark.full
    def test_caseid_1991656(self):  
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.NotInUse)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("车辆配备自动驻车车辆不处于P档不落锁")
    @pytest.mark.full
    def test_caseid_1991655(self):  
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.NotInUse)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=1)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)
    
    @allure.title("远控闭锁_四门开启10s超时关闭_闭锁不执行")
    @pytest.mark.sanity
    def test_caseid_1991654(self):
        self.io.set_door(Drvr=Door.open, LeRe=Door.open, Pass=Door.open, RiRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        sleep(11)
        self.io.set_door(Drvr=Door.close, LeRe=Door.close, Pass=Door.close, RiRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("远控闭锁_主驾门开10s计时内尾门触发防夹_闭锁不执行")
    @pytest.mark.sanity
    def test_caseid_1991653(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.Telm, timeout=5) 
        self.bus_comm.set_tailgate_antiPnch_sts(sts=True)
        sleep(1)  # 防止防夹状态未通知
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_tailgate_antiPnch_sts(sts=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("远控闭锁_尾门开10s计时内左后门触发防夹_闭锁不执行")
    @pytest.mark.sanity
    def test_caseid_1991652(self):
        self.io.set_door(Trunk=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        self.bus_comm.set_door_anti_pnch_sts(LeRe=True)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_door_anti_pnch_sts(LeRe=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("远控解锁_Convenience模式下有占座远控解锁")
    @pytest.mark.sanity
    def test_caseid_1991651(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)  # RKE & Telm之间至少隔1s  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_present()
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)  

    @allure.title("远控解锁_Active模式下远控解锁")
    @pytest.mark.sanity
    def test_caseid_1991650(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  
        sleep(1)  # RKE & Telm之间至少隔1s
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)  

    @allure.title("远控解锁_Abandoned模式下远控解锁")
    @pytest.mark.sanity
    def test_caseid_1991649(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  
        sleep(1)  # RKE & Telm之间至少隔1s
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)  

    @allure.title("远控闭锁联动关闭右前门_解闭锁状态提示及关门动作请求校验")
    @pytest.mark.full
    def test_caseid_1892750(self):
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.Telm, timeout=5) 
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("远控闭锁_Convenience模式1.5s内模式下切到Abandoned整车落锁")
    @pytest.mark.full
    def test_caseid_1892749(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics, time_wait=0.3)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)  

    @allure.title("驻车舒享模式_外部其它方式闭锁触发源::InOth")
    @pytest.mark.full
    def test_caseid_1991632(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        sleep(1)  # 等待驻车舒享开
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.soa.set_convenience_duration(time=0)  # 维持上电恢复环境
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)

    @allure.title("不同CarMode模式下中央锁定行为_Transport模式远控闭锁禁用")
    @pytest.mark.full
    def test_caseid_1991643(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        sleep(1)  # 防止仲裁逻辑
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("不同CarMode模式下中央锁定行为_Transport模式PE闭锁禁用")
    @pytest.mark.full
    def test_caseid_1987142(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("驻车舒享模式_外部其它方式闭锁Convenience闭锁转InsOth")
    @pytest.mark.full
    def test_caseid_1994877(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        sleep(1)  # 等待驻车舒享开
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA, time_wait=0.3)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("驻车舒享模式_驻车舒享开外锁转内锁驻车舒享关_1.5s内下切到Inactive恢复OutsOth")
    @pytest.mark.full
    def test_caseid_1994878(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.set_convenience_duration(time=1)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 1)
        sleep(1)  # 等待驻车舒享开
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA, time_wait=0.3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.set_convenience_duration(time=0)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)
        self.io.driver_seat_notpresent()
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        sleep(.7)  # 1.5内下切
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth, timeout=3)

    @allure.title("ASM请求锁定和解锁_Driving模式内部其它方式锁定")
    @pytest.mark.full
    def test_caseid_1989368(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("ASM请求锁定和解锁_Driving模式外部锁定DecUsgModAut计时内下切到Inactive闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1989365(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_notpresent()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(.5)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA, time_wait=0.3)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("被ASM请求锁定_外部锁定CCP不满足整车不闭锁")
    @pytest.mark.full
    def test_caseid_1989364(self):
        self.sd_tester.write_ccp(ccp={142: 0x00})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("ASM请求锁定_内部锁定锁定CCP不满足整车不闭锁")
    @pytest.mark.full
    def test_caseid_1994880(self):
        self.sd_tester.write_ccp(ccp={142: 0x00})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("ASM请求锁定_内部解锁CCP不满足整车不解锁")
    @pytest.mark.full
    def test_caseid_1994881(self):
        self.sd_tester.write_ccp(ccp={142: 0x00})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("ASM请求锁定和解锁_Active外部锁定DecUsgModAut计时超时下切到Inactive闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1989363(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.io.driver_seat_notpresent()
        sleep(.5)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA, time_wait=1.6)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("ASM请求锁定和解锁_Active内部锁定整车闭锁")
    @pytest.mark.full
    def test_caseid_1989362(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("ASM请求锁定和解锁_外部锁定DecUsgModAutTi计时器内模式下切到Inactive")
    @pytest.mark.full
    def test_caseid_1989361(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.io.driver_seat_present()
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA, time_wait=0.3)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.io.driver_seat_notpresent()

    @allure.title("ASM请求锁定和解锁_外部锁定解闭锁动作触发源校验")
    @pytest.mark.full
    def test_caseid_1989360(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.OutsOth, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)

    @allure.title("ASM请求锁定和解锁_解锁并解防解闭锁动作触发源校验")
    @pytest.mark.full
    def test_caseid_1989359(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.APA)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.InsOth, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("ASM请求锁定和解锁_内部锁定解闭锁动作触发源校验")
    @pytest.mark.full
    def test_caseid_1989356(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.InsOth, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        
    @allure.title("NFC闭锁+PEPS解锁+重锁可见反馈")
    @pytest.mark.full
    def test_caseid_1919328(self):
        self.io.set_hood_sts(HoodSts.Close)     
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut, timeout=5)

    @allure.title("车速落锁_主驾无人中央不落锁解闭锁")
    @pytest.mark.full
    def test_caseid_1989370(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Unlock)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.No)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("车速落锁_右后门开中央不落锁解闭锁")
    @pytest.mark.full
    def test_caseid_1989375(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        self.io.set_door(RiRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes, time_wait=0.5)
        self.io.driver_seat_present()
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.No, time_wait=0)
        
    @allure.title("车速落锁_尾门开中央不落锁解闭锁")
    @pytest.mark.full
    def test_caseid_1989379(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        self.io.set_door(RiRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes, time_wait=0.5)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes, time_wait=0.5)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.No, time_wait=0.5)

    @allure.title("车速落锁_尾门解锁状态车速落锁")
    @pytest.mark.full
    def test_caseid_1989380(self):  
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorFrontLeft, lock_sts=Locksts.Lockd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr08", "TrLockSts", 1)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)

    @allure.title("车速落锁_有车速 &&UsageMode！=Driving车速不落锁")
    @pytest.mark.full
    def test_caseid_1989447(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        
    @allure.title("车速落锁_ CarMode = Dyno车速不落锁")
    @pytest.mark.full
    def test_caseid_1989448(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO)  
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("车速落锁_ CarMode = Factory 车速不落锁")
    @pytest.mark.full
    def test_caseid_1989449(self):  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.FACTORY)
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        sleep(1)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  # 一个上电周期工厂模式会解锁一次，触发源不确定

    @allure.title("车速落锁_CrashUnlckFailrSts触发车速不落锁")
    @pytest.mark.full
    def test_caseid_1989451(self):  
        self.mix.set_common_precontion(UsageMode.INACTIVE,CarMode.CRASH)
        self.bus_comm.set_door_lock_sts(drv_lock=Locksts.Lockd, pass_lock=Locksts.Unlckd,
                          lere_lock=Locksts.Unlckd, rire_lock=Locksts.Unlckd)
        self.bus_comm.check_crashunllock_failrSts(Unlockfailtohmi.SafeOn)
        time.sleep(15)  # Crash 有15s安全状态不执行解闭锁
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)  

    @allure.title("ASM请求锁定和解锁_主驾门开外部其它方式闭锁关门后闭锁不执行")
    @pytest.mark.full
    def test_caseid_1994882(self):
        self.io.set_door(Drvr=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE) 
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.OutsOth, time_wait=1)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("车辆非静止TrUnlock状态下HMI开门解锁不执行")
    @pytest.mark.full
    def test_caseid_1993003(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(drv_opener= DoorOpenerReq.Idle)
        sleep(7)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车速落锁_ CarMode = Transport 车速不落锁")
    @pytest.mark.full
    def test_caseid_1989450(self):  
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT)  
        self.bus_comm.set_blt_sts(seat_id=SeatId.FrontLeft, blt_flt_sts=BltFltSts.NoFault, blt_lock_sts=BltLockSts.Lock)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.check_driver_prsnt_sts(present=NoYesCrit1.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)  

    @allure.title("474634 内门把手解锁_车速落锁内门把手解锁")
    @pytest.mark.full
    def test_caseid_1995279(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr02", "AccrPedlPsdSts", 1)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr02", "AccrPedlPsdAccrPedlPsd", 1)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)  # 踏板踩下驾驶员在才会为Yes
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr02", "AccrPedlPsdSts", 0)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr02", "AccrPedlPsdAccrPedlPsd", 0)     
             
    @allure.title("474634 内门把手解锁_内部其它方式落锁内门把手解锁")
    @pytest.mark.full
    def test_caseid_1995281(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal2)  
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus=OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("内门把手解锁_TrUnlckd内门把手解锁")
    @pytest.mark.full
    def test_caseid_1995282(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal2)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        sleep(3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.InsdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("外锁计时9.8s解锁开启主驾门_LockgDecodeEvalSwtIntrDisabledFlg=0")
    @pytest.mark.full
    def test_caseid_1996231(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(9.8)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外锁计时10s解锁开启主驾门_LockgDecodeEvalSwtIntrDisabledFlg=0")
    @pytest.mark.sanity
    def test_caseid_1996232(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(10)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("外锁计时10.1s解锁开启主驾门_LockgDecodeEvalSwtIntrDisabledFlg=0")
    @pytest.mark.sanity
    def test_caseid_1996233(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(10.1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内开关启用_外锁计时9.5s副驾车门开启10%解锁LockgDecodeEvalSwtIntrDisabledFlg=0")
    @pytest.mark.full
    def test_caseid_1996234(self):
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(9.5)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.OutdSwt) 
        self.bus_comm.check_door_opener_req_and_trigsrc( drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("近车解锁_2段开门请求open打断逻辑_1600ms内主驾门从开变关_30s计时器打断2段开门打断不发Open")
    @pytest.mark.full
    def test_caseid_1999071(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.io.set_door(Drvr=Door.open)
        self.io.set_door(Drvr=Door.close)
        sleep(.5)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle, timeout=30)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后计时1.4s主驾门开启且Zone7有有效钥匙_2段开门请求Open")
    @pytest.mark.sanity
    def test_caseid_1999072(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(1.4)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度开门请求后1600ms车门超时开启(大概1.7s)_30s计时器打断2段开门打断不发Open")
    @pytest.mark.full
    def test_caseid_1999073(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(1.5)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,
                                            trigger_src=DoorTrigerSource.NoTrigSrc)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle, timeout=30)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_1段开门请求主驾车门超1600ms一直未开启_30s计时器打断2段开门打断不发Open")
    @pytest.mark.sanity
    def test_caseid_1999074(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(1.7)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle, timeout=30)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)


    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后计时0.5s主驾门开启且Zone7有有效钥匙_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999075(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(0.5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        
    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后计时1600ms内主驾门开启且Zone7无钥匙_2段开门请求不发")
    @pytest.mark.full
    def test_caseid_1999076(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(0.5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle, timeout=30)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后计时1600ms内主驾门开ApproachTi = 20s识别钥匙在Zone7_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999077(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1) # 近车解锁开主驾生效起ApproachTi=30s计时器
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.io.set_door(Drvr=Door.open)
        sleep(20)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后计时1600ms内主驾门开ApproachTi = 26s识别钥匙在Zone7_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999078(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1) # 近车解锁开主驾生效起ApproachTi=30s计时器
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.io.set_door(Drvr=Door.open)
        sleep(26)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后1600ms内触发主驾关门请求_2段开门请求不发")
    @pytest.mark.sanity
    def test_caseid_1999079(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(.5)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.StopDurgOpen)  # 开启中停止
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle, timeout=30)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后1600ms内触发主驾暂停请求_2段开门请求Open")
    @pytest.mark.sanity
    def test_caseid_1999080(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(.8)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)  # 开启中
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,  trigger_src=DoorTrigerSource.NoTrigSrc)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后1600ms内右后车门触发暂停请求_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999081(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        sleep(.5)  # 等待配置生效
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(.8)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)  # 开启中
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Stop)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后1600ms内左后车门触发关闭请求_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999082(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(.8)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后1600ms内副驾车门触发开启请求_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999083(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(.8)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("498408 近车解锁_2段开门请求open打断逻辑_1600ms内主驾门开右后车门关_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999084(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.io.set_door(Drvr=Door.open, RiRe=Door.open)
        self.io.set_door(RiRe=Door.close)
        sleep(.5)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后计时1600ms内主驾门开ApproachTi = 30.1s识别钥匙在Zone7_2段开门请求Open不发")
    @pytest.mark.sanity
    def test_caseid_1999085(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1) # 近车解锁开主驾生效起ApproachTi=30s计时器
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.io.set_door(Drvr=Door.open)
        sleep(30.1)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_without_open_req(drv_opener=DoorOpenerReq.Idle, timeout=30)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后1600ms内触发主驾开门请求_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999086(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(.5)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,trigger_src=DoorTrigerSource.NoTrigSrc)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    @allure.title("近车解锁_2段开门请求open打断逻辑_小角度请求后1600ms内触发主驾开启10°_2段开门请求Open")
    @pytest.mark.full
    def test_caseid_1999087(self):
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(.5)  # 等待配置生效
        self.bus_comm.set_door_perc_position(doorpos= DoorPos.Dirver, perc_position=0)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=DoorTrigerSource.KeyRem)
        sleep(.5)
        self.soa.hmi_set_door_postion(door_pos= DoorPos.Dirver, pos= 10, scene=VehicleInsideOutside.VehicleInSide)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=101, door_trigsrc=DoorOpenSource.NoTrigSrc)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=DoorTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7,valid=Validity.NotValid)

    # @allure.title("验证ctrl_lock抽象接口")
    # @pytest.mark.debug
    # def test_caseid_001(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.TmrAut)
    #     sleep(.2)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.Apprch)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Apprch)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.OutsOth)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.InsOth)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.InsOth)