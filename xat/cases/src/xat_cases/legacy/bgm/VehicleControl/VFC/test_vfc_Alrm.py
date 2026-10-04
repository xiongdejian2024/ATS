#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_npc_vfc.py
@Author      : shulin.zheng@jiduauto.com
@Time        : 2023/11/9 11:30
@Description : BGM车控车设VFC
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
@allure.story("VFC")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_client","CentralLockService_client","SteerWheelService_client",
                         "LightService_client",'ClimateControlService_client',"VehicleModeService_client",
                         "WiperService_client","ChargeLidService_client","TailWingService_client",
                         "KeyService_client","WindowAppService_client","GloveBoxService_client",
                         "OuterRearViewService_client","DoorService_client"])
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
        
    @allure.title("车控车设_VFCPNC16_AlrmStsAlrmSt")
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1919350(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC16_AlrmStsAlrmSt")
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1919351(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)

    @allure.title("车控车设_VFCPNC16_AlrmStsAlrmSt")
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1919352(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        self.io.set_door(Drvr=Door.close)
    
    @allure.title("车控车设_VFCPNC16_AlrmStsAlrmSt")
    @pytest.mark.smoke
    @pytest.mark.PNC16
    def test_vfc_caseid_1919353(self):
        self.mix.clear_pnc(BGMPNC.PNC16)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(30)
        self.io.set_door(Drvr=Door.open)
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
        sleep(25)
        self.bus_comm.check_alrm_sts_req(AlrmSts.Armd)
        # self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC16, 3.0, 1.5)
    
   
    

    