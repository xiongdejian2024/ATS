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
@allure.story("外灯/刹车灯")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client",'KeyService_client'])
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})
        sleep(2)

    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})
        sleep(2)
        

    def after_each_func(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        self.bus_comm.resume_bus_send("backbonefr")
        

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
    
    @allure.title("Dyno Convenience mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.smoke
    def test_caseid_111304(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Transport Convenience mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_114969(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115025(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115041(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Normal Inactive mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_114943(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115109(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Transport Inactive mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115100(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115262(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Dyno Driving mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115240(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Factory Convenience mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115220(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Factory Active mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115215(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Factory Driving mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115209(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Dyno Active mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115205(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115204(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Dyno Inactive mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115188(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Factory Inactive mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115184(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Crash Inactive mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115172(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Crash Convenience mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115164(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Normal Convenience mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115056(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
    
    @allure.title("Normal Driving mode E2E正确未再检测到刹车动作关闭刹车灯")
    @pytest.mark.full
    def test_caseid_115052(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_pedal(sts=YesOrNo.No)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115143(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Transport Active mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115142(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115141(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Driving mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115139(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Driving mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115138(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Driving mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115137(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Transport Convenience mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115134(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Inactive mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115130(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Driving mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115129(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115126(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Active mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115123(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Transport Inactive mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115119(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Active mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115116(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Active mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115112(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115097(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Active mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115094(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
    
    @allure.title("Transport Active mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115085(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Transport Inactive mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115080(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Driving mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115077(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Inactive mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115075(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115071(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Convenience mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115067(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Inactive mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115044(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    

    @allure.title("Factory Convenience mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115037(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115028(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    

    @allure.title("Crash Driving mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115020(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Transport Driving mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115016(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Convenience mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115004(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
    
    @allure.title("Dyno Inactive mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_115001(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Active mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114996(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Inactive mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    @pytest.mark.mcu_test
    def test_caseid_114988(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Convenience mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114984(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Convenience mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114972(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
    
    @allure.title("Transport Active mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114967(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Inactive mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114965(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Active mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114963(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Convenience mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114961(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Transport Inactive mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114957(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Convenience mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114955(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Driving mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114951(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Inactive mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114949(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Active mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114945(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
    
    @allure.title("Crash Inactive mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114939(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Inactive mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114936(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Transport Driving mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114932(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114931(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Inactive mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114926(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Active mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114925(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Convenience mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_114921(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Convenience mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113769(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        
    @allure.title("Transport Convenience mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113763(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Inactive mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113760(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Factory Inactive mode 自动刹车灯通过VDDM请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113760(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Driving mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113750(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Inactive mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113740(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Convenience mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113738(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Convenience mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113738(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Crash Driving mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113735(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Convenience mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113707(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Dyno Active mode E2E正确检测到刹车动作点亮刹车灯")
    @pytest.mark.full
    def test_caseid_113694(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("CC#508=[3]制动系统或刹车踏板传感器请求激活制动灯过程_左侧刹车灯故障")
    @pytest.mark.full
    def test_caseid_115127(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.Err)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.sd_tester.set_ccp()
        # 故障恢复
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.On)

    @allure.title("CC#114=[2] Crash Driving mode 请求点亮刹车灯时触发紧急制动闪烁所有刹车灯")
    @pytest.mark.full
    def test_caseid_115410(self):
        self.sd_tester.set_ccp(ccp_vlaue={114:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        sleep(.3)
        self.io.hazard_light_close()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        # 恢复
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("CC#114=[2] Crash Driving mode 请求点亮刹车灯时触发紧急制动后解除紧急自动刹车灯不再闪烁")
    @pytest.mark.full
    def test_caseid_115397(self):
        self.sd_tester.set_ccp(ccp_vlaue={114:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        sleep(.3)
        self.io.hazard_light_close()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
    

    @allure.title("CC#114=[2] Dyno Driving mode 踩刹车触发紧急制动闪烁所有刹车灯")
    @pytest.mark.full
    def test_caseid_115396(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)


    @allure.title("CC#114=[2] Dyno Driving mode 请求点亮刹车灯时触发紧急制动闪烁所有刹车灯")
    @pytest.mark.full
    def test_caseid_115386(self):
        self.sd_tester.set_ccp(ccp_vlaue={114:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("CC#114=[2] Crash Driving mode 踩刹车触发紧急制动后解除紧急自动刹车灯不再闪烁")
    @pytest.mark.full
    def test_caseid_115378(self):
        self.sd_tester.set_ccp(ccp_vlaue={114:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        sleep(.3)
        self.io.hazard_light_close()
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)


    @allure.title("CC#114=[2] Dyno Driving mode 踩刹车触发紧急制动后解除紧急自动刹车灯不再闪烁")
    @pytest.mark.full
    def test_caseid_115414(self):
        self.sd_tester.set_ccp(ccp_vlaue={114:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
    
    @allure.title("CC#114=[2] Dyno Driving mode 请求点亮刹车灯时触发紧急制动后解除紧急自动刹车灯不再闪烁")
    @pytest.mark.full
    def test_caseid_115415(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("CC#508=[2]&[3],CC#114=[2]紧急制动进行时请求制动灯激活过程闪烁3次_右侧刹车灯故障")
    @pytest.mark.full
    def test_caseid_115145(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2,508:3})
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Right,sts=ExtrLtgSts.Err)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        # 恢复
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Right,sts=ExtrLtgSts.On)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)


    @allure.title("CC#114=[2] Normal Driving mode 请求点亮刹车灯时触发紧急制动后解除紧急自动刹车灯不再闪烁")
    @pytest.mark.smoke
    def test_caseid_115385(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode刹车信号Qf!=3超过200ms辅助制动踏板传感器触发刹车灯")
    @pytest.mark.smoke
    def test_caseid_1994426(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 2)
        sleep(1)
        self.io.brake_light_close()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        # 恢复
        self.io.brake_light_open()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Factory Convenience mode 自动刹车灯通过BBM用作备份请求点亮刹车灯")
    @pytest.mark.full
    def test_caseid_111342(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set("backbonefr","BbmVcuBackBoneFr05", 'BrkLiOnReqForBkpBrkLiOnReqSts', 'ReqSts1_Reqd')
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("功能安全_刹车灯开启需要UB位判别_Left1")
    @pytest.mark.full
    def test_caseid_1988747(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01,'StsOfLedStopLampRi1',1,ub_flag=True)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01,'StsOfLedStopLampLe1',1,ub_flag=True)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02,'StsOfLedStopLampMid',1,ub_flag=True)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01,'StsOfLedStopLampLe1',1,ub_flag=False)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01,'StsOfLedStopLampLe1',1,ub_flag=True)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("功能安全_刹车灯开启需要UB位判别_Right1")
    @pytest.mark.full
    def test_caseid_1988760(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01,'StsOfLedStopLampRi1',1,ub_flag=True)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01,'StsOfLedStopLampLe1',1,ub_flag=True)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02,'StsOfLedStopLampMid',1,ub_flag=True)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01,'StsOfLedStopLampRi1',1,ub_flag=False)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01,'StsOfLedStopLampRi1',1,ub_flag=True)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("功能安全_刹车灯开启需要UB位判别_Mid")
    @pytest.mark.full
    def test_caseid_1988761(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmrBodyExpoFr01,'StsOfLedStopLampRi1',1,ub_flag=True)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01,'StsOfLedStopLampLe1',1,ub_flag=True)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02,'StsOfLedStopLampMid',1,ub_flag=True)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02,'StsOfLedStopLampMid',1,ub_flag=False)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmmBodyExpoFr02,'StsOfLedStopLampMid',1,ub_flag=True)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("Normal Driving mode下CCP 508！=02  or 03踩刹车无法激活刹车灯")
    @pytest.mark.full
    def test_caseid_1990226(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:0x01})
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})

    @allure.title("Normal Driving mode下CCP 508！=03踩刹车踏板后不能激活刹车灯")
    @pytest.mark.full
    def test_caseid_1990236(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:0x01})
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})

    @allure.title("踩刹车踏板后触发EBL，EBL信号丢失后刹车灯结束闪烁")
    @pytest.mark.full
    def test_caseid_1990173(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:0x03,114:0x02})
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(.5)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.resume_bus_send('backbonefr')
        sleep(2)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("ccp#114=04EBL触发打开后转向灯_方向盘打开左转向灯_EBL保持")
    @pytest.mark.full
    def test_caseid_1994406(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x04})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_singal("bodyexposedcanfd","CemBodyExpoFr51","EmgyBrkLiIndcrTurn",2)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_singal("bodyexposedcanfd","CemBodyExpoFr51","EmgyBrkLiIndcrTurn",2)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)

    @allure.title("ccp#114=04转向灯或HWL打开后触发紧急制动_EBL抑制")
    @pytest.mark.full
    def test_caseid_1994407(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x04})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        sleep(1)
        self.bus_comm.check_singal("bodyexposedcanfd","CemBodyExpoFr51","EmgyBrkLiIndcrTurn",2)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        # 恢复
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=95)
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("ccp#114=04紧急制动打开后转向灯后关闭后转向灯")
    @pytest.mark.full
    def test_caseid_1994408(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x04})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_singal("bodyexposedcanfd","CemBodyExpoFr51","EmgyBrkLiIndcrTurn",2)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.check_singal("bodyexposedcanfd","CemBodyExpoFr51","EmgyBrkLiIndcrTurn",1)

    @allure.title("ccp#114=04紧急制动打开后转向灯且不闪烁")
    @pytest.mark.full
    def test_caseid_1994409(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x04})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_singal("bodyexposedcanfd","CemBodyExpoFr51","EmgyBrkLiIndcrTurn",2)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
    
    @allure.title("Crash Active触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994413(self):
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=47)
        sleep(6)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH,ccp={114:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("Crash Convenience触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994414(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={114:2})
        sleep(3)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(3)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("Normal Inactive触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994415(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("Normal Abandoned触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994416(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("Dyno Driving触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994417(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("Transport Driving触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994418(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("Factory Driving mode触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994419(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("ccp#114 != 02踩刹车触发紧急制动不能触发闪烁刹车灯")
    @pytest.mark.full
    def test_caseid_1994420(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL ,ccp={114:3})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)

    @allure.title("CC#508=02/03,CC#114=02紧急制动进行时请求制动灯激活过程闪烁4次_中央刹车灯故障")
    @pytest.mark.full
    def test_caseid_1994427(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2,508:3})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(4):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Mid,sts=ExtrLtgSts.Err)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Mid,sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("CC#508=02/03,CC#114=02紧急制动进行时请求制动灯激活过程闪烁3次_左侧刹车灯故障")
    @pytest.mark.full
    def test_caseid_1994428(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL ,ccp={508:3,114:2})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.Err)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.On)

    @allure.title("CC#508=03制动系统或刹车踏板传感器请求激活制动灯过程_中央刹车灯故障")
    @pytest.mark.full
    def test_caseid_1994429(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Mid,sts=ExtrLtgSts.Err)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Mid,sts=ExtrLtgSts.On)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)

    @allure.title("CC#508=03制动系统或刹车踏板传感器请求激活制动灯过程_右侧刹车灯故障")
    @pytest.mark.full
    def test_caseid_1994430(self):
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Right,sts=ExtrLtgSts.Err)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Err)
        self.bus_comm.set_brake_lamp_fault_sts(pos=GeneralPos.Right,sts=ExtrLtgSts.On)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)

    @allure.title("Abandoned下踩下刹车踏板刹车灯不亮")
    @pytest.mark.full
    def test_caseid_1990227(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)

    @allure.title("Crash Convenience刹车信号Qf!=3超过200ms辅助制动踏板传感器触发刹车灯")
    @pytest.mark.full
    def test_caseid_1994425(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 1)
        sleep(1)
        self.io.brake_light_close()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        # 恢复
        self.io.brake_light_open()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Dyno Inactive刹车信号Qf!=3超过200ms辅助制动踏板传感器触发刹车灯")
    @pytest.mark.full
    def test_caseid_1994424(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.DYNO)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 2)
        sleep(1)
        self.io.brake_light_close()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
         # 恢复
        self.io.brake_light_open()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Transport Active刹车信号Qf!=3超过200ms辅助制动踏板传感器触发刹车灯")
    @pytest.mark.full
    def test_caseid_1994423(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 0)
        sleep(1)
        self.io.brake_light_close()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
         # 恢复
        self.io.brake_light_open()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Factory Inactive刹车信号Qf!=3超过200ms辅助制动踏板传感器触发刹车灯")
    @pytest.mark.full
    def test_caseid_1994422(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 2)
        sleep(1)
        self.io.brake_light_close()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
         # 恢复
        self.io.brake_light_open()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("Qf!=3超过200ms辅助制动踏板传感器触发刹车灯之后失活刹车灯")
    @pytest.mark.full
    def test_caseid_1994421(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_singal("backbonefr", "BcmVddmBackBoneFr00", "BrkPedlPsdQf", 2)
        sleep(1)
        self.io.brake_light_close()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.io.brake_light_open()
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)

    @allure.title("刹车灯时间要求_BGM收到请求之后80ms之内刹车灯开启")
    @pytest.mark.full
    def test_caseid_1994412(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        sleep(.8)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)