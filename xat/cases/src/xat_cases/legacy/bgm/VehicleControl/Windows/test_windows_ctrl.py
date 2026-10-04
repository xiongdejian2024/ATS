# # -*- coding:utf-8 -*-
# """
# @File        :test_window_ctrl.py
# @Author      :hui.zhao@jiduatuo.com
# @Time        :2023/06/16 11:00 AM
# @Description :Test body control test case about window
# """

# import os
# import sys
# from time import sleep
# import pytest
# import allure

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../../.."))

# from test_case.bgm.case_helper.test_base import TestBase
# from test_case.bgm.s2s.case_helper.S2S_can_sim import *
# from ecu_simulator.common.logger import logger
# from ecu_simulator.ecu_sim.sd_tester import Sd_Tester
# from ecu_simulator.soa_partner.src.base_partner import *
# from test_case.bgm.VehicleControl.case_helper.common_lib_bgm import *
# from test_case.bgm.VehicleControl.case_helper.parse_excel_bgm import *
# from ecu_simulator.sdk.digital_key.digital_key_class import DigitalKey
# from test_case.bgm.case_helper.environment_check import partner_process_check
# from ecu_simulator.sdk.digital_key.digital_key_const import *
# from test_case.bgm.case_helper.bgm_case_helper.common_interface import *
# from test_case.bgm.case_helper.bgm_case_helper.data_drive_lib import *


# conf_file_name = r"testcase_config_bodyctrl_window.xlsx"
# service_name_type = ("WindowService", "client")
# service_name_type_key = ("KeyService", "client")
# service_name_type_lock = ("CentralLockService", "client")
# service_name_type_reset = ("ResetSOAConfigService", "client")
# service_name_type_winapp = ("WindowAppService", "client")
# CENTRALLOCK_SERVICE_CLIENT = "CentralLockService_client"

# global case_list_full
# global case_id_list_full
# global case_list_smoke
# global case_id_list_smoke
# case_list_full, case_id_list_full = get_testconfig_by_read_excel(
#     conf_file_name, "window"
# )
# case_list_smoke, case_id_list_smoke = get_testconfig_by_read_excel(
#     conf_file_name, "smoke"
# )


# @allure.feature("车身网关测试/整车控制")
# @allure.story("窗户控制")
# @pytest.mark.run(order=1)
# class TestWindowCtrl(TestBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         global case_list_full
#         global case_id_list_full

#         self.sd_tester = Sd_Tester(**self.tc_config)
#         self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

#         self.sd_tester.update_serverdoipid(0x1002)
#         sleep(0.5)
#         self.sd_tester.diagnostic_client_sim_start()
#         sleep(0.5)
#         self.sd_tester.tester_present()
#         sleep(0.5)

#         with allure.step("Test Class Pre Step can_lin_fr 启动"):
#             self.ipdu.start_all_time_control()  # 启动数据模拟(数据库周期性报文和调度表)
#             self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动,总线开始收发报文

#         # 为了防止诊断反馈NRC22,需要发送FlexRay报文
#         self.ipdu.set_vehspd(0.0)
#         sleep(1)
#         self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#         self.ipdu.set(
#             self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0
#         )

#         sleep(1)

#         # 检查上位机上是否有其它未关闭的soa_partner进程在运行,如果有,则杀死进程
#         partner_process_check()
#         sleep(1)

#         # 启动partner operator
#         self.partner = S2sBaseClass(
#             [
#                 service_name_type,
#                 service_name_type_key,
#                 service_name_type_lock,
#                 service_name_type_reset,
#                 service_name_type_winapp,
#             ]
#         )
#         sleep(2)
#         self.partner.send_method_request(
#             "WindowService_client", "SetRainAutoCloseWindow", {"isOn": True}
#         )
#         sleep(1)
#         self.com_lib = CommonInterface(
#             self.tc_config,
#             self.ipdu,
#             self.busapp,
#             self.nucapp,
#             self.dk,
#             self.io,
#             self.sd_tester,
#             self.partner,
#         )
#         self.data_drive_lib = DataDriveInterface(
#             self.tc_config,
#             self.ipdu,
#             self.io,
#             self.sd_tester,
#             self.partner,
#             conf_file_name,
#             service_name_type,
#         )

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)
#         self.sd_tester.change_usage_mode(1, do_assert=False)
#         sleep(0.1)
#         self.sd_tester.change_car_mode(0, do_assert=False)
#         sleep(0.1)
#         self.partner.send_method_request(
#             "KeyService_client", "SetConfigInfo", {"infos": [{"key": 4, "value": 1}]}
#         )
#         sleep(0.1)
#         self.partner.empty_all()
#         sleep(1)

#     def after_each_func(self, ecu):
#         self.ipdu.set_vehspd(0.0)
#         self.sd_tester.change_usage_mode(1, do_assert=False)
#         sleep(0.1)
#         self.sd_tester.change_car_mode(0, do_assert=False)
#         sleep(0.1)
#         self.ipdu.resume_all_bus_send()
#         sleep(0.1)
#         self.ipdu.reset_check_results()
#         sleep(0.1)
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         self.sd_tester.change_usage_mode(1)
#         self.sd_tester.change_car_mode(0)
#         self.ipdu.time_control_stop()  # 停止数据模拟(数据库周期性报文和调度表)
#         self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动,总线开始收发报文
#         sleep(0.5)
#         self.sd_tester.stop_tester_present()
#         sleep(0.5)
#         self.sd_tester.diagnostic_client_sim_close()
#         sleep(0.5)
#         self.partner.stop_operators()
#         sleep(0.5)
#         sleep(0.5)
#         super().after_class(self, ecu)

#     def five_door_close(self):
#         self.io.pass_door_close()
#         self.io.drvr_door_close()
#         self.io.lere_door_close()
#         self.io.rire_door_close()
#         self.io.trunk_door_close()

#     def set_centrllock_pre_condition(self):
#         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, "GearLvrIndcn", 0)
#         sleep(0.1)
#         self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#         sleep(0.1)
#         self.ipdu.pause_bus_send("chassiscan1")
#         self.ipdu.pause_bus_send("chassiscan2")
#         self.ipdu.pause_bus_send("passivesafetycan")
#         self.ipdu.pause_ecu_send("connectivitycanfd", "DRMFL")
#         self.ipdu.pause_ecu_send("connectivitycanfd", "DRMFR")
#         self.ipdu.pause_ecu_send("connectivitycanfd", "DRMRL")
#         self.ipdu.pause_ecu_send("connectivitycanfd", "DRMRR")
#         self.ipdu.pause_ecu_send("connectivitycanfd", "TCAM")
#         self.ipdu.stop_send_pdu("connectivitycanfd", 0x10)
#         self.ipdu.stop_send_pdu("connectivitycanfd", 0x40)
#         sleep(0.1)
#         self.dk.set_pass_seat_notpresent()
#         self.dk.set_secle_seat_notpresent()
#         self.dk.set_secmid_seat_notpresent()
#         self.dk.set_secri_seat_notpresent()
#         self.dk.reset_bncm_digital_keyinfo()
#         sleep(0.1)
#         self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
#         sleep(0.1)
#         self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
#         sleep(1)
#         self.set_5_door_lock_status("unlock")
#         self.dk.set_cenlock_sts(0x1)
#         sleep(0.1)

#     def set_5_door_lock_status(self, status):
#         logger.info("设置5门锁的状态为{}".format(status))
#         if status == "lock":
#             self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", 3)
#             self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", 3)
#             self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", 3)
#             self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", 3)
#             self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "TrOpenerSts", 1)
#         elif status == "unlock":
#             self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, "DoorDrvrLockSts", 1)
#             self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, "DoorPassLockSts", 1)
#             self.ipdu.set(self.ipdu.bodycan.RldmBodyFr01, "DoorLeReLockSts", 1)
#             self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr01, "DoorRiReLockSts", 1)
#             self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, "TrOpenerSts", 1)

#     def send_close_win_dueto_rain(self):
#         with allure.step("通过NFC锁车，确保车辆进入防盗状态"):
#             logger.info("通过NFC锁车，确保车辆进入防盗状态")
#             self.set_centrllock_pre_condition()
#             self.dk.set_cenlock_sts(1)
#             sleep(1)
#             self.dk.send_nfc_cmd()
#             sleep(1)
#             self.dk.ck_cenlock_sts(3)
#             sleep(2)
#         with allure.step("发送检测到下雨的请求"):
#             self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr03, "RainDetected", 1)

#     def trigger_outside_switch(self):
#         with allure.step(f"Step:按下门内外关然后释放"):
#             self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrOpenReqOutdSwt2", 1)
#             self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, "DoorDrvrOpenReqOutdSwt3", 1)
#             self.io.drvr_door_outswitch_pressed()
#             sleep(1)
#             self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrOpenReqOutdSwt2", 2)
#             self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, "DoorDrvrOpenReqOutdSwt3", 0)
#             self.io.drvr_door_outswitch_unpressed()

#     def check_win_req(self, check_dic):
#         check_list = []
#         target_msg = self.ipdu.bodycan.CemBodyFr68
#         if "drv" in check_dic.keys():
#             check_list.append((target_msg, "WinOpenDrvrReq", check_dic["drv"]))
#         if "pass" in check_dic.keys():
#             check_list.append((target_msg, "WinOpenPassReq", check_dic["pass"]))
#         if "rl" in check_dic.keys():
#             check_list.append((target_msg, "WinOpenReLeReq", check_dic["rl"]))
#         if "rr" in check_dic.keys():
#             check_list.append((target_msg, "WinOpenReRiReq", check_dic["rr"]))
#         self.ipdu.check_multiple_signals(check_list, timeout=1)
#         self.ipdu.reset_check_results()
#         sleep(1)

#     def check_signal_value(self, check_obj, check_type="Positive"):
#         target_msg = check_obj[0]
#         check_signal = check_obj[1]
#         check_value = check_obj[2]
#         result_ori = self.ipdu.check_signal(target_msg, check_signal, timeout=1)
#         logger.info("result_original {}".format(result_ori))
#         result = get_signal_times_interval(result_ori, check_value)
#         logger.info("result:{}".format(result))
#         if check_type == "Negtive":
#             if result[0] == 0:
#                 assert True
#             else:
#                 assert False
#         else:
#             if result[0] != 0:
#                 assert True
#             else:
#                 assert False
#         self.ipdu.reset_check_results()

#     def win_test_basic(
#         self,
#         win_pre_pos,
#         trigger_method,
#         check_win_req,
#         act_time_interval="NA",
#         win_pos_after_trigger=(1, 1, 1, 1),
#         check_win_short_drop_req="NA",
#         check_win_short_drop_pos={"drv": 26, "pass": 26, "rl": 26, "rr": 26},
#     ):
#         self.set_centrllock_pre_condition()
#         self.dk.set_window_position(
#             win_pre_pos[0], win_pre_pos[1], win_pre_pos[2], win_pre_pos[3]
#         )
#         sleep(1)
#         with allure.step("触发:{}".format(trigger_method)):
#             if trigger_method == "Rain":
#                 logger.info("模拟雨天触发关窗")
#                 self.send_close_win_dueto_rain()
#             elif trigger_method == "NFC":
#                 logger.info("发送NFC闭锁请求")
#                 self.dk.send_nfc_cmd()
#             elif trigger_method == "OutSwitch":
#                 logger.info("发送门外开关触发闭锁请求")
#                 self.trigger_outside_switch()
#             elif trigger_method == "WalkAway":
#                 logger.info("离车触发闭锁请求")
#                 self.sd_tester.write_multi_ccp({94: 0x8})
#                 self.partner.send_method_request(
#                     "KeyService_client",
#                     "SetConfigInfo",
#                     {"infos": [{"key": 0, "value": 2}]},
#                 )
#                 sleep(1)
#                 self.dk.send_walk_away_lock_cmd()
#             elif trigger_method == "RKE":
#                 logger.info("蓝牙触发闭锁请求")
#                 self.partner.send_method_request(
#                     CENTRALLOCK_SERVICE_CLIENT,
#                     "SetDoorCloseLock",
#                     {"cmd": 1, "source": 0},
#                 )
#             elif trigger_method == "Telm":
#                 logger.info("远控触发闭锁请求")
#                 self.partner.send_method_request(
#                     CENTRALLOCK_SERVICE_CLIENT,
#                     "SetDoorCloseLock",
#                     {"cmd": 1, "source": 1},
#                 )

#         if check_win_short_drop_req == "No":
#             self.start_thread_check_win_request(
#                 check_win_short_drop_pos, check_type="Negtive"
#             )
#         elif check_win_short_drop_req == "Yes":
#             self.start_thread_check_win_request(check_win_short_drop_pos)

#         if act_time_interval != "NA":
#             sleep(act_time_interval)
#             self.dk.set_window_position(
#                 win_pos_after_trigger[0],
#                 win_pos_after_trigger[1],
#                 win_pos_after_trigger[2],
#                 win_pos_after_trigger[3],
#             )

#         self.check_win_req(check_win_req)
#         sleep(3)

#     def start_thread_check_win_request(self, check_dic, check_type="Positive"):
#         target_msg = self.ipdu.bodycan.CemBodyFr68
#         if "drv" in check_dic.keys():
#             check_obj = (target_msg, "WinOpenDrvrReq", check_dic["drv"])
#             thread_1 = Thread(
#                 target=self.check_signal_value,
#                 args=(check_obj, check_type),
#             )
#             thread_1.start()
#         if "pass" in check_dic.keys():
#             check_obj = (target_msg, "WinOpenPassReq", check_dic["pass"])
#             thread_2 = Thread(
#                 target=self.check_signal_value,
#                 args=(check_obj, check_type),
#             )
#             thread_2.start()
#         if "rl" in check_dic.keys():
#             check_obj = (target_msg, "WinOpenReLeReq", check_dic["rl"])
#             thread_3 = Thread(
#                 target=self.check_signal_value,
#                 args=(check_obj, check_type),
#             )
#             thread_3.start()
#         if "rr" in check_dic.keys():
#             check_obj = (target_msg, "WinOpenReRiReq", check_dic["rr"])
#             thread_4 = Thread(
#                 target=self.check_signal_value,
#                 args=(check_obj, check_type),
#             )
#             thread_4.start()

#     def check_signal_always_is(self, mes, signal, value):
#         result_ori = self.ipdu.check_signal(mes, signal, timeout=5)
#         logger.info("result_original {}".format(result_ori))
#         result = check_all_value_is(result_ori, value)
#         logger.info("result:{}".format(result))
#         assert result
#         self.ipdu.reset_check_results()

#     @pytest.mark.smoke
#     @pytest.mark.data_dri
#     @pytest.mark.parametrize("test_case", case_list_smoke, ids=case_id_list_smoke)
#     def test_window_ctrl_smoke_case(self, test_case):
#         self.data_drive_lib.test_data_drive_case(test_case)

#     @pytest.mark.full
#     @pytest.mark.flaky(reruns=3, reruns_delay=2)
#     @pytest.mark.parametrize("test_case", case_list_full, ids=case_id_list_full)
#     def test_window_ctrl_full_case(self, test_case):
#         self.data_drive_lib.test_data_drive_case(test_case)

#     @allure.title("HMI单独控制主驾驶窗户打开100%(CarMode=Normal、UsageMode=Convenience)")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/118258?projectId=46",
#         name="窗户控制测试case:118258",
#     )
#     @pytest.mark.smoke
#     # @pytest.mark.flaky(reruns=3, reruns_delay=2)
#     def test_window_ctrl_caseid_118258(self):
#         with allure.step(f"Step:设置初始条件"):
#             self.com_lib.set_common_precontion(usage_mode=2)
#             self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
#             sleep(1)

#         self.com_lib.send_s2s_request_and_check(
#             ("WindowService", "SetPosition", {"windows": [{"id": 0, "position": 100}]}),
#             check_signal_parameter=("bodycan.CemBodyFr68", "WinOpenDrvrReq", 26),
#         )
#         sleep(3)

#     @allure.title("HMI单独控制主驾驶窗户打开4%(CarMode=Normal、UsageMode=Convenience)")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/118263?projectId=46",
#         name="窗户控制测试case:118263",
#     )
#     @pytest.mark.smoke
#     @pytest.mark.verify
#     def test_window_ctrl_caseid_118263(self):
#         with allure.step(f"Step:设置初始条件"):
#             self.com_lib.set_common_precontion(usage_mode=2)
#             self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
#             sleep(1)
#         self.com_lib.send_s2s_request_and_check(
#             ("WindowService", "SetPosition", {"windows": [{"id": 0, "position": 4}]}),
#             check_signal_parameter=("bodycan.CemBodyFr68", "WinOpenDrvrReq", 2),
#         )
#         sleep(3)

 
#     @allure.title("验证按下车外副驶位门开关窗户会自动短降")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/119283?projectId=46"
#     )
#     @pytest.mark.full
#     def test_caseid_119283(self):
#         with allure.step(f"Step:设置初始条件"):
#             logger.info("设置CCP#561=02")
#             ccp_val = self.sd_tester.make_ccp_according_id_and_data("561", "02")
#             self.sd_tester.write_ccp(ccp_val)
#             sleep(0.2)
#             self.dk.set_window_position(0x1, 0x1, 0x1, 0x1)
#         sleep(0.5)
#         with allure.step(f"Step:设置DoorPassLockSts状态为unlock"):
#             self.ipdu.set(
#                 self.ipdu.bodycan.PdmBodyFr01,
#                 "DoorPassLockSts",
#                 1,
#             )
#         sleep(3)

#         with allure.step(f"Step:按下门内开关然后释放"):
#             self.ipdu.set(
#                 self.ipdu.bodycan.PpodBodyFr01,
#                 "DoorPassOpenReqOutdSwt2",
#                 1,
#             )
#             self.ipdu.set(
#                 self.ipdu.bodycan.IpmBodyFr01,
#                 "DoorPassOpenReqOutdSwt3",
#                 1,
#             )
#             self.io.pass_door_outswitch_pressed()
#             sleep(1)
#             self.ipdu.set(
#                 self.ipdu.bodycan.PpodBodyFr01,
#                 "DoorPassOpenReqOutdSwt2",
#                 2,
#             )
#             self.ipdu.set(self.ipdu.bodycan.IpmBodyFr01, "DoorPassOpenReqOutdSwt3", 0)
#             self.io.pass_door_outswitch_unpressed()
#         with allure.step(f"Step:Check BGM 发送 500 ms ShortDropWinPassDoor=2然后恢复到0"):
#             result_ori = self.ipdu.check_signal(
#                 self.ipdu.bodycan.CemBodyFr103, "ShortDropWinPassDoor", timeout=5
#             )
#             logger.info("result_original {}".format(result_ori))
#             result = get_signal_times_interval(result_ori, 2)
#             logger.info("result:{}".format(result))
#             if result[1] != 0:
#                 assert True
#             else:
#                 assert False
#             self.ipdu.reset_check_results()
#         sleep(3)

    
   