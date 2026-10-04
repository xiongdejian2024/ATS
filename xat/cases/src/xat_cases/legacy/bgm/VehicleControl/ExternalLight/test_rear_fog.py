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
@allure.story("外灯/后雾灯")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client",'KeyService_client'])
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

    @allure.title("Normal Convenience mode通过大屏开关关闭后雾灯")
    @pytest.mark.full
    def test_caseid_113401(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode通过大屏开关关闭后雾灯")
    @pytest.mark.full
    def test_caseid_113395(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode通过大屏开关关闭后雾灯")
    @pytest.mark.full
    def test_caseid_113389(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Convenience mode通过大屏开关关闭后雾灯")
    @pytest.mark.full
    def test_caseid_113386(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode通过大屏开关关闭后雾灯")
    @pytest.mark.full
    def test_caseid_113381(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode通过大屏开关关闭后雾灯")
    @pytest.mark.full
    def test_caseid_113378(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Convenience mod通过大屏开关打开后雾灯左后雾灯故障")
    @pytest.mark.full
    def test_caseid_113360(self):
        self.mix.set_ccp({225:0x02})
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01", 'StsOfLedReFogLampLe1', 2)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Crash Driving mode VDDM踩刹车紧急制动EBL请求点亮后雾灯_请求结束熄灭后雾灯")
    @pytest.mark.full
    def test_caseid_113310(self):
        self.mix.set_ccp({508:0x03,255:0x02,114:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Dyno Driving mode VDDM踩刹车紧急制动EBL请求点亮后雾灯_请求结束熄灭后雾灯")
    @pytest.mark.full
    def test_caseid_113305(self):
        self.mix.set_ccp({508:0x03,255:0x02,114:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00",'BrkPedlPsdBrkPedlPsd', 1)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00",'BrkPedlPsdQf', 3)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00",'BrkPedlPsdBrkPedlNotPsdSafe', 1)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr16",'EmgyBrkLiReqEmgyBrk', 1)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr16",'EmgyBrkLiReqEmgyBrk', 0)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode BBM踩刹车紧急制动EBL请求点亮刹车灯后雾灯同步点亮_请求结束熄灭后雾灯")
    @pytest.mark.full
    def test_caseid_113292(self):
        self.mix.set_ccp({508:0x03,255:0x02,114:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        sleep(.5)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgsAtSpdLo)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Dyno Driving mode BBM踩刹车紧急制动EBL请求点亮刹车灯后雾灯同步点亮_请求结束熄灭后雾灯")
    @pytest.mark.full
    def test_caseid_113288(self):
        self.mix.set_ccp({508:0x03,255:0x02,114:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr16",'BrkLiOnReqSts', 1)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr16",'EmgyBrkLiReqEmgyBrk', 1)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr16",'EmgyBrkLiReqEmgyBrk', 0)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode近光已激活通过大屏开关关闭后雾灯")
    @pytest.mark.smoke
    def test_caseid_113469(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.Off)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("功能安全_后雾灯开启需要UB位判别_Left1")
    @pytest.mark.full
    def test_caseid_1988746(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.All,sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReFogLampRi1",1,ub_flag=True)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReFogLampLe1",1,ub_flag=True)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReFogLampLe1",1,ub_flag=False)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReFogLampLe1",1,ub_flag=True)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后雾灯在Dyno下无法点亮")
    @pytest.mark.full
    def test_caseid_1990209(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.All,sts=ExtrLtgSts.Off)
    
    @allure.title("后雾灯在factory下无法点亮")
    @pytest.mark.full
    def test_caseid_1990210(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.All,sts=ExtrLtgSts.Off)

    @allure.title("后雾灯在transport下无法点亮")
    @pytest.mark.full
    def test_caseid_1990211(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.All,sts=ExtrLtgSts.Off)
    
    @allure.title("Abandoned mode无法打开后雾灯")
    @pytest.mark.full
    def test_caseid_1990212(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.All,sts=ExtrLtgSts.Off)

    @allure.title("Inactive mode无法打开后雾灯")
    @pytest.mark.full
    def test_caseid_1990213(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.All,sts=ExtrLtgSts.Off)
    
    @allure.title("ccp#508=03, ccp#225=02近光已激活通过大屏开关打开后雾灯右后雾灯故障")
    @pytest.mark.full
    def test_caseid_1994434(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.Right,sts=ExtrLtgSts.Err)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
    
    @allure.title("ccp#508=03, ccp#225=04近光已激活通过大屏开关打开后雾灯左后雾灯故障")
    @pytest.mark.full
    def test_caseid_1994435(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.Left,sts=ExtrLtgSts.Err)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("ccp#225!=04/02无法打开后雾灯")
    @pytest.mark.full
    def test_caseid_1994436(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.mix.set_ccp({225:0x03})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_ccp({225:0x02})

    @allure.title("ccp#508!=03无法打开后雾灯")
    @pytest.mark.full
    def test_caseid_1994437(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_ccp({508:0x01})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_ccp({508:0x03})

    @allure.title("功能安全_后雾灯开启不需要UB位判别_Right1")
    @pytest.mark.full
    def test_caseid_1988724(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={508:3,255:2})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.set_rear_fog_fault_sts(pos=GeneralPos.All,sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReFogLampRi1",1,ub_flag=True)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedReFogLampLe1",1,ub_flag=True)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReFogLampRi1",1,ub_flag=False)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedReFogLampRi1",1,ub_flag=True)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)