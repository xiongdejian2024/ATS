#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_lock_ctrl_wti_abc.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM门锁告警
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
@allure.story("BGM门锁告警")
class TestCentralLockWTIService(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            [
                "CentralLockService_client",
                "DoorService_client",
                "TailGateService_client",
                "KeyService_client",
                "WTIService_client",
                "EntryService_client",
                
            ]
        )
        sleep(2)

    def before_each_func(self, ecu):
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)

    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_NFC闭锁联动关门_五门开启6.5s内关闭无防夹_无提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985643(self): 
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.send_nfc_cmd()
        sleep(1)  # 长刷
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        sleep(6)
        self.io.set_five_door_sts(Door.open)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_PE闭锁联动左后门关闭&&车门处于正在开启MovgOut_无提示")
    @pytest.mark.full
    def test_caseid_1985640(self):
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        sleep(2)  # 等待前置条件生效
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 1)
        self.soa.hmi_get_door_anti_pinch_sts(DoorId.kDoorFrontRight, isantipinch=True)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 0)

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_NFC闭锁联动关门_五门开启6.5s内关闭无防夹_无提示")
    @pytest.mark.full
    def test_caseid_1985639(self): 
        self.io.set_five_door_sts(Door.open)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOutBrkg)
        sleep(2)  # 等待前置条件生效
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 1)
        self.soa.hmi_get_door_anti_pinch_sts(DoorId.kDoorFrontRight, isantipinch=True)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 0)

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_NFC闭锁联动主驾门关闭_6.5s内尾门触发防夹&&尾门其它状态_正常提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985637(self): 
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 9)  
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.send_nfc_cmd()
        sleep(1)  # 长刷
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        sleep(5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 1)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseFailByNfcPe, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)


    @allure.title("MSO-SREQ-13252 闭锁告警提醒_NFC闭锁联动主驾门关闭_6.5s内尾门触发防夹&&尾门MovgUpBrkg_正常提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985636(self): 
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 3)  
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.send_nfc_cmd()
        sleep(1)  # 长刷
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        sleep(4)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 1)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseFailByNfcPe, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)


    @allure.title("MSO-SREQ-13252 闭锁告警提醒_NFC闭锁联动主驾门关闭_6.5s内尾门触发防夹&&尾门MovgUp_正常提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985635(self): 
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 2)  
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.send_nfc_cmd()
        sleep(1)  # 长刷
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        sleep(5.5)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 1)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseFailByNfcPe, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_NFC闭锁联动主驾门关闭_6.5s超时触发防夹提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985634(self): 
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.send_nfc_cmd()
        sleep(1)  # 长刷
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        sleep(7)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 1)
        self.soa.hmi_get_door_anti_pinch_sts(DoorId.kDoorFrontLeft, isantipinch=True)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseFailByNfcPe, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_PE闭锁联动左后门关闭_6.5s超时触发防夹_无提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985633(self): 
        self.io.set_door(LeRe=Door.open)
        sleep(2)  # 等待前置条件生效
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        sleep(7)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeReAntiPnch", 1)
        self.soa.hmi_get_door_anti_pinch_sts(DoorId.kDoorRearLeft, isantipinch=True)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeReAntiPnch", 0)

    @allure.title("MSO-SREQ-13252_闭锁状态告警_离车闭锁&&存在非主驾门未关_无提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985618(self): 
        self.io.set_door(Pass=Door.open)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(2)  # 等待前置条件生效
        self.bus_comm.send_approach_unlock_cmd()
        sleep(1)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_PE闭锁联动左后门关闭_6.5s内副驾触发防夹提示")
    @pytest.mark.longtime
    @pytest.mark.full
    def test_caseid_1985482(self): 
        self.io.set_door(Pass=Door.open)
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 1)
        self.soa.hmi_get_door_anti_pinch_sts(DoorId.kDoorFrontRight, isantipinch=True)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseFailByNfcPe, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)

    @allure.title("MSO-SREQ-13252 闭锁告警提醒_NFC闭锁联动主驾门关闭_6.5s超时触发防夹_正常提示")
    @pytest.mark.full
    def test_caseid_1985481(self): 
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 1)
        self.bus_comm.send_nfc_cmd()
        sleep(1)  # 长刷
        self.bus_comm.set_singal("connectivitycanfd", "NfcrConnFr02", "NFCStatus", 0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 1)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseFailByNfcPe, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        
    @allure.title("WTI_ 关门失败_关门失败请手动关门1")
    @pytest.mark.full
    def test_caseid_1983058(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 1)
        self.soa.hmi_get_door_postion(doors=DoorPos.All,door_pos=DoorPos.Dirver,pos=1)
        self.soa.hmi_set_door_postion(door_pos=DoorPos.Dirver, pos=0)
        sleep(3)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseDoorFail, DoorRemind.NoRequest)  
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.soa.event_check_warning_info_list(name = "Please Manual Close Door", info="1")
        self.soa.event_check_warning_info_list(name = "Please Manual Close Door", info="0")

    @allure.title("WTI_解闭锁提醒1_锁车失败，需要NFC长刷 NFC")
    @pytest.mark.full
    def test_caseid_1982702(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.send_nfc_cmd()
        self.soa.get_and_event_check_warning_info_list(name = "Unlock Reminder", info="1")     
        self.io.set_door(Drvr=Door.close)  
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.soa.get_and_event_check_warning_info_list(name = "Unlock Reminder", info="0")       

    @allure.title("WTI_解闭锁提醒2_因车门故障关门上锁失败_防夹")
    @pytest.mark.full
    def test_caseid_1982716(self):
        self.io.set_door(Pass=Door.open)
        sleep(.5)  # 等待前置条件生效
        self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=2.5)
        sleep(4.5)  #6.5s计时器
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 1)
        self.soa.hmi_get_door_anti_pinch_sts(DoorId.kDoorFrontRight, isantipinch=True)
        self.soa.notyfy_lock_warn_info(LockWarn.CloseFailByNfcPe, DoorRemind.NoRequest)  
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.soa.event_check_warning_info_list(name = "Door Cannot Closed Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 0)
        self.soa.event_check_warning_info_list(name = "Door Cannot Closed Reminder", info="0")

    # @allure.title("MSO-SVRIF-3901_WTI_解闭锁提醒5_无有效钥匙")
    # @pytest.mark.update_1
    # @pytest.mark.full
    # def test_caseid_1982729(self):
    #     self.bus_comm.reset_bncm_digital_keyinfo() # 所有区域无钥匙
    #     sleep(.5)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.1)
    #     self.soa.notyfy_lock_warn_info(LockWarn.NoKey, DoorRemind.NoRequest) 
    #     self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest) 
    #     self.soa.event_check_warning_info_list(name = "No Key Present", info="1")
    #     self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
    #     self.soa.event_check_warning_info_list(name = "No Key Present", info="0")

    @allure.title("MSO-SVRIF-3589_WTI_解闭锁提醒4_离车落锁关门失败触发车外关门提醒")
    @pytest.mark.full
    def test_caseid_1982727(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.event_check_warning_info_list(name = "Cannot unLock", info="2")
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_warning_info_list(name = "Cannot unLock", info="0")

    # @allure.title("MSO-SVRIF-3589_WTI_解闭锁提醒4_车速关门失败触发车内关门提醒")
    # @pytest.mark.update_1
    # @pytest.mark.full
    # def test_caseid_1982728(self):
    #     self.io.set_door(Door.open)
    #     self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr06", "VehSpdLgtQf", 3)
    #     self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr06", "VehSpdLgtA", 7)  
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
    #     sleep(1.4)
    #     self.soa.notyfy_lock_warn_info(LockWarn.CloseDoorFail, DoorRemind.CloseDoorInside)
    #     # self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr06", "VehSpdLgtQf", 3)
    #     # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3) 
    #     # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 498) 
    #     # sleep(1.3)
    #     self.soa.event_check_warning_info_list(name = "Cannot unLock", info="1")

    @allure.title("关门提示_通知及获取进入系统的报警信息_主驾门Open&&主驾触发热保护_离车闭锁无提示")
    @pytest.mark.full
    def test_caseid_1986475(self): 
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean1", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontLeft, doorfaultsts=DoorfFultSts.ThermalProtection)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio) 
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean1", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("关门提示_通知及获取进入系统的报警信息_主驾门Open&&主驾车身横摆角异常_离车闭锁无提示")
    @pytest.mark.full
    def test_caseid_1986474(self): 
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean3", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontLeft, doorfaultsts=DoorfFultSts.RollAngleAbnormal)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean3", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("通知及获取进入系统的报警信息_右后门Open&&右后门道路倾斜角异常_离车闭锁无提示")
    @pytest.mark.full
    def test_caseid_1986473(self): 
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DtcInfDoorRiReBoolean4", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorRearRight, doorfaultsts=DoorfFultSts.RoadInclinationAbnormal)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DtcInfDoorRiReBoolean4", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("关门提示_通知及获取进入系统的报警信息_右前门Open&&右前门霍尔传感器异常_离车闭锁无提示")
    @pytest.mark.full
    def test_caseid_1986472(self): 
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean5", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontRight, doorfaultsts=DoorfFultSts.HallSensorsError)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean5", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)
 
    @allure.title("关门提示_通知及获取进入系统的报警信息_左后门Open&&左后门道路倾斜角异常_离车闭锁无提示")
    @pytest.mark.full
    def test_caseid_1986471(self): 
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean4", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorRearLeft, doorfaultsts=DoorfFultSts.RoadInclinationAbnormal)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean4", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("关门提示_通知及获取进入系统的报警信息_主驾门Open&&副驾横摆角度故障_离车闭锁正常提示")
    @pytest.mark.full
    def test_caseid_1986470(self): 
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean3", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontRight, doorfaultsts=DoorfFultSts.RollAngleAbnormal)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio) 
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.CloseDoorWalkAway)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean3", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("关门提示_通知及获取进入系统的报警信息_中央尾门解锁状态_离车落锁触发无提示告警")
    @pytest.mark.full
    def test_caseid_1986468(self): 
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        sleep(3)  # 延时获取锁状态
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.send_walk_away_lock_cmd()
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.Idle) 
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)

    @allure.title("关门提示_通知及获取进入系统的报警信息_中央解锁尾门关闭主驾门开启&&主驾触发防玩_无提示告警")
    @pytest.mark.full
    def test_caseid_1986467(self): 
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean2", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontLeft, doorfaultsts=DoorfFultSts.FaultPlayProtectionActive, time_wait=3)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean2", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("关门提示_通知及获取进入系统的报警信息_中央解锁四门及尾门关闭_无提示告警")
    @pytest.mark.full
    def test_caseid_1986466(self): 
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.Idle) 
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)

    @allure.title("MSO-SREQ-13793 关门提示_通知及获取进入系统的报警信息_四门关闭尾门开启_离车闭锁告触发告警")
    @pytest.mark.Bug
    @pytest.mark.full
    def test_caseid_1986461(self): 
        self.io.set_door(Trunk=Door.open)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio) 
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.CloseDoorWalkAway)

    @allure.title("MSO-SREQ-13793 关门提示_通知及获取进入系统的报警信息_主驾门Open&&无故障_离车闭锁触发告警")
    @pytest.mark.full
    def test_caseid_1986459(self):
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 3) 
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr38", "LockgEventTrigsrc", 9) 
        self.soa.check_envent_lock_reminder(lockreminder=LockReminder.WalkAwayAudio)      
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.CloseDoorWalkAway)
