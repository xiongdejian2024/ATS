#!/usr/bin/env python
# -*- coding: utf-8 -*-


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


@allure.feature("互联服务/远程控制/远控座舱预约")
@allure.story("远控座舱通风预约")
class TestVentReserv(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server", "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server", "RtcAlarmService_client",
                         "ClimateControlService_server", "CentralLockService_server", "InteractiveService_server",
                         "VehicleTimeService_server", "SteerWheelService_server", "SeatService_server"]) 
        sleep(10)
        self.bus_comm.send_ccp_to_tcam(ccp_byte_index=189,ccp_value=0x02) # 设置整车CCP支持远控二排座椅通风
    
    def before_each_func(self, ecu):
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.INACTIVE)
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
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        sleep(20)

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    
    @pytest.mark.smoke
    @allure.title("RVC_预约座椅通风_inactive")
    def test_caseid_1987702(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, driver_level=-1,passenger_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            sleep(2)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(timeout=20)
            self.soa.check_RemoteOn_req(timeout=20)
            self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight,timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft,timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight,timeout=20)
            self.soa.notify_RemotePowerStatus(RemoteClimateStatus.On)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            self.soa.notify_RearRightSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            self.soa.notify_RearLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_inactive30自动关闭")
    def test_caseid_1987701(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, driver_level=-1,passenger_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            sleep(2)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(timeout=20)
            self.soa.check_RemoteOn_req(timeout=20)
            self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight,timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft,timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight,timeout=20)
            self.soa.notify_RemotePowerStatus(sts=RemoteClimateStatus.On)
            self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            self.soa.notify_RearRightSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            self.soa.notify_RearLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            time_start = time.time()
            sleep(25)
            result = self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result)
            self.mix.chk_rvc_vent_reserv_threads(ids=[1,6,4,0])
            assert time.time() - time_start > 1700     
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_convience主驾座椅占座")
    def test_caseid_1987700(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,0,0,0,0])
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_convience副驾座椅占座")
    def test_caseid_1987699(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[0,1,0,0,0])
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=17, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail")

    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_active")
    def test_caseid_1987698(self):
        self.soa.s2s_set_usage_mode(UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.ACTIVE)
        sleep(1)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail")
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_driving")
    def test_caseid_1987697(self):
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.DRIVING)
        sleep(1)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
            sleep(25)
            result = self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="UsageModeFail")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result, expected_msg="UsageModeFail", success=False)
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约主驾座椅通风打断远控主驾座椅通风")
    def test_caseid_1987696(self):
        execid = self.tsp.rvc_driver_seat_vent(level=1)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=1800)
            assert time.time() - time_start > 1700 
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约主驾座椅加热打断远控座椅加热")
    def test_caseid_1987695(self):
        execid = self.tsp.rvc_driver_seat_heat(level=1)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontLeft, heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_heat"])
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=1800)
            assert time.time() - time_start > 1700 
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约副驾座椅加热打断远控座椅加热")
    def test_caseid_1987694(self):
        execid = self.tsp.rvc_passenger_seat_heat(level=1)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontRight, heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=1,steering_level=-1)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["passenger_seat_heat"])
            self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=1800)
            assert time.time() - time_start > 1700 
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约副驾座椅通风打断远控副驾座椅通风")
    def test_caseid_1987693(self):
        execid = self.tsp.rvc_passenger_seat_vent(level=1)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontRight, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,PassengerVent_level=1)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["passenger_seat_vent"])
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.Off, timeout=1800)
            assert time.time() - time_start > 1700 
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约方向盘加热打断远控方向盘加热")
    def test_caseid_1987692(self):
        execid = self.tsp.rvc_steering_wheel_heat(level=1)
        self.soa.rvc_steer_wheel_heating_success(heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约远控方向盘加热"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["steering_wheel_heat"])
            self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=1800)
            assert time.time() - time_start > 1700 

    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约空调打断远控空调")
    def test_caseid_1987691(self):
        execid = self.tsp.rvc_ac_control(1,220)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True,timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status = RemoteClimateStatus.On)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=22,timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        with allure.step('校验远控空调执行结果'):         
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=1,driver_level=-1,passenger_level=-1,steering_level=-1)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(extendtime=30, timeout=20)
            self.soa.check_RemoteOn_req(timeout=20)
            self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
            time_start=time.time()
            sleep(25)
            assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.soa.check_RemoteOff_req(timeout=1830)
            assert time.time() - time_start > 1770

    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约左后座椅通风打断远控左后座椅通风")
    def test_caseid_1987690(self):
        execid = self.tsp.rvc_rear_left_seat_vent(level=1)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearLeft, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,PassengerVent_level=-1,RearLeftVent_level=1,RearRightVent_level=-1)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["rear_left_seat_vent"])
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Off, timeout=1800)
            assert time.time() - time_start > 1700 

    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约右后座椅通风打断远控右后座椅通风")
    def test_caseid_1987689(self):
        execid = self.tsp.rvc_rear_right_seat_vent(level=1)
        self.soa.rvc_seat_venting_start_success(id=SeatId.RearRight, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=1)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["rear_right_seat_vent"])
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=1800)
            assert time.time() - time_start > 1700 

    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_预约座椅通风换挡打断远控座椅通风")
    def test_caseid_1987688(self):
        execid1 = self.tsp.rvc_driver_seat_vent(level=3)
        execid2 = self.tsp.rvc_passenger_seat_vent(level=3)
        execid3 = self.tsp.rvc_rear_left_seat_vent(level=3)
        execid4 = self.tsp.rvc_rear_right_seat_vent(level=3)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=HeatLevel.High, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=HeatLevel.High, timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.High)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid1, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid2, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid3, keywords="Success")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid4, keywords="Success")
        sleep(60)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Low, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
            self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.Off, heat_level=HeatLevel.Off, vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
            self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
            self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            # self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["rear_right_seat_vent", "rear_left_seat_vent", "driver_seat_vent", "passenger_seat_vent"])
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=1800)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Off, timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
            assert time.time() - time_start > 1700 

    @pytest.mark.smoke
    @allure.title("RVC_预约座椅通风_预约座椅通风执行中远控座椅加热")
    def test_caseid_1987687(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
        sleep(2)
        execid =self.tsp.rvc_driver_seat_heat(level=1)
        self.soa.rvc_seat_venting_start_success(id=SeatId.FrontLeft, vent_level=VentLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SeatVentOn")
        sleep(20)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
    
    @pytest.mark.smoke
    @allure.title("RVC_预约座椅通风_预约座椅加热执行中远控座椅通风")
    def test_caseid_1987686(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=1,passenger_level=-1,steering_level=-1)
        sleep(2)
        execid = self.tsp.rvc_driver_seat_vent(level=1)
        self.soa.rvc_seat_heating_start_success(id=SeatId.FrontLeft, heat_level=HeatLevel.Low)
        assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="SeatHeatOn")
        sleep(20)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_heat"])

    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_预约座椅通风执行中触发预约座椅通风")
    def test_caseid_1987685(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
        sleep(2)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
        sleep(20)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="SysBusy")
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_预约座椅通风执行中触发预约空调")
    def test_caseid_1987684(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1, driver_level=-1, passenger_level=-1, steering_level=-1, DriverVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
        sleep(2)
        self.tsp.rvc_taskCmd(appointment_minute=15, driver_level=-1, passenger_level=-1, steering_level=-1)
        sleep(20)
        # assert self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="SysBusy")
        
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_inactive下座椅占座预约")
    def test_caseid_1987683(self):
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
        assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId")
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_预约全部功能")
    def test_caseid_1987682(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=1,driver_level=1,passenger_level=1,steering_level=1,DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        # self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["ac_control", "rear_right_seat_vent", "rear_left_seat_vent"])
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_预约全部功能30min自动关闭")
    def test_caseid_1987681(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=1,driver_level=1,passenger_level=1,steering_level=1,DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        time_start = time.time()
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        # self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["ac_control", "rear_right_seat_vent", "rear_left_seat_vent"])
        self.soa.check_RemoteOff_req(timeout=1830)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Off, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Off, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Off, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Off, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Off, timeout=20)
        assert time.time() - time_start > 1700 

    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_预约全部功能用户上车")
    def test_caseid_1987680(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=1,driver_level=1,passenger_level=1,steering_level=1,DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        time.sleep(0.8)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_RemoteOn_req(timeout=20)
        self.soa.check_SetTemperature_req(zoneid=ClimateZoneId.FirstRowLeft, temp=23,timeout=20)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_RemotePowerStatus(sts = RemoteClimateStatus.On)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        # self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["ac_control", "rear_right_seat_vent", "rear_left_seat_vent"])
        self.soa.empty_all()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "Off", 1800, None)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1, None) 
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 1, None)
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 1, None) 
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_预约全部功能上切convience")
    def test_caseid_1987679(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=1,driver_level=1,passenger_level=1,steering_level=1,DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        # self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["ac_control", "rear_right_seat_vent", "rear_left_seat_vent"])
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约全部功能上切convience30min")
    def test_caseid_1987678(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=1,driver_level=1,passenger_level=1,steering_level=1,DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=1,RearRightVent_level=1)
        self.soa.check_SetRemoteClimateSwitchToHV_req(isOn=True, keep_time=30, timeout=20)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(0.8)
        self.soa.check_SteerWheelService_SetHeat_req_and_feedback_resp(heat_level=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetHeatingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=HeatLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft, info=VentLevel.Low, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight, info=VentLevel.Low, timeout=20)
        self.soa.notify_ClimateSystemStatus(ac_status = False, first_row_power_status = True)
        self.soa.notify_SteerWheelService_Heat(heat_level=HeatLevel.Low)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_FrntRightSeatHeatVentStatus(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low, vent_work_sts=HeatVentWorkStatus.Off, vent_level=VentLevel.Off)
        self.soa.notify_RearLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.notify_RearRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        # self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["ac_control", "rear_right_seat_vent", "rear_left_seat_vent"])
        self.soa.empty_all()
        self.soa.soa_partner.ck_no_req("ClimateControlService_server", "Off", 1800, None)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1, None) 
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetHeatingLevel", 1, None)
        self.soa.soa_partner.ck_no_req("SteerWheelService_server", "SetHeat", 1, None) 

    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约主驾座椅通风远控调档")
    def test_caseid_1987677(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
        self.mix.chk_rvc_cock_reserv_pnc()
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
        sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
        sleep(25)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
        time_start = time.time()
        sleep(600)
        self.tsp.rvc_driver_seat_vent(level=2)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Mid,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=1230)
        assert time.time() - time_start > 1700 

    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约主驾座椅通风预约调档")
    def test_caseid_1987676(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
        self.mix.chk_rvc_cock_reserv_pnc()
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
        sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
        sleep(25)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
        sleep(60)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=2)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Mid,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        time_start = time.time()
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=1830)
        assert time.time() - time_start > 1700 
        
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_transport")
    def test_caseid_1987675(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1,PassengerVent_level=1,RearLeftVent_level=1,RearRightVent_level=1)
        assert self.tsp.log_SubscribeTaskResp_search(keywords="CarModeFail")
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约主驾座椅通风成功预约副驾座椅通风")
    def test_caseid_1987674(self):
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
        self.mix.chk_rvc_cock_reserv_pnc()
        self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
        sleep(1)
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
        sleep(25)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
        sleep(600)
        self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=-1,PassengerVent_level=2)
        self.soa.check_SetRemoteClimateSwitchToHVDelay_req(extendtime=30, timeout=20)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight,info=VentLevel.Mid,timeout=20)
        self.soa.notify_FrntRightSeatHeatVentStatus(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Mid)
        time_start = time.time()
        sleep(25)
        result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
        self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["passenger_seat_vent"])
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Off, timeout=1830)
        self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight, info=VentLevel.Off, timeout=1830)
        assert time.time() - time_start > 1700 
    
    @pytest.mark.smoke
    @allure.title("RVC_预约座椅通风_abandoned")
    def test_caseid_1987673(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
            
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_abandoned30自动关闭")
    def test_caseid_1987672(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            time_start = time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Off,timeout=1800)
            assert time.time() - time_start > 1700 
    
    @pytest.mark.smoke
    @allure.title("RVC_预约座椅通风_主驾座椅通风开启失败")
    def test_caseid_1987671(self):
        self.mix.tcam_network_sleep()
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.io.tcam_kl15_up()
            self.bus_comm.resume_all_bus_send()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"],success=False,expected_msg="DelayFail")
    
    @pytest.mark.smoke
    @allure.title("RVC_预约座椅通风_inactive通风3档")
    def test_caseid_1987670(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_inactive通风2档")
    def test_caseid_1987669(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=2)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Mid,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Mid,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Mid, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_inactive通风1档")
    def test_caseid_1987668(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Low,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Low,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_inactive30自动关闭")
    def test_caseid_1987667(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            time_start=time.time()
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
            sleep(275)
            execid = self.tsp.rvc_driver_seat_vent(level=1)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Low,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            assert self.tsp.log_search_remote_vehicle_control(execid=execid, keywords="Success")
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Off,timeout=1510)
            assert time.time() - time_start > 1700
    
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_inactive高压失败")
    def test_caseid_1987666(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
            self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC26, NMSts.valid, timeout=20)
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="RemClimaHvStrtFail")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"],expected_msg="RemClimaHvStrtFail",success=False)
            
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_inactive主驾座椅通风开启失败")
    def test_caseid_1987665(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC30, NMSts.valid, timeout=20)
            self.bus_comm.check_PNC(BusName.connectivitycanfd, NMMsgId.x509, TCAMPNC.PNC26, NMSts.valid, timeout=20)
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(2)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"],expected_msg="DelayFail",success=False)
            
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约副驾开启成功")
    def test_caseid_1987664(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,PassengerVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontRight,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntRightSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success")
            
    @pytest.mark.smoke
    @allure.title("RVC_预约座椅通风_convience通风3档")
    def test_caseid_1987663(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
               
    @pytest.mark.santiy
    @allure.title("RVC_预约座椅通风_convience通风2档")
    def test_caseid_1987662(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=2)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Mid,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Mid, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
            
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_convience通风1档")
    def test_caseid_1987661(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft, info=VentLevel.Low, timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
               
    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_convience主驾座椅通风开启失败")
    def test_caseid_1987660(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=1)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.Low,timeout=20)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="DelayFail")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"],expected_msg="DelayFail",success=False)
            
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_convience主驾座椅加热开启")
    def test_caseid_1987659(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(heat_level=HeatLevel.Low, heat_work_sts=HeatVentWorkStatus.On)
        with allure.step("下发远控预约座椅通风3档"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_convience主驾座椅通风开启")
    def test_caseid_1987658(self):
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.Low, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId"), f"TCAM远程座舱预约执行结果上报到车云的结果校验失败"
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_用户上车维持")
    def test_caseid_1987657(self):
        with allure.step("下发远控预约通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])
        self.soa.s2s_set_usage_mode(UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(UsageMode.CONVENIENCE)
        self.soa.soa_partner.ck_no_req("SeatService_server", "SetVentingLevel", 1800, {"params": [{"id": 0, "uint8Info": 0}], "source": 2}) 
    
    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约左后座椅通风")
    def test_caseid_1987656(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,RearLeftVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_RearLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success")

    @pytest.mark.full
    @allure.title("RVC_预约座椅通风_预约右后座椅通风")
    def test_caseid_1987655(self):
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,RearRightVent_level=3)
            self.mix.chk_rvc_cock_reserv_pnc()
            self.soa.check_SetRemoteClimateSwitchToHV_req_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight,info=VentLevel.High,timeout=20)
            sleep(1)
            self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.RearRight,info=VentLevel.High,timeout=20)
            self.soa.notify_RearRightSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            assert self.tsp.log_SubscribeTaskResp_search(detail="cmdResp=execId", keywords="Success")

    @pytest.mark.sanity
    @allure.title("RVC_预约座椅通风_延长高压")
    def test_caseid_1987654(self):
        self.soa.notify_RemoteClimateHVStatus(remote_climate_Status=RemoteClimateStatus.On)
        with allure.step("下发远控预约座椅通风"):
            self.tsp.rvc_taskCmd(appointment_minute=15, ac=-1,driver_level=-1,passenger_level=-1,steering_level=-1,DriverVent_level=3)
            self.soa.check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(timeout=20)
            self.soa.check_SeatService_SetVentingLevel_req_and_feedback_resp(id=SeatId.FrontLeft,info=VentLevel.High,timeout=20)
            self.soa.notify_FrntLeftSeatHeatVentStatus(vent_level=VentLevel.High, vent_time=30, vent_work_sts=HeatVentWorkStatus.On)
            sleep(25)
            result=self.tsp.log_SubscribeTaskUpload_search(fuzz_match="msg=SubscribeTask|SubscribeTaskExecUpload finsh", detail="taskExec=execId", keywords="Success")
            self.mix.chk_rvc_vent_reserv_taskupload(message=result,fields_to_check=["driver_seat_vent"])             