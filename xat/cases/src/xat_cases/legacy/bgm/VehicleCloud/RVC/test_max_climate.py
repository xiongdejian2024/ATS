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

@allure.feature("远程控制/远控两域联调测试/急速制冷/急速制热")
@allure.story("急速制冷/急速制热")
class TestRvcseat(TestABCBase):
    def before_class(self, ecu):
        partner_process_check()
        self.soa.update(["SeatService_client",
                         "CentralLockService_client",
                         "SteerWheelService_client",
                         "VehicleSetStatusService_client",
                         "ClimateControlService_client"])
        sleep(2)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodycan.CcmBodyFr22, 'RemClimaHvSts', 1)

    def before_each_func(self, ecu):
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.Off,level2=HeatLevel.Off)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
         
    def after_each_func(self, ecu):
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.set_and_check_steer_wheel_sts(level1=HeatLevel.Off,level2=HeatLevel.Off)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
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

    @allure.title("RVC_急速制冷开启_ABANDONED")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991495(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(15.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Lo)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)

    @allure.title("RVC_急速制冷关闭_ABANDONED")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991494(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(False)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.Off)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制冷开启_INACTIVE")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991493(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(15.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Lo)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)

    @allure.title("RVC_急速制冷关闭_INACTIVE")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991492(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(False)
        # self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.Off)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制冷模式上切_ACTIVE")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991491(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(15.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Lo)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制热_设置温度后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991481(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(28.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Hi)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)
        self.soa.hmi_set_climate_temperature(zone=ClimateZone.FirstRowLeft, value=24)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制冷_开启急速加热后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991489(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(15.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Lo)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)
        self.soa.set_Max_Heating_Ctrl(True)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)

    @allure.title("RVC_急速制冷_开启除霜后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991488(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(15.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Lo)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)
        self.tsp.rvc_defrost_control(1)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制冷_关闭空调后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991487(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(15.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Lo)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)
        # self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.tsp.rvc_ac_control(-1)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制热开启_ABANDONED")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991486(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(28.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Hi)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)

    @allure.title("RVC_急速制热关闭_ABANDONED")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991485(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(False)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.Off)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制热开启_INACTIVE")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991484(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(28.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Hi)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)

    @allure.title("RVC_急速制热关闭_INACTIVE")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1991483(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(False)
        # self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.Off)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制热模式上切_ACTIVE")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991482(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(28.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Hi)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制冷_设置温度后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991490(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(15.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Lo)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)
        self.soa.hmi_set_climate_temperature(zone=ClimateZone.FirstRowLeft, value=19)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制热_开启急速制冷后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991480(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(28.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Hi)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)
        self.soa.set_Max_Cooling_Ctrl(True)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=True,maxHeatingSts=False)

    @allure.title("RVC_急速制热_开启除霜后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991479(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(28.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Hi)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)
        self.tsp.rvc_defrost_control(1)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)

    @allure.title("RVC_急速制热_关闭空调后退出")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1991478(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.soa.set_Max_Heating_Ctrl(True)
        self.bus_comm.check_telm_clima_req(RemHvStrtActvReq.On)
        self.bus_comm.check_telm_clima_temp_range(28.5)
        self.bus_comm.check_telm_clima_cmptmt_spcl(ClimateSpcl.Hi)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.On)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=True)
        self.tsp.rvc_ac_control(-1)
        self.soa.check_max_cooling_heating_info(maxCoolingSts=False,maxHeatingSts=False)