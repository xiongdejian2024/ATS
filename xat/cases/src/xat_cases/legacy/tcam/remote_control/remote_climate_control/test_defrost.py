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


@allure.feature("互联服务/远程控制/远控除霜控制")
@allure.story("远控除霜控制")
class TestRCDefrost(TestABCBase):
    def before_class(self, ecu):
        self.rvc_data = deepcopy(rvc_config_data)
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", "SteerWheelService_server",
                         "HighVoltageService_server","ClimateControlService_server","VehicleTimeService_server",
                         "ShieldWindowService_server","OuterRearViewService_server",'ConfigMasterService_server'])
        time.sleep(60)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.bus_comm.resume_all_bus_send()
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_ShieldWindowService_HeatStatus(heat_status=HeatStatus.HeatStatusOff)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_OuterRearViewService_HeatStatus(status= False)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        self.soa.notify_RearShieldWindowHeatStatus(heat_sts = HeatStatus.HeatStatusOff)
        self.soa.notify_OuterRearViewHeatStatus(heat_work_sts = HeatStatus.HeatStatusOff, heat_sts = HeatStatus.HeatStatusOff)
        sleep(1)

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(rvc_config_data), app_name="rvc", publish_id=int(time.time()))
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Close)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        self.soa.notify_ShieldWindowService_HeatStatus(heat_status=HeatStatus.HeatStatusOff)
        self.soa.notify_OuterRearViewService_HeatStatus(status= False)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_RearShieldWindowHeatStatus(heat_sts = HeatStatus.HeatStatusOff)
        self.soa.notify_OuterRearViewHeatStatus(heat_work_sts = HeatStatus.HeatStatusOff, heat_sts = HeatStatus.HeatStatusOff)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        time.sleep(10)
        logger.info("等待10s再操作")

    def after_class(self, ecu):
        pass

    @allure.title("远控除霜-RVC_远控开启除霜_transport")
    @pytest.mark.sanity
    def test_defrost_caseid_1980487(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="CarModeFail", execid=execid)
    
    @allure.title("远控除霜-RVC_远控开启除霜_Factory")
    @pytest.mark.full
    def test_defrost_caseid_1980486(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="CarModeFail", execid=execid)
        
    @allure.title("远控除霜-RVC_远控开启除霜_abandoned")
    @pytest.mark.smoke
    def test_defrost_caseid_1980485(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)
        time.sleep(180)

    @allure.title("远控除霜-RVC_远控开启除霜_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_defrost_caseid_1980484(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        time_start = time.time()
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=1900)
        assert time.time() - time_start > 1770
        
    @allure.title("远控除霜-RVC_远控开启除霜_abandoned未上切")
    @pytest.mark.full
    def test_defrost_caseid_1980483(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(keywords="NetwakeFail", execid=execid)       

    @allure.title("远控除霜-RVC_远控开启除霜_abandoned高压失败")
    @pytest.mark.sanity
    def test_defrost_caseid_1980482(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="RemClimaHvStrtFail", execid=execid)     

    @allure.title("远控除霜-RVC_远控开启除霜_除霜开启失败")
    @pytest.mark.sanity
    def test_defrost_caseid_1980481(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)        

    @allure.title("远控除霜-RVC_远控开启除霜_inactive")
    @pytest.mark.smoke
    def test_defrost_caseid_1980480(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive30自动关闭")
    @pytest.mark.sanity
    def test_defrost_caseid_1980479(self, ecu):
        self.rvc_data[0]["value"][11]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,keep_time=3,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        time_start = time.time()
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=1)
        time.sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=190)
        assert time.time() - time_start > 180

    @allure.title("远控除霜-RVC_远控开启除霜_inactive高压失败")
    @pytest.mark.sanity
    def test_defrost_caseid_1980478(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="RemClimaHvStrtFail", execid=execid)
        
    @allure.title("远控除霜-RVC_远控开启除霜_inactive除霜开启失败")
    @pytest.mark.sanity
    def test_defrost_caseid_1980477(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive后除霜开启")
    @pytest.mark.full
    def test_defrost_caseid_1980476(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive后除霜16min自动关闭")
    @pytest.mark.full
    def test_defrost_caseid_1980475(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.soa.check_SetOutput_req(timeout=20)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Close)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)
        time_start = time.time()
        sleep(5)
        self.soa.notify_RearShieldWindowHeatStatus(heat_sts = HeatStatus.HeatStatusOn)
        self.soa.notify_OuterRearViewHeatStatus(heat_work_sts = HeatStatus.HeatStatusOn, heat_sts = HeatStatus.HeatStatusOn)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOff,timeout=1820)
        assert time.time() - time_start > 870

    @allure.title("远控除霜-RVC_远控开启除霜_inactive后与外后视镜除霜开启")
    @pytest.mark.full
    def test_defrost_caseid_1980474(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.soa.check_SetOutput_req(timeout=20)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Close)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_已上后除霜高压")
    @pytest.mark.sanity
    def test_defrost_caseid_1980473(self, ecu):
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Close)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_convience")
    @pytest.mark.smoke
    def test_defrost_caseid_1980472(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 
    
    @allure.title("远控除霜-RVC_远控开启除霜_convience除霜开启失败")
    @pytest.mark.sanity
    def test_defrost_caseid_1980471(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)              

    @allure.title("远控除霜-RVC_远控开启除霜_convience后与外后视镜除霜开启")
    @pytest.mark.full
    def test_defrost_caseid_1980470(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_convience后除霜15min自动关闭")
    @pytest.mark.full
    def test_defrost_caseid_1980469(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.notify_RearShieldWindowHeatStatus(heat_sts = HeatStatus.HeatStatusOn)
        self.soa.notify_OuterRearViewHeatStatus(heat_work_sts = HeatStatus.HeatStatusOn, heat_sts = HeatStatus.HeatStatusOn)
        time_start = time.time()
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOff,timeout=960)
        assert time.time() - time_start > 870

    @allure.title("远控除霜-RVC_远控开启除霜_convience后挡除霜已开启")
    @pytest.mark.full
    def test_defrost_caseid_1980468(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_ShieldWindowService_HeatStatus(heat_status=HeatStatus.HeatStatusOn)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_convience外后视镜除霜已开启")
    @pytest.mark.sanity
    def test_defrost_caseid_1980467(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_OuterRearViewService_HeatStatus(status= True)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_convience后与外后视镜除霜均开启")
    @pytest.mark.full
    def test_defrost_caseid_1980466(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_ShieldWindowService_HeatStatus(heat_status=HeatStatus.HeatStatusOn)
        self.soa.notify_OuterRearViewService_HeatStatus(status= True)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_convience后与外后视镜除霜开启")
    @pytest.mark.full
    def test_defrost_caseid_1980465(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_convience主驾占座")
    @pytest.mark.sanity
    def test_defrost_caseid_1980464(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)   

    @allure.title("远控除霜-RVC_远控开启除霜_convience副驾占座")
    @pytest.mark.full
    def test_defrost_caseid_1980463(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus= [0,1,0,0,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 
         

    @allure.title("远控除霜-RVC_远控开启除霜_convience左后座椅占座")
    @pytest.mark.full
    def test_defrost_caseid_1980462(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,1,0,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)        

    @allure.title("远控除霜-RVC_远控开启除霜_convience右后座椅占座")
    @pytest.mark.full
    def test_defrost_caseid_1980461(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,1,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)         

    @allure.title("远控除霜-RVC_远控开启除霜_convience中后座椅占座")
    @pytest.mark.full
    def test_defrost_caseid_1980460(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,0,0,0,1])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 
   
    @allure.title("远控除霜-RVC_远控开启除霜_convience主驾与副驾占座")
    @pytest.mark.full
    def test_defrost_caseid_1980459(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,0,0,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 

    @allure.title("远控除霜-RVC_远控开启除霜_convience主驾与左后座椅占座")
    @pytest.mark.full
    def test_defrost_caseid_1980458(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,1,0,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 

    @allure.title("远控除霜-RVC_远控开启除霜_convience主驾与右后座椅占座")
    @pytest.mark.full
    def test_defrost_caseid_1980457(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,1,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 

    @allure.title("远控除霜-RVC_远控开启除霜_convience主驾与中后座椅占座")
    @pytest.mark.full
    def test_defrost_caseid_1980456(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,1])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)        

    @allure.title("远控除霜-RVC_远控开启除霜_convience三座占座")
    @pytest.mark.full
    def test_defrost_caseid_1980455(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,0,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)   

    @allure.title("远控除霜-RVC_远控开启除霜_convience四座占座")
    @pytest.mark.full
    def test_defrost_caseid_1980454(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,0])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)     

    @allure.title("远控除霜-RVC_远控开启除霜_convience全部占座")
    @pytest.mark.sanity
    def test_defrost_caseid_1980453(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 
         
    @allure.title("远控除霜-RVC_远控开启除霜_active")
    @pytest.mark.sanity
    def test_defrost_caseid_1980452(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 
         
    @allure.title("远控除霜-RVC_远控开启除霜_driving")
    @pytest.mark.sanity
    def test_defrost_caseid_1980451(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 
         
    @allure.title("远控除霜-RVC_远控开启除霜_维修模式")
    @pytest.mark.sanity
    def test_defrost_caseid_1980450(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="MntnMode", execid=execid)
         
    @allure.title("远控除霜-RVC_远控开启除霜_N档")
    @pytest.mark.sanity
    def test_defrost_caseid_1980449(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 
         
    @allure.title("远控除霜-RVC_远控开启除霜_FOTAUPDATE")
    @pytest.mark.sanity
    def test_defrost_caseid_1980448(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="OTAOngoing", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_FOTAROLLBACK")
    @pytest.mark.sanity
    def test_defrost_caseid_1980447(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="OTAOngoing", execid=execid)
        
    @allure.title("远控除霜-RVC_远控开启除霜_预约空调打断远控除霜")
    @pytest.mark.full
    def test_defrost_caseid_1980446(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "RemoteOn", 3, None)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
   
    @allure.title("远控除霜-RVC_远控开启除霜_Abandoned上切convience除霜与座椅加热")
    @pytest.mark.full
    def test_defrost_caseid_1980445(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        execid1 = self.tsp.rvc_driver_seat_heat(level=3)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20) 
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 1, None)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        with allure.step('校验远控除霜执行结果'):        
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
     
    @allure.title("远控除霜-RVC_远控开启除霜_Abandoned上切convience除霜与座椅通风")
    @pytest.mark.full
    def test_defrost_caseid_1980444(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20) 
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 1, None)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        with allure.step('校验远控除霜执行结果'):        
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
     
    @allure.title("远控除霜-RVC_远控开启除霜_Abandoned上切convience除霜与方向盘加热")
    @pytest.mark.full
    def test_defrost_caseid_1980443(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        execid1 = self.tsp.rvc_steering_wheel_heat(3)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=30) 
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 1, None)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        with allure.step('校验远控除霜执行结果'):        
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
        
    @allure.title("远控除霜-RVC_远控开启除霜_服务未上线上切convience30")
    @pytest.mark.full
    def test_defrost_caseid_1980442(self, ecu):
        self.soa.soa_partner.stop_single_partner("ClimateControlService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        time.sleep(5)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):        
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控除霜-RVC_远控开启除霜_高压上切convience")
    @pytest.mark.full
    def test_defrost_caseid_1980441(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)  

    @allure.title("远控除霜-RVC_远控开启除霜_inactive上切convience")
    @pytest.mark.full
    def test_defrost_caseid_1980440(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        
    @allure.title("远控除霜-RVC_远控开启除霜_transport与维修模式")
    @pytest.mark.full
    def test_defrost_caseid_1980439(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="CarModeFail", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_高压上切convience30min")
    @pytest.mark.full
    def test_defrost_caseid_1980438(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.empty_all()
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 10, None)      

    @allure.title("远控除霜-RVC_远控开启除霜_inactive上切convience30min")
    @pytest.mark.full
    def test_defrost_caseid_1980437(self, ecu):
        self.rvc_data[0]["value"][11]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,keep_time=3,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 180, None)

    @allure.title("远控除霜-RVC_远控开启除霜_远控除霜后预约座椅加热")
    @pytest.mark.full
    def test_defrost_caseid_1980436(self, ecu):
        self.rvc_data[0]["value"][11]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,keep_time=3,timeout=20)
        time_start = time.time()
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, temp=250, driver_level=1, passenger_level=-1, steering_level=-1, DriverVent_level=-1)
        time.sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=190)
        assert time.time() - time_start > 180
        

    @allure.title("远控除霜-RVC_远控开启除霜_维修模式与FOTA")
    @pytest.mark.full
    def test_defrost_caseid_1980435(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="MntnMode", execid=execid)

    @allure.title("远控除霜-RVC_远控关闭除霜_上切convience")
    @pytest.mark.full
    def test_defrost_caseid_1980434(self, ecu):
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        execid1 = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False,timeout=20)
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")
        
    @allure.title("远控除霜-RVC_远控关闭除霜_inactive")
    @pytest.mark.smoke
    def test_defrost_caseid_1980433(self, ecu):
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        time.sleep(5)
        self.soa.check_SetFastDefrostMode_req(on=False,timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)

    @allure.title("远控除霜-RVC_远控关闭除霜_inactive关闭失败")
    @pytest.mark.sanity
    def test_defrost_caseid_1980432(self, ecu):
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False,timeout=20)
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)

    @allure.title("远控除霜-RVC_远控关闭除霜_convience")
    @pytest.mark.smoke
    def test_defrost_caseid_1980431(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        time.sleep(5)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False,timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 

    @allure.title("远控除霜-RVC_远控关闭除霜_convience关闭失败")
    @pytest.mark.sanity
    def test_defrost_caseid_1980430(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        time.sleep(5)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False,timeout=20)
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):           
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid) 

    @allure.title("远控除霜-RVC_远控开启除霜_BatteryLow")
    @pytest.mark.sanity
    def test_defrost_caseid_1980429(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultBatteryLow)     
        assert self.tsp.log_search_remote_vehicle_control(keywords="BatteryLow", execid=execid)

    @allure.title("远控除霜-RVC_除霜维持_inactive")
    @pytest.mark.sanity
    def test_defrost_caseid_1980428(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 20, None)

    @allure.title("远控除霜-RVC_除霜异常_inactivefaultId7")
    @pytest.mark.sanity
    def test_defrost_caseid_1980427(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultBatteryLow)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 10, None)

    @allure.title("远控除霜-RVC_除霜异常_ActivationLimited")
    @pytest.mark.sanity
    def test_defrost_caseid_1980426(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_ClimateFault(fault_id = FaultId.FaultActivationLimited)   
        assert self.tsp.log_search_remote_vehicle_control(keywords="ActivationLimited", execid=execid) 

    @allure.title("远控除霜-RVC_远控开启除霜_高压流程")
    @pytest.mark.full
    def test_defrost_caseid_1980425(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        execid1 = self.tsp.rvc_driver_seat_heat(level=3)
        logger.info("已发送远控主驾座椅加热三档请求")
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        with allure.step('校验远控主驾座椅加热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid1)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Open,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off)

    @allure.title("远控除霜-RVC_远控开启除霜_高压流程失败")
    @pytest.mark.full
    def test_defrost_caseid_1980424(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        execid1 = self.tsp.rvc_driver_seat_heat(level=3)
        logger.info("已发送远控主驾座椅加热三档请求")
        time.sleep(15)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="RemClimaHvStrtFail", execid=execid)
        with allure.step('校验远控主驾座椅加热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="RemClimaHvStrtFail", execid=execid1)

    @allure.title("远控除霜-RVC_远控开启除霜_高压流程后30min")
    @pytest.mark.full
    def test_defrost_caseid_1980423(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.tsp.rvc_driver_seat_heat(level=3)
        logger.info("已发送远控主驾座椅加热三档请求")
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)
        time_start = time.time()
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=1900)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=1900) 
        assert time.time() - time_start > 1770

    @allure.title("远控除霜-RVC_远控开启除霜_二次除霜")
    @pytest.mark.full
    def test_defrost_caseid_1980422(self, ecu):
        self.tsp.rvc_defrost_control(1)
        time.sleep(10)
        execid = self.tsp.rvc_defrost_control(1)         
        assert self.tsp.log_search_remote_vehicle_control(keywords="SysBusy", execid=execid)

    @allure.title("远控空调-RVC_远控开启除霜_除霜与空调")
    @pytest.mark.full
    def test_defrost_caseid_1980421(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        execid1 = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控空调与除霜开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="SysBusy", execid=execid1)
        time.sleep(20) 

    @allure.title("远控除霜-RVC_远控开启除霜_除霜关闭")
    @pytest.mark.full
    def test_defrost_caseid_1980420(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetFastDefrostMode", 20, None)

    @allure.title("远控除霜-RVC_远控开启除霜_convience除霜已开启")
    @pytest.mark.full
    def test_defrost_caseid_1980419(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        execid = self.tsp.rvc_defrost_control(1)
        assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive响应错误")
    @pytest.mark.full
    def test_defrost_caseid_1980418(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_convience响应错误")
    @pytest.mark.full
    def test_defrost_caseid_1980417(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        time.sleep(15)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_TCAM先收到除霜状态")
    @pytest.mark.full
    def test_defrost_caseid_1980416(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_D档")
    @pytest.mark.full
    def test_defrost_caseid_1980415(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn) 

    @allure.title("远控除霜-RVC_远控开启除霜_R档")
    @pytest.mark.full
    def test_defrost_caseid_1980414(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        time.sleep(2)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid) 
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)

    @allure.title("远控除霜-RVC_远控开启除霜_NEWTASK")
    @pytest.mark.full
    def test_defrost_caseid_1980412(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_DOWNLOADING")
    @pytest.mark.full
    def test_defrost_caseid_1980411(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_ACIVE")
    @pytest.mark.full
    def test_defrost_caseid_1980410(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_defrost_caseid_1980409(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_FAILEDDRIVING")
    @pytest.mark.full
    def test_defrost_caseid_1980408(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求") 
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_SUCCESSFUL")
    @pytest.mark.full
    def test_defrost_caseid_1980407(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_defrost_caseid_1980406(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_14abandoned")
    @pytest.mark.full
    def test_defrost_caseid_1980405(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(14)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)
        time.sleep(180)

    @allure.title("远控除霜-RVC_远控开启除霜_abandoned16s上切")
    @pytest.mark.full
    def test_defrost_caseid_1980404(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(16)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive14s高压")
    @pytest.mark.full
    def test_defrost_caseid_1980403(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求") 
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(14)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(14)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive14s响应")
    @pytest.mark.full
    def test_defrost_caseid_1980402(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(14)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive16s高压失败")
    @pytest.mark.full
    def test_defrost_caseid_1980401(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(16)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="RemClimaHvStrtFail", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_inactive除霜16s开启失败")
    @pytest.mark.full
    def test_defrost_caseid_1980400(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(16)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)

    @allure.title("远控除霜-RVC_远控开启除霜_convience14s响应")
    @pytest.mark.full
    def test_defrost_caseid_1980399(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetFastDefrostMode_req(on=True,timeout=20)
        time.sleep(14)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn)

    @allure.title("远控除霜-RVC_远控开启除霜_convience16s开启失败")
    @pytest.mark.full
    def test_defrost_caseid_1980398(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控除霜开启请求")
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        time.sleep(16)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)  

    @allure.title("远控除霜-RVC_远控关闭除霜_inactive14s响应")
    @pytest.mark.full
    def test_defrost_caseid_1980397(self, ecu):
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=20)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        time.sleep(14)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)

    @allure.title("远控除霜-RVC_远控关闭除霜_inactive16s关闭失败")
    @pytest.mark.full
    def test_defrost_caseid_1980396(self, ecu):
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=20)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        time.sleep(16)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)

    @allure.title("远控除霜-RVC_远控关闭除霜_convience14s响应")
    @pytest.mark.full
    def test_defrost_caseid_1980395(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        time.sleep(5)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=20)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        time.sleep(14)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="Success", execid=execid)
   
    @allure.title("远控除霜-RVC_远控关闭除霜_convience16s关闭失败")
    @pytest.mark.full
    def test_defrost_caseid_1980394(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        time.sleep(5)
        execid = self.tsp.rvc_defrost_control(-1)
        logger.info("已发送远控除霜关闭请求")
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=20)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        time.sleep(16)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        with allure.step('校验远控除霜执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail", execid=execid)