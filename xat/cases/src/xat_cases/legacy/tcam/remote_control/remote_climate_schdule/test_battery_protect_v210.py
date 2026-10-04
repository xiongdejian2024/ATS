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
import threading


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
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        self.soa.notify_SeatHeatVentStatus()
        self.soa.notify_SteerWheelService_Heat()
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.Off)
        self.soa.notify_NotifyACDefrostSts()
        self.soa.notify_FrntLeftSeatHeatVentStatus()
        self.soa.notify_BookChargingInfo(source=DischargeSourceId.kDefault)
        
    def after_each_func(self, ecu):
        time.sleep(10)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)
        self.soa.notify_BookChargingInfo(source=DischargeSourceId.kDefault)

    def after_class(self, ecu):
        self.mix.stop_get_request_and_send_response_to_tcam_thread()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        pass


    @allure.title("RVC_低温自保护_kDC执行A方案_inactive")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_caseid_1990008_1990010(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_01")
    @pytest.mark.smoke
    def test_batt_protect_dc_exect_planA_fail_to_exect_planB_caseid_1990007(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.9)
        self.soa.battery_protect_exect_planb()
        
    @allure.title("RVC_低温自保护_kDefault执行A方案_inactive")
    @pytest.mark.smoke
    def test_batt_protect_kDefault_execting_planA_caseid_1989999(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(10)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_01")
    @pytest.mark.smoke
    def test_batt_protect_kDefault_exect_planA_fail_to_exect_planB_caseid_1989998(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDefault, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.9)
        self.soa.battery_protect_exect_planb()


    @allure.title("RVC_低温自保护_执行B方案_02")
    @pytest.mark.smoke
    def test_batt_protect_execting_planB_caseid_1989916(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_执行B方案_01")
    @pytest.mark.smoke
    def test_batt_protect_execting_planB_caseid_1989963(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_充电状态true")
    @pytest.mark.sanity
    def test_batt_protect_ischarging_true_caseid_1990011(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护加热中退出_isCharging ==True")
    @pytest.mark.sanity
    def test_batt_protect_ischarging_true_caseid_1990011(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_02")
    @pytest.mark.sanity
    def test_batt_protect_dc_exect_planA_fail_to_exect_planB_caseid_1990006(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithoutPower)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.9)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_07")
    @pytest.mark.sanity
    def test_batt_protect_dc_exect_planA_fail_to_exect_planB_caseid_1990001(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithoutPower)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.5)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(39.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.9)
        self.soa.battery_protect_exect_planb()


    @allure.title("RVC_低温自保护_kAC执行A方案_inactive")
    @pytest.mark.sanity
    def test_batt_protect_ac_execting_planA_caseid_1989990(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kAC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        time.sleep(9.5)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kAC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(29.5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)


    @allure.title("RVC_低温自保护_执行B方案高压超时")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_hvActiveSts_timeout_caseid_1989962(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        time.sleep(5.1)
        self.soa.notify_hvActiveSts()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_convenience")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_wait_hvActiveSts_interrupted_by_convenience_caseid_1989957(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_hvActiveSts()
        self.soa.check_no_SetOutput_req(timeout=4)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控极速制冷指令")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_wait_hvActiveSts_interrupted_by_climatecooling_caseid_1989947(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        self.tsp.rvc_cold_down()
        time.sleep(1)
        self.soa.notify_hvActiveSts()
        self.soa.check_no_SetOutput_req(timeout=4)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_pluggerStatus ==3")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_wait_hvActiveSts_interrupted_by_connectedwithpower_caseid_1989941(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(1)
        self.soa.notify_hvActiveSts()
        self.soa.check_no_SetOutput_req(timeout=4)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_执行B方案等待热管理状态超时")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_wait_batteryheatinginfo_timeout_caseid_1989940(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        time.sleep(40.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        time.sleep(5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断convenience")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_wait_batteryheatinginfo_interrupted_by_convenience_caseid_1989933(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_no_SetOutput_req(timeout=6)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行B方案_03")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_caseid_1989915(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_convenience")
    @pytest.mark.sanity
    def test_batt_protect_dc_exect_planA_acdctype_interruputed_by_convenience_caseid_1989910(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        time.sleep(0.9)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_convenience")
    @pytest.mark.sanity
    def test_batt_protect_dc_exect_planA_wait_connectedwithpower_interruputed_by_convenience_caseid_1989890(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.1)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=10)


    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_convenience")
    @pytest.mark.sanity
    def test_batt_protect_dc_exect_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_convenience_caseid_1989870(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_convenience")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_wait_batteryheatinginfo_interrupted_by_convenience_caseid_1989850(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=5)   


    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_convenience")
    @pytest.mark.sanity
    def test_batt_protect_dc_exect_planA_fail_to_exect_planB_interrupted_by_convenience_caseid_1989830(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(39.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_isCharging ==True")
    @pytest.mark.sanity
    def test_batt_protect_dc_exect_planA_fail_to_exect_planB_interrupted_by_charging_caseid_1989826(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=3)
        time.sleep(9.9)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(39.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_no_SetOutput_req(timeout=6)


    @allure.title("RVC_低温自保护_加热中_MntnMode =true")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_exit_mntnmode_caseid_1989794(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(10)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_加热中_GearR")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_exit_gearr_caseid_1989793(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(10)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_加热中_FOTA状态update")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_exit_fotaupdate_caseid_1989789(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(10)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_400v_CCP #566=0x19")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planA_400v_ccp566_0x19_caseid_1989812_1989792(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-21.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-18.0, thermal_sts=ThermalReqSts.Heating)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_执行A方案_800v_CCP #566=0x10")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planA_800v_ccp566_0x10_caseid_1989811_1989791(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x10}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行A方案_800v_CCP #566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planA_800v_ccp566_0x18_caseid_1989810_1989790(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18},{"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_执行A方案_800v_CCP #566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planA_800v_ccp566_0x18_caseid_1989809_1989788(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17},{"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-21.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-18.0, thermal_sts=ThermalReqSts.Heating)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_执行A方案_800v_CCP #566=0x19")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planA_800v_ccp566_0x19_caseid_1989808(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19},{"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-21.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-18.0, thermal_sts=ThermalReqSts.Heating)

    @allure.title("RVC_低温自保护_执行B方案_400v_CCP #566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_400v_ccp566_0x18_caseid_1989807(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_执行B方案_400v_CCP #566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_400v_ccp566_0x17_caseid_1989806(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18.0)

    @allure.title("RVC_低温自保护_执行B方案_400v_CCP #566=0x19")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_400v_ccp566_0x19_caseid_1989805(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18.0)

    @allure.title("RVC_低温自保护_执行B方案_800v_CCP #566=0x10")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x10_caseid_1989804(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_执行B方案_800v_CCP #566=0x10")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x10_caseid_1989804(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_执行B方案_800v_CCP #566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x18_caseid_1989803(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02},{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_执行B方案_800v_CCP #566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x17_caseid_1989802(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18.0)

    @allure.title("RVC_低温自保护_执行B方案_800v_CCP #566=0x19")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x19_caseid_1989801(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02},{"name": 566, "value": 0x19}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18.0)

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_MntnMode =true")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_mntnmode_caseid_1990102(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.1)
        self.soa.notify_hvActiveSts()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=5)
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_MntnMode =true")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_mntnmode_caseid_1990102(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=2)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.1)
        self.soa.notify_hvActiveSts()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=5)
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_gearr_caseid_1990101(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_gearr_caseid_1990101(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()
        
    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_GearN")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_gearn_caseid_1990100(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_GearD")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_geard_caseid_1990099(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_GearM")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_gearm_caseid_1990098(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_FOTA状态update")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_fota_update_caseid_1990097(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_FOTA状态rollback")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_fota_rollback_caseid_1990096(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_transport")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_carmode_transport_caseid_1989961(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_factory")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_carmode_factory_caseid_1989960(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_crash")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_carmode_crash_caseid_1989959(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_dyno")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_carmode_dyno_caseid_1989958(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_active")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_usagemode_active_caseid_1989956(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_driving")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_usagemode_driving_caseid_1989955(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_soc_17_caseid_1989954(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.notify_HVSOCInfo(displaySoc=17)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_isCharging=True")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_ischarging_true_caseid_1989953(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remoteac_caseid_1989952(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.tsp.rvc_ac_control()
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_seatheating_caseid_1989951(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.tsp.rvc_driver_seat_heat()
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_seatventing_caseid_1989950(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.tsp.rvc_driver_seat_vent()
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_swhheating_caseid_1989949(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.tsp.rvc_steering_wheel_heat()
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_defrost_caseid_1989948(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.tsp.rvc_defrost_control()
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_heatup_caseid_1989946(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.tsp.rvc_heat_up()
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_colddown_caseid_1989947(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        self.tsp.rvc_cold_down()
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_HVActiveSts_closed()

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_schedule_ac_caseid_1989945(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=1,driver_level=-1,passenger_level=-1,steering_level=-1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_schedule_seatheating_caseid_1989944(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行B方案等待高压过程中打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_schedule_seatventing_caseid_1989943(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("VC_低温自保护_执行B方案等待高压过程中打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_hvactivests_interrupted_by_remote_schedule_swhheating_caseid_1989942(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_HVActiveSts()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,steering_level=1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_MntnMode=true")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_mntnmode_true_caseid_1990095(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_gearr_caseid_1990094(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_GearN")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_gearn_caseid_1990093(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_GearD")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_geard_caseid_1990092(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_GearM")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_gearm_caseid_1990091(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_FOTA状态update")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_fota_update_caseid_1990090(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()


    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_FOTA状态rollback")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_fota_update_caseid_1990089(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断transport")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_wait_thermalreqsts_interrupted_by_carmode_transport_caseid_1990089(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.1)
        self.soa.check_battery_protect_planB_stoped_with_ThermalReqSts_heating()


    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_MntnMode=true")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_mntnmode_caseid_1990088(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_gearr_caseid_1990087(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_GearN")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_gearn_caseid_1990086(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_GearD")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_geard_caseid_1990085(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_GearM")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_gearm_caseid_1990084(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_FOTA状态update")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_fota_update_caseid_1990083(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_FOTA状态rollback")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_fota_rollback_caseid_1990082(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_MntnMode=true")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_mntnmode_caseid_1990081(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_gearr_caseid_1990080(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_GearN")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_gearr_caseid_1990079(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_GearD")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_geard_caseid_1990078(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_GearM")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_gearm_caseid_1990077(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_FOTA状态update")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_fota_update_caseid_1990076(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_fota_rollback_caseid_1990075(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_MntnMode=true")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_mntnmode_caseid_1990074(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Disconnected)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_gearr_caseid_1990073(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Disconnected)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearN")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_gearn_caseid_1990072(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Disconnected)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearD")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_geard_caseid_1990071(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Disconnected)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_GearM")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_gearm_caseid_1990070(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Disconnected)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_FOTA状态update")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_fota_update_caseid_1990069(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Disconnected)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_fota_rollback_caseid_1990068(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Disconnected)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_MntnMode=true")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_mntnmode_caseid_1990067(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_gearr_caseid_1990066(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_GearN")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_gearn_caseid_1990065(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_GearD")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_geard_caseid_1990064(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_GearM")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_gearm_caseid_1990063(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_FOTA状态update")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_fota_update_caseid_1990062(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_fota_rollback_caseid_1990061(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_MntnMode=true")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_mntnmode_caseid_1990060(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearR")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_gearr_caseid_1990059(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearN")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_gearn_caseid_1990058(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearD")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_gearn_caseid_1990057(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_GearM")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_gearm_caseid_1990056(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_FOTA状态updat")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_fota_update_caseid_1990055(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Fault)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_FOTA状态rollback")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_fota_rollback_caseid_1990054(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Fault)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_03")
    @pytest.mark.full
    def test_batt_protect_dc_planA_fail_transfor_planB_caseid_1990005(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_04")
    @pytest.mark.full
    def test_batt_protect_dc_planA_fail_transfor_planB_caseid_1990004(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_05")
    @pytest.mark.full
    def test_batt_protect_dc_planA_fail_transfor_planB_caseid_1990003(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_06")
    @pytest.mark.full
    def test_batt_protect_dc_planA_fail_transfor_planB_caseid_1990002(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDC执行A方案失败跳转B方案执行_08")
    @pytest.mark.full
    def test_batt_protect_dc_planA_fail_transfor_planB_caseid_1990000(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_02")
    @pytest.mark.full
    def test_batt_protect_default_planA_fail_transfor_planB_caseid_1989997(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kDefault, plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_03")
    @pytest.mark.full
    def test_batt_protect_default_planA_fail_transfor_planB_caseid_1989996(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kDefault, plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_04")
    @pytest.mark.full
    def test_batt_protect_default_planA_fail_transfor_planB_caseid_1989995(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kDefault, plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_05")
    @pytest.mark.full
    def test_batt_protect_default_planA_fail_transfor_planB_caseid_1989994(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kDefault, plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_06")
    @pytest.mark.full
    def test_batt_protect_default_planA_fail_transfor_planB_caseid_1989993(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kDefault, plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_07")
    @pytest.mark.full
    def test_batt_protect_default_planA_fail_transfor_planB_caseid_1989992(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kDefault, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_02")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989988(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_03")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989987(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_04")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989986(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_05")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989985(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_06")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989984(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_07")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989983(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_08")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989982(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_01")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989980(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_02")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989979(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_03")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989978(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_04")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989977(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_05")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989976(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_06")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989975(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_07")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989974(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kACDC执行A方案失败跳转执行B方案_08")
    @pytest.mark.full
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989973(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kACDC, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案_inactive")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989972(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown)

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_01")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989971(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_02")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989970(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.ConnectedWithoutPower)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_03")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989969(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.PowerAvailableButNotActivated)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_04")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989968(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.Init)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_05")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989967(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_06")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989966(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.Default)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_07")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989965(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Inhibited)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kUnknown执行A方案失败跳转执行B方案_08")
    @pytest.mark.full
    def test_batt_protect_unknown_planA_fail_transfor_planB_caseid_1989964(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kUnknown, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态Inhibited")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_inhibited_timeout_caseid_1989939(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        time.sleep(29.5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        self.soa.soa_partner.empty_all()
        self.soa.check_RemoteBatteryHeatingInfo(heatsts=RemoteBatteryHeatingSts.kError)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态Fault")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_fault_timeout_caseid_1989938(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        time.sleep(29.5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Fault)
        self.soa.soa_partner.empty_all()
        self.soa.check_RemoteBatteryHeatingInfo(heatsts=RemoteBatteryHeatingSts.kError)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断transport")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_transport_caseid_1989937(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断factory")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_factory_caseid_1989936(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断crash")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_crash_caseid_1989935(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断crash")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_dyno_caseid_1989934(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断active")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_active_caseid_1989932(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断driving")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_driving_caseid_1989931(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断soc17")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_soc17_caseid_1989930(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.notify_HVSOCInfo(displaySoc=17)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断isCharging=True")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_ischarging_true_caseid_1989929(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_ischarging_true_caseid_1989928(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.tsp.rvc_ac_control()
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_remote_seatheating_caseid_1989927(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.tsp.rvc_rearright_seat_heat()
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_remote_seatventing_caseid_1989926(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.tsp.rvc_rear_left_seat_vent()
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_remote_stwlheating_caseid_1989925(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.tsp.rvc_steering_wheel_heat()
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_remote_defrost_control_caseid_1989924(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.tsp.rvc_defrost_control()
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_remote_colddown_caseid_1989923(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.tsp.rvc_cold_down()
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)


    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_remote_heatup_caseid_1989922(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        self.tsp.rvc_heat_up()
        time.sleep(0.1)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=3)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_schedule_ac_caseid_1989921(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=1,driver_level=-1,passenger_level=-1,steering_level=-1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)


    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_schedule_seatheating_caseid_1989920(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_schedule_seatheating_caseid_1989919(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_schedule_stwlheating_caseid_1989918(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        time.sleep(5)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=5)

    @allure.title("RVC_低温自保护_执行B方案等待热管理状态打断_pluggerStatus=3")
    @pytest.mark.full
    def test_batt_protect_exect_planB_wait_thermalreqsts_interrupted_by_pluggerstatus_connectedwithpower_caseid_1989917(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planB_by_stage_wait_ThermalReqSts()
        time.sleep(5)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_transport")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_transport_caseid_1989914(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_factory")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_factory_caseid_1989913(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_crash")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_crash_caseid_1989912(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_dyno")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_dyno_caseid_1989911(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_active")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_active_caseid_1989909(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_driving")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_driving_caseid_1989908(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_soc17_caseid_1989907(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.notify_HVSOCInfo(displaySoc=17)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_isCharging=True")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_ischarging_true_caseid_1989906(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_remote_ac_caseid_1989905(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.tsp.rvc_ac_control()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_remote_seatheating_caseid_1989904(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.tsp.rvc_passenger_seat_heat()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_remote_seatventing_caseid_1989903(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.tsp.rvc_passenger_seat_vent()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_remote_seatventing_caseid_1989902(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.tsp.rvc_steering_wheel_heat()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_remote_defrost_control_caseid_1989901(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.tsp.rvc_defrost_control()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_remote_colddown_caseid_1989900(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.tsp.rvc_cold_down()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_remote_colddown_caseid_1989899(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        self.tsp.rvc_heat_up()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_schedule_ac_caseid_1989898(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=1,driver_level=-1,passenger_level=-1,steering_level=-1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_schedule_seatheating_caseid_1989897(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_schedule_seatventing_caseid_1989896(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行A方案_判断插直流枪后1s内打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_acdctype_interrupted_by_schedule_stwlheating_caseid_1989895(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_DC_by_stage_SetCharging()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_transport")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_transport_caseid_1989894(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_factory")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_factory_caseid_1989893(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_crash")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_crash_caseid_1989892(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_dyno")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_dyno_caseid_1989891(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_active")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_active_caseid_1989889(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_driving")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_driving_caseid_1989888(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_soc17_caseid_1989887(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_HVSOCInfo(displaySoc=17)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_isCharging=True")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_ischarging_true_caseid_1989886(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                 acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_remote_ac_caseid_1989885(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.tsp.rvc_ac_control()
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_remote_seatheating_caseid_1989884(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.tsp.rvc_rearleft_seat_heat()
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_remote_seatventing_caseid_1989883(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.tsp.rvc_rear_left_seat_vent()
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_remote_stwlheating_caseid_1989882(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.tsp.rvc_steering_wheel_heat()
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_remote_defrost_control_caseid_1989881(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.tsp.rvc_defrost_control()
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_remote_colddown_caseid_1989880(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.tsp.rvc_cold_down()
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_remote_colddown_caseid_1989879(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.tsp.rvc_heat_up()
        time.sleep(0.1)
        self.soa.check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating()

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远预约空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_schedule_ac_caseid_1989878(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=1,driver_level=-1,passenger_level=-1,steering_level=-1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远预约座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_schedule_ac_caseid_1989877(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)


    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远预约座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_schedule_seatheating_caseid_1989876(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus时打断_TSP下发远预约方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_exect_planA_wait_pluggerstatus_interrupted_by_schedule_stwlheating_caseid_1989875(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_transport")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_transport_caseid_1989874(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_factory")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_factory_caseid_1989873(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_craash")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_crash_caseid_1989872(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_dyno")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_dyno_caseid_1989871(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_active")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_active_caseid_1989869(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_driving")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_driving_caseid_1989868(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_soc17_caseid_1989867(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_isCharging=True")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_ischarging_true_caseid_1989866(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True, 
                                 acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_ac_caseid_1989865(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.tsp.rvc_ac_control()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_seatheating_caseid_1989864(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.tsp.rvc_rearright_seat_heat()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_seatventing_caseid_1989863(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.tsp.rvc_rear_right_seat_vent()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_stwlheating_caseid_1989862(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.tsp.rvc_steering_wheel_heat()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_defrost_control_caseid_1989861(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.tsp.rvc_defrost_control()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_cold_down_caseid_1989860(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.tsp.rvc_cold_down()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_remote_cold_down_caseid_1989859(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(9.9)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2.5)
        self.tsp.rvc_heat_up()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_ac_caseid_1989858(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(10)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=1,driver_level=-1,passenger_level=-1,steering_level=-1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_seatheating_caseid_1989857(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(10)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)
        
    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_seatventing_caseid_1989856(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(10)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待pluggerStatus失败后跳转执行B方案时打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_plugggerstatus_timeout_transfor_planB_interrupted_by_schedule_stwlheating_caseid_1989855(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        time.sleep(10)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        time.sleep(2)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_transport")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_transport_caseid_1989854(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_factory")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_factory_caseid_1989853(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_crash")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_crash_caseid_1989852(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_dyno")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_dyno_caseid_1989851(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_active")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_active_caseid_1989849(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_driving")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_driving_caseid_1989848(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_soc17_caseid_1989847(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_isCharging=True")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_ischarging_true_caseid_1989846(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(0.1)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=True, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_remote_ac_caseid_1989845(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_ac_control).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_remote_seatheating_caseid_1989844(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_driver_seat_heat).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)


    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_remote_seatventing_caseid_1989843(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_driver_seat_vent).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_remote_stwlheating_caseid_1989842(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_steering_wheel_heat).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_remote_defrost_control_caseid_1989841(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_defrost_control).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_remote_cold_down_caseid_1989840(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_cold_down).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_remote_heat_up_caseid_1989839(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_heat_up).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_schedule_ac_caseid_1989838(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_schedule_seatheating_caseid_1989837(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":1, "passenger_level":-1, "steering_level":-1}).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_schedule_seatventing_caseid_1989836(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":-1, "DriverVent_level":1}).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态时打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_interrupted_by_schedule_stwlheating_caseid_1989835(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.battery_protect_exect_planA_by_stage_wait_pluggerStatus()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        threading.Thread(target=self.tsp.rvc_taskCmd, kwargs={"appointment_minute":13, "driver_level":-1, "passenger_level":-1, "steering_level":1}).start()
        self.soa.soa_partner.empty_all()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_transport")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_transport_caseid_1989834(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_factory")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_factory_caseid_1989833(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_crash")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_crash_caseid_1989832(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_dyno")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_dyno_caseid_1989831(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_active")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_active_caseid_1989829(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_driving")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_driving_caseid_1989828(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_DisplaySOC=17%")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_soc17_caseid_1989827(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_remote_ac_caseid_1989825(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_ac_control()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_remote_seatheating_caseid_1989824(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_rearleft_seat_heat()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_remote_seatventing_caseid_1989823(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_rear_left_seat_vent()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_remote_stwlheating_caseid_1989822(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_steering_wheel_heat()
        time.sleep(0.1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控除霜指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_remote_defrost_control_caseid_1989821(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_defrost_control()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控极速制冷指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_remote_cold_down_caseid_1989820(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_cold_down()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发远控极速制热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_remote_cold_down_caseid_1989819(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        self.tsp.rvc_heat_up()
        time.sleep(0.1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约空调指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_schedule_ac_caseid_1989818(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=1,driver_level=-1,passenger_level=-1,steering_level=-1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约座椅加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_schedule_seatheating_caseid_1989817(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约座椅通风指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_schedule_seatventing_caseid_1989816(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_等待热管理状态失败跳转执行B方案时打断_TSP下发预约方向盘加热指令")
    @pytest.mark.full
    def test_batt_protect_dc_planA_wait_thermalreqsts_timeout_transfor_planB_interrupted_by_schedule_stwlheating_caseid_1989815(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(thermal_sts=ThermalReqSts.Inhibited)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14,ac=-1,driver_level=-1,passenger_level=-1,steering_level=1)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle, heatsts=RemoteBatteryHeatingSts.kOff,
                                              source=HeatingEnergySource.kNone, timeout=3)

    @allure.title("RVC_低温自保护_执行A方案_400v_CCP #566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planA_400v_ccp566_0x18_caseid_1989814(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)

    @allure.title("RVC_低温自保护_执行A方案_400v_CCP #566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planA_400v_ccp566_0x17_caseid_1989813(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-21.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-18.0, thermal_sts=ThermalReqSts.Heating)


    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x10")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x10_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x18_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值800V_CCP566=0x10")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_800v_ccp566_0x10_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值800V_CCP566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_800v_ccp566_0x18_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}, {"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x10_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x19")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x19_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值800V_CCP566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_800v_ccp566_0x17_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x19_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}, {"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行B方案_温度高于阈值400V_CCP566=0x10")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x10_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_kDC不执行B方案_温度高于阈值400V_CCP566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x18_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_kDC不执行B方案_温度高于阈值800V_CCP566=0x10")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_800v_ccp566_0x10_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetBatteryHeating_req(timeout=3)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetCharging_req(timeout=10)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值800V_CCP566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_800v_ccp566_0x18_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x18}, {"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)


    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x10_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x19")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x19_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值800V_CCP566=0x17")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_800v_ccp566_0x17_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x02}, {"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)

    @allure.title("RVC_低温自保护_kDC不执行A方案_温度高于阈值400V_CCP566=0x18")
    @pytest.mark.full
    def test_batt_protect_dc_not_exect_planA_400v_ccp566_0x19_caseid_01(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x19}, {"name": 962, "value": 0x02}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.soa_partner.empty_all()
        self.soa.check_no_SetOutput_req(timeout=6)
        
        


    @allure.title("RVC_低温自保护_Heating_on_quitforminTemperature=-27.9℃")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_caseid_1981798(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=27.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_Heating_on_quitforminTemperature=-17.9℃")
    @pytest.mark.smoke
    def test_batt_protect_caseid_1981797(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 566, "value": 0x17}, {"name": 962, "value": 0x0}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=5)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.notify_BatteryTemperatureInfo(min_temp=17.9)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_低温自保护_Heating_on_quitforDisplaySOC=17%_01")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_caseid_1981800(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_低温自保护_Heating_on_quitforDisplaySOC=17%_02")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_caseid_1981799(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.notify_HVSOCInfo(displaySoc=17)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_noneedheating_0x10")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_caseid_1981911(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_TRANSPORT_01")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981814(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_TRANSPORT_02")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981813(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_低温自保护_远程电池加热未运行")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1989800(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)


    @allure.title("RVC_低温自保护加热中退出_TSP下发远控电池包立即加热")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1990009(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.tsp.rvc_realtime_battery_heat()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanB_05")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x10_caseid_1981761(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.battery_protect_exect_planb()


    @allure.title("RVC_低温自保护_Heating_planB_on_quitfor_pluggerStatus=3_02")
    @pytest.mark.santiy
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x10_caseid_1981769(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        time.sleep(5)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("RVC_低温自保护_V2.0_LowTempProtect_0x19(800v)_needheating_planA")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1987625(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x19}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        time.sleep(9.5)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        # time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)


    @allure.title("RVC_低温自保护_V2.0_LowTempProtect_0x19(800v)_needheating_planB")
    @pytest.mark.santiy
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x19_caseid_1987626(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x19}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)



    @allure.title("Heating_on_quitforNotifyUsageMode_convenience_01")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981806(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("Heating_on_quitforNotifyUsageMode_convenience_02")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981805(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("Heating_abandon_wakeup_success_needheating_executePlanB_04")
    @pytest.mark.santiy
    def test_batt_protect_dc_execting_planB_800v_ccp566_0x17_caseid_1981762(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)


    @allure.title("RVC_低温自保护_Heating_on_quitfor远程开启空调_01")
    @pytest.mark.santiy
    def test_batt_protect_execting_planB_caseid_1981792(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()
        self.tsp.rvc_ac_control() 
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
    @allure.title("Heating_on_quitfor远程开启空调_02")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981791(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.tsp.rvc_ac_control() 
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控预约开启空调_01")
    @pytest.mark.santiy
    def test_batt_protect_execting_planB_caseid_1981782(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
    @allure.title("Heating_on_quitfor_远控预约开启空调_02")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981781(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("Heating_executePlanB_执行过程中打断_01")
    @pytest.mark.santiy
    def test_batt_protect_execting_planB_caseid_1981759(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.check_SetOutput_req(timeout=5)
        time.sleep(1)
        self.soa.notify_hvActiveSts()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28, timeout=5)  
        time.sleep(5)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_planB_on_quitfor_pluggerStatus=3_01")
    @pytest.mark.santiy
    def test_batt_protect_execting_planB_caseid_1981770(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_HeatFinished_over 5s_01")
    @pytest.mark.santiy
    def test_batt_protect_execting_planB_caseid_1985730(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatFinished)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_HeatFinished_over 5s_02")
    @pytest.mark.santiy
    def test_batt_protect_execting_planB_caseid_1985729(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatFinished)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=5)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
        
        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_04")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981844(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)



    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanB_06")
    @pytest.mark.santiy
    def test_batt_protect_dc_execting_planB__caseid_1981760(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[7])
        self.soa.battery_protect_exect_planb(value=-18)
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_convenience_01")
    @pytest.mark.santiy
    def test_batt_protect_dc_execting_planB__caseid_1981887(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)    
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_convenience_02")
    @pytest.mark.santiy
    def test_batt_protect_dc_execting_planB__caseid_1981886(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)    
        

    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_DisplaySOC=19%_02")
    @pytest.mark.full
    def test_batt_protect_dc_execting_planB__caseid_1981868(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_HVSOCInfo(displaySoc=19)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_DisplaySOC=19%_01")
    @pytest.mark.santiy
    def test_batt_protect_dc_execting_planB__caseid_1981869(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_HVSOCInfo(displaySoc=19)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_FOTAstatus_Rollback_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981870(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_FOTAstatus_Rollback_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981871(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_FOTAstatus_Update_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981872(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)      
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_FOTAstatus_Update_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981873(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_GearD_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981874(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)    
        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_GearD_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981875(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  



    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_GearR_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981876(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_GearR_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981877(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_GearN_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981878(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_GearN_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981879(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
         
         
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_MntnMode_ture_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981880(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_MntnMode_ture_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981881(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
         
         
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_driving_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981882(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
         
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_driving_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981883(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)      
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_active_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981884(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)   


    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_active_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981885(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)   
        
        

    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_DYNO_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981888(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)   
        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_DYNO_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981889(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        
        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_CRASH_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981890(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)   
        
          
          
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_CRASH_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981891(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)   
        
        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_ FACTORY_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981892(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        
        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_ FACTORY_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981893(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)   
           
           
           
           
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_ TRANSPORT_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981894(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        
        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_Precondition_mismatch_ TRANSPORT_01")
    @pytest.mark.sanity
    def test_batt_protect_caseid_1981895(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 



    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_座椅加热通风工作中_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1987415(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=60)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SeatHeatVentStatus(heat_level=HeatLevel.High)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)   
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_座椅加热通风工作中_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1987416(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SeatHeatVentStatus(heat_level=HeatLevel.High)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        self.soa.soa_partner.empty_all()   
           
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_方向盘加热=low_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1987417(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        self.soa.soa_partner.empty_all()     


    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_方向盘加热=low_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1987419(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        self.soa.soa_partner.empty_all()  
        

    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_方向盘加热=Mid_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1987420(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        self.soa.soa_partner.empty_all()
        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_方向盘加热=Mid_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1987421(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Mid)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        self.soa.soa_partner.empty_all()  
        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_方向盘加热=High_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1987422(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        self.soa.soa_partner.empty_all()
        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_方向盘加热=High_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1987423(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        self.soa.soa_partner.empty_all() 
        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_空调状态处于工作中_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1987424(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        self.soa.soa_partner.empty_all() 
        
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_空调状态处于工作中_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1987425(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        self.soa.soa_partner.empty_all()
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_除霜状态处于工作中_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1987426(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=60)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_NotifyACDefrostSts(climate_defrost=True)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)  
        self.soa.soa_partner.empty_all()
        
        
    @allure.title("RVC_低温自保护_Heating_Precondition_mismatch_除霜状态处于工作中_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1987427(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=60)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_NotifyACDefrostSts(climate_defrost=True)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 
        self.soa.soa_partner.empty_all() 
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforNotifyUsageMode_driving_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981801(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforNotifyUsageMode_driving_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981802(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforNotifyUsageMode_active_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981803(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforNotifyUsageMode_active_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981804(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_ DYNO_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981807(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_ DYNO_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981808(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_CRASH_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981809(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_CRASH_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981810(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_FACTORY_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981811(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitforCarMode_FACTORY_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981812(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_Fault_over 5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985715(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Fault)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_Fault_over 5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985716(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Fault)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_HeatingByEmotCoolt_over 5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985717(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatingByEmotCoolt)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_HeatingByEmotCoolt_over 5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985718(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.HeatingByEmotCoolt)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_Inhibited_over 5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985719(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_Inhibited_over 5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985720(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Inhibited)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_ CoolingFinish_over 5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985721(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CoolingFinish)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_ CoolingFinish_over 5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985722(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CoolingFinish)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_ CompressorCooling_over 5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985723(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CompressorCooling)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_ CompressorCooling_over 5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985724(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.CompressorCooling)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_RadiatorCooling_over 5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985725(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.RadiatorCooling)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_RadiatorCooling_over 5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985726(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.RadiatorCooling)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_Default_over 5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985727(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_ThermalReqSts_Default_over 5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985728(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default)
        time.sleep(11)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kError,
                                                 source=HeatingEnergySource.kHVBattery, timeout=3)   
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控电池预加热_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981773(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控电池预加热_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981774(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)


    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控预约开启方向盘加热_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981775(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控预约开启方向盘加热_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981776(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控预约开启副驾座椅加热_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981777(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控预约开启副驾座椅加热_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981778(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控预约开启主驾座椅加热_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981779(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
 
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor_远控预约开启主驾座椅加热_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981780(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd(appointment_minute=14)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远控开启前挡最大除霜_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981783(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.tsp.rvc_defrost_control(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远控开启前挡最大除霜_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981784(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.tsp.rvc_defrost_control(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远控开启方向盘加热_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981785(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.tsp.rvc_steering_wheel_heat(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远控开启方向盘加热_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981786(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.tsp.rvc_steering_wheel_heat(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远程开启副驾座椅加热_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981787(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.tsp.rvc_passenger_seat_heat(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远程开启副驾座椅加热_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981788(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.tsp.rvc_passenger_seat_heat(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远程开启主驾座椅加热_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981789(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.tsp.rvc_driver_seat_heat(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远程开启主驾座椅加热_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981790(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.tsp.rvc_driver_seat_heat(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
   
   
    @allure.title("RVC_低温自保护_Heating_on_quitfor远程开启座椅通风_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1987081(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.tsp.rvc_driver_seat_vent(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
        
        
    @allure.title("RVC_低温自保护_Heating_on_quitfor远程开启座椅通风_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1987080(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-28)
        self.tsp.rvc_driver_seat_vent(1)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)
   
        



#新增

    # @allure.title("RVC_低温自保护_远程电池加热开启中")
    # @pytest.mark.sanity
    # def test_realtime_caseid_1989799(self, ecu):
    #     self.soa.soa_partner.empty_all()
    #     self.soa.notify_NotifyConfigList()
    #     wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
    #     logger.info("等待时间： {0}".format(wait_time))
    #     self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
    #     self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
    #     time.sleep(100) 
    #     time.sleep(1)
    #     with allure.step("下发远控电池包立即加热指令"): 
    #         execid = self.tsp.rvc_realtime_battery_heat()
    #     self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
    #     self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
    #     self.soa.notify_ThermalSystemDeviceFaultInfo()
    #     self.soa.notify_BatteryTemperatureInfo(min_temp = 17)
    #     self.soa.check_SetOutput_req(timeout=25)  # 监听TCAM发送上高压请求
    #     self.soa.notify_hvActiveSts()
    #     self.soa.check_SetBatteryHeating_exit_req(on=True,value=20,timeout=5)  # 监听TCAM发送电池加热请求
    #     time.sleep(15)
    #     self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 




    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_03")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1981846(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)



    @allure.title("RVC_低温自保护_V2.0_LowTempProtect_0x18(800v)_needheating_planA")
    @pytest.mark.sanity
    def test_batt_protect_dc_execting_planA_caseid_1987627(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        


    @allure.title("RVC_低温自保护_kACDC执行A方案_inactive")
    @pytest.mark.sanity
    def test_batt_protect_acdc_execting_planA_caseid_1989981(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kACDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kACDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)



    @allure.title("Heating_abandon_wakeup_success_needheating_executePlanB_03")
    @pytest.mark.sanity
    def test_batt_protect_execting_planB_caseid_1981763(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_noneedheating_0x17")
    @pytest.mark.full
    def test_batt_protect_caseid_1981910(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_UpdateFailedNotDriving(7)")
    @pytest.mark.full
    def test_batt_protect_caseid_1981839(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)

        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_ Active(4)")
    @pytest.mark.full
    def test_batt_protect_caseid_1981840(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)
        

    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_Downloading(3)")
    @pytest.mark.full
    def test_batt_protect_caseid_1981841(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)


    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_NEWTASK(2)")
    @pytest.mark.full
    def test_batt_protect_caseid_1981842(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)
        

    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_QUERY(1)")
    @pytest.mark.full
    def test_batt_protect_caseid_1981843(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(min_temp=-31.0, acdc_type=ACDCType.kDC, 
                                            plug_sts1=PluggerSts.Disconnected, 
                                            plug_sts2=PluggerSts.ConnectedWithPower,
                                            value=-28.0, thermal_sts=ThermalReqSts.Heating)

   
        
    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanB_01")
    @pytest.mark.smoke
    def test_batt_protect_execting_planB_caseid_1981768(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()


    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanB_02")
    @pytest.mark.smoke
    def test_batt_protect_execting_planB_caseid_1981764(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)



    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_02")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_caseid_1981847(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=60)


    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_success_needheating_executePlanA_01")
    @pytest.mark.smoke
    def test_batt_protect_dc_execting_planA_caseid_1981849(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=60)

    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_fail_0x10")
    @pytest.mark.full
    def test_batt_protect_caseid_1981909(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)


    @allure.title("Heating_abandon_wakeup_fail_0x17")
    @pytest.mark.full
    def test_batt_protect_caseid_1981908(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ABANDONED)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)

    @allure.title("RVC_低温自保护_Heating_Precondition_优先级判断_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981862(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)


    @allure.title("RVC_低温自保护_Heating_Precondition_优先级判断_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981863(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)

    @allure.title("Heating_abandon_wakeup_fail_DisplaySOC=19%_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981899(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_HVSOCInfo(displaySoc=19)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)


    @allure.title("Heating_abandon_wakeup_fail_DisplaySOC=19%_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981898(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_HVSOCInfo(displaySoc=19)
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)



    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_minTemperature=0x7FFFFFFF(默认值)_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1981897(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=0x7FFFFFFF)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)


    @allure.title("RVC_低温自保护_V2.0_LowTempProtect_0x19(800v)_noneedheating")
    @pytest.mark.full
    def test_batt_protect_caseid_1987623(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x19}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-20)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)



    @allure.title("Heating_on_ThermalReqSts_Default_notover5s_01")
    @pytest.mark.full
    def test_batt_protect_caseid_1985714(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb()
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default) 
        time.sleep(9)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating) 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=60)


    @allure.title("RVC_低温自保护_V2.0_LowTempProtect_0x18(800v)_noneedheating")
    @pytest.mark.full
    def test_batt_protect_caseid_1987624(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-30)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)


    @allure.title("Heating_on_ThermalReqSts_Default_notover5s_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1985713(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21.0)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[3])
        self.soa.battery_protect_exect_planb(value=-18)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Default) 
        time.sleep(9)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating) 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=60)



    @allure.title("RVC_低温自保护_Heating_abandon_wakeup_minTemperature=0x7FFFFFFF(默认值)_02")
    @pytest.mark.full
    def test_batt_protect_caseid_1981896(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=0x7FFFFFFF)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=60)


    @allure.title("RVC_低温自保护_远程电池预加热工作中")
    @pytest.mark.full
    def test_batt_protect_caseid_1989798(self, ecu):
        appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd()
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
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        time.sleep(wait_time-1)
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=5)


    @allure.title("RVC_低温自保护_kDefault执行A方案失败跳转执行B方案_08")
    @pytest.mark.sanity
    def test_batt_protect_default_planA_fail_transfor_planB_caseid_1989991(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kDefault, plug_sts2=PluggerSts.ConnectedWithPower, thermal_sts=ThermalReqSts.Fault)
        self.soa.battery_protect_exect_planb()

    @allure.title("RVC_低温自保护_kAC执行A方案失败跳转执行B方案_01")
    @pytest.mark.sanity
    def test_batt_protect_ac_planA_fail_transfor_planB_caseid_1989989(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.battery_protect_exect_plana(acdc_type=ACDCType.kAC, plug_sts2=PluggerSts.Disconnected)
        self.soa.battery_protect_exect_planb()


    @allure.title("RVC_低温自保护_Heating_on_quitfor_Countdown ends_01")
    @pytest.mark.sanity
    def test_batt_protect_quitfor_Countdownends_caseid_1981772(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kAC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=5)
        time.sleep(1)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kAC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(40*60)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 


    @allure.title("RVC_低温自保护_Heating_on_quitfor_Countdown ends_02")
    @pytest.mark.sanity
    def test_batt_protect_quitfor_Countdownends_caseid_1981771(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x0},{"name": 566, "value": 0x17}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-21)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kAC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-18.0, timeout=5)
        time.sleep(1)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kAC, plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(5)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        time.sleep(40*60)
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=3)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=3)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 


    @allure.title("RVC_低温自保护_V2.0_LowTempProtect_0x18(800v)_needheating_planB")
    @pytest.mark.sanity
    def test_batt_protect_caseid_1987628(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList([{"name": 962, "value": 0x2},{"name": 566, "value": 0x18}])
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation(equipment_types=[4])
        self.soa.battery_protect_exect_planb()


    @allure.title("RVC_低温自保护_远程电池立即加热工作中")
    @pytest.mark.sanity
    def test_batt_protect_caseid_1989797(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=False, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        time.sleep(5)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)   
        time.sleep(1)
        with allure.step("下发远控电池包立即加热指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_NotifyRemoteBatteryHeatingInfo_event(heatSts=RemoteBatteryHeatingSts.kReady,modeSts=RemoteBatteryHeatingModeSts.kRealTimeHeat,source=HeatingEnergySource.kNone,timeout=30)
        time.sleep(9.5)
        self.soa.notify_HVSOCInfo(displaySoc=10.0)
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
        self.soa.soa_partner.empty_all()
        self.soa.check_no_RemoteBatteryHeatingInfo(timeout=120)

    @allure.title("RVC_低温自保护_加热中退出_通知预约交流充电的激活任务 ")
    @pytest.mark.full
    def test_batt_protect_caseid_1991096(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        time.sleep(wait_time-1)
        self.soa.notify_BatteryTemperatureInfo(min_temp=-31)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True, 
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.Disconnected)
        self.soa.notify_NotifyChargingEquipmentInformation()
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, value=-28.0, timeout=3)
        self.soa.check_SetCharging_req(req=True, timeout=10)
        time.sleep(2)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False, isConnect=True,
                                     acdc_type=ACDCType.kDC, plug_sts=PluggerSts.ConnectedWithPower)
        self.soa.notify_BatteryHeatingInfo(req_sts=ThermalReqSts.Heating)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                                 heatsts=RemoteBatteryHeatingSts.kOn,
                                                 source=HeatingEnergySource.kCharger, timeout=3)
        self.soa.notify_BookChargingInfo(workSts=ACBookChargingWorkSts.kBookStsStandby)
        self.soa.send_SetBookEvent_req(ser_name=" ac_book_charging",book_type="book charging start time",sch_time=120) 
        self.soa.check_SetBatteryHeating_req(req_type=ThermalRequestType.kBookHeating, on=False, value=-40.0, timeout=130)
        self.soa.check_RemoteBatteryHeatingInfo(modests=RemoteBatteryHeatingModeSts.kIdle,
                                                 heatsts=RemoteBatteryHeatingSts.kOff,
                                                 source=HeatingEnergySource.kNone, timeout=5)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120)

    @allure.title("RVC_低温自保护_前置条件_10min内有预约交流充电的激活任务")
    @pytest.mark.full
    def test_batt_protect_caseid_1991097(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_BookChargingInfo(workSts=ACBookChargingWorkSts.kBookStsStandby,startTime=int(time.time()+9*60))
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 


    @allure.title("RVC_低温自保护_前置条件_充电桩在 (充电、预加热）输出")
    @pytest.mark.full
    def test_batt_protect_caseid_1991098(self, ecu):
        self.soa.soa_partner.empty_all()
        self.soa.notify_NotifyConfigList()
        wait_time=self.soa.send_SetBookEvent_req(sch_time=120)  # 设置RTC预约2分钟后低温自保护任务
        logger.info("等待时间： {0}".format(wait_time))
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default, is_charging=False,plug_sts=PluggerSts.ConnectedWithPower)
        time.sleep(wait_time-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=120) 

