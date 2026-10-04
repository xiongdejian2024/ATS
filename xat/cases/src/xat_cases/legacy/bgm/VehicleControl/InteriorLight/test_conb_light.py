# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_conb_light.py
@Time         :11/18/24 10:11 AM
@Author       :yucheng.zhu@jiduauto.com 
@Description  :
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
            vehmtnst=VehMtnSts.StandStillVal3
        )
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.set_brake_pedal_sts(YesOrNo.No)
        sleep(.5)
        # self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.CancelSet)
        sleep(1)

    def after_each_func(self, ecu):
        self.bus_comm.set_vehmtn()
        self.bus_comm.set_vehspd()
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
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
            logger.info(f",,> after_class Error{str(e)}")
            pass


    # 阅读灯照脚灯状态不一致
    # -------------------------------灭-----灭---------------------------------------

    @allure.title("P挡切D挡,控制照脚灯点亮,大屏点击常关")
    @pytest.mark.full
    def test_caseid_1992010(self):
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("Crash进Normal,控制照脚灯点亮,大屏点击常关")
    @pytest.mark.full
    def test_caseid_1992009(self):
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("Conv下切Inactive,控制照脚灯点亮,大屏点击常关")
    @pytest.mark.full
    def test_caseid_1992008(self):
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("D挡切P挡等1分钟,控制照脚灯点亮,大屏点击常关")
    @pytest.mark.full
    def test_caseid_1992005(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(61)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("P挡切R挡,控制照脚灯点亮,外部闭锁")
    @pytest.mark.full
    def test_caseid_1992030(self):
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("P挡切R挡,控制照脚灯点亮,闭内锁")
    @pytest.mark.full
    def test_caseid_1992004(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.On)

    # @allure.title("Crash进Normal,控制照脚灯点亮,外部闭锁")
    # def test_caseid_1991984(self):
    #     self.mix.set_car_mode(CarMode.CRASH)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
    #     self.soa.get_footlight_sts(FootLightSts.On)
    #     self.mix.set_car_mode(CarMode.NORMAL)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
    #     self.soa.get_footlight_sts(FootLightSts.Off)
    #     self.soa.set_footlight_sts(OnOff.On)
    #     sleep(0.3)
    #     self.soa.get_footlight_sts(FootLightSts.On)
    #     self.io.hazard_light_open()
    #     self.io.hazard_light_close()
    #     self.mix.set_usage_mode(UsageMode.INACTIVE)
    #     sleep(1)
    #     self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
    #     self.io.set_five_door_sts(Door.close)
    #     sleep(1.5)
    #     self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
    #     self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("Conv下切Inactive,控制照脚灯点亮,外部闭锁")
    @pytest.mark.full
    def test_caseid_1991983(self):
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(.3)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.Telm)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("D挡切P挡等1分钟,控制照脚灯点亮,外部闭锁")
    @pytest.mark.full
    def test_caseid_1991982(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(61)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(.3)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("大屏切常关,控制照脚灯点亮,外部闭锁")
    @pytest.mark.full
    def test_caseid_1991968(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(.3)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("大屏切常关,控制照脚灯点亮,断开节电继电器")
    @pytest.mark.full
    def test_caseid_1991967(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(360)
        try:
            self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
        except:
            logger.info("节电继电器已断开")
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    # ------------------------------灭-----亮----------------------------------------
    @allure.title("P挡切D挡,控制照脚灯点亮,大屏点击常开")
    @pytest.mark.full
    def test_caseid_1991966(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("Crash进Normal,控制照脚灯点亮,大屏点击常开")
    @pytest.mark.full
    def test_caseid_1991965(self):
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("Conv下切Inactive,控制照脚灯点亮,大屏点击常开")
    @pytest.mark.full
    def test_caseid_1992029(self):
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("D挡切P挡等1分钟,控制照脚灯点亮,大屏点击常开")
    @pytest.mark.full
    def test_caseid_1992017(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(61)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("P挡切R挡,控制照脚灯点亮,R挡切P挡")
    @pytest.mark.full
    def test_caseid_1992016(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(2)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("Crash进Normal,控制照脚灯点亮,开门")
    @pytest.mark.full
    def test_caseid_1992015(self):
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.io.set_door(Drvr=Door.open)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("Conv下切Inactive,控制照脚灯点亮,闭锁、解锁")
    @pytest.mark.full
    def test_caseid_119053(self):
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.io.set_door(Drvr=Door.open)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("R挡切P挡等1分钟,控制照脚灯点亮,开门")
    @pytest.mark.full
    def test_caseid_119052(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(61)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.io.set_door(Drvr=Door.open)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("大屏点击常关,控制照脚灯点亮,大屏点击常开")
    @pytest.mark.full
    def test_caseid_119050(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("大屏点击常关,控制照脚灯点亮,大屏点击自动,D挡切P挡")
    @pytest.mark.full
    def test_caseid_1992432(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("大屏点击常关,控制照脚灯点亮,大屏点击自动,开门")
    @pytest.mark.full
    def test_caseid_1992431(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(Drvr=Door.open)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("大屏点击常关,控制照脚灯点亮,大屏点击自动,闭锁、解锁")
    @pytest.mark.full
    def test_caseid_1992433(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    # ——————————————————————————————亮————亮————————————————————————————

    @allure.title("D挡切P挡-----控制照脚灯熄灭-----大屏点击常开")
    @pytest.mark.full
    def test_caseid_1992474(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("开门-----控制照脚灯熄灭-----大屏点击常开")
    @pytest.mark.full
    def test_caseid_1992471(self):
        self.io.set_door(Drvr=Door.open)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("解锁-----控制照脚灯熄灭-----大屏点击常关")
    @pytest.mark.full
    def test_caseid_1992469(self):
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("大屏点击常开-----控制照脚灯熄灭-----大屏点击自动,R挡切P挡")
    @pytest.mark.full
    def test_caseid_119048(self):
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1.5)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("大屏点击常开-----控制照脚灯熄灭-----大屏点击自动，开门")
    @pytest.mark.full
    def test_caseid_1999121(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.io.set_door(Drvr=Door.open)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("大屏点击常开-----控制照脚灯熄灭-----大屏点击自动，闭锁、解锁")
    @pytest.mark.full
    def test_caseid_1999122(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("D挡切P挡-----控制照脚灯熄灭-----等1分钟")
    @pytest.mark.full
    def test_caseid_1992434(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        sleep(61)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("开门-----控制照脚灯熄灭-----Conv下切Inactive")
    @pytest.mark.full
    def test_caseid_1992488(self):
        self.io.set_door(Drvr=Door.open)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("闭锁、解锁-----控制照脚灯熄灭-----P挡切R挡")
    @pytest.mark.full
    def test_caseid_1999123(self):
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("D挡切P挡-----控制照脚灯熄灭-----外部闭锁")
    @pytest.mark.full
    def test_caseid_1992481(self):
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(1.5)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("开门-----控制照脚灯熄灭-----外部闭锁")
    @pytest.mark.full
    def test_caseid_1992480(self):
        self.io.set_door(Drvr=Door.open)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("开门-----控制照脚灯熄灭-----断开节电继电器")
    @pytest.mark.full
    def test_caseid_1992479(self):
        self.io.set_door(Drvr=Door.open)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(360)
        try:
            self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
        except:
            logger.info("节电继电器已断开")
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("R挡切P挡-----控制照脚灯熄灭-----大屏点击常关")
    @pytest.mark.full
    def test_caseid_1999124(self):
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1.5)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("大屏点击常开-----控制照脚灯熄灭-----外部闭锁")
    @pytest.mark.full
    def test_caseid_119011(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        sleep(0.3)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("大屏点击常开-----控制照脚灯熄灭-----断开节点继电器")
    @pytest.mark.full
    def test_caseid_119009(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        sleep(0.3)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(360)
        try:
            self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
        except:
            logger.info("节电继电器已断开")
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("大屏点击常开-----控制照脚灯熄灭-----大屏点击常关")
    @pytest.mark.full
    def test_caseid_1978060(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        
    @allure.title("内灯自动,解闭锁点亮内灯,控制照脚灯熄灭,P挡切D挡")
    @pytest.mark.full
    def test_caseid_1992486(self):
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(0.3)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)

