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


# @allure.feature("MCU 基础平台/诊断路由")
# @allure.story("功能用例/boot下")
# class TestDiagRouteBootStress(TestABCBase):
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
#         data_info_list_func = self.mix.read_diag_route_excel(self.excel_path, 'doip_func')
#         self.data_info_list_func = [item for item in data_info_list_func if 'boot' in item.get("session", "")]

#         self.data_info_list = self.mix.read_diag_route_excel(self.excel_path, 'doip2docan')
#         self.data_info_list_phy = [item for item in self.data_info_list if 'boot' in item.get("session", "")]
#         self.data_info_list_phy_app_only = [item for item in self.data_info_list if 'app' == item.get("session", "")]

#     def before_each_func(self, ecu):
#         # super().before_each_func(ecu,True)
#         # self.excel_path = "config_data/diag_route/"
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.enter_boot()

#     def after_each_func(self, ecu):
#         logger.info("after_each_func")
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         self.sd_tester.update_serverdoipid(0x1002)
#         self.sd_tester.quit_boot()
#         super().after_class(self, ecu)


#     @pytest.mark.repeat(20)
#     @pytest.mark.mcu_stress
#     def test_boot_eth2can_send_response_recv_flow_frame_1985016(self):
#         """
#         在boot 下 不发送请求，直接回复多帧响应，bgm 需要回复流控帧
#         """
#         self.mix.eth2can_send_response_recv_flow_frame(self.data_info_list_phy)


# # pytest test_diag_route_boot_stress.py
# # pytest basic_platform/diag_route/function/test_diag_route_boot.py
