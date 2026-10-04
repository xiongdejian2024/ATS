#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_extilight.py
@Author      : daidi.liang@jiduauto.com
@Time        : 2024/03/26 11:30
@Description: BGM车控车设外灯
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
@allure.story("外灯/自适应前照明系统")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client"])
        sleep(2)
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    def before_each_func(self, ecu):
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.bus_comm.set_vehspd_gear(vehspd=0)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)

    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=0)
        sleep(1)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    @allure.title("大屏Pos位切换到Auto位_AFS开启")
    @pytest.mark.full
    def test_caseid_1995239(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_afs_act(isOn.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)

    @allure.title("大屏近光位切换到Auto位_AFS开启")
    @pytest.mark.full
    def test_caseid_1995240(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_afs_act(isOn.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)

    @allure.title("AFS开启_大屏设置Pos位_AFS关闭")
    @pytest.mark.sanity
    def test_caseid_1995241(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_afs_act(isOn.Off)

    @allure.title("AFS开启_大屏设置近光位_AFS关闭")
    @pytest.mark.sanity
    def test_caseid_1995242(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_afs_act(isOn.Off)

    @allure.title("大屏在Auto位_AFS开启_白天夜晚切换不影响AFS")
    @pytest.mark.full
    def test_caseid_1995244(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_afs_act(isOn.On)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_afs_act(isOn.On)

    @allure.title("大屏在Auto位_AFS开启")
    @pytest.mark.sanity
    def test_caseid_1995245(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)

    @allure.title("大屏在Auto位开启AFS_大屏不在Auto位关闭AFS")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995340(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_afs_act(isOn.Off)

    @allure.title("大屏在Auto位_AFS开启_下切Inactive_AFS维持")
    @pytest.mark.full
    def test_caseid_1995351(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_afs_act(isOn.On)

    @allure.title("大屏在Auto位_AFS开启_下切Abandoned_AFS维持")
    @pytest.mark.full
    def test_caseid_1995352(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_afs_act(isOn.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.check_afs_act(isOn.On)

    @allure.title("大屏近光位切换到Pos位_AFS维持关闭")
    @pytest.mark.full
    @pytest.mark.auto1112
    def test_caseid_1995243(self):
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_afs_act(isOn.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_afs_act(isOn.Off)