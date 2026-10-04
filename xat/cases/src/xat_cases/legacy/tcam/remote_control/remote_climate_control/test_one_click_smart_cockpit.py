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


@allure.feature("互联服务/远程控制/一键备车控制")
@allure.story("一键备车控制")
class TestOneClickSmartCockpit(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server","CentralLockService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","ClimateControlService_server","InteractiveService_server",
                         "VehicleTimeService_server","WindowService_server","WindowAppService_server",
                         "SteerWheelService_server", "RemoteCtrlService_client"])
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        time.sleep(60)
        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=[181,189],ccp_value=[0x02,0x02])# 设置整车CCP支持远控后排座椅加热、后排座椅通风 
    
    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_SetClimateTempMaintainSts(data="0")
        self.soa.notify_WindowService_NotifyPosition_sts(win_id=[0,1,2,3,],position=0)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.notify_ClimateFault()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20)
        self.soa.notify_hvActiveSts(HVActiveSts.Open)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=False)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=False)
        sleep(1)

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        self.soa.notify_SetClimateTempMaintainSts(data="0")
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = False)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=False)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=False)
        time.sleep(10)
        logger.info("等待10s再操作")

    def after_class(self, ecu):
        pass

    @allure.title("一键备车-RVC_一键备车_transport")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987562(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5,6])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        logger.info("已发送一键备车开启请求")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 
    
    @allure.title("一键备车-RVC_一键备车_Factory")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987561(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5,6])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        logger.info("已发送一键备车开启请求")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")    

    @allure.title("一键备车-RVC_一键备车_维修模式")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987560(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5,6])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        logger.info("已发送一键备车开启请求")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("一键备车-RVC_一键备车_FOTAUPDATE")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987559(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5,6])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        logger.info("已发送一键备车开启请求")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("一键备车-RVC_一键备车_FOTAROLLBACK")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987558(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5,6])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        logger.info("已发送一键备车开启请求")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("一键备车-RVC_一键备车_QUERY")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987557(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_NEWTASK")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987556(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_DOWNLOADING")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987555(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_ACIVE")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987554(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987553(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_FAILEDDRIVING")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987552(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_SUCCESSFUL")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987551(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987550(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        self.tsp.rvc_one_click_smart_cockpit_1()
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_transport与维修模式")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987549(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        logger.info("已发送一键备车开启请求")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 

    @allure.title("一键备车-RVC_一键备车_维修模式与FOTA")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987548(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        logger.info("已发送一键备车开启请求")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("一键备车-RVC_一键备车_SOAFail")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987546(self, ecu):
        self.soa.soa_partner.stop_single_partner("ClimateControlService_server")
        time.sleep(5)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        logger.info("已发送一键备车开启请求")
        time.sleep(55)
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        time.sleep(5)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SOAFail")

    @allure.title("一键备车-RVC_一键备车_StartOK")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987545(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        logger.info("已发送一键备车开启请求")
        time.sleep(50)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="StartOK")

    @allure.title("一键备车-RVC_一键备车_主座加热车外温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987544(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&driverSeatHeat"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_Temperature_req_and_feedback_resp(s=2,ambienttemp=9.1,temp=10.0,is_valid=False)
        time.sleep(5)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="AmbientTempUnknown")

    @allure.title("一键备车-RVC_一键备车_方向盘加热车外温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987543(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&steeringWheelHeat"
        logger.info(execid)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_Temperature_req_and_feedback_resp(s=1,ambienttemp=9.1,temp=10.0,is_valid=False)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="AmbientTempUnknown")

    @allure.title("一键备车-RVC_一键备车_主座加热车内温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987542(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&driverSeatHeat"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=False)
        self.soa.check_GetCurrentTemperature_req_and_feedback_resp(zone_id=ClimateZoneId.AllZone,temp=10.0,is_valid=True, timeout=10)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_方向盘加热车内温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987541(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&steeringWheelHeat"
        logger.info(execid)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=False)
        self.soa.check_GetCurrentTemperature_req_and_feedback_resp(zone_id=ClimateZoneId.AllZone,temp=10.0,is_valid=False, timeout=10)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CabinTempUnknown")

    @allure.title("一键备车-RVC_一键备车_方向盘加热车内温度True")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987540(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&steeringWheelHeat"
        logger.info(execid)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=False)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_getAmbientTempRawData_req_and_feedback_resp(temp=9.1,is_valid=False, timeout=10)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="AmbientTempUnknown")
        time.sleep(15)

    @allure.title("一键备车-RVC_一键备车_座椅自动外温>30内温<30")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987539(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=31, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=29, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温>30内温=30")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987538(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=31, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=30, is_valid=True)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off,vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off,vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温>30内温=33")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987537(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=31, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=33, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温>30内温=35")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987536(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=31, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=35, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温>30内温>35")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987535(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=31, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=40, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温=30内温<30")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987534(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=30, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=29, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温=30内温=33")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987533(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=30, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=33, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温=30内温>35")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987532(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=30, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=40, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_Abandoned30min")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987531(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.notify_NotifyAmbientTempRawData(temp=30, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=35.5, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        time_start = time.time()
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time_start = time.time()
        self.soa.check_RemoteOff_req(timeout=1830)
        assert time.time() - time_start > 1770  

    @allure.title("一键备车-RVC_上切convience计时取消")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987530(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
        self.soa.empty_all()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "Off", 1800, None)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1, None) 
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 1, None) 

    @allure.title("一键备车-RVC_一键备车_get上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987529(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        logger.info("已发送一键备车开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Mid, timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("一键备车-RVC_一键备车_abandoned")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1987528(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("一键备车-RVC_一键备车_inactive9次")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1987527(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_convience9次")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1987526(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive7次")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987525(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive主副座加热方向盘")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987524(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive主座加热方向盘")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987523(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive副座加热方向盘")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987522(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [2,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive主副座加热")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987521(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive主座加热")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987520(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive副座加热")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987519(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [2])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive方向盘加热")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987518(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_convience方向盘车外温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987517(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&steeringWheelHeat"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=False)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_getAmbientTempRawData_req_and_feedback_resp(temp=9.1,is_valid=False, timeout=10)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="AmbientTempUnknown")
    
    @allure.title("一键备车-RVC_一键备车_convience方向盘车内温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987516(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&steeringWheelHeat"
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=False)
        self.soa.check_GetCurrentTemperature_req_and_feedback_resp(zone_id=ClimateZoneId.AllZone,temp=10.0,is_valid=False, timeout=10)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CabinTempUnknown")

    @allure.title("一键备车-RVC_一键备车_convience座椅车外温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987515(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&driverSeatHeat"
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=False)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_getAmbientTempRawData_req_and_feedback_resp(temp=9.1,is_valid=False, timeout=10)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="AmbientTempUnknown")

    @allure.title("一键备车-RVC_一键备车_convience座椅车内温度False")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987514(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&driverSeatHeat"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=False)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CabinTempUnknown")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温<10内温=15")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987513(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=0, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=15, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温<10内温=10")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987512(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=0, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_座椅自动外温<10内温=8")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987511(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=0, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=8, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")


    @allure.title("一键备车-RVC_一键备车_座椅自动外温<10内温=5")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987510(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=0, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=5, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")


    @allure.title("一键备车-RVC_一键备车_座椅自动外温<10内温=0")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987509(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=0, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=0, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")


    @allure.title("一键备车-RVC_一键备车_座椅通风运行")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987508(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=10, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")


    @allure.title("一键备车-RVC_一键备车_加热方向盘运行")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987507(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&steeringWheelHeat"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.Off, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Off, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_通风方向盘运行")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987506(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.Off, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Off, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_仅开空调")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987505(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive座椅通风运行")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987504(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid1 = execid0 + "&&&acControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive座椅加热运行")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987503(self, ecu):
        execid = self.tsp.rvc_driver_seat_heat(level=3)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontLeft, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid1 = execid0 + "&&&driverSeatHeat"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive方向盘加热运行")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987502(self, ecu):
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid1 = execid0 + "&&&steeringWheelHeat"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_active9次")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987501(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_driving9次")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987500(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&acControl"
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive座椅加通风换挡")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987499(self, ecu):
        execid = self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.Mid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid1 = execid0 + "&&&acControl"
        execid2 = execid0 + "&&&driverSeatVent"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=20, is_valid=True)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.Off, vent_level=HeatLevel.Off)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")

    @pytest.mark.repeat(100)
    @allure.title("一键备车-RVC_一键备车_inactive压测100次")
    @pytest.mark.stress_test
    def test_rvc_climate_control_caseid_1988773(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(random.uniform(0.8,10))
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive10次")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1990149(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive全部功能")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1990150(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive大于40℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990151(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=50.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=50, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive等于40℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990152(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=50.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=50, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive等于35℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990153(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=30.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=35, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive小于10℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990154(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=0, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=0, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_inactive零下20℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990155(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=-20, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=-20, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_abandoned全部功能")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1990157(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_一键备车_convience全部功能")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1990158(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [1,2,3,4,5])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        time.sleep(1)
        self.soa.notify_NotifyAmbientTempRawData(temp=0, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=0, is_valid=True)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        with allure.step('校验一键备车执行结果'):     
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_inactive大于40℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990156(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=50, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_inactive等于40℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990159(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=40, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_inactive等于35℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990161(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=35, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_inactive等于10℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990163(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_inactive小于10℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990164(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=9.9, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        
    @allure.title("一键备车-RVC_自动空调_CabinTempUnknown")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990165(self, ecu):
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=False)
        self.soa.check_GetCurrentTemperature_req_and_feedback_resp(zone_id=ClimateZoneId.AllZone,temp=10.0,is_valid=False, timeout=10)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CabinTempUnknown")

    @allure.title("一键备车-RVC_自动空调_convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990166(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_ACTIVE")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990167(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_DRIVING")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990168(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_Abandoned等于10℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990169(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=10, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("一键备车-RVC_自动空调_Abandoned小于10℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990170(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=9.9, is_valid=True)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        
    @allure.title("一键备车-RVC_自动空调_AbandonedCabinTempUnknown")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1990171(self, ecu):
        self.mix.tcam_network_sleep()
        self.tsp.rvc_one_click_smart_cockpit_3(selectedLoc = [])
        execid0 = self.tsp.rvc_one_click_smart_cockpit_2()
        execid = execid0 + "&&&conditionalAcControl"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_NotifyAmbientTempRawData(temp=9.1, is_valid=True)
        self.soa.notify_Temperature(climatezoneId = ClimateZoneId.AllZone, temp=9.9, is_valid=False)
        self.soa.check_GetCurrentTemperature_req_and_feedback_resp(zone_id=ClimateZoneId.AllZone,temp=10.0,is_valid=False, timeout=10)
        with allure.step('校验一键备车执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CabinTempUnknown")