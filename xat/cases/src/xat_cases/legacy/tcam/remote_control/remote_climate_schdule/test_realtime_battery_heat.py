#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import time
import threading
import pytest
import allure
from xat_ecu.api.constants.config_data import *
from copy import deepcopy


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.remote_subscribe.remote_subscribe_class import *


@allure.feature("互联服务/远程控制/电池包立即加热")
@allure.story("电池包立即加热")
class TestBattHeat(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server","CarConfigService_server",'RemoteCtrlService_client',"HighVoltageAppService_server","ConfigMasterService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["CarConfigService_server","HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server"],ignore_func=['GetSeatHeatVentStatus',"GetDefrostSts","GetRemotePowerStatus","GetHeat","GetChargingInfo","getEquipmentInfo",'GetBatteryTemperatureInfo'])
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20)
        self.soa.notify_hvActiveSts(HVActiveSts.Open)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
        # self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[0])
        # self.soa.notify_SeatHeatVentStatus()
        self.soa.notify_SteerWheelService_Heat()
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.Off)
        self.soa.notify_NotifyACDefrostSts()
        self.soa.notify_FrntLeftSeatHeatVentStatus()
        self.soa.notify_FrntRightSeatHeatVentStatus()
        self.soa.notify_RearLeftSeatHeatVentStatus()
        self.soa.notify_RearRightSeatHeatVentStatus()
        self.soa.notify_BookChargingInfo()

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        time.sleep(2)
        
    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20)
        self.soa.notify_hvActiveSts(HVActiveSts.Open)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyConfigList()
        time.sleep(2)

    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
        pass

    def open_realtime_battery_heat(self):
        execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_inactive")
    @pytest.mark.smoke
    def test_realtime_caseid_1988983(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

            
    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_abandoned")
    @pytest.mark.smoke
    def test_realtime_caseid_1988984(self, ecu):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_transport")
    @pytest.mark.sanity
    def test_realtime_caseid_1988979(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('CarModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_convenience")
    @pytest.mark.sanity
    def test_realtime_caseid_1988975(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('UsageModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_MntnMode_true")
    @pytest.mark.sanity
    def test_realtime_caseid_1988972(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('MntnMode',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_GearD")
    @pytest.mark.sanity
    def test_realtime_caseid_1988969(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('ParkFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_UPDATE")
    @pytest.mark.sanity
    def test_realtime_caseid_1988967(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('OTAOngoing',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_ChargingInfo.isConnected")
    @pytest.mark.sanity
    def test_realtime_caseid_1988952(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('PluggerConnected',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_DisplaySOC=7%")
    @pytest.mark.sanity
    def test_realtime_caseid_1988947(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        assert self.tsp.log_search_remote_vehicle_control('SOCLow',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_minTemperature=18℃")
    @pytest.mark.sanity
    def test_realtime_caseid_1988944(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 18)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('HvBattTempHigh', execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_HVActiveStstimeout")
    @pytest.mark.sanity
    def test_realtime_caseid_1988943(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            time.sleep(5.2)
            self.soa.notify_hvActiveSts()
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
            sleep(2)
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req(timeout=20)
            

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态超时")
    @pytest.mark.sanity
    def test_realtime_caseid_1988942(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            time.sleep(31)
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_车端计时满自动关闭")
    @pytest.mark.sanity
    def test_realtime_caseid_1988920(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("40min后自动关闭"): 
            sleep(39*60)
        self.soa.check_SetBatteryHeating_exit_req(timeout=70)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_达到目标电池温度自动关闭")
    @pytest.mark.smoke
    def test_realtime_caseid_1988919(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("达到目标温度"): 
            self.soa.notify_BatteryTemperatureInfo(min_temp = 20)
        self.soa.check_SetBatteryHeating_exit_req(timeout=10)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70) # PNC检查会失败，509报文会直接停止

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_carmode_transport")
    @pytest.mark.sanity
    def test_realtime_caseid_1988918(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("达到目标温度"): 
            self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_exit_req(timeout=10)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70) # PNC检查会失败，509报文会直接停止

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_usagemode_convenience")
    @pytest.mark.sanity
    def test_realtime_caseid_1988914(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("达到目标温度"): 
            self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_exit_req(timeout=10)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70)  # PNC检查会失败，509报文会直接停止

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_用户插枪")
    @pytest.mark.sanity
    def test_realtime_caseid_1988904(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("达到目标温度"): 
            self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        self.soa.check_SetBatteryHeating_exit_req(timeout=10)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70) # PNC检查会失败，509报文会直接停止

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_.DisplaySOC=7%")
    @pytest.mark.sanity
    def test_realtime_caseid_1988902(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("达到目标温度"): 
            self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.check_SetBatteryHeating_exit_req(timeout=10)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70) # PNC检查会失败，509报文会直接停止

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_convenience")
    @pytest.mark.sanity
    def test_realtime_caseid_1988901(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        sleep(2)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)   
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_用户插枪")
    @pytest.mark.sanity
    def test_realtime_caseid_1988887(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        sleep(2)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_convenience")
    @pytest.mark.sanity
    def test_realtime_caseid_1988884(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)  
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=10)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70) # PNC检查会失败，509报文会直接停止

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_用户充电")
    @pytest.mark.sanity
    def test_realtime_caseid_1988869(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=10)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70) # PNC检查会失败，509报文会直接停止


    # @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_下发一键备车指令")
    # @pytest.mark.sanity
    # def test_realtime_caseid_1988846(self, ecu):
    #     self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
    #     self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
    #     time.sleep(1)
    #     with allure.step("下发一键备车的远控电池包立即加热指令"): 
    #         execid = self.tsp.rvc_one_click_smart_cockpit_1(selectedLoc=[6])  # 一键备车指令的电池立即加热暂未定义
    #     self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
    #     self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
    #     self.soa.notify_HVSOCInfo(displaySoc=10.0)
    #     self.soa.notify_ThermalSystemDeviceFaultInfo()
    #     self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
    #     self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
    #     self.soa.notify_hvActiveSts()
    #     self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
    #     time.sleep(5)
    #     self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
    #     self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
    #     self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
    #     assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_400v_CCP #566=0x17")
    @pytest.mark.sanity
    def test_realtime_caseid_1988836(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList(ccp_dict_list = [{"name": 566, "value": 0x17}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_800v_CCP #566=0x10")
    @pytest.mark.sanity
    def test_realtime_caseid_1988830(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList(ccp_dict_list = [{"name": 962, "value": 0x2}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_convenience")
    @pytest.mark.sanity
    def test_realtime_caseid_1988826(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(1)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE) 
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_transport")
    @pytest.mark.sanity
    def test_realtime_caseid_1988823(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(1)
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_GearD")
    @pytest.mark.sanity
    def test_realtime_caseid_1988816(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE) 
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)  
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(1)
        self.soa.s2s_set_gear(Gear.Drv)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_用户插枪")
    @pytest.mark.sanity
    def test_realtime_caseid_1988812(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17) 
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(1)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_用户充电")
    @pytest.mark.sanity
    def test_realtime_caseid_1988811(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17) 
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(1)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=70)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_DisplaySOC_7%")
    @pytest.mark.full
    def test_realtime_caseid_1988810(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_FOTA状态_ROLLBACK")
    @pytest.mark.full
    def test_realtime_caseid_1988813(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_FOTA状态_UPDATE")
    @pytest.mark.full
    def test_realtime_caseid_1988814(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_FOTA状态_UPDATE")
    @pytest.mark.full
    def test_realtime_caseid_1988814(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_GearM")
    @pytest.mark.full
    def test_realtime_caseid_1988815(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_GearN")
    @pytest.mark.full
    def test_realtime_caseid_1988817(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_gear(gear=Gear.Neut)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_GearR")
    @pytest.mark.full
    def test_realtime_caseid_1988818(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_维修模式开启")
    @pytest.mark.full
    def test_realtime_caseid_1988819(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_mntnmode(mntnmode=True)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_dyno")
    @pytest.mark.full
    def test_realtime_caseid_1988820(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_crash")
    @pytest.mark.full
    def test_realtime_caseid_1988821(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_factory")
    @pytest.mark.full
    def test_realtime_caseid_1988822(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_driving")
    @pytest.mark.full
    def test_realtime_caseid_1988824(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_开启过程中SOA服务上线后打断_active")
    @pytest.mark.full
    def test_realtime_caseid_1988825(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        sleep(random.randint(1,9))
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热_下发远控空调打开指令后再下发远控立即加热指令")
    @pytest.mark.full
    def test_realtime_caseid_1988827(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.tsp.rvc_ac_control()
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            self.open_realtime_battery_heat()
        sleep(10)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_400v_CCP #566=0x18")
    @pytest.mark.full
    def test_realtime_caseid_1988831(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList(ccp_dict_list = [{"name": 566, "value": 0x18},{"name": 962, "value": 0x2}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_800v_CCP #566=0x19")
    @pytest.mark.full
    def test_realtime_caseid_1988832(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList(ccp_dict_list = [{"name": 566, "value": 0x19},{"name": 962, "value": 0x2}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_400v_CCP #566=0x17")
    @pytest.mark.full
    def test_realtime_caseid_1988833(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList(ccp_dict_list = [{"name": 566, "value": 0x17}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
    
    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_400v_CCP #566=0x18")
    @pytest.mark.full
    def test_realtime_caseid_1988834(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList(ccp_dict_list = [{"name": 566, "value": 0x18}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_abandoned模式下执行1000次")
    @pytest.mark.skip
    @pytest.mark.repeat(1000)
    @pytest.mark.long_time
    def test_realtime_caseid_1988837(self, ecu):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_inactive模式下执行1000次")
    @pytest.mark.skip
    @pytest.mark.repeat(1000)
    @pytest.mark.long_time
    def test_realtime_caseid_1988838(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_远控关闭_电池预加热动力电池取电加热中")
    @pytest.mark.full
    def test_realtime_caseid_1988839(self, ecu):
        #下发2min后的预约电池加热指令   
        startTime = get_timestamp_after_minutes(2)
        battery_pack_heat_subscribe = battery_pack_heat_Subscribe(slotID=1,status=1,cyclesType=1,AppointWeekday='0000000',startTime=startTime)
        self.tsp.rvc_set_subscribe_task(battery_pack_heat_subscribe)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetOutput_req(timeout=150)
        time.sleep(0.5)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=5)
        time.sleep(4.9)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_subscribe_remote(battery_pack_heat_subscribe, "Success"),f"TCAM远程控制上报到车云的结果校验失败"
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid = self.tsp.rvc_realtime_battery_heat(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_远控关闭_低温自保护动力电池取电加热中")
    @pytest.mark.full
    def test_realtime_caseid_1988840(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        time.sleep(wait_time+1)
        self.soa.battery_protect_exect_planb()
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid = self.tsp.rvc_realtime_battery_heat(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_SOAFail")
    @pytest.mark.full
    def test_realtime_caseid_1988841(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        self.soa.soa_partner.stop_single_partner("HighVoltageService_server")
        time.sleep(10)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      
        self.soa.soa_partner.start_single_partner(service="HighVoltageService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("HighVoltageService_server",timeout=30)    

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_同时下发远控电池立即加热，远控座椅通风指令")
    @pytest.mark.full
    def test_realtime_caseid_1988842(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_vent()
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            self.open_realtime_battery_heat()
        sleep(10)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_同时下发远控电池立即加热，远控座椅加热指令")
    @pytest.mark.full
    def test_realtime_caseid_1988843(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_heat()
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            self.open_realtime_battery_heat()
        sleep(10)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_同时下发远控电池立即加热，远控方向盘加热指令")
    @pytest.mark.full
    def test_realtime_caseid_1988844(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.tsp.rvc_steering_wheel_heat()
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            self.open_realtime_battery_heat()
        sleep(10)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_同时下发远控电池立即加热，远控空调指令")
    @pytest.mark.full
    def test_realtime_caseid_1988845(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.tsp.rvc_ac_control()
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            self.open_realtime_battery_heat()
        sleep(10)

    # @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_远控电池预加热动力电池取电加热中")
    # @pytest.mark.full
    # def test_realtime_caseid_1988847(self, ecu):
    #     self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
    #     self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE) 
    #       #下发2min后的预约电池加热指令   
    #     startTime = get_timestamp_after_minutes(2)
    #     battery_pack_heat_subscribe = battery_pack_heat_Subscribe(slotID=1,status=1,cyclesType=1,AppointWeekday='0000000',startTime=startTime)
    #     self.tsp.rvc_set_subscribe_task(battery_pack_heat_subscribe)
    #     # self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
    #     # self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
    #     self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
    #     self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
    #                                  acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
    #     self.soa.notify_NotifyChargingEquipmentInformation()
    #     self.soa.check_SetOutput_req(timeout=150)
    #     time.sleep(0.5)
    #     self.soa.notify_hvActiveSts()
    #     self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=5)
    #     time.sleep(4.9)
    #     self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
    #     assert self.tsp.log_search_subscribe_remote(battery_pack_heat_subscribe, "Success"),f"TCAM远程控制上报到车云的结果校验失败"
    #     with allure.step("下发远控电池包立即加热指令"): 
    #         execid = self.tsp.rvc_realtime_battery_heat()
    #     self.open_realtime_battery_heat()
    #     assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    # @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_低温自保护动力电池取电加热中")
    # @pytest.mark.full
    # def test_realtime_caseid_1988848(self, ecu):
    #     self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
    #     self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
    #     time.sleep(1)
    #     self.soa.soa_partner.empty_all()
    #     self.soa.notify_NotifyConfigList()
    #     wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
    #     logger.info("等待时间： {0}".format(wait_time))
    #     time.sleep(wait_time+1)
    #     self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
    #     self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
    #                                  acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
    #     self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
    #     self.soa.battery_protect_exect_planb()
    #     with allure.step("下发远控电池包立即加热指令"): 
    #         execid = self.tsp.rvc_realtime_battery_heat()
    #     self.open_realtime_battery_heat()
    #     assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_下发远控开启立即加热指令后再次下发远控电池立即加热关闭指令")
    @pytest.mark.full
    def test_realtime_caseid_1988849(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        execid = self.tsp.rvc_realtime_battery_heat()
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat(-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_连续下发两次远控电池立即加热指令")
    @pytest.mark.full
    def test_realtime_caseid_1988850(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        execid = self.tsp.rvc_realtime_battery_heat()
        sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('Sysbusy',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_DisplaySOC _7%")
    @pytest.mark.full
    def test_realtime_caseid_1988868(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_用户插枪")
    @pytest.mark.full
    def test_realtime_caseid_1988870(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_ChargingInfo(isConnect=True)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_FOTA_ROLLBACK")
    @pytest.mark.full
    def test_realtime_caseid_1988871(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_FOTA_UPDATE")
    @pytest.mark.full
    def test_realtime_caseid_1988872(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_GearM")
    @pytest.mark.full
    def test_realtime_caseid_1988873(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_GearD")
    @pytest.mark.full
    def test_realtime_caseid_1988874(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_GearN")
    @pytest.mark.full
    def test_realtime_caseid_1988875(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_GearR")
    @pytest.mark.full
    def test_realtime_caseid_1988876(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_维修模式开启")
    @pytest.mark.full
    def test_realtime_caseid_1988877(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  




    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_dyno")
    @pytest.mark.full
    def test_realtime_caseid_1988878(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)  


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_crash")
    @pytest.mark.full
    def test_realtime_caseid_1988879(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_factory")
    @pytest.mark.full
    def test_realtime_caseid_1988880(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_transport")
    @pytest.mark.full
    def test_realtime_caseid_1988881(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_driving")
    @pytest.mark.full
    def test_realtime_caseid_1988882(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中等待热管理状态打断_active")
    @pytest.mark.full
    def test_realtime_caseid_1988883(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_DisplaySOC_7%")
    @pytest.mark.full
    def test_realtime_caseid_1988885(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_DisplaySOC_7%")
    @pytest.mark.full
    def test_realtime_caseid_1988885(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_用户充电")
    @pytest.mark.full
    def test_realtime_caseid_1988886(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_FOTA_ROLLBACK")
    @pytest.mark.full
    def test_realtime_caseid_1988888(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_FOTA_UPDATE")
    @pytest.mark.full
    def test_realtime_caseid_1988889(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_M档")
    @pytest.mark.full
    def test_realtime_caseid_1988890(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_D档")
    @pytest.mark.full
    def test_realtime_caseid_1988891(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_N档")
    @pytest.mark.full
    def test_realtime_caseid_1988892(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_R档")
    @pytest.mark.full
    def test_realtime_caseid_1988893(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_维修模式开启")
    @pytest.mark.full
    def test_realtime_caseid_1988894(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_dyno")
    @pytest.mark.full
    def test_realtime_caseid_1988895(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_crash")
    @pytest.mark.full
    def test_realtime_caseid_1988896(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_factory")
    @pytest.mark.full
    def test_realtime_caseid_1988897(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_transport")
    @pytest.mark.full
    def test_realtime_caseid_1988898(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_driving")
    @pytest.mark.full
    def test_realtime_caseid_1988899(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_active")
    @pytest.mark.full
    def test_realtime_caseid_1988900(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_开启过程中上高压打断_active")
    @pytest.mark.full
    def test_realtime_caseid_1988900(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.notify_hvActiveSts()
        assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req()
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1) 



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_用户充电")
    @pytest.mark.full
    def test_realtime_caseid_1988903(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_FOTA_ ROLLBACK")
    @pytest.mark.full
    def test_realtime_caseid_1988905(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_FOTA_UPDATE")
    @pytest.mark.full
    def test_realtime_caseid_1988906(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_GearM")
    @pytest.mark.full
    def test_realtime_caseid_1988907(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_gear(gear=Gear.ManMode)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_GearD")
    @pytest.mark.full
    def test_realtime_caseid_1988908(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_gear(gear=Gear.Drv)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_GearN")
    @pytest.mark.full
    def test_realtime_caseid_1988909(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_gear(gear=Gear.Neut)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_GearR")
    @pytest.mark.full
    def test_realtime_caseid_1988910(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_gear(gear=Gear.Rvs)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_维修模式开启")
    @pytest.mark.full
    def test_realtime_caseid_1988911(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_mntnmode(mntnmode=True)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_usagemode_driving")
    @pytest.mark.full
    def test_realtime_caseid_1988912(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_usagemode_active")
    @pytest.mark.full
    def test_realtime_caseid_1988913(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_carmode_dyno")
    @pytest.mark.full
    def test_realtime_caseid_1988915(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_carmode_crash")
    @pytest.mark.full
    def test_realtime_caseid_1988916(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_carmode_factory")
    @pytest.mark.full
    def test_realtime_caseid_1988917(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_加热中_carmode_factory")
    @pytest.mark.full
    def test_realtime_caseid_1988917(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)




    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_远程电池加热故障")
    @pytest.mark.full
    def test_realtime_caseid_1988931(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
            time.sleep(10.1)
        with allure.step("发送远控电池包立即加热关闭"): 
            execid = self.tsp.rvc_realtime_battery_heat(-1)  
        assert self.tsp.log_search_remote_vehicle_control('StsError',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_开启中_TSP下发远控关闭立即加热指令")
    @pytest.mark.full
    def test_realtime_caseid_1988932(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        with allure.step("发送远控电池包立即加热关闭"): 
            execid01 = self.tsp.rvc_realtime_battery_heat(-1)  
        assert self.tsp.log_search_remote_vehicle_control(execid=execid01),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热关闭_未加热_TSP下发远控关闭立即加热指令")
    @pytest.mark.full
    def test_realtime_caseid_1988933(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("发送远控电池包立即加热关闭"): 
            execid = self.tsp.rvc_realtime_battery_heat(-1)
        self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
        assert self.tsp.log_search_remote_vehicle_control('Success',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        with allure.step("发送远控电池包立即加热关闭"): 
            execid01 = self.tsp.rvc_realtime_battery_heat(-1)
        assert self.tsp.log_search_remote_vehicle_control('Success',execid=execid01),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_HeatingByEmotCoolt")
    @pytest.mark.full
    def test_realtime_caseid_1988934(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatingByEmotCoolt)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_CoolingFinish")
    @pytest.mark.full
    def test_realtime_caseid_1988935(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CoolingFinish)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_CompressorCooling")
    @pytest.mark.full
    def test_realtime_caseid_1988936(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CompressorCooling)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_RadiatorCooling")
    @pytest.mark.full
    def test_realtime_caseid_1988937(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.RadiatorCooling)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_HeatFinished")
    @pytest.mark.full
    def test_realtime_caseid_1988938(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatFinished)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_Default")
    @pytest.mark.full
    def test_realtime_caseid_1988939(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_ Fault")
    @pytest.mark.full
    def test_realtime_caseid_1988940(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Fault)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_热管理状态_Inhibited")
    @pytest.mark.full
    def test_realtime_caseid_1988941(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
            self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
            self.soa.notify_hvActiveSts()
            self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)  # 设置电池加热状态事件
            time.sleep(31)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_minTemperature=0x7FFFFFFF(默认值)")
    @pytest.mark.full
    def test_realtime_caseid_1988945(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_ThermalSystemDeviceFaultInfo()
            self.soa.notify_BatteryTemperatureInfo(min_temp = 0x7FFFFFFF)
            assert self.tsp.log_search_remote_vehicle_control('DelayFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_NetWakeFail")
    @pytest.mark.full
    def test_realtime_caseid_1988948(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            assert self.tsp.log_search_remote_vehicle_control('NetWakeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_优先级判断_3")
    @pytest.mark.full
    def test_realtime_caseid_1988949(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.s2s_set_gear(gear=Gear.Drv) 
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        assert self.tsp.log_search_remote_vehicle_control('ParkFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_优先级判断_2")
    @pytest.mark.full
    def test_realtime_caseid_1988950(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        assert self.tsp.log_search_remote_vehicle_control('UsageModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_优先级判断_1")
    @pytest.mark.full
    def test_realtime_caseid_1988951(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)  
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        assert self.tsp.log_search_remote_vehicle_control('CarModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_FACTORY_FAILED")
    @pytest.mark.full
    def test_realtime_caseid_1988953(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_FAILED) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_FACTORY_SUCCESSFUL")
    @pytest.mark.full
    def test_realtime_caseid_1988954(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_SUCCESSFUL) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_FACTORY_UPDATE")
    @pytest.mark.full
    def test_realtime_caseid_1988955(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_UPDATE) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_FACTORY_TASK")
    @pytest.mark.full
    def test_realtime_caseid_1988956(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.FACTORY_TASK) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_REMOTE_UPDATE")
    @pytest.mark.full
    def test_realtime_caseid_1988957(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.REMOTE_UPDATE) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_REACH_APPOINTMENT")
    @pytest.mark.full
    def test_realtime_caseid_1988958(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_SUCCESSFUL")
    @pytest.mark.full
    def test_realtime_caseid_1988959(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_FAILED_DRIVING")
    @pytest.mark.full
    def test_realtime_caseid_1988960(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_FAILED_NOT_DRIVING")
    @pytest.mark.full
    def test_realtime_caseid_1988961(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_ACTIVE")
    @pytest.mark.full
    def test_realtime_caseid_1988962(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_DOWNLOADING")
    @pytest.mark.full
    def test_realtime_caseid_1988963(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_NEW_TASK")
    @pytest.mark.full
    def test_realtime_caseid_1988964(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_QUERY")
    @pytest.mark.full
    def test_realtime_caseid_1988965(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY) 
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_FOTA_ROLLBACK")
    @pytest.mark.full
    def test_realtime_caseid_1988966(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK) 
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('OTAOngoing',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_GearM")
    @pytest.mark.full
    def test_realtime_caseid_1988968(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('ParkFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_GearN")
    @pytest.mark.full
    def test_realtime_caseid_1988970(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('ParkFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_GearR")
    @pytest.mark.full
    def test_realtime_caseid_1988971(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('ParkFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_driving")
    @pytest.mark.full
    def test_realtime_caseid_1988973(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('UsageModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_active")
    @pytest.mark.full
    def test_realtime_caseid_1988974(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('UsageModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_dyno")
    @pytest.mark.full
    def test_realtime_caseid_1988976(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('CarModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_crash")
    @pytest.mark.full
    def test_realtime_caseid_1988977(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('CarModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_factory")
    @pytest.mark.full
    def test_realtime_caseid_1988978(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        assert self.tsp.log_search_remote_vehicle_control('CarModeFail',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_远程电池加热故障")
    @pytest.mark.full
    def test_realtime_caseid_1988980(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
            time.sleep(10.1)
        with allure.step("开启远控电池包立即加热"): 
            execid = self.tsp.rvc_realtime_battery_heat()  
        assert self.tsp.log_search_remote_vehicle_control('StsError',execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_远程电池加热加热中")
    @pytest.mark.full
    def test_realtime_caseid_1988981(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
        with allure.step("开启远控电池包立即加热"): 
            execid = self.tsp.rvc_realtime_battery_heat()  
        assert self.tsp.log_search_remote_vehicle_control('Success',execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 


    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_远程电池加热正在开启中")
    @pytest.mark.full
    def test_realtime_caseid_1988982(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        with allure.step("下发远控电池包立即加热指令"): 
            execid01 = self.tsp.rvc_realtime_battery_heat()
            assert self.tsp.log_search_remote_vehicle_control('SysBusy',execid=execid01),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池立即加热执行_400v_CCP #566=0x19")
    @pytest.mark.full
    def test_realtime_caseid_1988835(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x19}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态Default持续10s")
    @pytest.mark.sanity
    def test_realtime_caseid_1991082(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态HeatFinished持续10s")
    @pytest.mark.full
    def test_realtime_caseid_1991081(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatFinished)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态RadiatorCooling持续10s")
    @pytest.mark.full
    def test_realtime_caseid_1991080(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.RadiatorCooling)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态CompressorCooling持续10s")
    @pytest.mark.full
    def test_realtime_caseid_1991079(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CompressorCooling)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态CoolingFinish持续10s")
    @pytest.mark.full
    def test_realtime_caseid_1991078(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CoolingFinish)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态Inhibited持续10s")
    @pytest.mark.full
    def test_realtime_caseid_1991077(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态HeatingByEmotCoolt持续10s")
    @pytest.mark.full
    def test_realtime_caseid_1991076(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatingByEmotCoolt)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)




    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_PTC加热中_热管理状态Fault持续10s")
    @pytest.mark.full
    def test_realtime_caseid_1991075(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            self.open_realtime_battery_heat()
            self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Fault)  # 设置电池加热状态事件
            time.sleep(10)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kRealTimeHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
            time.sleep(5)
            self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
            self.soa.check_SetBatteryHeating_exit_req(timeout=5)  # 监听TCAM发送电池加热请求
            self.soa.empty_all()
            self.soa.check_no_SetOutput_req()
            self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x17_CCP962=0x0_minTemperature=20.9℃")
    @pytest.mark.sanity
    def test_realtime_caseid_1991090(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20.9)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x19_CCP962=0x0_minTemperature=20.9℃")
    @pytest.mark.full
    def test_realtime_caseid_1991089(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x19}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20.9)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x17_CCP962=0x2_minTemperature=20.9℃")
    @pytest.mark.full
    def test_realtime_caseid_1991088(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x17}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20.9)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x19_CCP962=0x2_minTemperature=20.9℃")
    @pytest.mark.full
    def test_realtime_caseid_1991087(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x19}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("开启远控电池包立即加热"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20.9)
        self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=23,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x17_CCP962=0x0_minTemperature=21℃")
    @pytest.mark.sanity
    def test_realtime_caseid_1991086(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_BatteryTemperatureInfo(min_temp = 21)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('HvBattTempHigh', execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x19_CCP962=0x0_minTemperature=21℃")
    @pytest.mark.full
    def test_realtime_caseid_1991085(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x19}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_BatteryTemperatureInfo(min_temp = 21)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('HvBattTempHigh', execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x17_CCP962=0x2_minTemperature=21℃")
    @pytest.mark.full
    def test_realtime_caseid_1991084(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x17}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_BatteryTemperatureInfo(min_temp = 21)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('HvBattTempHigh', execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控电池包立即加热-RVC_远控电池包立即加热执行_CCP566=0x19_CCP962=0x2_minTemperature=21℃")
    @pytest.mark.full
    def test_realtime_caseid_1991083(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x19}])
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
            self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
            self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
            self.soa.notify_HVSOCInfo(displaySoc=10.0)
            self.soa.notify_BatteryTemperatureInfo(min_temp = 21)
            self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
            assert self.tsp.log_search_remote_vehicle_control('HvBattTempHigh', execid=execid),f"TCAM远程控制上报到车云的结果校验失败"




@allure.feature("互联服务/远程控制/脉冲加热")
@allure.story("脉冲加热")
class TestplsBattHeat(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server","CarConfigService_server",'RemoteCtrlService_client',"HighVoltageAppService_server","ConfigMasterService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["CarConfigService_server","HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server"],ignore_func=['GetSeatHeatVentStatus',"GetDefrostSts","GetRemotePowerStatus","GetHeat","GetChargingInfo","getEquipmentInfo",'GetBatteryTemperatureInfo'])
        self.rvc_data = deepcopy(rvc_config_data)
        # 设置脉冲加热使能
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(rvc_config_data), app_name="rvc", publish_id=int(time.time()))


        time.sleep(30)
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}]) #设置车辆高压系统为800V
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20)
        self.soa.notify_hvActiveSts(HVActiveSts.Open)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)  # 设置电池加热状态事件
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[0])
        self.soa.notify_SteerWheelService_Heat()
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.Off)
        self.soa.notify_NotifyACDefrostSts()
        self.soa.notify_FrntLeftSeatHeatVentStatus()
        self.soa.notify_FrntRightSeatHeatVentStatus()
        self.soa.notify_RearLeftSeatHeatVentStatus()
        self.soa.notify_RearRightSeatHeatVentStatus()
        self.soa.notify_BookChargingInfo()

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        time.sleep(2)


    def after_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 20)
        self.soa.notify_hvActiveSts(HVActiveSts.Open)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kDefault) #设置脉冲加热状态事件
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}]) #设置车辆高压系统为800V
        time.sleep(2)

    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
        pass



    def open_plsrealtime_battery_heat(self):
        execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"




    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_inactive")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991074(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                # self.open_plsrealtime_battery_heat()
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_abandoned")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991073(self, ecu):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_minTemperature=-2℃")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991072(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -2)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_minTemperature=-30℃")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991071(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -30)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_DisplaySOC=90%")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991070(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=90.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_DisplaySOC=-1%")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991069(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        time.sleep(10)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_HVActiveStstimeout")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991068(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(5.1)
        self.soa.notify_hvActiveSts()
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_高压状态Open")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991067(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        time.sleep(5.1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_高压状态Keep")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991066(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Keep)
        time.sleep(5.1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_高压状态Open_And_Req_Act_Dcha")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991065(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open_And_Req_Act_Dcha)
        time.sleep(5.1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_factory")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991064(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)   
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_transport")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991063(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)   
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_crash")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991062(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)   
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_dyno")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991061(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)   
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_convenience")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991060(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)  
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_active")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991059(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)  
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_driving")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991058(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)  
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_维修模式开启")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991057(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_R档")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991056(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_N档")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991055(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_D档")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991054(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_M档")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991053(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_FOTA_UPDATE")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991052(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_FOTA_ROLLBACK")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991051(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_用户插枪")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991050(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)  
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_用户充电")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991049(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)  
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中上高压打断_DisplaySOC_7%")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991048(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        self.soa.notify_HVSOCInfo(displaySoc=7.0) 
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_transport")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991047(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_factory")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991046(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_crash")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991045(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_dyno")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991044(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_convenience")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991043(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_active")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991042(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_driving")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991041(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_维修模式开启")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991040(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_GearR")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991039(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_GearN")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991038(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_GearD")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991037(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_GearM")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991036(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_FOTA_UPDATE")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991035(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_FOTA_UPDATE")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991035(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_FOTA_ROLLBACK")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991034(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_用户插枪")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991033(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_用户充电")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991032(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态打断_DisplaySOC _7%")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991031(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_下发远控关闭指令")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991030(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid01 = self.tsp.rvc_realtime_battery_heat(op=-1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid01),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_transport")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991029(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_factory")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991028(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_crash")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991027(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_dyno")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991026(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_convenience")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991025(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_active")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991024(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_driving")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991023(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_维修模式开启")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991022(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_GearR")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991021(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_GearN")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991020(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_GearD")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991019(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_GearM")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991018(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_FOTA_UPDATE")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991017(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_FOTA_ROLLBACK")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991016(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_用户插枪")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991015(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_用户充电")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991014(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_DisplaySOC_7%")
    @pytest.mark.smoke
    def test_plsrealtime_caseid_1991013(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_倒计时结束跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991012(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(8*60)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_CCP#962改变跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991011(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(10)
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])  
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_温度达到0度跳转PTC加热")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991010(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(10)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_开启过程中等待脉冲加热状态超时跳转PTC加热")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1991009(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_开启后PulseHeatingSts=kIdle持续300ms跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991008(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kIdle) #设置脉冲加热状态事件
        time.sleep(0.35)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_开启后PulseHeatingSts=kInit持续300ms跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991007(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kInit) #设置脉冲加热状态事件
        time.sleep(0.35)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_开启后PulseHeatingSts=kHeatFinish持续300ms跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991006(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeatFinish) #设置脉冲加热状态事件
        time.sleep(0.35)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_开启后PulseHeatingSts=kError持续300ms跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991005(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kError) #设置脉冲加热状态事件
        time.sleep(0.35)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_开启后PulseHeatingSts=kInhibit持续300ms跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991004(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kInhibit) #设置脉冲加热状态事件
        time.sleep(0.35)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_退出_开启后PulseHeatingSts=kDefault持续300ms跳转PTC加热")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991003(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kDefault) #设置脉冲加热状态事件
        time.sleep(0.35)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(60)
        #跳转PTC加热
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_transport")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991001(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_factory")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991000(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_crash")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990999(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_dyno")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990998(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_convenience")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1990997(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_active")
    @pytest.mark.sanity
    def test_plsrealtime_caseid_1990996(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_driving")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990995(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_维修模式开启")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990994(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_GearR")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990993(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_GearN")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990992(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_GearD")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990991(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_GearM")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990990(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_FOTA状态_UPDATE")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990989(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_FOTA状态_ROLLBACK")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990988(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_用户插枪")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990987(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_用户充电")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990986(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_DisplaySOC_7%")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990985(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启失败跳转PTC加热时打断_下发远控关闭指令")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990984(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(30.1)
        self.soa.notify_pulseHeatingInfo(pulseHeating_sts=PulseHeatingSts.kHeating) #设置脉冲加热状态事件
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid_01 = self.tsp.rvc_realtime_battery_heat(op=-1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(keywords="DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control(execid=execid_01),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_transport")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990983(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_factory")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990982(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_crash")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990981(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_dyno")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990980(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_convenience")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990979(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_active")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990978(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_driving")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990977(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_维修模式开启")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990976(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_GearR")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990975(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_GearN")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990974(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_GearD")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990973(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_GearM")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990972(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_FOTA状态_UPDATE")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990971(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_FOTA状态_ROLLBACK")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990970(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_用户插枪")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990969(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_ChargingInfo(is_charging=False,isConnect=True,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_用户充电")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990968(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_ChargingInfo(is_charging=True,isConnect=False,plug_sts=PluggerSts.Disconnected)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_DisplaySOC_7%")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990967(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        self.soa.notify_HVSOCInfo(displaySoc=7.0)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_脉冲加热开启成功后跳转PTC加热时打断_下发远控关闭指令")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990966(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 0)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)      
        time.sleep(10)
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid_01 = self.tsp.rvc_realtime_battery_heat(op=-1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid_01),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_前置条件_CCP#962 =0")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990964(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_前置条件_DisplaySOC=19%")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990963(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=19.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    
    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_前置条件_DisplaySOC=91%")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990962(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=91.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_前置条件_minTemperature=-1.9℃")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990961(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -1.9)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_前置条件_minTemperature=-30.1℃")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990960(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -30.1)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远控脉冲加热-RVC_远控电池包立即加热_立即电池加热开启中_等待上高压过程中下发远控电池包加热关闭指令")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990959(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        time.sleep(2)
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid_01 = self.tsp.rvc_realtime_battery_heat(op=-1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control(execid=execid_01),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控电池包立即加热_立即电池加热开启中_等待脉冲加热状态反馈中下发远控电池包加热关闭指令")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990958(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = -10)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetHvPulseHeating_req(timeout=10)
        time.sleep(5)
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid_01 = self.tsp.rvc_realtime_battery_heat(op=-1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOff,modeSts=RemoteBatteryHeatingModeSts.kIdle,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.check_SetHvPulseHeating_req(on=False,timeout=10)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid,keywords="DelayFail"),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control(execid=execid_01),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热_RVC_远控电池包立即加热_低温自保护开启中_下发远控电池包关闭指令")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990957(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time+1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(10)
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid = self.tsp.rvc_realtime_battery_heat(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热_RVC_远控电池包立即加热_预约加热开启中_下发远控电池包关闭指令")
    @pytest.mark.skip
    def test_plsrealtime_caseid_1990956(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)

    @allure.title("远控脉冲加热_RVC_远控电池包立即加热_低温自保护开启中_下发远控电池包开启指令")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990955(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time+1)
        self.soa.check_SetOutput_req(timeout=10)
        time.sleep(0.5)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28, timeout=5)
        time.sleep(4.9)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_ThermalSystemDeviceFaultInfo()
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("RVC_远控电池包立即加热_预约加热开启中_下发远控电池包开启指令")
    @pytest.mark.skip
    def test_plsrealtime_caseid_1990954(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time+1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.ConnectedWithPower)



    @allure.title("RVC_远控电池包立即加热_低温自保护开启中_下发远控电池包关闭指令")
    @pytest.mark.full
    def test_plsrealtime_caseid_1990953(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time+1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(10)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid = self.tsp.rvc_realtime_battery_heat(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("RVC_远控电池包立即加热_预约加热开启中_下发远控电池包关闭指令")
    @pytest.mark.skip
    def test_plsrealtime_caseid_1990952(self, ecu):
  
        with allure.step("下发远控电池包立即加热关闭指令"): 
            execid = self.tsp.rvc_realtime_battery_heat(op=-1)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远控脉冲加热-RVC_远控脉冲加热执行_加热中_下发脉冲加热使能=False")
    @pytest.mark.full
    def test_plsrealtime_caseid_1991002(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x10}])
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
                self.open_plsrealtime_battery_heat()
        time.sleep(5)
        #下发脉冲加热未使能
        self.rvc_data = deepcopy(rvc_config_data)
        self.rvc_data[0]["value"][19]["value"] = 0 #设置脉冲加热未使能
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        self.soa.check_no_SetBatteryHeating_req(timeout=5)


    @allure.title("远控电池包立即加热-RVC_远控脉冲加热执行_前置条件_脉冲加热未使能")
    @pytest.mark.full
    def test_realtime_caseid_1990965(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        self.rvc_data = deepcopy(rvc_config_data)
        self.rvc_data[0]["value"][19]["value"] = 0 #设置脉冲加热未使能
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        self.soa.notify_HVSOCInfo(displaySoc=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=10)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)  # 设置电池加热状态事件
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kOn,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kHVBattery,timeout=30)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,timeout=1)
        self.rvc_data = deepcopy(rvc_config_data)
        self.rvc_data[0]["value"][19]["value"] = 1 #设置脉冲加热使能
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"