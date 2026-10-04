#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_centrallock_communiaction_safety_abc.py
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


@allure.feature("Locking功能安全")
@allure.story("锁控制")
class TestCentralLockCommuniactionSafetyCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            [
                "CentralLockService_client",
                "DoorService_client",
                "TailGateService_client",
                "KeyService_client",
                "VehicleSetStatusService_client", 

            ]
        )
        sleep(2)

    def before_each_func(self, ecu):
        self.io.set_five_door_sts(Door.close)
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83, 10: 0x2})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(2)  # 避免触发防玩
        
    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
            self.soa.hmi_set_wash_mode(isOn.Off)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("498583 v26 车速自动落锁_VehSpdLgtA == 7.02_中控解锁")
    @pytest.mark.sanity
    def test_caseid_1986483(self):
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)

    @allure.title("463009 解闭锁设置项_近车解锁开门设置开启_断电重启NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1986486(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0)  
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "ApproachUnlockHmi", 1)  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=1)  
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "ApproachUnlockHmi", 0)  
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.io.io_reset_bgm()
        time.sleep(5)
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "ApproachUnlockHmi", 0)  
 

    @allure.title("463009 解闭锁设置项_离车闭锁仅关主驾门设置开启_断电重启NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1986487(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 0)  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)    
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)    
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.io.io_reset_bgm()
        sleep(5)
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)    

    @allure.title("463009 解闭锁设置项_离车闭锁关四门设置开启_断电重启NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1986491(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 0)  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)    
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)    
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.io.io_reset_bgm()
        sleep(5)
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3)  

    @allure.title("466165 内部开关解禁用_外部闭锁开门内开关禁用解锁解禁用")
    @pytest.mark.sanity
    def test_caseid_1986493(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        # self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Idle, trigger_src=DoorTrigerSource.NoTrigSrc)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_four_door_opener_req(door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)

    @allure.title("466165 内部开关解禁用_外部闭锁开门内开关禁用解锁解禁用")
    @pytest.mark.full
    def test_caseid_1986556(self):
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_tailgate_opener_req(SetTailGatePos.Open)

    @allure.title("489522 开门开关输入安全机制_内开关控制电动门开")
    @pytest.mark.full
    def test_caseid_1986684(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 1)  
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Idle,trigger_src=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_singal("bodycan", "DdmBodyFr04", "DoorDrvrOpenReqInsdSwt1", 1)  
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrOpenReqInsdSwt2", 1)  
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.InsdSwt)

    @allure.title("489522 开门开关输入安全机制_外开关控制电动门开")
    @pytest.mark.full
    def test_caseid_1986685(self):
        self.bus_comm.set_singal("backbonefr", "VddmBackBoneFr00", "EngSt1WdStsEngSt1WdSts", 8)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.io.trigger_door_outswitch_sts(Pass=OutSwitchPressSts.Press)
        self.io.trigger_door_outswitch_sts(Pass=OutSwitchPressSts.NoPress)
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Idle,trigger_src=DoorTrigerSource.NoTrigSrc)
        self.mix.push_door_outer_switch(DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.OutdSwt)
        self.bus_comm.set("bodycan","PpodBodyFr01", 'DoorPassOpenReqOutdSwt2', 0)
        self.bus_comm.check_door_opener_req(pass_opener= DoorPos.Pass, door_req=DoorOpenerReq.Idle,trigger_src=DoorTrigerSource.NoTrigSrc)

    @allure.title("457942_VehMtnSt通信安全机制_crash模式下开门可见反馈")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_115439(self):
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.Ukwn)
        time.sleep(15)  # crash发生，15s门不可控
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On, Pass=DoorRelsReq.On, ReLe=DoorRelsReq.On,
                                        RiRe=DoorRelsReq.On)

    @allure.title("457942_VehMtnSt通信安全机制_crash模式下开门可见反馈")
    @pytest.mark.sanity
    @pytest.mark.mcu_test
    def test_caseid_115439(self):
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.Off, Pass=DoorRelsReq.Off, ReLe=DoorRelsReq.Off,
                                        RiRe=DoorRelsReq.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.Ukwn)
        time.sleep(15)  # crash发生，15s门不可控
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorAll, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_rels_req(Drv=DoorRelsReq.On, Pass=DoorRelsReq.On, ReLe=DoorRelsReq.On,
                                        RiRe=DoorRelsReq.On)

    @allure.title("闭锁后IntrSwtDiTi计时期间触发蓝牙解锁_开关解禁用")
    @pytest.mark.full
    def test_caseid_1991611(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("蓝牙闭锁10s后大屏开关禁用")
    @pytest.mark.full
    def test_caseid_1991631(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(drv_opener= DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("远控闭锁HMI控制四门指定开度开关禁用")
    @pytest.mark.full
    def test_caseid_1991630(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.RearLeft, perc_position=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearLeft, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearLeft, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("NFC闭锁10s后_HMI开启侧门开关禁用")
    @pytest.mark.full
    def test_caseid_1991629(self):
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(drv_opener= DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("PE闭锁计时10s_HMI控制副驾门开启20°_开关禁用")
    @pytest.mark.full
    def test_caseid_1991628(self):
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 20)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("重锁计时10s后HMI控制左后门开_开关禁用")
    @pytest.mark.full
    def test_caseid_1991627(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        time.sleep(1)  # 避免仲裁逻辑触发
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(lere_opener= DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("离车落锁计时10s后_HMI控制左后门开开关禁用")
    @pytest.mark.full
    def test_caseid_1991626(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(lere_opener= DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外部其他方式闭锁HMI控制右后门开_开关禁用")
    @pytest.mark.full
    def test_caseid_1991625(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(rire_opener= DoorOpenerReq.Idle)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI闭锁计时10sHMI控制右后门开_HMI开关不禁用")
    @pytest.mark.full
    def test_caseid_1991624(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内部其它方式闭锁计时10s后HMI控制车门开50°_HMI开关不禁用")
    @pytest.mark.full
    def test_caseid_1991623(self):
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 50)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=50, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车速落锁计时10s_HMI开关不禁用")
    @pytest.mark.full
    def test_caseid_1991622(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2)  
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        time.sleep(10)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, door_trigsrc=DoorTrigerSource.HMI) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("NFC闭锁开关禁用远控解锁_开关解禁用")
    @pytest.mark.full
    def test_caseid_1991621(self):
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        time.sleep(10)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open,)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI, timeout=3)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        
    @allure.title("离车落锁开关禁用计时器内主驾门开启10°_开关解禁用整车解锁")
    @pytest.mark.full
    def test_caseid_1991609(self):
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Dirver, perc_position=0)
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        sleep(2)  # 避免闭锁联动关门影响开门逻辑
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("PE闭锁开关禁用计时器内HMI开启左后门_开关解禁用整车解锁")
    @pytest.mark.full
    def test_caseid_1991608(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls, timeout=2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(5)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("NFC闭锁开关禁用计时器内HMI控制右后门开_开关解禁用整车")
    @pytest.mark.full
    def test_caseid_1991607(self):    
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        time.sleep(6)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("NFC闭锁开关禁用计时器内HMI控制右后门开_开关解禁用整车")
    @pytest.mark.full
    def test_caseid_1992558(self):    
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.RearRight, perc_position=0)
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        time.sleep(1)  # 避免仲裁逻辑触发
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        time.sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        time.sleep(7)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearRight, pos= 50)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearRight, position=50, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外部其方式闭锁副驾HMI开启指定角度_开关解禁用整车解锁")
    @pytest.mark.full
    def test_caseid_1992560(self):
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 50)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=50, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间主驾门from close change to Open_开关解禁用")
    @pytest.mark.full
    def test_caseid_1991606(self):    
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        time.sleep(4)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        time.sleep(6)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间副驾门from close change to Open_开关解禁用")
    @pytest.mark.full
    def test_caseid_1991605(self):    
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        time.sleep(10)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间左后门from close change to Open_开关解禁用")
    @pytest.mark.full
    def test_caseid_1991604(self):    
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        time.sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间左后门from close change to Open_开关解禁用")
    @pytest.mark.full
    def test_caseid_1991603(self):    
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        time.sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("远控闭锁主驾门HMI开门解锁_开关不禁用整车解锁")
    @pytest.mark.full
    def test_caseid_1991610(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        time.sleep(2)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI, timeout=3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间尾门from close change to Open_开关不禁用")
    @pytest.mark.full
    def test_caseid_1991602(self):
        self.bus_comm.set_child_lock_sts(side=Side.Right, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间UsageMode上切到Active_开关不禁用")
    @pytest.mark.full
    def test_caseid_1991600(self):
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 11)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间UsageMode上切到Driving_开关不禁用")
    @pytest.mark.full
    def test_caseid_1991601(self):
        self.bus_comm.set_child_lock_sts(side=Side.Left, childlockstatus= OnOffSafe1.OnOffSafeOff)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间HMI设置副驾门开_开关不禁用")
    @pytest.mark.full
    def test_caseid_1991586(self):    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgIn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Closing, isopen=False, antipinch=False)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间HMI设置左后门关_开关解禁用")
    @pytest.mark.full
    def test_caseid_1991585(self):    
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Dirver, perc_position=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间HMI设置右后门暂停_开关禁用")
    @pytest.mark.full
    def test_caseid_1991584(self):    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Dirver, perc_position=0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.RearRightDoorSts, doormovests=DoorMoveStatus.Opening, isopen=False, antipinch=False)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Stop)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req=DoorOpenerReq.Stop, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(10)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("不同CarMode模式下中央锁定行为_Factory模式RKE闭锁禁用")
    @pytest.mark.full
    def test_caseid_1991644(self):    
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)  # 工厂模式锁源可能是内部方式可以确定不闭锁

    @allure.title("不同CarMode模式下中央锁定行为_Factory模式外部方式闭锁禁用")
    @pytest.mark.full
    def test_caseid_1991641(self):    
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("不同CarMode模式下中央锁定行为_Transport模式内部方式闭锁禁用")
    @pytest.mark.full
    def test_caseid_1991640(self):    
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("NFC闭锁蓝牙解锁_开关不禁用")
    @pytest.mark.full
    def test_caseid_1991620(self):    
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Dirver, perc_position=0)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)

    @allure.title("蓝牙闭锁远控解锁_尾门开度开关不禁用")
    @pytest.mark.full
    def test_caseid_1991619(self):    
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)  # 防止触发仲裁逻辑不执行闭锁
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.soa.hmi_set_tailgate_postion(pos=10)
        self.bus_comm.check_singal("bodycan", "CemBodyFr131", "TrOpenPosnReqFromHmi", 10)

    @allure.title("闭锁后IntrSwtDiTi计时期间UsageMode上切到Convenience开关禁用")
    @pytest.mark.sanity
    def test_caseid_1991583(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(pass_opener= DoorOpenerReq.Idle)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间UsageMode上切到Inactive开关禁用")
    @pytest.mark.full
    def test_caseid_1991582(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(pass_opener= DoorOpenerReq.Idle)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时期间UsageMode下切到Abandoned开关禁用")
    @pytest.mark.sanity
    def test_caseid_1991599(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 0)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(pass_opener= DoorOpenerReq.Idle)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("闭锁后IntrSwtDiTi计时超时副驾门from close change to Open_开关不禁用")
    @pytest.mark.full
    def test_caseid_1991598(self):    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Armd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(11)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Disarmd)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外锁HMI开关禁用整车设防期间UsageMode上切到Active_车辆解防内开关启用")
    @pytest.mark.full
    def test_caseid_1991597(self):  
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Armd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(11)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 11)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Disarmd)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("466165 内开关启用_外锁开关禁用车辆触发防盗_内开关不启用")
    @pytest.mark.full
    def test_caseid_1991596(self):  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Armd)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(30)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_alrm_sts_req(alrm_sts=AlrmSts.Actv)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(pass_opener= DoorOpenerReq.Idle)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外锁内开关禁用PE解锁开关启用")
    @pytest.mark.full
    def test_caseid_1991595(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(10)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外锁内开关禁用近车解锁开关启用")
    @pytest.mark.full
    def test_caseid_1991594(self):
        self.sd_tester.write_ccp(ccp={94: 0x80})
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(10)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        # sleep(2)  # 防止开门触发仲裁逻辑
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外锁内开关禁用NFC解锁开关启用")
    @pytest.mark.full
    def test_caseid_1991593(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock, value=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(10)
        self.bus_comm.send_nfc_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.NFC)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("引擎盖状态 Hood1 Opend & Hood2 Clsd_HoodSts=Clsd")
    @pytest.mark.full
    def test_caseid_1989272(self):
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 2)
        self.io.set_hood1_sts(sts1=HoodSts.Close)
        self.io.set_hood2_sts(sts2=HoodSts.Close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.io.set_hood_sts(sts=HoodSts.Close)

    @allure.title("中央锁状态_LockgEventTrigsrc信号周期监测")
    @pytest.mark.full
    def test_caseid_1989262(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.IntrSwt, time_wait=0.2)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("Driving模式外锁不执行")
    @pytest.mark.full
    def test_caseid_1989367(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.io.driver_seat_notpresent()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=0.2)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst= VehMtnSts.StandStillVal2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("引擎盖状态 Hood1 Opend & Hood2 Opend _HoodSts=Opend")
    @pytest.mark.full
    def test_caseid_1989274(self):
        self.io.set_hood1_sts(sts1=HoodSts.Open)
        self.io.set_hood2_sts(sts2=HoodSts.Close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 2)

    @allure.title("Hood1 Clsd & Hood2 Opend _HoodSts=Opend")
    @pytest.mark.full
    def test_caseid_1989273(self):
        self.io.set_hood1_sts(sts1=HoodSts.Open)
        self.io.set_hood2_sts(sts2=HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 2)

    @allure.title("Hood1 Clsd & Hood2 Opend _HoodSts=Opend")
    @pytest.mark.full
    def test_caseid_110367(self):
        self.io.set_hood_sts(sts=HoodSts.Open)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 1)
        self.io.set_hood_sts(sts=HoodSts.Close)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr06", "HoodSts", 2)

    @allure.title("闭锁后IntrSwtDiTi计时期间主驾门设置开启10°_开关不禁用")
    @pytest.mark.full
    def test_caseid_1991587(self):    
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Dirver, perc_position=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Dirver, position=10, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Close, trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("RKE闭锁关门DelayCloseDoor超时车门Fullopend触发远控关门上锁请求_中断RKE门锁联动")
    @pytest.mark.full
    def test_caseid_1986451(self):    
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm)
        sleep(5)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("RKE闭锁关门DelayCloseDoor计时超时触发HMI解锁请求_HMI请求忽略")
    @pytest.mark.full
    def test_caseid_1986448(self):    
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgIn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closing,isopen=True, antipinch=False) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem)
        sleep(5.5)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Hmi)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.IntrSwt)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("闭锁event非默认值LockgEventTrigsrc周期监测3帧恢复默认值")
    @pytest.mark.full
    def test_caseid_1986450(self):    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=0.2)  # 总线3帧大概0.2s
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("RKE关门Movein请求延时期间远控关门上锁 _远控闭锁忽略整车RKE闭锁")
    @pytest.mark.full
    def test_caseid_1986447(self):   
        self.io.set_door(Drvr=Door.open) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgIn)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Closing,isopen=True, antipinch=False) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm)
        sleep(5)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("RKE闭锁关门DelayCloseDoor计时期间触发远控解锁请求_RKE闭锁不中断")
    @pytest.mark.full
    def test_caseid_1986445(self):   
        self.io.set_door(Drvr=Door.open) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm)
        sleep(5)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("HMI上锁后Trunlock_尾门关闭锁状态恢复Lockd")
    @pytest.mark.full    
    def test_caseid_1985014(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(cmd=TailGateMode.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("离车落锁关门执行中主驾门MovgIn状态_短按主驾车门_主驾门正常关闭离车落锁中断")
    @pytest.mark.full    
    def test_caseid_1919346(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.io.set_door(Drvr=Door.open) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)     
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Apprch, time_wait=1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req=DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("离车落锁关门执行中主驾门MovgIn状态_短按主驾车门_主驾门正常关闭离车落锁中断")
    @pytest.mark.full    
    def test_caseid_1919344(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.io.set_door(Drvr=Door.open) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opened,isopen=True, antipinch=False) 
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0) 
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=2)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass, time_interval=0.2, pe_test=True)
        self.bus_comm.check_door_opener_req(pass_opener=DoorPos.Pass, door_req=DoorOpenerReq.Open, trigger_src=DoorTrigerSource.OutdSwt)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("RKE闭锁联动关门尾门MoveDown状态同时触发远控关门落锁_远控闭锁请求忽略")
    @pytest.mark.full    
    def test_caseid_1919343(self):
        self.bus_comm.set_door_opener_sts(tr_opener=TailGateOpenerSts.MovgDown)
        # self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 6) 
        self.io.set_door(Trunk=Door.open) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Talematics)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Telm, time_wait=2)
        sleep(3)
        self.io.set_door(Trunk=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("主驾车门MovgOut右后车门被短按_右后门Open闭锁中断")
    @pytest.mark.full    
    def test_caseid_1919342(self):
        self.io.set_door(Drvr=Door.open) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.Opening,isopen=True, antipinch=False) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.mix.push_door_outer_switch(pos= DoorPos.RearRight, time_interval=0.2)
        self.bus_comm.check_door_opener_req(rire_opener= DoorPos.RearRight, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.OutdSwt)
        self.bus_comm.check_door_opener_req(rire_opener= DoorPos.RearRight, door_req=DoorOpenerReq.Idle,trigger_src=DoorTrigerSource.NoTrigSrc)
        sleep(3)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullClsd, rire_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("RKE闭锁联动关门尾门MoveDown状态同时触发远控关门落锁_远控闭锁请求忽略")
    @pytest.mark.full    
    def test_caseid_1919341(self):
        self.io.set_door(Drvr=Door.open) 
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.HalfClsd)
        self.soa.check_envent_door_movement_and_antipinch_status(sidedoor=SideDoor.FrntLeftDoorSts, doormovests=DoorMoveStatus.HalfClosed,isopen=True, antipinch=False) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)    
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.mix.push_door_outer_switch(pos= DoorPos.Dirver, time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener= DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.OutdSwt)
        sleep(3)
        self.io.set_door(Drvr=Door.close) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("工厂解锁")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_110347(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.io.io_reset_bgm()
        sleep(5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt, timeout=3)

    @allure.title("HMI控制车门开启到目标位置解锁_开关禁用左后门开启到指定角度不解锁")
    @pytest.mark.full
    def test_caseid_1991686(self):
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.RearLeft, perc_position=0)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.RearLeft, pos= 10)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.RearLeft, position=101, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("HMI控制车门开启到目标位置解锁_TrUnlock副驾门开启50°整车解锁")
    @pytest.mark.full
    def test_caseid_1991685(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.bus_comm.set_door_perc_position(doorpos=DoorPos.Pass, perc_position=0)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)
        sleep(.5)  # 以上都是Precondition
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Pass, pos= 50)
        self.bus_comm.check_door_open_pos_and_trigsrc(doorpos=DoorPos.Pass, position=50, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.IntrSwt)


    @allure.title("HMI开门解锁_车辆非静止HMI开门解锁不执行")
    @pytest.mark.full
    def test_caseid_1991684(self):
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal1)
        sleep(3)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(drv_opener= DoorOpenerReq.Idle)
        sleep(7)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("外部上锁开关禁用HMI开门解锁失效")
    @pytest.mark.full
    def test_caseid_1991683(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal1)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(10)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(drv_opener= DoorOpenerReq.Idle)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("车辆非静止TrUnlock状态下HMI开门解锁不执行")
    @pytest.mark.full
    def test_caseid_1993003(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal1)
        sleep(3)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_without_open_req(drv_opener= DoorOpenerReq.Idle)
        sleep(7)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("尾门开HMI仅闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991682(self):
        self.io.set_door(Trunk=Door.open)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Hmi)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.IntrSwt, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("主驾门开仅闭锁闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991681(self):
        self.io.set_door(Drvr=Door.open)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Hmi)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.IntrSwt, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("整车解锁状态HMI开门_仅开门不解锁")
    @pytest.mark.full
    def test_caseid_1993004(self):
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(1)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Open)
        self.bus_comm.check_door_opener_req(drv_opener= DoorPos.Dirver, door_req=DoorOpenerReq.Open,trigger_src=DoorTrigerSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("HMI开门解锁_车辆非静止HMI开门解锁不执行")
    @pytest.mark.smoke
    def test_caseid_110346(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Hmi)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.IntrSwt, time_wait=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("Crash unlock_CrashStsSafeSts触发Crash整车解锁")
    @pytest.mark.sanity
    def test_caseid_1991648(self):
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem) 
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.Crash) 
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1CarModSts1", 3) 
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Crash, time_wait=2)
        sleep(15)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
                
    @allure.title("CrashStsSafeSts触发Crash解锁使能监测Crash10s恢复默认值")
    @pytest.mark.full
    def test_caseid_1991646(self):
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.Crash)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Crash, time_wait=2)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.All, req=DoorLockCmd.UnlckByCrash0)
        sleep(10)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.All, req=DoorLockCmd.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        # self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1CarModSts1", 0) 
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)

    @allure.title("466340 发送端DoorLockCmd通信安全机制_Crash四门锁使能监测")
    @pytest.mark.sanity
    def test_caseid_1986482(self):
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.Crash)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Crash, time_wait=2)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.All, req=DoorLockCmd.UnlckByCrash0)
        sleep(10)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.All, req=DoorLockCmd.Off)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)

    @allure.title("Crash unlock_车速自动落锁Crash解锁使能监测Crash10s恢复默认值")
    @pytest.mark.full
    def test_caseid_1900114(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)  
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.UsageMode, usagemode=UsageMode.DRIVING)
        self.bus_comm.set_brake_pedal_sts(sts=YesOrNo.Yes)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.Crash)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.CRASH)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Crash, time_wait=2)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.All, req=DoorLockCmd.UnlckByCrash0)
        sleep(10)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.All, req=DoorLockCmd.Off)
        self.bus_comm.set_crashsts_safests(CrashSts= crashsts.NoCrash)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.bus_comm.check_carmode_and_usagemode_sts(mode=VehicleMode.CarMode, carmode=CarMode.NORMAL)
        
    @allure.title("RKE闭锁_车辆配备自动驻车_驻车锁P档EPB处于Off")
    @pytest.mark.full
    def test_caseid_1991671(self):  
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.ParkEngd)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=1)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)

    @allure.title("RKE闭锁_车辆配备自动驻车_驻车锁不处于P档EPB处于On")
    @pytest.mark.full
    def test_caseid_1991670(self):  
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.NotInUse)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)

    @allure.title("RKE闭锁联动关门_车辆配备自动驻车车辆不处于P档不落锁")
    @pytest.mark.full
    def test_caseid_1991669(self):  
        self.sd_tester.write_ccp(ccp={10: 0x02})
        self.bus_comm.set_gear_pos(gear= Gear.Park, parklock=ParkLockSts.NotInUse)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=1)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_wti_signal(func=WTI_Func.EPBWarningChime, value=0)

    @allure.title("RKE闭锁_Convenience模式1.5s内UsageMode下切到Inactive_中央上锁")
    @pytest.mark.full
    def test_caseid_1991668(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.io.driver_seat_notpresent()
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke, time_wait=0.3)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("RKE闭锁_RKE闭锁联动关门_解闭锁动作及四门动作请求及触发源校验")
    @pytest.mark.full
    def test_caseid_1991667(self):
        self.io.set_door(Drvr=Door.open,Pass=Door.open, RiRe=Door.open, LeRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio) 
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=5) 
        self.io.set_door(Drvr=Door.close,Pass=Door.close, RiRe=Door.close, LeRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("RKE闭锁_RKE闭锁联动关门_尾门动作请求及触发源校验")
    @pytest.mark.full
    def test_caseid_1991666(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("RKE闭锁_RKE闭锁联动关门_10s关门期间右后门触发防夹_闭锁退出")
    @pytest.mark.full
    def test_caseid_1991665(self):
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=5) 
        self.bus_comm.set_door_anti_pnch_sts(RiRe=True)
        self.io.set_door(RiRe=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_door_anti_pnch_sts(RiRe=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("RKE闭锁_RKE闭锁联动关门_10s关门期间尾门触发防夹_闭锁退出")
    @pytest.mark.full
    def test_caseid_1991664(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        self.bus_comm.set_tailgate_antiPnch_sts(sts=True)
        sleep(1)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_tailgate_antiPnch_sts(sts=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("RKE解锁_Convenience模式RKE解锁")
    @pytest.mark.full
    def test_caseid_1991663(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)  
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("RKE解锁_Active模式RKE解锁")
    @pytest.mark.full
    def test_caseid_1991662(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, vehmtnst=VehMtnSts.StandStillVal2)
        self.io.driver_seat_present()
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)  
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.io.driver_seat_notpresent()

    @allure.title("RKE解锁_Abandoned模式RKE解锁")
    @pytest.mark.full
    def test_caseid_1991661(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)  
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("RKE解锁_Driving模式RKE解锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991660(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)  
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)  

    @allure.title("KV闭锁_PE闭锁联动关门_尾门防夹触发闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991733(self):
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        self.bus_comm.set_tailgate_antiPnch_sts(sts=True)
        sleep(4)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_tailgate_antiPnch_sts(sts=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("KV闭锁_PE闭锁联动关门_防夹触发闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991732(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt, timeout=5) 
        self.bus_comm.set_door_anti_pnch_sts(Drvr=True)
        sleep(4)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_door_anti_pnch_sts(Drvr=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("PE闭锁联动尾门关_尾门动作请求及触发源监测")
    @pytest.mark.full
    def test_caseid_1991730(self):
        self.io.set_door(Trunk=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        
    @allure.title("KV闭锁_尾门开PE闭锁DelayCloseDoor关门提示监测")
    @pytest.mark.full
    def test_caseid_1991729(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.OutdSwt, timeout=5) 
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("PE闭锁联动尾门关_尾门动作请求及触发源监测")
    @pytest.mark.full
    def test_caseid_1991728(self):
        self.io.set_door(Trunk=Door.open)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_door_opener_req(tr_opener=DoorPos.Tailgate, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.NoTrigSrc, timeout=5) 
        sleep(6)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("KV闭锁_主驾门开PE闭锁10s超时关门_闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991727(self):
        self.io.set_door(Drvr=Door.open)
        self.io.driver_seat_present()
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        sleep(11)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.io.driver_seat_notpresent()

    # @allure.title("KV闭锁_TrUnlock状态主驾门开DoorTailgateCloseTi计时超时关门PE闭锁不执行")
    # @pytest.mark.v140
    # @pytest.mark.update
    # @pytest.mark.full
    # def test_caseid_1991726(self):
    #     self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
    #     sleep(.5)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls)
    #     self.io.set_door(Drvr=Door.open)
    #     self.io.driver_seat_present()
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
    #     self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
    #     sleep(11)
    #     self.io.set_door(Drvr=Door.close)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
    #     self.io.driver_seat_notpresent()

    @allure.title("Unlock状态四门及尾门关闭_PE闭锁")
    @pytest.mark.full
    def test_caseid_1991725(self):
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("KV闭锁_Active主驾有占位闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991724(self):
        self.io.driver_seat_present()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.io.driver_seat_notpresent()

    @allure.title("KV闭锁_Active主驾无占位中控闭锁")
    @pytest.mark.full
    def test_caseid_1991723(self):
        self.io.driver_seat_notpresent()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Pass, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=0.3)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("KV闭锁_Convenience主驾无占位中控闭锁")
    @pytest.mark.full
    def test_caseid_1991722(self):
        self.io.driver_seat_present()
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.io.driver_seat_notpresent()

    @allure.title("KV闭锁_Convenience主驾有占位闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991721(self):
        self.io.driver_seat_notpresent()
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=0.3)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("KV闭锁_洗车模式激活PE闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991720(self):
        self.soa.hmi_set_wash_mode(isOn.On)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=0.3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.soa.hmi_set_wash_mode(isOn.Off)

    @allure.title("KV解锁联动开门_寻钥匙请求校验")
    @pytest.mark.full
    def test_caseid_1991719(self):
        self.bus_comm.check_signal_thread_start('infocanfd', 'BgmInfoCanFdDevFr02', 'KeyReadReqFromLockg')  
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        result_ori = self.bus_comm.check_signal_thread_stop('KeyReadReqFromLockg')  
        logger.info(f'获取到的原始数据KeyReadReqFromLockg为{result_ori}')
        result = get_signal_times_interval(result_ori, 1)
        logger.info("期望值的统计结果:{}".format(result))
        assert result[0] !=0
        self.bus_comm.ipdu.reset_check_results()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("KV解锁联动开门_主驾门动作请求及触发源校验")
    @pytest.mark.full
    def test_caseid_1991718(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.2)
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Open, trigger_src=DoorTrigerSource.OutdSwt, timeout=5) 
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("KV闭锁_Active主驾有占位PE解锁不执行")
    @pytest.mark.full
    def test_caseid_1991716(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_present()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.io.driver_seat_notpresent()

    @allure.title("KV闭锁_Active主驾无占位中控解锁")
    @pytest.mark.full
    def test_caseid_1991717(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_notpresent()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=0.3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("498582 KV解锁_CCP94 不满足 _解锁不执行")
    @pytest.mark.full
    def test_caseid_1991715(self):
        self.sd_tester.write_ccp(ccp={94: 0x00})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=0.3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.sd_tester.write_ccp(ccp={94: 0x02})

    @allure.title("KV解锁_CCP94 = 0x02TrUnlockPE解锁")
    @pytest.mark.full
    def test_caseid_1991714(self):
        self.sd_tester.write_ccp(ccp={94: 0x02})
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(.5)
        self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)

    @allure.title("KV闭锁_Driving主驾无占位_PE闭锁不执行")
    @pytest.mark.full
    def test_caseid_1991680(self):
        self.io.driver_seat_notpresent()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  

    @allure.title("KV闭锁_CCP94 = 0x02PE闭锁")
    @pytest.mark.full
    def test_caseid_1991679(self):
        self.sd_tester.write_ccp(ccp={94: 0x02})
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("498582 KV闭锁_AbandonedPE解锁")
    @pytest.mark.full
    def test_caseid_1991676(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("KV解锁_Abandoned 有占座PE解锁")
    @pytest.mark.full
    def test_caseid_1991678(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_notpresent()
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("KV闭锁_Convenience副驾有占位PE闭锁")
    @pytest.mark.full
    def test_caseid_1994894(self):
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight, seat_sts=SeatOccptSts.OccptLrg)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)  
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight, seat_sts=SeatOccptSts.Empty)

    @allure.title("KV闭锁_Abandoned 主驾无占位中控闭锁")
    @pytest.mark.full
    def test_caseid_1994893(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.push_door_outer_switch(pos=DoorPos.RearLeft, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)  

    @allure.title("KV解锁_convenience主驾有占座解锁不执行")
    @pytest.mark.full
    def test_caseid_1988721(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_present()
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.io.driver_seat_present()

    @allure.title("463009 解闭锁设置项_挂挡自动关门设置项开启_断电重启存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1986492(self):
        self.soa.cancel_auto_close_door_by_gear_driving()
        self.soa.hmi_get_automatic_door_closing(TriggerType.disable)
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.io.io_reset_bgm()
        sleep(15)
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)

    @allure.title("463009 解闭锁设置项_挂挡自动关门设置项开启_1181")
    @pytest.mark.restart
    @pytest.mark.full
    def test_caseid_1994474(self):
        self.soa.cancel_auto_close_door_by_gear_driving()
        self.soa.hmi_get_automatic_door_closing(TriggerType.disable)
        self.soa.hmi_set_auto_close_door_by_drive_gear()  
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)
        self.sd_tester.reset_bgm()
        self.soa.hmi_get_automatic_door_closing(TriggerType.enable)

    @allure.title("不同CarMode模式下中央锁定行为_Transport模式PE闭锁禁用")
    @pytest.mark.full
    def test_caseid_1991642(self):    
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT, vehmtnst=VehMtnSts.StandStillVal2)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.Keyls, time_wait=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)

# 用例ID不对
    @allure.title("RKE闭锁_RKE闭锁联动关门_10s关门期间左后门触发防夹_闭锁退出")
    @pytest.mark.full
    def test_caseid_1991652(self):
        self.io.set_door(Trunk=Door.open, LeRe=Door.open)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd, mai=0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock, source=LockReqSource.Ble_Rke)
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.DoorCloseAudio)
        self.bus_comm.check_door_opener_req(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Close, trigger_src=DoorTrigerSource.KeyRem, timeout=5) 
        self.bus_comm.set_door_anti_pnch_sts(LeRe=True)
        self.io.set_door(Trunk=Door.close, LeRe=Door.close)
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.bus_comm.set_door_anti_pnch_sts(LeRe=False)
        self.bus_comm.set_engine_and_check_energy_level(engine= EngSt1WdStsEngSt1WdSts.EngSt1_Ini)

    @allure.title("内门把手解锁_车辆非静止内按键不解锁")
    @pytest.mark.full
    def test_caseid_1995283(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal2)  
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,  source=LockReqSource.Hmi)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal1)  
        self.bus_comm.press_door_inside_switch(pos=DoorPos.Pass, time_interval=0.2)
        self.bus_comm.check_door_opener_req_and_trigsrc( pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Idle, door_trigsrc=DoorTrigerSource.NoTrigSrc)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)

    @allure.title("498582 PE解锁_Driving 主驾无占座_PE解锁请求忽略")
    @pytest.mark.full
    def test_caseid_1991677(self):
        self.io.driver_seat_present()
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)  
        self.io.driver_seat_notpresent()

    @allure.title("RKE闭锁_covenience模式模式1.5s超时下切到Inactive_中控闭锁不执行")
    @pytest.mark.full
    def test_caseid_110360(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)  
        self.io.driver_seat_notpresent()
        sleep(.5)  # 以上都是Precondition
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock,  source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=0.2)
        sleep(2)  # 1.5s内模式下切会闭锁
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)  
        sleep(3)  # 防止中央锁闭锁延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)

    @allure.title("494582 RKE门锁联动_Active使用者模式1.5s内下切到Inactive整车落锁")
    @pytest.mark.full
    def test_caseid_1892737(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.UnLock,  source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)  
        self.io.driver_seat_notpresent()
        sleep(.5)  # 以上都是Precondition
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.AllDoorCloseAndLock,  source=LockReqSource.Ble_Rke)
        self.soa.check_envent_unlocking_action_sts(sourceid=LockTrigerSource.KeyRem, time_wait=0.2)
        sleep(.8)  # 1.5s内模式下切
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)  
        sleep(3)  # 防止中央锁闭锁延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)