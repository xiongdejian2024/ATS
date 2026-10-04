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


@allure.feature("互联服务/远程控制/极速制冷控制")
@allure.story("极速制冷控制")
class TestRCColdDown(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server","CentralLockService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","ClimateControlService_server","InteractiveService_server",
                         "VehicleTimeService_server","WindowService_server","WindowAppService_server",
                         "SteerWheelService_server"])
        time.sleep(60)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_SetClimateTempMaintainSts(data="0")
        self.soa.notify_WindowService_NotifyPosition_sts(win_id=[0,1,2,3,],position=0)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_ClimateFault(fault_id=FaultId.OK)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        self.soa.notify_SetClimateTempMaintainSts(data="0")
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        time.sleep(15)
        logger.info("等待15s再操作")

    def after_class(self, ecu):
        pass


    @allure.title("极速制冷-RVC_极速制冷_transport")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988657(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 
    
    @allure.title("极速制冷-RVC_极速制冷_Factory")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988656(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")    

    @allure.title("极速制冷-RVC_极速制冷_维修模式")
    @pytest.mark.sanity
    def test_rvc_cold_down_caseid_1988655(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("极速制冷-RVC_极速制冷_FOTAUPDATE")
    @pytest.mark.sanity
    def test_rvc_cold_down_caseid_1988654(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("极速制冷-RVC_极速制冷_FOTAROLLBACK")
    @pytest.mark.sanity
    def test_rvc_cold_down_caseid_1988653(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("极速制冷-RVC_极速制冷_abandoned")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988652(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制冷-RVC_极速制冷_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_rvc_cold_down_caseid_1988651(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time_start = time.time()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = False,timeout=1830)
        assert time.time() - time_start > 1770

    @allure.title("极速制冷-RVC_极速制冷_abandoned未上切")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988650(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="NetwakeFail")
        
    @allure.title("极速制冷-RVC_极速制冷_abandoned高压失败")
    @pytest.mark.sanity
    def test_rvc_cold_down_caseid_1988649(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        time.sleep(15)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")      

    @allure.title("极速制冷-RVC_极速制冷_制冷开启失败")
    @pytest.mark.sanity
    def test_rvc_cold_down_caseid_1988648(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        time.sleep(15)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")  

    @allure.title("极速制冷-RVC_极速制冷_inactive1.5s内上高压")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988647(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
    
    @allure.title("极速制冷-RVC_极速制冷_inactive1.5s后上高压")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988646(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        time_start = time.time()
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(2.5)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        logger.info("执行时间：{}s".format(time.time() - time_start))
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制冷-RVC_极速制冷_inactive占座")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988645(self, ecu):
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")      

    @allure.title("极速制冷-RVC_极速制冷_convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988644(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  
    
    @allure.title("极速制冷-RVC_极速制冷_convience占座")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988643(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制冷-RVC_极速制冷_active")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988642(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制冷-RVC_极速制冷_driving")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988641(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制冷-RVC_极速制冷_Transport and 维修模式")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988640(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")             

    @allure.title("极速制冷-RVC_极速制冷_Transport and convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988639(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 

    @allure.title("极速制冷-RVC_极速制冷_Transport and UPDATE")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988638(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 

    @allure.title("极速制冷-RVC_极速制冷_convience and 维修模式")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988637(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制冷-RVC_极速制冷_convience and UPDATE")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988636(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制冷-RVC_极速制冷_维修模式 and UPDATE")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988635(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送极速制冷请求")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("极速制冷-RVC_极速制冷_极速制冷与极速制冷")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988634(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        sleep(5)
        execid1 = self.tsp.rvc_cold_down(1)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制冷-RVC_极速制冷_极速制冷与极速制热")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988633(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        sleep(5)
        execid1 = self.tsp.rvc_heat_up(1)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制冷-RVC_极速制冷_极速制冷与远控空调")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988632(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        sleep(5)
        execid1 = self.tsp.rvc_ac_control(1, 220)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制冷-RVC_极速制冷_远控空调与极速制冷")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988631(self, ecu):
        execid = self.tsp.rvc_ac_control(1, 220)
        sleep(5)
        execid1 = self.tsp.rvc_cold_down(1)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制冷-RVC_极速制冷_极速制冷与预约空调")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988630(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        sleep(5)
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=200, driver_level=-1, passenger_level=-1, steering_level=-1)
        sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="SysBusy")

    @allure.title("极速制冷-RVC_极速制冷_预约空调与极速制冷")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988629(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=200, driver_level=-1, passenger_level=-1, steering_level=-1)
        sleep(5)
        execid1 = self.tsp.rvc_cold_down(1)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制冷-RVC_极速制冷_极速制冷与远控除霜")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988628(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        sleep(5)
        execid1 = self.tsp.rvc_defrost_control(1)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制冷-RVC_极速制冷_远控除霜与极速制冷")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988627(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        sleep(5)
        execid1 = self.tsp.rvc_cold_down(1)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(50)

    @allure.title("极速制冷-RVC_极速制冷_制冷已开启")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988626(self, ecu):
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        execid = self.tsp.rvc_cold_down(1)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("极速制冷-RVC_极速制冷_StartOK")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988625(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="StartOK")
        sleep(15)

    @allure.title("极速制冷-RVC_极速制冷_SOAFail")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988624(self, ecu):
        self.soa.soa_partner.stop_single_partner("ClimateControlService_server")
        time.sleep(5)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送极速制冷开启请求")
        sleep(51)
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SOAFail")

    @allure.title("极速制冷-RVC_极速制冷_FaultId7")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988623(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow) 
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow") 

    @allure.title("极速制冷-RVC_极速制冷_FaultId13")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988622(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited) 
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited") 

    @allure.title("极速制冷-RVC_极速制冷_上高压FaultId7")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988621(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow) 
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow") 

    @allure.title("极速制冷-RVC_极速制冷_上高压FaultId13")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988620(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited) 
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited") 

    @allure.title("极速制冷-RVC_极速制冷_上高压响应OFF")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988619(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.Off)
        sleep(15) 
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail") 
    
    @allure.title("极速制冷-RVC_极速制冷_延长上高压")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988618(self, ecu):
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        execid = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制冷-RVC_极速制冷_制冷关闭")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988617(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_cold_down(-1)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = False,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制冷-RVC_极速制冷_制冷关闭失败")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988616(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_cold_down(-1)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = False,timeout=20)
        sleep(15)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")

    @allure.title("极速制冷-RVC_极速制冷_制冷关闭取消计时")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988615(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxCoolingCtrl", 1800, None)

    @allure.title("极速制冷-RVC_极速制冷_上切convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988614(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time_start = time.time()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")      

    @allure.title("极速制冷-RVC_极速制冷_上切active")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988613(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送远控空调开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxCoolingCtrl", 1, None)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")   

    @allure.title("极速制冷-RVC_极速制冷_上切driving")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988612(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("极速制冷-RVC_极速制冷_服务未上线上切convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988611(self, ecu):
        self.soa.soa_partner.stop_single_partner("ClimateControlService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送远控空调开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("极速制冷-RVC_极速制冷_制冷关闭上切convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988610(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_cold_down(-1)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = False,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")  

    @allure.title("极速制冷-RVC_极速制冷_远控主驾座椅通风后,再极速制冷延长高压上切convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988609(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="DelayFail")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("极速制冷-RVC_极速制冷_远控主驾座椅通风后,再极速制冷未高压上切convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988608(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="DelayFail")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("极速制冷-RVC_极速制冷_极速制冷开启成功,远控开启空调Lo")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988607(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time_start = time.time()
        sleep(300)
        execid1 = self.tsp.rvc_ac_control(1,0)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperature", 1, None)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = False,timeout=1500)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        assert time.time() - time_start > 1770

    @allure.title("极速制冷-RVC_极速制冷_极速制冷开启成功,远控调节温度")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988606(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        execid1 = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time_start = time.time()
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.check_RemoteOff_req(timeout=1830)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        assert time.time() - time_start > 1770

    @allure.title("极速制冷-RVC_极速制冷_远控空调开启成功,极速制冷")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988605(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(120)
        execid1 = self.tsp.rvc_cold_down(1)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        time_start1 = time.time()
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = False,timeout=1800)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "RemoteOff", 1, None)
        assert time.time() - time_start1 > 1770

    @allure.title("极速制冷-RVC_极速制冷_制冷开启,上切convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1988604(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts = False, maxHeatingSts = False)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxCoolingCtrl", 1800, None)

    @allure.title("极速制冷-RVC_极速制冷_远控主驾座椅通风后,极速制冷成功")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1989545(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("极速制冷-RVC_极速制冷_abandoned上切convience")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1989546(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxCoolingCtrl", 1, None)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("极速制冷-RVC_极速制冷_远控主驾座椅通风后,极速制冷成功")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1989545(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_cold_down(1)
        execid3 = self.tsp.rvc_passenger_seat_vent(level=3)
        execid4 = self.tsp.rvc_rearleft_seat_heat(level=3)
        execid5 = self.tsp.rvc_rearright_seat_heat(level=3)
        execid6 = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(2.5)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts= True, maxHeatingSts = False)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid3, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid4, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid5, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid6, keywords="Success")

    @allure.title("极速制冷-RVC_极速制冷_远控主驾座椅通风后,极速制冷成功")
    @pytest.mark.full
    def test_rvc_cold_down_caseid_1989545(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_cold_down(1)
        execid3 = self.tsp.rvc_passenger_seat_vent(level=3)
        execid4 = self.tsp.rvc_rearleft_seat_heat(level=3)
        execid5 = self.tsp.rvc_rearright_seat_heat(level=3)
        execid6 = self.tsp.rvc_steering_wheel_heat(level=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 2, None)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts= True, maxHeatingSts = False)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="DelayFail")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid3, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid4, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid5, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid6, keywords="Success")