# """
# @File        : test_climate_dtc.py
# @Author      : xiangyue.li@jiduauto.com
# @Time        : 2024/04/07 15:12
# @Description : 空调DTC
#
# """
#
# import os
# import sys
# import pytest
# import allure
# from time import sleep
#
# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))
# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
# from sdk_interface.abc_interface import *
# import re
#
#
# @allure.feature("车控车设")
# @allure.story("空调功能")
# @pytest.mark.tailwing
# class TestClimateCtrlDtc(TestABCBase):
#
#     def before_class(self, ecu):
#         self.soa.update(["CentralLockService_client", "ClimateControlService_client", "VehicleSetStatusService_client",
#                          "TailGateService_client", "ResetSOAConfigService_client"])
#         sleep(1)
#         self.sd_tester.write_ccp(ccp={564: 0x2, 642: 0x3})
#
#     def before_each_func(self, ecu):
#         self.mix.set_dtc_precontion()
#         self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x08])
#         self.sd_tester.send_data([0x14, 0xFF, 0xFF, 0xFF])
#         sleep(1)
#
#     def after_each_func(self, ecu):
#         try:
#             self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L0, '54')
#         except Exception as e:
#             logger.info(f"----------> after_class Error{str(e)}")
#             pass
#
#     def after_class(self, ecu):
#         try:
#             self.mix.set_common_precontion(
#                 usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
#             )
#         except Exception as e:
#             logger.info(f"----------> after_class Error{str(e)}")
#             pass
#
#     @allure.title("验证阳光传感器组件内部故障的DTC故障码90BE96")
#     @pytest.mark.smoke
#     def test_caseid_1987993(self):
#         self.mix.generate_dtc_fault(dtc_fault=DTCFault.SolarSnsrErr, last_time=1)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.SolarSnsrErr, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
#         sleep(10)
#         self.mix.remove_dtc_fault(dtc_fault=DTCFault.SolarSnsrErr, last_time=1)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.SolarSnsrErr, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
#
#     # @allure.title("验证RLSM相对湿度传感器故障的DTC故障码970149")
#     # @pytest.mark.smoke
#     # def test_caseid_1986386(self):
#     #     self.mix.generate_dtc_fault(dtc_fault=DTCFault.RelHumSnsrErr,last_time=1)
#     #     self.sd_tester.dtc_read_and_check(dtc=DTCFault.RelHumSnsrErr, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
#     #     sleep(10)
#     #     self.mix.remove_dtc_fault(dtc_fault=DTCFault.RelHumSnsrErr,last_time=1)
#     #     self.sd_tester.dtc_read_and_check(dtc=DTCFault.RelHumSnsrErr, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
#
#     @allure.title("OHC丢失LIN响应_DTC_D30787")
#     @pytest.mark.full
#     def test_dtc_1989186(self):
#         ccp = {
#             "venus800": {950: 0x2, 636: 0x2},
#             "venus": {950: 0x02, 636: 0x01},
#             "MarsOne_MCA": {950: 0x01, 636: 0x02},
#             "MarsOne": {950: 0x01, 636: 0x01}
#         }
#         for car_mode, car_ccp in ccp.items():
#             self.sd_tester.write_ccp(car_ccp)
#             sleep(1)
#             self.bus_comm.pause_OHC(wait_time=10)
#             self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCLossLin, dtc_sts=DTCSts.CurrentFailed)
#             # self.sd_tester.send_data([0x19, 0x04, 0xD3, 0x07, 0x87, 0x20])
#             sleep(1)
#             self.bus_comm.resume_OHC(wait_time=20)
#             self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCLossLin, dtc_sts=DTCSts.FullWithHistory)
#
#     @pytest.mark.full
#     @pytest.mark.parametrize(
#         "alm_num",
#         [1, 2, 3, 4, 5, 6],
#         ids=[1986835, 1986832, 1986829, 1986826, 1986823, 1989827]
#     )
#     def test_dtc_alm_led_fault_caseid_(self, alm_num):
#         allure.dynamic.title(f"451482_ALM{alm_num}_LED_DTC")
#         ccp = {
#             "venus800": {950: 0x2, 636: 0x2},
#             "venus": {950: 0x02, 636: 0x01},
#             "MarsOne_MCA": {950: 0x01, 636: 0x02},
#             "MarsOne": {950: 0x01, 636: 0x01}
#         }
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_led_fault(alm_num, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=getattr(DTCFault, f"ALM{alm_num}Fault_LED"), dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_led_fault(alm_num, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=getattr(DTCFault, f"ALM{alm_num}Fault_LED"), dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @pytest.mark.full
#     @pytest.mark.parametrize(
#         "alm_num",
#         [1, 2, 3, 4, 5, 6],
#         ids=[1991448, 1986831, 1986828, 1986825, 1986822, 1989854]
#     )
#     def test_dtc_alm_vlt_fault_caseid_(self, alm_num):
#         allure.dynamic.title(f"451482_ALM{alm_num}_Vlt_DTC")
#         ccp = {
#             "venus800": {950: 0x2, 636: 0x2},
#             "venus": {950: 0x02, 636: 0x01},
#             "MarsOne_MCA": {950: 0x01, 636: 0x02},
#             "MarsOne": {950: 0x01, 636: 0x01}
#         }
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_vlt_fault(alm_num, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=getattr(DTCFault, f"ALM{alm_num}Fault_Vlt"), dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_vlt_fault(alm_num, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=getattr(DTCFault, f"ALM{alm_num}Fault_Vlt"), dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @pytest.mark.full
#     @pytest.mark.parametrize(
#         "alm_num",
#         [1, 2, 3, 4, 5, 6],
#         ids=[1986833, 1986830, 1986828, 1986824, 1986821, 1989853]
#     )
#     def test_dtc_alm_tmp_fault_caseid_(self, alm_num):
#         allure.dynamic.title(f"451482_ALM{alm_num}_Tmp_DTC")
#         ccp = {
#             "venus800": {950: 0x2, 636: 0x2},
#             "venus": {950: 0x02, 636: 0x01},
#             "MarsOne_MCA": {950: 0x01, 636: 0x02},
#             "MarsOne": {950: 0x01, 636: 0x01}
#         }
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_tmp_fault(alm_num, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=getattr(DTCFault, f"ALM{alm_num}Fault_Tmp"), dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_tmp_fault(alm_num, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=getattr(DTCFault, f"ALM{alm_num}Fault_Tmp"), dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @allure.title("451482_ALM7_DTC_Led")
#     @pytest.mark.full
#     def test_dtc_ALM7Fault_caseid_1989828(self):
#         ccp = {"venus": {950: 0x02, 636: 0x01},
#                "venus800": {950: 0x02, 636: 0x02},
#                "MarsOne_MCA": {950: 0x01, 636: 0x02}}
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_led_fault(7, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM7Fault_LED, dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_led_fault(7, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM7Fault_LED, dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @allure.title("451482_ALM7_DTC_Vlt")
#     @pytest.mark.full
#     def test_dtc_ALM7Fault_caseid_1989847(self):
#         ccp = {"venus": {950: 0x02, 636: 0x01},
#                "venus800": {950: 0x02, 636: 0x02},
#                "MarsOne_MCA": {950: 0x01, 636: 0x02}}
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_vlt_fault(7, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM7Fault_Vlt, dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_vlt_fault(7, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM7Fault_Vlt, dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @allure.title("451482_ALM7_DTC_Tmp")
#     @pytest.mark.full
#     def test_dtc_ALM7Fault_caseid_1989844(self):
#         ccp = {"venus": {950: 0x02, 636: 0x01},
#                "venus800": {950: 0x02, 636: 0x02},
#                "MarsOne_MCA": {950: 0x01, 636: 0x02}}
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_tmp_fault(7, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM7Fault_Tmp, dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_tmp_fault(7, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM7Fault_Tmp, dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @allure.title("451482_ALM8_DTC_Led")
#     @pytest.mark.full
#     def test_dtc_ALM8Fault_caseid_1989829(self):
#         ccp = {"venus": {950: 0x02, 636: 0x01},
#                "venus800": {950: 0x02, 636: 0x02},
#                "MarsOne_MCA": {950: 0x01, 636: 0x02}}
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_led_fault(8, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM8Fault_LED, dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_led_fault(8, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM8Fault_LED, dtc_sts=DTCSts.FullWithHistory
#             )
#
#     @allure.title("451482_ALM8_DTC_Vlt")
#     @pytest.mark.full
#     def test_dtc_ALM8Fault_caseid_1989852(self):
#         ccp = {"venus": {950: 0x02, 636: 0x01},
#                "venus800": {950: 0x02, 636: 0x02},
#                "MarsOne_MCA": {950: 0x01, 636: 0x02}}
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_vlt_fault(8, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM8Fault_Vlt, dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_vlt_fault(8, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM8Fault_Vlt, dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @allure.title("451482_ALM8_DTC_Tmp")
#     @pytest.mark.full
#     def test_dtc_ALM8Fault_caseid_1989850(self):
#         ccp = {"venus": {950: 0x02, 636: 0x01},
#                "venus800": {950: 0x02, 636: 0x02},
#                "MarsOne_MCA": {950: 0x01, 636: 0x02}}
#         for car_mode, car_ccp in ccp.items():
#             with allure.step("车型：" + car_mode):
#                 self.sd_tester.write_ccp(car_ccp)
#                 sleep(2)
#             self.bus_comm.set_alm_tmp_fault(8, 1)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM8Fault_Tmp, dtc_sts=DTCSts.CurrentFailed
#             )
#             self.bus_comm.set_alm_tmp_fault(8, 0)
#             self.sd_tester.dtc_read_and_check(
#                 dtc=DTCFault.ALM8Fault_Tmp, dtc_sts=DTCSts.FullWithHistory
#             )
#             sleep(1)
#
#     @allure.title("451482_ALM9_DTC_Led")
#     @pytest.mark.full
#     def test_dtc_ALM9Fault_caseid_1989830(self):
#         self.sd_tester.write_ccp({950: 0x2, 636: 0x2})
#         self.bus_comm.set_alm_led_fault(9, 1)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM9Fault_LED, dtc_sts=DTCSts.CurrentFailed
#         )
#         self.bus_comm.set_alm_led_fault(9, 0)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM9Fault_LED, dtc_sts=DTCSts.FullWithHistory
#         )
#
#     @allure.title("451482_ALM9_DTC_Vlt")
#     @pytest.mark.full
#     def test_dtc_ALM9Fault_caseid_1989857(self):
#         self.sd_tester.write_ccp({950: 0x2, 636: 0x2})
#         self.bus_comm.set_alm_vlt_fault(9, 1)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM9Fault_Vlt, dtc_sts=DTCSts.CurrentFailed
#         )
#         self.bus_comm.set_alm_vlt_fault(9, 0)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM9Fault_Vlt, dtc_sts=DTCSts.FullWithHistory
#         )
#
#     @allure.title("451482_ALM9_DTC_Tmp")
#     @pytest.mark.full
#     def test_dtc_ALM9Fault_caseid_1989855(self):
#         self.sd_tester.write_ccp({950: 0x2, 636: 0x2})
#         self.bus_comm.set_alm_tmp_fault(9, 1)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM9Fault_Tmp, dtc_sts=DTCSts.CurrentFailed
#         )
#         self.bus_comm.set_alm_tmp_fault(9, 0)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM9Fault_Tmp, dtc_sts=DTCSts.FullWithHistory
#         )
#
#     @allure.title("451482_ALM10_DTC_Led")
#     @pytest.mark.full
#     def test_dtc_ALM10Fault_caseid_1986750(self):
#         self.sd_tester.write_ccp({950: 0x2, 636: 0x2})
#         self.bus_comm.set_alm_led_fault(10, 1)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM10Fault_LED, dtc_sts=DTCSts.CurrentFailed
#         )
#         self.bus_comm.set_alm_led_fault(10, 0)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM10Fault_LED, dtc_sts=DTCSts.FullWithHistory
#         )
#
#     @allure.title("451482_ALM10_DTC_Vlt")
#     @pytest.mark.full
#     def test_dtc_ALM9Fault_caseid_1986749(self):
#         self.sd_tester.write_ccp({950: 0x2, 636: 0x2})
#         self.bus_comm.set_alm_vlt_fault(10, 1)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM10Fault_Vlt, dtc_sts=DTCSts.CurrentFailed
#         )
#         self.bus_comm.set_alm_vlt_fault(10, 0)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM10Fault_Vlt, dtc_sts=DTCSts.FullWithHistory
#         )
#
#     @allure.title("451482_ALM10_DTC_Tmp")
#     @pytest.mark.full
#     def test_dtc_ALM9Fault_caseid_1986748(self):
#         self.sd_tester.write_ccp({950: 0x2, 636: 0x2})
#         self.bus_comm.set_alm_tmp_fault(10, 1)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM10Fault_Tmp, dtc_sts=DTCSts.CurrentFailed
#         )
#         self.bus_comm.set_alm_tmp_fault(10, 0)
#         self.sd_tester.dtc_read_and_check(
#             dtc=DTCFault.ALM10Fault_Tmp, dtc_sts=DTCSts.FullWithHistory
#         )
#
#     @allure.title("验证DSGL-Supply电压太高的DTC故障码A03417")
#     @pytest.mark.full
#     def test_dtc_DSGL_vol_high_caseid_1988220(self):
#         self.sd_tester.write_ccp({183: 0x84, 1532: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltHiVoltDetdFlt", 1)
#         sleep(2)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLVolHigh, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltHiVoltDetdFlt", 0)
#         sleep(2)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLVolHigh, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("验证DSGL-Supply电压太低的DTC故障码A03416")
#     @pytest.mark.full
#     def test_dtc_DSGL_vol_low_caseid_1986842(self):
#         self.sd_tester.write_ccp({183: 0x84, 1532: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltLoVoltDetdFlt", 1)
#         sleep(2)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLVolLow, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltLoVoltDetdFlt", 0)
#         sleep(2)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLVolLow, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("验证DSGL-温度太高的DTC故障码A0344B")
#     @pytest.mark.full
#     def test_dtc_DSGL_tmp_high_caseid_1986840(self):
#         self.sd_tester.write_ccp({183: 0x84, 1532: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltTpmFlt", 1)
#         sleep(2)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLTempHigh, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltTpmFlt", 0)
#         sleep(2)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLTempHigh, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("验证DSGL-LED故障（短路或开路）的DTC故障码A03414")
#     @pytest.mark.full
#     def test_dtc_DSGL_led_fail_caseid_1986841(self):
#         self.sd_tester.write_ccp({183: 0x84, 1532: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltLEDsFlt", 1)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLLedFail, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "DsglCem_Lin3Fr01", "DSGLIntFltLEDsFlt", 0)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.DSGLLedFail, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("验证PSGL-Supply电压太高的DTC故障码A03517")
#     @pytest.mark.full
#     def test_dtc_PSGL_vol_high_caseid_1986839(self):
#         self.sd_tester.write_ccp({183: 0x84, 1531: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltHiVoltDetdFlt", 1)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLVolHigh, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltHiVoltDetdFlt", 0)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLVolHigh, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("验证PSGL-Supply电压太低的DTC故障码A03516")
#     @pytest.mark.full
#     def test_dtc_PSGL_vol_low_caseid_1986838(self):
#         self.sd_tester.write_ccp({183: 0x84, 1531: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltLoVoltDetdFlt", 1)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLVolLow, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltLoVoltDetdFlt", 0)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLVolLow, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("验证PSGL-温度太高的DTC故障码A0354B")
#     @pytest.mark.full
#     def test_dtc_PSGL_tmp_high_caseid_1986836(self):
#         self.sd_tester.write_ccp({183: 0x84, 1531: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltTpmFlt", 1)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLTempHigh, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltTpmFlt", 0)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLTempHigh, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("验证PSGL-LED故障（短路或开路）的DTC故障码A03514")
#     @pytest.mark.full
#     def test_dtc_PSGL_led_fail_caseid_1986837(self):
#         self.sd_tester.write_ccp({183: 0x84, 1531: 0x02})
#         sleep(1)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltLEDsFlt", 1)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLLedFail, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "PsglCem_Lin3Fr01", "PSGLIntFltLEDsFlt", 0)
#         sleep(3)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.PSGLLedFail, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("OHC第二排左内灯按钮卡滞_DTC_A07271")
#     @pytest.mark.full
#     def test_dtc_LiBtnReadingLe_caseid_1991368(self):
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "BtnStsOHCRLiBtnReadingLe", 1)
#         sleep(70)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCRLiBtnReadingLe, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "BtnStsOHCRLiBtnReadingLe", 0)
#         sleep(5)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCRLiBtnReadingLe, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("OHC第二排右内灯按钮卡滞_DTC_A07371")
#     @pytest.mark.full
#     def test_dtc_LiBtnReadingRi_caseid_1991369(self):
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "BtnStsOHCRLiBtnReadingRi", 1)
#         sleep(70)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCRLiBtnReadingRi, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "BtnStsOHCRLiBtnReadingRi", 0)
#         sleep(5)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCRLiBtnReadingRi, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("OHC左前内灯按钮卡滞_DTC_A07071")
#     @pytest.mark.full
#     def test_dtc_OHCLiBtnReadingLe_caseid_1991366(self):
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr04", "BtnStsOHCLiBtnReadingLe", 1)
#         sleep(70)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCLiBtnReadingLe, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr04", "BtnStsOHCLiBtnReadingLe", 0)
#         sleep(5)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCLiBtnReadingLe, dtc_sts=DTCSts.FullWithHistory)
#
#     @allure.title("OHC右前内灯按钮卡滞_DTC_A07071")
#     @pytest.mark.full
#     def test_dtc_OHCLiBtnReadingRi_caseid_1991367(self):
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr04", "BtnStsOHCLiBtnReadingRi", 1)
#         sleep(70)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCLiBtnReadingRi, dtc_sts=DTCSts.CurrentFailed)
#         self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr04", "BtnStsOHCLiBtnReadingRi", 0)
#         sleep(5)
#         self.sd_tester.dtc_read_and_check(dtc=DTCFault.OHCLiBtnReadingRi, dtc_sts=DTCSts.FullWithHistory)
#
#     def test_dtc_missALM1_6(self):
#         ccp = {
#             "venus800": {950: 0x2, 636: 0x2},
#             "venus": {950: 0x02, 636: 0x01},
#             "MarsOne_MCA": {950: 0x01, 636: 0x02},
#             "MarsOne": {950: 0x01, 636: 0x01}
#         }
#         alm_lst = ["ALM" + str(i) for i in range(1, 7)]
#         for car_mode, car_ccp in ccp.items():
#             self.sd_tester.write_ccp(car_ccp)
#             for alm in alm_lst:
#                 sleep(1)
#                 self.bus_comm.pause_ecu_send("cem_lin5", "ALM1")
#                 sleep(10)
#                 self.sd_tester.dtc_read_and_check(
#                     dtc=getattr(DTCFault, alm + "missLin"),
#                     dtc_sts=DTCSts.CurrentFailed
#                 )
#                 sleep(1)
#                 self.bus_comm.resume_ecu_send("cem_lin5", "ALM1")
#                 sleep(10)
#                 self.sd_tester.dtc_read_and_check(
#                     dtc=getattr(DTCFault, alm + "missLin"),
#                     dtc_sts=DTCSts.FullWithHistory
#                 )
#
#     def test_dtc_missALM7_MarsOneMCA(self):
#         with allure.step("车型：MarsOneMCA"):
#             self.sd_tester.write_ccp({950: 0x01, 636: 0x02})
#         with allure.step("当前为ALM7"):
#             sleep(1)
#         self.bus_comm.pause_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM7missLin"),
#             dtc_sts=DTCSts.CurrentFailed
#         )
#         sleep(1)
#         self.bus_comm.resume_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM7missLin"),
#             dtc_sts=DTCSts.FullWithHistory
#         )
#
#     def test_dtc_missALM7_venus(self):
#         with allure.step("车型：venus"):
#             self.sd_tester.write_ccp({950: 0x02, 636: 0x01})
#         with allure.step("当前为ALM7"):
#             sleep(1)
#         self.bus_comm.pause_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM7missLin"),
#             dtc_sts=DTCSts.CurrentFailed
#         )
#         sleep(1)
#         self.bus_comm.resume_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM7missLin"),
#             dtc_sts=DTCSts.FullWithHistory
#         )
#
#     def test_dtc_missALM8_venus(self):
#         with allure.step("车型：venus"):
#             self.sd_tester.write_ccp({950: 0x02, 636: 0x01})
#         with allure.step("当前为ALM8"):
#             sleep(1)
#         self.bus_comm.pause_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM8missLin"),
#             dtc_sts=DTCSts.CurrentFailed
#         )
#         sleep(1)
#         self.bus_comm.resume_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM8missLin"),
#             dtc_sts=DTCSts.FullWithHistory
#         )
#
#     def test_dtc_missALM8_MarsOneMCA(self):
#         with allure.step("车型：MarsOneMCA"):
#             self.sd_tester.write_ccp({950: 0x01, 636: 0x02})
#         with allure.step("当前为ALM8"):
#             sleep(1)
#         self.bus_comm.pause_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM8missLin"),
#             dtc_sts=DTCSts.CurrentFailed
#         )
#         sleep(1)
#         self.bus_comm.resume_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM8missLin"),
#             dtc_sts=DTCSts.FullWithHistory
#         )
#
#     def test_dtc_missALM9_venus800(self):
#         with allure.step("车型：venus"):
#             self.sd_tester.write_ccp({950: 0x02, 636: 0x02})
#         with allure.step("当前为ALM9"):
#             sleep(1)
#         self.bus_comm.pause_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM9missLin"),
#             dtc_sts=DTCSts.CurrentFailed
#         )
#         sleep(1)
#         self.bus_comm.resume_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM9missLin"),
#             dtc_sts=DTCSts.FullWithHistory
#         )
#
#     def test_dtc_missALM10_venus800(self):
#         with allure.step("车型：venus"):
#             self.sd_tester.write_ccp({950: 0x02, 636: 0x02})
#         with allure.step("当前为ALM10"):
#             sleep(1)
#         self.bus_comm.pause_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM10missLin"),
#             dtc_sts=DTCSts.CurrentFailed
#         )
#         sleep(1)
#         self.bus_comm.resume_ecu_send("cem_lin5", "ALM1")
#         sleep(10)
#         self.sd_tester.dtc_read_and_check(
#             dtc=getattr(DTCFault, "ALM10missLin"),
#             dtc_sts=DTCSts.FullWithHistory
#         )
