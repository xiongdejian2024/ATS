# """
# @File        : test_communicate_dtc.PY
# @Author      : junxing.pang@jiduauto.com
# @Time        : 2024/07/18 20:07
# @Description : cdd 打包的相关用例

# """
# import pytest
# import allure
# import pytest
# import allure
# from test_case.bgm.mcu.case_helper.test_abc_base import TestABCBase
# from sdk_interface.common.common import *


# @allure.feature("诊断DTC")
# @allure.story("通讯DTC")
# class Test_Switch(TestABCBase):
#     def before_class(self, ecu):
#         super().before_class(self, ecu)

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)
#         # 读取ccp  方便后面进行恢复
#         err_code, recv_data_list = self.sd_tester.send_request_and_recv_response(
#             [0x22, 0xF1, 0x06], recv=[0x62, 0xF1, 0x06])
#         self.ccp_original_value = recv_data_list[3:1556 + 3]
#         self.mix.write_vehicle_model_ccp(
#             vehicle_model=VehicleType.Mars, vehicle_mca=VehicleMca.Mca_400v)
#         # Code Location
#         # DTC前置条件
#         self.mix.set_dtc_precontion()
#         # 继电器恢复初始状态
#         # for i in ["bodycan","propulsioncan","chassiscan1","chassiscan2","passivesafetycan","infocanfd","bodyexposedcanfd","adcanfd"]:
#         #     self.io.close_control_can_busoff(i)
#         # 清除历史故障
#         self.sd_tester.send_data_and_check(
#             0x1002, 0x14FFFFFF, '54', diagnostic_action="清除当前故障")

#     def after_each_func(self, ecu):
#         # Code Location
#         super().after_each_func(ecu)
#         self.sd_tester.send_data_and_check(
#             0x1002, 0x14FFFFFF, '54', diagnostic_action="清除的历史故障")
#         self.sd_tester.write_ccp_value(self.ccp_original_value)
#         time.sleep(10)

#     def after_class(self, ecu):
#         # Code Location

#         super().after_class(self, ecu)

#     # @pytest.mark.full
#     # def test_InfoCANFD_busoff_caseid_111701(self):
#     #     """
#     #     InfoCANFD总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("infocanfd")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1108820,'5904f110882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("infocanfd")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1108820,'5904f110882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_PassiveSafetyCAN_busoff_caseid_111700(self):
#     #     """
#     #     PassiveSafetyCAN总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("passivesafetycan")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1118820,'5904f111882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("passivesafetycan")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1118820,'5904f111882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_ChassisCAN1_busoff_caseid_111699(self):
#     #     """
#     #     ChassisCAN1总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("chassiscan1")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1128820,'5904f112882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("chassiscan1")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1128820,'5904f112882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_ChassisCAN2_busoff_caseid_111698(self):
#     #     """
#     #     ChassisCAN2总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("chassiscan2")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1138820,'5904f113882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("chassiscan2")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1138820,'5904f113882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_ADCANFD_busoff_caseid_111697(self):
#     #     """
#     #     ADCANFD总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("adcanfd")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1148820,'5904f114882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("adcanfd")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1148820,'5904f114882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_BodyCAN_busoff_caseid_111696(self):
#     #     """
#     #     BodyCAN总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("bodycan")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1178820,'5904f117882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("bodycan")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1178820,'5904f117882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_BodyExposedCANFD_busoff_caseid_111695(self):
#     #     """
#     #     BodyExposedCANFD总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("bodyexposedcanfd")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1188820,'5904f118882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("bodyexposedcanfd")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1188820,'5904f118882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_ConnectivityCANFD_busoff_caseid_111701(self):
#     #     """
#     #     ConnectivityCANFD总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("connectivitycanfd")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1198820,'5904f119882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("connectivitycanfd")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F1198820,'5904f119882e',diagnostic_action="检查故障是否存在历史故障")

#     # @pytest.mark.full
#     # def test_PropulsionCAN_busoff_caseid_111693(self):
#     #     """
#     #     PropulsionCAN总线关闭
#     #     """
#     #     self.io.open_control_can_busoff("propulsioncan")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F11A8820,'5904f11a882f',diagnostic_action="检查故障是否制造成功")
#     #     self.io.close_control_can_busoff("propulsioncan")
#     #     time.sleep(10)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F11A8820,'5904f11a882e',diagnostic_action="检查故障是否存在历史故障")

#     @pytest.mark.full
#     def test_hod_error_caseid_111512(self):
#         """
#         HOD 故障
#         """
#         self.bus_comm.set("cem_lin4", "HodDim_Lin1Fr04",
#                           "HandsOnDetectionErrorStatus", 3)
#         time.sleep(1)
#         # self.sd_tester.send_data_and_check(0x1002,0x1904A0659620,'5904a0659627',diagnostic_action="检查故障是否制造成功")
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x65, 0x96, 0x20], [
#                                                   0x59, 0x04, 0xA0, 0x65, 0x96], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'
#         self.bus_comm.set("cem_lin4", "HodDim_Lin1Fr04",
#                           "HandsOnDetectionErrorStatus", 0)
#         time.sleep(1)
#         # self.sd_tester.send_data_and_check(0x1002,0x1904A0659620,'5904a0659626',diagnostic_action="检查故障是否已置为历史故障")
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xA0, 0x65, 0x96, 0x20], [
#                                                   0x59, 0x04, 0xA0, 0x65, 0x96], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'

#     @pytest.mark.full
#     def test_bodycan_ccm_frame_loss_caseid_111456(self):
#         """
#         bodycan bgm与ccm丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'CCM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x00, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x00, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x00, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x00, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','CCM',0x1904D1008720,'5904d1008727','5904d1008726')

#     @pytest.mark.full
#     def test_bodycan_DDM_frame_loss_caseid_111455(self):
#         """
#         bodycan bgm与ddm丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'DDM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x01, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x01, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障失败'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x01, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x01, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','DDM',0x1904D1018720,'5904d1018727','5904d1018726')

#     @pytest.mark.full
#     def test_bodycan_PDM_frame_loss_caseid_111454(self):
#         """
#         bodycan bgm与pdm丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'PDM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x02, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x02, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x02, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x02, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','PDM',0x1904D1028720,'5904d1028727','5904d1028726')

#     @pytest.mark.full
#     def test_bodycan_RLDM_frame_loss_caseid_111453(self):
#         """
#         bodycan bgm与rldm丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'RLDM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x03, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x03, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x03, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x03, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','RLDM',0x1904D1038720,'5904d1038727','5904d1038726')

#     @pytest.mark.full
#     def test_bodycan_RRDM_frame_loss_caseid_111452(self):
#         """
#         bodycan bgm与rrdm丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'RRDM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x04, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x04, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x04, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x04, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','RRDM',0x1904D1048720,'5904d1048727','5904d1048726')

#     @pytest.mark.full
#     def test_bodycan_DPOD_frame_loss_caseid_111451(self):
#         """
#         bodycan bgm与dpod丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'DPOD')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x05, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x05, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x05, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x05, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','DPOD',0x1904D1058720,'5904d1058727','5904d1058726')

#     @pytest.mark.full
#     def test_bodycan_PPOD_frame_loss_caseid_111450(self):
#         """
#         bodycan bgm与ppod丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'PPOD')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x06, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x06, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x06, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x06, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','PPOD',0x1904D1068720,'5904d1068727','5904d1068726')

#     @pytest.mark.full
#     def test_bodycan_LPOD_frame_loss_caseid_111449(self):
#         """
#         bodycan bgm与lpod丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'LPOD')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x07, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x07, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x07, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x07, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','LPOD',0x1904D1078720,'5904d1078727','5904d1078726')

#     @pytest.mark.full
#     def test_bodycan_RPOD_frame_loss_caseid_111448(self):
#         """
#         bodycan bgm与rpod丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'RPOD')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x08, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x08, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x08, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x08, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','RPOD',0x1904D1088720,'5904d1088727','5904d1088726')

#     @pytest.mark.full
#     def test_bodycan_POT_frame_loss_caseid_111447(self):
#         """
#         bodycan bgm与POT丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'POT')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x09, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x09, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x09, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x09, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','POT',0x1904D1098720,'5904d1098727','5904d1098726')

#     @pytest.mark.full
#     def test_bodycan_SMD_frame_loss_caseid_111446(self):
#         """
#         bodycan bgm与SMD丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'SMD')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0A, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0A, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0A, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0A, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','SMD',0x1904D10A8720,'5904d10a8727','5904d10a8726')

#     @pytest.mark.full
#     def test_bodycan_SMP_frame_loss_caseid_111445(self):
#         """
#         bodycan bgm与SMP丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'SMP')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0B, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0B, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0B, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0B, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','SMP',0x1904D10B8720,'5904d10b8727','5904d10b8726')

#     @pytest.mark.full
#     def test_bodycan_SWTL_frame_loss_caseid_111444(self):
#         """
#         bodycan bgm与SWTL丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'SWTL')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0D, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0D, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0D, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0D, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','SWTL',0x1904D10D8720,'5904d10d8727','5904d10d8726')

#     @pytest.mark.full
#     def test_bodycan_SWTR_frame_loss_caseid_111443(self):
#         """
#         bodycan bgm与SWTR丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodycan', 'SWTR')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0E, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0E, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0E, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0E, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','SWTR',0x1904D10E8720,'5904d10e8727','5904d10e8726')

#     @pytest.mark.full
#     def test_BodyExposedCANFD_HCML_frame_loss_caseid_111442(self):
#         """
#         BodyExposedCANFD bgm与HCML丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodyexposedcanfd', 'HCML')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0F, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0F, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x0F, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x0F, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodyexposedcanfd','HCML',0x1904D10F8720,'5904d10f8727','5904d10f8726')

#     @pytest.mark.full
#     def test_BodyExposedCANFD_HCMR_frame_loss_caseid_111441(self):
#         """
#         BodyExposedCANFD bgm与HCMR丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodyexposedcanfd', 'HCMR')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x10, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x10, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x10, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x10, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodyexposedcanfd','HCMR',0x1904D1108720,'5904d1108727','5904d1108726')

#     @pytest.mark.full
#     def test_BodyExposedCANFD_RCML_frame_loss_caseid_111440(self):
#         """
#         BodyExposedCANFD bgm与RCML丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodyexposedcanfd', 'RCML')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x11, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x11, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x11, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x11, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodyexposedcanfd','RCML',0x1904D1118720,'5904d1118727','5904d1118726')

#     @pytest.mark.full
#     def test_BodyExposedCANFD_RCMR_frame_loss_caseid_111438(self):
#         """
#         BodyExposedCANFD bgm与RCMR丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('bodyexposedcanfd', 'RCMR')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x13, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x13, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x13, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x13, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodyexposedcanfd','RCMR',0x1904D1138720,'5904d1138727','5904d1138726')

#     @pytest.mark.full
#     def test_PassiveSafetyCAN_RML_frame_loss_caseid_111437(self):
#         """
#         PassiveSafetyCAN bgm与RML丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('passivesafetycan', 'RML')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x14, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x14, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x14, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x14, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('passivesafetycan','RML',0x1904D1148720,'5904d1148727','5904d1148726')

#     @pytest.mark.full
#     def test_Flexray_ACU_frame_loss_caseid_111436(self):
#         """
#         Flexray bgm与ACU丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('backbonefr', 'ACU')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x15, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x15, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x15, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x15, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('backbonefr','ACU',0x1904D1158720,'5904d1158727','5904d1158726')

#     @pytest.mark.full
#     def test_Flexray_SRS_frame_loss_caseid_111435(self):
#         """
#         Flexray bgm与SRS/PSGM丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send(
#             'backbonefr', 'PSGM')  # ! NEED TO PAUSE PSGM
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x16, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x16, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x16, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x16, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('backbonefr','SRS',0x1904D1168720,'5904d1168727','5904d1168726')

#     @pytest.mark.full
#     def test_Flexray_VDDM_frame_loss_caseid_111434(self):
#         """
#         Flexray bgm与VDDM丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('backbonefr', 'VDDM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x17, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x17, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x17, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x17, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('backbonefr','VDDM',0x1904D1178720,'5904d1178727','5904d1178726')

#     @pytest.mark.full
#     def test_Flexray_BBM_frame_loss_caseid_111433(self):
#         """
#         Flexray bgm与BBM丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('backbonefr', 'BBM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x18, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x18, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x18, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x18, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('backbonefr','BBM',0x1904D1188720,'5904d1188727','5904d1188726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_TCAM_frame_loss_caseid_111432(self):
#         """
#         ConnectivityCANFD bgm与TCAM丢失帧通信
#         """
#         # self.bus_comm.pause_ecu_send('connectivitycanfd', 'TCAM')
#         self.io.tcam_power_off()
#         time.sleep(20)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x19, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x19, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         # self.bus_comm.resume_all_bus_send()
#         self.io.tcam_power_on()
#         time.sleep(60 * 4)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x19, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x19, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','TCAM',0x1904D1198720,'5904d1198727','5904d1198726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_NKR_frame_loss_caseid_111431(self):
#         """
#         ConnectivityCANFD bgm与NKR丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'NKR')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1A, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1A, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1A, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1A, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','NKR',0x1904D11A8720,'5904d11a8727','5904d11a8726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_WPC_frame_loss_caseid_111430(self):
#         """
#         ConnectivityCANFD bgm与WPC丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'WPC')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1B, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1B, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1B, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1B, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','WPC',0x1904D11B8720,'5904d11b8727','5904d11b8726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_BNCM_frame_loss_caseid_111429(self):
#         """
#         ConnectivityCANFD bgm与BNCM丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'BNCM')
#         time.sleep(10)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1C, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1C, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(10)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1C, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1C, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','BNCM',0x1904D11C8720,'5904d11c8727','5904d11c8726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_DRMFL_frame_loss_caseid_111428(self):
#         """
#         ConnectivityCANFD bgm与DRMFL丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'DRMFL')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1D, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1D, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1D, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1D, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','DRMFL',0x1904D11D8720,'5904d11d8727','5904d11d8726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_DRMFR_frame_loss_caseid_111427(self):
#         """
#         ConnectivityCANFD bgm与DRMFR丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'DRMFR')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1E, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1E, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1E, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1E, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','DRMFR',0x1904D11E8720,'5904d11e8727','5904d11e8726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_DRMRL_frame_loss_caseid_111426(self):
#         """
#         ConnectivityCANFD bgm与DRMRL丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'DRMRL')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1F, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1F, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x1F, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x1F, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','DRMRL',0x1904D11F8720,'5904d11f8727','5904d11f8726')

#     @pytest.mark.full
#     def test_ConnectivityCANFD_DRMRR_frame_loss_caseid_111425(self):
#         """
#         ConnectivityCANFD bgm与DRMRR丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'DRMRR')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x20, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x20, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x20, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x20, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','DRMRR',0x1904D1208720,'5904d1208727','5904d1208726')

#     @pytest.mark.full
#     def test_InfoCANFD_CDC_frame_loss_caseid_113199(self):
#         """
#         infocanfd bgm与CDC丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('infocanfd', 'CDC')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x22, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x22, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x22, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x22, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('infocanfd','CDC',0x1904D1228720,'5904d1228727','5904d1228726')

#     @pytest.mark.full
#     def test_ADCANFD_ACU_frame_loss_caseid_113198(self):
#         """
#         ADCANFD bgm与ACU丢失帧通信
#         """
#         self.bus_comm.pause_ecu_send('adcanfd', 'ACU')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x23, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x23, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x23, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x23, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'

#         # self.mix.make_can_communicate_err('adcanfd','ACU',0x1904D1238720,'5904d1238727','5904d1238726')

#     @pytest.mark.full
#     def test_bodycan_SMB_frame_loss_caseid_1986446(self):
#         """
#         bodycan丢失SMB丢失帧通信
#         """
#         self.sd_tester.write_ccp({1473: 0x02})
#         self.bus_comm.set("bodycan", "SmbBodyFr00",
#                           "SeatHeatgLvlStsRowSecLe", 1)
#         self.bus_comm.pause_ecu_send('bodycan', 'SMB')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x20, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x20, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x20, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x20, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('bodycan','SMB',0x1904D3208720,'5904d3208727','5904d3208726')

#     @pytest.mark.full
#     def test_connectivitycanfd_WPC3_frame_loss_caseid_1986478(self):
#         """
#         connectivitycanfd丢失WPC3丢失帧通信
#         """
#         self.sd_tester.write_ccp({1439: 0x02})
#         self.bus_comm.set("connectivitycanfd",
#                           "Wpc3ConnFr01", "WPCChrgnStsPass", 1)
#         self.bus_comm.pause_ecu_send('connectivitycanfd', 'WPC3')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x25, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x25, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x25, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x25, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('connectivitycanfd','WPC3',0x1904D1258720,'5904d125872f','5904d125872e')

#     @pytest.mark.full
#     def test_Lin1_RLSM_frame_loss_caseid_111477(self):
#         """
#         RLSM丢失LIN响应
#         """
#         self.bus_comm.pause_ecu_send('cem_lin1', 'RLSM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x00, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x00, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x00, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x00, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('cem_lin1','RLSM',0x1904D3008720,'5904d3008727','5904d3008726')

#     @pytest.mark.full
#     def test_Lin1_WMM_frame_loss_caseid_111476(self):
#         """
#         WMM丢失LIN响应
#         """
#         self.bus_comm.pause_ecu_send('cem_lin1', 'WMM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x01, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x01, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x01, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x01, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('cem_lin1','WMM',0x1904D3018720,'5904d3018727','5904d3018726')

#     @pytest.mark.full
#     def test_Lin1_IRMM_frame_loss_caseid_111475(self):
#         """
#         IRMM丢失LIN响应
#         """
#         self.bus_comm.pause_ecu_send('cem_lin1', 'IRMM')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x02, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x02, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x02, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x02, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('cem_lin1','IRMM',0x1904D3028720,'5904d3028727','5904d3028726')

#     @pytest.mark.full
#     def test_Lin2_PRLD_frame_loss_caseid_111474(self):
#         """
#         PRLD丢失LIN响应
#         """
#         self.bus_comm.pause_ecu_send('cem_lin2', 'PRLD')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x03, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x03, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x03, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x03, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('cem_lin2','PRLD',0x1904D3038720,'5904d3038727','5904d3038726')

#     @pytest.mark.full
#     def test_Lin2_FCSI_frame_loss_caseid_111473(self):
#         """
#         FCSI丢失LIN响应
#         """
#         self.bus_comm.pause_ecu_send('cem_lin2', 'FCSI')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x04, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障失败'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x04, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x04, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         self.mix.make_can_communicate_err('cem_lin2','FCSI',0x1904D3048720,'5904d3048727','5904d3048726')

#     @pytest.mark.full
#     def test_Lin4_HOD_frame_loss_caseid_111468(self):
#         """
#         HOD丢失LIN响应
#         """
#         self.bus_comm.pause_ecu_send('cem_lin4', 'HOD')
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0C, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x0C, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(5)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD3, 0x0C, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD3, 0x0C, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'
#         # self.mix.make_can_communicate_err('cem_lin4','HOD',0x1904D30C8720,'5904d30c8727','5904d30c8726')

#     @pytest.mark.smoke
#     def test_BodyExposedCANFD_missing_RCMM_111439(self):
#         """
#         RCMM丢失CANFD帧
#         """
#         self.bus_comm.pause_ecu_send('bodyexposedcanfd', 'RCMM')
#         time.sleep(10)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x12, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x12, 0x87], diagnostic_action="检查故障是否制造成功")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 1, f'dtc的故障掩码为{data}，制造故障成功'

#         self.bus_comm.resume_all_bus_send()
#         time.sleep(10)
#         data = self.sd_tester.send_data_and_check(0x1002, [0x19, 0x04, 0xD1, 0x12, 0x87, 0x20], [
#                                                   0x59, 0x04, 0xD1, 0x12, 0x87], diagnostic_action="检查是否有存历史故障")[10:12]
#         logger.info(f"receive DTC statusMask is {data}")
#         bit_0 = (int(data, 16) >> 0) & 0x01
#         bit_3 = (int(data, 16) >> 3) & 0x01
#         with allure.step(f"dtc的故障掩码为{data.upper()}, bit0:{bit_0}, bit_3:{bit_3}"):
#             assert bit_0 == 0, f'dtc的故障掩码为{data}，不是历史故障'


#     # @pytest.mark.full
#     # def test_FlexRay_start_error_caseid_111400(self):
#     #     """
#     #     FlexRay启动错误
#     #     """
#     #     self.bus_comm.pause_bus_send("backbonefr")
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F2000020,'5904f2000027','5904f2000026',diagnostic_action="检查故障是否制造成功")
#     #     self.bus_comm.resume_all_bus_send()
#     #     time.sleep(5)
#     #     self.sd_tester.send_data_and_check(0x1002,0x1904F2000020,'5904f2000027','5904f2000026',diagnostic_action="检查是否有存历史故障")
