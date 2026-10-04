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
# import time

# import pytest
# import allure

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))
# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
# from sdk_interface.abc_interface import *


# @allure.feature("MCU 基础平台/诊断路由")
# @allure.story("功能用例")
# class TestDiagRouteAppStress(TestABCBase):
#     def before_class(self, ecu):
#         self.bus_comm.get_vehicle_speed()
#         self.bus_comm.set_vehspd()
#         # self.bus_comm.resume_all_bus_send()
#         self.bus_comm.pause_all_bus_send()
#         self.bus_comm.pause_cycle_tx_rx_d()
#         self.excel_path = "mcu/config_data/diag_route/"
#         self.data_info_list = self.mix.read_diag_route_excel(self.excel_path, 'doip2docan')
#         self.data_info_list_phy = [item for item in self.data_info_list if 'app' in item.get("session", "")]

#         data_info_list_func = self.mix.read_diag_route_excel(self.excel_path, 'doip_func')
#         self.data_info_list_func = [item for item in data_info_list_func if 'app' in item.get("session", "")]

#         self.data_info_list_phy_boot_only = [item for item in self.data_info_list if 'boot' == item.get("session", "")]

#     def before_each_func(self, ecu):
#         pass

#     def after_each_func(self, ecu):
#         logger.info("after_each_func")

#     def after_class(self, ecu):
#         logger.info("after_class")


#     @pytest.mark.repeat(20)
#     @pytest.mark.mcu_stress
#     def test_app_eth2can_send_response_recv_flow_frame_1985015(self):
#         """
#         不发送请求，直接回复多帧响应，bgm 需要回复流控帧
#         出现问题 40%的概率收不到
#         """
#         self.mix.eth2can_send_response_recv_flow_frame(self.data_info_list_phy)

# # pytest mcu/00ltg/test_diag_route_app_stress.py
