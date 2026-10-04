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

@allure.feature("互联服务/远程控制/远程座椅加热")
@allure.story("远控座椅加热")
class TestPassengerSeatHeating(TestABCBase):
    def before_class(self, ecu):
        self.rvc_data = deepcopy(rvc_config_data)
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server", "VehicleTimeService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "SeatService_server", 
                         "HighVoltageService_server", "ClimateControlService_server",'ConfigMasterService_server'])
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        time.sleep(60)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        time.sleep(1)

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(rvc_config_data), app_name="rvc", publish_id=int(time.time()))
        self.soa.soa_partner.start_single_partner(service="SeatService", role="server")
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(20)
        logger.info("等待20s再操作")

    def after_class(self, ecu):
        pass

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_transport")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980918(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")
    
    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_Factory")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980917(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_abandoned")
    @pytest.mark.smoke
    def test_rvc_seat_heating_caseid_1980916(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 20, None)     

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980915(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=1830)
        assert time.time() - time_start > 1770  
        

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_abandoned未上切")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980914(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="NetwakeFail")
        

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_abandoned高压失败")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980913(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")      

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_副驾座椅加热开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980912(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")      

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive加热3档")
    @pytest.mark.smoke
    def test_rvc_seat_heating_caseid_1980911(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 20, None)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive加热2档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980910(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 20, None)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive加热1档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980909(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_passenger_seat_heat(level=1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 20, None)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive30自动关闭")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980908(self, ecu):
        self.rvc_data[0]["value"][8]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, keep_time=3,heat_level=HeatLevel.High)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_passenger_seat_heat(level=1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20) 
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=190)
        assert time.time() - time_start > 180  

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive高压失败")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980907(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")
        
    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive副驾座椅加热开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980906(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive副驾座椅加热开启")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980905(self, ecu):
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience加热3档")
    @pytest.mark.smoke
    def test_rvc_seat_heating_caseid_1980904(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience加热2档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980903(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience加热1档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980902(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        execid = self.tsp.rvc_passenger_seat_heat(level=1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience副驾座椅加热开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980901(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")           

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive副驾座椅加热换挡失败")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980900(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience副驾座椅加热开启")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980899(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")   

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_StartOK")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980898(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="StartOK")
    

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive上切active")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980897(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(5)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive上切driving")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980896(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(5)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_维修模式")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980895(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")      

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_FOTAUPDATE")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980894(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_FOTAROLLBACK")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980893(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing") 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_维修模式与FOTA")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980892(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_inactive")
    @pytest.mark.smoke
    def test_rvc_seat_heating_caseid_1980891(self, ecu):
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_inactive关闭失败")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980890(self, ecu):
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_convience")
    @pytest.mark.smoke
    def test_rvc_seat_heating_caseid_1980889(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
           
    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_convience关闭失败")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980888(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_kError")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980887(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Error, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Error")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_kEnergyLimit")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980886(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.EnergyLimit, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="EnergyLimit")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_kFunctionLimit")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980885(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.FunctionLimit, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FunctionLimit")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_上切convience加热开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980884(self, ecu):
        self.rvc_data[0]["value"][8]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20,keep_time=3)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 190, None) 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_上切convience加热开启2档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980883(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        # self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience全部占座")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980882(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_二次副驾座椅加热")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980881(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        time.sleep(5)
        execid1 = self.tsp.rvc_passenger_seat_heat(level=3)
        logger.info("已发送两次远控座椅加热开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy") 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_副驾座椅加热2档3档")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980880(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        time.sleep(5)
        execid1 = self.tsp.rvc_passenger_seat_heat(level=2)
        logger.info("已发送两次远控座椅加热开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive响应错误")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980879(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience响应错误")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980878(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_延长高压")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980877(self, ecu):
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)     
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 20, None) 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_16hTCAM重启后远控")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980876(self, ecu):
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
        time.sleep(300)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_QUERY")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980875(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        time.sleep(2)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_NEWTASK")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980874(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_DOWNLOADING")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980870(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_ACIVE")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980869(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980868(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_FAILEDDRIVING")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980867(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_SUCCESSFUL")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980866(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980865(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_14abandoned")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980864(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(14)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)     
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_abandoned16s上切")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980863(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(16)    
        # self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_上切convience加热无30min计时")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980862(self, ecu):
        self.soa.soa_partner.stop_single_partner("SeatService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.start_single_partner(service="SeatService", role="server")
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive14s响应")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980861(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        time.sleep(14)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive16s高压失败")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980860(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)     
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive副驾座椅加热16s开启失败")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980859(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience14s响应")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980858(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(14)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience16s开启失败")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980857(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_inactive14s响应")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980856(self, ecu):
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        time.sleep(14)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_inactive16s关闭失败")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980855(self, ecu):
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        time.sleep(16)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_convience14s响应")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980854(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        time.sleep(14)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
   
    @allure.title("远控座椅加热-RVC_远控关闭副驾座椅加热_convience16s关闭失败")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980853(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_passenger_seat_heat(level=-1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        time.sleep(16)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive上切convience")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980852(self, ecu):
        self.rvc_data[0]["value"][8]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High,keep_time=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 190, None)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience副驾座椅加热已开启")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980851(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_发送高压上切convience")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980850(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_上切active加热开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980849(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        # self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_发送高压上切active")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980848(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_上切driving加热开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980847(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_发送高压上切driving")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980846(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_发送高压为Off")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980845(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.Off)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_active加热3档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980844(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_active加热2档")
    @pytest.mark.sanity
    def test_rvc_seat_heating_caseid_1980843(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_高压faultid7")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980919(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20) 
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultBatteryLow)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_高压faultid13")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980920(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultActivationLimited)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_active加热1档")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980921(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        execid = self.tsp.rvc_passenger_seat_heat(level=1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_driving加热3档")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980922(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_driving加热2档")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980923(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_driving加热1档")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980924(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=1)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_inactive座椅占座")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980925(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience加热3档30未关闭")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980926(self, ecu):
        self.rvc_data[0]["value"][8]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 190, None)  

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_先座椅通风后加热")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980927(self, ecu):
        execid1 = self.tsp.rvc_passenger_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        time.sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatVentOn")
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off,vent_level=VentLevel.Off)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_同时座椅加热通风上切driving")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980928(self, ecu):
        execid1 = self.tsp.rvc_passenger_seat_heat(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_passenger_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(0.8)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatHeatOn")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_先座椅加热后座椅通风")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980929(self, ecu):
        execid1 = self.tsp.rvc_passenger_seat_heat(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_passenger_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatHeatOn")
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_预约副驾座椅加热远控副驾座椅加热")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980930(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, ac= -1, driver_level=-1, passenger_level=1, steering_level=-1, DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SysBusy")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_预约副驾座椅加热远控主驾座椅加热")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980931(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, ac= -1, driver_level=-1, passenger_level=1, steering_level=-1, DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        execid = self.tsp.rvc_driver_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)  
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_换挡上切convience")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980932(self, ecu):
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_passenger_seat_heat(level=2)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Mid, timeout=20) 
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        with allure.step('校验远控副驾座椅加热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")

    @allure.title("远控座椅加热-RVC_远控开启副驾座椅加热_convience座椅占座")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1980933(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_passenger_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")