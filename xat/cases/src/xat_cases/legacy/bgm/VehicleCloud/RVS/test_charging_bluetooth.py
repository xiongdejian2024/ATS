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

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.legacy.tsp.proto_parse import ProtoParse
from xat_ecu.api.abc_interface import *
from google.protobuf.json_format import MessageToJson
running_flag = True

@allure.feature("BGM车云")
@allure.story("蓝牙数据上报")
# @pytest.mark.flaky(reruns=1, reruns_delay=1)
@pytest.mark.order_last
class TestBle(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["ClimateControlService_client","CentralLockService_client","TailWingService_client","SteerWheelService_client","TyreService_client","ChargeLidService_client","OuterRearViewService_client","ShieldWindowService_client","VehicleModeService_client","VehicleSetStatusService_client","LightService_client","HighVoltageService_client"])
        running_flag = True
        self.rev_msg_list = []
        self.protoparse = ProtoParse()
        # self.bus_comm.blue_data_preheat_start()
        self.bus_comm.start_dk()
        sleep(1)
        self.bus_comm.set_door_open_angle_sts(door_pos=DoorId.kDoorAll,angle=1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
        self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Init,DispHvBattLvlOfChrg=0)
        self.bus_comm.set_bluetooth_key_connect_sts(key_num=1,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        self.bus_comm.get_ble_bytes_thread_start()
        sleep(3)

    def before_each_func(self, ecu):
        pass
        #self.bus_comm.set_blue_id_type_sts(key_id=66,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        #self.bus_comm.set_bluetooth_key_connect_sts(key_num=1,connect_sts=ConnSts.Connect,key_type=BlueType.BLE_Key)

    def after_each_func(self, ecu):
        self.bus_comm.clear_all_bus_buffer()
        sleep(1)

    def after_class(self, ecu):
        # pass
        self.bus_comm.get_ble_bytes_thread_stop()
        # self.bus_comm.blue_data_preheat_stop()


    def get_ble_bytes(self, msg_list, blockid:BlockName):
        ble_bytes = None
        if msg_list == None:
            logger.info(f"获取的总线报文为空,没有触发响应的蓝牙数据")
            assert False
        else:
            for msg in msg_list:
                logger.info(f'msg_block_id:{self.protoparse.get_vehicle_mode(bytes(msg)).head.blockID}')
                if self.protoparse.get_vehicle_mode(bytes(msg)).head.blockID == blockid.value:
                    ble_bytes = bytes(msg)
            return ble_bytes

    def handle_ble_msg_BLEEicCharging(self,ble_date,func_module:str):
        prompt_info = f"---------->解析接收的蓝牙充电三电信息块(BLEEicChargingBlock)总线数据"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            get_data = self.protoparse.get_bleeiccharging_info(ble_date)
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            logger.info(f"---------->解析之后的BLEEicChargingBlock具体信息:")
            if func_module == "ChargeTargetSoc":
                info = get_data.chargeTargetSoc
            if func_module == "PluggerStatus":
                info = get_data.pluggerStatus
            if func_module == "IsConnect":
                info = get_data.isConnect
            if func_module == "ChargingLidPos":
                info = get_data.chargingLidPos
            if func_module == "RemainChargingTime":
                info = get_data.remainChargingTime
                 
            logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
            return info
        


    @pytest.mark.sanity
    @pytest.mark.v220
    def test_charg_targetsoc_caseid_1995681(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",0)
        sleep(1)
        for signal_value in [50,0,100,110,800,1000]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",signal_value)
            start_time = time.time()
            while time.time() - start_time < 12:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
                get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="ChargeTargetSoc")
                if get_data == signal_value*0.1:
                    assert get_data == signal_value*0.1
                    break
                sleep(0.5)
            assert get_data == signal_value*0.1 
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",0)



    @pytest.mark.smoke
    @pytest.mark.v220
    def test_isConnect_caseid_1995679(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="IsConnect")
            if get_data == True:
                assert get_data == True
                break
            sleep(0.5)
        assert get_data == True
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="IsConnect")
            if get_data == False:
                assert get_data == False
                break
            sleep(0.5)
        assert get_data == False



    @pytest.mark.sanity
    @pytest.mark.v220
    def test_chrglid_pos_caseid_1995680(self):
        self.bus_comm.set_chrglid_pos(0)
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(100)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="ChargingLidPos")
            if get_data == 100:
                assert get_data == 100
                break
            sleep(0.5)
        assert get_data == 100
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="ChargingLidPos")
            if get_data == 0:
                assert get_data == 0
                break
            sleep(0.5)
        assert get_data == 0


    
    @pytest.mark.sanity
    @pytest.mark.v220
    def test_charggun_caseid_1995678(self):
        self.sd_tester.write_multi_ccp({973:2})
        sleep(2)
        self.io.bgm_power_off()
        sleep(1)
        self.io.bgm_power_on()
        sleep(15)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        sleep(1)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 0:
                assert get_data == 0
                break
            sleep(0.5)
        assert get_data == 0         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 1:
                assert get_data == 1
                break
            sleep(0.5)
        assert get_data == 1        
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',2)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 2:
                assert get_data == 2
                break
            sleep(0.5)
        assert get_data == 2         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',3)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 3:
                assert get_data == 3
                break
            sleep(0.5)
        assert get_data == 3         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',4)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 4:
                assert get_data == 4
                break
            sleep(0.5)
        assert get_data == 4         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',5)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 5:
                assert get_data == 5
                break
            sleep(0.5)
        assert get_data == 5
        sleep(1)      
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',10)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 7:
                assert get_data == 7
                break
            sleep(0.5)
        assert get_data == 7        
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',4)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 8:
                assert get_data == 8
                break
            sleep(0.5)
        assert get_data == 8  
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',5)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 9:
                assert get_data == 9
                break
            sleep(0.5)
        assert get_data == 9  
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',6)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 10:
                assert get_data == 10
                break
            sleep(0.5)
        assert get_data == 10  
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',7)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
            get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="PluggerStatus")
            if get_data == 11:
                assert get_data == 11
                break
            sleep(0.5)
        assert get_data == 11 
        sleep(1)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)



    # @pytest.mark.sanity
    # def test_remainChargingTime_caseid_501501(self):
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr21","HvBattChrgnTiEstimd",0)
    #     sleep(1)
    #     for signal_value in [60,50]:
    #         self.bus_comm.clear_block_bytes()
    #         self.bus_comm.set_singal("propulsioncan","BecmPropFr21","HvBattChrgnTiEstimd",signal_value)
    #         ble_bytes = self.bus_comm.get_block_bytes(BlockName.BLEEicCharging)
    #         get_data = self.handle_ble_msg_BLEEicCharging(ble_date=bytes(ble_bytes),func_module="RemainChargingTime")
    #         assert get_data == signal_value