#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_Intrlight_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2023/12/7 11:30
@Description : BGM车控车设迎宾灯
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
        self.io.set_pwm(io_signal="pwm_crash", freq=10, duty=50)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE, time_wait=1)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(0.5)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,
            vehmtnst=VehMtnSts.StandStillVal3
        )
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode(wait_time=2)
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
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
        )
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

    # ——————————————————————————————————————————Courtesy————————————————————————————————————————

    @allure.title("阅读灯On_切为未锁定")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "lock_source",
        [LockSource.NFC, LockSource.HMI, LockSource.Telm, LockSource.KV_PEPS],
        ids=['1991386', '1991377', '1991381', '1991383']
    )
    def test_intrlight_ctrl_unlock_caseid_(self, lock_source):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, doors_sts=Door.close
        )
        self.soa.hmi_set_intr_light_mode()
        self.bus_comm.set_night_mode()
        self.io.set_five_door_sts(Door.close)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=lock_source)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=lock_source)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("阅读灯On_normal_inactive_RKE解锁")
    @pytest.mark.smoke
    @pytest.mark.add1
    def test_intrlight_ctrl_caseid_1991375(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, doors_sts=Door.close
        )
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)
        sleep(1)
        self.bus_comm.check_singal("CEM_LIN3", "CemCem_Lin3Fr05", "IntrLiGen2RoofDimSpeed", 0)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Courtesy_锁状态从locked切为unlocked_Keyls")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991376(self):
        self.mix.set_usage_mode(
            usage_mode=UsageMode.INACTIVE
        )
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.soa.hmi_set_intr_light_mode()
        sleep(1)
        self.bus_comm.set_singal("infocanfd", "BgmInfoCanFdDevFr03", "KeyReadStsToLockgBLEKey0", 2)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2.5)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.MovgOut)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        # self.bus_comm.set_singal("infocanfd", "BgmInfoCanFdDevFr03", "KeyReadStsToLockgBLEKey0", 2)
        self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Courtesy_锁状态从locked切为unlocked_InsOth")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991385(self):
        self.sd_tester.write_ccp(ccp={10: 0x02})
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.get_internal_light_mode(LightMode.Auto)
        sleep(1)
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.Set)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.set_gear_pos(Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(Gear.Park)
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Courtesy_锁状态从locked切为unlocked_Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991382(self):
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Crash, timeout=5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("阅读灯unknow_day_normal_inactive_RKE解锁")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1991556(self):
        self.bus_comm.set_day_mode()
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(3)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, doors_sts=Door.close
        )
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("day_Unknow_锁状态从locked切为unlocked_NFC")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1991557(self):
        self.bus_comm.set_day_mode()
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(3)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, doors_sts=Door.close
        )
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.RKE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("重启bgm后内灯模式记忆On")
    @pytest.mark.smoke
    @pytest.mark.nvm
    def test_intrlight_ctrl_caseid_1985677(self):
        self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
        self.soa.get_internal_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        logger.info("===================开始掉电======================")
        self.io.io_reset_bgm(times=1)
        sleep(25)
        self.soa.get_internal_light_mode(LightMode.On)

    @allure.title("重启bgm后内灯模式记忆Auto")
    @pytest.mark.smoke
    @pytest.mark.nvm
    def test_intrlight_ctrl_caseid_1993305(self):
        self.io.io_reset_bgm(times=1)
        sleep(25)
        self.soa.get_internal_light_mode(LightMode.Auto)

    @allure.title("Normal_Convenience开启主驾驶门可以打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_118111(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, veh_spd=5)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3.5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )

    @allure.title("Normal_Convenience开启副驾门可以打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980963(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, veh_spd=0.1)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(3.5)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )

    @allure.title("Normal_Convenience开启左后门可以打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980964(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, veh_spd=0.1)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(0.5)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )

    @allure.title("Normal_Convenience_车速等于5km/h_开启右后门可以打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980965(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, veh_spd=5)
        try:
            self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, timeout=3)
        except:
            self.mix.ctrl_lock(LockCmd.UnLock, LockSource.NFC)
            sleep(0.5)
        with allure.step("设置内灯模式Off"):
            self.soa.hmi_set_intr_light_mode(LightMode.Off)
        with allure.step("设置内灯模式Auto"):
            self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(2)
        with allure.step("后中占座"):
            self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
            sleep(3)
        self.io.set_five_door_sts(Door.close)
        sleep(0.5)
        with allure.step("开右后门"):
            self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("下切abandoned阅读灯熄灭")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979650(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, veh_spd=0.1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(2)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(3)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(10)
        self.bus_comm.check_lin_bus_sts(lin_channel=LinChannel.LIN3, sts=BusSendSts.Sleep)

    # @allure.title("阅读灯Courtesy下切abandoned再切回Conv")
    # @pytest.mark.smoke
    # def test_intrlight_ctrl_caseid_AAA(self):
    #     """@bug"""
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, veh_spd=0.1)
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     sleep(0.5)
    #     self.soa.hmi_set_intr_light_mode(LightMode.Auto)
    #     sleep(0.5)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
    #     sleep(0.5)
    #     self.io.set_five_door_sts(Door.close)
    #     sleep(0.5)
    #     self.io.set_door(RiRe=Door.open)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
    #     self.io.set_door(RiRe=Door.close)
    #     # self.mix.set_usage_mode(UsageMode.ABANDONED)
    #     sleep(360)
    #     try:
    #         self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 1)
    #         self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
    #     except:
    #         logger.info("节电继电器还没置1")
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("内灯挡位记忆_休眠唤醒_ForceOn")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1987108(self):
        self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
        sleep(.1)
        self.soa.get_internal_light_mode(LightMode.On)
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(.2)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOn)

    @allure.title("内灯挡位记忆_NFC闭锁未休眠_ForceOn")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1987105(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(2)
        self.io.set_five_door_sts(Door.open)
        sleep(1)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
        self.soa.get_internal_light_mode(LightMode.On)
        self.io.set_five_door_sts(Door.close)
        sleep(5)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOn)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOn)

    @allure.title("内灯挡位记忆_休眠唤醒_AllOff")
    @pytest.mark.smoke
    @pytest.mark.notready
    def test_intrlight_ctrl_caseid_1987106(self):
        self.soa.hmi_set_intr_light_mode(mode=LightMode.Off)
        self.soa.get_internal_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.AllOff)
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.AllOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.AllOff)

    @allure.title("内灯挡位记忆_NFC闭锁未休眠_AllOff")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1987103(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(mode=LightMode.Off)
        self.soa.get_internal_light_mode(LightMode.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(1)
        self.soa.get_internal_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.AllOff)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.AllOff)

    # @allure.title("内灯挡位记忆_休眠唤醒_Auto_NFC解锁")
    # def test_intrlight_ctrl_caseid_1991548(self):
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     sleep(5)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     sleep(1)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
    #     sleep(2)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
    #     self.mix.network_sleep()
    #     sleep(5)
    #     # self.tsp.rvc_ac_control()
    #     # self.bus_comm.resume_bus_send("backbonefr")
    #     self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)  # 和远控唤醒的区别
    #     # self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
    #     sleep(5)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("day内灯挡位记忆_闭锁休眠唤醒_Auto")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991549(self):
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.bus_comm.wakeup_lin1()
        sleep(1)
        self.bus_comm.set_day_mode()
        sleep(3)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.Telm)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    @allure.title("内灯挡位记忆_闭锁休眠_远控唤醒_Auto")
    @pytest.mark.add
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1987107(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(1)
        self.io.set_door(Drvr=Door.close)
        self.mix.network_sleep_unlock()
        sleep(5)
        self.tsp.rvc_ac_control()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_FLEXRAY)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)

    @allure.title("内灯挡位记忆_NFC闭锁未休眠_Courtesy")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1987104(self):
        self.bus_comm.set_gear_pos(Gear.Park)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(10)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(1)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("内灯挡位记忆_NFC闭锁未休眠_Courtesy_day")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1987104_day_nfc(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        sleep(3)
        self.soa.get_and_event_check_day_and_night_sts(sts=1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(1)
        self.soa.get_internal_light_mode(LightMode.Auto)
        try:
            self.bus_comm.check_lin_bus_sts(LinChannel.LIN1, BusSendSts.Awakeup)
            self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Awakeup)
            self.soa.get_and_event_check_day_and_night_sts(sts=1)
        except:
            logger.info("LIN状态或白天黑夜模式不满足")
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    #————————————————————————————————————————————未闭锁休眠用例需要修改————————————————————————————————————

    # @allure.title("内灯挡位记忆_开门不闭锁休眠唤醒_AllOff")
    # @pytest.mark.full
    # def test_intrlight_ctrl_caseid_1991546(self):
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     self.io.set_door(Pass=Door.open)
    #     self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
    #     sleep(600)
    #     self.io.set_door(Drvr=Door.open)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    # @allure.title("内灯挡位记忆_未闭锁_休眠_远控唤醒_Auto")
    # def test_intrlight_ctrl_caseid_1991574(self):
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     sleep(5)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     sleep(1)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     self.mix.network_sleep()
    #     sleep(5)
    #     # self.tsp.rvc_ac_control()
    #     # self.bus_comm.resume_bus_send("backbonefr")
    #     self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)  # 和远控唤醒的区别
    #     self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
    #     sleep(2)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)
    #     self.io.set_door(Drvr=Door.open)
    #     sleep(0.1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)
    #     # self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
    #     # self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
    #
    # @allure.title("内灯挡位记忆_未闭锁_休眠_寻车唤醒_Auto")
    # def test_intrlight_ctrl_caseid_1991573(self):
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     sleep(5)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     sleep(1)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     self.mix.network_sleep(door_lock_sts=3)
    #     sleep(5)
    #     self.tsp.rvc_find_vehicle()
    #     # self.bus_comm.resume_bus_send("backbonefr")
    #     self.bus_comm.resume_all_bus_send()
    #     self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)  # 和远控唤醒的区别
    #     self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
    #     sleep(2)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)
    #     self.io.set_door(Drvr=Door.open)
    #     sleep(0.1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)
    #
    # @allure.title("内灯挡位记忆_未闭锁_休眠_寻车唤醒_Auto")
    # def test_intrlight_ctrl_caseid_1991573(self):
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     sleep(5)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     sleep(1)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     self.mix.network_sleep(door_lock_sts=3)
    #     sleep(5)
    #     self.tsp.rvc_find_vehicle()
    #     sleep(2)
    #     self.bus_comm.resume_bus_send("backbonefr")
    #     # self.bus_comm.resume_all_bus_send()
    #     # self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)  # 和远控唤醒的区别
    #     sleep(2)
    #     # self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)
    #     self.io.set_door(Drvr=Door.open)
    #     sleep(0.1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)
    #     self.io.set_door(Drvr=Door.close)
    #     sleep(0.1)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
    #
    # @allure.title("内灯挡位记忆_未闭锁_休眠_远控唤醒_On")
    # def test_intrlight_ctrl_caseid_1992585(self):
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     sleep(5)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
    #     sleep(1)
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
    #     self.soa.get_internal_light_mode(LightMode.On)
    #     self.mix.network_sleep(lock_sts=1)
    #     sleep(5)
    #     self.tsp.rvc_ac_control()
    #     self.bus_comm.resume_bus_send("backbonefr")
    #     # self.bus_comm.resume_all_bus_send()
    #     # self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)  # 和远控唤醒的区别
    #     self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
    #     sleep(2)
    #     self.soa.get_internal_light_mode(LightMode.On)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOn)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
    #
    # @allure.title("内灯挡位记忆_开主驾门休眠_远控唤醒_Auto")
    # def test_intrlight_ctrl_caseid_1991575(self):
    #     self.soa.hmi_set_intr_light_mode(LightMode.Off)
    #     sleep(5)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     sleep(1)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     self.mix.network_sleep(door_lock_sts=2)
    #     sleep(5)
    #     self.tsp.rvc_find_vehicle()
    #     # self.bus_comm.resume_bus_send("backbonefr")
    #     self.bus_comm.resume_all_bus_send()
    #     self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)  # 和远控唤醒的区别
    #     self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
    #     sleep(2)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)
    #     self.io.set_door(Drvr=Door.open)
    #     sleep(0.1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)

    #————————————————————————————————————上述为未闭锁休眠脚本————————————————————————————————————————

    # @allure.title("内灯挡位记忆_闭锁休眠_crash唤醒_Auto")
    # def test_intrlight_ctrl_caseid_1991552(self):
    #     """
    #     脚本问题
    #     @return:
    #     """
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     sleep(1)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
    #     sleep(2)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
    #     self.mix.network_sleep()
    #     sleep(5)
    #     # self.bus_comm.set_singal("InfoCANFD", "BgmInfoCanFdDevFr02", "CarModChgReq", 3)
    #     self.mix.set_car_mode(CarMode.CRASH)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOn)

    @allure.title("内灯挡位记忆_HMI闭锁未休眠_Courtesy_day")
    def test_intrlight_ctrl_caseid_1987104_day_hmi(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
        )
        self.bus_comm.set_day_mode()
        sleep(3)
        self.soa.get_and_event_check_day_and_night_sts(sts=1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        sleep(3)
        # self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(1)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    @allure.title("阅读灯On_开主驾门_车速等于0.1km/h_Normal_Inactive")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980951(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, veh_spd=0.1)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3.5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("阅读灯On_开副驾门_车速等于5km/h_Normal_Active")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980942(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, veh_spd=5)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3.5)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )

    @allure.title("Courtesy_占用后排中间座位,从N挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1992532(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Carmode_内灯可用")
    @pytest.mark.full
    @pytest.mark.parametrize("carmode", [CarMode.NORMAL, CarMode.CRASH, CarMode.DYNO])
    def test_intrlight_ctrl_caseid_1988661(self, carmode):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=carmode)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("Carmode_内灯不可用")
    @pytest.mark.full
    @pytest.mark.parametrize("carmode", [CarMode.TRANSPORT, CarMode.FACTORY])
    def test_intrlight_ctrl_caseid_1988660(self, carmode):
        """
        transport、factory模式内灯可控，偏差接受
        @param carmode:
        @return:
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=carmode)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("Courtesy_占用左后座位_从R挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991390(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_占用后排中间座位，从D挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991391(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_占用右后座位，从D挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991389(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_占用副驾座位，从R挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991388(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_占用主驾座位，从D挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991387(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_占用后排中间座位，从N挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1992532(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_占用主驾座位,从N挡切到P挡")
    @pytest.mark.full
    @pytest.mark.notready
    def test_intrlight_ctrl_caseid_1992531(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_占用主驾座位，从N挡切到P挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1992531(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_HMI解锁")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_118832(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("阅读灯Courtesy_不占座_切到P挡")
    @pytest.mark.full
    @pytest.mark.parametrize(
        "um, gear",
        [[UsageMode.CONVENIENCE, Gear.Drv], [UsageMode.CONVENIENCE, Gear.Rvs],
         [UsageMode.DRIVING, Gear.Drv], [UsageMode.DRIVING, Gear.Rvs]]
    )
    def test_intrlight_ctrl_caseid_118833(self, um, gear):
        self.mix.set_common_precontion(usage_mode=um, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=gear)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("Manual_占用任意座位，将挡位从P切到D/R")
    @pytest.mark.full
    @pytest.mark.add
    def test_intrlight_ctrl_caseid_118836(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.io.set_door(Drvr=Door.close)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Normal_inactive开启主驾驶门可以打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_asd(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, veh_spd=0.1)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        # self.bus_comm.set_day_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3.5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("crash切On切Normal_manual")
    @pytest.mark.sanity
    @pytest.mark.add1
    def test_intrlight_ctrl_caseid_1989078(self):
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Courtesy_锁状态从TrUnlckd切为unlocked")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991453(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.soa.hmi_set_tailgate_mode(cmd=TailGateMode.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt
        )
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("阅读灯不点亮_开副驾门_车速等于5.1km/h_Normal_Driving")
    @pytest.mark.smoke
    @pytest.mark.add1
    def test_intrlight_ctrl_caseid_1991451(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, veh_spd=5.1)
        sleep(1)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        sleep(.3)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("day_unknow_占用主驾座位_从D挡切到P挡")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1991559(self):
        self.bus_comm.set_day_mode()
        sleep(3)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    @allure.title("Conv_白天状态R挡切到P挡无法切到courtesy")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_daymode_RP_conv(self):
        self.bus_comm.set_day_mode()
        sleep(3)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    @allure.title("解锁开阅读灯_day")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_daymode_unlock(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_day_mode()
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(2)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    @allure.title("day_Normal_Convenience开启主驾驶门不能打开阅读灯")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_daymode_open(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, veh_spd=0.1)
        self.bus_comm.set_day_mode()
        sleep(2)
        self.soa.hmi_set_intr_light_mode()
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3.5)
        self.io.set_door(Drvr=Door.open)
        sleep(2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    # ——————————————————————————————————————————Manual————————————————————————————————————————

    @allure.title("阅读灯manual_Convenience_Normal下切inactive")
    @pytest.mark.full
    @pytest.mark.add1
    def test_intrlight_ctrl_caseid_118837(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal3
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.set_night_mode()
        self.io.set_five_door_sts(Door.close)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(1)
        self.bus_comm.check_intr_light_read_lamp_req(zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        sleep(2)
        self.bus_comm.check_singal("CEM_LIN3", "CemCem_Lin3Fr05", "IntrLiGen2RoofDimSpeed", 0)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("crash持续25min迎宾灯状态转manual")
    @pytest.mark.full
    @pytest.mark.notready
    def test_intrlight_ctrl_caseid_TmrForCrash1991890(self):
        self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(300)
        self.bus_comm.wakeup_lin5()
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(300)
        self.bus_comm.wakeup_lin5()
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(300)
        self.bus_comm.wakeup_lin5()
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(300)
        self.bus_comm.wakeup_lin5()
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(299)
        self.bus_comm.wakeup_lin5()
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
    #
    # @allure.title("Manual_inactive_crash_TmrForCrash")
    # @pytest.mark.full
    # def test_intrlight_ctrl_caseid_TmrForCrash118834(self):
    #     self.mix.set_usage_mode(UsageMode.INACTIVE)
    #     sleep(1)
    #     self.mix.set_common_precontion(car_mode=CarMode.CRASH, usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
    #     sleep(1499)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
    #     sleep(5)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("阅读灯manual_convenience_crash切Normal")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1979648(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH
        )
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
        )
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_dyno_convenience下切Inactive")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1991860(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO, veh_spd=0.1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_five_door_sts(Door.close)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(2)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(3)
        self.io.set_door(RiRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("迎宾灯Manual_无占座关闭最后一扇门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_118838(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        sleep(1)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        sleep(1)
        self.io.set_door(Drvr=Door.close)
        sleep(181)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Manual
        )

    @allure.title("Manual_convenience后排中间占座关闭主驾驶门")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991862(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        sleep(1)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(1)
        self.io.set_door(Drvr=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Manual_convenience后排中间占座关闭主驾驶门")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991399(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        self.io.set_door(LeRe=Door.open)
        sleep(1)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(1)
        self.io.set_door(Drvr=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("迎宾灯Manual_占座关闭最后一扇门")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_118838A(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_night_mode()
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        sleep(1)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.Pres)
        sleep(1)
        self.io.set_door(Drvr=Door.close)
        sleep(181)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Courtesy
        )

    @allure.title("阅读灯manual_占用主驾座位_从P挡切到D挡")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1980960(self):
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(3)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    # ——————————————————————————————————————————AllOFF————————————————————————————————————————

    @allure.title("阅读灯Off CDC设置内灯模式为Off")
    @pytest.mark.full
    @pytest.mark.add1
    def test_intrlight_ctrl_caseid_118885(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_singal("CEM_LIN3", "CemCem_Lin3Fr05", "IntrLiGen2RoofDimSpeed", 1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    @allure.title("AllOff_normal_convenience_CDC设置内灯为Off_ReadLiSts=1")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991948(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_normal_active_CDC设置内灯为Off_ReadLiSts=1")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991949(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_dyno_convenience_CDC设置内灯为Off_ReadLiSts=1")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991950(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_dyno_driving_CDC设置内灯为Off_ReadLiSts=1")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991951(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_dyno_active_CDC设置内灯为Off_ReadLiSts=1")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991952(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_normal_driving_CDC设置内灯为Off_ReadLiSts=1")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991953(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_normal_driving_CDC设置内灯为Off")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991959(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_normal_active_CDC设置内灯为Off")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991955(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_normal_convenience_CDC设置内灯为Off")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991954(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_dyno_active_CDC设置内灯为Off")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991958(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_dyno_driving_CDC设置内灯为Off")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991957(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    @allure.title("AllOff_dyno_convenience_CDC设置内灯为Off")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991956(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )

    # ——————————————————————————————————————————ForceOn————————————————————————————————————————

    @allure.title("ForceOn_normal_convenience_CDC设置内灯为On")
    @pytest.mark.smoke
    @pytest.mark.add1
    def test_intrlight_ctrl_caseid_119055(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
        )
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_singal("CEM_LIN3", "CemCem_Lin3Fr05", "IntrLiGen2RoofDimSpeed", 1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        sleep(0.15)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("阅读灯On_normal_driving_carmode切为Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1960164(self):
        self.soa.hmi_set_intr_light_mode()
        self.mix.set_common_precontion(
            usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH
        )
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("阅读灯On_normal_active_carmode切为Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_118864(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH
        )
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("阅读灯On_normal_convenience_carmode切为Crash")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1960163(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH
        )
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("阅读灯On_dyno_active_carmode切为Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1979661(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH
        )
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_factory_convenience切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991911(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH
        )
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_normal_abandoned切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991919(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH
        )
        sleep(2)
        self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Sleep)

    @allure.title("ForceOn_factory_convenience_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_transport_1991895(self):
        self.mix.set_common_precontion(car_mode=CarMode.FACTORY, usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
        self.soa.get_internal_light_mode(LightMode.On)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOn)

    # @allure.title("normal下切transport_内灯On状态记忆")
    # def test_intrlight_ctrl_caseid_transport_normal_to_transport_on(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
    #     sleep(1)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
    #     sleep(1)
    #     self.soa.get_internal_light_mode(LightMode.On)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    # @allure.title("factory_forceOn无法点亮迎宾灯")
    # def test_intrlight_ctrl_caseid_factory_forceOn(self):
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Off)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
    #     sleep(0.5)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
    #     sleep(1)
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.AllOff)

    # @allure.title("normal下切factory_内灯On状态记忆")
    # def test_intrlight_ctrl_caseid_transport_normal_to_factory_on(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.On)
    #     sleep(1)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
    #     sleep(1)
    #     self.soa.get_internal_light_mode(LightMode.On)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    # @allure.title("normal下切factory_内灯Courtesy状态记忆")
    # def test_intrlight_ctrl_caseid_transport_normal_to_factory_courtesy(self):
    #     self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_night_mode()
    #     self.soa.hmi_set_intr_light_mode(mode=LightMode.Auto)
    #     sleep(1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Drv)
    #     sleep(1)
    #     self.bus_comm.set_gear_pos(gear=Gear.Park)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
    #     sleep(1)
    #     self.soa.get_internal_light_mode(LightMode.Auto)
    #     sleep(1)
    #     self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Unknow)

    @allure.title("ForceOn_normal_convenience_CDC设置内灯为On_ReadLiSts=0")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1991924(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_normal_convenience切Crash_ReadLiSts=0")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991932(self):
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_normal_abandoned切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991934(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Sleep)

    @allure.title("ForceOn_normal_inactive切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991937(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_normal_driving切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991935(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_normal_driving_CDC设置内灯为On_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991929(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_normal_active切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991923(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_abandoned切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991930(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        # self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Sleep)

    # ——————————————————————————————————————————ForceOff————————————————————————————————————————
    @allure.title("Courtesy_Apprch上锁")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991405(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set_singal("bodycan", "PotBodyFr02", "TrOpenerSts", 1)
        self.soa.hmi_event_check_tailgate_movests(MoveSts.Closed)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)
        sleep(3)  # 等待前置条件生效
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("Courtesy_KeyIs上锁")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991401(self):
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        # self.bus_comm.check_turn_indicate_lamp_req(IndcrSts.Off)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("Courtesy_keyRem上锁")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991400(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("Courtesy_车速上锁_SpdAut")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991378(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.bus_comm.set_vehspd(value=3.95)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.bus_comm.set_vehspd(value=0)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("NFC关锁阅读灯forceoff")
    @pytest.mark.full
    @pytest.mark.add1
    def test_intrlight_ctrl_caseid_1991407(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_singal("CEM_LIN3", "CemCem_Lin3Fr05", "IntrLiGen2RoofDimSpeed", 1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("OutsOth关锁阅读灯forceoff")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991406(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.io.hazard_light_close()
        self.mix.set_lock_unlock_visible_feedback_precondition(LockState.Lock)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.LockCompleteArm, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.OutsOth)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("ForceOff_通过Telm方式闭锁")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991403(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("ForceOff_通过TmrAut方式闭锁")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991402(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL,
                                       vehmtnst=VehMtnSts.StandStillVal2)
        self.io.set_hood_sts(HoodSts.Close)

        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Talematics, time_wait=0.1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(30)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("ForceOff_RlyPwrDistbnCmd1WdPreBattSaveCmd=1")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_118883(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(360)
        try:
            self.bus_comm.check_singal("CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
        except:
            logger.info("节电继电器已置1")
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("ForceOn_通过IntrSwt方式闭锁迎宾灯不熄灭")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991943(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_通过InsOth方式闭锁迎宾灯不熄灭")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991940(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.5)
        self.bus_comm.check_singal("infocanfd", "BgmInfoCanFdFr18", "PrkgCmftModTiCtrl", 0)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.APA)
        self.bus_comm.check_central_lock_sts(
            exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.InsOth, timeout=3
        )
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    # ——————————————————————————————————————————调试————————————————————————————————————————

    @allure.title("阅读灯manual_照脚灯慢速熄灭")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991430(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(.1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("阅读灯manual_占用左后座位_P挡切到R挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980961(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(.1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("阅读灯manual_占用右后座位，从P挡切到D挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1980958(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(.1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("阅读灯manual_不占座_P挡切到R挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991887(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(.1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(0.1)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("阅读灯manual_不占座_P挡切到D挡")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991886(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(.1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        sleep(0.1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("内灯模式On诊断复位阅读灯点亮")
    @pytest.mark.full
    @pytest.mark.add
    def test_intrlight_ctrl_caseid_1980957(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.soa.get_internal_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.sd_tester.send_data("1181")
        sleep(25)
        self.soa.get_internal_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("内灯模式Auto诊断复位阅读灯点亮")
    @pytest.mark.sanity
    @pytest.mark.add
    def test_intrlight_ctrl_caseid_1984483(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.sd_tester.send_data("1181")
        sleep(25)
        self.soa.get_internal_light_mode(LightMode.Auto)

    @allure.title("阅读灯manual_driving_normal下切inactive")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1979894(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal3
        )
        sleep(1)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        sleep(.1)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.HMI)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("阅读灯ForceOn_照脚灯快速点亮")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1989087(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("阅读灯ForceOff_照脚灯快速熄灭")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991428(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)

    @allure.title("阅读灯courtesy_照脚灯慢速点亮")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991429(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)

    @allure.title("阅读灯AllOff_照脚灯快速熄灭")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991427(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
        )
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    @allure.title("transport模式无法切到courtesy")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991449(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT, veh_spd=0)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(LeRe=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("transport_forceOn迎宾灯无法点亮")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1992534(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT, veh_spd=0)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("transport_ForceOn_CDC设置内灯为On_不点亮")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991371(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT, veh_spd=0)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    @allure.title("transport_AllOff_CDC设置内灯模式为Off")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1992588(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT, veh_spd=0)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    @allure.title("Manual_normal_driving下切Inactive")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991861(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL, veh_spd=0
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_normal_active下切Inactive")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991392(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL, veh_spd=0
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_dyno_driving下切Inactive")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991859(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO, veh_spd=0
        )
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_dyno_convenience下切Inactive")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991860(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO, veh_spd=0
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_dyno_active下切Inactive")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991858(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO, veh_spd=0
        )
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_crash_inactive切normal")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991888(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH, veh_spd=0
        )
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_crash_active切normal")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991889(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH, veh_spd=0
        )
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_convenience无占座关闭右后门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991398(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(1)
        self.io.set_door(RiRe=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_convenience无占座关闭副驾驶门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991396(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(1)
        self.io.set_door(Pass=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("Manual_convenience左后占座关闭左后门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991863(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.io.set_door(LeRe=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        self.io.set_door(LeRe=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("内灯挡位记忆_等待节电继电器断开forceoff")
    def test_intrlight_ctrl_caseid_1987112(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(0.5)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(361)
        try:
            self.bus_comm.check_singal(
                "CEM_LIN4", "CemCem_Lin4Fr02", "RlyPwrDistbnCmd1WdPreBattSaveCmd", 0)
        except:
            logger.info("节电继电器已断开")
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("Manual_convenience后排中间占座关闭主驾驶门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991862(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        self.io.set_door(Drvr=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Manual_convenience右后占座关闭右后门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991864(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.io.set_door(RiRe=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.io.set_door(RiRe=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Manual_convenience副驾占座关闭副驾驶门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991865(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.io.set_door(Pass=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.io.set_door(Pass=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Manual_convenience主驾占座关闭主驾驶门")
    @pytest.mark.full
    @pytest.mark.add
    def test_intrlight_ctrl_caseid_1991866(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.io.set_door(Drvr=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @allure.title("Manual_active无占座关闭左后门")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991397(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.io.set_door(LeRe=Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.io.set_door(LeRe=Door.close)
        sleep(181)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)

    @allure.title("ForceOn_通过SpdAut方式闭锁迎宾灯不熄灭")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991940(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.mix.set_common_precontion(UsageMode.DRIVING)
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr02", "VehModMngtGlbSafe1UsgModSts", 13)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 3)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdBrkPedlPsd", 1)
        self.bus_comm.set_vehspd(value=1.95)
        self.io.driver_seat_present()
        self.bus_comm.check_singal("backbonefr", "CemBackBoneFr03", "DrvrPrsntStsDrvrPrsnt", 2)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.SpdAut)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_通过IntrSwt方式闭锁迎宾灯不熄灭")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991942(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.5)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_inactive切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991907(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_active切Crash")
    @pytest.mark.full
    @pytest.mark.add
    def test_intrlight_ctrl_caseid_1991905(self):
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_driving_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991896(self):
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_convenience_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991898(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_active_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991897(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_convenience切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991906(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_active切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991908(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_abandoned切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991904(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Sleep)

    @allure.title("ForceOn_normal_inactive切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991922(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_normal_driving切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991920(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_car_mode(CarMode.NORMAL)
        sleep(.1)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(.1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_normal_driving_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991902(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_normal_convenience切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991921(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_car_mode(CarMode.NORMAL)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_normal_active_CDC设置内灯为On_ReadLiSts=0")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991925(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_normal_active_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991903(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_factory_inactive切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991912(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH
        )
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_factory_active切Crash")
    @pytest.mark.sanity
    @pytest.mark.add
    def test_intrlight_ctrl_caseid_1991910(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH
        )
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_factory_driving_CDC设置内灯为On")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991893(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY
        )
        sleep(0.1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_factory_active切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991913(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH
        )
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_factory_active_CDC设置内灯为On")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991894(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY
        )
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY
        )
        sleep(0.1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_transport_inactive切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991907(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_factory_abandoned切Crash")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991909(self):
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        self.mix.set_car_mode(CarMode.FACTORY)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Sleep)

    @allure.title("ForceOn_dyno_inactive切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991933(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_inactive切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991917(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_dyno_driving切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991931(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_driving切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991915(self):
        self.mix.set_car_mode(CarMode.DYNO)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_dyno_driving_CDC设置内灯为On_ReadLiSts=0")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991927(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_driving_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991899(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_dyno_convenience切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991936(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_convenience切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991916(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_dyno_convenience_CDC设置内灯为On_ReadLiSts=0")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991926(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_convenience_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991901(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_dyno_active切Crash_ReadLiSts=0")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991938(self):
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.mix.set_car_mode(CarMode.DYNO)
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_active切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991918(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ACTIVE)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_dyno_active_CDC设置内灯为On_ReadLiSts=0")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1991928(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.AllOff
        )
        sleep(0.2)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.ForceOn
        )

    @allure.title("ForceOn_dyno_convenience_CDC设置内灯为On")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991900(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("ForceOn_dyno_abandoned切Crash_ReadLiSts=0")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_ReadLiSts1991930(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.set_singal("CEM_LIN3", "OhcCem_Lin3Fr01", "ReadLiStsFirstRowLe", 0)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Sleep)

    @allure.title("ForceOn_dyno_abandoned切Crash")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_1991914(self):
        self.mix.set_car_mode(CarMode.DYNO)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_car_mode(CarMode.CRASH)
        self.bus_comm.check_lin_bus_sts(LinChannel.LIN3, BusSendSts.Sleep)

    @allure.title("ForceOff_闭锁状态且信号满足固定值")
    @pytest.mark.sanity
    def test_intrlight_ctrl_caseid_118884(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOff)

    @allure.title("factory模式_开主驾门_车速5km/h_Convenience_无法切到courtesy")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1991450(self):
        self.mix.set_car_mode(CarMode.FACTORY)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, veh_spd=5)
        self.soa.hmi_set_intr_light_mode()
        self.io.set_five_door_sts(Door.close)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(3.5)
        self.io.set_door(Pass=Door.open)
        self.bus_comm.check_intr_light_read_lamp_req(
            zone=ReadLampZone.FrontLeft, sts=ReadLampSts.Unknow
        )

    @allure.title("factory_forceOn阅读灯不点亮")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1992533(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("factory_ForceOn_CDC设置内灯为On_不点亮")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1991370(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @allure.title("factory_AllOff_CDC设置内灯模式为Off")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1992589(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    @allure.title("day_unknow_开主驾门_车速5km/h_Normal_Convenience")
    @pytest.mark.smoke
    def test_intrlight_ctrl_caseid_1991558(self):
        self.bus_comm.set_day_mode()
        sleep(3)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL, veh_spd=5)
        with allure.step("设置内灯模式Off"):
            self.soa.hmi_set_intr_light_mode(LightMode.Off)
        with allure.step("设置内灯模式Auto"):
            self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(2)
        with allure.step("主驾占座"):
            self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
            sleep(3)
        sleep(0.5)
        with allure.step("主驾开门"):
            self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("Courtesy_锁状态从TrUnlckd切为unlocked_Keyls")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1992536(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Ble_Rke)
        sleep(0.1)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver, time_interval=0.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("Courtesy_锁状态从TrUnlckd切为unlocked_IntrSwt")
    @pytest.mark.full
    def test_intrlight_ctrl_caseid_1992537(self):
        """
        结果是courtesy
        @return:
        """
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        self.soa.hmi_set_tailgate_mode(cmd=TailGateMode.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("Courtesy_锁状态从TrUnlckd切unlocked_KeyRem")
    @pytest.mark.full
    @pytest.mark.manul
    def test_intrlight_ctrl_caseid_1992535(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.HMI)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.soa.hmi_set_tailgate_mode(cmd=TailGateMode.Open)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
        sleep(.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @allure.title("黑夜信号无效处理TwliBriRaw信号丢失")
    @pytest.mark.full
    def test_signal_lost_caseid_1991374(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.1)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.1)
        self.bus_comm.stop_send_pdu("cem_lin1", "RlsmCem_Lin1Fr01")
        sleep(5)
        self.io.set_door(Drvr=Door.open)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.resume_send_pdu("cem_lin1", "RlsmCem_Lin1Fr01")
        sleep(5)

    @allure.title("白天信号无效处理TwliBriRaw信号丢失")
    @pytest.mark.full
    def test_signal_lost_caseid_1992006(self):
        self.bus_comm.set_day_mode()
        sleep(3)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.1)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(0.1)
        self.bus_comm.stop_send_pdu("cem_lin1", "RlsmCem_Lin1Fr01")
        sleep(5)
        self.io.set_door(Drvr=Door.open)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.bus_comm.resume_send_pdu("cem_lin1", "RlsmCem_Lin1Fr01")
        sleep(5)

    @allure.title("挡位信号GearLvrIndcn丢失_内灯继续工作")
    @pytest.mark.full
    @pytest.mark.add1
    def test_signal_lost_caseid_1991408(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(0.1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.stop_send_pdu("propulsioncan", "EcmPropFr24")
        self.bus_comm.stop_send_pdu("chassiscan2", "EcmChas2Fr07")
        self.bus_comm.stop_send_pdu("backbonefr", "VddmBackBoneFr03")
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        sleep(0.1)
        self.bus_comm.resume_send_pdu("propulsioncan", "EcmPropFr24")
        self.bus_comm.resume_send_pdu("chassiscan2", "EcmChas2Fr07")
        self.bus_comm.resume_send_pdu("backbonefr", "VddmBackBoneFr03")
        sleep(10)

    @allure.title("副驾信号PassSeatSts丢失_内灯继续工作")
    @pytest.mark.full
    def test_signal_lost_caseid_1991409(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.stop_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.resume_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(5)

    @allure.title("左后座位信号SeatOccptAtRowSecLe丢失_内灯继续工作")
    @pytest.mark.full
    def test_signal_lost_caseid_1991410(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.stop_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.resume_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(5)

    @allure.title("右后座位信号SeatOccptAtRowSecRi丢失_内灯继续工作")
    @pytest.mark.full
    def test_signal_lost_caseid_1991411(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(0.1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.stop_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(10)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.resume_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(5)

    @allure.title("后排中间座位信号SeatOccptAtRowSecMid丢失_内灯继续工作")
    @pytest.mark.full
    def test_signal_lost_caseid_1991412(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)  
        sleep(0.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(0.1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.stop_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(10)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.bus_comm.resume_send_pdu("backbonefr", "SrsBackBoneFr04")
        sleep(5)

    @allure.title("白天黑夜模式")
    @pytest.mark.full
    def test_day_to_night_caseid_1989076(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
        )
        self.bus_comm.set_day_mode()
        sleep(2)
        self.soa.get_and_event_check_day_and_night_sts(sts=1)
        self.bus_comm.set_night_mode()
        sleep(2)
        self.soa.get_and_event_check_day_and_night_sts(sts=0)

    @allure.title("白天黑夜信号无效处理TwliBriRawQF != 3")
    @pytest.mark.full
    def test_invalid_day_to_night_caseid_1989077(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={352: 0x80}
        )
        self.bus_comm.set_day_mode()
        sleep(2.1)
        with allure.step("设置当前黑夜模式SUS QF1"):
            self.bus_comm.set_singal(bus="cem_lin1", msg="RlsmCem_Lin1Fr01", signal="TwliBriRawTwliBriRaw", value=0)
            self.bus_comm.set_singal(bus="cem_lin1", msg="RlsmCem_Lin1Fr01", signal="TwliBriRawQf", value=1)
        sleep(2)
        self.soa.get_and_event_check_day_and_night_sts(sts=1)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("day_内灯挡位记忆_开右后门休眠_开门唤醒_Auto")
    def test_caseid_1991578(self):
        self.bus_comm.set_day_mode()
        sleep(2.5)
        self.mix.network_sleep_unlock(unlock=True, door_open="rire")
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_FLDOOR_SW)
        sleep(5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @pytest.mark.longtime2
    @allure.title("day_内灯挡位记忆_关门不闭锁休眠_开门唤醒_Auto")
    def test_caseid_1991572(self):
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        self.bus_comm.set_day_mode()
        sleep(2.5)
        self.mix.network_sleep_unlock(unlock=True)
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_FLDOOR_SW)
        sleep(5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_关门不闭锁休眠_crash唤醒_Auto")
    def test_caseid_1991561(self):
        self.mix.network_sleep_unlock(unlock=True)
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_HAZARD)
        sleep(5)
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_关门不闭锁休眠_开门唤醒_Auto")
    def test_caseid_1991571(self):
        self.mix.network_sleep_unlock(unlock=True)
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_FLDOOR_SW)
        sleep(5)
        self.io.set_door(Door.open)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_关门不闭锁休眠_远控唤醒_Auto")
    def test_caseid_1991574(self):
        self.mix.network_sleep_unlock(unlock=True)
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_FLEXRAY)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_关门不闭锁休眠唤醒_AllOff")
    def test_caseid_1991545(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.mix.network_sleep_unlock(unlock=True)
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_关门不闭锁休眠唤醒_ForceOn")
    def test_caseid_1992584(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.mix.network_sleep_unlock(unlock=True)
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_开主驾门休眠_唤醒_Auto")
    def test_caseid_1991575(self):
        self.mix.network_sleep_unlock(unlock=True, door_open="drv")
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_开右后门休眠_开门唤醒_Auto")
    def test_caseid_1991577(self):
        self.mix.network_sleep_unlock(unlock=True, door_open="rire")
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_FLDOOR_SW)
        sleep(5)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_开左后门休眠_crash唤醒_Auto")
    def test_caseid_1991579(self):
        self.mix.network_sleep_unlock(unlock=True, door_open="lere")
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_HAZARD)
        sleep(5)
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_开门不闭锁休眠唤醒_AllOff")
    def test_caseid_1991546(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.mix.network_sleep_unlock(unlock=True, door_open="pass")
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_开门不闭锁休眠唤醒_On")
    def test_caseid_1992585(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.mix.network_sleep_unlock(unlock=True, door_open="pass")
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_闭锁休眠_crash唤醒_Auto")
    def test_caseid_1991552(self):
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_HAZARD)
        sleep(5)
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("内灯挡位记忆_闭锁休眠_NFC解锁唤醒_Auto")
    def test_caseid_1991548(self):
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.NFC)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)

    @pytest.mark.full
    @pytest.mark.notready
    def test_caseid_1991581(self):
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        self.bus_comm.send_approach_unlock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.Apprch)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    # def test_pwm(self):
        # self.io.set_pwm(io_signal="pwm_crash", freq=10, duty=50)
        # self.bus_comm.check_car_mode_status(CarMode.CRASH, car_mode_sub=1)
        # self.io.set_pwm(io_signal="pwm_crash", freq=10, duty=50)
        # self.sd_tester.send_data([0x22, 0x42, 0xFB])
        # self.io.set_pwm(io_signal="pwm_crash", freq=255, duty=50)
        # self.sd_tester.send_data([0x22, 0x42, 0xFB])
        # self.io.set_pwm(io_signal="pwm_crash", freq=10, duty=50)

    def test_rheostat_wheel_ctrl(self):
        self.soa.hmi_light_control(type=LightType.LightBackground, zone=LightZone.LightZoneAllOrSingle, mode=LightMode.On,
                                   brightness=12)
        self.soa.ck_s2s_event("LightService_client",
                               "Status",
                               {"sts": {"light": {"type": 23, "zoneId": 0}, "brightness": 12}})
        logger.info("=========================开始休眠===============================")
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(2)
        logger.info("=========================休眠结束===============================")
        self.soa.ck_s2s_event("LightService_client",
                               "Status",
                               {"sts": {"light": {"type": 23, "zoneId": 0}, "brightness": 12}})

    
