# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# @File         :test_xcall.py
# @Time         :2023/12/11 10:04
# @Author       :yunpeng.zhou@jiduauto.com
# @Description  :
# """

# import time
# import allure
# import pytest

# from test_case.abc_demo.case_helper.test_abc_base import TestABCBase
# from sdk_interface.abc_interface import *


# @allure.feature("互联服务")
# @allure.story("呼叫服务")
# class TestXcall(TestABCBase):

#     def before_class(self, ecu):
#         self.soa.update(["CallService_client"])
#         sleep(2)
#         self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3)
#         super().before_class(self, ecu)

#     def before_each_func(self, ecu):
#         super().before_each_func(ecu)

#     def after_each_func(self, ecu):
#         self.ssh.set_airplane_mode(isOn.Off)
#         # self.soa.hang_up_call_sos()
#         super().after_each_func(ecu)

#     def after_class(self, ecu):
#         super().after_class(self, ecu)
        

#     @pytest.mark.join_smoke
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199622?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_send_call_status_activecall_SOS_cancel")
#     def test_ecall_caseid_1898410_101330(self):
#         with allure.step('1.通过SOS触发Ecall'):
#             self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kCDC)
#         # 7.5s以内有两个按钮（取消或者挂断）
#         # 7.5s以后只有挂断
#         sleep(5)
#         with allure.step('2.在eCallCountTi_TCAM(7.5s)时间内，再次按压SOS按键挂断Ecall'):
#             self.soa.cancel_call_sos(ReqSrc=eCallReqSource.kCDC)

#     @pytest.mark.join_smoke
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199643?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Active_triggered_by_SOS_button")
#     def test_ecall_caseid_1898337_101320(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 1",  # 正在拨号
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 2, Type = 1",  # 正在响铃
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 1",  # 已挂断
#         ], timeout=30):
#             self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kCDC)
#             # 接通后20s挂断
#             sleep(20)
#             self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kCDC)
    
#     @pytest.mark.join_smoke
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199643?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Active_triggered_by_SOS_button")
#     def test_ecall_caseid_101319(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 1",  # 正在拨号
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 2, Type = 1",  # 正在响铃
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 1",  # 已挂断
#         ], timeout=30):
#             self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kCDC)
#             sleep(4)
#             self.soa.confirm_call_sos()
#             # 接通后15s挂断
#             sleep(15)
#             self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kCDC)


#     @pytest.mark.join_smoke
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199643?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_send_call_status_passivecall_ACU_success")
#     def test_ecall_caseid_1898388(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 2",  # 正在拨号
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 3, Type = 2",  # 正在响铃
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 2",  # 已挂断
#         ], timeout=30):
#             with allure.step('1.通过SOA接口发送[API:SetECallWorkStatus].eCallOperationCmd==START_ECALL触发Ecall话'):
#                 self.soa.trigger_call_sos_by_soa_partner(ReqSrc=eCallReqSource.kACU, type=eCallType.kPASSIVE, status=eCallSts.kDIALING)
#                 self.soa.confirm_call_sos()
#             # 接通后20s挂断
#             sleep(20)
#             with allure.step('2.通话30s后，模拟acu发送挂断消息'):
#                 self.soa.hang_up_call_sos(ReqSrc=eCallReqSource.kACU, type=eCallType.kPASSIVE,status=eCallSts.kHANG_UP)

#     @pytest.mark.join_smoke
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199643?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Passive_triggered_by_CarMode_Crash")
#     def test_ecall_caseid_1898378(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 2",  # 正在拨号
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 3, Type = 2",  # 正在响铃
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 2",  # 已挂断
#         ], timeout=30):
#             self.mix.trigger_call_sos_by_crash()
#             # 接通后10s挂断
#             sleep(10)
#             self.soa.hang_up_call_sos(type=eCallType.kPASSIVE, status=eCallSts.kHANG_UP)
    
#     @pytest.mark.join_sanity
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199643?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Passive_triggered_by_Can_Signal_Crash")
#     def test_ecall_caseid_1898333(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 2",  # 正在拨号
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 3, Type = 2",  # 正在响铃
#             "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 2",  # 已挂断
#         ], timeout=30):
#             self.bus_comm.trigger_call_sos_by_can()
#             # 接通后10s挂断
#             sleep(10)
#             self.soa.hang_up_call_sos(type=eCallType.kPASSIVE, status=eCallSts.kHANG_UP)
    
#     # @pytest.mark.sanity
#     # @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199643?projectId=46")
#     # @allure.title("互联服务_呼叫服务_Ecall_Active_interrupted_by_SRS_Signal")
#     # def test_ecall_caseid_1898371(self):
#     #     with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#     #                                                   keywords=[
#     #         "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 2",  # 正在拨号
#     #         "UpdateNotifyECallStatus FunctionSts = 0, Status = 3, Type = 2",  # 正在响铃
#     #         "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 2",  # 已挂断
#     #     ], timeout=40):
#     #         self.bus_comm.trigger_call_sos_by_pwm(run_time=6000, lin_bus=LinChannel.LIN2, dutyCycle=550)
#     #         # 接通后10s挂断
#     #         sleep(10)
#     #         self.soa.hang_up_call_sos(type=eCallType.kPASSIVE, status=eCallSts.kHANG_UP)

#     @pytest.mark.join_full
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199643?projectId=46")
#     @allure.title("互联服务_呼叫服务_Bcall_Active_triggered_by_partner")
#     def test_ecall_caseid_1898402(self):
#         # 设置BCALL触发前置条件
#         self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
#         self.soa.trigger_bcall_sos(bCallOperCmd.kSTART_BCALL)
#         # 接通后20s挂断
#         sleep(20)
#         self.soa.trigger_bcall_sos(bCallOperCmd.kHANG_UP_BCALL)

#     @pytest.mark.join_full
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199654?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Passive_retry_twice")
#     def test_ecall_caseid_1898318(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#                     # 第一次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 第二次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 关闭飞行模式呼叫成功
#                     "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 2",  # 正在拨号
#                     "UpdateNotifyECallStatus FunctionSts = 0, Status = 3, Type = 2",  # 正在响铃
#                     "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 2",  # 已挂断
#                 ],
#                 timeout=130
#         ):
#             self.ssh.set_airplane_mode(isOn.On)
#             with allure.step('1.第一次开始呼叫'):
#                 self.bus_comm.trigger_call_sos_by_can()
#                 sleep(60)
#             with allure.step('2.关闭飞行模式'):
#                 self.ssh.set_airplane_mode(isOn.Off)
#                 sleep(20)
#                 self.soa.hang_up_call_sos(type=eCallType.kPASSIVE)

#     @pytest.mark.join_full
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199655?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Passive_retry_three_times")
#     def test_ecall_caseid_1898319(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                 keywords=[
#                     # 第一次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 第二次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 第三次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 三次呼叫后，呼叫异常失败
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 5, Type = 2"   # 呼叫异常失败
#                 ],
#                 timeout=190
#         ):
#             self.ssh.set_airplane_mode(isOn.On)
#             self.bus_comm.trigger_call_sos_by_can()

#     @pytest.mark.join_full
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199653?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Passive_retry_once")
#     def test_ecall_caseid_1898317(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#                     # 第一次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 关闭飞行模式呼叫成功
#                     "UpdateNotifyECallStatus FunctionSts = 0, Status = 1, Type = 2",  # 正在拨号
#                     "UpdateNotifyECallStatus FunctionSts = 0, Status = 3, Type = 2",  # 正在响铃
#                     "UpdateNotifyECallStatus FunctionSts = 0, Status = 5, Type = 2",  # 已挂断
#                 ],
#                 timeout=140
#         ):
#             self.ssh.set_airplane_mode(isOn.On)
#             with allure.step('1.第一次开始呼叫'):
#                 self.bus_comm.trigger_call_sos_by_can()
#                 sleep(60)
#             self.ssh.set_airplane_mode(isOn.Off)
#             sleep(5)
#             self.soa.hang_up_call_sos(type=eCallType.kPASSIVE)

#     @pytest.mark.join_full
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199653?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Passive_fail_reboot")
#     def test_ecall_caseid_1898320(self):
#         with self.log_manage.check_jetlog_by_keywords(log_type='EcallService.cpp',
#                                                       keywords=[
#                     # 第一次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 第二次呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 2, Status = 1, Type = 2",  # 正在拨号
#                     # 重启后不再尝试呼叫
#                     "UpdateNotifyECallStatus FunctionSts = 0, Status = 0, Type = 0",  # 正在拨号
#                 ],
#                 timeout=260
#         ):
#             self.ssh.set_airplane_mode(isOn.On)
#             with allure.step('1.第一次开始呼叫'):
#                 self.bus_comm.trigger_call_sos_by_can()
#                 sleep(10)
#             with allure.step('2.重启TCAM'):
#                 self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
#         self.soa.chk_xcall_notify()

#     @pytest.mark.join_full
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199618?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Self_test_without_error")
#     def test_ecall_caseid_1898125(self):
#         self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
#         sleep(0.5)
#         self.soa.chk_xcall_in_self_test_notify()

#     @pytest.mark.join_full
#     @allure.testcase("https://jama.jiduauto.com/perspective.req#/testCases/1199618?projectId=46")
#     @allure.title("互联服务_呼叫服务_Ecall_Self_test_with_SIM_Error")
#     def test_ecall_caseid_101340(self):
#         self.ssh.set_airplane_mode(isOn.On)
#         sleep(5)
#         self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
#         sleep(0.5)
#         self.soa.chk_xcall_in_self_test_notify(eCallFunSts.kECALL_ERROR_SEVERE)


# if __name__ == '__main__':
#     pytest.main()

# # pytest -sv xcall/test_xcall_abc.py -k test_ecall_caseid_1898378
