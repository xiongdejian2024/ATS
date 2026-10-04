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
        self.soa.update(["CentralLockService_client","VehicleModeService_client","VehicleSetStatusService_client","InteractiveService_server"])
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
        #self.bus_comm.set_blue_id_type_sts(key_id=66,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
        #self.bus_comm.set_bluetooth_key_connect_sts(key_num=1,connect_sts=ConnSts.Connect,key_type=BlueType.BLE_Key)

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
        self.bus_comm.clear_all_bus_buffer()
        sleep(1)

    def after_class(self, ecu):
        # pass
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        self.sd_tester.write_ccp({225: 7, 226: 7}) 
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
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
            if func_module == "ParkingComfortMode":
                info = get_data.parkingComfortMode
            if func_module == "petModeSts":
                info = get_data.petModeSts
            if func_module == "washModeSts":
                info = get_data.washModeSts
            if func_module == "MaintenanceMode":
                info = get_data.maintenanceMode
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

    @pytest.mark.smoke
    def test_10102_usagemode_caseid_112128(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(2)
        usage_mode = [0,1,2,11,13,1]
        for value in usage_mode:
            self.bus_comm.clear_block_bytes()
            self.sd_tester.sd_tester.change_usage_mode(value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            logger.info(f'ble_bytes:{ble_bytes}')
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="UsageMode")
            assert get_data == int(value)
            # sleep(1)
        # self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        # sleep(2)
        # usage_mode = [0,1,2,11,13,1]
        # for value in usage_mode:
        #     self.bus_comm.clear_block_bytes()
        #     self.sd_tester.sd_tester.change_usage_mode(value)
        #     ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
        #     logger.info(f'ble_bytes:{ble_bytes}')
        #     get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="UsageMode")
        #     assert get_data == int(value)
        #     # sleep(1)

    @pytest.mark.sanity
    @pytest.mark.carmode
    def test_10102_carmode_caseid_112129(self):
        self.sd_tester.change_car_mode(car_mode=CarMode.NORMAL)
        sleep(2)
        usage_mode = [1,2,5,0]
        for value in usage_mode:
            self.bus_comm.clear_block_bytes()
            self.sd_tester.sd_tester.change_car_mode(value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            logger.info(f'ble_bytes:{ble_bytes}')
            get_data=self.protoparse.get_vehicle_messages("10102",raw_data=bytes(ble_bytes))
            logger.info(f"---------->解析之后的子模块{CarMode}信息为:{value}")
            assert get_data.model== int(value)


    @pytest.mark.sanity
    def test_caseid_1989470(self):
        '''维持上电模式进入 '''
        self.set_pre_condition_for_keep_power()
        self.sd_tester.change_car_mode(car_mode=CarMode.NORMAL)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        self.bus_comm.clear_block_bytes()
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
        get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
        assert get_data.status == 1


    @pytest.mark.sanity
    def test_caseid_1989469(self):
        '''维持上电模式退出_用户关闭 '''
        self.set_pre_condition_for_keep_power()
        self.sd_tester.change_car_mode(car_mode=CarMode.NORMAL)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        time.sleep(5)
        self.bus_comm.clear_block_bytes()
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
            if get_data.status == 0 and get_data.offReason == 1:
                assert get_data.status == 0
                assert get_data.offReason == 1
                break
            sleep(0.5)
        # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
        # get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
        assert get_data.status == 0
        assert get_data.offReason == 1



    @pytest.mark.sanity
    def test_caseid_1989468(self):
        '''维持上电模式退出_电量低 '''
        self.set_pre_condition_for_keep_power()
        self.sd_tester.change_car_mode(car_mode=CarMode.NORMAL)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_hvsoc)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
            if get_data.status == 0 and get_data.offReason == 2:
                assert get_data.status == 0
                assert get_data.offReason == 2
                break
            sleep(0.5)
        # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
        # get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
        assert get_data.status == 0
        assert get_data.offReason == 2


    @pytest.mark.sanity
    def test_caseid_1989467_1989466_1989465(self):
        '''维持上电模式退出_挡位不满足 '''
        self.set_pre_condition_for_keep_power()
        self.sd_tester.change_car_mode(car_mode=CarMode.NORMAL)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_gear)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
            if get_data.status == 0 and get_data.offReason == 3:
                assert get_data.status == 0
                assert get_data.offReason == 3
                break
            sleep(0.5)
        # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
        # get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
        assert get_data.status == 0
        assert get_data.offReason == 3



    @pytest.mark.sanity
    def test_caseid_1989464_1989463_1989462_1989461(self):
        '''维持上电模式退出_carmode不满足 '''
        self.set_pre_condition_for_keep_power()
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.change_car_mode(car_mode=CarMode.NORMAL)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_service)
        sleep(5)
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.open)
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.mix.set_keep_power_and_check_notify(flag=KeepPowerFlag.close_carmode)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
            if get_data.status == 0 and get_data.offReason == 4:
                assert get_data.status == 0
                assert get_data.offReason == 4
                break
            sleep(0.5)
        # ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
        # get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="ParkingComfortMode")
        assert get_data.status == 0
        assert get_data.offReason == 4



    @pytest.mark.full
    def test_PetmodeSts_caseid_1988849_1988848_1988847_1988846_1988845_1988844(self):
        '''宠物模式 '''
        self.soa.send_event_notify("InteractiveService_server", "PetModeSts", {"sts": 0})
        sleep(1)
        for key in [1,2,1,0]:
            self.bus_comm.clear_block_bytes()
            self.soa.send_event_notify("InteractiveService_server", "PetModeSts", {"sts": key})
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
                get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="petModeSts")
                if get_data == key:
                    assert get_data == key
                    break
                sleep(0.5)
            assert get_data == key



    @pytest.mark.sanity
    @pytest.mark.v210
    def test_washMode_caseid_1990904(self):
        '''洗车模式 '''
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.soa.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": True})
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="washModeSts")
            if get_data == 1:
                assert get_data == 1
                break
            sleep(0.5)
        assert get_data == 1
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.soa.send_method_request("VehicleSetStatusService_client", "SetWashMode", {"isOn": False})
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="washModeSts")
            if get_data == 0:
                assert get_data == 0
                break
            sleep(0.5)
        assert get_data == 0

    
    @allure.title("设置维修模式")
    @pytest.mark.full
    def test_caseid_1990652(self):
        self.soa.send_method_request("VehicleSetStatusService_client", "SetMaintenanceMode", {"isOn": False})
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.soa.send_method_request("VehicleSetStatusService_client", "SetMaintenanceMode", {"isOn": True})
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="MaintenanceMode")
            if get_data == 11:
                assert get_data == 11
                break
            sleep(0.5)
        assert get_data == 11
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.soa.send_method_request("VehicleSetStatusService_client", "SetMaintenanceMode", {"isOn": False})
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleMode)
            get_data = self.handle_ble_msg_vehicle_mode(ble_date=bytes(ble_bytes),func_module="MaintenanceMode")
            if get_data == 10:
                assert get_data == 10
                break
            sleep(0.5)
        assert get_data == 10
