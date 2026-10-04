# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_welcomelight.py
@Time         :2024/03/14 14:20:31
@Author       :xiangyue.li@jiduauto.com
@Description  :BGM车控车设迎宾灯
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
@allure.story("内灯功能")
class TestIntrlightCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(
            [
                "LightService_client",
                "CentralLockService_client",
                "DoorService_client",
                "TailGateService_client",
                "SeatService_client",
                "KeyService_client",
                "VehicleModeService_client",
                "WiperService_client"
            ]
        )

    def before_each_func(self, ecu):
        """
        解锁、Normal、Conv、关5门、夜晚、P挡、无占座
        @param ecu:
        @return:
        """
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE, time_wait=1)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(0.5)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,
            vehmtnst=VehMtnSts.StandStillVal3, doors_sts=Door.close
        )
        self.bus_comm.set_night_mode()
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.No)
        sleep(.5)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.CancelSet)
        sleep(1)

    def after_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE, time_wait=1)
        sleep(1)


    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    @allure.title("Normal_Inactive开启副驾驶门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980950(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_Inactive开启左后门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980949(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_Inactive开启右后门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980948(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_active开启主驾驶门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980943(self):
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_active开启左后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980941(self):
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_active开启右后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980940(self):
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_driving开启主驾驶门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980947(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_driving开启副驾驶门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980946(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_driving开启左后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980945(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_driving开启右后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980944(self):
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Driving开启主驾驶门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980986(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_driving开启副驾驶门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980985(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_driving开启左后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980984(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_driving开启右后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980983(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Convenience开启主驾驶门可以打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980970(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Convenience开启副驾驶门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980954(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Convenience开启左后门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980953(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Convenience开启右后门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980952(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Inactive开启主驾驶门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980974(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Inactive满足条件的情况下开启副驾驶门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980973(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Inactive满足条件的情况下开启左后门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980972(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Inactive满足条件的情况下开启右后门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980971(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_active开启主驾驶门可以打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980978(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_active开启副驾驶门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980977(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_active开启左后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980976(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_active开启右后门可以打开阅读灯")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980975(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Abandoned开启主驾驶门打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980982(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Abandoned开启副驾门打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980981(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Abandoned开启左后门打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980980(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Dyno_Abandoned开启右后门打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980979(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_Abandoned开启主驾驶门打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980962(self):
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_Abandoned开启副驾门打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980961(self):
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_Abandoned开启左后门打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980960(self):
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Normal_Abandoned开启右后门打开阅读灯")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1980959(self):
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Transport_Abandoned开启主驾驶门打开阅读灯")
    @pytest.mark.full
    @pytest.mark.trans
    def test_intrlight_ctrl_caseid_1980958(self):
        self.mix.set_car_mode(CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("Transport_Abandoned开启副驾门打开阅读灯")
    @pytest.mark.sanity
    @pytest.mark.trans
    def test_intrlight_ctrl_caseid_1980957(self):
        self.mix.set_car_mode(CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("Transport_Abandoned开启左后门打开阅读灯")
    @pytest.mark.sanity
    @pytest.mark.trans
    def test_intrlight_ctrl_caseid_1980956(self):
        with allure.step(f"Step:设置初始条件"):
            self.mix.set_car_mode(CarMode.TRANSPORT)
            sleep(1)
            self.mix.set_usage_mode(UsageMode.ABANDONED)
            sleep(1)
            self.mix.set_usage_mode(UsageMode.INACTIVE)
            self.io.set_door(LeRe=Door.open)
            self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("Transport_Abandoned开启右后门打开阅读灯")
    @pytest.mark.sanity
    @pytest.mark.trans
    def test_intrlight_ctrl_caseid_1998909(self):
        self.mix.set_car_mode(CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("TmrForCrash")
    @pytest.mark.full
    @pytest.mark.longtime
    def test_intrlight_ctrl_caseid_118834(self):
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(300)
        self.bus_comm.wakeup_lin5()
        sleep(300)
        self.bus_comm.wakeup_lin5()
        sleep(300)
        self.bus_comm.wakeup_lin5()
        sleep(300)
        self.bus_comm.wakeup_lin5()
        sleep(300)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
