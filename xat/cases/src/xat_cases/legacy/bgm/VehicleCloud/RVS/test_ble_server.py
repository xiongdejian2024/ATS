# import os
# import sys
# import pytest
# import allure
# from time import sleep
# import threading
# import math


# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))

# from ecu_simulator.driver.ssh_interface import command_send
# from ecu_simulator.common.data_type_handing import logger
# from ecu_simulator.soa_partner.src.base_partner import *


# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
# from sdk_interface.abc_interface import *
# from ecu_simulator.tsp.proto_parse import ProtoParse
# # from signal_value_mapping import *
# from google.protobuf.json_format import MessageToJson
# running_flag = True

# @allure.feature("SOA服务接口")
# @allure.story("BGM应用/ConditionCheckService")
# class TestBle(TestABCBase):    
#     def before_class(self, ecu):
#         """测试用例的前处理"""
#         super().before_class(self, ecu)
#         for process_name in ["monitor_em2.sh", "em2", "s2s_service","SOAApp","service_monitor"]:
#             res = command_send(
#                 device_name="BGM",
#                 cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
#                 timeout=60,
#             )[1]
#             logger.info(f"res: {res}")
#             pid = res.split()[1]
#             command_send(device_name="BGM", cmd=f"kill -9 {pid}")
#         sleep(2)
#         command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /app/etc/service_monitor.json &"', timeout=15)

#         self.soa.update(["HighVoltageService_server","WiperService_server","ChassisService_server","ShieldWindowService_server","VehicleModeService_server","CentralLockService_server","OuterRearViewService_server","InteractiveService_server","TyreService_server","SentryModeService_server","SteerWheelService_server","AccountService_server","VehicleSetStatusService_server","LowVoltageService_server","KeyService_server","BlueToothService_server"])
   
#         self.soa.start_send_GetHVBatterySOH_response()
#         self.soa.start_send_GetHVSOCInfo_response()
#         self.soa.start_send_GetRange_response()
#         self.soa.start_send_GetBatteryStatus_response()
#         # self.bus_comm.set_bluetooth_key_connect_sts(key_num=1,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
#         # self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15],
#         #                 "type": 2, "isConnected": True, "zone": 1},
#         #                {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#         #                 "type": 0, "isConnected": False, "zone": 0},
#         #                {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#         #                 "type": 0, "isConnected": False, "zone": 0},
#         #                {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#         #                 "type": 0, "isConnected": False, "zone": 0}]})

#         running_flag = True
#         self.rev_msg_list = []
#         self.protoparse = ProtoParse()
#         self.bus_comm.start_dk()
#         sleep(1)
#         self.bus_comm.set_door_open_angle_sts(door_pos=DoorId.kDoorAll,angle=1)
#         self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)
#         self.bus_comm.set_batterylow_mode(DCChrgnHndlSts=DCChrgnHndlSts.Init,DispHvBattLvlOfChrg=0)
#         # self.bus_comm.set_bluetooth_key_connect_sts(key_num=1,type=BlueType.BLE_Key,con_sts=ConnSts.Connect)
#         self.soa.send_event_notify("KeyService_server", "DigitalKeyConnectedStatus",{"status":[{"keyId": [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15],
#                         "type": 2, "isConnected": True, "zone": 1},
#                        {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#                         "type": 0, "isConnected": False, "zone": 0},
#                        {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#                         "type": 0, "isConnected": False, "zone": 0},
#                        {"keyId": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#                         "type": 0, "isConnected": False, "zone": 0}]})
#         self.bus_comm.get_ble_bytes_thread_start()
#         sleep(3)

#     def after_class(self, ecu):
#         """测试用例全部完成后的后处理"""
#         self.bus_comm.get_ble_bytes_thread_stop()
#         self.soa.stop_soa()
#         sleep(1)
#         self.io.bgm_power_off()
#         sleep(1)
#         self.io.bgm_power_on()
#         sleep(15)

#     def before_each_func(self, ecu):
#         """每个测试用例前置步骤"""
#         pass

#     def after_each_func(self, ecu):
#         self.bus_comm.clear_all_bus_buffer()
#         sleep(1)


#     def get_ble_bytes(self, msg_list, blockid:BlockName):
#         ble_bytes = None
#         if msg_list == None:
#             logger.info(f"获取的总线报文为空,没有触发响应的蓝牙数据")
#             assert False
#         else:
#             for msg in msg_list:
#                 logger.info(f'msg_block_id:{self.protoparse.get_vehicle_mode(bytes(msg)).head.blockID}')
#                 if self.protoparse.get_vehicle_mode(bytes(msg)).head.blockID == blockid.value:
#                     ble_bytes = bytes(msg)
#             return ble_bytes

    
#     def handle_ble_msg_veh_body(self,ble_date,func_module:Union[DoorId,WindowId,DCChrgnHndlSts,str]):
#         prompt_info = f"---------->解析接收的车身状态(VehicleBodyBlock)总线数据"
#         with allure.step(prompt_info):
#             logger.info(prompt_info)
#             get_data = self.protoparse.get_vehicle_body_info(ble_date)
#             get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
#             logger.info(f'get_data_dict: {get_data_dict}')
#             if isinstance(func_module,DoorId):
#                 for get_info in get_data.doors:
#                         if get_info.id == func_module.value:
#                             info = get_info
#             elif isinstance(func_module,WindowId):
#                 for get_info in get_data.windows:
#                         if get_info.id == func_module.value:
#                             info = get_info
#             elif func_module == "CentralLock":
#                 info = get_data.centralLock
#             elif func_module == "TailGateSts":
#                 info = get_data.tailGate.status
#             elif func_module == "TailGatePos":
#                 info = get_data.tailGate.position
#             logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
#             return info

#     def handle_ble_msg_eic_charge(self,ble_date,func_module:BleEicCharg):
#         prompt_info = f"---------->解析接收的充电三电信息块(EicChargingBlock)总线数据"
#         with allure.step(prompt_info):
#             logger.info(prompt_info)
#             get_data = self.protoparse.get_charging_info(ble_date)
#             get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
#             logger.info(f'get_data_dict: {get_data_dict}')
#             logger.info(f"---------->解析之后的EicChargingBlock具体信息:")
#             if func_module.name == "Charging":
#                 info = get_data.charging
#             if func_module.name == "BatteryInfo":
#                 info = get_data.batteryInfo     
                
#             logger.info(f"---------->解析之后的子模块{func_module.name}信息为:{info}")
#             return info
    
#     def handle_ble_msg_vehicle_mode(self,ble_date,func_module:str):
#         prompt_info = f"---------->解析接收的车辆模式信息块(VehicleMode)总线数据"
#         with allure.step(prompt_info):
#             logger.info(prompt_info)
#             get_data = self.protoparse.get_vehicle_mode(ble_date)
#             get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
#             logger.info(f'get_data_dict: {get_data_dict}')
#             logger.info(f"---------->解析之后的VehicleMode具体信息:")
#             if func_module == "UsageMode":
#                 info = get_data.usage  
#             if func_module == "CarMode":
#                 info = get_data.model
#             logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
#             return info

#     def handle_ble_msg_BusStatus(self,ble_date,func_module:str):
#         prompt_info = f"---------->解析接收的车辆状态信息块(BusStatus)总线数据"
#         with allure.step(prompt_info):
#             logger.info(prompt_info)
#             get_data = self.protoparse.get_function_info(ble_date)
#             get_data_dict = MessageToJson(get_data, including_default_value_fields=True)
#             logger.info(f'get_data_dict: {get_data_dict}')
#             logger.info(f"---------->解析之后的BusStatus具体信息:")
#             if func_module == "account":
#                 info = get_data.account
#             logger.info(f"---------->解析之后的子模块{func_module}信息为:{info}")
#             return info




#     @pytest.mark.smoke
#     def test_charggun_caseid_111111(self):
#         self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
#                                        {"info":{"pluggerStatus":1}})
#         sleep(1)
#         for charggun_sts in range(0,12):
#             self.bus_comm.clear_block_bytes()
#             self.soa.send_event_notify("HighVoltageService_server",  "ChargingInfo",
#                                        {"info":{"pluggerStatus":charggun_sts}})
#             start_time = time.time()
#             while time.time() - start_time < 2:
#                 ble_bytes = self.bus_comm.get_block_bytes(BlockName.EicCharging)
#                 get_data = self.handle_ble_msg_eic_charge(ble_date=bytes(ble_bytes),func_module=BleEicCharg.Charging)
#                 if get_data.pluggerStatus == charggun_sts:
#                     assert get_data.pluggerStatus == charggun_sts
#                     break
#                 sleep(0.5)
#             assert get_data.pluggerStatus == charggun_sts


#     @allure.title("左前胎压")
#     @pytest.mark.sanity
#     def test_caseid_222222(self):
#         self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
#                                        {"infos": [{"id": 0, "pressure": 230.5},
#                                                 {"id": 1, "pressure": 220.5},
#                                                 {"id": 2, "pressure": 220.5},
#                                                 {"id": 3, "pressure": 220.5}]})
#         sleep(1)
#         for key in [220.5,226.5,350.114]:
#             self.bus_comm.clear_block_bytes()
#             self.soa.send_event_notify("TyreService_server", "AllTyrePressure", 
#                                        {"infos": [{"id": 0, "pressure": key},
#                                                 {"id": 1, "pressure": 220.5},
#                                                 {"id": 2, "pressure": 220.5},
#                                                 {"id": 3, "pressure": 220.5}]})
#             sleep(1)
#             start_time = time.time()
#             while time.time() - start_time < 3:
#                 ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
#                 get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module=BleVehicleBody.Tire)
#                 if get_data.get_data.pressure == round(key*0.01,1):
#                     assert get_data.get_data.pressure == round(key*0.01,1)
#                     break
#                 sleep(0.5)
#             assert get_data.pressure == round(key*0.01,1)


#     @allure.title("中控锁状态")
#     @pytest.mark.sanity
#     def test_caseid_220220(self):
#         self.soa.send_event_notify("CentralLockService_server", "NotifyCentralLockSysInfo",  {"info": {"sts":0}})
#         for key in [1,2,3,0]:
#             self.bus_comm.clear_block_bytes()
#             self.soa.send_event_notify("CentralLockService_server", "NotifyCentralLockSysInfo",  {"info": {"sts":key}})
#             ble_bytes = self.bus_comm.get_block_bytes(BlockName.VehicleBody)
#             get_data = self.handle_ble_msg_veh_body(ble_date=bytes(ble_bytes),func_module="CentralLock")
#             assert get_data.status ==  key