#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
from threading import *
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("/跨域功能/维持上电模式控制")
@allure.story("远控维持上电模式")
class TestMaintainPower(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "CentralLockService_server", "InteractiveService_server",
                         "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server"])
        sleep(8)
    
    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        sleep(5)

    def after_each_func(self, ecu):
        self.soa.notify_ParkingComfortModeSts()
        pass

    def after_class(self, ecu):
        pass


    @pytest.mark.smoke
    @allure.title("RVC_退出维持上电_成功")
    def test_maintain_power_caseid_1986788(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ParkingComfortModeSts(ParkingComfortModeSts=1, exit_reason=0)
        with allure.step("下发远控关闭维持上电"):
            self.tsp.rvc_maintainpower_control()
            self.soa.check_GetParkingComfortModeSts_req_and_feedback_resp(modeSts=1, reason=0, timeout=5)
            self.soa.check_ParkingComfortModeOff_req_and_feedback_resp(timeout=5)
            self.soa.notify_ParkingComfortModeSts()
            assert self.tsp.log_search(), f"TCAM远程维持上电执行上报车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_退出维持上电_DelayFail")
    def test_maintain_power_caseid_1986787(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ParkingComfortModeSts(ParkingComfortModeSts=1, exit_reason=0)
        sleep(3)
        with allure.step("下发远控关闭维持上电"):
            self.tsp.rvc_maintainpower_control()
            self.soa.check_GetParkingComfortModeSts_req_and_feedback_resp(modeSts=1,reason=0, timeout=5)
            self.soa.check_ParkingComfortModeOff_req_and_feedback_resp(timeout=5)
            assert self.tsp.log_search(keywords="DelayFail"), f"TCAM远程维持上电执行上报车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_退出维持上电_SysBusy")
    def test_maintain_power_caseid_1986785(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ParkingComfortModeSts(ParkingComfortModeSts=1, exit_reason=0)
        sleep(3)
        with allure.step("下发远控关闭维持上电"):
            self.tsp.rvc_maintainpower_control()
            self.tsp.rvc_maintainpower_control()
            assert self.tsp.log_search(keywords="SysBusy"), f"TCAM远程维持上电执行上报车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_退出维持上电_超时2s")
    def test_maintain_power_caseid_1987078(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ParkingComfortModeSts(ParkingComfortModeSts=1, exit_reason=0)
        with allure.step("下发远控关闭维持上电"):
            self.tsp.rvc_maintainpower_control()
            self.soa.check_GetParkingComfortModeSts_req_and_feedback_resp(modeSts=1, reason=0, timeout=5)
            self.soa.check_ParkingComfortModeOff_req_and_feedback_resp(timeout=5)
            sleep(2)
            self.soa.notify_ParkingComfortModeSts()
            assert self.tsp.log_search(), f"TCAM远程维持上电执行上报车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_退出维持上电_超时4s")
    def test_maintain_power_caseid_1987079(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ParkingComfortModeSts(ParkingComfortModeSts=1, exit_reason=0)
        with allure.step("下发远控关闭维持上电"):
            self.tsp.rvc_maintainpower_control()
            self.soa.check_GetParkingComfortModeSts_req_and_feedback_resp(modeSts=1, reason=0, timeout=5)
            self.soa.check_ParkingComfortModeOff_req_and_feedback_resp(timeout=5)
            sleep(4)
            self.soa.notify_ParkingComfortModeSts()
            assert self.tsp.log_search(keywords="DelayFail"), f"TCAM远程维持上电执行上报车云的结果校验失败"

    @pytest.mark.full
    @allure.title("RVC_退出维持上电_SOAFail")
    def test_maintain_power_caseid_1986786(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ParkingComfortModeSts(ParkingComfortModeSts=1, exit_reason=0)
        sleep(3)
        with allure.step("下发远控关闭维持上电"):
            self.soa.soa_partner.stop_single_partner("VehicleSetStatusService_server")
            self.tsp.rvc_maintainpower_control()
            assert self.tsp.log_search(keywords="SOAFail", timeout=80), f"TCAM远程维持上电执行上报车云的结果校验失败"
            self.soa.soa_partner.start_single_partner(service="VehicleSetStatusService", role="server")
            

    
    