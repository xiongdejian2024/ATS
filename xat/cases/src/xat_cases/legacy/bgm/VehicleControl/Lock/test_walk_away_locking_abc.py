#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_walk_away_locking_abc.py
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
@allure.story("离车落锁")
class TestWalkAwayLockingCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            [
                "CentralLockService_client",
                "DoorService_client",
                "TailGateService_client",
                "KeyService_client",

            ]
        )
        sleep(2)

    def before_each_func(self, ecu):
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83, 10: 0x2})
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2) 
        sleep(1)  # 防止解闭锁1内触发仲裁逻辑

    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
            self.io.driver_seat_notpresent()
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("离车落锁_设置离车落锁关主驾门&&五门全关_中央落锁")
    @pytest.mark.smoke
    def test_caseid_1986404(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("离车落锁_设置仅主驾门关闭&&主驾门开计时12s关闭主驾门_中央落锁")
    @pytest.mark.sanity
    def test_caseid_1986405(self):
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(12)
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kClosed)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title(" 离车落锁_设置离车落锁关四门&&四门及尾门全关_中央落锁")
    @pytest.mark.smoke
    def test_caseid_1986406(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("离车落锁_设置离车落锁关四门&&12s计时内四门全关_中央落锁")
    @pytest.mark.sanity
    def test_caseid_1986408(self):
        self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kOpened)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(11)
        self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kClosed)  # 耗时1s
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("离车落锁_设置离车落锁关四门&&尾门处于关闭中15s超时关闭尾门_中央不落锁")
    @pytest.mark.full
    def test_caseid_1986410(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closing)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(15.5)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("离车落锁_设置离车落锁关四门&&尾门非关闭中14s计时内关闭尾门_中央不落锁")
    @pytest.mark.full
    def test_caseid_1986411(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Opening)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(3)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("离车落锁_设置仅主驾门关闭&&非主驾门开14s内关闭车门门_中央不落锁")
    @pytest.mark.full
    def test_caseid_1986412(self):
        self.mix.set_open_close_door_precondition(DoorPos.Pass, DoorStatus.kOpened)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(3)
        self.mix.set_open_close_door_precondition(DoorPos.Pass, DoorStatus.kClosed)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("离车落锁_设置离车落锁关四门&&14s计时超时关闭四门_中央不落锁")
    @pytest.mark.full
    def test_caseid_1986413(self):
        self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kOpened)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(15.5)
        self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kClosed)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("离车落锁_离车落锁设置项不生效_离车落锁不执行")
    @pytest.mark.sanity
    def test_caseid_1986414(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 0)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 0) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    # @allure.title("离车落锁_仲裁逻辑&&离车落锁关门请求延时期间远控关门上锁 _离车落锁中断")
    # @pytest.mark.Bug
    # @pytest.mark.full
    # def test_caseid_1986415(self):
    #     self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kOpened)
    #     self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
    #     self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
    #     self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.send_walk_away_lock_cmd()
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
    #     self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio, time_wait=0) 
    #     time.sleep(4) 
    #     self.soa.hmi_set_door_close_lock(LockCmd.AllDoorCloseAndLock, LockSource.Telm)
    #     self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 7) 
    #     time.sleep(3)
    #     self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kClosed)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("657337 离车落锁_仲裁逻辑_离车落锁关门等待关门计时器超过5s服务开启主驾门_关门请求忽略")
    @pytest.mark.full
    def test_caseid_1986441(self):
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.mix.set_open_close_door_precondition(DoorPos.Pass, DoorStatus.kOpened)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        sleep(6)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kClosed)
        sleep(2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("497859 v16 离车落锁联动关门_尾门开启离车落锁不执行无关门提示")
    @pytest.mark.full
    def test_caseid_1985324(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 5)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Opened)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_Lock_and_unlock_remind(LockStsPrmt.Idle)
        sleep(13)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)  
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)        
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("497859 v16 离车落锁_尾门开关闭中MoveDow&&延时12s尾门关闭无关门提示中央落锁")
    @pytest.mark.full
    def test_caseid_1985541(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.MovgDown)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closing)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)    
        self.bus_comm.check_walk_away_and_approch_settings(keysettingtype= KeySettingType.WalkAay, walkaway=KeySettingItem.OnWithAllDoorClose, time_wait=1)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=1)
        # self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio)  # 发7 是Bug
        self.bus_comm.check_Lock_and_unlock_remind(lockstsprmt= LockStsPrmt.Idle)
        sleep(10)  # 提示动作有2s延时
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.FullClsd)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("离车落锁_设置离车落锁关四门&&尾门处于关闭中15s计时内尾门全关_中央落锁")
    @pytest.mark.sanity
    def test_caseid_1986409(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6)  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(13)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)    
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)

    @allure.title("PwrLvlElec == 1_HMI闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991639(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Hmi)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.IntrSwt, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_NFC解锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991638(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_外部其它方式闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991637(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm,  source=LockReqSource.APA)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.OutsOth, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_重锁不执行")
    @pytest.mark.full
    def test_caseid_1991636(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)  # 1s防止仲裁逻辑
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(15)  
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        sleep(15)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_PE解锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991635(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_内部其它方式闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991634(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.InsOth, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_离车落锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991633(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED,UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_远控闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1988625(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("PwrLvlElec == 1_NFC解锁请求忽略")
    @pytest.mark.full
    def test_caseid_1988624(self):
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x03, SESSION.EXTENDED, UnLock.L0, '1100', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=1, subtype=1)
        sleep(1)
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.sd_tester.io_ctrl_and_check(TA.BGM_MCU, 0X429E, 0x00, SESSION.EXTENDED, UnLock.L0, '00', '6f429e', check_method=Check_Method.response, recover=False)
        self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)

    @allure.title("MSO-SREQ-21365 远控闭锁刹车踏板状态从踩下跳变为未踩下不解锁")
    @pytest.mark.full
    def test_caseid_1987413(self):
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.Yes)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm, timeout=2)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleKey)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.BLE_Key, isconnect=True)
        self.bus_comm.set_brake_pedal(safe=YesOrNo.Yes, qf=ValueQf.AccurData, sts=YesOrNo.No)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm, timeout=2)
        self.bus_comm.set_keyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Disconnect, keyconnecttype=KeyConnectType.NoKeyConnected)
        self.soa.hmi_check_notify_key_connect_sts(KeyType.NoKeyConnected, isconnect=False)

    @allure.title("内门把手解锁_离车落锁副驾门开_整车不解锁")
    @pytest.mark.full
    def test_caseid_1991692(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        sleep(2)  # 等待设置项生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass,time_interval=0.2)
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("重锁内门把手控制四门开_中央不解锁")
    @pytest.mark.full
    def test_caseid_1991691(self):  
        self.bus_comm.set_child_lock_sts(side=Side.All, childlockstatus=OnOffSafe1.OnOffSafeOff)
        self.io.set_hood_sts(HoodSts.Close)     
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(30)  
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorAll, lock_sts=Locksts.Unlckd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        sleep(4)  # 等待四门锁闭锁请求置位
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver,time_interval=0.2)  # 主驾门内开关按下
        self.bus_comm.check_door_opener_req(drv_opener= DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass,time_interval=0.2)  # 副驾门内开关按下
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft,time_interval=0.2)  # 左后门内开关按下
        self.bus_comm.check_door_opener_req(lere_opener= DoorPos.RearLeft, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight,time_interval=0.2)  # 右后门内开关按下
        self.bus_comm.check_door_opener_req(rire_opener= DoorPos.RearRight, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内门把手解锁_外部其它方式闭锁后排车门开_中央不解锁")
    @pytest.mark.full
    def test_caseid_1991690(self):  
        self.bus_comm.set_child_lock_sts(side=Side.All, childlockstatus=OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft,time_interval=0.2)  # 左后门内开关按下
        self.bus_comm.check_door_opener_req(lere_opener= DoorPos.RearLeft, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight,time_interval=0.2)  # 右后门内开关按下
        self.bus_comm.check_door_opener_req(rire_opener= DoorPos.RearRight, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("远控闭锁内门把手控制副驾门开_中央不解锁")
    @pytest.mark.full
    def test_caseid_1991689(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass,time_interval=0.2)  # 副驾门内开关按下
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("儿童锁上锁_内开关禁用")
    @pytest.mark.full
    def test_caseid_1991687(self):  
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus=OnOffSafe1.OnOffSafeOn)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft,time_interval=0.2)  # 左后门内开关按下
        self.bus_comm.check_door_without_open_req(lere_opener=DoorOpenerReq.Idle)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus=OnOffSafe1.OnOffSafeOff)
        
    @allure.title("InsOth锁车左后门内部硬按键开门解锁")
    @pytest.mark.full
    def test_caseid_1991688(self):  
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus=OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft,time_interval=0.2)  # 左后门内开关按下
        self.bus_comm.check_door_opener_req(lere_opener= DoorPos.RearLeft, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("蓝牙闭锁内门把手控制主驾门开_主驾门开中央不解锁")
    @pytest.mark.sanity
    def test_caseid_1892762(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)  # 等前置条件生效
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver,time_interval=0.2)  
        self.bus_comm.check_door_opener_req(drv_opener= DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)


    @allure.title(" NFC锁车_五门锁全解锁整车解锁")
    @pytest.mark.full
    def test_caseid_111324(self):
        self.bus_comm.set_child_lock_sts(side=Side.All, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorAll, lock_sts=Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(4)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver,time_interval=0.2)  # 主驾门内开关按下
        self.bus_comm.check_door_opener_req(drv_opener= DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass,time_interval=0.2)  # 副驾门内开关按下
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft,time_interval=0.2)  # 左后门内开关按下
        self.bus_comm.check_door_opener_req(lere_opener= DoorPos.RearLeft, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)  # 尾门解锁
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight,time_interval=0.2)  # 右后门内开关按下
        self.bus_comm.check_door_opener_req(rire_opener= DoorPos.RearRight, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内部门把手解锁_NFC闭锁_四门全开中央不解锁")
    @pytest.mark.full
    def test_caseid_115504(self):
        self.bus_comm.set_child_lock_sts(side=Side.All, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorAll, lock_sts=Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(4)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver,time_interval=0.2)  # 主驾门内开关按下
        self.bus_comm.check_door_opener_req(drv_opener= DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass,time_interval=0.2)  # 副驾门内开关按下
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearLeft,time_interval=0.2)  # 左后门内开关按下
        self.bus_comm.check_door_opener_req(lere_opener= DoorPos.RearLeft, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight,time_interval=0.2)  # 右后门内开关按下
        self.bus_comm.check_door_opener_req(rire_opener= DoorPos.RearRight, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内门把手开门解锁_TrUnlock内部硬开关开启右后门_整车解锁")
    @pytest.mark.full
    def test_caseid_115502(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.set_door_lock_status(doorid=DoorId.kDoorAll, lock_sts=Locksts.Unlckd)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)  # 尾门解锁
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)  # 尾门解锁
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.RearRight,time_interval=0.2)  # 右后门内开关按下
        self.bus_comm.check_door_opener_req(rire_opener= DoorPos.RearRight, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内门把手解锁_HMI锁车主驾门内部硬按键开门解锁")
    @pytest.mark.full
    def test_caseid_110355(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Dirver,time_interval=0.2)  
        self.bus_comm.check_door_opener_req(drv_opener= DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("NFC解锁_Driving主驾无占位_NFC解锁不执行")
    @pytest.mark.full
    def test_caseid_1991754(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("NFC解锁_Active主驾有占位_NFC解锁不执行")
    @pytest.mark.full
    def test_caseid_1991753(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 2)  
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_notpresent()

    @allure.title("Active 主驾无占位_NFC解锁")
    @pytest.mark.full
    def test_caseid_1991752(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 1)  
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("NFC解锁_Convenience主驾有占位_NFC解锁不执行")
    @pytest.mark.full
    def test_caseid_1991751(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 2)  
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_notpresent()

    @allure.title("Convenience 主驾无占位_NFC解锁")
    @pytest.mark.full
    def test_caseid_1991750(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 1)  
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("NFC解锁_Abandoned模式NFC闭锁")
    @pytest.mark.full
    def test_caseid_1991749(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("NFC闭锁联动关门_TrUnlock状态NFC刷卡_执行解锁")
    @pytest.mark.full
    def test_caseid_1991742(self): 
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus=OnOffSafe1.OnOffSafeOn)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  # 前置条件
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)       

    @allure.title("Active主驾无占座1.5s超时下切到Abandoned_闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991741(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 1)  
        self.bus_comm.send_nfc_cmd()
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("Convenience主驾无占座1.5s超时下切到Inactive_闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991740(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 1)  
        self.bus_comm.send_nfc_cmd()
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("Active主驾无占座1.5s内下切到Abandoned整车闭锁")
    @pytest.mark.full
    def test_caseid_1991739(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 1)  
        self.bus_comm.send_nfc_cmd()
        sleep(0.8)        
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("Convenience主驾无占座1.5s内下切到Inactive整车闭锁")
    @pytest.mark.full
    def test_caseid_1991738(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr12", "DrvrSeatSts", 1)  
        self.bus_comm.send_nfc_cmd()
        sleep(0.8)        
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("NFC闭锁联动关门_车辆配备自动驻车_驻车锁不处于P档EPB处于On")
    @pytest.mark.full
    def test_caseid_1991736(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Drv, parklock=ParkLockSts.ParkNotEngd)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq", 0)  
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.ParkEngd)

    @allure.title("NFC闭锁联动关门_车辆配备自动驻车_驻车锁不处于P档EPB处于On")
    @pytest.mark.full
    def test_caseid_1991736(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Drv, parklock=ParkLockSts.ParkNotEngd)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq", 0)  
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.ParkEngd)

    @allure.title("车辆配备自动驻车车辆不处于P档不落锁")
    @pytest.mark.full
    def test_caseid_1991735(self):  
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.CancelSet)  # 避免触发P档解锁
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq", 1)  
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 0)  
        sleep(2)  # 等待条件生效
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        
    @allure.title("车辆配备自动驻车_驻车锁P档EPB处于Off")
    @pytest.mark.full
    def test_caseid_1991737(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.ParkEngd)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr39", "EpbLampReqEpbLampReq", 0)  
        sleep(1)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
    
    @allure.title("Driving主驾无占座1.5s超时下切到Abandoned_闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991673(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.io.driver_seat_notpresent()
        self.bus_comm.send_nfc_cmd()
        sleep(0.8)        
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("Abandoned 主驾有占座_NFC闭锁")
    @pytest.mark.full
    def test_caseid_1991672(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.io.driver_seat_present()
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC, timeout=3)

    @allure.title("NFC解锁_Abandoned模式NFC闭锁")
    @pytest.mark.full
    def test_caseid_1991748(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.send_nfc_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NFC, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("离车落锁延时期间15s内触发防夹离车落锁退出")
    @pytest.mark.full
    def test_caseid_1991713(self):  
        self.io.set_door(Drvr=Door.open)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.bus_comm.check_walk_away_and_approch_settings(keysettingtype= KeySettingType.WalkAay, walkaway=KeySettingItem.OnWithAllDoorClose, time_wait=1)
        self.io.driver_seat_present()
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        sleep(6)  # 离车落锁关门有5s等待提示时间
        self.bus_comm.set_door_anti_pnch_sts(Drvr=True)
        sleep(.5)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_door_anti_pnch_sts(Drvr=False)

    @allure.title("离车落锁联动关门关门提示WalkAwayDelayCloseDoor计时器监测")
    @pytest.mark.full
    def test_caseid_1991712(self):  
        self.io.set_door(Drvr=Door.open)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.bus_comm.check_walk_away_and_approch_settings(keysettingtype= KeySettingType.WalkAay, walkaway=KeySettingItem.OnWithAllDoorClose, time_wait=1)
        self.io.driver_seat_present()
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio, time_wait=1)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)     

    @allure.title("离车落锁_Abandoned离车落锁正常执行")
    @pytest.mark.full
    def test_caseid_1991710(self):
        self.io.driver_seat_notpresent()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch) 

    @allure.title("离车落锁_Convenience主驾无占位1.5s内模式不下切离车落锁不执行")
    @pytest.mark.full
    def test_caseid_1991711(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.io.driver_seat_notpresent()  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        sleep(2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("离车落锁_Inactive && 主驾有占座TrUnlock离车落锁正常执行")
    @pytest.mark.full
    def test_caseid_1991709(self):
        self.io.driver_seat_present()  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  # 前置条件
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)  
        self.io.driver_seat_notpresent()  
        
    @allure.title("497859 离车落锁_Convenience主驾无占位离车落锁正常执行")
    @pytest.mark.full
    def test_caseid_1991708(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.io.driver_seat_notpresent()  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        sleep(.7)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch) 

    @allure.title("离车落锁_Active主驾无占位离车落锁正常执行")
    @pytest.mark.full
    def test_caseid_1991707(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.io.driver_seat_notpresent()  
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        sleep(.7)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch) 

    @allure.title("离车落锁_Active主驾有占位离车落锁不执行")
    @pytest.mark.full
    def test_caseid_1991706(self):
        self.io.driver_seat_present()  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        sleep(.7)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem) 
        self.io.driver_seat_notpresent()  

    @allure.title("离车落锁_Convenience主驾有占位离车落锁不执行")
    @pytest.mark.full
    def test_caseid_1991705(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.io.driver_seat_present()  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        sleep(.7)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem) 
        self.io.driver_seat_notpresent()  

    @allure.title("离车落锁_CarMode=Transport离车落锁不执行")
    @pytest.mark.full
    def test_caseid_1991704(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem) 
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)

    @allure.title("离车落锁_CarMode=Factory离车落锁不执行")
    @pytest.mark.full
    def test_caseid_1991703(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock) 
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)

    @allure.title("离车落锁_有自动驻车不处于P档EPB为On离车落锁正常执行")
    @pytest.mark.full
    def test_caseid_1991702(self):  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.ParkNotEngd)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,  exp_trigsrc=LockTrigerSource.Apprch) 

    @allure.title("离车落锁_有自动驻车不处于P档")
    @pytest.mark.full
    def test_caseid_1991701(self):  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.ParkNotEngd)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=1)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,  exp_trigsrc=LockTrigerSource.KeyRem) 
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)

    @allure.title("离车落锁_CCP不满足")
    @pytest.mark.full
    def test_caseid_1991700(self):  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.sd_tester.write_ccp(ccp={94: 0x00})
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,  exp_trigsrc=LockTrigerSource.KeyRem) 
        self.sd_tester.write_ccp(ccp={94: 0x80})

    @allure.title("近车解锁联动开门钥匙不在Zone7小角度开门监测")
    @pytest.mark.full
    def test_caseid_1991699(self):  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,  exp_trigsrc=LockTrigerSource.Apprch) 
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.OpenMinang, door_trigsrc=DoorTrigerSource.KeyRem)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("近车解锁Active主驾有占位近车解锁不执行")
    @pytest.mark.full
    def test_caseid_1991698(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_present()  
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,  exp_trigsrc=LockTrigerSource.KeyRem) 
        self.io.driver_seat_notpresent()  

    @allure.title("近车解锁Active主驾无占位近车执行解锁")
    @pytest.mark.full
    def test_caseid_1991697(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_notpresent()  
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,  exp_trigsrc=LockTrigerSource.Apprch) 

    @allure.title("近车解锁Convenience主驾有占位近车解锁不执行")
    @pytest.mark.full
    def test_caseid_1991696(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_present()  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,  exp_trigsrc=LockTrigerSource.KeyRem) 
        self.io.driver_seat_notpresent() 

    @allure.title("近车解锁Convenience主驾无占位近车解锁")
    @pytest.mark.full
    def test_caseid_1991695(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_notpresent()  
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,  exp_trigsrc=LockTrigerSource.Apprch) 

    @allure.title("近车解锁_Abandoned模式下TrUnlock近车解锁")
    @pytest.mark.full
    def test_caseid_1991694(self):
        self.io.driver_seat_present()  
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.ABANDONED)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)  # 前置条件
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,  exp_trigsrc=LockTrigerSource.Apprch) 
        self.io.driver_seat_notpresent() 

    @allure.title("近车解锁_CCP不满足近车解锁不执行")
    @pytest.mark.full
    def test_caseid_1991693(self):
        self.sd_tester.write_ccp(ccp={94: 0x00})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,  exp_trigsrc=LockTrigerSource.KeyRem) 
        self.sd_tester.write_ccp(ccp={94: 0x80})

    @allure.title("离车落锁_Driving主驾无占位_离车落锁忽略")
    @pytest.mark.full
    def test_caseid_1991675(self):
        self.io.driver_seat_notpresent()  
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        sleep(.7)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,  exp_trigsrc=LockTrigerSource.KeyRem) 

    @allure.title("近车解锁_Driving主驾无占位_近车解锁忽略")
    @pytest.mark.full
    def test_caseid_1991674(self):
        self.io.driver_seat_notpresent()  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,  exp_trigsrc=LockTrigerSource.KeyRem) 

    @allure.title("重锁_RKE闭锁Apprch解锁_relocking")
    @pytest.mark.sanity
    def test_caseid_1995339(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_Keyls闭锁Apprch解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995338(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_重锁TmrAut闭锁Apprch解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995337(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_远控Telm闭锁Apprch解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995336(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_外部其它方式OutsOth闭锁Apprch解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995335(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_NFC闭锁Apprch解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995334(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_离车落锁Apprch闭锁Apprch解锁_relocking")
    @pytest.mark.sanity
    def test_caseid_1995348(self):       
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("离车落锁Apprch闭锁RKE解锁_relocking")
    @pytest.mark.sanity
    def test_caseid_1995332(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_离车落锁Apprch闭锁Keyls解锁解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995331(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("462858 重锁_离车落锁Apprch闭锁Telm解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995330(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title(" 重锁_离车落锁Apprch闭锁Crash解锁_重锁不执行")
    @pytest.mark.full
    def test_caseid_1995328(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)  

    @allure.title("重锁_离车落锁Apprch闭锁HMI解锁_重锁不执行")
    @pytest.mark.full
    def test_caseid_1995327(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        
    @allure.title("重锁_离车落锁Apprch闭锁内部其它方式InsOth解锁_重锁不执行")
    @pytest.mark.full
    def test_caseid_1995326(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth)

    @allure.title("重锁_离车落锁Apprch闭锁NFC解锁_重锁不执行")
    @pytest.mark.full
    def test_caseid_1995325(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)

    @allure.title("重锁_IntrSwt闭锁Apprch解锁_重锁不执行")
    @pytest.mark.full
    def test_caseid_1995324(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("462858 重锁_车速SpdAut闭锁Apprch解锁_重锁不执行")
    @pytest.mark.full
    def test_caseid_1995323(self):  
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, vehmtnst=VehMtnSts.StandStillVal2)  
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("重锁_InsOth闭锁Apprch解锁_重锁不执行")
    @pytest.mark.full
    def test_caseid_1995322(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        
    @allure.title("重锁_RKE闭锁Apprch解锁_relocking计时期间开启引擎盖重锁不执行")
    @pytest.mark.full
    def test_caseid_1995321(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(20)
        self.io.set_hood_sts(sts=HoodSts.Open)
        sleep(10)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("重锁_Keyls闭锁Apprch解锁_relocking计时期间开启尾门重锁不执行")
    @pytest.mark.full
    def test_caseid_1995320(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        sleep(25)
        self.io.set_door(Trunk=Door.open)
        sleep(5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.io.set_door(Trunk=Door.close)

    @allure.title("重锁_重锁TmrAut闭锁Apprch解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995319(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(29.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(10)
        self.io.set_door(Drvr=Door.open)
        sleep(20)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.io.set_door(Drvr=Door.close)

    @allure.title("重锁_远控Telm闭锁Apprch解锁_relocking计时期间开启副驾门重锁不执行")
    @pytest.mark.full
    def test_caseid_1995318(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(10)
        self.io.set_door(Pass=Door.open)
        self.io.set_door(Pass=Door.close)
        sleep(20)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("重锁_外部其它方式OutsOth闭锁Apprch解锁_relocking计时期间开启左后门重锁不执行")
    @pytest.mark.full
    def test_caseid_1995317(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(10)
        self.io.set_door(LeRe=Door.open)
        sleep(20)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.io.set_door(LeRe=Door.close)

    @allure.title("重锁_NFC闭锁Apprch解锁_relocking计时期间开启右后门重锁不执行")
    @pytest.mark.full
    def test_caseid_1995316(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(10)
        self.io.set_door(RiRe=Door.open)
        sleep(20)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.io.set_door(RiRe=Door.close)

    @allure.title("RKE闭锁Apprch解锁_relocking计时期间UsageMode上切到Convenience重锁不执行")
    @pytest.mark.full
    def test_caseid_1995315(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(20)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(10)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("重锁_远控Telm闭锁Apprch解锁_relocking计时期间UsageMode上切到Active重锁不执行")
    @pytest.mark.full
    def test_caseid_1995314(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(20)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(10)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("重锁_外部其它方式OutsOth闭锁Apprch解锁_UsageMode上切到Driving重锁不执行")
    @pytest.mark.full
    def test_caseid_1995313(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(20)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(10)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("RKE闭锁Apprch解锁_relocking计时期间UsageMode上切到Convenience重锁不执行")
    @pytest.mark.full
    def test_caseid_1995312(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(10)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        sleep(20)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("重锁_RKE闭锁Apprch解锁_relocking计时期间Telm闭锁重锁不执行")
    @pytest.mark.full
    def test_caseid_1995311(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(10)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        sleep(20)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("462858 重锁_RKE闭锁Apprch解锁_钥匙遗留车内重锁不执行")
    @pytest.mark.full
    def test_caseid_1995309(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(20)
        self.bus_comm.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        sleep(10)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("离车落锁_尾门MovgDownBrkg&&四门全关_不触发关门提示")
    @pytest.mark.full
    def test_caseid_1987090(self):  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_tailgate_opener_sts(sts=TailGateOpenerSts.MovgDownBrkg)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_Lock_and_unlock_remind(lockstsprmt= LockStsPrmt.Idle, timeout=5)
        sleep(5)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title("离车落锁_尾门Ukwn&&四门全关_不触发关门提示")
    @pytest.mark.full
    def test_caseid_1987089(self):  
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_tailgate_opener_sts(sts=TailGateOpenerSts.Ukwn)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_Lock_and_unlock_remind(lockstsprmt= LockStsPrmt.Idle, timeout=5)
        sleep(5)
        self.io.set_door(Trunk=Door.close)  # Ukwn关掉也不闭锁
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("离车落锁_尾门HalfClsd&&10sFullClsd内尾门关闭中央落锁")
    @pytest.mark.full
    def test_caseid_1985630(self):  
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_tailgate_opener_sts(sts=TailGateOpenerSts.HalfClsd)
        sleep(1)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        sleep(10)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)

    @allure.title(" 重锁_RKE闭锁Apprch解锁_引擎盖开启重锁不执行")
    @pytest.mark.full
    def test_caseid_1995308(self):  
        self.io.set_hood_sts(sts=HoodSts.Open)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(30)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.io.set_hood_sts(sts=HoodSts.Close)
        
    @allure.title("462858 重锁_NFC闭锁PE解锁_relocking")
    @pytest.mark.full
    def test_caseid_1995307(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        sleep(30)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_离车落锁Apprch闭锁Apprch解锁_LockgEventTrigsrc检测")
    @pytest.mark.V220
    @pytest.mark.sanity
    def test_caseid_1995306(self):       
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(28)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.TmrAut, time_wait=3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("重锁_RKE闭锁Apprch解锁_relocking计时期间UsageMode下切到Abandoned重锁正常执行")
    @pytest.mark.V220
    @pytest.mark.full
    def test_caseid_1995305(self):  
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        sleep(20)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(10)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)

    @allure.title("离车落锁_四门全开&&10s计时器内关闭_中央落锁")
    @pytest.mark.full
    def test_caseid_1985631(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.io.set_door(Drvr=Door.open, Pass= Door.open, LeRe=Door.open, RiRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        sleep(7)
        self.io.set_door(Drvr=Door.close, Pass= Door.close, LeRe=Door.close, RiRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)  

    @allure.title("离车落锁_离车落锁关主驾&&10s内主驾门关闭_整车落锁")
    @pytest.mark.full
    def test_caseid_1985552(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2) 
        self.io.set_door(Drvr=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        sleep(10)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)  

    @allure.title("离车落锁_离车落锁关主驾&&副驾驾门开_闭锁请求忽略")
    @pytest.mark.full
    def test_caseid_1985551(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2) 
        self.io.set_door(Pass=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        sleep(10)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("离车落锁关五门_15s内关门中控上锁")
    @pytest.mark.full
    def test_caseid_111315(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.io.set_door(Drvr=Door.open, Pass= Door.open, LeRe=Door.open, RiRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        sleep(12)
        self.io.set_door(Drvr=Door.close, Pass= Door.close, LeRe=Door.close, RiRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)  

    @allure.title("近车解锁_小角度开门30s计时内Zone7钥匙占位_2段开门请求open")
    @pytest.mark.full
    def test_caseid_1985390(self):  
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7, valid= Validity.NotValid)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        sleep(.5)  # 等待配置生效
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.OpenMinang,
                                            trigger_src=LockTrigerSource.KeyRem)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,
                                            trigger_src=LockTrigerSource.NoTrigSrc)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.HalfClsd)
        self.io.set_door(Drvr=Door.open)
        sleep(20)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7, valid= Validity.Valid)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,
                                            trigger_src=LockTrigerSource.KeyRem)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,
                                            trigger_src=LockTrigerSource.NoTrigSrc)
        self.mix.set_lock_and_door_restore_default(door_opener=DoorOpenerSts.Ukwn, door_sts=Door.close, engine=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        self.bus_comm.set_bncm_key_key_zone(zone=Zone.Zone7, valid= Validity.NotValid)

    @allure.title("离车落锁_仲裁逻辑_离车落锁关5s计时内触发PE闭锁 _离车落锁中断")
    @pytest.mark.full
    def test_caseid_1986442(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.io.set_door(Drvr=Door.open, Pass= Door.open, LeRe=Door.open, RiRe=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        sleep(6)
        self.io.set_door(Drvr=Door.close, Pass= Door.close, LeRe=Door.close, RiRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("离车落锁_仲裁逻辑_离车落锁关门5s计时期间RKE关门上锁 _离车落锁中断")
    @pytest.mark.full
    def test_caseid_1986436(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.bus_comm.set_four_door_opener_sts(door_opener=DoorOpenerSts.FullOpend)
        self.io.set_door(Drvr=Door.open, Pass= Door.open, LeRe=Door.open, RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc)
        sleep(6)
        self.io.set_door(Drvr=Door.close, Pass= Door.close, LeRe=Door.close, RiRe=Door.close)
        self.bus_comm.set_four_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.mix.set_lock_and_door_restore_default(engine=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("离车落锁关门等待关门5s计时器内外部按键关闭主驾门_离车落锁中断")
    @pytest.mark.full
    def test_caseid_1986440(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5, pe_test=True)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt, timeout=2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5)
        sleep(6)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.mix.set_lock_and_door_restore_default(engine=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("离车落锁_仲裁逻辑_离车落锁关门等待关门计时器5s内服务请求关闭副驾门_离车落锁中断")
    @pytest.mark.full
    def test_caseid_1986439(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.io.set_door(Drvr=Door.open, Pass= Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Close,trigger_src=DoorTrigerSource.HMI)
        sleep(6)
        self.io.set_door(Drvr=Door.close, Pass= Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=3) 
        self.mix.set_lock_and_door_restore_default(engine=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("离车落锁_仲裁逻辑_离车落锁关门计时5s内远控关门上锁 _离车落锁中断")
    @pytest.mark.full
    def test_caseid_1986415(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.bus_comm.set_four_door_opener_sts(door_opener=DoorOpenerSts.FullOpend)
        self.io.set_door(Drvr=Door.open, Pass= Door.open, LeRe=Door.open, RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=2)
        sleep(3)
        self.io.set_door(Drvr=Door.close, Pass= Door.close, LeRe=Door.close, RiRe=Door.close)
        self.bus_comm.set_four_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)  
        self.mix.set_lock_and_door_restore_default(engine=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("离车落锁_仲裁逻辑_离车落锁关门等待关门计时6s服务请求关闭副驾车门_关门请求忽略")
    @pytest.mark.full
    def test_caseid_1986444(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3) 
        self.io.set_door(Drvr=Door.open, Pass= Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1) # 等前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio, time_wait=5) 
        sleep(3)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Close,trigger_src=DoorTrigerSource.HMI)
        sleep(6)
        self.io.set_door(Drvr=Door.close, Pass= Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch) 
        self.mix.set_lock_and_door_restore_default(engine=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("RKE关上锁关门触发源校验")
    @pytest.mark.full
    def test_caseid_1988582(self):
        self.io.set_door(Drvr=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=3)  # 校验上条case车门动作请求有没有恢复默认值
        sleep(1) # 等前置条件生效
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=2) 
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc) 
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)