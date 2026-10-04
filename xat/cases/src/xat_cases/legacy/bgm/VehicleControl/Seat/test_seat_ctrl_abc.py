#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_steerwheel_ctrl.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/21 11:30
@Description: BGM车控车座椅功能
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("车控车设")
@allure.story("后视镜功能")
class TestSeatCtrl(TestABCBase):
    def before_class(self, ecu):
        # logger.info("------------------>复位BGM")
        # self.io.bgm_power_off()
        # sleep(2)
        # self.io.bgm_power_on()
        # time.sleep(15)
        # logger.info("------------------>复位BGM结束")
        
        self.soa.update(["SeatService_client","CentralLockService_client","DoorService_client",
                         "TailGateService_client","KeyService_client","VehicleModeService_client",])
        sleep(2)
        self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
        self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)

    def before_each_func(self, ecu):
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2, 94: 0x80, 142:0x83, 10: 0x2})
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)

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

    @allure.title("主驾座椅加热到Level3(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    @pytest.mark.verify
    @pytest.mark.mcu_test
    def test_caseid_113220(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)

    @allure.title("主驾座椅加热到Level2(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_1983317(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)

    @allure.title("主驾座椅加热到Level1(CarMode=Normal;UsageMode=Driving)")  #o_fan.lilu pass
    @pytest.mark.smoke
    @pytest.mark.a0925
    def test_caseid_118723(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)

    @allure.title("副驾座椅加热到Level1(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118724(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)

    @allure.title("副驾座椅加热到Level2(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_1983318(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)

    @allure.title("副驾座椅加热到Level3(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118726(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)

    @allure.title("主驾座椅通风到Level3(CarMode=Normal;UsageMode=Driving)")     #o_fan.liu 整改ok
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    @pytest.mark.a0925
    def test_caseid_118731(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)

    @allure.title("主驾座椅通风到Level2(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_1983319(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)

    @allure.title("主驾座椅通风到Level1(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118734(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)

    @allure.title("副驾座椅通风到Level1(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118729(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)

    @allure.title("副驾座椅通风到Level2(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_1983320(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)

    @allure.title("副驾座椅通风到Level3(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118727(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)

 
    @allure.title("主驾座椅按摩到Level3(CarMode=Normal;UsageMode=Driving)")  #o_fan.liu 整改ok
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    @pytest.mark.a0925
    def test_caseid_118740(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_massg_level(pos=SeatId.FrontLeft,is_on=True,type=MassType.Type1,intensity=MassIntensity.High)
        self.bus_comm.check_seat_massg_req(pos=SeatId.FrontLeft,  is_on=True, type=MassType.Type1, level=MassIntensity.High)

    @allure.title("主驾座椅按摩到Level2(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118739(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_massg_level(pos=SeatId.FrontLeft,is_on=True,type=MassType.Type1,intensity=MassIntensity.Normal)
        self.bus_comm.check_seat_massg_req(pos=SeatId.FrontLeft,is_on=True, type=MassType.Type1, level=MassIntensity.Normal)

    @allure.title("主驾座椅按摩到Level1(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118738(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_massg_level(pos=SeatId.FrontLeft,is_on=True,type=MassType.Type1,intensity=MassIntensity.Low)
        self.bus_comm.check_seat_massg_req(pos=SeatId.FrontLeft,is_on=True,type=MassType.Type1,level=MassIntensity.Low)

    @allure.title("副驾座椅按摩到Level1(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118743(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_massg_level(pos=SeatId.FrontRight,is_on=True,type=MassType.Type1,intensity=MassIntensity.Low)
        self.bus_comm.check_seat_massg_req(pos=SeatId.FrontRight,is_on=True,type=MassType.Type1,level=MassIntensity.Low)

    @allure.title("副驾座椅按摩到Level2(CarMode=Normal;UsageMode=Driving)")    #LF  暂时屏蔽
    @pytest.mark.smoke
    def test_caseid_118742(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_massg_level(pos=SeatId.FrontRight,is_on=True,type=MassType.Type1,intensity=MassIntensity.Normal)
        self.bus_comm.check_seat_massg_req(pos=SeatId.FrontRight,is_on=True,type=MassType.Type1,level=MassIntensity.Normal)

    @allure.title("副驾座椅按摩到Level3(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118741(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_massg_level(pos=SeatId.FrontRight,is_on=True,type=MassType.Type1,intensity=MassIntensity.High)
        self.bus_comm.check_seat_massg_req(pos=SeatId.FrontRight,is_on=True,type=MassType.Type1,level=MassIntensity.High)

    @allure.title("主驾座椅高度向上调节(CarMode=Normal;UsageMode=Driving)")      #o_fan.liu 确认ok
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    @pytest.mark.a09251
    
    def test_caseid_118753(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        # self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.Seat,direction=AdjustDirection.Down)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.Seat,direction=AdjustDirection.Up)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Height,req=SeatUpDownAdj.Up)

    @allure.title("主驾座椅高度向下调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_caseid_118754(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.Seat,direction=AdjustDirection.Down)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Height,req=SeatUpDownAdj.Down)

    @allure.title("主驾座椅向前调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_caseid_114284(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.Seat,direction=AdjustDirection.Forward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Len,req=SeatForwBackAdj.Forward)

    @allure.title("主驾座椅向后调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    @pytest.mark.mcu_test
    def test_caseid_118744(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.Seat,direction=AdjustDirection.Backward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Len,req=SeatForwBackAdj.Backward)

    @allure.title("主驾靠背向前调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_114283(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatBack,direction=AdjustDirection.Forward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Back,req=SeatForwBackAdj.Forward)

    @allure.title("主驾靠背向后调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118757(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatBack,direction=AdjustDirection.Backward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Back,req=SeatForwBackAdj.Backward)

    @allure.title("主驾座椅腿托向上调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_114288(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatLegrest,direction=AdjustDirection.Up)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Legrest,req=SeatUpDownAdj.Up)

    @allure.title("主驾座椅腿托向下调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118752(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatLegrest,direction=AdjustDirection.Down)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Legrest,req=SeatUpDownAdj.Down)

    @allure.title("主驾座椅腰托向上调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118746(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatLumbar,direction=AdjustDirection.Up)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Lumbar,req=SeatUpDownAdj.Up)

    @allure.title("主驾座椅腰托向下调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118747(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatLumbar,direction=AdjustDirection.Down)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Lumbar,req=SeatUpDownAdj.Down)

    @allure.title("主驾座椅腰托向前调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_114289(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatLumbar,direction=AdjustDirection.Forward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Lumbar,req=SeatForwBackAdj.Forward)

    @allure.title("主驾座椅腰托向后调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118748(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_driver_seat_btn_psd_sts(sts=False,time_wait=2)
        self.bus_comm.set_driver_seat_ext_adj_allow_sts(sts=True,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontLeft,part=SeatPart.SeatLumbar,direction=AdjustDirection.Backward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontLeft,type=SeatAdjustType.Lumbar,req=SeatForwBackAdj.Backward)

    @allure.title("副驾座椅高度向上调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118756(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.Seat,direction=AdjustDirection.Up)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Height,req=SeatUpDownAdj.Up)

    @allure.title("副驾座椅高度向下调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118755(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.Seat,direction=AdjustDirection.Down)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Height,req=SeatUpDownAdj.Down)

    @allure.title("副驾座椅向前调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_114285(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.Seat,direction=AdjustDirection.Forward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Len,req=SeatForwBackAdj.Forward)

    @allure.title("副驾座椅向后调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118745(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.Seat,direction=AdjustDirection.Backward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Len,req=SeatForwBackAdj.Backward)

    @allure.title("副驾座椅靠背向前调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118759(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.SeatBack,direction=AdjustDirection.Forward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Back,req=SeatForwBackAdj.Forward)

    @allure.title("副驾座椅靠背向后调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118758(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.SeatBack,direction=AdjustDirection.Backward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Back,req=SeatForwBackAdj.Backward)

    @allure.title("副驾座椅腰托向上调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118750(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.SeatLumbar,direction=AdjustDirection.Up)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Lumbar,req=SeatUpDownAdj.Up)

    @allure.title("副驾座椅腰托向下调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118751(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.SeatLumbar,direction=AdjustDirection.Down)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Lumbar,req=SeatUpDownAdj.Down)

    @allure.title("副驾座椅腰托向前调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_113221(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.SeatLumbar,direction=AdjustDirection.Forward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Lumbar,req=SeatForwBackAdj.Forward)

    @allure.title("副驾座椅腰托向后调节(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118749(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_pass_seat_btn_psd_sts(sts=False,time_wait=2)
        self.soa.hmi_set_seat_adjust_direction(pos=SeatId.FrontRight,part=SeatPart.SeatLumbar,direction=AdjustDirection.Backward)
        self.bus_comm.check_seat_direction_adjust_req(pos=SeatId.FrontRight,type=SeatAdjustType.Lumbar,req=SeatForwBackAdj.Backward)

    @allure.title("主驾座椅加热到Level3后,锁车自动关闭加热(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118816(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)

    @allure.title("主驾座椅通风到Level3后,锁车自动关闭通风(CarMode=Normal;UsageMode=Driving)")
    @pytest.mark.smoke
    def test_caseid_118815(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)

    @allure.title("主驾座椅按摩到Level3后,锁车自动关闭按摩(CarMode=Normal;UsageMode=INACTIVE)")
    @pytest.mark.smoke
    def test_caseid_118814(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_seat_massg_level(pos=SeatId.FrontRight,is_on=True,type=MassType.Type1,intensity=MassIntensity.Normal)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_seat_heat_massg_sts(pos=SeatId.FrontRight,sts=isOn.Off)


    @allure.title("关闭二排右侧座椅加热(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418522?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982576(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off, source=SourceId.HMI)


    @allure.title("关闭二排左侧座椅加热(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418520?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982575(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)


    @allure.title("打开后排左侧座椅加热3档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418514?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982574(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)


    @allure.title("打开后排左侧座椅加热1档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418510?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982573(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)


    @allure.title("打开后排左侧座椅加热2档(CarMode=Normal;UsageMode=Driving)")   #o_fan.liu  整改ok
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2369929?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982569(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)


    @allure.title("打开后排右侧座椅加热3档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2419069?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982572(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)


    @allure.title("打开后排右侧座椅加热1档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2419066?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982571(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)


    @allure.title("打开后排右侧座椅加热2档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418506?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982570(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)


    @allure.title("打开后排右侧座椅通风3档(CarMode=Normal;UsageMode=Driving)")    
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418612?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982582(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)


    @allure.title("打开后排右侧座椅通风1档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418608?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982580(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)


    @allure.title("打开后排右侧座椅通风2档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418609?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982581(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)


    @allure.title("打开后排左侧座椅通风1档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2369992?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982577(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)


    @allure.title("打开后排左侧座椅通风3档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418606?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982579(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)



    @allure.title("打开后排左侧座椅通风2档(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418604?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982578(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)



    @allure.title("关闭后排右侧座椅通风(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418618?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982584(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off, source=SourceId.HMI)


    @allure.title("关闭后排左侧座椅通风(CarMode=Normal;UsageMode=Driving)")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2418613?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1982583(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)

    
    @allure.title("Crash模式打开加热3档(CarMode=Crash;UsageMode=Convenice)")
    @pytest.mark.full
    def test_caseid_1985071(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)


    @allure.title("Crash模式打开通风1档(CarMode=Crash;UsageMode=Convenice)")
    @pytest.mark.full
    def test_caseid_1985072(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)



    @allure.title("主驾座椅加热打开,5s没占位保存挡位自动关闭")
    @pytest.mark.full
    def test_caseid_118766(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        # self.bus_comm.set("chassiscan2","VddmChas2Fr17","DrvrSeatSts",2)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontLeft,seat_sts=DriverSeatOccptSts.OccptPrsnt)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.On)
        # self.bus_comm.set("chassiscan2","VddmChas2Fr17","DrvrSeatSts",1)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontLeft,seat_sts=DriverSeatOccptSts.OccptNotPrsnt)
        sleep(5)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)


    @allure.title("副驾座椅加热打开,5s没占位保存挡位自动关闭")
    @pytest.mark.full
    @pytest.mark.test
    def test_caseid_118767(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        # self.bus_comm.set("backbonefr","SrsBackBoneFr04","PassSeatSts",2)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight,seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
        # self.bus_comm.set("backbonefr","SrsBackBoneFr04","PassSeatSts",0)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight,seat_sts=SeatOccptSts.Empty)
        sleep(5)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Off, source=SourceId.HMI)





    @allure.title("后排座椅加热打开后,打开后排通风,座椅加热自动关闭")
    @pytest.mark.full
    def test_caseid_1985059(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRow,level=HeatVentiLvl.Off, source=SourceId.HMI)



    @allure.title("前排座椅加热打开后,打开前排通风,座椅加热自动关闭")
    @pytest.mark.full
    def test_caseid_1985052(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)


    @allure.title("后排座椅加热打开后,设置座椅加热状态等于3,加热自动关闭")
    @pytest.mark.full
    def test_caseid_1985056(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Error)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Off)



    @allure.title("后排座椅加热打开后,设置座椅加热状态等于4.加热自动关闭")
    @pytest.mark.full
    def test_caseid_1985057(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Functionallimit)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Off)



    @allure.title("后排座椅加热打开后,设置座椅加热状态等于5.加热自动关闭")
    @pytest.mark.full
    def test_caseid_1985058(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Energylimit)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Off)


    # @allure.title("前排座椅加热打开后,设置座椅加热状态等于3.加热自动关闭")
    # @pytest.mark.full
    # @pytest.mark.test_1
    # def test_caseid_1988133(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.On)
    #     self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level3)
    #     self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Error)
    #     self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off)
    #     self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Off)



    @allure.title("前排座椅加热打开后,设置座椅加热状态等于4.加热自动关闭")
    @pytest.mark.full
    @pytest.mark.test
    def test_caseid_1985054(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Functionallimit)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Off)


    @allure.title("前排座椅加热打开后,设置座椅加热状态等于5.加热自动关闭")
    @pytest.mark.full
    @pytest.mark.test
    def test_caseid_1985055(self):
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Energylimit)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Off)


    @allure.title("前排座椅通风打开后,设置座椅加热状态等于3.通风自动关闭")
    @pytest.mark.full
    @pytest.mark.test
    def test_caseid_1985067(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Error)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Off)


    @allure.title("前排座椅通风打开后,设置座椅加热状态等于4.通风自动关闭")
    @pytest.mark.full
    @pytest.mark.test_1
    def test_caseid_1985066(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Functionallimit)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Off)


    @allure.title("前排座椅通风打开后,设置座椅加热状态等于5.通风自动关闭")
    @pytest.mark.full
    @pytest.mark.test_1
    def test_caseid_1985065(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Energylimit)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRow,sts=HeatVentiSts.Off)



    @allure.title("后排座椅通风打开后,设置座椅加热状态等于5.通风自动关闭")
    @pytest.mark.full
    def test_caseid_1985064(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Energylimit)
        self.bus_comm.check_seat_venti_req(pos=SeatId.RearRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Off)



    @allure.title("后排座椅通风打开后,设置座椅加热状态等于4.通风自动关闭")
    @pytest.mark.full
    def test_caseid_1985063(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Functionallimit)
        self.bus_comm.check_seat_venti_req(pos=SeatId.RearRow,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Off)


    @allure.title("后排座椅通风打开后,设置座椅加热状态等于3.通风自动关闭")
    @pytest.mark.full
    def test_caseid_1985062(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.On)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.RearRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRow,sts=HeatVentiSts.Error)
        self.bus_comm.check_seat_venti_req(pos=SeatId.RearRow,level=HeatVentiLvl.Off, source=SourceId.HMI)



    @allure.title("前排座椅通风打开后,打开前排加热,座椅通风自动关闭")
    @pytest.mark.full
    def test_caseid_1985060(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)



    @allure.title("前排座椅通风打开后,打开前排加热,座椅通风自动关闭")
    @pytest.mark.full
    def test_caseid_1985061(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRow,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRow,level=HeatVentiLvl.Off, source=SourceId.HMI)



    @allure.title("Factory模式打开加热3档(CarMode=Factory;UsageMode=Convenice)")
    @pytest.mark.full
    def test_caseid_1985070(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)



    @allure.title("Crash模式打开加热3档(CarMode=Factory;UsageMode=Convenice)")
    @pytest.mark.full
    def test_caseid_1985071(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)



    @allure.title("Factory模式打开通风1档(CarMode=Factory;UsageMode=Convenice)")
    @pytest.mark.full
    def test_caseid_1985074(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)


    @allure.title("Transport模式打开通风1档")
    @pytest.mark.full
    def test_caseid_1985073(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_seat_venti_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2)
        self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Off, source=SourceId.HMI)


    # @allure.title("主驾座椅通风打开,5s没占位保存挡位自动关闭")
    # @pytest.mark.full
    # def test_caseid_118765(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
    #     # self.bus_comm.set("chassiscan2","VddmChas2Fr17","DrvrSeatSts",2)
    #     self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontLeft,seat_sts=DriverSeatOccptSts.OccptPrsnt)
    #     self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
    #     # self.bus_comm.set("chassiscan2","VddmChas2Fr17","DrvrSeatSts",1)
    #     self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontLeft,seat_sts=DriverSeatOccptSts.OccptNotPrsnt)
    #     sleep(6)
    #     self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)
    #     self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontLeft,sts=HeatVentiSts.Off)


    # @allure.title("副驾座椅通风打开,5s没占位保存挡位自动关闭")   
    # @pytest.mark.full
    # def test_caseid_118764(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     # self.bus_comm.set("backbonefr","SrsBackBoneFr04","PassSeatSts",2)
    #     self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight,seat_sts=SeatOccptSts.OccptLrg)
    #     self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.On)
    #     # self.bus_comm.set("backbonefr","SrsBackBoneFr04","PassSeatSts",0)
    #     self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.FrontRight,seat_sts=SeatOccptSts.Empty)
    #     sleep(5)
    #     self.bus_comm.check_seat_venti_req(SeatId.FrontRight,level=HeatVentiLvl.Off, source=SourceId.HMI)
    #     self.bus_comm.set_seat_venti_sts(pos=SeatId.FrontRight,sts=HeatVentiSts.Off)


    @allure.title("后排座椅加热打开,5s没占位保存挡位自动关闭")
    @pytest.mark.full
    def test_caseid_1985076(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        # self.bus_comm.set("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecLe",2)
        # self.bus_comm.set("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecRi",2)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearRow,seat_sts=SeatOccptSts.OccptLrg)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
        self.bus_comm.set_seat_heat_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
        # self.bus_comm.set("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecLe",0)
        # self.bus_comm.set("backbonefr","SrsBackBoneFr04","SeatOccptAtRowSecRi",0)
        self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearRow,seat_sts=SeatOccptSts.Empty)
        sleep(5)
        self.bus_comm.check_seat_venti_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)
        self.bus_comm.check_seat_venti_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off, source=SourceId.HMI)

    # @allure.title("后排座椅通风打开,5s没占位保存挡位自动关闭")
    # @pytest.mark.full
    # def test_caseid_1985077(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearRow,seat_sts=SeatOccptSts.OccptLrg)
    #     self.bus_comm.set_seat_venti_sts(pos=SeatId.RearLeft,sts=HeatVentiSts.On)
    #     self.bus_comm.set_seat_venti_sts(pos=SeatId.RearRight,sts=HeatVentiSts.On)
    #     self.bus_comm.set_seat_occpt_sts(seat_id=SeatId.RearRow,seat_sts=SeatOccptSts.Empty)
    #     sleep(5)
    #     self.bus_comm.check_seat_venti_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, source=SourceId.HMI)
    #     self.bus_comm.check_seat_venti_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off, source=SourceId.HMI)
        
        
 ##################################### 调试 #########################       
    # @allure.title("远控前左加热")   #o_fan.liu  
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/2369929?projectId=46"
    # )
    # @pytest.mark.a0990
    # def test_caseid_1912012(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED)
    #     self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_heat_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level2, source=SourceId.Remote)
   
        
    # @allure.title("远控前右加热")   #o_fan.liu  
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/2369929?projectId=46"
    # )
    # @pytest.mark.a0990
    # def test_caseid_1912013(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
    #     self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_heat_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level2, source=SourceId.Remote)
        
        
        
    # @allure.title("远控后左加热")   #o_fan.liu  
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/2369929?projectId=46"
    # )
    # @pytest.mark.a0990
    # def test_caseid_1912014(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED)
    #     self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, source=SourceId.Remote)
   
        
    # @allure.title("远控后右加热")   #o_fan.liu  
    # @allure.testcase(
    #     "https://jama.jiduauto.com/perspective.req#/testCases/2369929?projectId=46"
    # )
    # @pytest.mark.a0990
    # def test_caseid_1912015(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
    #     self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, source=SourceId.Remote)
        
        
    # @allure.title("前左远控通风")     #o_fan.liu 
    # @pytest.mark.smoke
    # @pytest.mark.a0990
    # def test_caseid_1912016(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED)             
    #     self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_venti_req(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
        
        
    # @allure.title("前右远控通风")     #o_fan.liu 
    # @pytest.mark.smoke
    # @pytest.mark.a0990
    # def test_caseid_1912017(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)             
    #     self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_venti_req(pos=SeatId.FrontRight,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
        
    # @allure.title("后左远控通风")     #o_fan.liu 
    # @pytest.mark.smoke
    # @pytest.mark.a0990
    # def test_caseid_1912018(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED)             
    #     self.soa.hmi_set_seat_vent_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_venti_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
        
        
    # @allure.title("后右远控通风")     #o_fan.liu 
    # @pytest.mark.smoke
    # @pytest.mark.a0990
    # def test_caseid_1912019(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)             
    #     self.soa.hmi_set_seat_vent_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
    #     self.bus_comm.check_seat_venti_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.Remote)
    
    
    ############################################## 1008 #############################################
    @allure.title("normal&&Active_打开二排右侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994668(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
        
    @allure.title("normal&&Driving_打开二排右侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994667(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Convinience_打开二排右侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994666(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
    @allure.title("Dyno&&Driving_打开二排右侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994665(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
        
    @allure.title("normal&&Active_打开二排左侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994664(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        

    @allure.title("normal&&Active_打开二排左侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994663(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Convinience_打开二排左侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994662(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        
    @allure.title("Dyno&&Driving_打开二排左侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994661(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        
        
    @allure.title("normal&&Active_打开二排右侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994660(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        
    @allure.title("normal&&Driving_打开二排右侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994659(self):  #o_fan.liu1111
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Convinience_打开二排右侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994658(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Driving_打开二排右侧座椅加热2级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994657(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level2, source=SourceId.HMI)
        
        
    @allure.title("normal&&Active_打开二排右侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994656(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
    @allure.title("normal&&Driving_打开二排右侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994655(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
    @allure.title("Dyno&&Convinience_打开二排右侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994654(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
    @allure.title("Dyno&&Driving_打开二排右侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994653(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
        
    @allure.title("normal&&Active_打开二排左侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994652(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
    @allure.title("normal&&Driving_打开二排左侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994651(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Convinience_打开二排左侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994650(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
    @allure.title("Dyno&&Driving_打开二排左侧座椅加热3级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994649(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, source=SourceId.HMI)
        
        
    @allure.title("normal&&Active_打开二排左侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994648(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
    @allure.title("normal&&Driving_打开二排左侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994647(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
    @allure.title("Dyno&&Convinience_打开二排左侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994646(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Driving_打开二排左侧座椅加热1级-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994645(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level1, source=SourceId.HMI)
        
        
    @allure.title("normal&&Active_关闭二排右侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994644(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
    @allure.title("normal&&Driving_关闭二排右侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994643(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Convinience_关闭二排右侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994642(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
    @allure.title("Dyno&&Driving_关闭二排右侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994641(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearRight,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearRight,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
        
        
        
    @allure.title("normal&&Active_关闭二排左侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994640(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
    @allure.title("normal&&Driving_关闭二排左侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994639(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
        
    @allure.title("Dyno&&Convinience_关闭二排左侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994638(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
    @allure.title("Dyno&&Driving_关闭二排左侧座椅加热-本地")
    @pytest.mark.full
    @pytest.mark.a1008
    def test_caseid_1994637(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Level3,  source=SourceId.HMI)
        
        self.soa.hmi_set_seat_heat_level(pos=SeatId.RearLeft,level=HeatVentiLvl.Off, sourceId=SourceId.HMI)
        self.bus_comm.check_seat_heat_req(pos=SeatId.RearLeft,level=HeatVentiLvl.Off,  source=SourceId.HMI)
        
        
    @allure.title("主驾_加热状态值由非0变为0_1s结束，通知订阅方")
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1994604(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)  
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On)          
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level1)   
        sleep(.1)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft, level=HeatVentiLvl.Off)   

        self.soa.event_check_frntleft_heat_sts2(heat_level= HeatLevel.Low,                       
                                                heat_work_sts = HeatVentWorkStatus.On,
                                                vent_level = VentLevel.Off,
                                                vent_work_sts = HeatVentWorkStatus.kNone, source = SourceId.HMI)           
            
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.Functionallimit)  
        sleep(1)
         
        self.soa.event_check_frntleft_heat_sts2(heat_level= HeatLevel.Off,                                          #异常情况，加热是1                              
                                                heat_work_sts = HeatVentWorkStatus.FunctionLimit,
                                                vent_level = VentLevel.Off,
                                                vent_work_sts = HeatVentWorkStatus.kNone, source = SourceId.HMI)      
        
        # self.soa.hmi_set_seat_vent_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)    

        # self.bus_comm.set_singal('bodycan','SmdBodyFr04','DrvrSeatVentnLvlSts', 1) 
        # sleep(.2)
   
        # self.soa.event_check_frntleft_heat_sts2(heat_level= HeatLevel.Off,                                                    #异常情况，通风是1                            
        #                                         heat_work_sts = HeatVentWorkStatus.FunctionLimit,
        #                                         vent_level = VentLevel.Low,
        #                                         vent_work_sts = HeatVentWorkStatus.kNone, source = SourceId.HMI)      
        # self.bus_comm.set_singal('bodycan','SmdBodyFr04','DrvrSeatHeatgAvlSts', 0) 
        # self.bus_comm.set_singal('bodycan','SmdBodyFr04','DrvrSeatVentnLvlSts', 0) 
        # sleep(.2)
        
        
         
    @allure.title("主驾_加热状态值由非0变为0_1s内变化，立即通知订阅方")
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1994603(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontLeft,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)  
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontLeft, sts=HeatVentiSts.On) 
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level1)   
        sleep(.2)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft, level=HeatVentiLvl.Off)  
        sleep(.1)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontLeft, level=HeatVentiLvl.Level2)  

        self.soa.event_check_frntleft_heat_sts2(heat_level= HeatLevel.Mid,                       
                                                heat_work_sts = HeatVentWorkStatus.On,
                                                vent_level = VentLevel.Off,
                                                vent_work_sts = HeatVentWorkStatus.kNone, source = SourceId.HMI)           
            
       
        
        
        
    @allure.title("副驾_加热状态值由非0变为0_1s结束，通知订阅方")
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1994606(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)    
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight, level=HeatVentiLvl.Level1)  
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On) 
        sleep(.2)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight, level=HeatVentiLvl.Off)  

        self.soa.event_check_frntright_heat_sts2(heat_level= HeatLevel.Low,                       
                                                heat_work_sts = HeatVentWorkStatus.On,
                                                vent_level = VentLevel.Off,
                                                vent_work_sts = HeatVentWorkStatus.kNone, source = SourceId.HMI)           
            
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.Functionallimit) 
        sleep(1)
         
        self.soa.event_check_frntright_heat_sts2(heat_level= HeatLevel.Off,                       
                                                heat_work_sts = HeatVentWorkStatus.FunctionLimit,
                                                vent_level = VentLevel.Off,
                                                vent_work_sts = HeatVentWorkStatus.kNone, source = SourceId.HMI)    
        
        
        
    @allure.title("副驾_加热状态值由非0变为0_1s内变化，立即通知订阅方")
    @pytest.mark.sanity
    @pytest.mark.a1112
    def test_caseid_1994605(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_seat_heat_level(pos=SeatId.FrontRight,level=HeatVentiLvl.Level1, sourceId=SourceId.HMI)    
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight, level=HeatVentiLvl.Level1)  
        self.bus_comm.set_seat_heat_sts(pos=SeatId.FrontRight, sts=HeatVentiSts.On) 
        sleep(.2)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight, level=HeatVentiLvl.Off)
        sleep(.1)
        self.bus_comm.set_seat_heat_level(pos=SeatId.FrontRight, level=HeatVentiLvl.Level2)

        self.soa.event_check_frntright_heat_sts2(heat_level= HeatLevel.Mid,                       
                                                heat_work_sts = HeatVentWorkStatus.On,
                                                vent_level = VentLevel.Off,
                                                vent_work_sts = HeatVentWorkStatus.kNone, source = SourceId.HMI)           
            
