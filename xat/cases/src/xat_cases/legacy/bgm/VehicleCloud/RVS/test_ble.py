# # -*- coding: utf-8 -*-

# import time
# from ecu_simulator.common.logger import logger
# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
# import pytest
# from test_case.bgm.rvs.service_starter import Service_Starter
# from ecu_simulator.tsp.proto_parse import ProtoParse
# from ecu_simulator.sdk.bus_app import *
# import allure
# from ecu_simulator.ecu_sim.sd_tester import Sd_Tester
# from ble_message_receiver import *
 
# from test_case.bgm.case_helper.environment_check import partner_process_check

# @pytest.mark.order_last
# class TestBLEData(TestABCBase):
#     def before_class(self, bgm):
#         super().before_class(self, bgm)
#         partner_process_check()
#         self.protoparse = ProtoParse()
#         self.sd_tester = Sd_Tester(**self.tc_config)
#         self.sd_tester.diagnostic_client_sim_start()
#         self.sd_tester.tester_present()
#         self.ipdu.start_all_time_control()
#         self.busapp.start_all_cyclic_msg()
#         self.bletp = BLETP(self.ipdu)
#         self.ble_op = Service_Starter()
#         self.avp_server = self.ble_op.avp_server
#         self.rpaapa_server = self.ble_op.rpaapa_server
#         # self.centrallock_server = self.ble_op.cental_lock_server
#         self.tyre_server = self.ble_op.tyre_server
#         self.account_server = self.ble_op.account_server
#         self.highvoltage_client = self.ble_op.highvoltage_client
#         # self.rtc_client = self.ble_op.rtc_client
#         self.centrallock_client = self.ble_op.cental_lock_client
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1_ub_value(1)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2_ub_value(1)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3_ub_value(1)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4_ub_value(1)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyidbyte0_value(65)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keytyp_keytyp_ble_key()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyprsntzone_keyprsntzone_zone1()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyconnectsts_connectionsts_connect()
#         time.sleep(10)

#     def after_class(self, bgm):
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyidbyte0_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keytyp_keytyp_nokeyconnected()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyconnectsts_connectionsts_disconnect()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyconnectsts_connectionsts_disconnect()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyconnectsts_connectionsts_disconnect()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4keyconnectsts_connectionsts_disconnect()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1_ub_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2_ub_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3_ub_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4_ub_value(0)
#         self.bletp.stop()
#         self.sd_tester.stop_tester_present()
#         self.sd_tester.diagnostic_client_sim_close()
#         self.ipdu.time_control_stop()
#         self.busapp.stop_all_cyclic_msgs()
#         self.ble_op.kill_operators()
#         partner_process_check()
#         super().after_class
#         logger.info("Teardown_class execute finished!")

#     def before_each_func(self, bgm):
#         super().before_each_func

#     def after_each_func(self, bgm):
#         super().after_each_func

#     def get_ble_bytes(self, msg_list, blockid):
#         ble_bytes = None
#         for msg in msg_list:
#             if self.protoparse.get_vehicle_mode(bytes(msg)).head.blockID == blockid:
#                 ble_bytes = bytes(msg)
#         return ble_bytes


#     @pytest.mark.sanity
#     @pytest.mark.connection
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359840?projectId=46', name='蓝牙数据上报 1359840')
#     def test_all_block_report_the_first_connection_caseid_1359840(self):
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyidbyte0_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keytyp_keytyp_nokeyconnected()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyconnectsts_connectionsts_disconnect()
#         time.sleep(10)
#         block_show = {"10102": False, "10103": False, "10107": False, "10109": False, "19001": False}
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyidbyte0_value(65)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keytyp_keytyp_ble_key()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo1keyconnectsts_connectionsts_connect()
#         data = self.bus_comm.get_blue_tp_data(timeout=10)
#         logger.info("Get BLE data: {0}".format(data))
#         for msg in data:
#             ble_bytes = bytes(msg)
#             block_id = self.protoparse.get_vehicle_mode(ble_bytes).head.blockID
#             block_show[str(block_id)] = True
#         for (key, value) in block_show.items():
#             logger.info("Result of block {0}, {1}".format(key, value))
#             assert value

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359841?projectId=46', name='蓝牙数据上报 1359841')
#     def test_all_block_report_the_second_connection_caseid_112038(self):
#         block_show = {"10102": False, "10103": False, "10107": False, "10109": False, "19001": False}
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyidbyte0_value(66)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keytyp_keytyp_ble_key()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyconnectsts_connectionsts_connect()
#         data = self.bletp.get_bletp(0x31A)
#         logger.info("Get BLE data: {0}".format(data))
#         for msg in data:
#             ble_bytes = bytes(msg)
#             block_id = self.protoparse.get_vehicle_mode(ble_bytes).head.blockID
#             block_show[str(block_id)] = True
#         for (key, value) in block_show.items():
#             logger.info("Result of block {0}, {1}".format(key, value))
#             assert value
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyidbyte0_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keytyp_keytyp_nokeyconnected()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyconnectsts_connectionsts_disconnect()

#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359842?projectId=46', name='蓝牙数据上报 1359842')
#     def test_all_block_report_the_third_connection_caseid_112037(self):
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyidbyte0_value(66)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keytyp_keytyp_ble_key()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyconnectsts_connectionsts_connect()
#         time.sleep(5)
#         block_show = {"10102": False, "10103": False, "10107": False, "10109": False, "19001": False}
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyidbyte0_value(67)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keytyp_keytyp_ble_key()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyconnectsts_connectionsts_connect()        
#         data = self.bletp.get_bletp(0x31A)
#         logger.info("Get BLE data: {0}".format(data))
#         for msg in data:
#             ble_bytes = bytes(msg)
#             block_id = self.protoparse.get_vehicle_mode(ble_bytes).head.blockID
#             block_show[str(block_id)] = True
#         for (key, value) in block_show.items():
#             logger.info("Result of block {0}, {1}".format(key, value))
#             assert value
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyidbyte0_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keytyp_keytyp_nokeyconnected()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyconnectsts_connectionsts_disconnect()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyidbyte0_value(0)
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keytyp_keytyp_nokeyconnected()
#         self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyconnectsts_connectionsts_disconnect()

#     # @pytest.mark.smoke
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359843?projectId=46', name='蓝牙数据上报 1359843')
#     # def test_all_block_report_the_forth_connection_caseid_112036(self):
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyidbyte0_value(66)
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keytyp_keytyp_ble_key()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyconnectsts_connectionsts_connect()
#     #     time.sleep(5)
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyidbyte0_value(67)
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keytyp_keytyp_ble_key()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyconnectsts_connectionsts_connect()
#     #     time.sleep(10)
#     #     block_show = {"10102": False, "10103": False, "10107": False, "10109": False, "19001": False}
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4keyidbyte0_value(68)
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4keytyp_keytyp_ble_key()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4keyconnectsts_connectionsts_connect()
#     #     data = self.bletp.get_bletp(0x31A)
#     #     logger.info("Get BLE data: {0}".format(data))
#     #     for msg in data:
#     #         ble_bytes = bytes(msg)
#     #         block_id = self.protoparse.get_vehicle_mode(ble_bytes).head.blockID
#     #         block_show[str(block_id)] = True
#     #     for (key, value) in block_show.items():
#     #         logger.info("Result of block {0}, {1}".format(key, value))
#     #         assert value
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyidbyte0_value(0)
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keytyp_keytyp_nokeyconnected()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr18_digkeyconnectinfo2keyconnectsts_connectionsts_disconnect()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyidbyte0_value(0)
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keytyp_keytyp_nokeyconnected()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo3keyconnectsts_connectionsts_disconnect()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4keyidbyte0_value(0)
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4keytyp_keytyp_nokeyconnected()
#     #     self.ipdu.connectivitycanfd_bncmconnectivityfr19_digkeyconnectinfo4keyconnectsts_connectionsts_disconnect()

#     @pytest.mark.smoke
#     def test_10102_usagemode_caseid_112128(self):
#         self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#         self.sd_tester.update_serverdoipid(0x1002)
#         time.sleep(1)
#         for um in [13,11,2,1,0]:
#             t = BLETP(self.ipdu)
#             t.start()
#             time.sleep(1)
#             logger.info(self.sd_tester.change_usage_mode(um,do_assert=True))
#             ble_bytes = self.get_ble_bytes(t.get_result(), 10102)
#             usage_mode = self.protoparse.get_vehicle_mode(ble_bytes).usage
#             logger.info("Get usagemode status: {0}".format(usage_mode))
#             assert usage_mode == um

#     # @pytest.mark.sanity
#     # @pytest.mark.carmode
#     # def test_10102_carmode_caseid_1359747(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     logger.info(self.sd_tester.change_usage_mode(1, do_assert=True))
#     #     for cm in [4,5,3,2,1,0]:
#     #         t = BLETP(self.ipdu)
#     #         t.start()
#     #         time.sleep(1)
#     #         logger.info("Start to get canTP!!")
#     #         logger.info(self.sd_tester.change_car_mode(cm,do_assert=True))
#     #         logger.info("change carmode!!")
#     #         ble_bytes = self.get_ble_bytes(t.get_result(), 10102)
#     #         car_mode = self.protoparse.get_vehicle_mode(ble_bytes).usage
#     #         logger.info("Get carmode status: {0}".format(car_mode))
#     #         assert car_mode == cm


#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359756?projectId=46', name='蓝牙数据上报 1359756')
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359757?projectId=46', name='蓝牙数据上报 1359757')
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359758?projectId=46', name='蓝牙数据上报 1359758')
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359759?projectId=46', name='蓝牙数据上报 1359759')
#     def test_window_status_caseid_1359759_1359758_1359757_1359756(self):
#         signal_name = ["WinPosnStsAtDrvr_0_DdmBodySignalIPdu04", "WinPosnStsAtPass_0_PdmBodySignalIPdu01",\
#                        "WinPosnStsAtReLe_0_RldmBodySignalIPdu01", "WinPosnStsAtReRi_0_RrdmBodySignalIPdu01"]
#         send_node = ["DdmBodyFr04", "PdmBodyFr01", "RldmBodyFr01", "RrdmBodyFr01"]
#         window_name = ["WindowFrontLeft", "WindowFrontRight", "WindowRearLeft", "WindowRearRight"]
#         for i in range(0,4):
#             for signal_value in [10, 20, 26, 1]:
#                 ble_bytes = None
#                 self.ipdu.set(getattr(self.ipdu.bodycan, send_node[i]), signal_name[i], signal_value)                
#                 ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(), 10103)
#                 window_info = self.protoparse.get_vehicle_body_info(ble_bytes).windows[i]
#                 logger.info("Test to window_id: {0}, window_posn:{1}".format(window_name[1], (signal_value-1)*4))
#                 assert i == window_info.id
#                 assert (signal_value-1)*4 == window_info.position
#                 # if signal_value == 1:
#                 #     assert window_info.status == 1
#                 # elif signal_value == 26:
#                 #     assert window_info.status == 0
#                 # else:
#                 #     assert window_info.status == 2

#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359798?projectId=46', name='蓝牙数据上报 1359798')
#     def test_tailgate_status_caseid_1359798(self):
#         for i in [1, 2, 3, 5, 6, 0]:
#             logger.info("Signal: {0}".format(i))
#             self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts_0_PotBodySignalIPdu02', i)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(), 10103)
#             tailgate_info = self.protoparse.get_vehicle_body_info(ble_bytes).tailGate
#             logger.info("Get tailgate status: {0}".format(tailgate_info))
#             if i == 3:
#                 assert tailgate_info.status == 4
#             elif i==0:
#                 assert tailgate_info.status == 5
#             elif i==1:
#                 assert tailgate_info.status == 2
#             elif i==2:
#                 assert tailgate_info.status == 3
#             elif i==5:
#                 assert tailgate_info.status == 0
#             elif i==6:
#                 assert tailgate_info.status == 1
    
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359797?projectId=46', name='蓝牙数据上报 1359797')
#     def test_tailgate_position_caseid_1359797(self):
#         for  j in range(1, 11):
#             logger.info("Signal: {0}".format(j))
#             self.ipdu.bodycan_potbodyfr03_tropenposn_value(j*10)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(), 10103)
#             tailgate_info = self.protoparse.get_vehicle_body_info(ble_bytes).tailGate
#             logger.info("Get tailgate position: {0}".format(tailgate_info.position))
#             assert tailgate_info.position == j*10

#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359752?projectId=46', name='蓝牙数据上报 1359752')
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359753?projectId=46', name='蓝牙数据上报 1359753')
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359754?projectId=46', name='蓝牙数据上报 1359754')
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359755?projectId=46', name='蓝牙数据上报 1359755')
#     def test_door_status_caseid_1359752_1359753_1359754_1359755(self):
#         signal_name = ["DoorOpenerDrvrSts_0_DpodBodySignalIPdu01", "DoorOpenerPassSts_0_PpodBodySignalIPdu01",\
#                        "DoorOpenerLeReSts_0_LpodBodySignalIPdu01", "DoorOpenerRiReSts_0_RpodBodySignalIPdu01"]
#         send_node = ["DpodBodyFr01", "PpodBodyFr01", "LpodBodyFr01", "RpodBodyFr01"]
#         for j in range(0,4):
#             for i in [5, 6, 1, 2, 3, 0]:
#                 self.ipdu.set(getattr(self.ipdu.bodycan, send_node[j]), signal_name[j], i)
#                 ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=1), 10103)
#                 for doorinfo in self.protoparse.get_vehicle_body_info(ble_bytes).doors:
#                     if doorinfo.id == j:
#                         door_info = doorinfo
#                 logger.info("Get dooropen status: {0}".format(door_info))
#                 if i == 3:
#                     assert door_info.status == 6
#                 elif i==0:
#                     assert door_info.status == 7
#                 elif i==1:
#                     assert door_info.status == 2
#                 elif i==2:
#                     assert door_info.status == 5
#                 elif i==5:
#                     assert door_info.status == 0
#                 elif i==6:
#                     assert door_info.status == 1
        
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359796?projectId=46', name='蓝牙数据上报 1359796')
#     def test_door_angle_caseid_1359796(self):
#         angle_message = ["DpodBodyFr01", "PpodBodyFr01", "LpodBodyFr01", "RpodBodyFr01"]
#         angle_signal = ["DoorDrvrPosn_0_DpodBodySignalIPdu01", "DoorPassPosn_0_PpodBodySignalIPdu01",\
#                         "DoorLeRePosn_0_LpodBodySignalIPdu01", "DoorRiRePosn_0_RpodBodySignalIPdu01"]
#         for j in range(0,4):
#             for angle in range(85, -1, -5):
#                 self.ipdu.set(getattr(self.ipdu.bodycan, angle_message[j]), angle_signal[j], angle)
#                 ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=3), 10103)
#                 for doorinfo in self.protoparse.get_vehicle_body_info(ble_bytes).doors:
#                     if doorinfo.id == j:
#                         door_info = doorinfo
#                 logger.info("Get dooropen angle: {0}".format(door_info))
#                 assert door_info.curAngle == angle

#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359797?projectId=46', name='蓝牙数据上报 1359797')
#     def test_door_postion_caseid_1359797(self):
#         position_message = ["DpodBodyFr01", "PpodBodyFr01", "LpodBodyFr01", "RpodBodyFr01"]
#         position_signal = ["DoorDrvrPercPosn", "DoorPassPercPosn", "DoorLeRePercPosn", "DoorRiRePercPosn"]
#         for j in range(0,4):
#             for position in range(0, 100, 10):
#                 self.ipdu.set(getattr(self.ipdu.bodycan, position_message[j]), position_signal[j], position)
#                 ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=1), 10103)
#                 for doorinfo in self.protoparse.get_vehicle_body_info(ble_bytes).doors:
#                     if doorinfo.id == j:
#                         door_info = doorinfo
#                 logger.info("Get dooropen position: {0}".format(door_info))
#                 assert door_info.id == j
#                 assert door_info.position == position

#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359769?projectId=46', name='蓝牙数据上报 1359769')
#     # def test_soc_caseid_1359769(self):
#     #     for soc in range(0, 1000, 50):
#     #         self.ipdu.propulsioncan_ecmpropfr04_disphvbattlvlofchrg_value(soc)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10105)
#     #         disp_soc = self.protoparse.get_position_info(ble_bytes).socInfo
#     #         logger.info("Get soc info: {0}".format(disp_soc))
#     #         assert disp_soc.displaySoc == soc*0.1
#     #     for soc in range(0, 2000, 100):
#     #         self.ipdu.propulsioncan_becmpropfr03_hvbattsoc_value(soc)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10105)
#     #         disp_soc = self.protoparse.get_position_info(ble_bytes).socInfo
#     #         logger.info("Get sco info: {0}".format(disp_soc))
#     #         assert disp_soc.realSoc == soc*0.05


#     # @pytest.mark.charge
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359786?projectId=46', name='蓝牙数据上报 1359786')
#     def test_totchrgegy_caseid_1359786(self):
#         for chrgegy in range(0, 2000, 100):
#             self.ipdu.propulsioncan_becmpropfr16_totchrgegy_value(chrgegy)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10107)
#             charg_info = self.protoparse.get_charging_info(ble_bytes).charging
#             logger.info("Get totchrgegy info: {0}".format(charg_info))
#             assert charg_info.totalChargeEgy == chrgegy

#     # @pytest.mark.charge
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359776?projectId=46', name='蓝牙数据上报 1359776')
#     def test_charggun_caseid_1359776(self):
#         for charggun_sts in range(0, 6):
#             self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15,"DCChrgnHndlSts", charggun_sts)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10107)
#             charg_info = self.protoparse.get_charging_info(ble_bytes).charging
#             logger.info("Get charggun status: {0}".format(charg_info))
#             assert charg_info.pluggerStatus == charggun_sts

#     #@pytest.mark.charge
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359784?projectId=46', name='蓝牙数据上报 1359784')
#     def test_chargpower_caseid_1359784(self):
#         self.ipdu.backbonefr_vddmbackbonefr16_chrgnordischrgnstsfb_chrgnsts2_supercharging()
#         for chargpower in range(0, 200, 50):
#             self.ipdu.propulsioncan_becmpropfr13_hvbattchrgnpwrcns1_value(chargpower)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10107)
#             charg_info = self.protoparse.get_charging_info(ble_bytes).charging
#             logger.info("Get chargpower status: {0}".format(charg_info))
#             assert charg_info.chargingPower == chargpower*100

#     # @pytest.mark.charge
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359781?projectId=46', name='蓝牙数据上报 1359781')
#     def test_chargcurrent_caseid_1359781(self):
#         for current in [0, 100, 1099, 1638, 1761, 2091, 2530, 2872, 3150, 3217, 3276]:
#             self.ipdu.propulsioncan_becmpropfr15_hvbattidc1_value(current)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10107)
#             batt_info = self.protoparse.get_charging_info(ble_bytes).batteryInfo
#             logger.info("Get chargpower status: {0}".format(batt_info))
#             assert round(batt_info.current,1) == current*0.1 - 1638

#     # @pytest.mark.charge
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359782?projectId=46', name='蓝牙数据上报 1359782')
#     def test_chargvoltage_caseid_1359782(self):
#         for voltage in [0, 123, 432, 243, 111, 333, 471, 500, 511]:
#             self.ipdu.propulsioncan_becmpropfr01_hvbattudc_value(voltage)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10107)
#             batt_info = self.protoparse.get_charging_info(ble_bytes).batteryInfo
#             logger.info("Get chargpower status: {0}".format(batt_info))
#             assert round(batt_info.voltage,2) == voltage*0.25

#     # # Not Ready
#     # def test_lowbattsoc(self):
#     #     for low_batt_soc in [0, 123, 432, 243, 111, 333, 471, 500, 511]:
#     #         self.ipdu.propulsioncan_becmpropfr01_hvbattudc_value(voltage)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#     #         batt_info = self.protoparse.get_charging_info(ble_bytes).batteryInfo
#     #         logger.info("Get chargpower status: {0}".format(batt_info))
#     #         assert round(batt_info.voltage,2) == voltage*0.25

#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359777?projectId=46', name='蓝牙数据上报 1359777')
#     def test_mirrorfolder_caseid_1359777(self):
#         for value in range(4, -1, -1):
#             self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'MirrFoldStsAtDrvr_0_DdmBodySignalIPdu01', value)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10103)
#             mirror_info = self.protoparse.get_vehicle_body_info(ble_bytes).outerRearView[1]
#             logger.info("Get mirror status: {0}".format(mirror_info))
#             assert mirror_info.id == 1
#             assert mirror_info.foldStatus == value
#         for value in range(4, -1, -1):
#             self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'MirrFoldStsAtPass_0_PdmBodySignalIPdu01', value)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10103)
#             mirror_info = self.protoparse.get_vehicle_body_info(ble_bytes).outerRearView[0]
#             logger.info("Get mirror status: {0}".format(mirror_info))
#             assert mirror_info.id == 0
#             assert mirror_info.foldStatus == value
 
#     # # Not Ready
#     # def test_target_soc(self):
#     #     for value in range(0, 101, 5):
#     #         logger.info("Set target soc: {0}".format(value))
#     #         self.ipdu.chassiscan1_vddmchas1fr34_localbookchrgntarval_value(value)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=6), 10107)
#     #         charg_info = self.protoparse.get_charging_info(ble_bytes).charging
#     #         logger.info("Get mirror status: {0}".format(charg_info))
#     #         # assert charg_info.chargeTargetSoc == value

#     #@pytest.mark.charge
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359774?projectId=46', name='蓝牙数据上报 1359774')
#     def test_estimated_charge_time_caseid_1359774(self):
#         for remain_t in range(2046, -1, -147):
#             self.ipdu.propulsioncan_becmpropfr21_hvbattchrgntiestimd_value(remain_t)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#             remain_charge_time = self.protoparse.get_charging_info(ble_bytes).charging.remainChargingTime
#             assert remain_charge_time == remain_t
#         self.ipdu.propulsioncan_becmpropfr21_hvbattchrgntiestimd_value(0)
#         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#         remain_charge_time = self.protoparse.get_charging_info(ble_bytes).charging.remainChargingTime
#         assert remain_charge_time == 0

#     @pytest.mark.xfail
#     #@pytest.mark.charge
#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359773?projectId=46', name='蓝牙数据上报 1359773')
#     def test_charge_speed_caseid_1359773(self):
#         for speed in range(65534, -1, -4351):
#             self.ipdu.chassiscan1_ecmchas1fr29_chrgnspd_1_bgmconnectivitysignalipdu03_value(speed)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#             charg_info = self.protoparse.get_charging_info(ble_bytes).charging
#             logger.info("Get mirror status: {0}".format(charg_info))
#             assert charg_info.chargingSpeed == speed


#     # # Not Ready
#     # def test_sunroof(self):
#     #     for value in range(100, -1, -5):
#     #         self.ipdu.cem_lin3_sigcem_lin3fr01_elecchromrooffb_0_sigcem_lin3signalipdu01_value(value)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10103)
#     #         sunroof_info = self.protoparse.get_vehicle_body_info(ble_bytes).sunroof
#     #         logger.info("Get mirror status: {0}".format(sunroof_info))
#     #         # assert sunroof. == speed


#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359816?projectId=46', name='蓝牙数据上报 1359816')
#     def test_block_10901_buttonstatus_rpafront_caseid_112063(self):
#         button = "RPAFront"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359817?projectId=46', name='蓝牙数据上报 1359817')
#     def test_block_10901_buttonstatus_rparear_caseid_112062(self):
#         button = "RPARear"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359818?projectId=46', name='蓝牙数据上报 1359818')
#     def test_block_10901_buttonstatus_rpaleftturn_caseid_112061(self):
#         button = "RPALeftTurn"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359819?projectId=46', name='蓝牙数据上报 1359819')
#     def test_block_10901_buttonstatus_rparightturn_caseid_112060(self):
#         button = "RPARightTurn"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i


#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359820?projectId=46', name='蓝牙数据上报 1359820')
#     def test_block_10901_buttonstatus_parkoutfrontleft_caseid_112059(self):
#         button = "parkOutFrontLeft"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i


#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359821?projectId=46', name='蓝牙数据上报 1359821')
#     def test_block_10901_buttonstatus_parkoutfrontright_caseid_112058(self):
#         button = "parkOutFrontRight"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359822?projectId=46', name='蓝牙数据上报 1359822')
#     def test_block_10901_buttonstatus_parkoutrearleft_caseid_112057(self):
#         button = "parkOutRearLeft"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359823?projectId=46', name='蓝牙数据上报 1359823')
#     def test_block_10901_buttonstatus_parkoutrearright_caseid_112056(self):
#         button = "parkOutRearRight"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359824?projectId=46', name='蓝牙数据上报 1359824')
#     def test_block_10901_buttonstatus_parkoutleftfront_caseid_112055(self):
#         button = "parkOutLeftFront"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359825?projectId=46', name='蓝牙数据上报 1359825')
#     def test_block_10901_buttonstatus_parkoutrightfront_caseid_112054(self):
#         button = "parkOutRightFront"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359826?projectId=46', name='蓝牙数据上报 1359826')
#     def test_block_10901_buttonstatus_parkoutfront_caseid_112053(self):
#         button = "parkOutFront"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359827?projectId=46', name='蓝牙数据上报 1359827')
#     def test_block_10901_buttonstatus_parkoutrear_caseid_112052(self):
#         button = "parkOutRear"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359828?projectId=46', name='蓝牙数据上报 1359828')
#     def test_block_10901_buttonstatus_button1_caseid_112051(self):
#         button = "button1"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359829?projectId=46', name='蓝牙数据上报 1359829')
#     def test_block_10901_buttonstatus_button2_caseid_112050(self):
#         button = "button2"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359830?projectId=46', name='蓝牙数据上报 1359830')
#     def test_block_10901_buttonstatus_button3_caseid_112049(self):
#         button = "button3"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i

#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359831?projectId=46', name='蓝牙数据上报 1359831')
#     def test_block_10901_buttonstatus_button4_caseid_112048(self):
#         button = "button4"
#         for i in [3, 2, 1, 0]:
#             self.avp_server.button_type[button] = i
#             self.avp_server.avpbutton_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             button_info = self.protoparse.get_avp_info(ble_bytes).button
#             assert getattr(button_info, button) == i


#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359832?projectId=46', name='蓝牙数据上报 1359832')
#     def test_block_10901_timercount_caseid_112047(self):
#         for counttime in [10, 20, 50, 100]:
#             self.avp_server.timer_count = counttime
#             self.avp_server.countdown_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             timecount = self.protoparse.get_avp_info(ble_bytes).timeCount
#             assert timecount == counttime

    
#     @pytest.mark.full
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359833?projectId=46', name='蓝牙数据上报 1359833')
#     def test_block_10901_parklotform_caseid_112046(self):
#         for parklotform in [2, 1, 0]:
#             self.avp_server.path_track["targetLotLocation"]["parkLotForm"] = parklotform
#             self.avp_server.planningpathtrack_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             parklottype = self.protoparse.get_avp_info(ble_bytes).parkLotType
#             assert parklottype == parklotform

    
#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359834?projectId=46', name='蓝牙数据上报 1359834')
#     def test_block_10901_pastatus_caseid_112045(self):
#         for pastatus in range(0, 14):
#             self.rpaapa_server.pa_remote_status["paStatus"] = pastatus
#             self.rpaapa_server.paremotestatus_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             paremotestatus = self.protoparse.get_avp_info(ble_bytes).paRemoteStatus
#             assert paremotestatus.paStatus == pastatus

#     @pytest.mark.sanity
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359835?projectId=46', name='蓝牙数据上报 1359835')
#     def test_block_10901_lasthandletype_caseid_1359835(self):
#         for lasthandletype in range(0, 4):
#             self.rpaapa_server.pa_remote_status["lastHandleType"] = lasthandletype
#             self.rpaapa_server.paremotestatus_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             paremotestatus = self.protoparse.get_avp_info(ble_bytes).paRemoteStatus
#             assert paremotestatus.lastHandleType == lasthandletype
    
    
#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359836?projectId=46', name='蓝牙数据上报 1359836')
#     def test_block_10901_lasthandleuid_caseid_112043(self):
#         for lasthandleuid in [0x12387566, 0x56782563, 0x4567345678]:
#             self.rpaapa_server.pa_remote_status["lastHandleUid"] = lasthandleuid
#             self.rpaapa_server.paremotestatus_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             paremotestatus = self.protoparse.get_avp_info(ble_bytes).paRemoteStatus
#             assert paremotestatus.lastHandleUid == lasthandleuid
    
    
#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359837?projectId=46', name='蓝牙数据上报 1359837')
#     def test_block_10901_remindersource_caseid_112042(self):
#         for source in range(4, -1, -1):
#             self.rpaapa_server.reminder["lastHandleType"] = source
#             self.rpaapa_server.aparemotereminder_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             reminder = self.protoparse.get_avp_info(ble_bytes).APARemoteReminder
#             assert reminder.source == source

#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359838?projectId=46', name='蓝牙数据上报 1359838')
#     def test_block_10901_remindertype_caseid_112041(self):
#         for type in range(16, -1, -1):
#             self.rpaapa_server.reminder["type"] = type
#             self.rpaapa_server.aparemotereminder_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             reminder = self.protoparse.get_avp_info(ble_bytes).APARemoteReminder
#             assert reminder.type == type

    
    
#     @pytest.mark.smoke
#     @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359839?projectId=46', name='蓝牙数据上报 1359839')
#     def test_block_10901_direction_caseid_112040(self):
#         for direction in range(2, -1, -1):
#             self.rpaapa_server.direction = direction
#             self.rpaapa_server.parkinglotdirection_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 19001)
#             parkdirection = self.protoparse.get_avp_info(ble_bytes).direction
#             assert parkdirection == direction

#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359760?projectId=46', name='蓝牙数据上报 1359760')
#     # def test_block_10103_tyre_pressure_fl_caseid_1359760(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_pressure = {"id": 0, "pressure": 200}
#     #     pres = 0.1
#     #     while pres < 350.115:
#     #         # tyre_pressure["pressure"] = pres
#     #         # self.tyre_server.pressure_info = tyre_pressure
#     #         # self.tyre_server.tyrepress_event_send()
#     #         self.tpms.set_pressure(1, pres)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 0:
#     #                 tyre_fl = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_fl))
#     #         assert round(tyre_fl.pressure, 1) == pres
#     #         pres = round(pres + 55.1, 1)

#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359761?projectId=46', name='蓝牙数据上报 1359761')
#     # def test_block_10103_tyre_pressure_fr_caseid_1359761(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_pressure = {"id": 1, "pressure": 200}
#     #     pres = 0.1
#     #     while pres < 350.115:
#     #         # tyre_pressure["pressure"] = pres
#     #         # self.tyre_server.pressure_info = tyre_pressure
#     #         # self.tyre_server.tyrepress_event_send()
#     #         self.tpms.set_pressure(2, pres)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=4), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 1:
#     #                 tyre_fr = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_fr))
#     #         assert round(tyre_fr.pressure, 1) == pres
#     #         pres = round(pres + 49.1, 1)

#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359762?projectId=46', name='蓝牙数据上报 1359762')
#     # def test_block_10103_tyre_pressure_rl_caseid_1359762(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_pressure = {"id": 2, "pressure": 200}
#     #     pres = 0.1
#     #     while pres < 350.115:
#     #         # tyre_pressure["pressure"] = pres
#     #         # self.tyre_server.pressure_info = tyre_pressure
#     #         # self.tyre_server.tyrepress_event_send()
#     #         self.tpms.set_pressure(3, pres)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 2:
#     #                 tyre_rl = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_rl))
#     #         assert round(tyre_rl.pressure, 1) == pres
#     #         pres = round(pres + 63.1, 1)

#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359763?projectId=46', name='蓝牙数据上报 1359763')
#     # def test_block_10103_tyre_pressure_rr_caseid_1359763(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_pressure = {"id": 3, "pressure": 200}
#     #     pres = 0.1
#     #     while pres < 350.115:
#     #         # tyre_pressure["pressure"] = pres
#     #         # self.tyre_server.pressure_info = tyre_pressure
#     #         # self.tyre_server.tyrepress_event_send()
#     #         self.tpms.set_pressure(4, pres)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 3:
#     #                 tyre_rr = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_rr))
#     #         assert round(tyre_rr.pressure, 1) == pres
#     #         pres = round(pres + 50.1, 1)
            
#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359764?projectId=46', name='蓝牙数据上报 1359764')
#     # def test_block_10103_tyre_temperature_fl_caseid_1359764(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_temp = {"id": 0, "temperature": 200}
#     #     temp = 1
#     #     while temp < 205:
#     #         # tyre_temp["temperature"] = temp
#     #         # self.tyre_server.temp_info = tyre_temp
#     #         # self.tyre_server.tyretemp_event_send()
#     #         self.tpms.set_temperature(1, temp)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 0:
#     #                 tyre_fl = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_fl))
#     #         assert tyre_fl.temperature == temp
#     #         temp = temp + 57

#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359765?projectId=46', name='蓝牙数据上报 1359765')
#     # def test_block_10103_tyre_temperature_fr_caseid_1359765(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_temp = {"id": 1, "temperature": 200}
#     #     temp = 1
#     #     while temp < 205:
#     #         # tyre_temp["temperature"] = temp
#     #         # self.tyre_server.temp_info = tyre_temp
#     #         # self.tyre_server.tyretemp_event_send()
#     #         self.tpms.set_temperature(2, temp)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 1:
#     #                 tyre_fr = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_fr))
#     #         assert tyre_fr.temperature == temp
#     #         temp = temp + 49

#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359766?projectId=46', name='蓝牙数据上报 1359766')
#     # def test_block_10103_tyre_temperature_rl_caseid_1359766(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_temp = {"id": 2, "temperature": 200}
#     #     temp = 1
#     #     while temp < 205:
#     #         # tyre_temp["temperature"] = temp
#     #         # self.tyre_server.temp_info = tyre_temp
#     #         # self.tyre_server.tyretemp_event_send()
#     #         self.tpms.set_temperature(3, temp)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 2:
#     #                 tyre_rl = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_rl))
#     #         assert tyre_rl.temperature == temp
#     #         temp = temp + 63

#     # @pytest.mark.tyre
#     # @pytest.mark.sanity
#     # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359767?projectId=46', name='蓝牙数据上报 1359767')
#     # def test_block_10103_tyre_temperature_rr_caseid_1359767(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgtqf_0_bcmvddmbackbonesignalipdu06_genqf1_accurdata()  # 车速Qf
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgt_0_bcmvddmbackbonesignalipdu06_ub_value(1)  # 车速UB
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(36.0)
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     self.sd_tester.change_usage_mode(0xD)
#     #     tyre_temp = {"id": 3, "temperature": 200}
#     #     temp = 1
#     #     while temp < 205:
#     #         # tyre_temp["temperature"] = temp
#     #         # self.tyre_server.temp_info = tyre_temp
#     #         # self.tyre_server.tyretemp_event_send()
#     #         self.tpms.set_temperature(4, temp)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10103)
#     #         tyre_info = self.protoparse.get_vehicle_body_info(ble_bytes).tire
#     #         for tyre in tyre_info:
#     #             if tyre.id == 3:
#     #                 tyre_rr = tyre
#     #                 break
#     #         logger.info("Get tyre info: {0}".format(tyre_rr))
#     #         assert tyre_rr.temperature == temp
#     #         temp = temp + 51

  
#     # @pytest.mark.soh
#     # @pytest.mark.sanity
#     # def test_lowbatt_soc_soh_caseid_1359789(self):
#     #     for soc in range(1000, -1, -50):
#     #         self.ipdu.connectivitycanfd_bgmconnectivityfr06_battsocraw2_value(soc)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#     #         lowbatt_info = self.protoparse.get_charging_info(ble_bytes).batteryInfo
#     #         assert lowbatt_info.calculatedSoc == soc
#     #     for soh in range(1000, -1, -50):
#     #         self.ipdu.connectivitycanfd_bgmconnectivityfr06_battsohraw2_value(soc)
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#     #         lowbatt_info = self.protoparse.get_charging_info(ble_bytes).batteryInfo
#     #         assert lowbatt_info.calculatedSoh == soh

#     #@pytest.mark.account
#     @pytest.mark.sanity
#     def test_account_info_uid_caseid_1502896(self):
#         for uid in [0x01, 0x02, 0x03, 0x04, 0x1020]:
#             self.account_server.accountsts["uid"] = uid
#             self.account_server.account_event_send()
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10109)
#             account_info = self.protoparse.get_function_info(ble_bytes).accountInfo
#             assert account_info.uid == uid

    # @pytest.mark.account
    # @pytest.mark.sanity
    # def test_account_info_loginsts_caseid_1502895(self):
    #     self.account_server.loginsts = 0
    #     self.account_server.account_event_send()
    #     ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10109)
    #     account_info = self.protoparse.get_function_info(ble_bytes).accountInfo
    #     assert account_info.loginStatus == 0
    #     self.account_server.loginsts = 1
    #     self.account_server.account_event_send()
    #     ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=5), 10109)
    #     account_info = self.protoparse.get_function_info(ble_bytes).accountInfo
    #     assert account_info.loginStatus == 1

#     #@pytest.mark.charge
#     @pytest.mark.sanity
#     def test_charge_state_caseid_1359772(self):
#         for chrgsts in range(30, -1, -1):
#             if chrgsts in [13, 16, 17]:
#                 continue
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr16, 'ChrgnOrDisChrgnStsFb', chrgsts)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#             charg_sts = self.protoparse.get_charging_info(ble_bytes).charging.chargingStatus
#             assert charg_sts == chrgsts

#     #@pytest.mark.charge
#     @pytest.mark.sanity
#     def test_charge_setimated_remaintime_caseid_1359774(self):
#         for remain_t in range(204, -1, -147):
#             self.ipdu.propulsioncan_becmpropfr21_hvbattchrgntiestimd_value(remain_t)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#             remain_charge_time = self.protoparse.get_charging_info(ble_bytes).charging.remainChargingTime
#             assert remain_charge_time == remain_t
#         self.ipdu.propulsioncan_becmpropfr21_hvbattchrgntiestimd_value(0)
#         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#         remain_charge_time = self.protoparse.get_charging_info(ble_bytes).charging.remainChargingTime
#         assert remain_charge_time == 0


#     # @pytest.mark.full
#     # def test_central_lock_status_caseid_1359749(self):
#     #     for lock_cmd in range(3,-1,-1):
#     #         self.centrallock_client.lock_cmd = lock_cmd
#     #         self.centrallock_client.lock_request_send()
#     #         logger.info("Send lock request")
#     #         ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10103)
#     #         lock_info = self.protoparse.get_vehicle_body_info(ble_bytes).centralLock
#     #         logger.info("Get central lock status: {0}".format(lock_info))
#     #         assert lock_info == lock_cmd
#     #         time.sleep(1)


#     # # Not ready
#     # @pytest.mark.equipmenttype
#     # def test_block_10107_equipment_info(self):
#     #     jidu_flg = [0x20,0,0,0,0,0,0,0]
#     #     chrg_pile = [0,0,0x20,0,0,0,0,0]
#     #     for chgrflg in [0x60, 0xA0, 0xE0]:
#     #         jidu_flg[0] = chgrflg
#     #         # self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr02, 'JIDUChgrFlg', chgrflg)
#     #         self.ipdu.send_pdu("propulsioncan", 0X175, jidu_flg, cycle_time=0.5)
#     #         for i in [0x60, 0xA0, 0xE0]:
#     #             # self.ipdu.set(self.ipdu.connectivitycanfd.BncmBsrmConnectivityFr03, 'ChrgrPileInfo', i)
#     #             chrg_pile[2] = i
#     #             self.ipdu.send_pdu("connectivitycanfd", 0X177, chrg_pile, cycle_time=0.5)
#     #             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=6), 10107)
#     #             equipment_info = self.protoparse.get_charging_info(ble_bytes).charging.equipmentInfo
#     #             logger.info("Get tyre info: {0}".format(equipment_info))
#     #             # assert tyre_info.temperature == temp

#     #@pytest.mark.current
#     @pytest.mark.full
#     def test_max_current_caseid_1359781(self):
#         for j in range(20000, -1, -440):
#             self.ipdu.propulsioncan_becmpropfr31_dcchrgrimax_value(j)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#             equipment_info = self.protoparse.get_charging_info(ble_bytes).charging.equipmentInfo
#             logger.info("Get charging info: {0}".format(equipment_info))
#             assert equipment_info.maxCurrent == j*0.1-1638

#         for i in range(20000, -1, -440):
#             self.ipdu.propulsioncan_becmpropfr22_chrgequipidc_value(i)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#             equipment_info = self.protoparse.get_charging_info(ble_bytes).charging.equipmentInfo
#             logger.info("Get charging info: {0}".format(equipment_info))
#             assert equipment_info.actualCurrent == i*0.1-1638

#     # @pytest.mark.chargelid
#     # @pytest.mark.full
#     # def test_chargelid_caseid_1359771(self):
#     #     self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#     #     self.sd_tester.update_serverdoipid(0x1002)
#     #     time.sleep(1)
#     #     logger.info(self.sd_tester.change_usage_mode(11, do_assert=True))
#     #     self.ipdu.cem_lin2_ecmecm_lin4fr02_chrglidrearsts_1_ecmecm_lin4signalipdu02_doorsts2_clsd()
#     #     ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#     #     chargelid = self.protoparse.get_charging_info(ble_bytes).charging.lidStatus
#     #     logger.info("Get chargelid info: {0}".format(chargelid))
#     #     assert chargelid == 1
#     #     self.ipdu.cem_lin2_ecmecm_lin4fr02_chrglidrearsts_1_ecmecm_lin4signalipdu02_doorsts2_opend()
#     #     ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#     #     chargelid = self.protoparse.get_charging_info(ble_bytes).charging.lidStatus
#     #     logger.info("Get chargelid info: {0}".format(chargelid))
#     #     assert chargelid == 2
#     #     self.ipdu.cem_lin2_ecmecm_lin4fr02_chrglidrearsts_1_ecmecm_lin4signalipdu02_doorsts2_ukwn()
#     #     ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=2), 10107)
#     #     chargelid = self.protoparse.get_charging_info(ble_bytes).charging.lidStatus
#     #     logger.info("Get chargelid info: {0}".format(chargelid))
#     #     assert chargelid == -1
#     #     logger.info(self.sd_tester.change_usage_mode(11, do_assert=True))

#     #@pytest.mark.maxsoc
#     @pytest.mark.full
#     def test_max_soc_caseid_1359775(self):
#         for soc in range(1000, -1, -100):
#             self.ipdu.chassiscan1_ecmchas1fr13_bookchrgntarvalfb_1_bgmconnectivitysignalipdu10_value(soc)
#             ble_bytes = self.get_ble_bytes(self.bletp.get_bletp(timeout=3), 10107)
#             maxsoc = self.protoparse.get_charging_info(ble_bytes).charging.chargeTargetSoc
#             logger.info("Get charging info: {0}".format(maxsoc))
#             assert maxsoc == soc*0.1

