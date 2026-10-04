# # -*- coding: utf-8 -*-
# """
# @File        : test_can_lin_fr_signal_route.py
# @Author      : tanggeng.li@jiduauto.com
# @Time        : 2023/11/22 11:36
# @Description :

# """

# import os
# import random
# import sys
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
# @allure.story("功能用例/boot下/doip2can")
# class TestDiagRouteBootDoip2Docan(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         try:
#             self.mix.init_boot_per()
#             self.sd_tester.send_request_and_recv_response([0x10, 0x01])
#             self.bus_comm.pause_all_bus_send()
#             self.bus_comm.pause_cycle_tx_rx_d()
#         except Exception as e:
#             logger.warning(f"boot 下的诊断路由前提条件失败error>>{str(e)}")

#         self.excel_path = "mcu/config_data/diag_route/"
#         # doip2can
#         data_info_list_func = self.mix.read_diag_route_excel(self.excel_path, 'doip_func')
#         self.data_info_list_func = [item for item in data_info_list_func if 'boot' in item.get("session", "")]
#         self.data_info_list = self.mix.read_diag_route_excel(self.excel_path, 'doip2docan')
#         self.data_info_list_phy = [item for item in self.data_info_list if 'boot' in item.get("session", "")]
#         self.data_info_list_phy_app_only = [item for item in self.data_info_list if 'app' == item.get("session", "")]

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu,True)
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.enter_boot()

#     def after_each_func(self, ecu):
#         logger.info("after_each_func")
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.quit_boot()
#         super().after_class(self, ecu)

#     @pytest.mark.smoke
#     def test_boot_phy_eth2can_single_frame_caseid_1984516(self):
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [1])

#     @pytest.mark.smoke
#     def test_boot_phy_eth2can_single_frame_caseid_1984509(self):
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [7])

#     @pytest.mark.smoke
#     def test_boot_phy_eth2can_single_frame_caseid_1984517(self):
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [8])

#     @pytest.mark.smoke
#     def test_boot_phy_eth2can_single_frame_caseid_1984508(self):
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [100])

#     @pytest.mark.smoke
#     def test_boot_phy_eth2can_single_frame_caseid_1984507(self):
#         self.mix.diag_route_eth2can(self.data_info_list_phy, [4095])

#     @pytest.mark.smoke
#     def test_boot_func_single_frame_caseid_1984518(self):
#         self.mix.diag_route_doip2can_func(self.data_info_list_func, [1])

#     @pytest.mark.smoke
#     def test_boot_func_single_frame_caseid_1984512(self):
#         self.mix.diag_route_doip2can_func(self.data_info_list_func, [6])

#     @pytest.mark.smoke
#     def test_boot_route_caseid_1984590(self):
#         '''
#         在 BOOT 下 发送单帧路由报文7个字节以内，非路由can 通道 不能接收报文
#         @return:
#         '''

#         lengh = random.randint(1, 7)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy, [lengh])

#     @pytest.mark.smoke
#     def test_boot_route_caseid_1984592(self):
#         '''
#         在 boot 下 发送多帧路由报文 8 到 4095 字节以内，非路由can 通道 不能接收报文
#         @return:
#         '''

#         lengh = random.randint(8, 4095)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy, [lengh])

#     @pytest.mark.smoke
#     def test_boot_send_app_route_caseid_1984585(self):
#         '''
#         在 boot 下 发送只能在app路由的 ，所有can 通道不能接收到报文
#         @return:
#         '''

#         lengh = random.randint(1, 7)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy_app_only, [lengh], all_can=True)
#         lengh = random.randint(8, 4095)
#         self.mix.diag_route_eth2can_unrecv(self.data_info_list_phy_app_only, [lengh], all_can=True)

#     @pytest.mark.sanity
#     def test_boot_send_route_caseid_1984591(self):
#         '''
#         在 app 下 发送
#         构建非法的逻辑地址，例如 到passivesafetycan 通道的 逻辑地址有 0x1510 0x1511 0x1512 0x1513构建
#         除去这四个地址的其他地址如 0X1509 0X1514等 ，随机选择几个发送，
#         @return:
#         '''
#         lengh = random.randint(1, 7)
#         data_list = self.mix.creat_diag_route_doip2can_phy_invalid_data_item(self.data_info_list)
#         self.mix.diag_route_eth2can_unrecv(data_list, [lengh], all_can=True)


# @pytest.mark.mcu_test
# @allure.feature("MCU 基础平台/诊断路由")
# @allure.story("功能用例/boot下/can2can")
# class TestDiagRouteBootDocan2Docan(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)
#         try:
#             self.mix.init_boot_per()
#             self.sd_tester.send_request_and_recv_response([0x10, 0x01])
#             self.bus_comm.pause_all_bus_send()
#             self.bus_comm.pause_cycle_tx_rx_d()
#         except Exception as e:
#             logger.warning(f"boot 下的诊断路由前提条件失败error>>{str(e)}")

#         self.excel_path = "mcu/config_data/diag_route/"
#         # can2can
#         can2can_data_info_list = self.mix.read_diag_route_excel(self.excel_path, 'docan2docan')
#         self.can2can_data_list = [item for item in can2can_data_info_list if 'app' == item.get("session", "")]
#         data_info_list_func = self.mix.read_diag_route_excel(self.excel_path, 'docan_func')
#         self.can2can_data_func = [item for item in data_info_list_func if 'app' == item.get("session", "")]

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu,True)
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.enter_boot()

#     def after_each_func(self, ecu):
#         logger.info("after_each_func")
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.quit_boot()
#         super().after_class(self, ecu)

#     @pytest.mark.sanity
#     def test_can2can_boot_send_app_route_caseid_1985654(self):
#         '''
#         物理寻址 在 boot 下 发送单帧 只能在app路由的 ，所有can 通道不能接收到报文
#         @return:
#         '''

#         lengh = random.randint(1, 7)
#         self.mix.diag_route_can2can_unrecv(self.can2can_data_list, [lengh], all_can=True,under_boot=True)


#     @pytest.mark.sanity
#     def test_can2can_boot_send_app_route_caseid_1985655(self):
#         '''
#         物理寻址 在 boot 下 发送 多帧 只能在app路由的 ，所有can 通道不能接收到报文
#         @return:
#         '''
#         lengh = random.randint(8, 4095)
#         self.mix.diag_route_can2can_unrecv(self.can2can_data_list, [lengh], all_can=True,under_boot=True)

#     @pytest.mark.sanity
#     def test_can2can_func_boot_send_app_route_caseid_1985655(self):
#         '''
#         功能寻址 在 boot 下 发送 多帧 只能在app路由的 ，所有can 通道不能接收到报文
#         @return:
#         '''
#         lengh = random.randint(1, 7)
#         self.mix.diag_route_can2can_func(self.can2can_data_func, [lengh], recv_able=False)

# # pytest mcu/00ltg/test_diag_route_boot.py
# # pytest mcu/basic_platform/diag_route/function/test_diag_route_boot.py
