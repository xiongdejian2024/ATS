#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature("远程控制/远控两域联调测试/远控方向盘加热")
@allure.story("远控方向盘加热")
class TestRvcseat(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client",
                         "SeatService_client",
                         "HighVoltageService_client",
                         "SteerWheelService_client",
                         "VehicleSetStatusService_client",
                         "ClimateControlService_client"])
        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02})
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.Off)

    def before_each_func(self, ecu):
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.Off)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Off)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.set_max_ClimaActv_sts(sts=isOn.Off)
        self.soa.hmi_set_acinhibit_sts(sts=False)
         
    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        # self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Start)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("两域RVC_远控开启方向盘加热_abandoned")
    @pytest.mark.Sanity
    def test_caseid_1984914(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=1)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_TelmSteerWhlHeatgReqLvl(level=HeatLevel.Low)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.Idle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("两域RVC_远控开启方向盘加热_inactive加热3档")
    @pytest.mark.Sanity
    def test_caseid_1984913(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=3)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_TelmSteerWhlHeatgReqLvl(level=HeatLevel.High)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.Idle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("两域RVC_远控关闭方向盘加热_inactive")
    @pytest.mark.Sanity
    def test_caseid_1984911(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=-1)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.check_TelmSteerWhlHeatgReqLvl(level=HeatLevel.Off)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.Idle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("两域RVC_远控开启方向盘加热_convience加热3档")
    @pytest.mark.Sanity
    def test_caseid_1984912(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=3)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.High)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.High, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("两域RVC_远控关闭方向盘加热_convience")
    @pytest.mark.Sanity
    def test_caseid_1984910(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=-1)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启方向盘加热_ACTIVE_1档")
    @pytest.mark.smoke
    def test_caseid_1991531(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=1)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控关闭方向盘加热_ACTIVE")
    @pytest.mark.smoke
    def test_caseid_1991530(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=-1)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启方向盘加热_DRIVING_2档")
    @pytest.mark.smoke
    def test_caseid_1991529(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=2)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控关闭方向盘加热_DRIVING")
    @pytest.mark.smoke
    def test_caseid_1991528(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=-1)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启方向盘加热_模式上切ACTIVE_加热保持")
    @pytest.mark.Sanity
    def test_caseid_1991527(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=2)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        self.bus_comm.check_TelmSteerWhlHeatgReqLvl(level=HeatLevel.Mid)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(2)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.Idle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控开启方向盘加热_模式上切INACTIVE_加热关闭")
    @pytest.mark.Sanity
    def test_caseid_1991526(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=2)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Off, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控预约开启方向盘加热_模式上切ACTIVE_加热保持")
    @pytest.mark.Sanity
    def test_caseid_1991525(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=2)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        self.bus_comm.check_TelmSteerWhlHeatgReqLvl(level=HeatLevel.Mid)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(2)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.Idle)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控方向盘加热1档切换2档")
    @pytest.mark.Sanity
    def test_caseid_1991524(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=1)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.tsp.rvc_steering_wheel_heat(level=2)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控方向盘加热3档切换1档")
    @pytest.mark.Sanity
    def test_caseid_1991523(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=3)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Low)
        # self.bus_comm.check('backbonefr', 'CemBackBoneFr19', 'SteerWhlHeatgLvlSts', 1)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Low, source=SourceId.Remote)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控方向盘座椅加热联动_模式上切_ACTIVE_加热保持")
    @pytest.mark.full
    def test_caseid_1991522(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        execid=self.tsp.rvc_steering_wheel_heat(level=2)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        sleep(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_steerwheel_remHeat_sts(level=HeatLevel.Mid)
        self.bus_comm.check_TelmSteerWhlHeatgReqLvl(level=HeatLevel.Mid)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.soa.event_check_steer_wheel_heat_level(level=HeatLevel.Mid, source=SourceId.Remote)
        self.soa.event_check_frntleft_heat_sts(heat_level=HeatLevel.High,heat_work_sts=HeatVentWorkStatus.On)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"