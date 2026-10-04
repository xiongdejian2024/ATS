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
        self.soa.update(["CentralLockService_client","VehicleModeService_client","VehicleSetStatusService_client"])
        sleep(3)
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.sd_tester.write_ccp(ccp={566: 25})
        self.bus_comm.set_dtc_pre()
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
        self.bus_comm.set_charging_sts(ChargingSts.Default)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_dcdc_battary_act_sts_on_can(DcDcActvd=DcDcActvd.ConversionToLVSide)
        self.bus_comm.set_dispbattegyout(DispBattEgyOut=40.0)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        pass
        # sleep(2)

    def after_each_func(self, ecu):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.io.set_five_door_sts(sts=Door.close)
        self.io.driver_seat_notpresent()
        self.bus_comm.set_secle_seat_notpresent()
        self.bus_comm.set_pass_seat_notpresent()
        self.io.hazard_light_close()
        self.io.bgm_diag_line_up()
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
    
    
    def set_pre_condition_for_keep_power(self):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.bus_comm.set_singal(bus="backbonefr", msg="VddmBackBoneFr18", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
        time.sleep(1)
        self.bus_comm.set_dtc_pre()
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Disconnected, DispHvBattLvlOfChrg=80.0)
        self.bus_comm.set_singal(bus="propulsioncan", msg="EcmPropComFr10", signal="TrsmParkLockdTrsmParkLockd", value=1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
        self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
        sleep(1)


    # @pytest.mark.sanity
    # def test_10102_carmode_caseid_1918797(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
    #     sleep(1)
    #     model = {
    #         "VehicleModeCrash": CarMode.CRASH,
    #         "VehicleModeDyno": CarMode.DYNO,
    #         # "VehicleModeFactory": CarMode.FACTORY,
    #         "VehicleModeTransport": CarMode.TRANSPORT,
    #         "VehicleModeNormal": CarMode.NORMAL,
    #     }

    #     for key in model:
    #         begin_time = time.time()
    #         # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
    #         # sleep(1)
    #         # self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.Telm)
    #         self.mix.set_common_precontion(car_mode=model[key])
    #         self.tsp.check_rvs_data_update_new(
    #             block=BlockName.VehicleMode, keys=["model"], target_value= getattr(VehicleStatusRvs, key).value,timeout=10,begin_time=begin_time,sleep_time=11
    #         )
    @pytest.mark.sanity
    def test_10102_carmode_caseid_1918797(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.CRASH)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode, keys=["model"], target_value=3,timeout=10)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode, keys=["model"], target_value=5,timeout=10)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode, keys=["model"], target_value=2,timeout=10)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.TRANSPORT)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode, keys=["model"], target_value=1,timeout=10)
        sleep(1)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode, keys=["model"], target_value=0,timeout=10)





    @pytest.mark.sanity
    def test_10102_usagemode_caseid_1918800(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(1)
        model = {
            "UsageModeDriving": UsageMode.DRIVING,
            "UsageModeActive": UsageMode.ACTIVE,
            "UsageModeConvenience": UsageMode.CONVENIENCE,
            "UsageModeInactive": UsageMode.INACTIVE,
            "UsageModeAbandoned": UsageMode.ABANDONED,
        }

        for key in model:
            begin_time = time.time()
            self.mix.set_common_precontion(usage_mode=model[key])
            self.tsp.check_rvs_data_update_new(
                block=BlockName.VehicleMode, keys=["usage"], target_value= getattr(UsageModeRvs, key).value,timeout=10,begin_time=begin_time
            )
        

    
    @pytest.mark.sanity
    def test_caseid_1983509(self):
        '''维持上电模式进入 '''
        self.set_pre_condition_for_keep_power()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        begin_time = time.time()
        self.tsp.check_rvs_data_update_new(
        block=BlockName.VehicleMode,keys=["parkingComfortMode","status"],target_value=1,begin_time=begin_time)


    @pytest.mark.sanity
    def test_caseid_1983508(self):
        '''维持上电模式退出_用户关闭 '''
        self.set_pre_condition_for_keep_power()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        begin_time = time.time()
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","status"],target_value=0,begin_time=begin_time)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","offReason"],target_value=1,begin_time=begin_time)



    @pytest.mark.sanity
    def test_caseid_1983507(self):
        '''维持上电模式退出_电量低 '''
        self.set_pre_condition_for_keep_power()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        begin_time = time.time()
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","status"],target_value=0,begin_time=begin_time)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","offReason"],target_value=2,begin_time=begin_time)


    @pytest.mark.sanity
    def test_caseid_1983506_1983505_1983504(self):
        '''维持上电模式退出_挡位不满足 '''
        self.set_pre_condition_for_keep_power()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_gear)
        begin_time = time.time()
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","status"],target_value=0,begin_time=begin_time)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","offReason"],target_value=3,begin_time=begin_time)



    @pytest.mark.sanity
    def test_caseid_1983503_1983502_1983501_1983500(self):
        '''维持上电模式退出_carmode不满足 '''
        self.set_pre_condition_for_keep_power()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_carmode)        
        begin_time = time.time()
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","status"],target_value=0,begin_time=begin_time)
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["parkingComfortMode","offReason"],target_value=4,begin_time=begin_time)


    @pytest.mark.sanity
    @pytest.mark.v210
    def test_washMode_caseid_1990896(self):
        '''洗车模式 '''
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
        sleep(1)
        self.soa.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": True})
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["washModeSts"],target_value=True)
        sleep(1)
        self.soa.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
        self.tsp.check_rvs_data_update_new(block=BlockName.VehicleMode,keys=["washModeSts"],target_value=False)