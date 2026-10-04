#!/usr/bin/env python
# -*- coding: utf-8 -*-


from copy import deepcopy
import os
import sys
import time
from threading import *
import pytest
import allure
import json

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.config_data import *


@allure.feature("互联服务/远程控制/远控座舱控制")
@allure.story("远控参数配置")
class TestRvcParamConfig(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "CentralLockService_server", "InteractiveService_server",
                         "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server",
                         "ConfigMasterService_server", "ShieldWindowService_server", "OuterRearViewService_server"])
        sleep(8)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_ClimateFault()
        self.soa.notify_RemotePowerStatus(RemoteClimateStatus.Off)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = False)
        self.soa.notify_RemoteClimateHVStatus(RemoteClimateStatus.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_RearRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off,vent_work_sts=HeatVentWorkStatus.Off)
        self.soa.notify_SteerHeatAvailiable(availiable=SteerHeatAvailiable.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Off)
        self.soa.notify_NotifyACDefrostSts(defrost_max = False,climate_defrost = False)
        self.soa.notify_ShieldWindowService_HeatStatus(heat_status=HeatStatus.HeatStatusOff)
        self.soa.notify_OuterRearViewService_HeatStatus(status= False)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Open)
        self.soa.notify_ViewFault([0,"1",2])
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusNa, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusNa, validity_right=ValidityLevel.kValid)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.rvc_data = deepcopy(rvc_config_data)
        sleep(15)

    def after_each_func(self, ecu):
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(rvc_config_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)

    def after_class(self, ecu):
        pass


    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemClimaHvTimeout")
    def test_caseid_1985683(self):
        self.rvc_data[0]["value"][4]["value"] = 5
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        sleep(6)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="RemClimaHvStrtFail")
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemClimaCtrlTimeout")
    def test_caseid_1985682(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.rvc_data[0]["value"][5]["value"] = 5
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetTemperatureAndOn_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22, timeout=20)
        sleep(6)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemClimaRunTime")
    def test_caseid_1985681(self):
        self.rvc_data[0]["value"][6]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetRemoteClimateSwitchToHV_req(keep_time=1, timeout=20)
        self.soa.check_RemoteOn_req_and_feedback_resp(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req_and_feedback_resp(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid)
        self.soa.check_RemoteOff_req(timeout=70)
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemSeatHeatTimeout")
    def test_caseid_1985680(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.rvc_data[0]["value"][7]["value"] = 5
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_driver_seat_heat(level=3)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        sleep(6)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemSeatHeatRunTime")
    def test_caseid_1985679(self):
        self.rvc_data[0]["value"][8]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_driver_seat_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(keep_time=1, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20) 
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20) 
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=HeatLevel.Off, timeout=70)
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemSteerWhlHeatTimeout")
    def test_caseid_1985678(self):
        self.rvc_data[0]["value"][9]["value"] = 5
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(isOn=True, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        sleep(6)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemSteerWhlHeatRunTime")
    def test_caseid_1985677(self):
        self.rvc_data[0]["value"][10]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_steering_wheel_heat(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(keep_time=1,timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.High, timeout=20)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=70)
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemFrontDefrostTimeout")
    def test_caseid_1985676(self):
        self.rvc_data[0]["value"][14]["value"] = 5
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        sleep(6)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemFrontDefrostRunTime")
    def test_caseid_1985675(self):
        self.rvc_data[0]["value"][11]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(keep_time=1, timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=False, timeout=75)
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemSeatVentTimeout")
    def test_caseid_1985686(self):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.rvc_data[0]["value"][15]["value"] = 5
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        sleep(6)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemSeatVentRunTime")
    def test_caseid_1985685(self):
        self.rvc_data[0]["value"][16]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_driver_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(keep_time=1, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20)
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.High, timeout=20) 
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=70)

    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemMaxCoolingRunTime")
    def test_caseid_1988774(self):
        self.rvc_data[0]["value"][17]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_cold_down(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True, keep_time=1, timeout=20)
        time_start = time.time()
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        sleep(2.5)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = True,timeout=20)
        logger.info("执行时间：{}s".format(time.time() - time_start))
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=True, maxHeatingSts = False)
        with allure.step('校验极速制冷执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SetMaxCoolingCtrl_req(onOffCmd = False,timeout=70)

    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemMaxHeatingRunTime")
    def test_caseid_1988775(self):
        self.rvc_data[0]["value"][18]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_heat_up(1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        time_start = time.time()
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn = True, keep_time=1, timeout=20)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = True,timeout=20)
        self.soa.notify_MaxCoolingHeatingInfo(maxCoolingSts=False, maxHeatingSts = True)
        with allure.step('校验极速制热执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        self.soa.check_SetMaxHeatingCtrl_req(onOffCmd = False,timeout=70)

    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemOutRearViewFoldTimeout")
    def test_caseid_1985684(self):
        self.rvc_data[1]["value"][8]["value"] = 5
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_rear_view_control(op=-1)
        self.soa.check_Fold_req_and_feedback_resp(id=ViewId.RearViewAll, result=0, is_auto_unfold=True, timeout=20)
        sleep(6)
        self.soa.notify_OuterRearViewFoldStatus(value_left=ViewFoldStatus.StatusFolded, validity_left=ValidityLevel.kValid,\
                                                 value_right=ViewFoldStatus.StatusFolded, validity_right=ValidityLevel.kValid)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="DelayFail")

    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemCockpitReserveRunTime")
    def test_caseid_1985674(self):
        self.rvc_data[1]["value"][1]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        self.tsp.rvc_taskCmd(appointment_minute=15, driver_level=-1, passenger_level=-1, DriverVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(keep_time=1, timeout=20)
        self.soa.remote_climate_check_tcam_request(temp=23, timeout=20)
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=1, timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Low,timeout=20)
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_work_sts=HeatVentWorkStatus.On)
        sleep(25)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        self.mix.chk_rvc_threads(target=self.soa.ck_s2s_req, args=[("ClimateControlService_server", "RemoteOff", None, 60), 
                                                                   ("SteerWheelService_server", "SetHeat", {"status": 0, "source": 2}, 60),
                                                                   ("SeatService_server", "SetVentingLevel", {"params": [{"id": 0, "uint8Info": 0}], "source": 2}, 60)])
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemCockpitReserveStartTime")
    def test_caseid_1985673(self):
        self.rvc_data[1]["value"][2]["value"] = 20
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        self.tsp.rvc_taskCmd(appointment_minute=20, driver_level=-1, passenger_level=-1, steering_level=-1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
        self.soa.remote_climate_check_tcam_request(temp=23, timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.remote_climate_check_tcam_request(temp=23, timeout=20)
        self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
        sleep(25)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemElecDefrostRunTime")
    def test_caseid_1989542(self):
        self.rvc_data[0]["value"][12]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True,climate_defrost = True)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.soa.check_SetOutput_req(timeout=20)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Close)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.notify_RearShieldWindowHeatStatus()
        self.soa.notify_OuterRearViewHeatStatus()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOff,timeout=120)
    
    @pytest.mark.join_full
    @allure.title("RVC_远控参数配置_RemElecDefrostHvRunTime")
    def test_caseid_1989543(self):
        self.rvc_data[0]["value"][13]["value"] = 1
        self.soa.send_config_data_and_feedback_result(config_data=json.dumps(self.rvc_data), app_name="rvc", publish_id=int(time.time()))
        sleep(1)
        start_time=time.time()
        execid = self.tsp.rvc_defrost_control(1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(timeout=20)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        sleep(2)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetFastDefrostMode_req(on=True, timeout=20)
        self.soa.notify_NotifyACDefrostSts(defrost_max = True, climate_defrost = True)
        self.soa.check_GetOuterRearViewHeatStatus_req_and_feedback_resp(heat_work_sts = HeatWorkSts.HeatOn, heat_sts = HeatSts.Off,timeout=20)
        self.soa.check_ShieldWindowService_GetHeat_req_and_feedback_resp(status=HeatStatus.HeatStatusOff)
        self.soa.check_GethvActiveSts_req_and_feedback_resp(hv_act_sts=HVActiveSts.Close,timeout=20)
        self.soa.check_SetOutput_req(timeout=20)
        self.soa.notify_hvActiveSts(sts=HVActiveSts.Close)
        self.soa.check_ShieldWindowService_SetHeat_req(id=ShieldWindowId.ShieldWindowRear,heat_status=HeatStatus.HeatStatusOn,timeout=20)
        self.soa.notify_RearShieldWindowHeatStatus()
        self.soa.notify_OuterRearViewHeatStatus()
        assert self.tsp.log_search_remote_vehicle_control(execid=execid)
        self.mix.ck_rvc_DefrostHvRunTime(start_time=start_time, ck_time=57)
    
        
        
        
        
             