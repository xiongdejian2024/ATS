#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import threading
import pytest
import allure
import json
from copy import deepcopy

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.config_data import *

@allure.feature("远程控制/远程座舱控制/远程方向盘加热")
@allure.story("远程方向盘加热")
class TestSteerWheelHeating(TestABCBase):
    def before_class(self, ecu):
        self.rvc_data = deepcopy(rvc_config_data)
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server", "VehicleTimeService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "SteerWheelService_server", 
                         "HighVoltageService_server", "ClimateControlService_server", "SeatService_server",'ConfigMasterService_server'])
        time.sleep(60)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        time.sleep(10)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.io.tcam_kl15_up()
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_ClimateFault(fault_id=FaultId.OK)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.On)
        sleep(1)

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.rvc_data[0]["value"][10]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(rvc_config_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        self.soa.soa_partner.start_single_partner(service="SteerWheelService", role="server")
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        time.sleep(10)

    def after_class(self, ecu):
        pass

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience方向盘加热已开启")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978634(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive响应失败")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978633(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience响应失败")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978632(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=2)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_16hTCAM重启后远控")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978631(self, ecu):
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
        time.sleep(300)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_D档")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978630(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_R档")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978629(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_QUERY")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978628(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_NEWTASK")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978627(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_DOWNLOADING")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978626(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_ACTIVE")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978625(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978624(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_FAILEDDRIVING")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978623(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_SUCCESSFUL")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978622(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1978621(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 20, None)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_transport")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960530(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_factory")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960529(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_abandoned")
    @pytest.mark.smoke
    def test_rvc_steer_wheel_heating_caseid_1960528(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time.sleep(180)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960527(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=1830)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_未上切abandoned")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960526(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="NetwakeFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_abandoned高压失败")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960525(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(15)
        self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_方向盘加热开启失败")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960524(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(15)
        self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive加热3档")
    @pytest.mark.smoke
    def test_rvc_steer_wheel_heating_caseid_1960523(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        
    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive加热2档")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960522(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_steering_wheel_heat(level=2)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 20, None) 

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive加热1档")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960521(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 20, None) 

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_开启方向盘加热预约座椅通风")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960520(self, ecu):
        self.rvc_data[0]["value"][10]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High,keep_time=3)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time.sleep(300)
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=1)
        time.sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=190)
        assert time.time() - time_start > 180
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive高压失败")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960519(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(15)
        self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive方向盘加热开启失败")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960518(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(15)
        self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive方向盘加热开启")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960517(self, ecu):
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience加热3档")
    @pytest.mark.smoke
    def test_rvc_steer_wheel_heating_caseid_1960516(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")


    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience加热2档")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960515(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        execid = self.tsp.rvc_steering_wheel_heat(level=2)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience加热1档")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960514(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-远控开启方向盘加热_convience方向盘加热开启失败")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960513(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=3)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience方向盘加热开启")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960512(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_用户上车维持")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960511(self, ecu):
        self.rvc_data[0]["value"][10]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High,keep_time=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 190, None)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience主驾占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960510(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience副驾占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960509(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience左后座椅占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960508(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience右后座椅占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960507(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience中后座椅占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960506(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        
    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience主驾与副驾占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960505(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience主驾与左后座椅占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960504(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,1,0,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience主驾与右后座椅占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960503(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,1])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience主驾与中后座椅占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960502(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,1,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience三座占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960501(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,0,0])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热RVC_远控开启方向盘加热_convience四座占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960500(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,0,1])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convience全部占座")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960499(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_active")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960498(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_driving")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960497(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_维修模式")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960496(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_N档")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960495(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_FOTAUPDATE")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960494(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_FOTAROLLBACK")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960493(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_transport与维修模式")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960492(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_预约换挡30自动关闭")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960491(self, ecu):
        self.rvc_data[0]["value"][10]["value"] = 3
        self.rvc_data[1]["value"][1]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High,keep_time=3)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time.sleep(60)
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, driver_level=-1, passenger_level=-1, steering_level=2)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=190)
        assert time.time() - time_start > 180
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_换档上切convience")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960490(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_steering_wheel_heat(level=2)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_服务未上线上切convience")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960489(self, ecu):
        self.rvc_data[0]["value"][10]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        self.soa.soa_partner.stop_single_partner("SteerWheelService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.start_single_partner(service="SteerWheelService", role="server")
        time.sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=30)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 190, None)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_服务未上线上切active")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960488(self, ecu):
        self.soa.soa_partner.stop_single_partner("SteerWheelService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.soa_partner.start_single_partner(service="SteerWheelService", role="server")
        time.sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=30)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_服务未上线上切driving")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960487(self, ecu):
        self.soa.soa_partner.stop_single_partner("SteerWheelService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.soa_partner.start_single_partner(service="SteerWheelService", role="server")
        time.sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_开启方向盘加热预约座椅加热")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960486(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time.sleep(300)
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, temp=250, driver_level=1, passenger_level=-1, steering_level=-1, DriverVent_level=-1)
        time.sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 20, None)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_开启方向盘加热预约空调")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960485(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=1, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=1, PassengerVent_level=-1, RearLeftVent_level=-1, RearRightVent_level=-1)
        time.sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 20, None)

    @allure.title("远控座椅加热-RVC_远控开启方向盘加热_预约方向盘远控方向盘")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960484(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, ac= -1, driver_level=-1, passenger_level=-1, steering_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req(heat_level=HeatLevel.Low,timeout=20)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SysBusy")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_inactive方向盘加热换档失败")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960483(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        execid = self.tsp.rvc_steering_wheel_heat(level=2)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=20)
        time.sleep(15)
        self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-远控开启方向盘加热_convience方向盘加热换挡失败")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960482(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=3)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_维修模式与FOTA")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960481(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("远控方向盘加热-RVC_远控关闭方向盘加热_上切convience")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960480(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_steering_wheel_heat(level=-1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(2)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控关闭方向盘加热_inactive")
    @pytest.mark.smoke
    def test_rvc_steer_wheel_heating_caseid_1960479(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_steering_wheel_heat(level=-1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控关闭方向盘加热_inactive关闭失败")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960478(self, ecu):
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        execid = self.tsp.rvc_steering_wheel_heat(level=-1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=3)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控关闭方向盘加热_convience")
    @pytest.mark.smoke
    def test_rvc_steer_wheel_heating_caseid_1960477(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        execid = self.tsp.rvc_steering_wheel_heat(level=-1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=3)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控关闭方向盘加热_convience关闭失败")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960476(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        execid = self.tsp.rvc_steering_wheel_heat(level=-1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=3)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convienceFuncational_Limit")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960475(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Funcational_Limit)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FunctionLimit")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_TelmFctReq")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960474(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_singal('connectivitycanfd', 'TcamConnectivityFr35','TelmFctReq','Boolean_TRUE',timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_方向盘加热异常_inactive_faultId7")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960473(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow")

    @allure.title("远控方向盘加热-RVC_方向盘加热异常_inactive_faultId13")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960472(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited")

    @pytest.mark.repeat(100)   
    @allure.title("远控方向盘加热-RVC_turnoon_abandon_Success-L3")
    @pytest.mark.stress_test
    def test_rvc_steer_wheel_heating_caseid_1960471(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time.sleep(180)

    @pytest.mark.repeat(100)
    @allure.title("远控方向盘加热-RVC_inactive_Success-L3")
    @pytest.mark.stress_test
    def test_rvc_steer_wheel_heating_caseid_1960470(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)

    @pytest.mark.repeat(100)
    @allure.title("远控方向盘加热-RVC_turnoff_convenience_Success-L3")
    @pytest.mark.stress_test
    def test_rvc_steer_wheel_heating_caseid_1960469(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        execid = self.tsp.rvc_steering_wheel_heat(level=-1)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_二次方向盘加热")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960468(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        time.sleep(10)
        execid1 = self.tsp.rvc_steering_wheel_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_方向盘加热2档3档")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960467(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        time.sleep(10)
        execid1 = self.tsp.rvc_steering_wheel_heat(level=2)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convienceError")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960466(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Error)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Error")
        
    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_convienceENERGY_LIMIT")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1960465(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=3)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Energy_Limit)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="EnergyLimit")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_延长高压")
    @pytest.mark.sanity
    def test_rvc_steer_wheel_heating_caseid_1960464(self, ecu):
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_高压kError")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1988417(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        time.sleep(1)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Error)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Error")
        
    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_高压kENERGY_LIMIT")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1988418(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        time.sleep(1)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Energy_Limit)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="EnergyLimit")

    @allure.title("远控方向盘加热-RVC_远控开启方向盘加热_高压kFuncational_Limit")
    @pytest.mark.full
    def test_rvc_steer_wheel_heating_caseid_1988419(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        time.sleep(1)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.Funcational_Limit)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FunctionLimit")