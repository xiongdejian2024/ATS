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
        self.soa.update(["ClimateControlService_client","CentralLockService_client","TailWingService_client","SteerWheelService_client","TyreService_client","ChargeLidService_client","OuterRearViewService_client","ShieldWindowService_client","VehicleModeService_client","VehicleSetStatusService_client","HighVoltageService_client"])
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

    
    def handle_ble_msg_veh_body(self,ble_date,func_module:Union[DoorId,WindowId,DCChrgnHndlSts,ViewId,str]):
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
            elif isinstance(func_module,ViewId):
                for get_info in get_data.outerRearView:
                        if get_info.id == func_module.value:
                            info = get_info
            elif func_module == "CentralLock":
                info = get_data.centralLock
            elif func_module == "TailGateSts":
                info = get_data.tailGate.status
            elif func_module == "TailGatePos":
                info = get_data.tailGate.position
            elif func_module == "TailWingPos":
                info = get_data.tailWing.position
            elif func_module == "TailWingMode":
                info = get_data.tailWing.wingMode
            elif func_module == "TailWingStatus":
                info = get_data.tailWing.status
            elif func_module == "BonnetStatus":
                info = get_data.bonnet.status
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
            logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
            return info


    @pytest.mark.smoke
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112125')
    def test_caseid_112125(self):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorOpenerDrvrSts",5)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",0)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",0)
        sleep(2)
        for angle in range(15, -1, -5):
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",angle)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontLeft)
                if get_data.curAngle == angle:
                    assert get_data.curAngle == angle
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontLeft)
            assert get_data.curAngle == angle
            # sleep(1)

    
    @pytest.mark.full
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112121')
    def test_caseid_112121(self): 
        for value in [10, 20, 26, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.Wins,sub_func=WindowId.kWindowFrontLeft,value=value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=WindowId.kWindowFrontLeft)
            assert get_data.position == 4*(value - 1)
            # sleep(1)

    @pytest.mark.smoke
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112124')
    def test_caseid_112124(self):
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPosn",0)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorOpenerPassSts",5)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPercPosn",0)
        sleep(2)
        for angle in range(15, -1, -5):
            self.bus_comm.clear_block_bytes()
            # self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.Doors,sub_func=DoorId.kDoorFrontRight,value=angle)
            self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPosn",angle)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontRight)
            assert get_data.curAngle == angle
            # sleep(1)

    
    @pytest.mark.smoke
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112123')
    def test_caseid_112123(self):
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePercPosn",0)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorOpenerLeReSts",5)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePosn",0)
        sleep(1)
        for angle in range(15, -1, -5):
            # self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.Doors,sub_func=DoorId.kDoorRearLeft,value=angle)
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePosn",angle)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody,timeout=8)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearLeft)
                if get_data.curAngle == angle:
                    assert get_data.curAngle == angle
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearLeft)
            assert get_data.curAngle == angle
            # sleep(1)

    
    @pytest.mark.smoke
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112122')
    def test_caseid_112122(self): 
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePercPosn",0)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorOpenerRiReSts",5)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePosn",0)
        sleep(1)
        for angle in range(15, -1, -5):
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePosn",angle)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearRight)
                if get_data.curAngle == angle:
                    assert get_data.curAngle == angle
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearRight)
            assert get_data.curAngle == angle
            # sleep(1)



    @pytest.mark.full
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112121')
    def test_caseid_112121(self): 
        for value in [10, 20, 26, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.Wins,sub_func=WindowId.kWindowFrontLeft,value=value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=WindowId.kWindowFrontLeft)
            assert get_data.position == 4*(value - 1)
            # sleep(1)

    @pytest.mark.full
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112120')
    def test_caseid_112120(self): 
        for value in [10, 20, 26, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.Wins,sub_func=WindowId.kWindowFrontRight,value=value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=WindowId.kWindowFrontRight)
            assert get_data.position == 4*(value - 1)
            # sleep(1)

    @pytest.mark.full
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112119')
    def test_caseid_112119(self): 
        for value in [10, 20, 26, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.Wins,sub_func=WindowId.kWindowRearLeft,value=value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=WindowId.kWindowRearLeft)
            assert get_data.position == 4*(value - 1)
            # sleep(1)

    @pytest.mark.full
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 112118')
    def test_caseid_112118(self): 
        for value in [10, 20, 26, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.Wins,sub_func=WindowId.kWindowRearRight,value=value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=WindowId.kWindowRearRight)
            assert get_data.position == 4*(value - 1)
            # sleep(1)


    @pytest.mark.smoke
    @allure.testcase( 'https://jama.jiduauto.com/perspective.req#/testCases/1350997?projectId=46',name='RVS Case 112081')
    def test_tailgate_status_caseid_112081(self):
        self.bus_comm.set_singal("bodycan","PotBodyFr02", 'TrOpenerSts', 5)
        sleep(2)
        tailgate_status = {
            "2":1,
            "3":2,
            "4":4,
            "1":6,
            "7":3,
            "0":5,
            "6":7,
        }
        for value in tailgate_status:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.TailGate,sub_func=None,value=tailgate_status[value])
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="TailGateSts")
                if get_data == int(value):
                    assert get_data == int(value)
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="TailGateSts")
            assert get_data == int(value)
            # sleep(1)

    @pytest.mark.smoke
    def test_central_lock_status_caseid_112127(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.status ==  1
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.status ==  3



    @pytest.mark.sanity
    def test_Drvrdoor_status_caseid_1989083(self):
        Drvrdoor_status = {
            DoorOpenerSts.MovgOut:5,
            DoorOpenerSts.FullClsd:2,
            DoorOpenerSts.FullOpend:0,
            DoorOpenerSts.HalfClsd:10,
            DoorOpenerSts.MovgInBrkg:8,
            DoorOpenerSts.MovgOutBrkg:9,
            DoorOpenerSts.StopDurgCls:6,
            DoorOpenerSts.Ukwn:7,
            DoorOpenerSts.MovgIn:1,
            DoorOpenerSts.StopDurgOpen:6,
        }
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorOpenerDrvrSts",1)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",0)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",0)
        for key in Drvrdoor_status:
            self.bus_comm.clear_block_bytes()
            logger.info(f'Drvrdoor_status[key].value  :{key.value}')
            self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorOpenerDrvrSts",value=key.value)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontLeft)
                if get_data.status == Drvrdoor_status[key]:
                    assert get_data.status == Drvrdoor_status[key]
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontLeft)
            assert get_data.status == Drvrdoor_status[key]


    @pytest.mark.sanity
    def test_Passdoor_status_caseid_1989082(self):
        Passdoor_status = {
            DoorOpenerSts.MovgOut:5,
            DoorOpenerSts.FullClsd:2,
            DoorOpenerSts.FullOpend:0,
            DoorOpenerSts.HalfClsd:10,
            DoorOpenerSts.MovgInBrkg:8,
            DoorOpenerSts.MovgOutBrkg:9,
            DoorOpenerSts.StopDurgCls:6,
            DoorOpenerSts.Ukwn:7,
            DoorOpenerSts.MovgIn:1,
            DoorOpenerSts.StopDurgOpen:6,
        }
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPosn",0)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPercPosn",0)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorOpenerPassSts",1)
        for key in Passdoor_status:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorOpenerPassSts",value=key.value)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontRight)
                if get_data.status == Passdoor_status[key]:
                    assert get_data.status == Passdoor_status[key]
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontRight)
            assert get_data.status == Passdoor_status[key]

    @pytest.mark.sanity
    def test_LeRedoor_status_caseid_1989081(self):
        LeRedoor_status = {
            DoorOpenerSts.MovgOut:5,
            DoorOpenerSts.FullClsd:2,
            DoorOpenerSts.FullOpend:0,
            DoorOpenerSts.HalfClsd:10,
            DoorOpenerSts.MovgInBrkg:8,
            DoorOpenerSts.MovgOutBrkg:9,
            DoorOpenerSts.StopDurgCls:6,
            DoorOpenerSts.Ukwn:7,
            DoorOpenerSts.MovgIn:1,
            DoorOpenerSts.StopDurgOpen:6,
        }
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePosn",0)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePercPosn",0)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorOpenerLeReSts",1)
        sleep(1)
        for key in LeRedoor_status:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorOpenerLeReSts",value=key.value)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearLeft)
                if get_data.status == LeRedoor_status[key]:
                    assert get_data.status == LeRedoor_status[key]
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearLeft)
            assert get_data.status == LeRedoor_status[key]

    @pytest.mark.sanity
    def test_RiRedoor_status_caseid_1989080(self):
        RiRedoor_status = {
            DoorOpenerSts.MovgOut:5,
            DoorOpenerSts.FullClsd:2,
            DoorOpenerSts.FullOpend:0,
            DoorOpenerSts.HalfClsd:10,
            DoorOpenerSts.MovgInBrkg:8,
            DoorOpenerSts.MovgOutBrkg:9,
            DoorOpenerSts.StopDurgCls:6,
            DoorOpenerSts.Ukwn:7,
            DoorOpenerSts.MovgIn:1,
            DoorOpenerSts.StopDurgOpen:6,
        }
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePosn",0)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePercPosn",0)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorOpenerRiReSts",1)
        for key in RiRedoor_status:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorOpenerRiReSts",value=key.value)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
                get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearRight)
                if get_data.status == RiRedoor_status[key]:
                    assert get_data.status == RiRedoor_status[key]
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody,timeout=7)
            # logger.info(f'ble_bytes:{ble_bytes}')
            # get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearRight)
            assert get_data.status == RiRedoor_status[key]


    @pytest.mark.sanity
    def test_Drvrdoor_position_caseid_1989079(self):
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorOpenerDrvrSts",1)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPosn",0)
        self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",0)
        sleep(5)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","DpodBodyFr01","DoorDrvrPercPosn",signal_value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontLeft)
            assert get_data.position == signal_value

    @pytest.mark.sanity
    def test_Passdoor_position_caseid_1989084(self):
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPosn",0)
        self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPercPosn",0)
        sleep(2)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","PpodBodyFr01","DoorPassPercPosn",signal_value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorFrontRight)
            assert get_data.position == signal_value


    @pytest.mark.sanity
    def test_LeRedoor_position_caseid_1989085(self):
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePosn",0)
        self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePercPosn",0)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","LpodBodyFr01","DoorLeRePercPosn",signal_value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearLeft)
            assert get_data.position == signal_value


    @pytest.mark.sanity
    def test_RiRedoor_position_caseid_1989086(self):
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePosn",0)
        self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePercPosn",0)
        for signal_value in [26, 20, 10, 1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","RpodBodyFr01","DoorRiRePercPosn",signal_value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=DoorId.kDoorRearRight)
            assert get_data.position == signal_value


    @pytest.mark.sanity
    def test_tailgate_position_caseid_112082(self):
        self.bus_comm.set_singal("bodycan","PotBodyFr03","TrOpenPosn",20)
        for signal_value in [99, 50, 30, 10]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("bodycan","PotBodyFr03","TrOpenPosn",signal_value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="TailGatePos")
            assert get_data ==  signal_value


    @pytest.mark.sanity
    def test_drive_mirrorfolder_caseid_112100(self):
        drive_mirrorfolder={
        "3":ViewFoldStatus.StatusUnfolding,
        "1":ViewFoldStatus.StatusUnfolded,
        "4":ViewFoldStatus.StatusFolding,
        "2":ViewFoldStatus.StatusFolded,
        }
        # self.bus_comm.set_singal("bodycan","DdmBodyFr01","MirrFoldStsAtDrvr",2)
        sleep(1)
        for key in drive_mirrorfolder:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_rear_view_mode(pos=ViewPos.RearLeft,mode=drive_mirrorfolder[key])
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=ViewId.RearViewLeft)
            assert get_data.foldStatus == drive_mirrorfolder[key].value
            


    @pytest.mark.full
    def test_pass_mirrorfolder_caseid_1989100(self):
        pass_mirrorfolder={
        "3":ViewFoldStatus.StatusUnfolding,
        "1":ViewFoldStatus.StatusUnfolded,
        "4":ViewFoldStatus.StatusFolding,
        "2":ViewFoldStatus.StatusFolded,
        }
        sleep(1)
        for key in pass_mirrorfolder:
            self.bus_comm.set_rear_view_mode(pos=ViewPos.RearRight,mode=pass_mirrorfolder[key])
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            logger.info(f'ble_bytes:{ble_bytes}')
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=ViewId.RearViewRight)
            assert get_data.foldStatus == pass_mirrorfolder[key].value



    @pytest.mark.sanity
    def test_tailwing_pos_caseid_112098(self):
        self.bus_comm.set_singal("cem_lin6","AwmCem_Lin6Fr01", 'ActvReSplrPosn', 3)
        sleep(2)
        tailwing_pos ={
           "0":1,
           "1":2,
           "2":3,
           "3":4,
           "5":0,
        }
        for value in tailwing_pos:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_veh_body(func_module=BleVehicleBody.TailWing,sub_func=None,value=tailwing_pos[value])
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody,timeout=10)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="TailWingPos")
            assert get_data == int(value)

    @pytest.mark.full
    def test_tailwing_mode_caseid_112099(self):
        self.sd_tester.write_single_ccp(564, 2)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_car_mode(CarMode.NORMAL)
        tailwing_mode = {
            "TwmTailWingModeOff":TailWindMode.Off,
            "TwmTailWingModeOn":TailWindMode.On,
            "TwmTailWingModeAuto":TailWindMode.Auto,
        }
        sleep(1)
        for key in tailwing_mode:
            self.bus_comm.clear_block_bytes()
            self.soa.hmi_set_tailwing_mode(mode=tailwing_mode[key])
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="TailWingMode")
            assert get_data == tailwing_mode[key].value

    @pytest.mark.full
    def test_tailwing_status_caseid_112084(self):
        tailwing_status ={
           "1" :TailWingPos.Shifting,
           "0" :TailWingPos.Ukwn,  
        }
        self.bus_comm.set_tailwing_pos(pos=TailWingPos.P1)
        sleep(2)
        for key in tailwing_status:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_tailwing_pos(pos=tailwing_status[key])
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
            logger.info(f'ble_bytes:{ble_bytes}')
            get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="TailWingStatus")
            # assert get_data == tailwing_status[key].value
            assert get_data == int(key)


    @pytest.mark.sanity
    def test_HoodStatus_caseid_112126(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.io.set_hood_sts(HoodSts.Close)
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.io.set_hood_sts(HoodSts.Open)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody,timeout=8)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="BonnetStatus")
        assert get_data == 0
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.io.set_hood_sts(HoodSts.Open)
        sleep(1)
        self.io.set_hood_sts(HoodSts.Close)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody,timeout=8)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="BonnetStatus")
        assert get_data == 1

    

    @pytest.mark.sanity
    def test_central_lock_status_caseid_1990903(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.status ==  1
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.status ==  3


    @pytest.mark.full
    def test_central_lock_TriggerSourceId_caseid_1990902(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.triggerSourceId ==  12
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.triggerSourceId ==  7
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.triggerSourceId ==  1
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.triggerSourceId ==  12
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.triggerSourceId ==  3
        sleep(3)
        self.bus_comm.clear_block_bytes()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.KV_PEPS)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
        get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
        assert get_data.triggerSourceId ==  2