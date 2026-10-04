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


@allure.feature("互联服务/远程控制/远控空调控制")
@allure.story("远控空调控制")
class TestRCClimate(TestABCBase):
    def before_class(self, ecu):
        self.rvc_data = deepcopy(rvc_config_data)
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server","CentralLockService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","ClimateControlService_server","InteractiveService_server",
                         "VehicleTimeService_server","WindowService_server","WindowAppService_server",
                         "SteerWheelService_server",'ConfigMasterService_server'])
        time.sleep(60)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        self.soa.notify_SetClimateTempMaintainSts(data="0")
        self.soa.notify_WindowService_NotifyPosition_sts(win_id=[0,1,2,3,],position=0)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))

    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(rvc_config_data), app_name="rvc", publish_id=int(time.time()))
        self.soa.soa_partner.start_single_partner(service="ClimateControlService", role="server")
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.Off)
        self.soa.notify_ClimateFault(fault_id = FaultId.OK)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
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


    @allure.title("远控空调-RVC_远控开启空调_transport")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981113(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail") 
    
    @allure.title("远控空调-RVC_远控开启空调_Factory")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981112(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail")    
    
    @allure.title("远控空调-RVC_远控开启空调_abandoned")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1981111(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_abandoned30自动关闭")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981110(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        time_start = time.time()
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_RemoteOff_req(timeout=1830)
        assert time.time() - time_start > 1770

    @allure.title("远控空调-RVC_远控开启空调_abandoned未上切")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981109(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="NetwakeFail")
        
    @allure.title("远控空调-RVC_远控开启空调_abandoned高压失败")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981108(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")      

    @allure.title("远控空调-RVC_远控开启空调_空调开启失败")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981107(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")  

    @allure.title("远控空调-RVC_远控开启空调_inactive")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1981106(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
    
    @allure.title("远控空调-RVC_远控开启空调_inactive22.5℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981105(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)       
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_ac_control(1,225)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22.5)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
       
    @allure.title("远控空调-RVC_远控开启空调_inactiveLo")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981104(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_ac_control(1,0)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=0)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_inactiveHi")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981103(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        execid1 = self.tsp.rvc_ac_control(1,1)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=1)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_convience")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1981102(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  
    
    @allure.title("远控空调-RVC_远控开启空调_convience22.5℃")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981101(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  
        execid1 = self.tsp.rvc_ac_control(1,225)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22.5,timeout=20)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_convienceLo")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981100(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  
        execid1 = self.tsp.rvc_ac_control(1,0)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=0,timeout=20)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_convienceHi")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981099(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  
        execid1 = self.tsp.rvc_ac_control(1,1)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=1,timeout=20)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_convience空调开启失败")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981098(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")              

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控主驾座椅加热")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981097(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_driver_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控副驾座椅加热")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981096(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_passenger_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")
         

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控左后座椅加热")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981095(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rearleft_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控右后座椅加热")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981094(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rearright_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")        

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控主驾座椅通风")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981093(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控副驾座椅通风")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981092(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_passenger_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")   

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控左后座椅通风")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981091(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rear_left_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控右后座椅通风")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981090(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rear_right_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_远控空调、四座座椅通风、方向盘加热")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981089(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_driver_seat_vent(level=3)
        execid3 = self.tsp.rvc_passenger_seat_vent(level=3)
        execid4 = self.tsp.rvc_rear_left_seat_vent(level=3)
        execid5 = self.tsp.rvc_rear_right_seat_vent(level=3)
        execid6 = self.tsp.rvc_steering_wheel_heat(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.High, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid3, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid4, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid5, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid6, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_远控空调、四座座椅加热、方向盘加热")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981088(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_driver_seat_heat(level=3)
        execid3 = self.tsp.rvc_passenger_seat_heat(level=3)
        execid4 = self.tsp.rvc_rearleft_seat_heat(level=3)
        execid5 = self.tsp.rvc_rearright_seat_heat(level=3)
        execid6 = self.tsp.rvc_steering_wheel_heat(level=3)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid3, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid4, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid5, keywords="Success") 
            assert self.tsp.log_search_remote_vehicle_control(execid=execid6, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_inactive占座")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981087(self, ecu):
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_convience占座")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981086(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_active")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981085(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_driving")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981084(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_维修模式")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981083(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode")

    @allure.title("远控空调-RVC_远控开启空调_N档")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981082(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_FOTAUPDATE")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981081(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控空调-RVC_远控开启空调_FOTAROLLBACK")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981080(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="OTAOngoing"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控空调-RVC_远控开启空调_transport与维修模式")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981079(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="CarModeFail"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控空调-RVC_远控开启空调_开启空调预约座椅通风")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981078(self, ecu):
        self.rvc_data[0]["value"][6]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20,keep_time=3)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        time_start = time.time()
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        time.sleep(60)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=1)
        time.sleep(25)
        assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
        self.soa.check_RemoteOff_req(timeout=190) 
        assert time.time() - time_start > 170    

    @allure.title("远控空调-RVC_远控开启空调_远控后预约")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981077(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1)
        time.sleep(2.5)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)  
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
        time.sleep(25)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="SysBusy")

    @allure.title("远控空调-RVC_远控开启空调_预约空调远控空调")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1981076(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=25,timeout=20) 
        execid = self.tsp.rvc_ac_control(1,220)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SysBusy")
        time.sleep(15)

    @allure.title("远控空调-RVC_远控开启空调_预约空调远控除霜")
    @pytest.mark.full
    def test_rvc_seat_heating_caseid_1981075(self, ecu):
        self.tsp.rvc_taskCmd(appointment_minute=15, temp=250, driver_level=-1, passenger_level=-1, steering_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=25,timeout=20) 
        execid = self.tsp.rvc_defrost_control(1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SysBusy")
        time.sleep(15)

    @allure.title("远控空调-RVC_远控关闭空调_上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981074(self, ecu):
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_RemoteOff_req()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("远控空调-RVC_远控开启空调_上切Active")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981073(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求")
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", 10, None)
        
    @allure.title("远控空调-RVC_远控开启空调_上切Driving")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981072(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求")
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", 10, None)

    @allure.title("远控空调-RVC_远控开启空调_上高压上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981071(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求")
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 
        

    @allure.title("远控空调-RVC_远控开启空调_上高压上切Active")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981070(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求")
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", 10, None)    

    @allure.title("远控空调-RVC_远控开启空调_inactive上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981069(self, ecu):
        self.rvc_data[0]["value"][6]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20,keep_time=3)
        logger.info("已发送高压请求")
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(2)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", 190, None) 

    @allure.title("远控空调-RVC_远控开启空调_维修模式与FOTA")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981068(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="MntnMode"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控除霜-RVC_远控开启空调_inactive上切driving")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981067(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求")
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(2)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控关闭空调_inactive")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1981066(self, ecu):
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_RemoteOff_req()
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控空调-RVC_远控关闭空调_inactive关闭失败")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981065(self, ecu):
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_RemoteOff_req(timeout=20)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("远控空调-RVC_远控关闭空调_convience")
    @pytest.mark.smoke
    def test_rvc_climate_control_caseid_1981064(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_ClimateSystemStatus(ac_status=True,first_row_power_status=True)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_Off_req(zoneid = ClimateZoneId.AllZone, timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status=False,first_row_power_status=False)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控空调-RVC_远控关闭空调_convience关闭失败")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981063(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_ClimateSystemStatus(ac_status=True,first_row_power_status=True)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_Off_req(zoneid = ClimateZoneId.AllZone, timeout=20)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail") 

    @allure.title("远控空调-RVC_远控开启空调_空调状态关闭")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981062(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "RemoteOff", 10, None)

    @allure.title("远控空调-RVC_远控开启空调_用户上车")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981061(self, ecu):
        self.rvc_data[0]["value"][6]["value"] = 3
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20,keep_time=3)
        logger.info("已发送高压请求")
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "SetTemperatureAndOn", 190, None)

    @allure.title("远控空调-RVC_远控开启空调_高压faultId7")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981060(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)       
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow")  

    @allure.title("远控空调-RVC_远控开启空调_高压faultId13")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1981059(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited)  
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited")

    @allure.title("远控空调-RVC_远控开启空调_Abandoned上切convience空调与座椅加热")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981058(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        execid1 = self.tsp.rvc_driver_seat_heat(level=3)
        logger.info("已发送远控空调开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20) 
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        with allure.step('校验远控空调执行结果'):        
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
   
    @allure.title("远控空调-RVC_远控开启空调_Abandoned上切convience空调与座椅通风")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981057(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        logger.info("已发送远控空调开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20) 
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        with allure.step('校验远控空调执行结果'):        
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
   
    @allure.title("远控空调-RVC_远控开启空调_Abandoned上切convience空调与方向盘加热")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981056(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        execid1 = self.tsp.rvc_steering_wheel_heat(3)
        logger.info("已发送远控除霜开启请求")
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=30) 
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        with allure.step('校验远控除霜执行结果'):        
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_二次空调")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981055(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_ac_control(1,220)
        time.sleep(4)
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送两次远控空调开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        time.sleep(20)

    @allure.title("远控空调-RVC_远控开启空调_除霜与空调")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981054(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        execid1 = self.tsp.rvc_defrost_control(1)
        logger.info("已发送远控空调与除霜开启请求")
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="SysBusy")
        time.sleep(20)       

    @allure.title("远控空调-RVC_远控开启空调_空调关闭")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981053(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "RemoteOff", 20, None)

    @allure.title("远控空调-RVC_远控开启空调_convience空调已开启")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981052(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        execid = self.tsp.rvc_ac_control(1,220)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_inactive空调已开启")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981051(self, ecu):
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        execid = self.tsp.rvc_ac_control(1,260)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=26,timeout=20)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_convience响应错误")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981050(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")  

    @allure.title("远控空调-RVC_远控开启空调_16hTCAM重启后远控")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981049(self, ecu):
        self.ssh.type_commands(DeviceName.TCAM, "reboot -f", timeout=5)
        time.sleep(300)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控空调,远控方向盘加热上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981048(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_steering_wheel_heat(level=3)
        logger.info("已发送远控方向盘加热请求")
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控主驾座椅加热上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981047(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_driver_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控副驾座椅加热上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981046(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_passenger_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")
         

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控左后座椅加热上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981045(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rearleft_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.High, timeout=20)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控右后座椅加热上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981044(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rearright_seat_heat(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")        

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控主驾座椅通风上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981043(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_driver_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控副驾座椅通风上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981042(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_passenger_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.High, timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")   

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控左后座椅通风上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981041(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rear_left_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.High, timeout=20)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控右后座椅通风上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981040(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_rear_right_seat_vent(level=3)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.High, timeout=20)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=HeatLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_远控主驾座椅通风,远控空调上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981039(self, ecu):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        execid2 = self.tsp.rvc_ac_control(1,220)
        time.sleep(0.8)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")  
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success") 

    @allure.title("远控空调-RVC_远控开启空调_14abandoned")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981038(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(14)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_abandoned15s内响应关闭")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981037(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(1)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_inactive14s高压")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981036(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(14)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_inactive14s响应")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981035(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(14)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_inactive16s高压失败")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981034(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(16)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")

    @allure.title("远控空调-RVC_远控开启空调_inactive空调16s开启失败")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981033(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(16)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控空调-RVC_远控开启空调_convience14s响应")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981032(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        time.sleep(14)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")  

    @allure.title("远控空调-RVC_远控开启空调_convience16s开启失败")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981031(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft,temp=22,timeout=20)
        time.sleep(16)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")  

    @allure.title("远控空调-RVC_远控关闭空调_inactive14s响应")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981030(self, ecu):
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_RemoteOff_req(timeout=5)
        time.sleep(14)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控关闭空调_inactive16s关闭失败")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981029(self, ecu):
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_RemoteOff_req(timeout=5)
        time.sleep(16)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.Off)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @allure.title("远控空调-RVC_远控关闭空调_convience14s响应")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981028(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_ClimateSystemStatus(ac_status=True,first_row_power_status=True)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_Off_req(zoneid = ClimateZoneId.AllZone, timeout=20)
        time.sleep(14)
        self.soa.notify_ClimateSystemStatus(ac_status=False,first_row_power_status=False)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
   
    @allure.title("远控空调-RVC_远控关闭空调_convience16s关闭失败")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1981027(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_ClimateSystemStatus(ac_status=True,first_row_power_status=True)
        execid = self.tsp.rvc_ac_control(-1,220)
        logger.info("已发送远控空调关闭请求")
        self.soa.check_Off_req(zoneid = ClimateZoneId.AllZone, timeout=20)
        time.sleep(16)
        self.soa.notify_ClimateSystemStatus(ac_status=False,first_row_power_status=False)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")  

    @allure.title("远控空调-RVC_远控开启空调_高压响应为OFF")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987045(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.Off)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail") 

    @allure.title("远控空调-RVC_远控开启空调_远控空调,远控方向盘加热")
    @pytest.mark.sanity
    def test_rvc_climate_control_caseid_1987082(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        logger.info("已发送远控方向盘加热请求")
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")

    @allure.title("远控空调-RVC_远控开启空调_高压流程高压失败")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987083(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        execid2 = self.tsp.rvc_steering_wheel_heat(level=3)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        logger.info("已发送远控方向盘加热请求")
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 20, None)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="RemClimaHvStrtFail")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="RemClimaHvStrtFail")

    @allure.title("远控空调-RVC_远控开启空调_高压流程失败")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1987084(self, ecu):
        execid1 = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        execid2 = self.tsp.rvc_steering_wheel_heat(level=3)
        logger.info("已发送远控方向盘加热请求")
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        time.sleep(15)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="DelayFail")
            assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="DelayFail")

    @allure.title("远控空调-RVC_远控开启空调_高压后BatteryLow")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1988202(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultBatteryLow)  
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="BatteryLow")

    @allure.title("远控空调-RVC_远控开启空调_高压后ActivationLimited")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1988201(self, ecu):
        execid = self.tsp.rvc_ac_control(1,220)
        logger.info("已发送远控空调开启请求")
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        logger.info("已发送高压请求") 
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_ClimateFault(fault_id=FaultId.FaultActivationLimited)  
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="ActivationLimited")

    @allure.title("远控空调-RVC_远控开启空调_abandoned上切convience")
    @pytest.mark.full
    def test_rvc_climate_control_caseid_1989544(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_ac_control(1,220)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "RemoteOn", 1, None)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")