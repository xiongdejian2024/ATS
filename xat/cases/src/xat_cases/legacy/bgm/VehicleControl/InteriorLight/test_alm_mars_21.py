# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_alm_mars_21.py
@Time         :7/26/24 9:48 AM
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
        self.soa.update(["LightService_client", "CentralLockService_client"])
        self.soa.send_method_request(
                "LightService_client",
                "SetAmbientInhibit",
                {"ambientInhibit": [{"type": 35, "inhibitSts": False}]},
            )
        sleep(1)

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

    # —————————————————————————————————2.1CR—————————————————————————————————— #

    @pytest.mark.sanity
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_Brightness_1", 1, 0, 0, 0, ],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_Brightness_100", 100, 0, 0, 0],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_Brightness_0", 0, 0, 0, 0],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_Brightness_99", 99, 0, 0, 0],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_Brightness_50", 50, 0, 0, 0]
        ], ids=[1987433, 1987432, 1987431, 1987430, 1987240]
    )
    def test_alm_case_id_alm1_6_bri_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x0}
        )
        sleep(2)
        with allure.step("点亮Mars_alm1-6"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight]
        )

    @pytest.mark.sanity
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_RGB_1", 100, 1, 1, 1],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_RGB_255", 100, 255, 255, 255],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_RGB_0", 100, 0, 0, 0],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_RGB_254", 100, 254, 254, 254],
            ["Mars不含头枕音响不含CC下方灯带_alm1-6_Normal_Convenience_RGB_128", 100, 128, 128, 128],
        ], ids=[1987239, 1987161, 1987160, 1987159, 1987158]
    )
    def test_alm_case_id_alm1_6_color_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x0}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-6"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_Brightness_1", 1, 0, 0, 0],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_Brightness_100", 100, 0, 0, 0],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_Brightness_0", 0, 0, 0, 0],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_Brightness_99", 99, 0, 0, 0],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_Brightness_50", 50, 0, 0, 0]
        ], ids=[1979886, 1979668, 1979667, 1979666, 1978338]
    )
    def test_alm_case_id_alm1_7_bri_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x1}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-7"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.CCUnder]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.CCUnder]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_RGB_1", 100, 1, 1, 1],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_RGB_255", 100, 255, 255, 255],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_RGB_0", 100, 0, 0, 0],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_RGB_254", 100, 254, 254, 254],
            ["Mars不含头枕音响含CC下方灯带_alm1-7_Normal_Convenience_RGB_128", 100, 128, 128, 128],
        ], ids=[1978337, 1985352, 1985350, 1985356, 1985349]
    )
    def test_alm_case_id_alm1_7_color_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x1, 964: 0x1}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-7"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.CCUnder]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.CCUnder]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_Brightness_1", 1, 0, 0, 0],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_Brightness_100", 100, 0, 0, 0],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_Brightness_0", 0, 0, 0, 0],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_Brightness_99", 99, 0, 0, 0],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_Brightness_50", 50, 0, 0, 0]
        ], ids=[1985357, 1985347, 1985354, 1985353, 1989784]
    )
    def test_alm_case_id_alm1_8_bri_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x0}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-8"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_RGB_1", 100, 1, 1, 1],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_RGB_255", 100, 255, 255, 255],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_RGB_0", 100, 0, 0, 0],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_RGB_254", 100, 254, 254, 254],
            ["Mars含头枕音响不含CC下方灯带_alm1-8_Normal_Convenience_RGB_128", 100, 128, 128, 128],
        ], ids=[1985369, 1985333, 1985334, 1985359, 1989785]
    )
    def test_alm_case_id_alm1_8_color_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x0}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-8"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_Brightness_1", 1, 0, 0, 0],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_Brightness_100", 100, 0, 0, 0],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_Brightness_0", 0, 0, 0, 0],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_Brightness_99", 99, 0, 0, 0],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_Brightness_50", 50, 0, 0, 0]
        ], ids=[1989765, 1989764, 1989762, 1989763, 1985374]
    )
    def test_alm_case_id_alm1_9_bri_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x1}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-9"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight, ALMZoneId.CCUnder]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight, ALMZoneId.CCUnder]
        )

    @pytest.mark.sanity
    @pytest.mark.parametrize(
        'title, bright, r, g, b',
        [
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_RGB_1", 100, 1, 1, 1],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_RGB_255", 100, 255, 255, 255],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_RGB_0", 100, 0, 0, 0],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_RGB_254", 100, 254, 254, 254],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Convenience_RGB_128", 100, 128, 128, 128],
        ], ids=[1986087, 1986086, 1986084, 1986085, 1989770]
    )
    def test_alm_case_id_alm1_9_color_caseid_(self, title, bright, r, g, b):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE,
            car_mode=CarMode.NORMAL,
            ccp={950: 0x1, 636: 0x2, 964: 0x1}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-9"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight, ALMZoneId.CCUnder]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight, ALMZoneId.CCUnder]
        )

    @pytest.mark.full
    @pytest.mark.parametrize(
        'title, bright, r, g, b, usage_mode, car_mode',
        [
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Inactive_RGB_255", 100, 255, 255, 255, UsageMode.INACTIVE,
             CarMode.NORMAL],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Normal_Active_RGB_0", 100, 0, 0, 0, UsageMode.ACTIVE, CarMode.NORMAL],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Crash_Inactive_RGB_128", 100, 128, 128, 128, UsageMode.INACTIVE,
             CarMode.CRASH],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Crash_Active_RGB_64", 1, 64, 64, 64, UsageMode.ACTIVE, CarMode.CRASH],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Dyno_Driving_RGB_1", 0, 1, 1, 1, UsageMode.DRIVING, CarMode.DYNO],
            ["Mars含头枕音响含CC下方灯带_alm1-9_Dyno_Convenience_RGB_254", 99, 254, 254, 254, UsageMode.CONVENIENCE,
             CarMode.DYNO]
        ], ids=[1989766, 1985375, 1991373, 1991372, 109497, 1991825]
    )
    def test_dif_mode_alm1_9_caseid_(self, title, bright, r, g, b, usage_mode, car_mode):
        allure.dynamic.title(title)
        self.mix.set_common_precontion(
            usage_mode=usage_mode,
            car_mode=car_mode,
            ccp={950: 0x1, 636: 0x2, 964: 0x1}
        )
        sleep(1)
        with allure.step("点亮Mars_alm1-9"):
            self.soa.ctrl_mul_alm_illuminate(
                bright, r, g, b,
                zoneid_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                            ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                            ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight, ALMZoneId.CCUnder]
            )
        self.bus_comm.check_mul_alms(
            bright, r, g, b,
            zone_lst=[ALMZoneId.FrontLeft, ALMZoneId.FrontRight, ALMZoneId.RearLeft,
                      ALMZoneId.RearRight, ALMZoneId.CCLeft, ALMZoneId.CCRight,
                      ALMZoneId.TweeterLeft, ALMZoneId.TweeterRight, ALMZoneId.CCUnder]
        )

    @allure.title("ALM1_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1996915(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM1, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM1, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM1_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997106(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM1, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM1, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM1_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997105(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM1, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM1, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM2_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997104(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM2, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM2, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM2, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM2_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997103(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM2, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM2, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM2, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM2_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997102(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM2, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM2, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM2, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM3_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997101(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            with allure.step(f"当前车型为{ccp}"):
                self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM3, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM3, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM3, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM3_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997100(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM3, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM3, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM3, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM3_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997099(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM3, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM3, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM3, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM4_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997098(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM4, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM4, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM4, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM4_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997097(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM4, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM4, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM4, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM4_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997096(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM4, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM4, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM4, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM5_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997095(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM5, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM5, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM5, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM5_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997094(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM5, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM5, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM5, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM5_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997093(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM5, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM5, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM5, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM6_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997092(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM6, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM6, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM6, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM6_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997091(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM6, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM6, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM6, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM6_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997090(self):
        ccp_lst = [
            {950: 0x1, 636: 0x1, 964: 0x0},
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM6, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM6, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM6, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM7_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997089(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
            self.bus_comm.set_alm_led_fault(AlmNum.ALM7, AlmSts.Fault)
            self.bus_comm.check_alm_flt(AlmNum.ALM7, AlmSts.Fault)
            self.bus_comm.set_alm_led_fault(AlmNum.ALM7, AlmSts.Normal)
            self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM7_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997088(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM7, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM7, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM7, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM7_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997087(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x1, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM7, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM7, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM7, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM8_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997086(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM8, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM8, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM8, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM8_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997085(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM8, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM8, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM8, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM8_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997084(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x1, 636: 0x2, 964: 0x0},
            {950: 0x2, 636: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM8, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM8, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM8, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM9_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997083(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM9, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM9, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM9, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM9_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997082(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM9, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM9, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM9, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM9_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997081(self):
        ccp_lst = [
            {950: 0x1, 636: 0x2, 964: 0x1},
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM9, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM9, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM9, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM10_led状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997080(self):
        ccp_lst = [
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM10, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM10, AlmSts.Fault)
        self.bus_comm.set_alm_led_fault(AlmNum.ALM10, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM10_vlt状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997079(self):
        ccp_lst = [
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM10, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM10, AlmSts.Fault)
        self.bus_comm.set_alm_vlt_fault(AlmNum.ALM10, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)

    @allure.title("ALM10_tmp状态故障")
    @pytest.mark.full
    @pytest.mark.man
    def test_caseid_1997078(self):
        ccp_lst = [
            {950: 0x2, 636: 0x2}
        ]
        for ccp in ccp_lst:
            self.sd_tester.write_ccp(ccp)
            sleep(2)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM10, AlmSts.Fault)
        self.bus_comm.check_alm_flt(AlmNum.ALM10, AlmSts.Fault)
        self.bus_comm.set_alm_tmp_fault(AlmNum.ALM10, AlmSts.Normal)
        self.bus_comm.check_alm_flt(AlmNum.ALM1, AlmSts.Normal)
