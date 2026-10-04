#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import threading
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务/远程控制/电池预加热")
@allure.story("电池预加热")
class TestBattProtect(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server",
                         "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.NORMAL)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_gear(gear=Gear.Park)
        self.soa.notify_fota_status(state=FOTAMasteSts.IDLE)
        self.soa.s2s_set_mntnmode(mntnmode=False)
        self.soa.notify_HVSOCInfo(displaySoc=90)
        self.soa.notify_VehicleTimeInfo(sync_sts=TimeSyncSts.NTP)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)  # 设置车辆唤醒上切usagemode到inactive

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    # http://172.18.128.76:8080/2023_11_28_19_40_46
    # 如下代码示例第一条电池低温自保护自动化用例，非插枪场景正常启动加热
    @allure.title("高压电池极低温自保护-非插枪场景正常启动加热")
    @pytest.mark.abc
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/xxxxxxx?projectId=46', name='Case xxxxxxxx')
    def test_batt_protect_caseid_0001(self, ecu):
        wait_time = self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        sleep(30)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=wait_time)
        self.soa.check_GetSeatHeatVentStatus_req_and_feedback_resp(work_sts=VentWorkStatus.Off, timeout=0.5)
        self.soa.check_steerwheel_GetHeat_req_and_feedback_resp(heatlevel=HeatLevel.Off, timeout=0.5)
        self.soa.check_climate_GetRemotePowerStatus_req_and_feedback_resp(rem_pow_sts=RemClimateSts.Off, timeout=0.5)
        self.soa.check_GetDefrostSts_req_and_feedback_resp(defrostmax=False, climatedefrost=False, timeout=0.5)
        self.soa.check_GetBatteryTemperatureInfo_req_and_feedback_resp(min_temp=-32, timeout=0.5)
        self.soa.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.Disconnected, timeout=0.5)
        self.soa.check_GetChargingInfo_req_and_feedback_resp(charg_sts=ChargingSts.Default,
                                                             plug_sts=PluggerSts.Disconnected, timeout=0.5)
        self.soa.check_SetOutput_req(timeout=0.5)  # 监听TCAM发送上高压请求
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close, timeout=0.5)
        self.soa.check_SetBatteryHeating_req(timeout=0.5)  # 监听TCAM发送电池加热请求
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_high_voltage_setoutput_request(check_time=30)
        sleep(5)
