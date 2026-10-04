#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import threading
import pytest
import allure
import json

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务/远程控制/远程座椅通风")
@allure.story("远控座椅通风")
class TestRearRightSeatVenting(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server", "VehicleTimeService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "SeatService_server", 
                         "HighVoltageService_server", "ClimateControlService_server"])
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        time.sleep(60)
        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=[181,189],ccp_value=[0x02,0x02])# 设置整车CCP支持远控后排座椅加热、后排座椅通风 

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        time.sleep(1)

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.soa_partner.start_single_partner(service="SeatService", role="server")
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(20)
        logger.info("等待20s再操作")

    def after_class(self, ecu):
        pass

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_transport")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988096(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")
    
    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_Factory")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988095(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_abandoned")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1988094(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)     

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988093(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=1830)
        assert time.time() - time_start > 1770  
        

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_abandoned未上切")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988092(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="NetwakeFail")
        

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_abandoned高压失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988091(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")      

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_右后座椅通风开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988090(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")      

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive通风3档")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1988089(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive通风2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988088(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Mid, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive通风1档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988087(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_rear_right_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive30自动关闭")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988086(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        time_start = time.time()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_rear_right_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20) 
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=1830)
        assert time.time() - time_start > 1770  

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive高压失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988085(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")
        
    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive右后座椅通风开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988084(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive右后座椅通风开启")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988083(self, ecu):
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience通风3档")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1988082(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience通风2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988081(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Mid, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience通风1档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988080(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        execid = self.tsp.rvc_rear_right_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience右后座椅通风开启失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988079(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")           

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive右后座椅通风换挡失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988078(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Mid, timeout=20) 
        time.sleep(15)      
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience右后座椅通风开启")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988077(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")   

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_StartOK")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988076(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="StartOK")
    

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive上切active")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988075(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(5)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive上切driving")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988074(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(5)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_维修模式")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988073(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")      

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_FOTAUPDATE")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988072(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_FOTAROLLBACK")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988071(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing") 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_维修模式与FOTA")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988070(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_inactive")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1988069(self, ecu):
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_inactive关闭失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988068(self, ecu):
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_convience")
    @pytest.mark.smoke
    def test_rvc_seat_venting_caseid_1988067(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
           
    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_convience关闭失败")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988066(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 


    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_kError")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988065(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Error, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Error")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_kEnergyLimit")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988064(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.EnergyLimit, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="EnergyLimit")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_kFunctionLimit")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988063(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.FunctionLimit, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="FunctionLimit")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_上切convience通风开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988062(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1800, None) 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_上切convience通风开启2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988061(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        # self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience全部占座")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988060(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_二次右后座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988059(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        time.sleep(5)
        execid1 = self.tsp.rvc_rear_right_seat_vent(level=3)
        logger.info("已发送两次远控座椅通风开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy") 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_右后座椅通风2档3档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988058(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        time.sleep(5)
        execid1 = self.tsp.rvc_rear_right_seat_vent(level=2)
        logger.info("已发送两次远控座椅通风开启请求")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive响应错误")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988057(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience响应错误")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988056(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Mid, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_延长高压")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988055(self, ecu):
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)     
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 20, None) 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_16hTCAM重启后远控")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988054(self, ecu):
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
        time.sleep(300)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_QUERY")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988053(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        time.sleep(2)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_NEWTASK")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988052(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_DOWNLOADING")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988051(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_ACIVE")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988050(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988049(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_FAILEDDRIVING")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988048(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_SUCCESSFUL")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988047(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988046(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_14abandoned")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988045(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(14)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)     
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_abandoned16s上切")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988044(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(16)    
        # self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_上切convience通风无30min计时")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988043(self, ecu):
        self.soa.soa_partner.stop_single_partner("SeatService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.start_single_partner(service="SeatService", role="server")
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1800, None)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988042(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        time.sleep(14)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive16s高压失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988041(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)     
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive右后座椅通风16s开启失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988040(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988039(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(14)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience16s开启失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988038(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        time.sleep(16)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_inactive14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988037(self, ecu):
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        time.sleep(14)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_inactive16s关闭失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988036(self, ecu):
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        time.sleep(16)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_convience14s响应")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988035(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        time.sleep(14)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
   
    @allure.title("远控座椅通风-RVC_远控关闭右后座椅通风_convience16s关闭失败")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988034(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time.sleep(5)
        execid = self.tsp.rvc_rear_right_seat_vent(level=-1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        time.sleep(16)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive上切convience")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988033(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1800, None)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience右后座椅通风已开启")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988032(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_发送高压上切convience")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988031(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_上切active通风开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988030(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        # self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_发送高压上切active")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988029(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_上切driving通风开启3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988028(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(3)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_发送高压上切driving")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988027(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("上切driving")
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_发送高压为Off")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988026(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.Off)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_active通风3档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988025(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_active通风2档")
    @pytest.mark.sanity
    def test_rvc_seat_venting_caseid_1988024(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Mid, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_高压faultid7")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988097(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20) 
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultBatteryLow)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_高压faultid13")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988098(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultActivationLimited)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_active通风1档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988099(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        execid = self.tsp.rvc_rear_right_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_driving通风3档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988100(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_driving通风2档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988101(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Mid, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_driving通风1档")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988102(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=1)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_inactive座椅占座")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988103(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience通风3档30未关闭")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988104(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 10, None)  

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_先座椅通风后加热")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988105(self, ecu):
        execid1 = self.tsp.rvc_rear_right_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_rearright_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        time.sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatVentOn")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_同时座椅加热通风上切driving")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988106(self, ecu):
        execid1 = self.tsp.rvc_rear_right_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_rearright_seat_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(0.8)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatVentOn")
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_先座椅加热后座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988107(self, ecu):
        execid1 = self.tsp.rvc_rearright_seat_heat(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="SeatHeatOn")
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)

    @allure.title("远控座椅加热-RVC_远控开启右后座椅通风_预约右后座椅通风远控右后座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988108(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, ac= -1, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.Low, timeout=20)
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SysBusy")

    @allure.title("远控座椅加热-RVC_远控开启右后座椅通风_预约右后座椅通风远控左后座椅通风")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988109(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, ac= -1, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.Low, timeout=20)
        execid = self.tsp.rvc_rear_left_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)  
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_换挡上切convience")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988110(self, ecu):
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_rear_right_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Mid, timeout=20) 
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        with allure.step('校验远控右后座椅通风执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_convience座椅占座")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1988111(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控座椅通风-RVC_远控开启右后座椅通风_CarConfigNotSupport")
    @pytest.mark.full
    def test_rvc_seat_venting_caseid_1987336(self, ecu):
        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=189,ccp_value=0x01) # 设置整车CCP支持远控二排座椅通风 
        execid = self.tsp.rvc_rear_right_seat_vent(level=3)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarConfigNotSupport")
        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=189,ccp_value=0x02)