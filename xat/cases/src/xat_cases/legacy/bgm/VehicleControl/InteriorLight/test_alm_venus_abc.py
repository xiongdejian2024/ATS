# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_alm_venus_abc.py
@Time         :7/15/24 10:56 AM
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
from xat_ecu.legacy.common.logger import logger
from xat_ecu.api.constants.common import UsageMode, CarMode


@allure.feature("车控车设")
@allure.story("内灯功能")
class TestIntrlightCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client", "CentralLockService_client"])

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")

    @pytest.mark.sanity
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Venus_8alm_Normal_Convenience_Brightness_1", 1, 0, 0, 0],
            ["Venus_8alm_Normal_Convenience_Brightness_100", 100, 0, 0, 0],
            ["Venus_8alm_Normal_Convenience_Brightness_0", 0, 0, 0, 0],
            ["Venus_8alm_Normal_Convenience_Brightness_99", 99, 0, 0, 0],
            ["Venus_8alm_Normal_Convenience_Brightness_50", 50, 0, 0, 0],
            ["Venus_8alm_Normal_Convenience_RGB_1", 100, 1, 1, 1],
            ["Venus_8alm_Normal_Convenience_RGB_255", 100, 255, 255, 255],
            ["Venus_8alm_Normal_Convenience_RGB_0", 100, 0, 0, 0],
            ["Venus_8alm_Normal_Convenience_RGB_254", 100, 254, 254, 254],
            ["Venus_8alm_Normal_Convenience_RGB_128", 100, 128, 128, 128]
        ], ids=[1991831, 1991832, 1988706, 1991855, 1991854, 1991829, 1991828, 109494, 1994508, 1994507]
    )
    def test_venus_8alm(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x2, 636: 0x1}
        )
        sleep(1)
        with allure.step("点亮Venus1-8氛围灯"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight]
        )

    @pytest.mark.sanity
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Venus_10alm_Normal_Convenience_Brightness_1", 1, 0, 0, 0],
            ["Venus_10alm_Normal_Convenience_Brightness_100", 100, 0, 0, 0],
            ["Venus_10alm_Normal_Convenience_Brightness_0", 0, 0, 0, 0],
            ["Venus_10alm_Normal_Convenience_Brightness_99", 99, 0, 0, 0],
            ["Venus_10alm_Normal_Convenience_Brightness_50", 50, 0, 0, 0],
            ["Venus_10alm_Normal_Convenience_RGB_1", 100, 1, 1, 1],
            ["Venus_10alm_Normal_Convenience_RGB_255", 100, 255, 255, 255],
            ["Venus_10alm_Normal_Convenience_RGB_0", 99, 0, 0, 0],
            ["Venus_10alm_Normal_Convenience_RGB_254", 100, 254, 254, 254],
            ["Venus_10alm_Normal_Convenience_RGB_128", 100, 128, 128, 128]
        ], ids=[1994509, 1992054, 1992103, 1992108, 1992106, 1992069, 1992067, 1992105, 1992064, 1992066]
    )
    def test_venus_10alm(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x2, 636: 0x2}
        )
        sleep(1)
        with allure.step("点亮Venus1-10氛围灯"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight, ALMZoneId.TweeterLeft,
                            ALMZoneId.TweeterRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight, ALMZoneId.TweeterLeft,
                      ALMZoneId.TweeterRight]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b, usage_mode, car_mode',
        [
            ["venus_10alm_Normal_Inactive_RGB_255", 50, 255, 255, 255, UsageMode.INACTIVE, CarMode.NORMAL],
            ["venus_10alm_Normal_Active_RGB_0", 2, 0, 0, 0, UsageMode.ACTIVE, CarMode.NORMAL],
            ["venus_10alm_Dyno_Conv_RGB_128", 100, 128, 128, 128, UsageMode.CONVENIENCE, CarMode.DYNO],
            ["venus_10alm_Dyno_Active_RGB_64", 1, 64, 64, 64, UsageMode.ACTIVE, CarMode.DYNO],
            ["venus_10alm_Crash_Driving_RGB_1", 0, 1, 1, 1, UsageMode.DRIVING, CarMode.CRASH],
            ["venus_10alm_Crash_Convenience_RGB_254", 99, 254, 254, 254, UsageMode.CONVENIENCE, CarMode.CRASH]
        ], ids=[1992073, 1992077, 1992060, 1992056, 1992093, 1992091]
    )
    def test_venus_dif_mode2_10alm(self, title, bright, r, g, b, usage_mode, car_mode):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=usage_mode,
            car_mode=car_mode,
            ccp={950: 0x2, 636: 0x2}
        )
        with allure.step("点亮venus所有氛围灯"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight, ALMZoneId.TweeterLeft,
                            ALMZoneId.TweeterRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight, ALMZoneId.TweeterLeft,
                      ALMZoneId.TweeterRight]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b, usage_mode, car_mode',
        [
            ["venus_8alm_Normal_Active_RGB_255", 100, 255, 255, 255, UsageMode.ACTIVE, CarMode.NORMAL],
            ["venus_8alm_Normal_Driving_RGB_0", 100, 0, 0, 0, UsageMode.DRIVING, CarMode.NORMAL],
            ["venus_8alm_Dyno_Active_RGB_128", 100, 128, 128, 128, UsageMode.ACTIVE, CarMode.DYNO],
            ["venus_8alm_Dyno_InActive_RGB_64", 1, 64, 64, 64, UsageMode.INACTIVE, CarMode.DYNO],
            ["venus_8alm_Crash_Inactive_RGB_1", 0, 1, 1, 1, UsageMode.INACTIVE, CarMode.CRASH],
            ["venus_8alm_Crash_Convenience_RGB_254", 99, 254, 254, 254, UsageMode.CONVENIENCE, CarMode.CRASH]
        ], ids=[1992087, 1992086, 1992099, 1992100, 1992083, 1992079]
    )
    def test_venus_dif_mode_10alm(self, title, bright, r, g, b, usage_mode, car_mode):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=usage_mode,
            car_mode=car_mode,
            ccp={950: 0x2, 636: 0x1}
        )
        with allure.step("点亮venus所有氛围灯"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.CCMiddleLeft, ALMZoneId.CCMiddleRight]
        )
