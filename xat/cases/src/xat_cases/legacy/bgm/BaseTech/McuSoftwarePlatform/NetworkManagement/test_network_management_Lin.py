# # -*- coding: utf-8 -*-
# """
# @File        : test_example_can_lin_fr.py
# @Author      : shulin.yang@jiduatuo.com
# @Time        : 2023/01/10 18:00 PM
# @Description : description about this file
# @Examples    : example of how to use it
# """

# import os
# import sys
# import time
# from time import sleep

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))
# from test_case.bgm.case_helper.test_base import TestBase
# import pytest
# import allure
# import threading
# from ecu_simulator.common.logger import logger
# from ecu_simulator.sdk.bus_app import BusApp
# from ecu_simulator.sdk.i_signal_i_pdu import ISignalIPdu
# from ecu_simulator.ecu_sim.sd_tester import Sd_Tester
# from ecu_simulator.soa_partner.src.base_partner import *
# from test_case.bgm.VehicleControl.case_helper.common_lib_bgm import *
# from test_case.bgm.VehicleControl.case_helper.parse_excel_bgm import *
# from ecu_simulator.sdk.digital_key.digital_key_class import DigitalKey


# @allure.feature("网络管理")
# @allure.story("网络PNC路由测试")
# class TestExample(TestBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
        
#         self.sd_tester = Sd_Tester(**self.tc_config)
#         self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
#         self.sd_tester.diagnostic_client_sim_start()
#         # self.partner = S2sBaseClass([("VehicleModeService", "client"), ("SteerWheelService", "client"),("ChargeLidService", "client"),("VehicleSetStatusService", "client")])
#         self.sd_tester.tester_present()
#         sleep(0.5)
#         self.sd_tester.update_serverdoipid(0x1002)
        
#         with allure.step(f"Test Class Pre Step can_lin_fr 启动"):
#             self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
#             self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
        
#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)
#         self.ipdu.reset_check_results()
#         self.sd_tester.change_car_mode(0, do_assert=1)
#         # Code Location

#     def after_each_func(self, ecu):
#         # Code Location
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         # Code Location
#         self.sd_tester.stop_tester_present()
#         sleep(0.5)
#         self.sd_tester.diagnostic_client_sim_close()
#         with allure.step(f"Test Class clearup Step can_lin_fr 停止"):
#             self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）\
#             self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
#         super().after_class(self, ecu)

#     def start_thread_check_signal(self,msg_obj,signal,observe_time):
#         self.ipdu.check_signal(msg_obj,signal,observe_time)
    
    
#     @allure.title("LIN1 Abandoned 切换Convenience 唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109663?projectId=46',
#         name='Can_Lin Pdu Case Example 109663',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109663(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(15)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠"):
#             logger.info("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'IntrMirrCmdDrvrSide',timeout=12)
            
        
#         with allure.step("切换UsageMode到Convenience"):
#             logger.info("切换UsageMode到Convenience")
#             self.sd_tester.change_usage_mode(2, do_assert=1)
        
#         with allure.step("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠"):
#             logger.info("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('IntrMirrCmdDrvrSide',timeout=24)
            
#             logger.info("result_original_1(IntrMirrCmdDrvrSide){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, [0,1]):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:LIN1FR01:IntrMirrCmdDrvrSide=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-12)<=0.8:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的IntrMirrCmdDrvrSide值为1")
#                     assert False       
#         sleep(3)

#     @allure.title("LIN1 Abandoned 切换inactive 唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109674?projectId=46',
#         name='Can_Lin Pdu Case Example 109674',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109674(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(15)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠"):
#             logger.info("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'IntrMirrCmdDrvrSide',timeout=12)
            
        
#         with allure.step("切换UsageMode到inactive"):
#             logger.info("切换UsageMode到inactive")
#             self.sd_tester.change_usage_mode(1, do_assert=1)
        
#         with allure.step("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠"):
#             logger.info("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('IntrMirrCmdDrvrSide',timeout=24)
            
#             logger.info("result_original_1(IntrMirrCmdDrvrSide){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 1):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:LIN1FR01:IntrMirrCmdDrvrSide=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-10)<=0.5:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的IntrMirrCmdDrvrSide值为1")
#                     assert False       
#         sleep(3)


#     @allure.title("LIN1 inactive 切换Active 唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/108201?projectId=46',
#         name='Can_Lin Pdu Case Example 108201',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_108201(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Inactive;
#             self.sd_tester.change_usage_mode(1, do_assert=1)
#             sleep(15)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠"):
#             logger.info("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin1.CemCem_Lin1Fr01, 'IntrMirrCmdDrvrSide',timeout=12)
            
        
#         with allure.step("切换UsageMode到Active"):
#             logger.info("切换UsageMode到Active")
#             self.sd_tester.change_usage_mode(11, do_assert=1)
        
#         with allure.step("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠"):
#             logger.info("检测 LIN1 通道唤醒 CEM:LIN1FR01:IntrMirrCmdDrvrSide 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('IntrMirrCmdDrvrSide',timeout=24)
            
#             logger.info("result_original_1(IntrMirrCmdDrvrSide){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 1):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:LIN1FR01:IntrMirrCmdDrvrSide=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-12)<=0.8:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的IntrMirrCmdDrvrSide值为1")
#                     assert False       
#         sleep(3)

#     @allure.title("LIN1 Driving 切换abonedone休眠")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109667?projectId=46',
#         name='Can_Lin Pdu Case Example 109667',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109667(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(1)
#             self.ipdu.reset_check_results()
#         with allure.step("诊断切换：usgmod为0d Driving"):
#             logger.info("诊断切换：usgmod为0d Driving")
#              # 设置:Usage 0d Driving;
#             self.sd_tester.change_usage_mode(13, do_assert=1)
        
#         with allure.step("检测 LIN1 通道被唤醒,开始发送报文"):
#             logger.info("检测 LIN1 通道休眠,开始发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             assert result
            
#         sleep(1)
#         with allure.step("1s 后继续检测LIN1是否被唤醒"):
#             logger.info("1s 后继续检测LIN1是否被唤醒")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             assert result       
        
#         self.ipdu.reset_check_results()
#         with allure.step("诊断切换：usgmod为00abonedone"):
#             logger.info("诊断切换：usgmod为00abonedone")
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#         sleep(15)
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
        
#         sleep(3)



#     @allure.title("LIN1 inactive 车速唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/1096651?projectId=46',
#         name='Can_Lin Pdu Case Example 109665',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109665(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Inactive;
#             self.sd_tester.change_usage_mode(1, do_assert=1)
#             sleep(15)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
                
#         self.ipdu.reset_check_results()
#         with allure.step("仿真车速大于 7km/h"):
#             logger.info("仿真车速大于 7km/h")
#             self.ipdu.set_vehspd(10.0)
        
#         with allure.step("检测 LIN1 通道被唤醒,开始发送报文"):
#             logger.info("检测 LIN1 通道休眠,开始发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             assert result
            
#         sleep(10)
#         with allure.step("10s 后继续检测LIN1是否被唤醒"):
#             logger.info("10s 后继续检测LIN1是否被唤醒")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             assert result       
        
#         self.ipdu.reset_check_results()
#         with allure.step("仿真车速大于 0km/h"):
#             logger.info("仿真车速大于 0km/h")
#             self.ipdu.set_vehspd(0.0)
#             sleep(0.5)
#             self.ipdu.set_vehspd(0.0)

#         sleep(15)
        
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
        
#         sleep(3)

#     @allure.title("LIN1 abonedone 车速唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109713?projectId=46',
#         name='Can_Lin Pdu Case Example 109713',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109713(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(13)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
                
#         self.ipdu.reset_check_results()
#         with allure.step("仿真车速大于 7km/h"):
#             logger.info("仿真车速大于 7km/h")
#             sleep(0.5)
#             logger.info("仿真车速大于 7km/h")
#             self.ipdu.set_vehspd(10.0)
#         sleep(0.5)
#         with allure.step("检测 LIN1 通道被唤醒,开始发送报文"):
#             logger.info("检测 LIN1 通道休眠,开始发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             assert result
            
#         sleep(10)
#         with allure.step("10s 后继续检测LIN1是否被唤醒"):
#             logger.info("10s 后继续检测LIN1是否被唤醒")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             assert result       
        
#         self.ipdu.reset_check_results()
#         with allure.step("仿真车速大于 0km/h"):
#             logger.info("仿真车速大于 0km/h")
#             self.ipdu.set_vehspd(0.0)
#             sleep(0.5)
#             self.ipdu.set_vehspd(0.0)
#         sleep(6)
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
        
#         sleep(3)    

#     @allure.title("LIN1 诊断唤醒Lin1ParNr调度表")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109675?projectId=46',
#         name='Can_Lin Pdu Case Example 109675',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109675(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(15)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN1 通道休眠,停止发送报文"):
#             logger.info("检测 LIN1 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  

#         with allure.step("读取版本信息22F1BB"):
#             logger.info("读取版本信息22F1BB")
#             self.sd_tester.update_serverdoipid(0x1002)
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
#             if payload[0:3] == [0x62,0xF1,0xBB]:
#                 assert True
#             else:
#                 assert False
#         with allure.step("10s 后继续检测LIN1是否被唤醒"):
#             logger.info("10s 后继续检测LIN1是否被唤醒")
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             result = self.ipdu.check_bus_recv_message("cem_lin1")
#             logger.info("result {}".format(result))
#             assert result         
#         sleep(3)


#     @allure.title("LIN2 Abandoned 切换Convenience 唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109661?projectId=46',
#         name='Can_Lin Pdu Case Example 109661',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109661(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(15)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道休眠,停止发送报文"):
#             logger.info("检测 LIN2 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin2")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin2.CemCem_Lin2Fr07, 'AIInteractionLampLeftY1',timeout=12)
            
        
#         with allure.step("切换UsageMode到Convenience"):
#             logger.info("切换UsageMode到Convenience")
#             self.sd_tester.change_usage_mode(2, do_assert=1)
        
#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('AIInteractionLampLeftY1',timeout=24)
            
#             logger.info("result_original_1(AIInteractionLampLeftY1){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 0):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:LIN2FR07:AIInteractionLampLeftY1=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-12)<=0.8:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的AIInteractionLampLeftY1值为0")
#                     assert False       
#         sleep(3)

#     @allure.title("LIN2 诊断唤醒Lin2ParNr调度表")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109659?projectId=46',
#         name='Can_Lin Pdu Case Example 109659',
#     )
#     @pytest.mark.debug_1
#     @pytest.mark.full
#     def test_lin_networkmanagement_caseid_1096591(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(3)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道休眠,停止发送报文"):
#             logger.info("检测 LIN2 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin2")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  

                  
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道唤醒 CEM:Lin4PartNrFr04:FCSIPartNo10CmplEndSgn1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:Lin4PartNrFr04:FCSIPartNo10CmplEndSgn1 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin2.FcsiEcm_Lin4PartNrFr04, 'FCSIPartNo10CmplEndSgn1',timeout=4)
            
        
#         with allure.step("切换UsageMode到Convenience"):
#             logger.info("切换UsageMode到Convenience")
#             self.sd_tester.update_serverdoipid(0x1002)
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
#             if payload[0:3] == [0x62,0xF1,0xBB]:
#                 assert True
#             else:
#                 assert False
#             sleep(0.5)   
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             sleep(0.5) 
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             self.sd_tester.change_usage_mode(2, do_assert=1)
        
#         with allure.step("检测 LIN2 通道唤醒 CEM:Lin4PartNrFr04:FCSIPartNo10CmplEndSgn1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:Lin4PartNrFr04:FCSIPartNo10CmplEndSgn1 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('FCSIPartNo10CmplEndSgn1',timeout=8)
            
#             logger.info("result_original_1(FCSIPartNo10CmplEndSgn1){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 0):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:Lin4PartNrFr04:FCSIPartNo10CmplEndSgn1=0持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-1)<=0.5:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的FCSIPartNo10CmplEndSgn1值为0")
#                     assert False       
#         sleep(3)

#     @allure.title("LIN2 诊断唤醒Lin2ParNr调度表")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109659?projectId=46',
#         name='Can_Lin Pdu Case Example 109659',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109659(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(3)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道休眠,停止发送报文"):
#             logger.info("检测 LIN2 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin2")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  

#         with allure.step("读取版本信息22F1BB"):
#             logger.info("读取版本信息22F1BB")
#             self.sd_tester.update_serverdoipid(0x1002)
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
#             if payload[0:3] == [0x62,0xF1,0xBB]:
#                 assert True
#             else:
#                 assert False
#         with allure.step("10s 后继续检测LIN2是否被唤醒"):
#             logger.info("10s 后继续检测LIN2是否被唤醒")
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             result = self.ipdu.check_bus_recv_message("cem_lin2")
#             logger.info("result {}".format(result))
#             assert result         
#         sleep(3)

#     @allure.title("LIN2 Abandoned DCChrgnHndlSts 0变为2 唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109679?projectId=46',
#         name='Can_Lin Pdu Case Example 109679',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109679(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:DCChrgnHndlSts 设置为0;
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29,'DCChrgnHndlSts',0)
#             sleep(5)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道休眠,停止发送报文"):
#             logger.info("检测 LIN2 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin2")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin2.CemCem_Lin2Fr07, 'AIInteractionLampLeftY1',timeout=15)       
#         with allure.step("设置:DCChrgnHndlSts 设置为2"):
#             logger.info("设置:DCChrgnHndlSts 设置为2")
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29,'DCChrgnHndlSts',2)
        
#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
#             result_ori_1 = self.ipdu.check_signal_thread_stop('AIInteractionLampLeftY1',timeout=30)
#             logger.info("result_original_1(AIInteractionLampLeftY1){}".format(result_ori_1))
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 0):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:LIN2FR07:AIInteractionLampLeftY1=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-15)<=0.5:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的AIInteractionLampLeftY1值为0")
#                     assert False       
#         sleep(3)
    
#     @allure.title("LIN2 Abandoned DCChrgnHndlSts 2变为0 唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109666?projectId=46',
#         name='Can_Lin Pdu Case Example 109666',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109666(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:DCChrgnHndlSts 设置为2;
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29,'DCChrgnHndlSts',2)
#             sleep(5)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道休眠,停止发送报文"):
#             logger.info("检测 LIN2 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin2")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin2.CemCem_Lin2Fr07, 'AIInteractionLampLeftY1',timeout=15)       
        
#         with allure.step("设置:DCChrgnHndlSts 设置为0"):
#             logger.info("设置:DCChrgnHndlSts 设置为0")
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr29,'DCChrgnHndlSts',0)
        
#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
#             result_ori_1 = self.ipdu.check_signal_thread_stop('AIInteractionLampLeftY1',timeout=30)
#             logger.info("result_original_1(AIInteractionLampLeftY1){}".format(result_ori_1))
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 0):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:LIN2FR07:AIInteractionLampLeftY1=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-15)<=0.5:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的AIInteractionLampLeftY1值为0")
#                     assert False       
#         sleep(3)

#     @allure.title("LIN2 NOT Abandoned 保持唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109660?projectId=46',
#         name='Can_Lin Pdu Case Example 109660',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109660(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(5)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道休眠,停止发送报文"):
#             logger.info("检测 LIN2 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin2")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin2.CemCem_Lin2Fr07, 'AIInteractionLampLeftY1',timeout=12)
            
        
#         with allure.step("切换UsageMode not abonedone"):
#             logger.info("切换UsageMode not abonedone")
#             self.sd_tester.change_usage_mode(1, do_assert=1)
#             sleep(0.5)
#             self.sd_tester.change_usage_mode(2, do_assert=1)
#             sleep(0.5)
#             self.sd_tester.change_usage_mode(11, do_assert=1)
#             sleep(0.5)
#             self.sd_tester.change_usage_mode(13, do_assert=1)

#         with allure.step("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠"):
#             logger.info("检测 LIN2 通道唤醒 CEM:LIN2FR07:AIInteractionLampLeftY1 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('AIInteractionLampLeftY1',timeout=24)
            
#             logger.info("result_original_1(AIInteractionLampLeftY1){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 0):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:LIN2FR07:AIInteractionLampLeftY1=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-12)<=0.8:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的AIInteractionLampLeftY1值为0")
#                     assert False       
#         sleep(3)
    
#     @allure.title("LIN3 NOT Abandoned 唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109676?projectId=46',
#         name='Can_Lin Pdu Case Example 109676',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109676(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(5)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN3 通道休眠,停止发送报文"):
#             logger.info("检测 LIN3 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin3")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False            
#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN3 通道唤醒 CEM:CemCem_Lin3Fr05:IntrLiGen2RoofDimSpeed 发送 发送3S之后休眠"):
#             logger.info("检测 LIN3 通道唤醒 CEM:CemCem_Lin3Fr05:IntrLiGen2RoofDimSpeed 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin3.CemCem_Lin3Fr05, 'IntrLiGen2RoofDimSpeed',timeout=12)
            
        
#         with allure.step("切换UsageMode not abonedone"):
#             logger.info("切换UsageMode not abonedone")
#             self.sd_tester.change_usage_mode(1, do_assert=1)
#             sleep(0.5)
#             self.sd_tester.change_usage_mode(2, do_assert=1)
#             sleep(0.5)
#             self.sd_tester.change_usage_mode(11, do_assert=1)
#             sleep(0.5)
#             self.sd_tester.change_usage_mode(13, do_assert=1)
        
#         with allure.step("检测 LIN3 通道唤醒 CEM:CemCem_Lin3Fr05:IntrLiGen2RoofDimSpeed 发送 发送3S之后休眠"):
#             logger.info("检测 LIN3 通道唤醒 CEM:CemCem_Lin3Fr05:IntrLiGen2RoofDimSpeed 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('IntrLiGen2RoofDimSpeed',timeout=24)
            
#             logger.info("result_original_1(IntrLiGen2RoofDimSpeed){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 result_1 = calculate_signal_times_and_duration(result_ori_1)
#                 frame_times = result_1[0]
#                 duration_time = result_1[1]
#                 logger.info("CEM:CemCem_Lin3Fr05:IntrLiGen2RoofDimSpeed=1持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                 if abs(duration_time-12)<=0.8:
#                     assert True
#                 else:
#                     logger.info("帧发送时间误差大于800ms")
#                     assert False       
#         sleep(3)

#     @allure.title("LIN3 诊断唤醒Lin3ParNr调度表")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/108211?projectId=46',
#         name='Can_Lin Pdu Case Example 108211',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_108211_109685(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(3)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN3 通道休眠,停止发送报文"):
#             logger.info("检测 LIN3 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin3")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  

#         with allure.step("读取版本信息22F1BB"):
#             logger.info("读取版本信息22F1BB")
#             self.sd_tester.update_serverdoipid(0x1002)
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
#             if payload[0:3] == [0x62,0xF1,0xBB]:
#                 assert True
#             else:
#                 assert False
#         with allure.step("10s 后继续检测LIN3是否被唤醒"):
#             logger.info("10s 后继续检测LIN3是否被唤醒")
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             result = self.ipdu.check_bus_recv_message("cem_lin3")
#             logger.info("result {}".format(result))
#             assert result         
#         sleep(3)

#     @allure.title("LIN4 abonedone SteerWhlHeatgDurgClima=1唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/116041?projectId=46',
#         name='Can_Lin Pdu Case Example 116041',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_116041(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(13)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN4 通道休眠,停止发送报文"):
#             logger.info("检测 LIN4 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
                
#         self.ipdu.reset_check_results()
#         with allure.step("仿真SteerWhlHeatgDurgClima=1"):
#             logger.info("仿真SteerWhlHeatgDurgClima=1")
#             self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31,'SteerWhlHeatgDurgClima',1)
#         sleep(0.5)
#         with allure.step("检测 LIN4 通道被唤醒,开始发送报文"):
#             logger.info("检测 LIN4 通道休眠,开始发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             assert result
            
#         sleep(10)
#         with allure.step("10s 后继续检测LIN4是否被唤醒"):
#             logger.info("10s 后继续检测LIN4是否被唤醒")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             assert result       
        
#         self.ipdu.reset_check_results()
#         with allure.step("仿真SteerWhlHeatgDurgClima=0"):
#             logger.info("仿真SteerWhlHeatgDurgClima=0")
#             self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31,'SteerWhlHeatgDurgClima',0)
#         sleep(3)
#         with allure.step("检测 LIN4 通道休眠,停止发送报文"):
#             logger.info("检测 LIN4 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
        
#         sleep(3)    

#         #VehicleModeService::UsageModeChanged == INACTIVE时，激活VFC - ParkingDrivingClimatization
#     @allure.title("LIN4 abonedone ParkingDrivingClimatization=1唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/116035?projectId=46',
#         name='Can_Lin Pdu Case Example 116035',
#     )
#     @pytest.mark.debug
#     @pytest.mark.full
#     def test_lin_networkmanagement_caseid_116035(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(13)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN4 通道休眠,停止发送报文"):
#             logger.info("检测 LIN4 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
                
#         self.ipdu.reset_check_results()
#         with allure.step("仿真SteerWhlHeatgDurgClima=1"):
#             logger.info("仿真SteerWhlHeatgDurgClima=1")
#             self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31,'SteerWhlHeatgDurgClima',1)
#         sleep(0.5)
#         with allure.step("检测 LIN4 通道被唤醒,开始发送报文"):
#             logger.info("检测 LIN4 通道休眠,开始发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             assert result
            
#         sleep(10)
#         with allure.step("10s 后继续检测LIN4是否被唤醒"):
#             logger.info("10s 后继续检测LIN4是否被唤醒")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             assert result       
        
#         self.ipdu.reset_check_results()
#         with allure.step("仿真SteerWhlHeatgDurgClima=0"):
#             logger.info("仿真SteerWhlHeatgDurgClima=0")
#             self.ipdu.set(self.ipdu.bodycan.CcmBodyFr31,'SteerWhlHeatgDurgClima',0)
#         sleep(3)
#         with allure.step("检测 LIN4 通道休眠,停止发送报文"):
#             logger.info("检测 LIN4 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
        
#         sleep(3)

#     @allure.title("LIN4 abonedone 车速唤醒")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109683?projectId=46',
#         name='Can_Lin Pdu Case Example 109683',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109683(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(13)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN4 通道休眠,停止发送报文"):
#             logger.info("检测 LIN4 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
                
#         self.ipdu.reset_check_results()
#         with allure.step("仿真车速大于 7km/h"):
#             logger.info("仿真车速大于 7km/h")
#             self.ipdu.set_vehspd(10.0)

#         sleep(1)
#         with allure.step("检测 LIN4 通道被唤醒,开始发送报文"):
#             logger.info("检测 LIN4 通道休眠,开始发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             assert result
            
#         sleep(10)
#         with allure.step("10s 后继续检测LIN4是否被唤醒"):
#             logger.info("10s 后继续检测LIN4是否被唤醒")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             assert result       
        
#         self.ipdu.reset_check_results()
#         with allure.step("仿真车速大于 0km/h"):
#             logger.info("仿真车速大于 0km/h")
#             self.ipdu.set_vehspd(0.0)
#             sleep(0.5)
#             self.ipdu.set_vehspd(0.0)
#         sleep(6)
#         with allure.step("检测 LIN4 通道休眠,停止发送报文"):
#             logger.info("检测 LIN4 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False
        
#         sleep(3) 

#     @allure.title("LIN4 诊断唤醒Lin4ParNr调度表")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/108211?projectId=46',
#         name='Can_Lin Pdu Case Example 108211',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_108211(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(6)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN4 通道休眠,停止发送报文"):
#             logger.info("检测 LIN4 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  

#         with allure.step("读取版本信息22F1BB"):
#             logger.info("读取版本信息22F1BB")
#             self.sd_tester.update_serverdoipid(0x1002)
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
#             if payload[0:3] == [0x62,0xF1,0xBB]:
#                 assert True
#             else:
#                 assert False
#         with allure.step("10s 后继续检测LIN4是否被唤醒"):
#             logger.info("10s 后继续检测LIN4是否被唤醒")
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             result = self.ipdu.check_bus_recv_message("cem_lin4")
#             logger.info("result {}".format(result))
#             assert result         
#         sleep(3)

#     @allure.title("LIN5 Abandoned 切换Convenience 唤醒 ")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109647?projectId=46',
#         name='Can_Lin Pdu Case Example 109647',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109647(self):
#         with allure.step("设置初始化条件"):
#             # 诊断激活线断开
#             logger.info("诊断激活线断开")
#             self.nucapp.bgm_diag_line_down()
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(10)
#             self.ipdu.reset_check_results()
#         with allure.step(f"检测是否IgnRly3Cmd=0"):
#             self.ipdu.check(
#                 self.ipdu.infocanfd.BgmInfoCanFdFr18, 'RlyPwrCmd', 0
#             )
#         with allure.step("检测 LIN5 通道休眠,停止发送报文"):
#             logger.info("检测 LIN5 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin5")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False

#         self.ipdu.reset_check_results()
#         with allure.step("检测 LIN5 通道唤醒 CEM:CemCem_Lin5Fr01:OrdinaryAmbientLightFrontLeftBlue 发送 发送3S之后休眠"):
#             logger.info("检测 LIN5 通道唤醒 CEM:CemCem_Lin5Fr01:OrdinaryAmbientLightFrontLeftBlue 发送 发送3S之后休眠")
            
#             self.ipdu.check_signal_thread_start(self.ipdu.cem_lin5.CemCem_Lin5Fr01,'OrdinaryAmbientLightFrontLeftBlue',timeout=12)
            
        
#         with allure.step("切换UsageMode到Convenience"):
#             logger.info("切换UsageMode到Convenience")
#             self.sd_tester.change_usage_mode(2, do_assert=1)

#         with allure.step(f"检测是否IgnRly3Cmd=1"):
#             self.ipdu.check(
#                 self.ipdu.infocanfd.BgmInfoCanFdFr18, 'RlyPwrCmd', 1
#             )
        
#         with allure.step("检测 LIN4 通道唤醒 CEM:CemCem_Lin5Fr01:OrdinaryAmbientLightFrontLeftBlue 发送 发送3S之后休眠"):
#             logger.info("检测 LIN4 通道唤醒 CEM:CemCem_Lin5Fr01:OrdinaryAmbientLightFrontLeftBlue 发送 发送3S之后休眠")
            
#             result_ori_1 = self.ipdu.check_signal_thread_stop('OrdinaryAmbientLightFrontLeftBlue',timeout=24)
            
#             logger.info("result_original_1(OrdinaryAmbientLightFrontLeftBlue){}".format(result_ori_1))
            
#             if result_ori_1 == None:
#                 assert False
#             else:
#                 if check_all_value_is(result_ori_1, 0):
#                     result_1 = calculate_signal_times_and_duration(result_ori_1)
#                     frame_times = result_1[0]
#                     duration_time = result_1[1]
#                     logger.info("CEM:CemCem_Lin5Fr01:OrdinaryAmbientLightFrontLeftBlue=0持续发送{}帧，持续时间为{}s".format(frame_times,duration_time))
#                     if abs(duration_time-12)<=0.8:
#                         assert True
#                     else:
#                         logger.info("帧发送时间误差大于500ms")
#                         assert False
#                 else:
#                     logger.info("不是所有的OrdinaryAmbientLightFrontLeftBlue值为0")
#                     assert False       
#         sleep(3)  

#     @allure.title("LIN5 Convenience 切换Abandoned 休眠 ")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/109647?projectId=46',
#         name='Can_Lin Pdu Case Example 109647',
#     )
#     @pytest.mark.smoke
#     def test_lin_networkmanagement_caseid_109647(self):
#         with allure.step("设置初始化条件"):
#             # 诊断激活线断开
#             logger.info("诊断激活线断开")
#             self.nucapp.bgm_diag_line_down()
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
            
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(10)
#             self.ipdu.reset_check_results()
#         with allure.step(f"检测是否IgnRly3Cmd=0"):
#             self.ipdu.check(
#                 self.ipdu.infocanfd.BgmInfoCanFdFr18, 'RlyPwrCmd', 0
#             )
#         with allure.step("检测 LIN5 通道休眠,停止发送报文"):
#             logger.info("检测 LIN5 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin5")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False

        
        
#         with allure.step("切换UsageMode到Convenience"):
#             logger.info("切换UsageMode到Convenience")
#             self.sd_tester.change_usage_mode(2, do_assert=1)

#         with allure.step(f"检测是否IgnRly3Cmd=1"):
#             self.ipdu.check(
#                 self.ipdu.infocanfd.BgmInfoCanFdFr18, 'RlyPwrCmd', 1
#             )
        

#     @allure.title("LIN6 诊断唤醒Lin6ParNr调度表")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/116030?projectId=46',
#         name='Can_Lin Pdu Case Example 116030',
#     )
#     @pytest.mark.smoke
#     @pytest.mark.V_1_3
#     def test_lin_networkmanagement_caseid_116030(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(3)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN6 通道休眠,停止发送报文"):
#             logger.info("检测 LIN6 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin6")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  

#         with allure.step("读取版本信息22F1BB"):
#             logger.info("读取版本信息22F1BB")
#             self.sd_tester.update_serverdoipid(0x1002)
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
#             if payload[0:3] == [0x62,0xF1,0xBB]:
#                 assert True
#             else:
#                 assert False
#         with allure.step("10s 后继续检测LIN6是否被唤醒"):
#             logger.info("10s 后继续检测LIN6是否被唤醒")
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             result = self.ipdu.check_bus_recv_message("cem_lin6")
#             logger.info("result {}".format(result))
#             assert result         
#         sleep(3)


#     @allure.title("LIN6 调度表切换测试")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/116036?projectId=46',
#         name='Can_Lin Pdu Case Example 116036',
#     )
#     @pytest.mark.smoke
#     @pytest.mark.V_1_3
#     def test_lin_networkmanagement_caseid_116036(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(3)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN6 通道休眠,停止发送报文"):
#             logger.info("检测 LIN6 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin6")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  

#         with allure.step("读取版本信息22F1BB"):
#             logger.info("读取版本信息22F1BB")
#             self.sd_tester.update_serverdoipid(0x1002)
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             payload = self.sd_tester.return_udsdata_and_check_and_print_response_result()
#             if payload[0:3] == [0x62,0xF1,0xBB]:
#                 assert True
#             else:
#                 assert False
#         with allure.step("10s 后继续检测LIN6是否被唤醒"):
#             logger.info("10s 后继续检测LIN6是否被唤醒")
#             self.sd_tester.send_data([0x22,0xF1,0xBB])
#             result = self.ipdu.check_bus_recv_message("cem_lin6")
#             logger.info("result {}".format(result))
#             assert result         
#         sleep(3)


#     @allure.title("LIN6 abonedone唤醒BattSnsrStsReq")
#     @allure.testcase(
#         'https://jama.jiduauto.com/perspective.req#/testCases/116040?projectId=46',
#         name='Can_Lin Pdu Case Example 116040',
#     )
#     @pytest.mark.smoke
#     @pytest.mark.V_1_3
#     def test_lin_networkmanagement_caseid_116040(self):
#         with allure.step("设置初始化条件"):
#             # self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
#             # self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
#             self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00,"VehMtnStVehMtnSt",3)
#             self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, "TrsmParkLockdTrsmParkLockd", 0)
#             sleep(1)
#             # 设置:Carmode 设置为Normal;
#             self.sd_tester.change_car_mode(0, do_assert=1)
#             sleep(0.5)
#             # 设置:Usage 设置为Abandoned;
#             self.sd_tester.change_usage_mode(0, do_assert=1)
#             sleep(3)
#             self.ipdu.reset_check_results()
#         with allure.step("检测 LIN6 通道休眠,停止发送报文"):
#             logger.info("检测 LIN6 通道休眠,停止发送报文")
#             result = self.ipdu.check_bus_recv_message("cem_lin6")
#             logger.info("result_original {}".format(result))
#             if result == None:
#                 assert True
#             else:
#                 assert False  
#         with allure.step(f"检测是否EgyLvlChk=0"):
#             self.ipdu.check(
#                 self.ipdu.infocanfd.BgmInfoCanFdFr23, 'EgyLvlChk', 0, 
#             )
#             sleep(1)
#         with allure.step("仿真EgyDesForClima=14"):
#             self.ipdu.set(self.ipdu.bodycan.CcmBodyFr27,'EgyDesForClima_0_CcmBodySignalIPdu27',14)
#             sleep(1)
#         with allure.step("1s 后继续检测LIN6是否被唤醒"):
#             logger.info("1s 后继续检测LIN6是否被唤醒")
#             result = self.ipdu.check_bus_recv_message("cem_lin6")
#             logger.info("result {}".format(result))
#             assert result         
#         sleep(3)