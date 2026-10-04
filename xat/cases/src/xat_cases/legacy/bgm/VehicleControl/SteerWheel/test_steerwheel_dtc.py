# """
# @File        : test_steerwheel_dtc.py
# @Author      : xiangyue.li@jiduauto.com
# @Time        : 2024/05/10 15:12
# @Description : 方向盘DTC

# """

# import os
# import sys
# import pytest
# import allure
# from time import sleep

# sys.path.append(os.getcwd())
# sys.path.append(os.path.join(os.getcwd(), ".."))
# sys.path.append(os.path.join(os.getcwd(), "../.."))
# sys.path.append(os.path.join(os.getcwd(), "../../.."))
# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
# from sdk_interface.abc_interface import *

# @allure.feature("车控车设")
# @allure.story("方向盘功能")
# @pytest.mark.tailwing
# class TestClimateCtrlDtc(TestABCBase):
#     def before_class(self, ecu):
#         # self.soa.update(["CentralLockService_client","ClimateControlService_client","VehicleSetStatusService_client","TailGateService_client","ResetSOAConfigService_client","CentralLockService_client",
#         #         "KeyService_client",
#         #         "DoorService_client",
#         #         "SteerWheelService_client"])
#         sleep(1)
#         self.sd_tester.write_ccp(ccp={564:0x2,642: 0x3})

#     def before_each_func(self, ecu):   
#         self.mix.set_dtc_precontion()
#         self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x08])

#     def after_each_func(self, ecu):
#         try:
#             self.sd_tester.clear_all_dtc_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L0, '54')
#         except Exception as e:
#             logger.info(f"----------> after_class Error{str(e)}")
#             pass

#     def after_class(self, ecu):
#         try:
#             self.mix.set_common_precontion(
#                 usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
#             )
#         except Exception as e:
#             logger.info(f"----------> after_class Error{str(e)}")
#             pass

#     @allure.title("DTC_可调方向盘模块(ASWM)机械故障电路对地短(D32471)")
#     @pytest.mark.smoke
#     def test_caseid_1982737(self):
#         # self.bus_comm.set_singal("cem_lin4","AswmCem_Lin4Fr01","WhlFailrSts",1)
#         # sleep(5)
#         # self.sd_tester.dtc_read_and_check(dtc=DTCFault.HWErrorInTheActuationCircuit, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)
#         # sleep(10)
#         # self.bus_comm.set_singal("cem_lin4","AswmCem_Lin4Fr01","WhlFailrSts",0)
#         # self.sd_tester.dtc_read_and_check(dtc=DTCFault.HWErrorInTheActuationCircuit, dtc_sts=DTCSts.FullWithHistory, fault_sts=True)
#         # sleep(10)
#         # self.bus_comm.set_singal("cem_lin4","AswmCem_Lin4Fr01","WhlFailrSts",0)
#         # self.sd_tester.dtc_read_and_check(dtc=DTCFault.HWErrorInTheActuationCircuit, dtc_sts=DTCSts.WithHistoryWithoutCurrent, fault_sts=True)
