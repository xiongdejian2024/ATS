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
            if func_module.name == "BatteryInfo":
                info = get_data.batteryInfo     
                
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
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359776?projectId=46', name='蓝牙数据上报 112101')
    def test_charggun_caseid_112101(self):
        for charggun_sts in [0,1,3]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_ble_bus_siginal_charge(func_module=BleEicCharg.Charging,sub_func=BleCharging.PluggerSts,value= charggun_sts)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.pluggerStatus == charggun_sts:
                    assert get_data.pluggerStatus == charggun_sts
                    break
                sleep(0.5)
            assert get_data.pluggerStatus == charggun_sts


    @pytest.mark.sanity
    def test_charging_status_caseid_1918982(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',15)
        sleep(1)
        for key in [1,15,24,26]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',key)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.chargingStatus == key:
                    assert get_data.chargingStatus == key
                    break
                sleep(0.5)
            assert get_data.chargingStatus == key
    

    @pytest.mark.sanity
    def test_chrglid_status_caseid_112106(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_chrglid_pos(0)
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(100)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.lidStatus == 0:
                assert get_data.lidStatus == 0
                break
            sleep(0.5)
        assert get_data.lidStatus == 0
        sleep(5)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.lidStatus == 2:
                assert get_data.lidStatus == 2
                break
            sleep(0.5)
        assert get_data.lidStatus == 2


    @pytest.mark.full
    def test_charg_maxcurrent_caseid_1990774(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",0)
        sleep(1)
        for signal_value in [1633.4, 1634.5, 1635.6,1637.7]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",signal_value)
            start_time = time.time()
            while time.time() - start_time < 10:
                self.bus_comm.clear_block_bytes()
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if round(get_data.equipmentInfo.maxCurrent,1) == signal_value:
                    assert round(get_data.equipmentInfo.maxCurrent,1) == signal_value
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
            # get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            assert round(get_data.equipmentInfo.maxCurrent,1) == signal_value


    @pytest.mark.full
    def test_charg_actualcurrent_caseid_1987912(self):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',5)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",0)
        sleep(1)
        for signal_value in [10.0]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",signal_value)
            sleep(10)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=10)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            assert get_data.equipmentInfo.actualCurrent == signal_value


    @pytest.mark.sanity
    def test_charg_voltage_caseid_112096(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",0)
        sleep(2)
        for signal_value in [220, 224, 880,884]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",signal_value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.BatteryInfo)
            assert get_data.voltage == signal_value*0.25


    # @pytest.mark.full
    # def test_equipment_type_caseid_1983037_116052(self):
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr02","JIDUChgrFlg",2)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","equipmentInfo","type"],target_value=[7,1]
    #         )
    #     self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03","ChrgrPileInfo",0)
    #     self.tsp.check_rvs_data_update_new(
    #             block=BlockName.EicCharging,keys=["charging","equipmentInfo","type"],target_value=[7,1],timeout=12,sleep_time=15
    #         )


    # @pytest.mark.sanity
    # def test_charg_InputPower_caseid_1989454(self):
    #     self.sd_tester.write_ccp(ccp={962: 0x00})
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr02","JIDUChgrFlg",2)
    #     self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03","ChrgrPileInfo",0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',0)
    #     sleep(1)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',5)
    #     for vol in [280]:
    #         for cur in [10]:
    #             self.bus_comm.clear_block_bytes()
    #             self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",vol)
    #             self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",cur)
    #             ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=10)
    #             get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #             assert round(get_data.chargerInputPower,1) == (vol)*0.25*(cur)


    # @pytest.mark.sanity
    # def test_charg_targetsoc_caseid_112102(self):
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",0)
    #     sleep(1)
    #     for signal_value in [100,110,800,1000]:
    #         self.bus_comm.clear_block_bytes()
    #         self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",signal_value)
    #         start_time = time.time()
    #         while time.time() - start_time < 2:
    #             ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
    #             get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #             if get_data.chargeTargetSoc == signal_value*0.1:
    #                 assert get_data.chargeTargetSoc == signal_value*0.1
    #                 break
    #             sleep(0.5)
    #         assert get_data.chargeTargetSoc == signal_value*0.1
             


    @pytest.mark.sanity
    def test_totalChargeEnergy_caseid_112092(self):
        self.sd_tester.write_ccp(ccp={566: 0x10})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",500)
        sleep(1)
        for signal_value in [10000,10100,80000,80100]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",signal_value)
            start_time = time.time()
            while time.time() - start_time < 12:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.totalChargeEgy == signal_value:
                    assert get_data.totalChargeEgy == signal_value
                    break
                sleep(0.5)
            assert get_data.totalChargeEgy == signal_value
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=10)
            # get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            # assert get_data.totalChargeEgy == signal_value

    @pytest.mark.sanity
    def test_remainChargingTime_caseid_112103(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr21","HvBattChrgnTiEstimd",0)
        sleep(1)
        for signal_value in [60,50]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr21","HvBattChrgnTiEstimd",signal_value)
            sleep(10)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=10)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            assert get_data.remainChargingTime == signal_value

    @pytest.mark.full
    def test_chrglid_pos_caseid_1989455(self):
        self.bus_comm.set_chrglid_pos(0)
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(100)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.chargingLidPos == 100:
                assert get_data.chargingLidPos == 100
                break
            sleep(0.5)
        assert get_data.chargingLidPos == 100
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.chargingLidPos == 0:
                assert get_data.chargingLidPos == 0
                break
            sleep(0.5)
        assert get_data.chargingLidPos == 0

    
    @pytest.mark.sanity
    def test_chrgegythistime_caseid_1989456_112093(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",0)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr16","TotChrgEgy",10000)
        sleep(30)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
        sleep(10)
        ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=10)
        get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
        assert get_data.chargeEgyThisTime == 10000

    @pytest.mark.sanity
    def test_chargTime_caseid_112353(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        sleep(2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        utc_timestamp = time.time()
        sleep(5)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","recentChargeStartTime"],target_value=utc_timestamp*1000,timeout=12,sleep_time=11,target_value_buffer=1000)
        sleep(10)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
        utc_timestamp =time.time()
        sleep(5)
        self.tsp.check_rvs_data_update_new(
                block=BlockName.EicCharging,keys=["charging","recentChargeEndTime"],target_value=utc_timestamp*1000,timeout=12,sleep_time=11,target_value_buffer=1000)


    @pytest.mark.sanity
    def test_charg_booktime_caseid_1989457(self):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrhour",24)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrmin",60)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrhour",24)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrmin",60)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr32","ChrgPilBookChrgn",1)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrmin",30)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrhour",20)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStopTiChrgnTmrChrgnTmrmin",10)
        for signal_value in [11,13,15]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr33","RemoteBookStrtTiChrgnTmrChrgnTmrhour",signal_value)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.bookInfo.startHour == signal_value:
                    assert get_data.bookInfo.startHour == signal_value
                    break
                sleep(0.5)
            assert get_data.bookInfo.startHour == signal_value

    @pytest.mark.sanity
    @allure.testcase(
        'https://jama.jiduauto.com/perspective.req#/testCases/1350998?projectId=46',
        name='RVS case 1981197',
    )
    def test_chargbook_status_caseid_1989458(self):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn',2)
        sleep(1)
        for key in [1,2]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr32", 'ChrgPilBookChrgn',key)
            start_time = time.time()
            while time.time() - start_time < 10:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.bookInfo.bookStatus == key:
                    assert get_data.bookInfo.bookStatus == key
                    break
                sleep(0.5)
            assert get_data.bookInfo.bookStatus == key


    # @pytest.mark.sanity
    # def test_targetRange_caseid_1989459(self):
    #     self.sd_tester.write_multi_ccp({3: 129, 566: 25,950:1,962:0})
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 90.0)
    #     self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 90.0)
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                         {"infos": {"type": 0, "CLTCRange": 50, "estimatedRange": 999}})
    #     sleep(2)
    #     self.bus_comm.clear_block_bytes()
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 100.0)
    #     self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 100.0)
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                         {"infos": {"type": 0, "CLTCRange": 600, "estimatedRange": 999}})
    #     start_time = time.time()
    #     while time.time() - start_time < 2:
    #         ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
    #         get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #         if get_data.chargeTargetMileage == 630:
    #             assert get_data.chargeTargetMileage == 630
    #             break
    #         sleep(0.5)
    #     assert get_data.chargeTargetMileage == 630
    #     sleep(2)
    #     self.bus_comm.clear_block_bytes()
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 0.0)
    #     self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 0.0)
    #     self.soa.send_method_request("HighVoltageService_client", "SetRange",
    #                                         {"infos": {"type": 0, "CLTCRange":0, "estimatedRange": 999}})
    #     start_time = time.time()
    #     while time.time() - start_time < 2:
    #         ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
    #         get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #         if get_data.chargeTargetMileage == 0:
    #             assert get_data.chargeTargetMileage == 0
    #             break
    #         sleep(0.5)
    #     assert get_data.chargeTargetMileage == 0

    
    @pytest.mark.sanity
    def test_incMileageThisTime_caseid_112091_1986702(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 25,950:1,962:0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 0.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 0.0)
        self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                            {"infos": {"type": 0, "CLTCRange":0, "estimatedRange": 999}})
        sleep(2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 100.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 100.0)
        sleep(2)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCChargingEnd)
        incMileageThisTime= [0,999]
        for key in incMileageThisTime:
            self.bus_comm.clear_block_bytes()
            self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                            {"infos": {"type": 0, "CLTCRange": key, "estimatedRange": 999}})
            start_time = time.time()
            while time.time() - start_time < 12:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=12)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.incMileageThisTime == key:
                    assert get_data.incMileageThisTime == key
                    break
                sleep(0.5)
            assert get_data.incMileageThisTime == key

    
    @pytest.mark.sanity
    def test_current_caseid_112097(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'HvBattIDc1', 0.0)
        sleep(2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        sleep(2)
        current= [-1638.0,10.0,11.0,1638.6]
        for key in current:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'HvBattIDc1', key)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.BatteryInfo)
            assert round(get_data.current,1) == key

    @pytest.mark.full
    def test_charg_maxcurrent_caseid_1987911(self):
        '''不用满足1A精度组包 '''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",0)
        sleep(1)
        for signal_value in [1637.0,1637.5,1638.7]:
            self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",signal_value)
            start_time = time.time()
            while time.time() - start_time < 10:
                self.bus_comm.clear_block_bytes()
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if round(get_data.equipmentInfo.maxCurrent,1) == signal_value:
                    assert round(get_data.equipmentInfo.maxCurrent,1) == signal_value
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
            # get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            assert round(get_data.equipmentInfo.maxCurrent,1) == signal_value

    @pytest.mark.full
    def test_charg_voltage_caseid_1987910(self):
        '''不用满足1V精度组包 '''
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",0)
        sleep(1)
        for signal_value in [220,222,880,882]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr01","HvBattUDc",signal_value)
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.BatteryInfo)
            assert get_data.voltage == signal_value*0.25

    @pytest.mark.full
    def test_batteryReqCurrent_caseid_1987908(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","EcmPropXEVFr16",'HvBattChrgnILim',20)
        sleep(1)
        for key in [0,21.0,819.1]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","EcmPropXEVFr16",'HvBattChrgnILim',key)
            start_time = time.time()
            while time.time() - start_time < 12:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if round(get_data.batteryReqCurrent,1) == key:
                    assert round(get_data.batteryReqCurrent,1) == key
                    break
                sleep(0.5)
            assert round(get_data.batteryReqCurrent,1) == key

    @pytest.mark.full
    def test_isCharging_caseid_1987907(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.isCharging == True:
                assert get_data.isCharging == True
                break
            sleep(0.5)
        assert get_data.isCharging == True
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.isCharging == False:
                assert get_data.isCharging == False
                break
            sleep(0.5)
        assert get_data.isCharging == False


    @pytest.mark.full
    def test_isConnect_caseid_1987906(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.isConnect == True:
                assert get_data.isConnect == True
                break
            sleep(0.5)
        assert get_data.isConnect == True
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.isConnect == False:
                assert get_data.isConnect == False
                break
            sleep(0.5)
        assert get_data.isConnect == False

    
    @pytest.mark.sanity
    def test_Temperature_caseid_1987905(self):
        '''电池显示温度 '''
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',0)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMax',0)
        for key in [-256.0,20.0,39.9,40.0,41.0,255.9]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',key)
            sleep(10)
            start_time = time.time()
            while time.time() - start_time < 12:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if round(get_data.chargingSlowRemind.temperature,1) == key:
                    assert round(get_data.chargingSlowRemind.temperature,1) == key
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
            # get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            assert round(get_data.chargingSlowRemind.temperature,1) == key
        # sleep(2)
        # for key in [40.0,41.0,255.9]:
        #     self.bus_comm.clear_block_bytes()
        #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',30.0)
        #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMax',key)
        #     ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
        #     get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
        #     assert round(get_data.chargingSlowRemind.temperature,1) == key

    # @pytest.mark.sanity
    # def test_ChargingSlowRemind_caseid_300300(self):
    #     '''从0开始跳变 '''
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr13",'HvBattChrgnPwrCns1',5)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMax',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",0)
    #     self.bus_comm.set_SOC_display_value(79.0)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
    #     sleep(1)
    #     self.bus_comm.clear_block_bytes()
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr22","ChrgEquipIDc",10.0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',30.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",30.0)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',19.0)
    #     sleep(2)
    #     ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
    #     get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #     assert get_data.chargingSlowRemind.reason == [1]
    #     sleep(10)
    #     ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
    #     get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #     assert get_data.chargingSlowRemind.reason == [3,1]
    #     sleep(2)
    #     self.bus_comm.set_SOC_display_value(80.0)
    #     ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
    #     get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #     assert get_data.chargingSlowRemind.reason == [3,2,1]
    #     sleep(2)
    #     self.bus_comm.clear_block_bytes()
    #     self.bus_comm.set_SOC_display_value(70.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr09",'HvBattTMin',20.0)
    #     self.bus_comm.set_singal("backbonefr","VddmBackBoneFr28",'HvBattILim',20.0)
    #     self.bus_comm.set_singal("propulsioncan","BecmPropFr31","DCChrgrIMax",150.0)
    #     ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
    #     get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
    #     assert get_data.chargingSlowRemind.reason == [0]


    @allure.title("获取和通知动力电池充电功率")
    @pytest.mark.sanity
    def test_caseid_112094(self):
        self.sd_tester.write_multi_ccp({950:2})
        self.sd_tester.write_multi_ccp({962:2})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr12", 'HvBattChrgnPwrCns800', 100.0)
        sleep(1)
        for key in [0,1000,4095]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr12", 'HvBattChrgnPwrCns800', key)
            start_time = time.time()
            while time.time() - start_time < 2:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=15)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.chargingPower == key*100:
                    assert get_data.chargingPower == key*100
                    break
                sleep(0.5)
            # ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=11)
            # get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            assert get_data.chargingPower == key*100
        sleep(1)
        self.sd_tester.write_multi_ccp({950:1})
        self.sd_tester.write_multi_ccp({962:0})


    @pytest.mark.sanity
    @pytest.mark.v210
    def test_isDischarging_caseid_1990901(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',0)
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',8)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.isDischarging == True:
                assert get_data.isDischarging == True
                break
            sleep(0.5)
        assert get_data.isDischarging == True
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',15)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.isDischarging == False:
                assert get_data.isDischarging == False
                break
            sleep(0.5)
        assert get_data.isDischarging == False
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb',0)


    @pytest.mark.sanity
    def test_acdcType_caseid_1990900(self):
        self.sd_tester.write_multi_ccp({973:2}) # 支持交直流  
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',1)        
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1) 
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',8)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.acdcType == 1:
                assert get_data.acdcType == 1
                break
            sleep(0.5)
        assert get_data.acdcType == 1
        sleep(1)
        self.bus_comm.clear_block_bytes()
        # self.sd_tester.write_multi_ccp({973:1}) # 支持交流
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',5)        
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.acdcType == 2:
                assert get_data.acdcType == 2
                break
            sleep(0.5)
        assert get_data.acdcType == 2
        # self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)        
        # self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0) 
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',1)        
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.acdcType == 3:
                assert get_data.acdcType == 3
                break
            sleep(0.5)
        assert get_data.acdcType == 3
        sleep(1)
        self.sd_tester.write_multi_ccp({973:2}) # 支持交直流  
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)        
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)


    @allure.title("2.1新增充电枪状态")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_charggun_caseid_1990899(self):
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
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 0:
                assert get_data.pluggerStatus == 0
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 0         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',1)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 1:
                assert get_data.pluggerStatus == 1
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 1        
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',2)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 2:
                assert get_data.pluggerStatus == 2
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 2         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',3)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 3:
                assert get_data.pluggerStatus == 3
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 3         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',4)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 4:
                assert get_data.pluggerStatus == 4
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 4         
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',5)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 5:
                assert get_data.pluggerStatus == 5
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 5
        sleep(1)      
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',10)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 7:
                assert get_data.pluggerStatus == 7
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 7        
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',4)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 8:
                assert get_data.pluggerStatus == 8
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 8  
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',5)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 9:
                assert get_data.pluggerStatus == 9
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 9  
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',6)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 10:
                assert get_data.pluggerStatus == 10
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 10  
        sleep(1)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',7)
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.pluggerStatus == 11:
                assert get_data.pluggerStatus == 11
                break
            sleep(0.5)
        assert get_data.pluggerStatus == 11 
        sleep(1)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts',0)
        self.bus_comm.set_singal("propulsioncan","CddObcPropFr01", 'OnBdChrgrHndlSts1',0)



    @pytest.mark.sanity
    def test_chrglid_status_caseid_112106(self):
        self.bus_comm.set_chrglid_pos(0)
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(100)
        start_time = time.time()
        while time.time() - start_time < 12:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.lidStatus == 0:
                assert get_data.lidStatus == 0
                break
            sleep(0.5)
        assert get_data.lidStatus == 0
        sleep(2)
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_chrglid_pos(0)
        start_time = time.time()
        while time.time() - start_time < 12:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.lidStatus == 2:
                assert get_data.lidStatus == 2
                break
            sleep(0.5)
        assert get_data.lidStatus == 2


    @pytest.mark.sanity
    def test_charg_targetsoc_caseid_112102(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",0)
        sleep(1)
        for signal_value in [50,0,100,110,800,1000]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",signal_value)
            start_time = time.time()
            while time.time() - start_time < 12:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if get_data.chargeTargetSoc == signal_value*0.1:
                    assert get_data.chargeTargetSoc == signal_value*0.1
                    break
                sleep(0.5)
            assert get_data.chargeTargetSoc == signal_value*0.1 
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",0)


    @allure.title("通知和获取充电桩信息_equipmentTypes")
    @pytest.mark.full
    @pytest.mark.v210only
    def test_caseid_112090_1990898_1990772(self):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts', 2)
        sleep(1)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts', 0)
        #非集度桩私桩
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr02", 'JIDUChgrFlg', 0)
        self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03", 'ChrgrPileInfo', 0)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts', 1)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr02", 'JIDUChgrFlg', 2)
        self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03", 'ChrgrPileInfo', 1)
        sleep(0.5)
        start_time = time.time()
        while time.time() - start_time < 12:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=12)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.equipmentInfo.type == [3,1]:
                assert get_data.equipmentInfo.type == [3,1]
                break
            sleep(0.5)
        assert get_data.equipmentInfo.type == [3,1]       
        #记忆集度桩公桩
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr02", 'JIDUChgrFlg', 2)
        self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03", 'ChrgrPileInfo', 2)
        sleep(0.5)
        start_time = time.time()
        while time.time() - start_time < 12:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=12)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.equipmentInfo.type == [4,1]:
                assert get_data.equipmentInfo.type == [4,1]
                break
            sleep(0.5)
        assert get_data.equipmentInfo.type == [4,1]
        #充电枪未连接2S内
        self.bus_comm.clear_block_bytes()
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts', 0)
        sleep(0.5)
        start_time = time.time()
        while time.time() - start_time < 12:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=12)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.equipmentInfo.type == [7,0]:
                assert get_data.equipmentInfo.type == [7,0]
                break
            sleep(0.5)
        assert get_data.equipmentInfo.type == [7,0]
    

    @allure.title("通知表显续航里程_100度电池_cltc续航660km_targetRange的情况")
    @pytest.mark.full
    @pytest.mark.v210only
    def test_caseid_1989459_1986703(self):
        self.sd_tester.write_multi_ccp({3: 128, 566: 16,950:1,962:0,966:0})
        self.bus_comm.set_singal("propulsioncan","BecmPropFr04", 'HvBattEgyCdn', 99.0)
        # self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 0)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", 'DispHvBattLvlOfChrg', 100.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13", 'BookChrgnTarValFb', 100.0)
        self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                            {"infos": {"type": 1, "CLTCRange": 999, "estimatedRange": 999}})
        self.soa.send_method_request("HighVoltageService_client", "SetAveragePowerConsume", {"power": 50})
        sleep(2)
        # targetRange跟随targetCLTCRange
        self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                            {"infos": {"type": 0, "CLTCRange": 999, "estimatedRange": 999}})
                #电池健康度大于99%时
        self.bus_comm.clear_block_bytes()
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.chargeTargetMileage == 660:
                assert get_data.chargeTargetMileage ==660
                break
            sleep(0.5)
        assert get_data.chargeTargetMileage ==660
        # self.tsp.check_rvs_data_update_new(BlockName.EicCharging,keys=["charging", "chargeTargetMileage"], target_value=660,timeout=12)
                #切换为1估算类型
        self.bus_comm.clear_block_bytes()
        self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                            {"infos": {"type": 1, "CLTCRange": 999, "estimatedRange": 999}})
        self.soa.send_method_request("HighVoltageService_client", "SetAveragePowerConsume", {"power": 20})
        start_time = time.time()
        while time.time() - start_time < 2:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.chargeTargetMileage == 483:
                assert get_data.chargeTargetMileage ==483
                break
            sleep(0.5)
        assert get_data.chargeTargetMileage ==483


    @allure.title("通知和获取充电桩信息_actualCurrent")
    @pytest.mark.full
    @pytest.mark.v210only
    def test_caseid_1990775(self):
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr16", 'ChrgnOrDisChrgnStsFb', 0)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts', 0)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'HvBattIDc1', 0.0)
        for key in [-1638.0,-10.0,0.0,1638.6]:
            self.bus_comm.clear_block_bytes()
            self.bus_comm.set_singal("propulsioncan","BecmPropFr22", 'ChrgEquipIDc', key)
            sleep(0.5)
            start_time = time.time()
            while time.time() - start_time < 13:
                ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=13)
                get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                if round(get_data.equipmentInfo.actualCurrent,1) == key:
                    assert round(get_data.equipmentInfo.actualCurrent,1) == key
                    break
                sleep(0.5)
            assert round(get_data.equipmentInfo.actualCurrent,1) == key


    
    @allure.title("通知和获取充电桩信息_chargePowerInput_800V")
    @pytest.mark.sanity
    @pytest.mark.v210only
    def test_caseid_1989454(self):
        self.sd_tester.write_single_ccp(962,2)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", 'HvBattUDc', 400.0)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", 'HvBattUDc800', 500.0)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr22", 'ChrgEquipIDc', 100.0)
        sleep(0.5)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", 'DCChrgnHndlSts', 0)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr22", 'ChrgEquipIDc', 10.0)
        sleep(1)
        #仅电流变化时
        for voltage1 in [1023.75]:
            for current1 in [100.0,200.0,800.0]:
                logger.info(f"发送电流={current1}")
                self.bus_comm.clear_block_bytes()
                self.bus_comm.set_singal("propulsioncan","BecmPropFr01", 'HvBattUDc800', voltage1)
                sleep(0.5)
                self.bus_comm.set_singal("propulsioncan","BecmPropFr22", 'ChrgEquipIDc', current1)
                sleep(1)
                start_time = time.time()
                while time.time() - start_time < 13:
                    ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=13)
                    get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
                    if get_data.chargerInputPower == (voltage1)*(current1):
                        assert get_data.chargerInputPower == (voltage1)*(current1)
                        break
                    sleep(0.5)
                assert get_data.chargerInputPower == (voltage1)*(current1)


    @allure.title("新75度设置百公里电耗为0_充电速度")
    @pytest.mark.sanity
    @pytest.mark.v210only
    def test_caseid_112104_1993243(self):
        self.sd_tester.write_multi_ccp({3: 129, 566: 25,950:1,962:0,966:2})#增加400V
        sleep(3)
        self.soa.send_method_request("HighVoltageService_client", "SetRange",
                                         {"infos": {"type": 0, "CLTCRange": 999, "estimatedRange": 999}})
        #12.75kWh/100km
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_charging_sts(sts=ChargingSts.NoCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr13", 'HvBattChrgnPwrCns1', 0)
        sleep(3)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_charging_sts(sts=ChargingSts.DCCharging)
        self.bus_comm.set_singal("propulsioncan","BecmPropFr13", 'HvBattChrgnPwrCns1', 100000.0)
        sleep(1)
        self.bus_comm.clear_block_bytes()
        start_time = time.time()
        while time.time() - start_time < 12:
            ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging,timeout=13)
            get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
            if get_data.chargingSpeed == 784:
                assert get_data.chargingSpeed ==784
                break
            sleep(0.5)
        assert get_data.chargingSpeed ==784