# # !/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# @File         :test_alm_calibration.py
# @Time         :10/23/24 8:16 PM
# @Author       :yucheng.zhu@jiduauto.com
# @Description  :
# """
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
#
#
# @allure.feature("车控车设")
# @allure.story("内灯功能")
# class TestIntrlightCtrl(TestABCBase):
#     def before_class(self, ecu):
#         self.soa.update(["VehicleSetStatusService_client", "VehicleModeService_client", "ObtDiagService_client", "KeyService_client"])
#         self.tsp.get_remote_diag_token()
#         self.sd_tester.stop_tester_present()
#         time.sleep(5)
#
#     def before_each_func(self, ecu):
#         """
#         解锁、Normal、Conv、关5门、夜晚、P挡、无占座
#         @param ecu:
#         @return:
#         """
#         self.sd_tester.write_ccp(ccp={950: 0x1, 636: 0x2, 964: 0x1})
#         sleep(2)
#         self.io.bgm_diag_line_down()
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#
#     def after_each_func(self, ecu):
#         # self.soa.set_auto_calibration(req=calibration_req.kOff, source=SourceType.kScreen, isAlloweSkip=False)
#         time.sleep(0.5)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
#         self.io.set_five_door_sts(sts=Door.close)
#         self.io.driver_seat_notpresent()
#         self.bus_comm.set_secle_seat_notpresent()
#         self.bus_comm.set_pass_seat_notpresent()
#         self.io.hazard_light_close()
#         self.io.bgm_diag_line_up()
#         sleep(1)
#
#     def after_class(self, ecu):
#         time.sleep(0.5)
#
#     @allure.title("智能标定_氛围灯_远程_判断竞争任务_有低优先级诊断任务")
#     @pytest.mark.full
#     def test_caseid_1995936(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#
#     @pytest.mark.sanity
#     @allure.title("智能标定_氛围灯_前提条件判断-车辆N挡-静止-无需授权-重试条件满足")
#     def test_caseid_1995926(self):
#         self.bus_comm.set_gear_pos(gear=Gear.Neut)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(10)
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         sleep(1)
#         self.soa.set_Calibration_Retry()
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(10)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆D挡-运动-需要授权-重试条件满足")
#     def test_caseid_1995923(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Drv)
#         self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
#         sleep(3)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(3)
#         self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
#         self.mix.set_usage_mode(UsageMode.CONVENIENCE)
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         sleep(3)
#         self.soa.set_Calibration_Retry()
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(10)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆D挡-静止-需要授权-重试条件满足")
#     def test_caseid_1995927(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Drv)
#         sleep(2)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(3)
#         self.mix.set_usage_mode(UsageMode.CONVENIENCE)
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         sleep(2)
#         self.soa.set_Calibration_Retry()
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(10)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆R挡-运动-需要授权-重试条件满足")
#     def test_caseid_1995922(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Rvs)
#         self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
#         sleep(2)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(3)
#         self.mix.set_usage_mode(UsageMode.CONVENIENCE)
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.bus_comm.set_vehmtn()
#         sleep(2)
#         self.soa.set_Calibration_Retry()
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(10)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆R挡-静止-无需授权-重试取消")
#     def test_caseid_1995929(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Rvs)
#         sleep(2)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(5)
#         self.soa.set_Calibration_Retry(retry_req.kCancel)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_前提条件判断-车辆N挡-运动-无需授权-重试条件满足")
#     def test_caseid_1995921(self):
#         self.bus_comm.set_gear_pos(gear=Gear.Neut)
#         self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
#         sleep(2)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(10)
#         self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         sleep(2)
#         self.soa.set_Calibration_Retry()
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(10)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆N挡-静止-无需授权-超时无重试")
#     def test_caseid_1995931(self):
#         self.bus_comm.set_gear_pos(gear=Gear.Neut)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(30)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionTimeout,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆D挡-静止-需要授权-重试条件还不满足")
#     def test_caseid_1995925(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Drv)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(10)
#         self.soa.set_Calibration_Retry()
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆R挡-静止-无需授权-重试条件还不满足")
#     def test_caseid_1995924(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Rvs)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(2)
#         self.soa.set_Calibration_Retry()
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @pytest.mark.seq
#     @allure.title("智能标定_氛围灯_远程-前提条件判断-车辆D挡-静止-需要授权-超时无重试")
#     def test_caseid_1995930(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Drv)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(30)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionTimeout,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.sanity
#     @allure.title("智能标定_氛围灯_前提条件判断-车辆N挡-静止-需要授权-重试取消")
#     def test_caseid_1995928(self):
#         self.bus_comm.set_gear_pos(gear=Gear.Neut)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(28)
#         self.soa.set_Calibration_Retry(retry_req.kCancel)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_屏幕-授权请求-无需授权")
#     @pytest.mark.sanity
#     def test_caseid_1995914(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程_授权请求_无需授权")
#     @pytest.mark.sanity
#     def test_caseid_1995935(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程_授权请求_需授权_授权通过")
#     @pytest.mark.sanity
#     def test_caseid_1995934(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程_有高优先级诊断任务_无需授权")
#     @pytest.mark.sanity
#     def test_caseid_1996189(self):
#         self.io.bgm_diag_line_up()
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程_有高优先级诊断任务_需要授权")
#     @pytest.mark.full
#     @pytest.mark.seq
#     def test_caseid_1996207(self):
#         self.io.bgm_diag_line_up()
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(4)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_屏幕-授权请求-需授权-授权通过")
#     @pytest.mark.sanity
#     def test_caseid_1995913(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_屏幕_D挡")
#     def test_caseid_1995703(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Drv)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(30)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionTimeout,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程_R挡")
#     def test_caseid_1995702(self):
#         self.mix.set_usage_mode(UsageMode.DRIVING)
#         self.bus_comm.set_gear_pos(gear=Gear.Rvs)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCheckPreconditionFailed,
#                                                      functionID=CalibrationFunctionID.ALM, text_id=0)
#         sleep(30)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kCheckPreconditionTimeout,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_屏幕_mars不含头枕音响含CC下方灯带")
#     @pytest.mark.sanity
#     def test_caseid_1995704(self):
#         self.sd_tester.write_ccp(ccp={950: 0x1, 636: 0x1, 964: 0x1})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         sleep(5)
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_屏幕_mars含头枕音响含CC下方灯带")
#     @pytest.mark.sanity
#     def test_caseid_1995708(self):
#         self.sd_tester.write_ccp(ccp={950: 0x1, 636: 0x2, 964: 0x1})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         self.bus_comm.set_vehspd_gear(vehspd=0.0)
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_屏幕_venus含头枕音响")
#     @pytest.mark.sanity
#     def test_caseid_1995706(self):
#         self.sd_tester.write_ccp(ccp={950: 0x2, 636: 0x2})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         self.bus_comm.set_vehspd_gear(vehspd=0.0)
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程诊断_venus不含头枕音响")
#     @pytest.mark.sanity
#     def test_caseid_1995707(self):
#         self.sd_tester.write_ccp(ccp={950: 0x2, 636: 0x1})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_语音_mars含头枕音响含CC下方灯带")
#     @pytest.mark.manual
#     def test_caseid_1995916(self):
#         self.sd_tester.write_ccp(ccp={950: 0x1, 636: 0x2, 964: 0x1})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_语音_venus不含头枕音响")
#     @pytest.mark.manual
#     def test_caseid_1995915(self):
#         self.sd_tester.write_ccp(ccp={950: 0x2, 636: 0x1, 964: 0x1})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程_mars不头枕音响不含CC下方灯带")
#     @pytest.mark.sanity
#     def test_caseid_1995705(self):
#         self.sd_tester.write_ccp(ccp={950: 0x1, 636: 0x1, 964: 0x0})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程_mars含头枕音响不含CC下方灯带")
#     @pytest.mark.sanity
#     def test_caseid_1995709(self):
#         self.sd_tester.write_ccp(ccp={950: 0x1, 636: 0x2, 964: 0x0})
#         self.io.io_reset_bgm(times=5)
#         sleep(25)
#         self.io.bgm_diag_line_down()
#         self.tsp.send_remote_diag_cmd(cmd_type=CmdType.SessionClose)
#         self.bus_comm.set_vehmtn()
#         self.bus_comm.set_vehspd()
#         self.bus_comm.set_trsm_park_lockd(TrsmParkLockd.ParkEngd)
#         self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Awake)
#         time.sleep(1)
#         self.bus_comm.set_dtc_pre()
#         self.bus_comm.set_gear_pos(gear=Gear.Park)
#         self.mix.service_change_usage_mode_and_check_result(usagemode=UsageMode.INACTIVE)
#         self.mix.s2s_change_car_mode_and_check_result(car_mode=CarMode.NORMAL, car_mode_sub=0)
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(5)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(2)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_屏幕_判断竞争任务_有低优先级诊断任务")
#     @pytest.mark.full
#     def test_caseid_1996206(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(4)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_语音_判断竞争任务_有低优先级诊断任务")
#     @pytest.mark.full
#     def test_caseid_1996203(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(4)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_屏幕_有高优先级诊断任务_无需授权")
#     @pytest.mark.full
#     def test_caseid_1996204(self):
#         self.io.bgm_diag_line_up()
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kHighPriorityRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#
#     @allure.title("智能标定_氛围灯_屏幕_有高优先级诊断任务_需要授权")
#     @pytest.mark.full
#     def test_caseid_1996202(self):
#         self.io.bgm_diag_line_up()
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kHighPriorityRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#
#     @allure.title("智能标定_氛围灯_屏幕_有高优先级诊断任务_无需授权")
#     @pytest.mark.full
#     def test_caseid_1996205(self):
#         self.io.bgm_diag_line_up()
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kHighPriorityRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#
#     @allure.title("智能标定_氛围灯_屏幕_有高优先级诊断任务_需要授权")
#     @pytest.mark.full
#     def test_caseid_1996188(self):
#         self.io.bgm_diag_line_up()
#         sleep(1)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kScreen, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kHighPriorityRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#
#     @allure.title("智能标定_氛围灯_语音-授权请求-无需授权")
#     @pytest.mark.sanity
#     def test_caseid_1995912(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_语音-授权请求-需授权-授权通过")
#     @pytest.mark.full
#     def test_caseid_1995911(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(4)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(2)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#         sleep(3)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-授权请求-需授权-取消授权")
#     def test_caseid_1995933(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kCancelAuthorize)
#         sleep(10)
#         self.soa.set_Calibration_Retry(retry_req.kCancel)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kAuthorizedFailed,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @pytest.mark.full
#     @allure.title("智能标定_氛围灯_远程-授权请求-需授权-授权超时")
#     def test_caseid_1995932(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(30)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kAuthorizedTimeout,
#                                                      functionID=CalibrationFunctionID.ALM)
#         sleep(1)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程-标定过程中5分钟超时-无需授权")
#     @pytest.mark.fail
#     def test_caseid_1995918(self):
#         self.bus_comm.pause_bus_send(bus_name="cem_lin5")
#         sleep(5)
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=True)
#         # self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#         #                                              functionID=CalibrationFunctionID.ALM)
#         sleep(300)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kRoutingTimeout,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#         self.bus_comm.resume_bus_send(bus_name="cem_lin5")
#         sleep(10)
#
#     @allure.title("智能标定_氛围灯_远程-标定过程中5分钟超时-需要授权")
#     @pytest.mark.fail
#     def test_caseid_1995917(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kVoicd, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.bus_comm.pause_bus_send(bus_name="cem_lin5")
#         sleep(300)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kRoutingTimeout,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#         self.bus_comm.wakeup_lin5()
#         sleep(10)
#
#     @allure.title("智能标定_氛围灯_远程-标定过程中取消-无需授权")
#     @pytest.mark.full
#     def test_caseid_1995920(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_auto_calibration(req=calibration_req.kOff, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kUserCancelRoutine,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
#
#     @allure.title("智能标定_氛围灯_远程-标定过程中取消-需要授权")
#     @pytest.mark.full
#     def test_caseid_1995919(self):
#         self.soa.set_auto_calibration(req=calibration_req.KOn, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=False)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kStartRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kAuthorization,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_Calibration_Authorization(req=Authorization_req.kAuthorize)
#         self.soa.event_check_Calibration_Status_Info(status=calibration_status.kCalibrationRunning,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.set_auto_calibration(req=calibration_req.kOff, functionID=CalibrationFunctionID.ALM,
#                                       source=SourceType.kRemote, isAlloweSkip=True)
#         self.soa.event_check_Calibration_Result_Info(errorCode=calibration_error_code.kUserCancelRoutine,
#                                                      functionID=CalibrationFunctionID.ALM)
#         self.soa.get_Calibration_Status_Info(status=calibration_status.kIdle,
#                                              functionID=CalibrationFunctionID.InvalidValue)
#         self.soa.get_Intelligent_Calibration_Result_Info(errorCode=calibration_error_code.kSuccess,
#                                                          functionID=CalibrationFunctionID.InvalidValue)
