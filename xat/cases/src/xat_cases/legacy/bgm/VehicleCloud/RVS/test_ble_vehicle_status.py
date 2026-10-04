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
        self.soa.update(["CentralLockService_client","VehicleModeService_client","VehicleSetStatusService_client","KeyService_client","RemoteCtrlService_client"])
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

    
    def handle_ble_msg_veh_body(self,ble_date,func_module:Union[DoorId,WindowId,DCChrgnHndlSts,str]):
        prompt_info = f"---------->解析接收的车身状态(VehicleBodyBlock)总线数据"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            get_data = self.protoparse.get_vehicle_body_info(ble_date)
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            if isinstance(func_module,DoorId):
                for get_info in get_data.doors:
                        if get_info.id == func_module.value:
                            info = get_info
            elif isinstance(func_module,WindowId):
                for get_info in get_data.windows:
                        if get_info.id == func_module.value:
                            info = get_info
            elif func_module == "CentralLock":
                info = get_data.centralLock
            elif func_module == "TailGateSts":
                info = get_data.tailGate.status
            elif func_module == "TailGatePos":
                info = get_data.tailGate.position
            logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
            return info

    def handle_ble_msg_eic_charge(self,ble_date,func_module:BleEicCharg):
        prompt_info = f"---------->解析接收的充电三电信息块(EicChargingBlock)总线数据"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            get_data = self.protoparse.get_charging_info(ble_date)
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            logger.info(f"---------->解析之后的EicChargingBlock具体信息:")
            if func_module.name == "Charging":
                info = get_data.charging     
                
            logger.info(f"---------->解析之后的子模块{func_module.name}信息为:{info}")
            return info
    
    def handle_ble_msg_vehicle_mode(self,ble_date,func_module:str):
        prompt_info = f"---------->解析接收的车辆模式信息块(VehicleMode)总线数据"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            get_data = self.protoparse.get_vehicle_mode(ble_date)
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            logger.info(f"---------->解析之后的VehicleMode具体信息:")
            if func_module == "UsageMode":
                info = get_data.usage  
            if func_module == "CarMode":
                info = get_data.model
            logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
            return info

    def handle_ble_msg_BusStatus(self,ble_date,func_module:str):
        prompt_info = f"---------->解析接收的车辆状态信息块(BusStatus)总线数据"
        with allure.step(prompt_info):
            logger.info(prompt_info)
            get_data = self.protoparse.get_function_info(ble_date)
            get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
            logger.info(f'get_data_dict: {get_data_dict}')
            logger.info(f"---------->解析之后的BusStatus具体信息:")
            if func_module == "account":
                info = get_data.account
            if func_module == "huntStatus":
                info = get_data.huntStatus
            if func_module == "RemoteAuthInfo":
                info = get_data.remoteAuthInfo
            logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
            return info


    
    @pytest.mark.sanity
    def test_findvehicle_caseid_112088(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.clear_block_bytes()
        self.soa.send_method_request("KeyService_client", 'SetCarLocalTraceRequest', {"carLoctrReq": 1})
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
        get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="huntStatus")
        assert get_data == 1


    
    @allure.title("通知/获取远程授权启动状态Default_Entry_Default")
    @pytest.mark.sanity
    def test_caseid_1988402_1988401_1988395(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",0)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",0)
        self.io.set_five_door_sts(sts=Door.close)
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.tsp.rvc_remote_authorization()
        self.io.set_five_door_sts(sts=Door.open)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
            get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="RemoteAuthInfo")
            if get_data.remoteAuthSts == 4:
                assert get_data.remoteAuthSts == 4
                break
            sleep(0.5)
        assert get_data.remoteAuthSts == 4
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.io.set_five_door_sts(sts=Door.close)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        # self.io.set_five_door_sts(sts=Door.close)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
            get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="RemoteAuthInfo")
            if get_data.remoteAuthSts == 0:
                assert get_data.remoteAuthSts == 0
                break
            sleep(0.5)
        assert get_data.remoteAuthSts == 0




    @allure.title("通知/获取远程授权启动状态_Default_ReadyEntry_Default")
    @pytest.mark.full
    def test_caseid_1988398_1988397(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.set_five_door_sts(sts=Door.open)
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.io.set_five_door_sts(sts=Door.close)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.tsp.rvc_remote_authorization()
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
            get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="RemoteAuthInfo")
            if get_data.remoteAuthSts == 3:
                assert get_data.remoteAuthSts == 3
                break
            sleep(0.5)
        assert get_data.remoteAuthSts == 3  
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
            get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="RemoteAuthInfo")
            if get_data.remoteAuthSts == 0:
                assert get_data.remoteAuthSts == 0
                break
            sleep(0.5)
        assert get_data.remoteAuthSts == 0




    @allure.title("通知/获取远程授权启动状态_ReadyEntry进Entry")
    @pytest.mark.full
    def test_caseid_1988396(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.set_five_door_sts(sts=Door.open)
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.io.set_five_door_sts(sts=Door.close)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.tsp.rvc_remote_authorization()
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
            get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="RemoteAuthInfo")
            if get_data.remoteAuthSts == 3:
                assert get_data.remoteAuthSts == 3
                break
            sleep(0.5)
        assert get_data.remoteAuthSts == 3 
        sleep(10)
        self.bus_comm.clear_block_bytes()
        self.io.set_five_door_sts(sts=Door.open)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
            get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="RemoteAuthInfo")
            if get_data.remoteAuthSts == 4:
                assert get_data.remoteAuthSts == 4
                break
            sleep(0.5)
        assert get_data.remoteAuthSts == 4
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        self.io.set_five_door_sts(sts=Door.close)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.BusStatus)
            get_data = self.handle_ble_msg_BusStatus(ble_date=bytes(ble_bytes),func_module="RemoteAuthInfo")
            if get_data.remoteAuthSts == 0:
                assert get_data.remoteAuthSts == 0
                break
            sleep(0.5)
        assert get_data.remoteAuthSts == 0