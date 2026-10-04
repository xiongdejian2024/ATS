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
        sleep(2)

        
    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        #mars1
        ccp="A3 01 80 06 FD 03 02 01 A3 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 02 04 8F 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 04 01 02 02 85 89 02 02 01 02 09 02 7B 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 01 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 05 01 02 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 02 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 02 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 82 01 02 01 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 01 02 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 04 01 02 01 02 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 02 02 01 01 03 01 04 02 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 02 01 02 02 01 01 02 01 01 01 01 01 00 01 04 00 00 00 02 01 00 02 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 02 05 08 08 02 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 01 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 02 01 01 01 01 01 01 02 02 01 02 02 01 01 02 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 02 02 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"
        # ccp="A3 01 81 06 FD 03 01 01 A2 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 01 04 8F 80 0C 01 01 01 01 02 01 82 02 01 02 16 01 07 01 01 01 00 03 01 02 02 80 89 02 03 01 01 03 02 73 72 03 01 01 01 01 01 01 01 03 01 02 02 02 02 0A 01 01 02 01 02 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 00 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 80 01 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 82 03 03 04 01 14 03 0A 80 01 04 01 02 01 02 02 03 82 05 02 05 01 01 02 01 01 80 04 01 02 01 01 01 02 05 02 01 01 00 03 02 02 03 04 02 02 02 01 01 01 02 00 01 01 01 01 01 01 01 01 01 80 03 0A 01 01 04 06 07 07 0A 0A 07 07 0A 0A 00 00 04 00 00 02 01 01 01 01 01 02 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 00 01 01 02 00 00 00 01 03 00 00 01 00 00 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00 00 00 00 01 00 01 01 00 00 02 00 00 00 80 00 00 00 00 84 03 01 01 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 01 01 01 01 01 05 03 80 02 06 01 03 01 10 00 00 02 03 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 02 01 00 00 00 00 00 85 04 01 02 02 02 01 02 02 02 04 85 01 02 01 01 02 80 04 03 01 01 02 02 01 03 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 00 00 00 01 80 02 02 01 01 02 02 01 02 02 02 01 02 01 03 02 02 01 01 01 01 01 01 01 01 00 01 03 01 02 01 01 05 02 03 03 04 01 01 01 01 03 01 01 04 02 01 02 01 01 01 01 02 01 01 01 01 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 01 02 01 01 03 01 04 01 04 01 01 01 01 01 02 01 03 01 05 02 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 01 01 01 01 01 02 01 01 01 01 02 06 00 00 01 01 04 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 03 02 02 08 01 00 00 01 02 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 01 02 02 01 01 02 02 02 02 02 02 02 02 01 02 02 01 02 01 02 02 02 02 01 02 02 02 02 01 02 02 02 02 02 02 01 02 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 00 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 02 02 01 01 01 01 01 01 02 02 01 02 02 01 01 01 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 01 02 02 02 01 02 02 01 01 01 02 02 01 01 02 02 02 02 02 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"
        self.sd_tester.write_ccp_value(ccp)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(10)

    def after_each_func(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        self.bus_comm.resume_bus_send("backbonefr")

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        
    @allure.title("CC#508=[3]，CC#259=[2] Crash Driving mode 倒挡切前进档倒车灯熄灭")
    @pytest.mark.full
    def test_caseid_113328(self):
        self.mix.set_ccp({508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 2)
        sleep(0.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 1)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("CC#508=[3]，CC#259=[2] Dyno Driving mode 倒挡切前进档倒车灯熄灭")
    @pytest.mark.full
    def test_caseid_113318(self):
        self.mix.set_ccp({508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 2)
        sleep(0.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 1)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("CC#508=[3]，CC#259=[2] Crash Driving mode 倒挡切空档倒车灯熄灭")
    @pytest.mark.full
    def test_caseid_113290(self):
        self.mix.set_ccp({508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 2)
        sleep(0.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 3)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("CC#508=[3]，CC#259=[2] Normal Driving mode 倒挡信号丢失超过5秒倒车灯熄灭")
    @pytest.mark.full
    def test_caseid_113252(self):
        self.mix.set_ccp({508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 2)
        sleep(0.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.pause_bus_send("backbonefr")
        sleep(5)
        # 停发fr，ExtrLtgStsReverseLi无法check
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp',0)
        self.bus_comm.resume_bus_send("backbonefr")
        sleep(1)

    @allure.title("CC#508=[3],CC#259=[2] Normal Driving mode 挂倒挡点亮倒车灯")
    @pytest.mark.smoke
    def test_caseid_113413(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("CC#508=[3]，CC#259=[4] Normal Driving mode 挂倒挡点亮倒车灯")
    @pytest.mark.smoke
    @pytest.mark.reverse
    def test_caseid_113370(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("CC#508=[3]，CC#259=[4] Normal Driving mode 倒挡切前进档倒车灯熄灭")
    @pytest.mark.smoke
    def test_caseid_113346(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("CC#508=[3]，CC#259=[2] Normal Driving mode 倒挡切前进档倒车灯熄灭")
    @pytest.mark.smoke
    # @pytest.mark.reverse
    def test_caseid_113331(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Fwd)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("CC#508=[3]，CC#259=[4] Normal Driving mode 倒挡切空档倒车灯熄灭")
    @pytest.mark.smoke
    # @pytest.mark.reverse
    def test_caseid_113314(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03,259:0x04})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Neut)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("CC#508=[3]，CC#259=[2] Normal Driving mode 倒挡切空档倒车灯熄灭")
    @pytest.mark.smoke
    # @pytest.mark.reverse
    def test_caseid_113296(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Neut)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("倒车灯在Factory mode下挂倒挡无法点亮")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1990202(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("倒车灯在Transport mode下挂倒挡无法点亮")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1990203(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("倒车灯在Active下挂倒挡无法点亮")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1990204(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("倒车灯在Convenice下挂倒挡无法点亮")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1990205(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("倒车灯在Inactive下挂倒挡无法点亮")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1990206(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("倒车灯在Abandoned下挂倒挡无法点亮")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1990207(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("ccp#508=03, ccp#259=02挂倒挡点亮倒车灯时右倒车灯反馈故障")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1994431(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,259:2})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("ccp#508=03, ccp#259=02挂倒挡点亮倒车灯时左倒车灯反馈故障")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1994432(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,259:2})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("ccp#508=03, ccp#259=04挂倒挡点亮倒车灯时右倒车灯反馈故障")
    @pytest.mark.full
    @pytest.mark.rl_new
    def test_caseid_1994433(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,259:4})
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Rvs)
        sleep(.25)
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_reverse_lamp_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_drvrdes_sts(drvrdes=DrvrDesDir.Undefd)

    @allure.title("CC#508=[3]，CC#259=[2] Crash Driving mode 倒挡信号丢失超过5秒倒车灯熄灭")
    @pytest.mark.full
    def test_caseid_113245(self):
        self.mix.set_ccp({508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 2)
        sleep(0.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.pause_bus_send("backbonefr")
        sleep(5)
        # 停发fr，ExtrLtgStsReverseLi无法check
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp',0)
        self.bus_comm.resume_bus_send("backbonefr")
        sleep(1)

    @allure.title("CC#508=[3]，CC#259=[2] Dyno Driving mode 倒挡信号丢失超过5秒倒车灯熄灭")
    @pytest.mark.full
    def test_caseid_113241(self):
        self.mix.set_ccp({508:0x03,259:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","VddmBackBoneFr10",'DrvrDesDirDrvrDesDir', 2)
        sleep(0.25)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.pause_bus_send("backbonefr")
        sleep(5)
        # 停发fr，ExtrLtgStsReverseLi无法check
        self.bus_comm.ipdu.check(self.bus_comm.ipdu.bodyexposedcanfd.CemBodyExpoFr50, 'ActnOfLedRvsgLamp',0)
        self.bus_comm.resume_bus_send("backbonefr")
        sleep(1)