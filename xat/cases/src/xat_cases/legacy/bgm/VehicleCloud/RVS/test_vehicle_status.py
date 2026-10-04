#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_rvs.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/12/1 11:30
@Description: BGM RVS功能测试
"""

import os
import sys
import pytest
import allure
from time import sleep
import threading
import math

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.tsp.rvs_client import RvsClient
from signal_value_mapping import *

@allure.feature("BGM车云")
@allure.story("基础数据上报")
@pytest.mark.order_last
class TestRVS(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","VehicleModeService_client","VehicleSetStatusService_client","KeyService_client","RemoteCtrlService_client"])
        sleep(3)
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        self.io.start_io()
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.sd_tester.write_ccp({225: 7, 226: 7}) 
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    # def auto_no_accredit(self, accredit):
    #     """
    #     0=满足自动授权, 1=不满足自动授权，不满足取消自动授权, 2=取消自动授权
    #     """
    #     if accredit == 0:  
    #         # self.io.io.init_bgm_HW()
    #         self.io.set_five_door_sts(sts=Door.open)
    #         self.io.driver_seat_present()
    #         self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 1)
    #     elif accredit == 1:
    #         # self.io.io.init_bgm_HW() 
    #         self.io.set_five_door_sts(sts=Door.close)
    #         self.io.driver_seat_present()
    #         self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 0)
    #         self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
    #     elif accredit ==2:
    #         self.io.set_five_door_sts(sts=Door.close)
    #         self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00", 'BrkPedlPsdBrkPedlPsd', 0)
    #         # self.io.io.init_bgm_HW() 
    #         self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     else:
    #         pass  

    
    @pytest.mark.full
    def test_findvehicle_caseid_112346(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.send_method_request("KeyService_client", 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["huntStatus"],target_value=1
        )


    @allure.title("通知/获取远程授权启动状态Default_Entry_Default")
    @pytest.mark.sanity
    def test_caseid_1988389_1988388_1988382(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",0)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",0)
        self.io.set_five_door_sts(sts=Door.close)
        sleep(5)
        self.tsp.rvc_remote_authorization()
        self.io.set_five_door_sts(sts=Door.open)
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=4)
        sleep(5)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        self.io.set_five_door_sts(sts=Door.close)
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=0)




    @allure.title("通知/获取远程授权启动状态_Default_ReadyEntry_Default")
    @pytest.mark.full
    def test_caseid_1988384_1988385(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.set_five_door_sts(sts=Door.open)
        sleep(5)
        self.io.set_five_door_sts(sts=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.tsp.rvc_remote_authorization()
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=3)  
        sleep(5)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=0)




    @allure.title("通知/获取远程授权启动状态_ReadyEntry进Entry")
    @pytest.mark.full
    def test_caseid_1988383(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.set_five_door_sts(sts=Door.open)
        sleep(5)
        self.io.set_five_door_sts(sts=Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.tsp.rvc_remote_authorization()
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=3)  
        sleep(10)
        self.io.set_five_door_sts(sts=Door.open)
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=4)
        sleep(5)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        self.io.set_five_door_sts(sts=Door.close)
        self.tsp.check_rvs_data_update_new(
           block=BlockName.BusStatus,keys=["remoteAuthInfo","remoteAuthSts"],target_value=0)