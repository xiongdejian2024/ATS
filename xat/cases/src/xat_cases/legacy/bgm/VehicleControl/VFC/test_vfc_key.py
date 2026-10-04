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
from groot2.cloud.biz.digital_key.manager import DigitalKeyManager


@allure.feature("车控车设")
@allure.story("VFC")
class TestHVAlarmCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_client","CentralLockService_client","SteerWheelService_client",
                         "LightService_client",'ClimateControlService_client',"VehicleModeService_client",
                         "WiperService_client","ChargeLidService_client","TailWingService_client",
                         "KeyService_client","WindowAppService_client","GloveBoxService_client",
                         "OuterRearViewService_client","DoorService_client"])
        
        self.tsp = DigitalKeyManager(self.tc_config.get('vid'),
                                     self.tc_config.get('tel'),
                                     "jiduapp/0.9.3 (iOS; 16.0; apple; jdcomiphone; iPhone 12; NULL; BF983636-D3F2-4805-90B4-77C3DC75D433; aVBob25l)")
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
        
    
    @allure.title("车控车设_VFCPNC21_KeyReadReqFromKeyWarn寻钥匙")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC21
    def test_vfc_caseid_1985710(self):
        self.mix.clear_pnc(BGMPNC.PNC21)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, 20.0, 3.0)

    @allure.title("车控车设_VFCPNC21_KeyReadReqFromKeyRmn寻钥匙")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC21
    def test_vfc_caseid_1985709(self):
        self.mix.clear_pnc(BGMPNC.PNC21)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, 20.0, 3.0)

    @allure.title("车控车设_VFCPNC21_KeyDiReq")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC21
    def test_vfc_caseid_1986104(self):
        self.mix.clear_pnc(BGMPNC.PNC21)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, 20.0, 3.0)

    @allure.title("车控车设_VFCPNC21_KeyReadReqFromVMM")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    )
    @pytest.mark.smoke
    @pytest.mark.PNC21
    def test_vfc_caseid_1985735(self):
        self.mix.clear_pnc(BGMPNC.PNC21)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(30)
        self.io.brake_light_close()
        self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, 3.0)
        self.io.brake_light_open()

    # @allure.title("车控车设_VFCPNC21_KeyDiReq钥匙ID变化")
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/1919295?projectId=46"
    # )
    # @pytest.mark.smoke
    # @pytest.mark.PNC21
    # def test_vfc_caseid_1990963(self):
    #     self.mix.clear_pnc(BGMPNC.PNC21)
    #     self.tsp.create_bluetooth_digital_key()
    #     sleep(1)
    #     self.bus_comm.dk.ck_white_list_update_req(sub_id=0x2, keyid_list=[key_id0])
    #     # self.dk.ck_white_list_update_req(2, [key_id0])
    #     self.bus_comm.dk.send_while_list_update_resp(0x12, 0x00, self.bus_comm.dk.last_sync_time_ble)
    #     # self.dk.send_while_list_update_resp(0x12, 0x00, self.dk.last_sync_time_ble)
    #     self.bus_comm.check_pnc_valid_last_time(BusName.connectivitycanfd, NMMsgId.x533, BGMPNC.PNC21, 3.0, 2.0)