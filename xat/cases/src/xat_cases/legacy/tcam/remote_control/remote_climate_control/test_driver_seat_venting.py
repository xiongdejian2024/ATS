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


@allure.feature("互联服务/远程控制/远程座椅通风")
@allure.story("远控座椅通风")
class TestDriverSeatVenting(TestABCBase):
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

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_transport")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986864(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")
    
    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_Factory")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986863(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_abandoned")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1986862(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)     

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986861(self, ecu):
        self.rvc_data[0]["value"][16]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High,keep_time=3)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=190)
        assert time.time() - time_start > 180  
        

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_abandoned未上切")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986860(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="NetwakeFail")
        

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_abandoned高压失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986859(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")      

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_主驾座椅通风开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986858(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")      

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive通风3档")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1986857(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive通风2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986856(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Mid, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive通风1档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986855(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_driver_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive30自动关闭")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986854(self, ecu):
        self.rvc_data[0]["value"][16]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High,keep_time=3)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_driver_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20) 
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.Low)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=190)
        assert time.time() - time_start > 180  

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive高压失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986853(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")
        
    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive主驾座椅通风开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986852(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive主驾座椅通风开启")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986851(self, ecu):
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience通风3档")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1986850(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience通风2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986849(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Mid, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience通风1档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986848(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        execid = self.tsp.rvc_driver_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience主驾座椅通风开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986847(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")           

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive主驾座椅通风换挡失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986846(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Mid, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience主驾座椅通风开启")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986845(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")   

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_StartOK")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986844(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="StartOK")
    

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_abandoned上切convience")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986843(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE) 
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1, None)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive上切driving")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986842(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(5)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_维修模式")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986841(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")      

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_FOTAUPDATE")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986840(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_FOTAROLLBACK")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986839(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing") 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_维修模式与FOTA")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986838(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_inactive")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1986837(self, ecu):
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_inactive关闭失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986836(self, ecu):
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_convience")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1986835(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
           
    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_convience关闭失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986834(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 


    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_kError")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986833(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Error, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Error")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_kEnergyLimit")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986832(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.EnergyLimit, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="EnergyLimit")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_kFunctionLimit")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986831(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.FunctionLimit, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FunctionLimit")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_上切convience通风开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986830(self, ecu):
        self.rvc_data[0]["value"][16]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20,keep_time=3)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 190, None) 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_上切convience通风开启2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986829(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        # self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience全部占座")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986828(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_二次主驾座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986827(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(5)
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        logger.info("已发送两次远控座椅通风开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy") 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_主驾座椅通风2档3档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986826(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(5)
        execid1 = self.tsp.rvc_driver_seat_vent(level=2)
        logger.info("已发送两次远控座椅通风开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive响应错误")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986825(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience响应错误")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986824(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Mid, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_延长高压")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986823(self, ecu):
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)     
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None) 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_16hTCAM重启后远控")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986822(self, ecu):
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
        time.sleep(300)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_QUERY")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986821(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(2)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_NEWTASK")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986820(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_DOWNLOADING")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986819(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_ACIVE")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986818(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986817(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_FAILEDDRIVING")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986816(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_SUCCESSFUL")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986815(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986814(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_14abandoned")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986813(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(14)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)     
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_abandoned16s上切")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986812(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(16)    
        # self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_上切convience通风无30min计时")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986811(self, ecu):
        self.soa.soa_partner.stop_single_partner("SeatService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.start_single_partner(service="SeatService", role="server")
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986810(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(14)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive16s高压失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986809(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)     
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive主驾座椅通风16s开启失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986808(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986807(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(14)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience16s开启失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986806(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_inactive14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986805(self, ecu):
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        time.sleep(14)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_inactive16s关闭失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986804(self, ecu):
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        time.sleep(16)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_convience14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986803(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        time.sleep(14)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
   
    @allure.title("远控座椅通风-RVC_远控关闭主驾座椅通风_convience16s关闭失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1986802(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_driver_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        time.sleep(16)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive上切convience")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986801(self, ecu):
        self.rvc_data[0]["value"][16]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High,keep_time=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 190, None)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience主驾座椅通风已开启")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986800(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_发送高压上切convience")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986799(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_上切active通风开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986798(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        # self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_发送高压上切active")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986797(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_上切driving通风开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986796(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_发送高压上切driving")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986795(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_发送高压为Off")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986794(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.Off)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_active通风3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986793(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_active通风2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1986792(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Mid, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_高压faultid7")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987444(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultBatteryLow)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_高压faultid13")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987445(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultActivationLimited)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_active通风1档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987923(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        execid = self.tsp.rvc_driver_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_driving通风3档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987924(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_driving通风2档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987925(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Mid, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_driving通风1档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987926(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_inactive座椅占座")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987927(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience通风3档30未关闭")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987928(self, ecu):
        self.rvc_data[0]["value"][16]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 190, None)  

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_先座椅通风后加热")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987929(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_driver_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatVentOn")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_同时座椅加热通风上切driving")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987930(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_driver_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(0.8)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatVentOn")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_先座椅加热后座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987931(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_heat(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatHeatOn")
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)

    @allure.title("远控座椅加热-RVC_远控开启主驾座椅通风_预约主驾座椅通风远控主驾座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987932(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, ac= -1, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SysBusy")

    @allure.title("远控座椅加热-RVC_远控开启主驾座椅通风_预约主驾座椅通风远控副驾座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987933(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, ac= -1, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        execid = self.tsp.rvc_passenger_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)  
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_换挡上切convience")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987934(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Mid, timeout=20) 
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        with allure.step('校验远控主驾座椅通风执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启主驾座椅通风_convience座椅占座")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987935(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")