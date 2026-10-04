# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_footlight_22.py
@Time         :10/8/24 6:24 PM
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
                "WiperService_client",
                "SeatService_client",
                "KeyService_client",
                "VehicleModeService_client"
            ]
        )
        # self.io.io_reset_bgm(10)
        # sleep(35)

    def before_each_func(self, ecu):
        """
        解锁、Normal、Conv、关5门、夜晚、P挡、无占座
        @param ecu:
        @return:
        """
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE, time_wait=1)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.soa.set_and_cancel_auto_lock_settings(settings=Settings.CancelSet)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        # self.bus_comm.set_brake_pedal_sts(YesOrNo.No)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(.5)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
        sleep(1)

    def after_each_func(self, ecu):
        # self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.NFC, time_wait=1)
        sleep(1)


    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    # def get_left_footlight_sts(self, sts: FootLightSts, timeout: int = 5):
    #     prompt_info = f"===============>获取左照脚灯模式为: {sts.name}"
    #     with allure.step(prompt_info):
    #         logger.info(prompt_info)
    #         self.soa.send_request_and_ck_resp(
    #             partner_key="LightService_client",
    #             method_name="GetStatus",
    #             args={"lights": [{"type": 24, "zoneId": 1}]},
    #             ck_info={
    #                 "out":
    #                     [
    #                         {"light": {"type": 24, "zoneId": 1}, "sts": sts.value, "brightness": 0,
    #                          "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}
    #                     ]
    #             },
    #             timeout=timeout
    #         )
    #
    # def get_right_footlight_sts(self, sts: FootLightSts, timeout: int = 5):
    #     prompt_info = f"===============>获取右照脚灯模式为: {sts.name}"
    #     with allure.step(prompt_info):
    #         logger.info(prompt_info)
    #         self.soa.send_request_and_ck_resp(
    #             partner_key="LightService_client",
    #             method_name="GetStatus",
    #             args={"lights": [{"type": 24, "zoneId": 2}]},
    #             ck_info={
    #                 "out":
    #                     [
    #                         {"light": {"type": 24, "zoneId": 2}, "sts": sts.value, "brightness": 0,
    #                          "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}
    #                     ]
    #             },
    #             timeout=timeout
    #         )
    #
    # def get_footlight_sts(self, sts: FootLightSts, timeout: int = 5):
    #     prompt_info = f"===============>获取照脚灯模式为: {sts.name}"
    #     with allure.step(prompt_info):
    #         logger.info(prompt_info)
    #         self.soa.send_request_and_ck_resp(
    #             partner_key="LightService_client",
    #             method_name="GetStatus",
    #             args={"lights": [{"type": 24, "zoneId": 0}]},
    #             ck_info={
    #                 "out":
    #                     [
    #                         {"light": {"type": 24, "zoneId": 1}, "sts": sts.value, "brightness": 0,
    #                          "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}},
    #                         {"light": {"type": 24, "zoneId": 2}, "sts": sts.value, "brightness": 0,
    #                          "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}
    #                     ]
    #             },
    #             timeout=timeout
    #         )
    #
    # def check_left_footlight_inform(self, sts: FootLightSts, timeout: int = 5):
    #     prompt_info = f"===============>通知左照脚灯模式为: {sts.name}"
    #     with allure.step(prompt_info):
    #         logger.info(prompt_info)
    #         self.soa.ck_s2s_event(
    #             partner_key="LightService_client",
    #             interface_name="Status",
    #             ck_info={"sts": {"light": {"type": 24, "zoneId": 1}, "sts": sts.value}},
    #             timeout=timeout
    #         )
    #
    # def check_right_footlight_inform(self, sts: FootLightSts, timeout: int = 5):
    #     prompt_info = f"===============>通知右照脚灯模式为: {sts.name}"
    #     with allure.step(prompt_info):
    #         logger.info(prompt_info)
    #         self.soa.ck_s2s_event(
    #             partner_key="LightService_client",
    #             interface_name="Status",
    #             ck_info={"sts": {"light": {"type": 24, "zoneId": 2}, "sts": sts.value}},
    #             timeout=timeout
    #         )
    #
    # def set_footlight_sts(self, sts: OnOff):
    #     logger.info(f"============>设置照脚灯模式为: {sts.name}")
    #     if sts.value:
    #         self.soa.hmi_light_control(type=LightType.LightFoot, zone=LightZone.LightZoneAllOrSingle,
    #                                    mode=LightMode.On, brightness=100)
    #     else:
    #         self.soa.hmi_light_control(type=LightType.LightFoot, zone=LightZone.LightZoneAllOrSingle,
    #                                    mode=LightMode.On, brightness=0)

    @allure.title("AllOff语音点亮，掉电重启后熄灭")
    @pytest.mark.full
    def test_footlight_caseid_1994901(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)
        logger.info("================开始掉电==================")
        self.io.io_reset_bgm(times=10)
        sleep(35)
        logger.info("================结束掉电==================")
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("ForceOn语音熄灭，掉电重启后点亮")
    @pytest.mark.full
    def test_footlight_caseid_1994902(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        logger.info("================开始掉电==================")
        self.io.io_reset_bgm(times=10)
        sleep(35)
        logger.info("================结束掉电==================")
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("transport模式语音无法控制照脚灯")
    @pytest.mark.full
    def test_footlight_caseid_1994903(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.set_car_mode(CarMode.TRANSPORT)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("factory模式语音无法控制照脚灯")
    @pytest.mark.full
    def test_footlight_caseid_1994904(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.mix.set_car_mode(CarMode.FACTORY)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.full
    @pytest.mark.parametrize(
        "car_mode, title",
        [
            [CarMode.DYNO, "dyno_inactive语音无法控制照脚灯"],
            [CarMode.NORMAL, "normal_inactive语音无法控制照脚灯"]
        ],
        ids=[1994905, 1994906]
    )
    def test_footlight_inactive(self, car_mode, title):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(car_mode=car_mode, usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(.2)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        sleep(.2)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(0.5)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @pytest.mark.parametrize(
        "usg_mode, title",
        [
            [UsageMode.DRIVING, "dyno_driving_alloff语音点亮照脚灯"],
            [UsageMode.ACTIVE, "dyno_active_alloff语音点亮照脚灯"],
            [UsageMode.CONVENIENCE, "dyno_conv_alloff语音点亮照脚灯"]
        ],
        ids=[1994907, 1994908, 1994909]
    )
    def test_footlight_alloff(self, usg_mode, title):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=usg_mode)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        sleep(.2)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @pytest.mark.parametrize(
        "usg_mode, title",
        [
            [UsageMode.DRIVING, "dyno_driving_manual语音点亮照脚灯"],
            [UsageMode.ACTIVE, "dyno_active_manual语音点亮照脚灯"],
            [UsageMode.CONVENIENCE, "dyno_conv_manual语音点亮照脚灯"]
        ],
        ids=[1994910, 1994911, 1994912]
    )
    def test_footlight_manual(self, usg_mode, title):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=usg_mode)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @pytest.mark.parametrize(
        "usg_mode, title",
        [
            [UsageMode.DRIVING, "dyno_driving_forceOn语音熄灭照脚灯"],
            [UsageMode.ACTIVE, "dyno_active_forceOn语音熄灭照脚灯"],
            [UsageMode.CONVENIENCE, "dyno_conv_forceOn语音熄灭照脚灯"]
        ],
        ids=[1994913, 1994914, 1994915]
    )
    def test_footlight_forceon(self, usg_mode, title):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=usg_mode)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("dyno_driving_courtesy语音熄灭照脚灯")
    @pytest.mark.full
    def test_footlight_caseid_1994916(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(0.5)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("dyno_active_courtesy语音熄灭照脚灯")
    @pytest.mark.full
    def test_footlight_caseid_1994917(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(.2)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        sleep(.1)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("dyno_conv_courtesy语音熄灭照脚灯")
    @pytest.mark.sanity
    def test_footlight_caseid_1994918(self):
        self.mix.set_common_precontion(car_mode=CarMode.DYNO, usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.full
    @allure.title("normal_driving_alloff语音点亮照脚灯")
    def test_footlight_caseid_1994919(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @allure.title("normal_active_alloff语音点亮照脚灯")
    def test_footlight_caseid_1994920(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(.1)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @allure.title("normal_conv_alloff语音点亮照脚灯")
    def test_footlight_caseid_1994921(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(.1)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @pytest.mark.parametrize(
        "usg_mode, title",
        [
            [UsageMode.DRIVING, "normal_driving_manual语音点亮照脚灯"],
            [UsageMode.ACTIVE, "normal_active_manual语音点亮照脚灯"],
            [UsageMode.CONVENIENCE, "normal_conv_manual语音点亮照脚灯"]
        ],
        ids=["1994922", "1994923", "1994924"]
    )
    def test_footlight_caseid_(self, usg_mode, title):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=usg_mode)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @allure.title("normal_driving_forceOn语音熄灭照脚灯")
    def test_footlight_caseid_1994925(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(1)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.full
    @allure.title("normal_active_forceOn语音熄灭照脚灯")
    def test_footlight_caseid_1994926(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.full
    @allure.title("normal_conv_forceOn语音熄灭照脚灯")
    def test_footlight_caseid_1994927(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("normal_driving_courtesy语音熄灭照脚灯")
    @pytest.mark.full
    def test_footlight_caseid_1994928(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING)
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.HMI)
        sleep(0.5)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.HMI)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("normal_active_courtesy语音熄灭照脚灯")
    @pytest.mark.full
    def test_footlight_caseid_1994929(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("normal_conv_courtesy语音熄灭照脚灯")
    @pytest.mark.sanity
    def test_footlight_caseid_1994930(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.sanity
    @allure.title("normal_conv_manual语音点亮照脚灯_切Factory熄灭")
    def test_footlight_caseid_1995232(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        sleep(.1)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.mix.set_car_mode(car_mode=CarMode.FACTORY)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.sanity
    @allure.title("normal_active_manual语音点亮照脚灯_切Transport熄灭")
    def test_footlight_caseid_1995231(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        sleep(.1)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        sleep(1)
        self.mix.set_car_mode(car_mode=CarMode.TRANSPORT)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("normal_conv_manual语音点亮照脚灯_下切inactive熄灭")
    @pytest.mark.sanity
    def test_footlight_caseid_1995229(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.sanity
    @allure.title("normal_conv_forceon语音熄灭照脚灯_下切inactive点亮")
    def test_footlight_caseid_1995228(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        sleep(1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("normal_conv_courtesy语音熄灭照脚灯_下切inactive熄灭")
    @pytest.mark.sanity
    def test_footlight_caseid_1995230(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(1)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.io.set_door(Drvr=Door.close)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.sanity
    @allure.title("normal_conv_forceon语音熄灭照脚灯_切常关再切常开点亮")
    def test_footlight_caseid_1995223(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(.1)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("normal_conv_courtesy语音熄灭照脚灯_切crash点亮")
    @pytest.mark.sanity
    def test_footlight_caseid_1995226(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.io.set_door(Drvr=Door.close)
        self.mix.set_car_mode(CarMode.CRASH)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("normal_conv_manual语音点亮照脚灯_切AllOff熄灭")
    @pytest.mark.sanity
    def test_footlight_caseid_1995224(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(.5)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        sleep(1)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.sanity
    @allure.title("normal_conv_alloff语音点亮照脚灯_下切inactive熄灭")
    def test_footlight_caseid_1995227(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(1)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        sleep(6)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @pytest.mark.sanity
    @allure.title("normal_conv_alloff语音点亮照脚灯_切Auto熄灭")
    def test_footlight_caseid_1995222(self):
        self.soa.hmi_set_intr_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.AllOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.hmi_set_intr_light_mode(LightMode.Auto)
        self.soa.get_footlight_sts(FootLightSts.Off)

    @allure.title("normal_conv_courtesy语音熄灭照脚灯_切ForceOn点亮")
    @pytest.mark.sanity
    def test_footlight_caseid_1995225(self):
        self.io.set_door(Drvr=Door.open)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.ForceOn)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("照脚灯跟随迎宾灯记忆_On休眠唤醒")
    @pytest.mark.sanity
    @pytest.mark.wakeup
    def test_footlight_caseid_1995220(self):
        self.soa.hmi_set_intr_light_mode(LightMode.On)
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.io.set_five_door_sts(Door.close)
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.On)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(.2)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("照脚灯跟随迎宾灯记忆_auto休眠唤醒")
    @pytest.mark.sanity
    @pytest.mark.wakeup
    def test_footlight_caseid_1995218(self):
        self.soa.set_footlight_sts(OnOff.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.io.set_five_door_sts(Door.close)
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.Auto)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.ForceOff)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(.1)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)

    @allure.title("照脚灯跟随迎宾灯记忆_AllOff休眠唤醒")
    @pytest.mark.sanity
    def test_footlight_caseid_1995219(self):
        self.soa.hmi_set_intr_light_mode(mode=LightMode.Off)
        self.soa.get_internal_light_mode(LightMode.Off)
        self.bus_comm.check_courtesy_light_req(sts=ReadLampSts.AllOff)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.io.set_five_door_sts(Door.close)
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.soa.get_internal_light_mode(LightMode.Off)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(.1)
        self.soa.get_footlight_sts(FootLightSts.Off)

    # @allure.title("白天unknow点亮照脚灯")
    # @pytest.mark.sanity
    # def test_footlight_caseid_day(self):
    #     self.bus_comm.set_day_mode()
    #     sleep(3)
    #     self.set_footlight_sts(OnOff.On)
    #     self.get_footlight_sts(FootLightSts.On)
    #
    # @allure.title("白天unknow点亮照脚灯")
    # @pytest.mark.sanity
    # def test_footlight_caseid_night_to_day(self):
    #     self.set_footlight_sts(OnOff.On)
    #     self.get_footlight_sts(FootLightSts.On)
    #     self.bus_comm.set_day_mode()
    #     sleep(3)
    #     self.bus_comm.check_courtesy_light_req(ReadLampSts.Unknow)
    #     self.get_footlight_sts(FootLightSts.On)

    @allure.title("normal_conv_manual语音点亮照脚灯_白天不熄灭")
    @pytest.mark.sanity
    def test_footlight_caseid_1997077(self):
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(.5)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.set_usage_mode(UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Courtesy)
        self.soa.get_footlight_sts(FootLightSts.On)
        sleep(65)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.soa.set_footlight_sts(OnOff.On)
        sleep(.3)
        self.soa.get_footlight_sts(FootLightSts.On)
        self.bus_comm.set_day_mode()
        sleep(3)
        self.bus_comm.check_courtesy_light_req(ReadLampSts.Manual)
        self.soa.get_footlight_sts(FootLightSts.On)

    @pytest.mark.full
    @pytest.mark.notready
    @allure.title("照脚灯休眠唤醒无记忆")
    def test_footlight_caseid_1995221(self):
        self.soa.set_footlight_sts(OnOff.On)
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(5)
        self.soa.get_footlight_sts(FootLightSts.Off)
        self.mix.ctrl_lock(LockCmd.UnLock, LockSource.NFC)
        self.soa.get_footlight_sts(FootLightSts.On)




