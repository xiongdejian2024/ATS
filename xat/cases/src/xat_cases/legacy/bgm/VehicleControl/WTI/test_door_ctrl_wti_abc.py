#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_door_ctrl_wti_abc.py
@Author      : qian.feng@jiduauto.com
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
@allure.story("BGM电动门告警")
class TestDoorWTIService(TestABCBase):
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
        self.io.set_hood_sts(HoodSts.Close)
        # self.bus_comm.set_gear_pos(Gear.Park, ParkLockSts.ParkEngd)
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

    @allure.title("WTI_前舱盖开报警信息_P挡通知和获取引擎盖告警")
    @pytest.mark.full
    def test_caseid_1985742(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Hood", info="4")
        self.soa.get_warning_msg_List(name="Hood", info="4")
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.event_check_warning_info_list(name = "Hood", info="0")
        self.soa.get_warning_info_list(name = "Hood", info="0")

    @allure.title("WTI_前舱盖开报警信息_N挡通知和获取引擎盖告警")
    @pytest.mark.sanity
    def test_caseid_1981007(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.bus_comm.set_gear_pos(Gear.Neut)
        self.soa.event_check_warning_info_list(name = "Hood", info="4")
        self.soa.get_warning_msg_List(name="Hood", info="4")
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.event_check_warning_info_list(name = "Hood", info="0")
        self.soa.get_warning_info_list(name = "Hood", info="0")

    @allure.title("WTI_前舱盖开报警信息_D挡通知和获取引擎盖告警")
    @pytest.mark.sanity
    def test_caseid_1981008(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.soa.event_check_warning_info_list(name = "Hood", info="5")
        self.soa.get_warning_msg_List(name="Hood", info="5")
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.event_check_warning_info_list(name = "Hood", info="0")
        self.soa.get_warning_info_list(name = "Hood", info="0")

    @allure.title("WTI_前舱盖开报警信息_R挡通知和获取引擎盖告警")
    @pytest.mark.sanity
    def test_caseid_1985743(self):
        self.io.set_hood_sts(HoodSts.Close)
        self.io.set_hood_sts(HoodSts.Open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.soa.event_check_warning_info_list(name = "Hood", info="5")
        self.soa.get_warning_msg_List(name="Hood", info="5")
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.event_check_warning_info_list(name = "Hood", info="0")
        self.soa.get_warning_info_list(name = "Hood", info="0")

    @allure.title("WTI_主驾门开报警信息_D挡通知和获取主驾门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981017(self):
        self.io.set_door(Drvr=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="5")
        self.soa.get_warning_msg_List(name="Driver Door", info="5")
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="0")
        self.soa.get_warning_info_list(name = "Driver Door", info="0")

    @allure.title("WTI_主驾门开报警信息_R挡通知和获取主驾门告警状态")
    @pytest.mark.full
    def test_caseid_1985745(self):
        self.io.set_door(Drvr=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="5")
        self.soa.get_warning_msg_List(name="Driver Door", info="5")
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="0")
        self.soa.get_warning_info_list(name = "Driver Door", info="0")

    @allure.title("WTI_主驾门开报警信息_P挡通知和获取主驾门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981018(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="4")
        self.soa.get_warning_msg_List(name="Driver Door", info="4")
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="0")
        self.soa.get_warning_info_list(name = "Driver Door", info="0")

    @allure.title("WTI_主驾门开报警信息_N挡通知和获取主驾门告警状态")
    @pytest.mark.full
    def test_caseid_1985744(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_gear_pos(Gear.Neut)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="4")
        self.soa.get_warning_msg_List(name="Driver Door", info="4")
        self.io.set_door(Drvr=Door.close)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="0")
        self.soa.get_warning_info_list(name = "Driver Door", info="0")

    @allure.title("WTI_主驾门开报警信息_挡位非D||R||N||P档主驾门告警状态恢复")
    @pytest.mark.sanity
    def test_caseid_1985746(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_gear_pos(Gear.Neut)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="4")
        self.soa.get_warning_msg_List(name="Driver Door", info="4")
        self.bus_comm.set_gear_pos(Gear.Resd1)
        self.soa.event_check_warning_info_list(name = "Driver Door", info="0")
        self.soa.get_warning_info_list(name = "Driver Door", info="0")

    @allure.title("WTI_副驾门开报警信息_D挡通知和获取副驾门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981022(self):
        self.io.set_door(Pass=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="5")
        self.soa.get_warning_msg_List(name="Passenger Door", info="5")
        self.io.set_door(Pass=Door.close)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="0")
        self.soa.get_warning_info_list(name = "Passenger Door", info="0")

    @allure.title("WTI_副驾门开报警信息_R挡通知和获取副驾门告警状态")
    @pytest.mark.full
    def test_caseid_1985747(self):
        self.io.set_door(Pass=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="5")
        self.soa.get_warning_msg_List(name="Passenger Door", info="5")
        self.io.set_door(Pass=Door.close)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="0")
        self.soa.get_warning_info_list(name = "Passenger Door", info="0")

    @allure.title("WTI_副驾门开报警信息_P挡通知和获取副驾门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981026(self):
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="4")
        self.soa.get_warning_msg_List(name="Passenger Door", info="4")
        self.io.set_door(Pass=Door.close)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="0")
        self.soa.get_warning_info_list(name = "Passenger Door", info="0")

    @allure.title("WTI_副驾门开报警信息_N挡通知和获取副驾门告警状态")
    @pytest.mark.full
    def test_caseid_1985748(self):
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_gear_pos(Gear.Neut)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="4")
        self.soa.get_warning_msg_List(name="Passenger Door", info="4")
        self.bus_comm.set_gear_pos(Gear.Resd2)
        self.soa.event_check_warning_info_list(name = "Passenger Door", info="0")
        self.soa.get_warning_info_list(name = "Passenger Door", info="0")

    @allure.title("GID-454737_WTI_左后门开报警信息_P挡通知和获取左后门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981027(self):
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="4")
        self.soa.get_warning_msg_List(name="Rear Left Door", info="4")
        self.io.set_door(LeRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Left Door", info="0")

    @allure.title("WTI_左后门开报警信息_N挡通知和获取左后门告警状态")
    @pytest.mark.full
    def test_caseid_1985775(self):
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.set_gear_pos(Gear.Neut)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="4")
        self.soa.get_warning_msg_List(name="Rear Left Door", info="4")
        self.io.set_door(LeRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Left Door", info="0")

    @allure.title("WTI_左后门开报警信息_D挡通知和获取左后门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981025(self):
        self.io.set_door(LeRe=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="5")
        self.soa.get_warning_msg_List(name="Rear Left Door", info="5")
        self.io.set_door(LeRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Left Door", info="0")

    @allure.title("WTI_左后门开报警信息_R挡通知和获取左后门告警状态")
    @pytest.mark.full
    def test_caseid_1985776(self):
        self.io.set_door(LeRe=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="5")
        self.soa.get_warning_msg_List(name="Rear Left Door", info="5")
        self.io.set_door(LeRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Left Door", info="0")

    @allure.title("WTI_左后门开报警信息_左后门告警状态5==>4==>0")
    @pytest.mark.full
    def test_caseid_1981024(self):
        self.io.set_door(LeRe=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="5")
        self.soa.get_warning_msg_List(name="Rear Left Door", info="5")
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="4")
        self.soa.get_warning_info_list(name = "Rear Left Door", info="4")
        self.io.set_door(LeRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Left Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Left Door", info="0")

    @allure.title("WTI_右后门开报警信息_P挡通知和获取右后门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981029(self):
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="4")
        self.soa.get_warning_msg_List(name="Rear Right Door", info="4")
        self.io.set_door(RiRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Right Door", info="0")

    @allure.title("WTI_右后门开报警信息_D挡通知和获取右后门告警状态")
    @pytest.mark.sanity
    def test_caseid_1981030(self):
        self.io.set_door(RiRe=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="5")
        self.soa.get_warning_msg_List(name="Rear Right Door", info="5")
        self.io.set_door(RiRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Right Door", info="0")

    @allure.title("WTI_右后门开报警信息_N挡通知和获取右后门告警状态")
    @pytest.mark.full
    def test_caseid_1985777(self):
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_gear_pos(Gear.Neut)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="4")
        self.soa.get_warning_msg_List(name="Rear Right Door", info="4")
        self.io.set_door(RiRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Right Door", info="0")

    @allure.title("WTI_右后门开报警信息_R挡通知和获取右后门告警状态")
    @pytest.mark.full
    def test_caseid_1985778(self):
        self.io.set_door(RiRe=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="5")
        self.soa.get_warning_msg_List(name="Rear Right Door", info="5")
        self.io.set_door(RiRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Right Door", info="0")

    @allure.title("WTI_右后门开报警信息_右后门告警状态5==>4==>0")
    @pytest.mark.full
    def test_caseid_1981028(self):
        self.io.set_door(RiRe=Door.open)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="5")
        self.soa.get_warning_msg_List(name="Rear Right Door", info="5")
        self.mix.set_common_precontion(UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="4")
        self.soa.get_warning_info_list(name = "Rear Right Door", info="4")
        self.io.set_door(RiRe=Door.close)
        self.soa.event_check_warning_info_list(name = "Rear Right Door", info="0")
        self.soa.get_warning_info_list(name = "Rear Right Door", info="0")

    @allure.title("WTI_电动门防玩和热保护提醒_右后门触发热保护")
    @pytest.mark.full
    def test_caseid_1982695(self):
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DtcInfDoorRiReBoolean1", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DtcInfDoorRiReBoolean1", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="0")

    @allure.title("WTI_电动门防玩和热保护提醒_左后门触发热保护")
    @pytest.mark.full
    def test_caseid_1982693(self):
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean1", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean1", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="0")

    @allure.title("WTI_电动门防玩和热保护提醒_主驾门触发防玩")
    @pytest.mark.full
    def test_caseid_1982692(self):
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean2", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean2", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="0")
        
    @allure.title("WTI_电动门防玩和热保护提醒_副驾门防玩激活")
    @pytest.mark.full
    def test_caseid_1982690(self):
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean2", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean2", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door AntiPlay Reminder", info="0")

    @allure.title("WTI_通知及获取车门破冰状态_左后门")
    @pytest.mark.full
    def test_caseid_1982598(self):
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr02", "IceBreakDoorRiReActv", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "RrdmBodyFr02", "IceBreakDoorRiReActv", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="0")

    @allure.title("WTI_通知及获取车门破冰状态_左后门")
    @pytest.mark.full
    def test_caseid_1982597(self):
        self.bus_comm.set_singal("bodycan", "RldmBodyFr02", "IceBreakDoorLeReActv", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "RldmBodyFr02", "IceBreakDoorLeReActv", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="0")
  
    @allure.title("WTI_通知及获取车门破冰状态_副驾门")
    @pytest.mark.full
    def test_caseid_1982596(self):
        self.bus_comm.set_singal("bodycan", "PdmBodyFr01", "IceBreakDoorPassActv", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "PdmBodyFr01", "IceBreakDoorPassActv", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="0")

    @allure.title("WTI_通知及获取车门破冰状态_主驾门")
    @pytest.mark.full
    def test_caseid_1982595(self):
        self.bus_comm.set_singal("bodycan", "DdmBodyFr07", "IceBreakDoorDrvrActv", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="1")
        self.bus_comm.set_singal("bodycan", "DdmBodyFr07", "IceBreakDoorDrvrActv", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door Ice Break Reminder", info="0")

    @allure.title("WTI_后排左侧电动门故障报警_通知及获取状态check")
    @pytest.mark.full
    def test_caseid_1982591(self):
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean5", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Sec Left Electric Door Warning", info="1")
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean5", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Sec Left Electric Door Warning", info="0")

    @allure.title("WTI_后排右侧电动门故障报警_通知及获取状态check")
    @pytest.mark.full
    def test_caseid_1982592(self):
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DtcInfDoorRiReBoolean5", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Sec Right Electric Door Warning", info="1")
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DtcInfDoorRiReBoolean5", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Sec Right Electric Door Warning", info="0")

    @allure.title("WTI_副驾电动门故障报警_通知及获取状态check")
    @pytest.mark.full
    def test_caseid_1982590(self):
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean5", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Passenger Electric Door Warning", info="1")
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean5", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Passenger Electric Door Warning", info="0")

    @allure.title("WTI_主驾电动门故障报警_通知及获取状态check")
    @pytest.mark.full
    def test_caseid_1982589(self):
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean5", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Driver Electric Door Warning", info="1")
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean5", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Driver Electric Door Warning", info="0")

    @allure.title("WTI_门雷达报警_左后门毫米波雷达异物遮挡_告警通知info：2")
    @pytest.mark.full
    def test_caseid_1982845(self):
        self.bus_comm.set_singal("connectivitycanfd", "DrmrlConnectivityFr07", "RadarLeReSts", 5)
        self.soa.get_and_event_check_warning_info_list(name = "Left Rear Radar Warning", info="2")
        self.bus_comm.set_singal("connectivitycanfd", "DrmrlConnectivityFr07", "RadarLeReSts", 2)
        self.soa.get_and_event_check_warning_info_list(name = "Left Rear Radar Warning", info="0")

    # @allure.title("右后门毫米波雷达故障_告警通知info：1")
    # @pytest.mark.update_1
    # @pytest.mark.full_1
    # def test_caseid_1982844(self):
    #     self.bus_comm.set_singal("connectivitycanfd", "DrmrrConnectivityFr07", "RadarRiReSts", 4)
    #     self.soa.get_and_event_check_warning_info_list(name = "Right Rear Radar Warning", info="2")
    #     self.bus_comm.set_singal("connectivitycanfd", "DrmrrConnectivityFr07", "RadarRiReSts", 2)
    #     self.soa.get_and_event_check_warning_info_list(name = "Right Rear Radar Warning", info="0")

    @allure.title("左前门毫米波雷达故障_告警通知info：1")
    @pytest.mark.full
    def test_caseid_1982843(self):
        self.bus_comm.set_singal("connectivitycanfd", "DrmflConnectivityFr07", "RadarDrvrSts", 4)
        self.soa.get_and_event_check_warning_info_list(name = "Driver Radar Warning", info="1")
        self.bus_comm.set_singal("connectivitycanfd", "DrmflConnectivityFr07", "RadarDrvrSts", 2)
        self.soa.get_and_event_check_warning_info_list(name = "Driver Radar Warning", info="0")

    @allure.title("WTI_门雷达报警_右前门毫米波雷达异物遮挡_告警通知info：2")
    @pytest.mark.full
    def test_caseid_1982842(self):
        self.bus_comm.set_singal("connectivitycanfd", "DrmfrConnectivityFr07", "RadarPassSts", 5)
        self.soa.get_and_event_check_warning_info_list(name = "Passenger Radar Warning", info="2")
        self.bus_comm.set_singal("connectivitycanfd", "DrmfrConnectivityFr07", "RadarPassSts", 3)
        self.soa.get_and_event_check_warning_info_list(name = "Passenger Radar Warning", info="0")

    @allure.title("WTI_门雷达报警_右前门info：2==>1==>0")
    @pytest.mark.full
    def test_caseid_1985809(self):
        self.bus_comm.set_singal("connectivitycanfd", "DrmfrConnectivityFr07", "RadarPassSts", 5)
        self.soa.get_and_event_check_warning_info_list(name = "Passenger Radar Warning", info="2")
        self.bus_comm.set_singal("connectivitycanfd", "DrmfrConnectivityFr07", "RadarPassSts", 4)
        self.soa.get_and_event_check_warning_info_list(name = "Passenger Radar Warning", info="1")
        self.bus_comm.set_singal("connectivitycanfd", "DrmfrConnectivityFr07", "RadarPassSts", 2)
        self.soa.get_and_event_check_warning_info_list(name = "Passenger Radar Warning", info="0")

    @allure.title("WTI_坡度过大开门提醒_左后门open&&道路倾斜角度不正常_左后门关闭后恢复")
    @pytest.mark.full
    def test_caseid_1982611(self):
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean4", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="1")
        self.io.set_door(LeRe=Door.close)
        # self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean4", 0)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="0")

    @allure.title("WTI_坡度过大开门提醒_副驾门道路倾斜角度不正常道路倾斜角度不正常Boolean4==1")
    @pytest.mark.full
    def test_caseid_1982609(self):
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean4", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="1")       
        self.io.set_door(Pass=Door.close)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="0")       

    @allure.title("WTI_坡度过大开门提醒_主驾门车辆横摆角度不正常Boolean3=1")
    @pytest.mark.full
    def test_caseid_1982608(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean3", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="1")       
        self.io.set_door(Drvr=Door.close)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="0")       

    @allure.title("WTI_坡度过大开门提醒_右后门车辆横摆角度不正常Boolean3=1")
    @pytest.mark.full
    def test_caseid_1985810(self):
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DtcInfDoorRiReBoolean3", 1)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="1")       
        self.io.set_door(RiRe=Door.close)
        self.soa.get_and_event_check_warning_info_list(name = "Door Reminder Due To Large Slope", info="0") 

    @allure.title("MSO-SREQ-20026 关门提示手动关门_主驾门开&&车门无故障触发防夹_关门提示LockWarning=12")
    @pytest.mark.full
    def test_caseid_1986953(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 9)
        self.soa.hmi_get_door_postion(doors=DoorPos.Dirver, door_pos=DoorPos.Dirver, pos=9)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        time.sleep(3)  # 计时3s
        self.soa.notyfy_lock_warn_info(LockWarn.CloseDoorFail, DoorRemind.NoRequest, timeout=0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 0)

    @allure.title("MSO-SREQ-20026 关门提示手动关门_副驾门关闭&&3s内主驾触发防夹_关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986954(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Pass, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassPercPosn", 5)
        self.soa.hmi_get_door_postion(doors=DoorPos.Pass, door_pos=DoorPos.Pass, pos=5)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Pass, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        time.sleep(1)  # 计时3s
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 1)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=2)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)

    @allure.title("MSO-SREQ-20026 关门提示手动关门主驾门关闭&&3s内左后门触发热保护_关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986955(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 9)
        self.soa.hmi_get_door_postion(doors=DoorPos.Dirver, door_pos=DoorPos.Dirver, pos=9)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean1", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorRearLeft, doorfaultsts=DoorfFultSts.ThermalProtection)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 0)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean1", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("MSO-SREQ-20026 关门提示手动关门_关闭左后门&&3s内主驾触发道路倾斜角异常_关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986956(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeReAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.RearLeft, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DoorLeRePercPosn", 7)
        self.soa.hmi_get_door_postion(doors=DoorPos.RearLeft, door_pos=DoorPos.RearLeft, pos=7)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(lere_opener=DoorPos.RearLeft, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean4", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontLeft, doorfaultsts=DoorfFultSts.RoadInclinationAbnormal)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=1)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean4", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)
        
    @allure.title("MSO-SREQ-20026 关门提示手动关门_右后门关闭&&3s内右前门触发车身横摆角度_关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986957(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiReAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.RearRight, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "RpodBodyFr01", "DoorRiRePercPosn", 7)
        self.soa.hmi_get_door_postion(doors=DoorPos.RearRight, door_pos=DoorPos.RearRight, pos=7)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorRearRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(rire_opener=DoorPos.RearRight, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean3", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontRight, doorfaultsts=DoorfFultSts.RollAngleAbnormal)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=1)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DtcInfDoorPassBoolean3", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK)

    @allure.title("MSO-SREQ-20026 关门提示手动关门_关闭主驾门&&3s主驾门霍尔传感器异常_关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986958(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 9)
        self.soa.hmi_get_door_postion(doors=DoorPos.Dirver, door_pos=DoorPos.Dirver, pos=9)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean5", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorFrontLeft, doorfaultsts=DoorfFultSts.HallSensorsError)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DtcInfDoorDrvrBoolean5", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("MSO-SREQ-20026 关门提示手动关门_关闭副驾门&&3s内左后门防玩激活_关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986968(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Pass, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassPercPosn", 9)
        self.soa.hmi_get_door_postion(doors=DoorPos.Pass, door_pos=DoorPos.Pass, pos=9)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean2", 1)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorRearLeft, doorfaultsts=DoorfFultSts.FaultPlayProtectionActive)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=0)
        self.bus_comm.set_singal("bodycan", "LpodBodyFr01", "DtcInfDoorLeReBoolean2", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)

    @allure.title("MSO-SREQ-20026 关门提示手动关门_关闭副驾门&&3s内车门全关_关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986970(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Pass, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "PpodBodyFr01", "DoorPassPercPosn", 9)
        self.soa.hmi_get_door_postion(doors=DoorPos.Pass, door_pos=DoorPos.Pass, pos=9)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontRight, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(pass_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        self.mix.set_open_close_door_precondition(DoorPos.All, DoorStatus.kClosed)
        sleep(2)
        self.soa.get_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=1)

    @allure.title("MSO-SREQ-20026 关门提示手动关门_主驾门开&&尾门触发防夹_关门提示LockWarning=12")
    @pytest.mark.full
    def test_caseid_1986971(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 9)
        self.soa.hmi_get_door_postion(doors=DoorPos.Dirver, door_pos=DoorPos.Dirver, pos=9)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 1)
        time.sleep(3)  # 计时3s
        self.soa.notyfy_lock_warn_info(LockWarn.CloseDoorFail, DoorRemind.NoRequest, timeout=0)
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 0)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrAntiPnch", 0)
        self.soa.get_and_check_envent_door_fault_sts(checkinterfacetype=CheckInterfaceType.CheckNotify, doorid=DoorId.kDoorAll, doorfaultsts=DoorfFultSts.OK, time_wait=5)
    
    @allure.title("MSO-SREQ-20026 关门提示手动关门_主驾门开&&主驾车门位置>10_无关门提示LockWarning=0")
    @pytest.mark.full
    def test_caseid_1986972(self):
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts.EngSt1_RunngRemStrtd)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrAntiPnch", 0)
        self.mix.set_open_close_door_precondition(DoorPos.Dirver, DoorStatus.kOpened)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 11)
        self.soa.hmi_get_door_postion(doors=DoorPos.Dirver, door_pos=DoorPos.Dirver, pos=11)
        self.soa.hmi_set_door_opener_sts(door_pos=DoorId.kDoorFrontLeft, sts=DoorOpenSts.Close)
        self.bus_comm.check_door_opener_req_and_trigsrc(drv_opener=DoorPos.Dirver, door_req= DoorOpenerReq.Close, door_trigsrc=DoorTrigerSource.HMI)
        time.sleep(2)  # 计时3s
        self.soa.notyfy_lock_warn_info(LockWarn.Idle, DoorRemind.NoRequest, timeout=1)
        self.bus_comm.set_singal("bodycan", "DpodBodyFr01", "DoorDrvrPercPosn", 0)