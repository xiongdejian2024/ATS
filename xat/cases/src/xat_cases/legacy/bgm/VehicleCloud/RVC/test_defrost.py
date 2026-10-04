#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("远程控制/远控两域联调测试/远控除霜")
@allure.story("远控除霜")
class TestRvcseat(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_client",
                         "VehicleSetStatusService_client",
                         "ClimateControlService_client"])
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.Off)

    def before_each_func(self, ecu):
        self.bus_comm.set_RemClimaDefrstSts(sts=OnOff.Off)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
         
    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("RVC_远控除霜开启_inactive")
    @pytest.mark.smoke
    def test_caseid_1991521(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_defrost_control(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_TelmDefrostReq(sts=OnOff.On)
        self.bus_comm.set_RemClimaDefrstSts(sts=OnOff.On)
        self.soa.check_NotifyACDefrostSts(defrost_max=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜关闭_inactive")
    @pytest.mark.smoke
    def test_caseid_1991520(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_defrost_control(-1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_TelmDefrostReq(sts=OnOff.Off)
        self.soa.check_NotifyACDefrostSts(defrost_max=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜开启_active")
    @pytest.mark.smoke
    def test_caseid_1991519(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        execid = self.tsp.rvc_defrost_control(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        self.bus_comm.set_defrost_sts(defrost_sts=isOn.On)
        self.soa.check_NotifyACDefrostSts(defrost_max=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜关闭_active")
    @pytest.mark.smoke
    def test_caseid_1991518(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        execid = self.tsp.rvc_defrost_control(-1)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        self.bus_comm.set_defrost_sts(defrost_sts=isOn.Off)
        self.soa.check_NotifyACDefrostSts(defrost_max=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜开启_CONVENIENCE")
    @pytest.mark.smoke
    def test_caseid_1991517(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_defrost_control(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        self.bus_comm.set_defrost_sts(defrost_sts=isOn.On)
        self.soa.check_NotifyACDefrostSts(defrost_max=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜关闭_CONVENIENCE")
    @pytest.mark.smoke
    def test_caseid_1991516(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_defrost_control(-1)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        self.bus_comm.set_defrost_sts(defrost_sts=isOn.Off)
        self.soa.check_NotifyACDefrostSts(defrost_max=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜开启_DRIVING")
    @pytest.mark.smoke
    def test_caseid_1991515(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_defrost_control(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        self.bus_comm.set_defrost_sts(defrost_sts=isOn.On)
        self.soa.check_NotifyACDefrostSts(defrost_max=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜关闭_DRIVING")
    @pytest.mark.smoke
    def test_caseid_1991514(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_defrost_control(-1)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.Off)
        self.bus_comm.set_defrost_sts(defrost_sts=isOn.Off)
        self.soa.check_NotifyACDefrostSts(defrost_max=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜开启_inactive模式上切")
    @pytest.mark.sanity
    def test_caseid_1991513(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_defrost_control(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_TelmDefrostReq(sts=OnOff.On)
        self.bus_comm.set_RemClimaDefrstSts(sts=OnOff.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_NotifyACDefrostSts(defrost_max=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控除霜开启_CONVENIENCE模式下切")
    @pytest.mark.sanity
    def test_caseid_1991512(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_defrost_control(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_HmiDefrstMaxReq(sts=OnOff.On)
        self.bus_comm.set_defrost_sts(defrost_sts=isOn.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.check_NotifyACDefrostSts(defrost_max=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_预约开启远控除霜_模式上切CONVENIENCE_除霜保持")
    @pytest.mark.full
    def test_caseid_1991511(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_defrost_control(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_TelmDefrostReq(sts=OnOff.On)
        self.bus_comm.set_RemClimaDefrstSts(sts=OnOff.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_NotifyACDefrostSts(defrost_max=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"