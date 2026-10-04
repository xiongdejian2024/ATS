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


@allure.feature("互联服务/远程控制/极速制热控制")
@allure.story("极速制热控制")
class TestRCHeatUp(TestABCBase):
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


    @allure.title("极速制热-RVC_极速制热_transport")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988711(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 
    
    @allure.title("极速制热-RVC_极速制热_Factory")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988710(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")    

    @allure.title("极速制热-RVC_极速制热_维修模式")
    @pytest.mark.sanity
    def test_rvc_heat_up_caseid_1988709(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("极速制热-RVC_极速制热_FOTAUPDATE")
    @pytest.mark.sanity
    def test_rvc_heat_up_caseid_1988708(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("极速制热-RVC_极速制热_FOTAROLLBACK")
    @pytest.mark.sanity
    def test_rvc_heat_up_caseid_1988707(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("极速制热-RVC_极速制热_abandoned")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988706(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制热-RVC_极速制热_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_rvc_heat_up_caseid_1988705(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time_start = time.time()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = False,timeout=1830)
        assert time.time() - time_start > 1770

    @allure.title("极速制热-RVC_极速制热_abandoned未上切")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988704(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="NetwakeFail")
        
    @allure.title("极速制热-RVC_极速制热_abandoned高压失败")
    @pytest.mark.sanity
    def test_rvc_heat_up_caseid_1988703(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        time.sleep(15)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")      

    @allure.title("极速制热-RVC_极速制热_制冷开启失败")
    @pytest.mark.sanity
    def test_rvc_heat_up_caseid_1988702(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        time.sleep(15)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")  

    @allure.title("极速制热-RVC_极速制热_inactive1.5s内上高压")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988701(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
    
    @allure.title("极速制热-RVC_极速制热_inactive1.5s后上高压")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988700(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        time_start = time.time()
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(2.5)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        logger.info("执行时间：{}s".format(time.time() - time_start))
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制热-RVC_极速制热_inactive占座")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988699(self, ecu):
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")      

    @allure.title("极速制热-RVC_极速制热_convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988698(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  
    
    @allure.title("极速制热-RVC_极速制热_convience占座")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988697(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制热-RVC_极速制热_active")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988696(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制热-RVC_极速制热_driving")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988695(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制热-RVC_极速制热_Transport and 维修模式")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988694(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")             

    @allure.title("极速制热-RVC_极速制热_Transport and convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988693(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 

    @allure.title("极速制热-RVC_极速制热_Transport and UPDATE")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988692(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 

    @allure.title("极速制热-RVC_极速制热_convience and 维修模式")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988691(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制热-RVC_极速制热_convience and UPDATE")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988690(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="UsageModeFail")  

    @allure.title("极速制热-RVC_极速制热_维修模式 and UPDATE")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988689(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送极速制热请求")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("极速制热-RVC_极速制热_极速制热与极速制热")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988688(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        sleep(5)
        execid1 = self.tsp.rvc_heat_up(1)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制热-RVC_极速制热_极速制热与极速制冷")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988687(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        sleep(5)
        execid1 = self.tsp.rvc_cold_down(1)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制热-RVC_极速制热_极速制热与远控空调")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988686(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        sleep(5)
        execid1 = self.tsp.rvc_ac_control(1, 220)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制热-RVC_极速制热_远控空调与极速制热")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988685(self, ecu):
        execid = self.tsp.rvc_ac_control(1, 220)
        sleep(5)
        execid1 = self.tsp.rvc_heat_up(1)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制热-RVC_极速制热_极速制热与预约空调")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988684(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        sleep(5)
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=200, driver_level=-1, passenger_level=-1, steering_level=-1)
        sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="SysBusy")

    @allure.title("极速制热-RVC_极速制热_预约空调与极速制热")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988683(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=200, driver_level=-1, passenger_level=-1, steering_level=-1)
        sleep(5)
        execid1 = self.tsp.rvc_heat_up(1)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制热-RVC_极速制热_极速制热与远控除霜")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988682(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        sleep(5)
        execid1 = self.tsp.rvc_defrost_control(1)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(15)

    @allure.title("极速制热-RVC_极速制热_远控除霜与极速制热")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988681(self, ecu):
        execid = self.tsp.rvc_defrost_control(1)
        sleep(5)
        execid1 = self.tsp.rvc_heat_up(1)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        sleep(50)

    @allure.title("极速制热-RVC_极速制热_制热已开启")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988680(self, ecu):
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        execid = self.tsp.rvc_heat_up(1)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("极速制热-RVC_极速制热_StartOK")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988679(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="StartOK")
        sleep(15)

    @allure.title("极速制热-RVC_极速制热_SOAFail")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988678(self, ecu):
        self.soa.soa_partner.stop_single_partner("ClimateControlService_server")
        time.sleep(5)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送极速制热开启请求")
        sleep(51)
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SOAFail")

    @allure.title("极速制热-RVC_极速制热_FaultId7")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988677(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow) 
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow") 

    @allure.title("极速制热-RVC_极速制热_FaultId13")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988676(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited) 
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited") 

    @allure.title("极速制热-RVC_极速制热_上高压FaultId7")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988675(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow) 
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow") 

    @allure.title("极速制热-RVC_极速制热_上高压FaultId13")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988674(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited) 
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited") 

    @allure.title("极速制热-RVC_极速制热_上高压响应OFF")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988673(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.Off)
        sleep(15) 
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail") 
    
    @allure.title("极速制热-RVC_极速制热_延长上高压")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988672(self, ecu):
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        execid = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制热-RVC_极速制热_制冷关闭")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988671(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_heat_up(-1)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = False,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("极速制热-RVC_极速制热_制热关闭失败")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988670(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_heat_up(-1)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = False,timeout=20)
        sleep(15)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")

    @allure.title("极速制热-RVC_极速制热_制冷关闭取消计时")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988669(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxHeatingCtrl", 1800, None)

    @allure.title("极速制热-RVC_极速制热_上切convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988668(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time_start = time.time()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")      

    @allure.title("极速制热-RVC_极速制热_上切active")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988667(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送远控空调开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxHeatingCtrl", 1, None)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")   

    @allure.title("极速制热-RVC_极速制热_上切driving")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988666(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("极速制热-RVC_极速制热_服务未上线上切convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988665(self, ecu):
        self.soa.soa_partner.stop_single_partner("ClimateControlService_server")
        time.sleep(5)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        logger.info("已发送远控空调开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("极速制热-RVC_极速制热_制热关闭上切convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988664(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_heat_up(-1)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = False,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")  

    @allure.title("极速制热-RVC_极速制热_远控主驾座椅通风后,再极速制热延长高压上切convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988663(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="DelayFail")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("极速制热-RVC_极速制热_远控主驾座椅通风后,再极速制热未高压上切convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988662(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_heat_up(1)
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

    @allure.title("极速制热-RVC_极速制热_极速制热开启成功,远控开启空调Hi")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988661(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time_start = time.time()
        sleep(300)
        execid1 = self.tsp.rvc_ac_control(1,1)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperature", 1, None)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = False,timeout=1500)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        assert time.time() - time_start > 1770

    @allure.title("极速制热-RVC_极速制热_极速制热开启成功,远控调节温度")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988660(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        execid1 = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time_start = time.time()
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.check_RemoteOff_req(timeout=1830)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        assert time.time() - time_start > 1770

    @allure.title("极速制热-RVC_极速制热_极速制冷开启成功,极速制热")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988659(self, ecu):
        execid = self.tsp.rvc_cold_down(1)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(120)
        execid1 = self.tsp.rvc_heat_up(1)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        time_start1 = time.time()
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = False,timeout=1800)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxCoolingCtrl", 1, None)
        assert time.time() - time_start1 > 1770

    @allure.title("极速制热-RVC_极速制热_制冷开启,上切convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1988658(self, ecu):
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts = False, maxHeatingSts = False)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxHeatingCtrl", 1800, None)

    @allure.title("极速制热-RVC_极速制热_远控主驾座椅通风后,极速制热成功")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1989548(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(1)
        execid2 = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)

    @allure.title("极速制热-RVC_极速制热_abandoned上切convience")
    @pytest.mark.full
    def test_rvc_heat_up_caseid_1989547(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetMaxHeatingCtrl", 1, None)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")