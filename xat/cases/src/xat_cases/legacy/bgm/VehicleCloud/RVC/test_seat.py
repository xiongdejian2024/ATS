#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure

from xat_cases.legacy.bgm.case_helper.environment_check import partner_process_check
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("远程控制/远控两域联调测试/远控座椅")
@allure.story("远控座椅")
class TestRvcseat(TestABCBase):
    def before_class(self, ecu):
        partner_process_check()
        self.soa.update(["SeatService_client","CentralLockService_client","DoorService_client",
                         "TailGateService_client","VehicleSetStatusService_client","KeyService_client",])
        sleep(2)
        # self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4, 179: 0x01, 180: 0x01, 181: 0x02, 189: 0x02})
        self.sd_tester.write_ccp(ccp={179: 0x02,181: 0x02, 189: 0x02})
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.Off)

    def before_each_func(self, ecu):
        # self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83, 10: 0x2, 179: 0x01, 180: 0x01})
        self.io.set_five_door_sts(Door.close)
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.Off)
        # self.bus_comm.send_ccp_to_tcam(ccp_byte_index=[181,189],ccp_value=[0x02,0x02])# 设置整车CCP支持远控后排座椅加热、后排座椅通风
         
    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Start)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def check_door_lock_ignored(self):
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorDrvrLockCmd", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorPassLockCmd", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorLeReLockCmd", 0)
        self.bus_comm.check_singal("bodycan", "CemBodyFr01", "DoorRiReLockCmd", 0)

    @allure.title("RVC_远控开启主驾座椅加热_INACTIVE_加热1档")
    @pytest.mark.smoke
    def test_caseid_1989019(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_heat(level=1)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        # self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        # self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控关闭主驾座椅加热_INACTIVE_加热1档")
    @pytest.mark.smoke
    def test_caseid_1989007(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控开启所有座椅加热_ACTIVE_加热3档")
    @pytest.mark.smoke
    def test_caseid_1989011(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_driver_seat_heat(level=3)
        self.tsp.rvc_passenger_seat_heat(level=3)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控关闭副驾座椅加热_INACTIVE_加热2档")
    @pytest.mark.smoke
    def test_caseid_1989006(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控开启副驾座椅通风_DRIVING_通风2档")
    @pytest.mark.smoke
    def test_caseid_1988983(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.tsp.rvc_passenger_seat_vent(level=2)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控关闭主驾座椅通风_INACTIVE_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988981(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_and_frntleft_heat_sts(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.tsp.rvc_driver_seat_vent(level=-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控开启副驾座椅加热_INACTIVE_加热2档")
    @pytest.mark.smoke
    def test_caseid_1989018(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_heat(level=2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控关闭主驾座椅加热_DRIVING_加热1档")
    @pytest.mark.smoke
    def test_caseid_1988998(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Low)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控关闭副驾座椅通风_INACTIVE_通风2档")
    @pytest.mark.smoke
    def test_caseid_1988980(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=VentLevel.Mid)
        self.tsp.rvc_passenger_seat_vent(level=-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控关闭所有座椅通风_ACTIVE_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988973(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_and_frntleft_heat_sts(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=VentLevel.High)
        self.tsp.rvc_driver_seat_vent(level=-1)
        self.tsp.rvc_passenger_seat_vent(level=-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控关闭副驾座椅加热_DRIVING_加热2档")
    @pytest.mark.smoke
    def test_caseid_1988997(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        self.tsp.rvc_passenger_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控关闭所有座椅加热_ACTIVE_加热3档")
    @pytest.mark.smoke
    def test_caseid_1988999(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.High)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.tsp.rvc_passenger_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控开启所有座椅通风_ACTIVE_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988985(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_driver_seat_vent(level=3)
        self.tsp.rvc_passenger_seat_vent(level=3)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控开启主驾座椅通风_DRIVING_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988984(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.tsp.rvc_driver_seat_vent(level=1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控开启副驾座椅加热_DRIVING_加热2档")
    @pytest.mark.smoke
    def test_caseid_1989009(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.tsp.rvc_driver_seat_heat(level=2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控开启主驾座椅加热_DRIVING_加热1档")
    @pytest.mark.smoke
    def test_caseid_1989010(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.tsp.rvc_driver_seat_heat(level=1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控关闭副驾座椅通风_DRIVING_通风2档")
    @pytest.mark.smoke
    def test_caseid_1988971(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.set_and_frntringht_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=VentLevel.Mid)
        self.tsp.rvc_passenger_seat_vent(level=-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控开启副驾座椅通风_INACTIVE_通风2档")
    @pytest.mark.smoke
    def test_caseid_1988992(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_passenger_seat_vent(level=2)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控关闭主驾座椅通风_DRIVING_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988972(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.set_and_frntleft_heat_sts(vent_work_sts=HeatVentWorkStatus.On, vent_level=VentLevel.Low)
        self.tsp.rvc_driver_seat_vent(level=-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控开启主驾座椅通风_INACTIVE_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988993(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_vent(level=1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控主驾座椅通风_通风3档_降低到通风2档_HMI显示通风2档")
    @pytest.mark.sanity
    def test_caseid_1988956(self):
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,sourceId=SourceId.Remote)
        self.tsp.rvc_driver_seat_vent(level=2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控主驾座椅通风_CONVENIENCE_锁车自动关闭通风")
    @pytest.mark.sanity
    def test_caseid_1988969(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_vent(level=2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.check_door_lock_ignored()
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控主驾座椅加热_CONVENIENCE_锁车自动关闭加热")
    @pytest.mark.sanity
    def test_caseid_1988995(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_heat(level=3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.check_door_lock_ignored()
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控主驾座椅加热打开后，打开座椅通风，座椅加热关闭")
    @pytest.mark.sanity
    def test_caseid_1988967(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Off)

    @allure.title("RVC_远控主驾打开座椅加热1档，副驾打开座椅通风2档_主驾加热打开_副驾通风打开")
    @pytest.mark.sanity
    def test_caseid_1988963(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level1)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontRight, level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控副驾座椅加热打开后，打开座椅通风，座椅加热关闭")
    @pytest.mark.sanity
    def test_caseid_1988966(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontRight, level=HeatVentiLvl.Level1)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontRight, level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontRight, level=HeatVentiLvl.Off)

    @allure.title("RVC_远控主驾座椅通风_通风1档500ms内提升到通风3档_HMI显示通风3档")
    @pytest.mark.sanity
    def test_caseid_1988958(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level1)
        self.tsp.rvc_driver_seat_vent(3)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控主驾座椅加热2档_500ms功能延续_座椅加热2档开启")
    @pytest.mark.sanity
    def test_caseid_1988951(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_driver_seat_heat(level=2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控主驾打开座椅通风1档，UsageMode 从Inactive切换到Convenience，500m后BGM会将当前座椅通风状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988945(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_vent(level=1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控主驾座椅通风3档_关闭座椅通风_1s后通风关闭")
    @pytest.mark.sanity
    def test_caseid_1988953(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.tsp.rvc_driver_seat_vent(level=-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控主驾座椅通风_通风2档_降低到通风1档_HMI显示通风1档")
    @pytest.mark.sanity
    def test_caseid_1988955(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.tsp.rvc_driver_seat_vent(level=1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控关闭主驾+副驾座椅通风_CONVENIENCE_通风2档")
    @pytest.mark.sanity
    def test_caseid_1988977(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontRight, level=HeatVentiLvl.Level2)
        self.tsp.rvc_driver_seat_vent(-1)
        self.tsp.rvc_passenger_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.Off)
        sleep(10)

    @allure.title("RVC_远控副驾打开座椅通风3档，UsageMode 从Inactive切换到active，500m后BGM会将当前座椅通风状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988943(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_passenger_seat_vent(3)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(0.5)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3,source=SourceId.Remote)

    @allure.title("RVC_远控主驾打开座椅加热2档，UsageMode 从Inactive切换到Convenience，100ms关闭座椅加热，BGM不会将当前座椅加热状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988949(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控主驾打开座椅通风2档，UsageMode 从Inactive切换到Convenience，100ms关闭座椅通风，BGM不会将当前座椅通风状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988944(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_driver_seat_vent(level=-1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控主驾座椅通风_通风2档_提升到通风3档_HMI显示通风3档")
    @pytest.mark.sanity
    def test_caseid_1988957(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控主驾+副驾打开座椅加热2档，UsageMode 从Inactive切换到driving，500m后BGM会将当前座椅加热状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988946(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_heat()
        self.tsp.rvc_passenger_seat_heat()
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控主驾打开座椅加热1档，UsageMode 从Inactive切换到Convenience，500m后BGM会将当前座椅加热状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988950(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)

    @allure.title("RVC_远控主驾座椅通风_通风3档_降低到通风1档_HMI显示通风1档")
    @pytest.mark.sanity
    def test_caseid_1988954(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level3)
        self.tsp.rvc_driver_seat_vent(level=1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控副驾打开座椅加热3档，UsageMode 从Inactive切换到active，500m后BGM会将当前座椅加热状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988948(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_passenger_seat_heat(3)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控关闭主驾+副驾座椅加热_CONVENIENCE_加热2档")
    @pytest.mark.sanity
    def test_caseid_1989003(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.set_and_frntleft_heat_sts(heat_work_sts=HeatVentWorkStatus.On, heat_level=HeatLevel.Mid)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off)

    @allure.title("RVC_远控开启主驾+副驾座椅加热_CONVENIENCE_加热2档")
    @pytest.mark.sanity
    def test_caseid_1989015(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_driver_seat_heat(level=2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控主驾座椅通风1档_500ms功能延续_座椅通风1档开启")
    @pytest.mark.sanity
    def test_caseid_1988952(self):
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level1)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)

    @allure.title("RVC_远控主驾座椅通风_通风1档500ms内提升到通风2档_HMI显示通风2档")
    @pytest.mark.sanity
    def test_caseid_1988959(self):
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)

    @allure.title("RVC_远控主驾+副驾打开座椅通风3档，UsageMode 从Inactive切换到driving，500m后BGM会将当前座椅通风状态通知给HMI")
    @pytest.mark.sanity
    def test_caseid_1988941(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3,source=SourceId.Remote)

    @allure.title("RVC_远控主驾座椅通风_锁车自动关闭通风_复开")
    @pytest.mark.full
    def test_caseid_1988968(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_vent(level=2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.check_door_lock_ignored()
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.tsp.rvc_driver_seat_vent(level=3)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控主驾座椅加热_锁车自动关闭加热_复开")
    @pytest.mark.full
    def test_caseid_1988994(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_driver_seat_heat(level=3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC)
        self.check_door_lock_ignored()
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.tsp.rvc_driver_seat_heat(level=2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控开启左后座椅加热_INACTIVE_加热3档")
    @pytest.mark.smoke
    def test_caseid_1989017(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(5)
        self.tsp.rvc_rearleft_seat_heat(level=3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)

    @allure.title("RVC_远控开启右后座椅加热_CONVENIENCE_加热1档")
    @pytest.mark.smoke
    def test_caseid_1989016(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_rearright_seat_heat(level=1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控开启主驾+左后座椅加热_CONVENIENCE_加热3档")
    @pytest.mark.smoke
    def test_caseid_1989014(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_driver_seat_heat(level=3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.tsp.rvc_rearleft_seat_heat(level=2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)

    @allure.title("RVC_远控开启主驾+右后座椅加热_ACTIVE_加热1档")
    @pytest.mark.smoke
    def test_caseid_1989013(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_driver_seat_heat(level=1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.tsp.rvc_rearright_seat_heat(level=2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)

    @allure.title("RVC_远控开启左后+右后座椅加热_ACTIVE_加热2档")
    @pytest.mark.smoke
    def test_caseid_1989012(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_rearleft_seat_heat(level=2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2)
        self.tsp.rvc_rearright_seat_heat(level=2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控开启左后座椅加热_DRIVING_加热3档")
    @pytest.mark.smoke
    def test_caseid_1989008(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.tsp.rvc_rearleft_seat_heat(level=3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控关闭左后座椅加热_INACTIVE_加热3档")
    @pytest.mark.smoke
    def test_caseid_1989005(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        self.tsp.rvc_rearleft_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭右后座椅加热_CONVENIENCE_加热1档")
    @pytest.mark.smoke
    def test_caseid_1989004(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level1)
        self.tsp.rvc_rearright_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭主驾+左后座椅加热_CONVENIENCE_加热3档")
    @pytest.mark.smoke
    def test_caseid_1989002(self):
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level3)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.tsp.rvc_rearleft_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭主驾+右后座椅加热_ACTIVE_加热1档")
    @pytest.mark.smoke
    def test_caseid_1989001(self):
        self.soa.rvc_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_driver_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)
        self.tsp.rvc_rearright_seat_heat(level=1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控关闭左后+右后座椅加热_ACTIVE_加热2档")
    @pytest.mark.smoke
    def test_caseid_1989000(self):
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_rearleft_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.Off)
        self.tsp.rvc_rearright_seat_heat(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控关闭右后座椅加热_DRIVING_加热3档")
    @pytest.mark.smoke
    def test_caseid_1988996(self):
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.tsp.rvc_rearright_seat_heat(level=-1)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控开启左后座椅通风_INACTIVE_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988991(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_rear_left_seat_vent(level=3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控开启右后座椅通风_CONVENIENCE_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988990(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_rear_right_seat_vent(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控开启主驾+左后座椅通风_CONVENIENCE_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988988(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_rear_left_seat_vent(3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)
        self.tsp.rvc_driver_seat_vent(3)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控开启主驾+右后座椅通风_ACTIVE_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988987(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_rear_right_seat_vent(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)
        self.tsp.rvc_driver_seat_vent(1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控开启左后+右后座椅通风_ACTIVE_通风2档")
    @pytest.mark.smoke
    def test_caseid_1988986(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_rear_right_seat_vent(2)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.tsp.rvc_rear_left_seat_vent(2)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2)

    @allure.title("RVC_远控开启左后座椅通风_DRIVING_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988982(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.tsp.rvc_rear_left_seat_vent(3)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_venti_level_sts(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3)

    @allure.title("RVC_远控关闭左后座椅通风_INACTIVE_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988979(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        self.tsp.rvc_rear_left_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭右后座椅通风_CONVENIENCE_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988978(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level1)
        self.tsp.rvc_rear_right_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭主驾+左后座椅通风_CONVENIENCE_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988976(self):
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level3)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_rear_left_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.Off)
        self.tsp.rvc_driver_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭主驾+右后座椅通风_ACTIVE_通风1档")
    @pytest.mark.smoke
    def test_caseid_1988975(self):
        self.soa.rvc_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level1)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level1)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_rear_right_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.Off)
        self.tsp.rvc_driver_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭左后+右后座椅通风_ACTIVE_通风2档")
    @pytest.mark.smoke
    def test_caseid_1988974(self):
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level3)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level1)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_rear_right_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.Off)
        self.tsp.rvc_rear_left_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控关闭右后座椅通风_DRIVING_通风3档")
    @pytest.mark.smoke
    def test_caseid_1988970(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level3)
        self.tsp.rvc_rear_right_seat_vent(-1)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.Off)
        self.bus_comm.check_seat_venti_available_sts(pos=SeatId.RearRight,sts=HeatVentiSts.Off)

    @allure.title("RVC_远控左后座椅加热打开后,打开座椅通风,座椅加热关闭")
    @pytest.mark.smoke
    def test_caseid_1988965(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level1)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearLeft, level=HeatVentiLvl.Off)

    @allure.title("RVC_远控右后座椅加热打开后,打开座椅通风,座椅加热关闭")
    @pytest.mark.smoke
    def test_caseid_1988964(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level1)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearRight, level=HeatVentiLvl.Off)

    @allure.title("RVC_远控左后打开座椅加热1档,右后打开座椅通风2档_左后加热打开_右后通风打开")
    @pytest.mark.smoke
    def test_caseid_1988962(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_rear_right_seat_vent(2)
        self.tsp.rvc_rearleft_seat_heat(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控主驾打开座椅加热1档,右后打开座椅通风2档_主驾加热打开_右后通风打开")
    @pytest.mark.smoke
    def test_caseid_1988961(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_rear_right_seat_vent(2)
        self.tsp.rvc_driver_seat_heat(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight,level=HeatVentiLvl.Level2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控副驾打开座椅加热1档,左后打开座椅通风2档_副驾加热打开_左后通风打开")
    @pytest.mark.smoke
    def test_caseid_1988960(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tsp.rvc_rear_left_seat_vent(2)
        self.tsp.rvc_passenger_seat_heat(1)
        self.bus_comm.set_RemClimaHvSts(sts=RemoteClimateStatus.On)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_venti_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_available_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        self.bus_comm.check_seat_heat_level_sts(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1)

    @allure.title("RVC_远控后排打开座椅加热1档,UsageMode 从Inactive切换到driving,500m后BGM会将当前座椅加热状态通知给HMI")
    @pytest.mark.smoke
    def test_caseid_1988947(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.soa.rvc_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_heat_climalvl(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)

    @allure.title("RVC_远控后排打开座椅通风1档,UsageMode 从Inactive切换到driving,500m后BGM会将当前座椅通风状态通知给HMI")
    @pytest.mark.smoke
    def test_caseid_1988942(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.soa.rvc_set_seat_vent_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1)
        self.bus_comm.check_seat_venti_climalvl(pos=SeatId.RearRight,level=HeatVentiLvl.Level1)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_seat_venti_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1,source=SourceId.Remote)
        self.bus_comm.check_seat_venti_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1,source=SourceId.Remote)