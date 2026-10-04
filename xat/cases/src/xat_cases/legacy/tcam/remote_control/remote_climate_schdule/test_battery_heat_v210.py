#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import threading
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务/远程控制/电池预加热")
@allure.story("电池预加热")
class TestBattProtect(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server","RemoteCtrlService_client", "CarConfigService_server",
                         "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server","HighVoltageAppService_server"])
        self.mix.start_get_request_and_send_response_to_tcam_thread(["CarConfigService_server","HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "RtcAlarmService_client",
                         "ClimateControlService_server",
                         "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server"],ignore_func=['GetSeatHeatVentStatus',"GetDefrostSts","GetRemotePowerStatus","GetHeat","GetChargingInfo",
                         "getEquipmentInfo",'GetBatteryTemperatureInfo', "SetBatteryHeating", "SetOutput"])
        sleep(2)

    def before_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        self.soa.notify_NotifyConfigList()
        self.soa.notify_SeatHeatVentStatus()
        self.soa.notify_SteerWheelService_Heat()
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.Off)
        self.soa.notify_NotifyACDefrostSts()
        self.soa.notify_FrntLeftSeatHeatVentStatus()
        self.soa.notify_BookChargingInfo(source=DischargeSourceId.kDefault)
        self.soa.empty_all()
        
    def after_each_func(self, ecu):
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)


    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        pass

    @allure.title("RVC_远控电池预加热_kDC执行A方案")
    @pytest.mark.smoke
    def test_batt_schedule_heating_dc_execting_planA_caseid_1989784(self, ecu):
        time.sleep(180)
        self.mix.tcam_network_sleep()
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热_kDC执行A方案_inactive")
    @pytest.mark.smoke
    def test_batt_schedule_heating_dc_execting_planA_caseid_1989783(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_01")
    @pytest.mark.smoke
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989782(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.9)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_07")
    @pytest.mark.smoke
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989776_1980040(self, ecu):
        self.soa.notify_HVSOCInfo(displaySoc=20)
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-13.1, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案")
    @pytest.mark.smoke
    def test_battery_schedule_heating_default_exect_planA_caseid_1989774_1989559(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)        

    @allure.title("RVC_远控电池预加热_执行B方案_01")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_caseid_1989738(self, ecu):
        self.mix.tcam_network_sleep()
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_01")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_caseid_1989737(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-50)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_02")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_caseid_1989683(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id, ), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热未插枪取消预约设置单次Success")
    @pytest.mark.smoke
    def test_battery_schedule_heating_cancel_schedule_caseid_1980258(self, ecu):
        time.sleep(180)
        self.mix.tcam_network_sleep()
        [task_time, exec_id] = self.tsp.rvc_taskCmd(appointment_minute=63)[1:]
        time.sleep(30)
        cancel_execid = self.tsp.cancel_cock_reserv_task(task_time)
        self.soa.check_no_NotifyTimeUpEventInfo(timeout=180)

    # @allure.title("RVC_远控电池预加热未插枪修改预约设置单次Success")
    # @pytest.mark.smoke
    # def test_battery_schedule_heating_modify_schedule_time_caseid_1980254(self, ecu):
    #     time.sleep(180)
    #     self.mix.tcam_network_sleep()
    #     [task_time, exec_id] = self.tsp.rvc_taskCmd(appointment_minute=63)[1:]
    #     time.sleep(60)
    #     exec_id2 = self.tsp.rvc_taskCmd(fixed=True, appointment_minute=65)[2]
    #     self.soa.check_no_NotifyTimeUpEventInfo(timeout=120)
    #     self.soa.check_NotifyTimeUpEventInfo_event(timeout=120)

    @allure.title("RVC_远控电池预加热未插枪预约执行电池温度-13℃")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_tempture_negative_13_caseid_1980229(self, ecu):
        time.sleep(180)
        self.mix.tcam_network_sleep()
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热未插枪预约执行_INACTIVE")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_tempture_negative_13_caseid_1980222(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热未插枪预约执行_SOC等于20%")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_sco20_caseid_1980207(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_HVSOCInfo(displaySoc=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行电池温度-13℃")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_not_jidu_chargepile_caseid_1980188(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_HVSOCInfo(displaySoc=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[2])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行电池温度-13℃")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_jidu_public_chargepile_caseid_1980146(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_HVSOCInfo(displaySoc=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_INACTIVE")
    @pytest.mark.smoke
    def test_battery_schedule_heating_exect_planB_jidu_public_chargepile_caseid_1980139(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_HVSOCInfo(displaySoc=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案20℃")
    @pytest.mark.smoke
    def test_battery_schedule_heating_dc_exect_planA_20C_caseid_1980105(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        assert self.tsp.log_search_battery(execid=exec_id, keyword="HvBattTempHigh"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"




    @allure.title("RVC_远控电池预加热_kDC执行A方案执行_INACTIVE")
    @pytest.mark.smoke
    def test_battery_schedule_heating_dc_exect_planA_caseid_1980055(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.9, acdc_type=ACDCType.kDC,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案执行_INACTIVE")
    @pytest.mark.smoke
    def test_battery_schedule_heating_dc_exect_planA_caseid_1980055_1989786(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_02")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989781_1989557(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)


    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_01")
    @pytest.mark.sanity
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989773_1989554(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_01")
    @pytest.mark.sanity
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989764(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_01")
    @pytest.mark.sanity
    def test_battery_schedule_heating_acdc_exect_planA_fail_transfor_planB_caseid_1989755(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案高压超时")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_timeout_caseid_1989736(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        time.sleep(5)
        self.soa.notify_hvActiveSts()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_convenience_caseid_1989731(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_pluggerStatus=3")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_connectedwithpower_caseid_1989715(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_MntnMode=true")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_mntnmode_caseid_1989714(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_GearR")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_gearr_caseid_1989713(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_FOTA状态update")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_update_caseid_1989709(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态超时")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_timeout_caseid_1989707(self, ecu):
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=5)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        time.sleep(40.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                              source=HeatingEnergySource.kNone, timeout=5)
        time.sleep(5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_convenience_caseid_1989700(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_03")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_caseid_1989682(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_convenience_caseid_1989677(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_convenience_caseid_1989657(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_convenience_caseid_1989637(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_convenience_caseid_1989617(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_convenience_caseid_1989597(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(39.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_远程立即电池加热开启中")
    @pytest.mark.sanity
    def test_battery_schedule_heating_battery_heating_opening_caseid_1989579(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Default) 
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        time.sleep(9.5)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="SysBusy"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"



    @allure.title("RVC_远控电池预加热_远程立即电池加热工作中")
    @pytest.mark.sanity
    def test_battery_schedule_heating_battery_heating_ongoing_caseid_1989578(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)  
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Default)  
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        time.sleep(9.5)
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
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_远程电池加热故障")
    @pytest.mark.sanity
    def test_battery_schedule_heating_battery_heating_error_caseid_1989575(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Default) 
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        time.sleep(9.5)
        self.soa.notify_HVSOCInfo(displaySoc=20.0)
        self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
        self.soa.check_SetOutput_req(timeout=5)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
        time.sleep(30.1)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kError,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=3)
        appointment_time, formattedUseVehicleTime,exec_id01 = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id01,keyword="StsError"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热未插枪预约执行电池温度-13℃-ccp566#0x17")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_ccp566_0x17_caseid_1987647(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热未插枪预约执行电池温度-13℃-ccp566#0x18")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_ccp566_0x18_caseid_1987646(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热未插枪预约执行电池温度-13℃-ccp566#0x19")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_ccp566_0x18_caseid_1987645(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案_ccp0x17")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_ccp566_0x17_caseid_1987644(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-10, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案_ccp0x18")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_800v_ccp566_0x18_caseid_1987643(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=15, acdc_type=ACDCType.kDC,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案_ccp0x19")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_800v_ccp566_0x19_caseid_1987642(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=16, acdc_type=ACDCType.kDC,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案_ccp0x19")
    @pytest.mark.sanity
    def test_battery_schedule_heating_dc_exect_planA_800v_ccp566_0x19_caseid_1987642(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=14.7, acdc_type=ACDCType.kDC,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行电池温度17℃_ccp0x19（800V）")
    @pytest.mark.sanity
    def test_batt_schedule_heating_dc_execting_planA_caseid_1987639(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}, {"name": 962, "value": 0x02}])
        time.sleep(180)
        self.mix.tcam_network_sleep()
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热预约退出_加热后carmode改变为transport")
    @pytest.mark.sanity
    def test_battery_schedule_heating_default_exect_planA_exit_by_transport_caseid_1987044(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=13.1, acdc_type=ACDCType.kDefault,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_远控电池预加热预约退出_加热后usagemode改变为convenience")
    @pytest.mark.sanity
    def test_battery_schedule_heating_default_exect_planA_exit_by_convenience_caseid_1987040(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=12.9, acdc_type=ACDCType.kDefault,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_远控电池预加热预约退出_加热后minTemperature=-9.9℃_PlanB")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_exit_by_tempture_satisfied_caseid_1987037(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_远控电池预加热预约退出_kDC执行A方案加热后minTemperature=20.1℃")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planA_exit_by_tempture_satisfied_caseid_1987037(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.9, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.notify_BatteryTemperatureInfo(min_temp=20.1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)


    @allure.title("RVC_远控电池预加热预约退出_加热后DisplaySOC=17%")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_exit_by_soc17_caseid_1987034(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_Default_over 5s")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planA_exit_by_thermalreqsts_default_over5s_caseid_1987031(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=11.1, acdc_type=ACDCType.kDC,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)
        time.sleep(11)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                              source=HeatingEnergySource.kCharger, timeout=3)

    @allure.title("RVC_远控电池预加热预约退出_未插枪场景(条件1)加热后pluggerStatus=3_planB1")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_exit_by_connectedwithpower_caseid_1987022(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热未插枪预约执行_HVActiveSts=open")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_hvactivests_open_caseid_1980191(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        time.sleep(9.9)
        # self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行_SOC等于20%")
    @pytest.mark.sanity
    def test_battery_schedule_heating_exect_planB_soc20_caseid_1980166(self, ecu):
        self.soa.notify_HVSOCInfo(displaySoc=20)
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[2])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_kDC执行A方案预约执行电池温度18℃")
    @pytest.mark.smoke
    def test_battery_schedule_heating_dc_exect_planA_18C_caseid_1980062(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=18)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(5)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="HvBattTempHigh"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行电池温度-5℃")
    @pytest.mark.smoke
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1980063(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-5.0, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_MntnMode=true")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_mntnmode_caseid_1990053(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_GearR")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_gearr_caseid_1990052(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_gearn_caseid_1990051(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)


    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_gearn_caseid_1990050(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_gearm_caseid_1990049(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_FOTA状态update")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_update_caseid_1990048(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)


    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_rollback_caseid_1990047(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_rollback_caseid_1990047(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=True, value=-10.0, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断Mntnmode")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_mntnmode_caseid_1990046(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_GearR")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_gearr_caseid_1990045(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=10.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_gearn_caseid_1990044(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=10.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_geard_caseid_1990043(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=10.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_gearm_caseid_1990042(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=10.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_FOTA状态update")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_update_caseid_1990041(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=10.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_rollback_caseid_1990040(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=10.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_MntnMode=true")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_mntnmode_caseid_1990039(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_GearR")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_gearr_caseid_1990038(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_gearr_caseid_1990037(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_gearr_caseid_1990036(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_gearm_caseid_1990035(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_FOTA状态update")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_update_caseid_1990034(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_rollback_caseid_1990033(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_MntnMode=true")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_mntnmode_caseid_1990032(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearR")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_gear_caseid_1990031(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_gearn_caseid_1990030(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_geard_caseid_1990029(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_gearm_caseid_1990028(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_FOTA状态update")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_update_caseid_1990027(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_rollback_caseid_1990026(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_MntnMode=true")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_mntnmode_caseid_1990025(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_GearR")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_gearr_caseid_1990024(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_gearn_caseid_1990023(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_geard_caseid_1990022(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_gearm_caseid_1990021(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_FOTA状态update")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_update_caseid_1990020(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_rollback_caseid_1990019(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_MntnMode=true")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_mntnmode_caseid_1990018(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearR")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_gearr_caseid_1990017(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_gearn_caseid_1990016(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_geard_caseid_1990015(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_gearm_caseid_1990014(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_FOTA状态update")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_update_caseid_1990013(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_rollback_caseid_1990012(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_充电状态true")
    @pytest.mark.full
    def test_battery_schedule_heating_charging_ongoing_caseid_1989787(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_NotifyChargingEquipmentInformation()
        assert self.tsp.log_search_battery(execid=exec_id, keyword="ChargingOngoing"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_加热中TSP下发远控电池包立即加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_exit_by_realtime_battery_heating_caseid_1989785(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.tsp.rvc_realtime_battery_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)


    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_03")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989780(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_04")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989779(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_05")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989778(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_06")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989777(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_kDC执行A方案失败跳转B方案_08")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_transfor_planB_caseid_1989775(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Fault)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_02")
    @pytest.mark.full
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989772(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_03")
    @pytest.mark.full
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989771(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_04")
    @pytest.mark.full
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989770(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_05")
    @pytest.mark.full
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989769(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_06")
    @pytest.mark.full
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989768(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_07")
    @pytest.mark.full
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989767(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kDefault执行A方案失败跳转执行方案B_08")
    @pytest.mark.full
    def test_battery_schedule_heating_default_exect_planA_fail_transfor_planB_caseid_1989766(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Fault)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kAC执行A方案")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_caseid_1989765(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.9, acdc_type=ACDCType.kAC, value=20.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_02")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989763(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_03")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989762(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_04")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989761(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_05")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989760(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_06")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989759(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_07")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989758(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Inhibited,
                                             plug_sts2=PluggerSts.ConnectedWithPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_kAC执行A方案失败跳转执行方案B_08")
    @pytest.mark.full
    def test_battery_schedule_heating_ac_exect_planA_fail_transfor_planB_caseid_1989757(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kAC,
                                             value=20.0, thermal_sts=ThermalReqSts.Fault,
                                             plug_sts2=PluggerSts.ConnectedWithPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989756(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=9.9, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.ConnectedWithPower,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_02")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989754(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-12.1, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_03")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989753(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-13, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_04")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989752(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-19.9, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_05")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989751(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-29.9, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_06")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989750(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-18.7, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_07")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989749(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-21.3, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Inhibited,
                                             plug_sts2=PluggerSts.ConnectedWithPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kACDC执行A方案失败跳转执行方案B_08")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989748(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-15.5, acdc_type=ACDCType.kACDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Fault,
                                             plug_sts2=PluggerSts.ConnectedWithPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989747(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-14.1, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.ConnectedWithPower,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_01")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989746(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-15.2, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_02")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989745(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31.1, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_03")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989744(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-100.1, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_04")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989743(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-16.1, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_05")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989742(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-34.5, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_06")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989741(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-17.7, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_07")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989740(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-28, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Inhibited,
                                             plug_sts2=PluggerSts.ConnectedWithPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_kUnknown执行A方案失败跳转执行方案B_08")
    @pytest.mark.full
    def test_battery_schedule_heating_acdc_exect_planA_caseid_1989739(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-18, acdc_type=ACDCType.kUnknown,
                                             value=20.0, thermal_sts=ThermalReqSts.Fault,
                                             plug_sts2=PluggerSts.ConnectedWithPower)
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断transport")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_transport_caseid_1989735(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断factory")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_factory_caseid_1989734(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断crash")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_crash_caseid_1989733(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_dyno_caseid_1989732(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断active")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_active_caseid_1989730(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断driving")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_driving_caseid_1989729(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_remote_ac_caseid_1989728(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_ac_control()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_remote_seat_heat_caseid_1989727(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_driver_seat_heat()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_remote_seat_vent_caseid_1989726(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_driver_seat_heat()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_remote_stwlheat_caseid_1989725(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_remote_defrost_caseid_1989724(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_defrost_control()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_remote_cold_down_caseid_1989723(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_cold_down()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_remote_cold_down_caseid_1989722(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_heat_up()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发预约远控开启空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_schedule_ac_caseid_1989721(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发预约远控开启座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_schedule_ac_caseid_1989720(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发预约远控开启座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_schedule_ac_caseid_1989719(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "DriverVent_level":1}).start()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_TSP下发预约远控开启方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_schedule_ac_caseid_1989718(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_SetOutput_req(timeout=2)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":1}).start()
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_DisplaySOC==17%")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_soc17_caseid_1989717(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_charging_caseid_1989716(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=True)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_gearr_caseid_1989712(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_GearN")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_gearr_caseid_1989712(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_geard_caseid_1989711(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_gearm_caseid_1989710(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_update_caseid_1989708(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待高压状态时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_hvactivests_interrupted_by_rollback_caseid_1989708(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态Fault")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_fault_caseid_1989705(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Fault)
        time.sleep(39.9)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                              source=HeatingEnergySource.kNone, timeout=5)
        time.sleep(5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断transport")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_transport_caseid_1989704(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断Factory")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_factory_caseid_1989703(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断crash")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_crash_caseid_1989702(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_dyno_caseid_1989701(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断active")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_active_caseid_1989699(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断driving")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_driving_caseid_1989698(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_remote_ac_caseid_1989697(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.tsp.rvc_ac_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_remote_seat_heating_caseid_1989696(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.tsp.rvc_passenger_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_remote_seat_venting_caseid_1989695(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.tsp.rvc_passenger_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_remote_stwl_heating_caseid_1989694(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_remote_defrost_caseid_1989693(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.tsp.rvc_defrost_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_remote_cold_down_caseid_1989692(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.tsp.rvc_cold_down()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_remote_heat_up_caseid_1989691(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.tsp.rvc_heat_up()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控预约空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_schedule_ac_caseid_1989690(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控预约座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_schedule_seat_heating_caseid_1989689(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控预约座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_schedule_seat_heating_caseid_1989688(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "PassengerVent_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_TSP下发远控预约方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_schedule_stwh_heating_caseid_1989687(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_soc17_caseid_1989686(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_charging_caseid_1989685(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_charging_caseid_1989685(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=True)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_pluggerStatus==3")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_charging_caseid_1989685(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态打断_pluggerStatus==3")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_interrupted_by_charging_caseid_1989684(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_transport")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_transport_caseid_1989681(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_factory")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_factory_caseid_1989680(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_crash")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_crash_caseid_1989679(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_crash")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_crash_caseid_1989679(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_dyno_caseid_1989678(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_active")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_active_caseid_1989676(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_driving")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_driving_caseid_1989675(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_remote_ac_caseid_1989674(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.tsp.rvc_ac_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_remote_seat_heating_caseid_1989673(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.tsp.rvc_rearleft_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_remote_seat_venting_caseid_1989672(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.tsp.rvc_rear_left_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_remote_stwh_heating_caseid_1989671(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_remote_defrost_caseid_1989670(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.tsp.rvc_defrost_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_remote_cold_down_caseid_1989669(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.tsp.rvc_cold_down()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_remote_heat_up_caseid_1989668(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.tsp.rvc_heat_up()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控预约空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_schedule_ac_caseid_1989667(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控预约座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_schedule_seat_heating_caseid_1989666(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "RearLeft_level": 1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控预约座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_schedule_seat_venting_caseid_1989665(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "RearLeftVent_level": 1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_TSP下发远控预约方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_schedule_stwh_heating_caseid_1989664(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "RearLeftVent_level": 1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_soc17_caseid_1989663(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_判断插直流枪后1s内打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_acdctype_interruputed_by_charging_caseid_1989662(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_transport")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_transport_caseid_1989661(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_factory")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_factory_caseid_1989660(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_crash")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_crash_caseid_1989659(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_dyno_caseid_1989658(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_active")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_active_caseid_1989656(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_driving")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_driving_caseid_1989655(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_remote_ac_caseid_1989654(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.tsp.rvc_ac_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_remote_seat_heating_caseid_1989653(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.tsp.rvc_rearright_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_remote_seat_venting_caseid_1989652(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.tsp.rvc_rear_right_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_remote_stwh_heating_caseid_1989651(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.tsp.rvc_rear_right_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_remote_defrost_caseid_1989650(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.tsp.rvc_defrost_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_remote_cold_down_caseid_1989649(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.tsp.rvc_cold_down()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_remote_heat_up_caseid_1989648(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.tsp.rvc_heat_up()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_schedule_ac_caseid_1989647(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_schedule_seat_heating_caseid_1989646(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "RearRight_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_schedule_seat_heating_caseid_1989645(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "RearRightVent_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_schedule_seat_heating_caseid_1989644(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_soc17_caseid_1989643(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus时打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_connectedwithpower_interruputed_by_charging_caseid_1989642(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.check_no_SetCharging_req(timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_transport")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_transport_caseid_1989641(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_factory")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_factory_caseid_1989640(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_crash")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_crash_caseid_1989639(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_dyno_caseid_1989638(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_active")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_active_caseid_1989636(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_driving")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_driving_caseid_1989635(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_ac_caseid_1989634(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.tsp.rvc_ac_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_seat_heating_caseid_1989633(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.tsp.rvc_driver_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_seat_venting_caseid_1989632(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.tsp.rvc_driver_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_seat_venting_caseid_1989631(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_stwh_heating_caseid_1989630(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.tsp.rvc_defrost_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_cold_down_caseid_1989629(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.tsp.rvc_cold_down()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_heat_up_caseid_1989628(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.tsp.rvc_heat_up()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_ac_caseid_1989627(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_seat_heating_caseid_1989626(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_seat_venting_caseid_1989625(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "DriverVent_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_stwh_heating_caseid_1989624(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_soc17_caseid_1989623(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_charging_caseid_1989622(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_transport")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_transport_caseid_1989621(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_factory")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_factory_caseid_1989620(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_crash")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_crash_caseid_1989619(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_dyno_caseid_1989618(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_active")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_active_caseid_1989616(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_driving")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_driving_caseid_1989615(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_ac_caseid_1989614(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_ac_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_seat_heating_caseid_1989613(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_driver_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_seat_venting_caseid_1989612(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_driver_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_seat_venting_caseid_1989611(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_driver_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_seat_venting_caseid_1989611(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_defrost_caseid_1989610(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_defrost_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_cold_down_caseid_1989609(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_cold_down()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_remote_heat_up_caseid_1989608(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.tsp.rvc_heat_up()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_schedule_ac_caseid_1989607(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_schedule_seat_heating_caseid_1989606(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_schedule_seat_venting_caseid_1989605(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "PassengerVent_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_schedule_stwh_heating_caseid_1989604(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_soc17_caseid_1989603(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态时打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_charging_caseid_1989602(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_transport")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_transport_caseid_1989601(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_factory")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_factory_caseid_1989600(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_crash")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_crash_caseid_1989599(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_dyno_caseid_1989598(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_active")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_active_caseid_1989596(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_driving")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_driving_caseid_1989595(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_remote_ac_caseid_1989594(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_ac_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_remote_seat_heating_caseid_1989593(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_rearleft_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_remote_seat_venting_caseid_1989592(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_rear_left_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_remote_stwh_heating_caseid_1989591(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_remote_defrost_caseid_1989590(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_defrost_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_remote_cold_down_caseid_1989589(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_cold_down()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_remote_heat_up_caseid_1989588(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_heat_up()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_schedule_ac_caseid_1989587(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_schedule_seat_heating_caseid_1989586(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "RearLeft_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_schedule_seat_venting_caseid_1989585(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "RearLeftVent_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_schedule_stwh_heating_caseid_1989584(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":1}).start()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_soc17_caseid_1989583(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_等待热管理状态失败跳转执行B方案时打断_isCharging==True")
    @pytest.mark.full
    def test_battery_schedule_heating_dc_exect_planA_fail_to_exect_planB_interrupted_by_charging_caseid_1989582(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=-31, value=20, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_低温自保护开启中")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_fail_when_battery_protect_openning_caseid_1989581(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time+9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=50)[2]
        assert self.tsp.log_search_battery(execid=exec_id, keyword="SysBusy"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_预约电池加热开启中")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_fail_when_battery_heating_openning_caseid_1989580(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-50)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=50)[2]
        assert self.tsp.log_search_battery(execid=exec_id, keyword="SysBusy"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_预约电池加热工作中")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_fail_when_battery_heating_running_caseid_1989577(self, ecu):
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id, ), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        time.sleep(30)
        exec_id2 = self.tsp.rvc_taskCmd(appointment_minute=50)[2]
        time.sleep(15)
        assert self.tsp.log_search_battery(execid=exec_id2), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_极低温自保护工作中")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_fail_when_battery_protec_running_caseid_1989576(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time+9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb()
        time.sleep(30)
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=50)[2]
        time.sleep(15)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_400v_CCP #566=0x17")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_400v_ccp566_0x17_caseid_1989574(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
  
    @allure.title("RVC_远控电池预加热_执行A方案_400v_CCP #566=0x19")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_400v_ccp566_0x19_caseid_1989573(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_400v_CCP #566=0x18")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_400v_ccp566_0x18_caseid_1989572(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_400v_CCP #566=0x17")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_400v_ccp566_0x17_caseid_1989571(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_400v_CCP #566=0x19")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_400v_ccp566_0x19_caseid_1989570(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_400v_CCP #566=0x18")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_400v_ccp566_0x18_caseid_1989569(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_800v_CCP #566=0x17")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_800v_ccp566_0x17_caseid_1989568(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x17}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.8, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_800v_CCP #566=0x19")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_800v_ccp566_0x19_caseid_1989567(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x19}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_800v_CCP #566=0x10")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_800v_ccp566_0x10_caseid_1989566(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x10}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行A方案_800v_CCP #566=0x18")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_800v_ccp566_0x18_caseid_1989565(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x18}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_800v_CCP #566=0x17")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_800v_ccp566_0x17_caseid_1989564(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_800v_CCP #566=0x19")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_800v_ccp566_0x17_caseid_1989563(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_800v_CCP #566=0x10")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_800v_ccp566_0x17_caseid_1989562(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x10}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_执行B方案_800v_CCP #566=0x18")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_800v_ccp566_0x17_caseid_1989561(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热_加热中退出_GearR")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_exit_by_gearr_caseid_1989558(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.5, acdc_type=ACDCType.kDC,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热_加热中退出_GearD")
    @pytest.mark.full
    def test_battery_schedule_heating_exec_planB_exit_by_geard_caseid_1989556(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热_加热中退出_GearM")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planA_800v_exit_by_gearm_caseid_1989555(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x17}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=17.8, acdc_type=ACDCType.kDefault,
                                             value=20.0, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热_加热中退出_FOTA状态rollback")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_800v_exit_by_rollback_caseid_1989553(self, ecu):
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}, {"name": 962, "value": 0x02}])
        exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)[2]
        self.soa.check_NotifyPrepareTimeUpEventInfo_event(timeout=120)
        self.soa.check_NotifyTimeUpEventInfo_event(timeout=20)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后远程预约控制开启方向盘加热")
    @pytest.mark.full
    def test_batt_heat_caseid_1980003(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,steering_level=1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_远控电池预加热预约退出_加热后远控预约控制开启座椅加热")
    @pytest.mark.full
    def test_batt_heat_caseid_1980004(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,driver_level=1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后远程预约控制开启空调")
    @pytest.mark.full
    def test_batt_heat_caseid_1980005(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_远控电池预加热预约退出_加热后立即远控开启座舱通风")
    @pytest.mark.full
    def test_batt_heat_caseid_1980007(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,PassengerVent_level=1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后立即远控开启前挡最大除霜")
    @pytest.mark.full
    def test_batt_heat_caseid_1980008(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.tsp.rvc_defrost_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后立即远控开启方向盘加热")
    @pytest.mark.full
    def test_batt_heat_caseid_1980009(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_远控电池预加热预约退出_加热后立即远控开启座椅通风")
    @pytest.mark.full
    def test_batt_heat_caseid_1980010(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.tsp.rvc_driver_seat_vent()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后立即远控开启座椅加热")
    @pytest.mark.full
    def test_batt_heat_caseid_1980011(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.tsp.rvc_driver_seat_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后立即远控开启空调")
    @pytest.mark.full
    def test_batt_heat_caseid_1980012(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.tsp.rvc_ac_control()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)




    @allure.title("RVC_远控电池预加热未插枪场景_SOC=17%")
    @pytest.mark.full
    def test_batt_heat_caseid_1980016(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热未插枪场景_ Driving")
    @pytest.mark.full
    def test_batt_heat_caseid_1980017(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热未插枪场景_ Active")
    @pytest.mark.full
    def test_batt_heat_caseid_1980018(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热未插枪场景_ Convenience")
    @pytest.mark.full
    def test_batt_heat_caseid_1980019(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热未插枪场景_ DYNO")
    @pytest.mark.full
    def test_batt_heat_caseid_1980020(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热未插枪场景_ CRASH")
    @pytest.mark.full
    def test_batt_heat_caseid_1980021(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热未插枪场景_TRANSPORT")
    @pytest.mark.full
    def test_batt_heat_caseid_1980022(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_SOC等于1%")
    @pytest.mark.full
    def test_batt_heat_caseid_1980038(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_HVSOCInfo(displaySoc=1)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="SOCLow"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"  


    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_SOC等于19%")
    @pytest.mark.full
    def test_batt_heat_caseid_1980039(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_HVSOCInfo(displaySoc=19)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="SOCLow"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"  


    @allure.title("RVC_远控电池预加热_kDC执行A方案预约执行_SOC等于20%")
    @pytest.mark.sanity
    def test_batt_heat_caseid_1980040(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_HVSOCInfo(displaySoc=20)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)



    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FOTA为UpdateFailedNotDriving")
    @pytest.mark.full
    def test_batt_heat_caseid_1980042(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        
    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FOTA为Active")
    @pytest.mark.full
    def test_batt_heat_caseid_1980043(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)


    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FOTA为Downloading")
    @pytest.mark.full
    def test_batt_heat_caseid_1980044(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FOTA为NewTask")
    @pytest.mark.full
    def test_batt_heat_caseid_1980045(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FOTA为Query")
    @pytest.mark.full
    def test_batt_heat_caseid_1980046(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)


    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_batt_heat_caseid_1980047(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)
        time.sleep(2)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(118)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="OTAOngoing"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FOTA为UPDATE")
    @pytest.mark.full
    def test_batt_heat_caseid_1980048(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)
        time.sleep(2)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(118)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="OTAOngoing"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_挡位GearD")
    @pytest.mark.full
    def test_batt_heat_caseid_1980049(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_gear(gear=Gear.Drv)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="ParkFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_挡位GearR")
    @pytest.mark.full
    def test_batt_heat_caseid_1980050(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="ParkFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_维修模式True")
    @pytest.mark.full
    def test_batt_heat_caseid_1980051(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)
        time.sleep(2)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(118)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="MntnMode"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_DRIVING")
    @pytest.mark.full
    def test_batt_heat_caseid_1980052(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="UsageModeFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_ACTIVE")
    @pytest.mark.full
    def test_batt_heat_caseid_1980053(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="UsageModeFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_CONVENIENCE")
    @pytest.mark.full
    def test_batt_heat_caseid_1980054(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="UsageModeFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_kDC执行A方案执行_INACTIVE")
    @pytest.mark.smoke
    def test_batt_heat_caseid_1980055(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)



    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_DYNO")
    @pytest.mark.full
    def test_batt_heat_caseid_1980056(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(118)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="CarModeFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_ CRASH")
    @pytest.mark.full
    def test_batt_heat_caseid_1980057(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(118)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="CarModeFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_FACTORY")
    @pytest.mark.full
    def test_batt_heat_caseid_1980058(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(118)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="CarModeFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"

    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行_TRANSPORT")
    @pytest.mark.full
    def test_batt_heat_caseid_1980059(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=62)
        time.sleep(2)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(118)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="CarModeFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"



    @allure.title(" RVC_远控电池预加热_kDC执行A方案预约执行电池温度18℃")
    @pytest.mark.sanity
    def test_batt_heat_caseid_1980062(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=18)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="HvBattTempHigh"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)



    @allure.title("RVC_远控电池预加热集度私桩插枪场景5预约执行电池温度-5℃")
    @pytest.mark.sanity
    def test_batt_heat_caseid_1980063(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-5)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)





    @allure.title("RVC_远控电池预加热集度私桩插枪预约执行_ pluggerStatus==3")
    @pytest.mark.full
    def test_batt_heat_caseid_1980068(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=15)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_HVActiveSts ==OPEN")
    @pytest.mark.full
    def test_batt_heat_caseid_1980107(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.soa_partner.empty_all()
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        time.sleep(10.1)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_ HVActiveSts ==OPEN_AND_REQ_ACTV_DCHA")
    @pytest.mark.full
    def test_batt_heat_caseid_1980108(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.soa_partner.empty_all()
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open_And_Req_Act_Dcha)
        time.sleep(10.1)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_ HVActiveSts ==OPEN_AND_REQ_ACTV_DCHA")
    @pytest.mark.full
    def test_batt_heat_caseid_1980108(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.soa_partner.empty_all()
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open_And_Req_Act_Dcha)
        time.sleep(10.1)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)


    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_ HVActiveSts ==KEEP_STS")
    @pytest.mark.full
    def test_batt_heat_caseid_1980109(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.soa_partner.empty_all()
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Keep)
        time.sleep(10.1)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_FOTA为UpdateFailedNotDriving")
    @pytest.mark.full
    def test_batt_heat_caseid_1980126(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_FOTA为Active")
    @pytest.mark.full
    def test_batt_heat_caseid_1980127(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_FOTA为Downloading")
    @pytest.mark.full
    def test_batt_heat_caseid_1980128(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)


    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_FOTA为NewTask")
    @pytest.mark.full
    def test_batt_heat_caseid_1980129(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行_FOTA为Query")
    @pytest.mark.full
    def test_batt_heat_caseid_1980130(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行电池温度-12℃")
    @pytest.mark.full
    def test_batt_heat_caseid_1980145(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="HvBattTempHigh"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)



    @allure.title("RVC_远控电池预加热集度公桩插枪预约执行电池温度-13℃")
    @pytest.mark.smoke
    def test_batt_heat_caseid_1980146(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)


    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行_SOC等于20%")
    @pytest.mark.sanity
    def test_batt_heat_caseid_1980166(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_HVSOCInfo(displaySoc=20)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)


    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行_FOTA为UpdateFailedNotDriving")
    @pytest.mark.full
    def test_batt_heat_caseid_1980168(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)



    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行_FOTA为Active")
    @pytest.mark.full
    def test_batt_heat_caseid_1980169(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)

    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行_FOTA为Downloading")
    @pytest.mark.full
    def test_batt_heat_caseid_1980170(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)


    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行_FOTA为NewTask")
    @pytest.mark.full
    def test_batt_heat_caseid_1980171(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)


    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行_FOTA为Query")
    @pytest.mark.full
    def test_batt_heat_caseid_1980172(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.check_SetOutput_req(timeout=15)  # 监听TCAM发送上高压请求
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        assert self.tsp.log_search_battery(execid=exec_id),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)
        self.soa.check_high_voltage_setoutput_request(check_time=10)


    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行电池温度-11℃")
    @pytest.mark.full
    def test_batt_heat_caseid_1980186(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-11)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-11)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="HvBattTempHigh"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)


    @allure.title("RVC_远控电池预加热非集度桩插枪预约执行电池温度-12℃")
    @pytest.mark.full
    def test_batt_heat_caseid_1980187(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kReady,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-11)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12)
        assert self.tsp.log_search_battery(execid=exec_id,keyword="HvBattTempHigh"),f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)



    @allure.title("RVC_远控电池预加热预约退出_kDC执行A方案加热后minTemperature=20.1℃")
    @pytest.mark.sanity
    def test_batt_schedule_heating_caseid_1987035(self, ecu):
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryTemperatureInfo(min_temp=20.1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        


    @allure.title("RVC_远控电池预加热预约退出_加热后carmode改变为dyno")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987041(self, ecu):
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.9)
        self.soa.battery_protect_exect_plana(min_temp=13.1, acdc_type=ACDCType.kDefault,
                                             value=20, thermal_sts=ThermalReqSts.Heating,
                                             modests=RemoteBatteryHeatingModeSts.kBookHeat)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)


    @allure.title("RVC_远控电池预加热_执行B方案等待热管理状态Inhibited")
    @pytest.mark.full
    def test_battery_schedule_heating_exect_planB_wait_batteryheatinginfo_fault_caseid_1989706(self, ecu):
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=-12.1)
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-10.0, timeout=3)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(40.1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat, heatsts=RemoteBatteryHeatingSts.kError,
                                              source=HeatingEnergySource.kNone, timeout=5)
        time.sleep(5)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热电池温度为0x7FFFFFFF(默认值)")
    @pytest.mark.full
    def test_battery_heating_caseid_1987019(self, ecu):
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        time.sleep(9.5)
        self.soa.notify_ChargingInfo(isConnect=False, is_charging=False)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.notify_BatteryTemperatureInfo(min_temp=0x7FFFFFFF)
        assert self.tsp.log_search_battery(execid=exec_id, keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热预约退出_执行B方案加热后pluggerStatus=3_planB3")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987020(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id, ), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)

    @allure.title("RVC_远控电池预加热预约退出_执行B方案加热后pluggerStatus=3_planB2")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987021(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id, ), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)



    @allure.title("RVC_远控电池预加热预约开启中热管理状态!= Heating连续4s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987023(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)
        time.sleep(9)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=60)


    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_Fault 5s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987024(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Fault)
        time.sleep(11)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_HeatingByEmotCoolt_over 5s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987025(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatingByEmotCoolt)
        time.sleep(11)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_Inhibited_over 5s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987026(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(11)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_CoolingFinish_over 5s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987027(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CoolingFinish)
        time.sleep(11)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_CompressorCooling_over 5s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987028(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CompressorCooling)
        time.sleep(11)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_RadiatorCooling_over 5s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987029(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.RadiatorCooling)
        time.sleep(11)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后热管理状态ThermalReqSts_HeatFinished_over 5s")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987030(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatFinished)
        time.sleep(11)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后usagemode改变为driving")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987038(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后usagemode改变为active")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987039(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热预约退出_加热后carmode改变为crash")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987042(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热预约退出_加热后carmode改变为factory")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987043(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热_前置条件不满足_座椅加热通风工作中")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987409(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_level=HeatLevel.High,heat_work_sts=HeatVentWorkStatus.On)
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()
        self.soa.notify_FrntLeftSeatHeatVentStatus()


    @allure.title("RVC_远控电池预加热_前置条件不满足_方向盘加热=low")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987410(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()

    @allure.title("RVC_远控电池预加热_前置条件不满足_方向盘加热=Mid")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987411(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()

    @allure.title("RVC_远控电池预加热_前置条件不满足_方向盘加热=High")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987412(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()

    @allure.title("RVC_远控电池预加热_前置条件不满足_空调状态处于工作中")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987413(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()


    @allure.title("RVC_远控电池预加热_前置条件不满足_除霜状态处于工作中")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1987414(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_NotifyACDefrostSts(climate_defrost=True,defrost_max=True)
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="DelayFail"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.soa_partner.empty_all()




    @allure.title("RVC_远控电池预加热未插枪预约执行电池温度-13℃ccp0x20(非预期值)")
    @pytest.mark.full
    def test_battery_heating_caseid_1987651(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x20}])
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热未插枪预约执行电池温度-13℃ccp错误)")
    @pytest.mark.full
    def test_battery_heating_caseid_1987703(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x1}])
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time.sleep(9.9)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-13)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.battery_protect_exect_planb(value=-10.0, modests=RemoteBatteryHeatingModeSts.kBookHeat)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        # assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("RVC_远控电池预加热_加热中退出_通知预约交流充电的激活任务 ")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1991091(self, ecu):
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=20.0, timeout=5)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kBookHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        assert self.tsp.log_search_battery(execid=exec_id), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.soa.notify_BookChargingInfo(workSts=ACBookChargingWorkSts.kBookStsStandby)
        self.soa.send_SetBookEvent_req(ser_name=" ac_book_charging",book_type="book charging start time",sch_time=120) 
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=130)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_远控电池预加热_优先级判断06")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1991092(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_HVSOCInfo(displaySoc=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False,plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BookChargingInfo(workSts=ACBookChargingWorkSts.kBookStsStandby,startTime=int(time.time()+9*60))
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="SOCLow"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热_优先级判断05")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1991093(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False,plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BookChargingInfo(workSts=ACBookChargingWorkSts.kBookStsStandby,startTime=int(time.time()+9*60))
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="ChargingOngoing"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热_10min内有预约交流充电的激活任务")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1991094(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_BookChargingInfo(workSts=ACBookChargingWorkSts.kBookStsStandby,startTime=int(time.time()+9*60))
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="AcBookCharging"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_远控电池预加热_充电桩在 (充电、预加热）输出")
    @pytest.mark.full
    def test_battery_schedule_heating_caseid_1991095(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False,plug_sts=PluggerSts.ConnectedWithPower)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        assert self.tsp.log_search_battery(execid=exec_id,keyword="ChargingOngoing"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
