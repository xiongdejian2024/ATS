# # -*- coding: utf-8 -*-
# """
# @File        : test_can_lin_fr_signal_route.py
# @Author      : tanggeng.li@jiduauto.com
# @Time        : 2023/11/22 11:36
# @Description :

# """
# import copy
# import os
# import sys
# import random

# import pytest
# import allure

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))
# from test_case.bgm.mcu.case_helper.test_abc_base import TestABCBase
# from sdk_interface.abc_interface import *


# @pytest.mark.mcu_test
# @allure.feature("MCU 基础平台/诊断路由")
# @allure.story("功能用例/app下/doip2docan")
# class TestDiagRouteAppDoip2Docan(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         self.bus_comm.get_vehicle_speed()
#         self.bus_comm.set_vehspd()
#         # self.bus_comm.resume_all_bus_send()
#         self.bus_comm.pause_all_bus_send()
#         self.bus_comm.pause_cycle_tx_rx_d()
#         self.excel_path = "mcu/config_data/diag_route/"
#         # doip2can
#         self.data_info_list = self.mix.read_diag_route_excel(self.excel_path, 'doip2docan')
#         self.data_info_list_phy = [item for item in self.data_info_list if 'app' in item.get("session", "")]
#         data_info_list_func = self.mix.read_diag_route_excel(self.excel_path, 'doip_func')
#         self.data_info_list_func = [item for item in data_info_list_func if 'app' in item.get("session", "")]

#         self.data_info_list_phy_boot_only = [item for item in self.data_info_list if 'boot' == item.get("session", "")]

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu, True)
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.quit_boot()

#     def after_each_func(self, ecu):
#         super().after_each_func(ecu)
#         logger.info("after_each_func")

#     def after_class(self, ecu):
#         logger.info("after_class")
#         super().after_class(self, ecu)

#     @pytest.mark.smoke
#     def test_app_phy_eth2can_single_frame_caseid_1984513(self):
#         """
#         """
#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [1])

#     @pytest.mark.smoke
#     def test_app_phy_eth2can_single_frame_caseid_1984501(self):
#         """
#         """
#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [7])

#     @pytest.mark.smoke
#     def test_app_phy_eth2can_mul_frame_caseid_1984514(self):
#         """
#         """
#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [8])

#     @pytest.mark.smoke
#     def test_app_phy_eth2can_mul_frame_caseid_1984502(self):
#         """
#         """
#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [100])

#     @pytest.mark.smoke
#     def test_app_phy_eth2can_mul_frame_caseid_1984503(self):
#         """
#         """
#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [4095])

#     @pytest.mark.smoke
#     def test_app_func_single_frame_caseid_1984515(self):
#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         self.mix.diag_route_doip2can_func(self.data_info_list_func, [1])

#     @pytest.mark.smoke
#     def test_app_func_single_frame_caseid_1984504(self):
#         '''
#         功能寻址，发送6个字节可以转
#         @return:
#         '''
#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         self.mix.diag_route_doip2can_func(self.data_info_list_func, [6])

#     @pytest.mark.smoke
#     def test_app_route_caseid_1984582(self):
#         '''
#         在 app 下 发送单帧路由报文7个字节以内，非路由can 通道 不能接收报文
#         @return:
#         '''

#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         lengh = random.randint(1, 7)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy_boot_only, [lengh])

#     @pytest.mark.smoke
#     def test_app_route_caseid_1984583(self):
#         '''
#         在 app 下 发送多帧路由报文 8 到 4095 字节以内，非路由can 通道 不能接收报文
#         @return:
#         '''

#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         lengh = random.randint(8, 4095)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy_boot_only, [lengh])

#     @pytest.mark.smoke
#     def test_app_send_boot_route_caseid_1984585(self):
#         '''
#         在 app 下 发送只能在boot路由的 ，所有can 通道不能接收到报文
#         @return:
#         '''

#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         lengh = random.randint(1, 7)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy_boot_only, [lengh], all_can=True)

#         lengh = random.randint(8, 4095)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy_boot_only, [lengh], all_can=True)

#     @pytest.mark.sanity
#     def test_app_send_boot_route_caseid_1984587(self):
#         '''
#         在 app 下 发送
#         构建非法的逻辑地址，例如 到passivesafetycan 通道的 逻辑地址有 0x1510 0x1511 0x1512 0x1513构建
#         除去这四个地址的其他地址如 0X1509 0X1514等 ，随机选择几个发送，
#         @return:
#         '''

#         self.mix.get_mcu_cpuload_save_data(mcu_version=self.mcu_version, boot_version=self.boot_version,
#                                            mpu_version=self.mpu_version)
#         lengh = random.randint(1, 7)
#         data_list = self.mix.creat_diag_route_doip2can_phy_invalid_data_item(self.data_info_list)
#         self.mix.diag_route_eth2can_unrecv(data_list, [lengh], all_can=True)

#     @pytest.mark.sanity
#     def test_doip2can_unsend_flow_frame_caseid_1985661(self):
#         """
#         下挂接收首帧后，不回复流控帧，则收不到后续连续帧
#         """
#         self.mix.diag_route_eth2can_unsend_flow_frame(self.data_info_list_phy, 8)


# @pytest.mark.mcu_test
# @allure.feature("MCU 基础平台/诊断路由")
# @allure.story("功能用例/app下/can2can")
# class TestDiagRouteAppDocan2Docan(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         self.bus_comm.get_vehicle_speed()
#         self.bus_comm.set_vehspd()
#         # self.bus_comm.resume_all_bus_send()
#         self.bus_comm.pause_all_bus_send()
#         self.bus_comm.pause_cycle_tx_rx_d()
#         self.excel_path = "mcu/config_data/diag_route/"

#         # can2can
#         can2can_data_info_list = self.mix.read_diag_route_excel(self.excel_path, 'docan2docan')
#         self.can2can_data_list = [item for item in can2can_data_info_list if 'app' in item.get("session", "")]

#         data_info_list_func = self.mix.read_diag_route_excel(self.excel_path, 'docan_func')
#         self.can2can_data_func = [item for item in data_info_list_func if 'app' in item.get("session", "")]

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu, True)
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.quit_boot()

#     def after_each_func(self, ecu):
#         super().after_each_func(ecu)
#         logger.info("after_each_func")

#     def after_class(self, ecu):
#         logger.info("after_class")
#         super().after_class(self, ecu)

#     @pytest.mark.smoke
#     def test_can2can_1_bytes_caseid_1985641(self):
#         '''
#         一个字节 单帧到单帧
#         @return:
#         '''
#         self.mix.diag_route_can2can(self.can2can_data_list, [1])

#     @pytest.mark.smoke
#     def test_can2can_7_bytes_caseid_1985644(self):
#         '''
#         7个字节 单帧到单帧的
#         @return:
#         '''
#         self.mix.diag_route_can2can(self.can2can_data_list, [7])

#     @pytest.mark.smoke
#     def test_can2can_8_bytes_caseid_1985645(self):
#         '''
#         8g个字节 多帧到多帧
#         @return:
#         '''
#         self.mix.diag_route_can2can(self.can2can_data_list, [8])

#     @pytest.mark.smoke
#     def test_can2can_20_bytes_caseid_1985646(self):
#         '''
#         20个字节多帧到多帧
#         @return:
#         '''
#         self.mix.diag_route_can2can(self.can2can_data_list, [20])

#     #
#     @pytest.mark.smoke
#     def test_can2can_4095_bytes_caseid_1985647(self):
#         '''
#         4095 个字节 多帧到多帧
#         @return:
#         '''
#         self.mix.diag_route_can2can(self.can2can_data_list, [4095])

#     @pytest.mark.smoke
#     def test_can2can_single_frame_unrecv_caseid_1985648(self):
#         '''
#          单帧 非路由通道无法收到
#         @return:
#         '''
#         lengh = random.randint(1, 7)
#         self.mix.diag_route_can2can_unrecv(self.can2can_data_list, [lengh])

#     @pytest.mark.smoke
#     def test_can2can_mul_frame_unrecv_caseid_1985649(self):
#         '''
#          多帧 非路由通道无法收到
#         @return:
#         '''
#         lengh = random.randint(8, 4095)
#         self.mix.diag_route_can2can_unrecv(self.can2can_data_list, [lengh])

#     @pytest.mark.smoke
#     def test_can2can_invalid_data_unroute_caseid_1985659(self):
#         '''
#          异常数据 所有由通道无法收到
#         @return:
#         '''
#         lengh = random.randint(1, 7)
#         # 构造异常数据
#         data_info_list = self.mix.creat_diag_route_can2can_phy_invalid_data_item(self.can2can_data_list)
#         self.mix.diag_route_can2can_unrecv(data_info_list, [lengh], all_can=True)

#     @pytest.mark.smoke
#     def test_can2can_send_res_recv_flow_frame_caseid_1985658(self):
#         """
#         不发送请求，直接回复多帧响应，bgm 需要回复流控帧
#         """
#         self.mix.eth2can_send_response_recv_flow_frame(self.can2can_data_list)

#     @pytest.mark.sanity
#     def test_can2can_unsend_flow_frame_caseid_1985658(self):
#         """
#         下挂接收首帧后，不回复流控帧，则收不到后续连续帧
#         """
#         self.mix.diag_route_can2can_unsend_flow_frame(self.can2can_data_list, 8)

#     @pytest.mark.smoke
#     def test_can2can_func_single_frame_caseid_1985650(self):
#         """
#         功能寻址 单帧  1个字节
#         """
#         self.mix.diag_route_can2can_func(self.can2can_data_func, 1)

#     @pytest.mark.smoke
#     def test_can2can_func_single_frame_caseid_1985651(self):
#         """
#         功能寻址 单帧  6个字节
#         """
#         self.mix.diag_route_can2can_func(self.can2can_data_func, 6)

#     @pytest.mark.smoke
#     def test_can2can_func_single_frame_caseid_1985652(self):
#         """
#         功能寻址 单帧  7个字节
#         """
#         self.mix.diag_route_can2can_func(self.can2can_data_func, 7)




# @pytest.mark.mcu_test
# @allure.feature("MCU 基础平台/诊断路由")
# @allure.story("功能用例/app下/doip2fr")
# class TestDiagRouteAppDoip2Dofr(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         self.bus_comm.get_vehicle_speed()
#         self.bus_comm.set_vehspd()
#         # self.bus_comm.resume_all_bus_send()
#         # self.bus_comm.pause_all_bus_send()
#         self.bus_comm.pause_cycle_tx_rx_d()
#         #
#         self.excel_path = "mcu/config_data/diag_route/"
#         self.data_info_list = self.mix.read_diag_route_excel(self.excel_path, 'doip2dofr')
#         self.data_info_list_phy = [item for item in self.data_info_list if 'app' in item.get("session", "")]

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu, True)
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.quit_boot()

#     def after_each_func(self, ecu):
#         super().after_each_func(ecu)
#         logger.info("after_each_func")

#     def after_class(self, ecu):
#         logger.info("after_class")
#         super().after_class(self, ecu)

#     @pytest.mark.smoke
#     def test_eth2fr_1_bytes_caseid_1985676(self):
#         '''
#         doip2fr_物理寻址_在app状态下诊断仪发送单帧（1个字节）以太报文可以正常路由到fr 通道
#         @return:
#         '''
#         self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 2)

#     @pytest.mark.smoke
#     def test_eth2fr_14_bytes_caseid_1985684(self):
#         '''
#         doip2fr_物理寻址_在app状态下诊断仪发送单帧（14个字节）以太报文可以正常路由到fr 通道
#         @return:
#         '''
#         self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 14)

#     @pytest.mark.smoke
#     def test_eth2fr_15_bytes_caseid_1985685(self):
#         '''
#         doip2fr_物理寻址_在app状态下诊断仪发送多帧（15个字节）以太报文可以正常路由到fr 通道
#         @return:
#         '''
#         self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 15)

#     @pytest.mark.smoke
#     def test_eth2fr_28_bytes_caseid_1985686(self):
#         '''
#         doip2fr_物理寻址_在app状态下诊断仪发送多帧（28个字节）以太报文可以正常路由到fr 通道
#         @return:
#         '''
#         self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 28)

#     @pytest.mark.smoke
#     def test_eth2fr_29_bytes_caseid_1985689(self):
#         '''
#         doip2fr_物理寻址_在app状态下诊断仪发送多帧（29个字节）以太报文可以正常路由到fr 通道
#         @return:
#         '''
#         self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 29)

#     @pytest.mark.smoke
#     def test_eth2fr_126_bytes_caseid_1985712(self):
#         '''
#         doip2fr_物理寻址_在app状态下诊断仪发送多帧（126个字节）以太报文可以正常路由到fr 通道
#         @return:
#         '''
#         self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 126)


#     @pytest.mark.smoke
#     def test_eth2fr_200_bytes_caseid_1985712(self):
#         '''
#         doip2fr_物理寻址_在app状态下诊断仪发送多帧（126个字节）以太报文可以正常路由到fr 通道
#         @return:
#         '''
#         self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 200)

#     # @pytest.mark.smoke
#     # def test_eth2fr_1000_bytes_caseid_1985712(self):
#     #     '''
#     #     doip2fr_物理寻址_在app状态下诊断仪发送多帧（126个字节）以太报文可以正常路由到fr 通道
#     #     @return:
#     #     '''
#     #     self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 1000)


#     # @pytest.mark.smoke
#     # def test_eth2fr_4095_bytes_caseid_1985712(self):
#     #     '''
#     #     doip2fr_物理寻址_在app状态下诊断仪发送多帧（126个字节）以太报文可以正常路由到fr 通道
#     #     @return:
#     #     '''
#     #     self.mix.send_diag_route_eth2fr(self.data_info_list_phy, 4095)




# # pytest mcu/00ltg/test_diag_route_app.py
# # pytest mcu/basic_platform/diag_route/function/test_diag_route_app.py
