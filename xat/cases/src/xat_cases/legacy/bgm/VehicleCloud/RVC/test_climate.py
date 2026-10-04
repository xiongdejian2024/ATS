#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure

from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("远程控制/远控两域联调测试/远控空调")
@allure.story("远控空调")
class TestRvcseat(TestABCBase):
    def before_class(self, ecu):
        partner_process_check()
        self.soa.update(["SeatService_client",
                         "CentralLockService_client",
                         "SteerWheelService_client",
                         "VehicleSetStatusService_client",
                         "ClimateControlService_client"])
        sleep(2)
        # self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Open)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', 1)

    def before_each_func(self, ecu):
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.Off,level2=HeatLevel.Off)
        # self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
         
    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Start)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("RVC_远控打开空调_abandoned")
    @pytest.mark.smoke
    def test_caseid_1991544(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.pause_all_bus_send()
        sleep(3)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_Remote_Climate_Status(status=RemClimateSts.On)

    @allure.title("RVC_远控关闭空调_abandoned")
    @pytest.mark.smoke
    def test_caseid_1991543(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.pause_all_bus_send()
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        sleep(3)
        self.tsp.rvc_ac_control(-1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
        self.soa.check_Remote_Climate_Status(status=RemClimateSts.Off)

    @allure.title("RVC_远控打开空调_inactive")
    @pytest.mark.smoke
    def test_caseid_1991542(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.pause_all_bus_send()
        sleep(3)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_Remote_Climate_Status(status=RemClimateSts.On)

    @allure.title("RVC_远控关闭空调_inactive")
    @pytest.mark.smoke
    def test_caseid_1991541(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.pause_all_bus_send()
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        sleep(3)
        self.tsp.rvc_ac_control(-1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
        self.soa.check_Remote_Climate_Status(status=RemClimateSts.Off)

    @allure.title("RVC_远控打开空调_CONVENIENCE")
    @pytest.mark.smoke
    def test_caseid_1991540(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.pause_all_bus_send()
        sleep(2)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("RVC_远控关闭空调_CONVENIENCE")
    @pytest.mark.smoke
    def test_caseid_1991539(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.pause_all_bus_send()
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRow,value=22)
        self.tsp.rvc_ac_control(-1)
        sleep(2)
        self.soa.send_method_request("ClimateControlService_client", 'RemoteOff', {})
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 2)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 0)

    @allure.title("RVC_远控打开空调_ACTIVE")
    @pytest.mark.smoke
    def test_caseid_1991538(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.pause_all_bus_send()
        sleep(2)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("RVC_远控关闭空调_ACTIVE")
    @pytest.mark.smoke
    def test_caseid_1991537(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.pause_all_bus_send()
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRow,value=22)
        self.tsp.rvc_ac_control(-1)
        sleep(2)
        self.soa.send_method_request("ClimateControlService_client", 'RemoteOff', {})
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 2)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 0)

    @allure.title("RVC_远控打开空调_DRIVING")
    @pytest.mark.smoke
    def test_caseid_1991536(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.pause_all_bus_send()
        sleep(2)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("RVC_远控关闭空调_DRIVING")
    @pytest.mark.smoke
    def test_caseid_1991535(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.pause_all_bus_send()
        self.soa.hmi_set_climate_temperature_sts(zone=ClimateZone.FirstRow,value=22)
        self.tsp.rvc_ac_control(-1)
        sleep(2)
        self.soa.send_method_request("ClimateControlService_client", 'RemoteOff', {})
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 2)
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodycan.CemBodyFr47, 'TelmClimaReq', 0)

    @allure.title("RVC_远控开启空调_inactive_模式上切")
    @pytest.mark.sanity
    def test_caseid_1991534(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.pause_all_bus_send()
        sleep(2)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_Remote_Climate_Status(status=RemClimateSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)

    @allure.title("RVC_远控开启空调_CONVENIENCE_模式下切")
    @pytest.mark.sanity
    def test_caseid_1991533(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.pause_all_bus_send()
        sleep(2)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.check_Remote_Climate_Status(status=RemClimateSts.Off)

    @allure.title("RVC_预约远控开启空调_模式上切CONVENIENCE_空调保持开启")
    @pytest.mark.full
    def test_caseid_1991532(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.pause_all_bus_send()
        sleep(2)
        self.tsp.rvc_ac_control(1)
        self.bus_comm.check_telm_clima_req(sts=RemHvStrtActvReq.On)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_Remote_Climate_Status(status=RemClimateSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.get_climate_sys_sts(power_sts_first_row=True)