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
@allure.story("外灯/倒车灯")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client",'KeyService_client'])
        # 设置车辆静止
        self.bus_comm.set_vehspd_gear(vehspd=0, gear=Gear.Park)
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        sleep(2)

        
    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)


    @allure.title("Normal Active mode_夜晚AHL跟随近光灯一起点亮")
    @pytest.mark.sanity
    def test_caseid_1985462(self):
        self.mix.set_ccp({274:0x80})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode_夜晚AHL跟随近光灯一起点亮")
    @pytest.mark.full
    def test_caseid_1985463(self):
        self.mix.set_ccp({274:0x80})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode_AHL随近光一起点亮")
    @pytest.mark.full
    def test_caseid_1985457(self):
        self.mix.set_ccp({274:0x80})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode_AHL跟随近光灯一起点亮")
    @pytest.mark.sanity
    def test_caseid_1985456(self):
        self.mix.set_ccp({274:0x80})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("Normal Driving mode下CCP 60=01 or 274！=80 or 81通过软开关无法开启自动前照灯")
    @pytest.mark.full
    def test_caseid_1990196(self):
        self.mix.set_ccp({274:0x82})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_ccp({274:0x80})

    @allure.title("自动前照灯在Inactive下无法点亮")
    @pytest.mark.full
    def test_caseid_1990197(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("自动前照灯在Abandoned下无法点亮")
    @pytest.mark.full
    def test_caseid_1990198(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("AHL跟随近光灯一起点亮_挂倒挡AHL熄灭")
    @pytest.mark.full
    def test_caseid_1994455(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("自动前照灯在Convenience下无法点亮")
    @pytest.mark.full
    def test_caseid_1994456(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_夜晚AHL跟随近光灯一起点亮")
    @pytest.mark.full
    def test_caseid_1994457(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Crash Active mode_AHL跟随近光灯一起点亮")
    @pytest.mark.full
    def test_caseid_1994458(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("AHL跟随近光灯一起点亮_关闭近光灯AHL一起熄灭")
    @pytest.mark.full
    def test_caseid_1994459(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("打开近光灯点亮AHL_右灯故障")
    @pytest.mark.full
    def test_caseid_1994460(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_ahl_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        # 恢复防止影响后面case
        self.bus_comm.set_ahl_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)

    @allure.title("打开近光灯点亮AHL_左灯故障")
    @pytest.mark.full
    def test_caseid_1994461(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_ahl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        sleep(1)
        self.bus_comm.set_ahl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)
        sleep(1)
        self.bus_comm.check_ahl_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)