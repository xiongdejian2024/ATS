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
@allure.story("外灯/NVM")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client",'KeyService_client'])
        self.bus_comm.resume_all_bus_send()
        sleep(2)

        
    def before_each_func(self, ecu):
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.bus_comm.resume_all_bus_send()
        sleep(2)

    def after_each_func(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    def check_night_mode(self):
        ori_data = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts')
        check_result = check_all_value_is(ori_data, 1)
        logger.info(f"Check 结果是：{check_result}")
        assert check_result

    def check_day_mode(self):
        ori_data = self.bus_comm.ipdu.check_signal(self.bus_comm.ipdu.cem_lin1.RlsmCem_Lin1Fr01, 'OutdBriSts')
        check_result = check_all_value_is(ori_data, 2)
        logger.info(f"Check 结果是：{check_result}")
        assert check_result
    
    @allure.title("诊断复位_方向盘回正转向灯熄灭")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995537(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)
        self.sd_tester.reset_bgm()
        sleep(3)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("io复位_方向盘回正转向灯熄灭")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995538(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("休眠唤醒_方向盘回正转向灯熄灭")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995539(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.LeOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.Off,act_sts=IndcrSts.Off)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(15)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.trigger_steer_wheel_button(pos=SteerWhlTouchSwtPos.Left2,press_type=SteerWhlTouchSwtSts.ShortPress)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.LeOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeOn,act_sts=IndcrSts.Off)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.8)
        sleep(1)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr02", 'SteerWhlSnsrAg', 0.52)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=6)

    @allure.title("休眠唤醒_EBL请求刹车灯闪烁频率")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995546(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(1)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
    
    @allure.title("诊断复位_EBL请求刹车灯闪烁频率")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995542(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(1)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.sd_tester.reset_bgm()
        sleep(15)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(1)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("io复位_EBL请求刹车灯闪烁频率")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995544(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(1)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.io.io_reset_bgm()
        sleep(15)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:0x02})
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(.5)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    @allure.title("诊断复位_热失控信号丢失HWL继续闪烁")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995540(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_hvbatt(128)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(1)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        self.bus_comm.resume_bus_send('backbonefr')
        self.sd_tester.reset_bgm()
        sleep(3)
        self.bus_comm.set_hvbatt(128)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On,pos_sts=IndcrSts.LeAndRiOn)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off,pos_sts=IndcrSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        self.bus_comm.pause_bus_send('backbonefr')
        sleep(1)
        for num in range(3):
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.LeAndRiOn)
            sleep(.4)
            self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
            self.bus_comm.check_turn_lamp_act_req(sts=IndcrSts.LeAndRiOn,act_sts=IndcrSts.Off)
        self.bus_comm.resume_bus_send('backbonefr')
        self.bus_comm.set_hvbatt(0)
        sleep(1)
        self.bus_comm.check_turn_lamp_always_off(pos=GeneralPos.All,last_time=3)

    @allure.title("诊断复位TmrForNightToDay切换时间为2000ms")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995548(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.sd_tester.reset_bgm()
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()

    @allure.title("诊断复位TmrForDayToNight切换时间为2000ms")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995549(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.sd_tester.reset_bgm()
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()

    @allure.title("io复位TmrForNightToDay切换时间为2000ms")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995550(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        
    @allure.title("io复位TmrForDayToNight切换时间为2000ms")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995551(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.io.io_reset_bgm()
        sleep(15)
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()

    @allure.title("休眠唤醒TmrForNightToDay切换时间为2000ms")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995552(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(15)
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        
    @allure.title("休眠唤醒TmrForDayToNight切换时间为2000ms")
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1995553(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        sleep(15)
        self.bus_comm.set_day_mode(wait_time=2)
        self.check_day_mode()
        self.bus_comm.set_night_mode(wait_time=2)
        self.check_night_mode()