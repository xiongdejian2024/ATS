#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_extilight.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
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
@allure.story("后视镜功能")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client"])
        sleep(2)
        # mars1
        # ccp="A3 01 80 06 FD 03 02 01 A3 02 09 03 04 02 01 02 85 8B 06 01 00 04 05 02 03 00 00 02 04 8F 80 0C 01 01 03 01 02 01 82 02 01 02 16 01 07 01 01 01 00 04 01 02 02 85 89 02 02 01 02 09 02 7B 74 03 01 01 01 01 01 01 01 03 01 02 02 02 02 01 02 01 02 01 01 01 01 01 02 02 01 03 01 02 01 80 02 03 02 80 01 80 00 01 00 81 80 11 01 03 04 01 01 01 01 02 01 03 02 81 02 02 01 01 01 01 01 04 01 01 01 01 01 01 01 02 03 01 01 03 02 02 01 83 02 01 01 02 01 01 29 02 01 04 02 03 80 02 81 03 81 04 01 14 01 0A 80 01 01 01 02 01 02 02 03 82 05 02 05 01 02 02 01 01 80 04 01 02 01 01 01 02 02 03 01 01 01 03 02 02 03 04 02 04 02 01 01 01 03 02 0A 02 01 01 01 02 01 01 01 80 81 0A 01 02 04 01 07 07 0A 0A 07 07 0A 0A 00 00 04 00 01 02 02 02 01 01 01 01 80 03 03 01 02 00 00 00 02 02 02 01 02 02 04 02 01 01 02 00 00 00 01 03 00 01 03 00 01 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 00 00 00 00 00 00 00 01 00 01 01 00 00 02 01 00 00 80 00 00 00 00 84 03 01 03 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 02 01 80 01 02 01 01 01 01 01 02 01 03 02 01 80 01 80 02 02 02 01 01 01 02 05 03 80 01 06 01 03 01 10 01 00 03 03 01 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 02 01 03 01 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 01 01 00 00 00 00 02 04 03 02 01 01 01 02 02 02 04 82 01 02 01 01 02 03 02 03 01 01 02 02 01 01 01 01 01 02 02 02 04 01 02 01 01 01 01 01 03 02 00 00 02 80 02 02 02 01 01 02 01 02 02 01 02 03 01 03 02 02 01 01 01 01 01 01 01 01 00 01 04 01 02 01 02 05 02 02 02 04 08 08 08 08 03 02 01 04 02 01 02 02 01 01 01 02 01 01 01 03 01 01 01 00 00 00 00 00 00 01 02 03 01 02 01 10 03 01 01 01 02 02 02 01 01 03 01 04 02 04 01 01 01 01 01 02 03 03 05 05 02 00 01 01 02 01 01 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 02 01 02 02 01 01 02 01 01 01 01 01 00 01 04 00 00 00 02 01 00 02 01 01 04 04 00 00 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 02 02 05 08 08 02 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 01 02 01 02 02 02 02 01 02 02 02 01 01 01 02 01 01 02 02 01 01 02 01 02 02 01 02 01 01 01 01 02 01 01 01 01 02 01 01 01 01 01 02 01 01 01 00 01 01 01 01 01 02 02 02 01 01 01 01 02 01 01 01 01 01 01 02 02 01 02 02 01 01 02 01 01 01 00 01 01 01 01 01 01 01 02 01 01 01 01 01 02 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 02 02 01 01 01 01 02 02 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 02 02 00 01 01 01 01 01 01 02 02 02 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 02 02 02 02 02 02 01 02 02 02 01 02 02 02 01 01 02 02 01 01 02 02 02 02 01 01 00 02 02 02 02 02 01 02 02 02 01 02 00 01"
        # self.sd_tester.write_ccp_value(ccp)


    def before_each_func(self, ecu):
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()

    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        sleep(1)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

    #在白天，进入自动模式近光灯自动关闭
    def auto_low_beam_off_by_enter_day_mode(self,usage_mode:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.bus_comm.set_day_mode()
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    
    #从白天进入晚上，自动近光灯自动打开
    def auto_low_beam_on_by_enter_night_mode(self,usage_mode:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.bus_comm.set_day_mode()
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    
    #UsageMode 切换到Convenience以及以上，自动近光灯自动打开
    def auto_low_beam_on_by_transfer_usage_mode(self,usage_mode_start:UsageMode,usage_mode_target:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode_start,car_mode=car_mode)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=usage_mode_target)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)


    #UsageMode 切换到Convenience以及以下，自动近光灯自动熄灭
    def auto_low_beam_off_by_transfer_usage_mode(self,usage_mode_start:UsageMode,usage_mode_target:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode_start,car_mode=car_mode)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=usage_mode_target)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    
    #从晚上进入白天，自动近光灯自动熄灭
    def auto_low_beam_off_by_enter_from_night_to_day(self,usage_mode:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode()
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode()
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)


    #从进入白天，自动近光灯自动不会打开
    def auto_low_beam_off_in_day(self,usage_mode:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.mix.set_and_check_low_beam(sts=isOn.Off)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    
    #从进入白天，自动切手动，近光灯被点亮
    def auto_low_beam_on_by_auto_to_manual_in_day(self,usage_mode:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.bus_comm.set_day_mode()
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)


    #进入晚上，手动切换到自动，近光灯保持点亮
    def auto_low_beam_keep_on_manual_to_auto_in_night(self,usage_mode:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.bus_comm.set_night_mode()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    
    #进入晚上，自动切换到手动，近光灯保持点亮
    def auto_low_beam_keep_on_auto_to_manual_in_night(self,usage_mode:UsageMode,car_mode:CarMode):
        self.mix.set_common_precontion(usage_mode=usage_mode,car_mode=car_mode)
        self.bus_comm.set_night_mode()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)


    def check_turn_lamp_flash(self,pos:GeneralPos,sts:isOn,last_time:int):
        start_time = time.time()
        logger.info(f"----------->Check Start{start_time}")
        for num in range(last_time):
            if sts.name == "On":
                if pos.name == "Left":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Left,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeOn)
                elif pos.name == "Right":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Right,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
                elif pos.name == "All":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)

                if pos.name == "Left":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Left,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
                elif pos.name == "Right":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Right,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.Off)
                elif pos.name == "All":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
            
            if sts.name == "Off":
                if pos.name == "Left":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Left,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.Off)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeOn)
                elif pos.name == "Right":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.Right,act_sts_le=PosnLampSts.Off,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.RiOn)
                elif pos.name == "All":
                    self.bus_comm.check_outside_turn_lamp_act_sts(pos=GeneralPos.All,act_sts_le=PosnLampSts.On,act_sts_ri=PosnLampSts.On)
                    self.bus_comm.check_active_indicator_lamp_req(indcr_sts=IndcrSts.LeAndRiOn)
                sleep(0.9)

        stop_time = time.time()
        logger.info(f"----------->Check Stop{stop_time}")
        test_duration = stop_time - start_time 
        logger.info(f"----------->Check 信号跳变执行时间{test_duration},时间差为{test_duration - last_time}")
        if abs(test_duration - last_time) > 2:
            assert False

    @allure.title("Normal Convenience_手动开启近光")
    @pytest.mark.full
    def test_caseid_113263(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Active_手动开启近光")
    @pytest.mark.full
    def test_caseid_113313(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY
        )
        self.mix.set_lb_off_and_night_mode_sped0()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Convenience_手动开启近光")
    @pytest.mark.full
    def test_caseid_113325(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY
        )
        self.mix.set_lb_off_and_night_mode_sped0()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Driving_手动开启近光")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113323(self):
       self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
       self.mix.set_lb_off_and_night_mode_sped0()
       self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
       self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
       self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Active_手动关闭近光")
    @pytest.mark.full_001
    def test_caseid_113274(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.mix.set_and_check_low_beam(sts=isOn.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode_手动切自动夜晚继续被点亮")
    @pytest.mark.full
    def test_caseid_114749(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT
        )
        self.mix.set_lb_off_and_night_mode_sped0()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(
            actn_sts=isOn.On, extr_light_sts=ExtrLtgSts.On
        )

    @allure.title("Transport Active_手动开启近光")
    @pytest.mark.full_002
    def test_caseid_113358(self):
        self.mix.set_common_precontion(
            usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT
        )
        self.mix.set_lb_off_and_night_mode_sped0()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Convenience_手动关闭近光")
    @pytest.mark.full_002
    def test_caseid_113287(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        sleep(1)
        self.mix.set_and_check_low_beam(sts=isOn.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving自动近光夜晚切白天熄灭")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_115069(self):
       self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
       self.mix.set_lb_off_and_night_mode_sped0()
       self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
       self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
       self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
       self.bus_comm.set_day_mode()
       self.bus_comm.check_low_beam_act_sts(
           actn_sts=isOn.Off, extr_light_sts=ExtrLtgSts.Off)


    @allure.title("Normal Driving手动近光夜晚切白天熄灭")
    @pytest.mark.smoke
    @pytest.mark.lobeam
    def test_caseid_114791(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Convenience mode_夜晚自动被关闭近光灭")
    @pytest.mark.smoke
    @pytest.mark.lobeam
    def test_caseid_115068(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        sleep(2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving近光单边失效信号双侧不会关_使用模式正常HCM近光开右近光故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113520(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Normal Driving近光单边失效信号双侧不会关_使用模式正常HCM近光开左近光故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    @pytest.mark.mcu_test
    def test_caseid_113519(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Normal active夜晚自动被关近光灭")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113445(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal active手动切自动白天近光灭")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113448(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving安全要求_近光单边失效_左近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113450(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)

    @allure.title("Normal Driving_手动开启近光")
    @pytest.mark.smoke
    @pytest.mark.lobeam
    def test_caseid_113270(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Driving_手动关闭近光")
    @pytest.mark.smoke
    @pytest.mark.lobeam
    def test_caseid_113289(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving_手动开启近光Driving变Inactive熄灭")
    @pytest.mark.smoke
    @pytest.mark.lobeam
    def test_caseid_113299(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving_手动切自动夜晚继续被点亮")
    @pytest.mark.smoke
    @pytest.mark.lobeam
    def test_caseid_114773(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Driving_白天自动切手动近光被点亮")
    @pytest.mark.smoke
    @pytest.mark.lobeam
    def test_caseid_114795(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Driving_自动近光白天切夜晚被点亮")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_114786(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Driving_夜晚自动近光关闭近光灭")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_114799(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving_自动近光夜晚切白天熄灭")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_114836(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving_夜晚自动切手动近光继续被点亮")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_114854(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Driving_自动近光夜晚被点亮")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_114869(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Driving_自动近光夜晚白天未被点亮")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_114876(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("abandone下近光关CDC断连BGM保持近光关")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_1900121(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.stop_get_light_inhibit_sts()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.start_get_light_inhibit_sts()

    @allure.title("convenience下近光关CDC断连BGM保持近光关")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_1900119(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.stop_get_light_inhibit_sts()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.start_get_light_inhibit_sts()

    @allure.title("BGM上电30s内不检测通道阻塞近光可控")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_1900118(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.io.io_reset_bgm()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(31)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("convenience模式下近光开电源复位近光600ms内打开并保持")
    @pytest.mark.full
    def test_caseid_113497(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.bus_comm.set_vehspd_and_qf(vehspd=0.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(3)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Driving模式下近光开电源复位近光600ms内打开并保持")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113495(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode_夜晚自动切手动近光继续被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_111385(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)


    @allure.title("Driving下近光关CDC断连BGM主动设置外灯Auto")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_113532(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.stop_get_light_inhibit_sts()
        sleep(5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.start_get_light_inhibit_sts()

    @allure.title("active下近光开CDC断连BGM主动设置外灯Auto")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_113533(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.stop_get_light_inhibit_sts()
        sleep(5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.start_get_light_inhibit_sts()

    @allure.title("Driving下近光开CDC断连BGM主动设置外灯Auto")
    @pytest.mark.smoke
    @pytest.mark.lowbeam
    def test_caseid_113534(self):
        self.bus_comm.set_vehmtn(vehmtnst=VehMtnSts.StandStillVal3)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.stop_get_light_inhibit_sts()
        sleep(5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.start_get_light_inhibit_sts()


    @allure.title("Normal Driving mode VDDM踩刹车紧急制动EBL请求点亮后雾灯_请求结束熄灭后雾灯")
    @pytest.mark.smoke
    @pytest.mark.rearfog
    def test_caseid_113316(self):
        self.mix.set_ccp({508:0x03,255:0x02,114:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(5)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode BBM紧急制动EBL请求点亮刹车灯后雾灯同步点亮_请求结束熄灭后雾灯")
    @pytest.mark.smoke
    @pytest.mark.rearfog
    def test_caseid_113298(self):
        self.mix.set_ccp({508:0x03,255:0x02,114:0x03})
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(5)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)


    @allure.title("关闭LoBeam时FPL同步关闭_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113759(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        sleep(2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("后位置灯激活条件_开关处于Auto 位置_Factory Active mode")
    @pytest.mark.smoke
    @pytest.mark.position
    @pytest.mark.mcu_test
    def test_caseid_113824(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113749(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("关闭LoBeam时RPL同步关闭_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    @pytest.mark.mcu_test
    def test_caseid_113789(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        sleep(2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    @pytest.mark.mcu_test
    def test_caseid_113666(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113693(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_激活LoBeam时RPL同步点亮_Normal Driving mode")
    @pytest.mark.smoke
    def test_caseid_113705(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_激活LoBeam时FPL同步点亮_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113677(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关处于Auto 位置_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    @pytest.mark.mcu_test
    def test_caseid_113809(self):
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.set_night_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("开关POS位改变使用模式关闭后位置灯_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    @pytest.mark.mcu_test
    def test_caseid_113779(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Normal Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113748(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)


    @allure.title("开关POS位改变使用模式关闭前位置灯_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113754(self):
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.set_night_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("ASIL近光功能失活前提速度冗余_Active模式下近光关电源复位近光600ms内打开并保持")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113502(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.sd_tester.send_data([0x11,0x01])
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(.3)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("ASIL近光功能失活前提速度冗余_Active模式下近光开电源复位近光600ms内打开并保持")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113496(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(15)

    @allure.title("ASIL近光功能失活前提速度冗余_Active模式下近光开电源复位近光重新打开后手动关闭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113506(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(15)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("ASIL近光功能失活前提速度冗余_Convenience式下近光开电源复位近光重新打开后手动关闭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113509(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(3)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(3)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("ASIL近光功能失活前提速度冗余_Driving模式下近光开电源复位近光重新打开后手动关闭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113505(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(15)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("ASIL近光功能失活前提速度冗余_Convenience模式下夜晚AUTO近光开电源复位近光重新打开后切换白天")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113514(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(3)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(2)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("ASIL近光功能失活前提速度冗余_Active模式下夜晚AUTO近光开电源复位近光重新打开后切换白天")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113512(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode(wait_time=15)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)  

    @allure.title("ASIL近光功能失活前提速度冗余_Driving模式下夜晚AUTO近光开电源复位近光重新打开后切换白天")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113510(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        sleep(3)
        self.bus_comm.set_night_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.io.io_reset_bgm()
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode(wait_time=15)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)  

    @allure.title("ASIL近光功能失活前提速度冗余_车速大于3km|h,QF=0or1")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113480(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=3.2,veh_qf=VehSpdQf.UndefindDataAccur)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)

    @allure.title("ASIL近光功能失活前提速度冗余_车速大于3km|h,QF=0or1昼夜变化")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113494(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=3.2,veh_qf=VehSpdQf.UndefindDataAccur)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)

    @allure.title("ASIL近光功能失活前提速度冗余_车速大于3km|h改变使用模式")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113472(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=3.2)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("ASIL近光功能失活前提速度冗余_车速等于3km|h改变使用模式")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113476(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=3)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("ASIL近光功能失活前提速度冗余_车速小于3km|h改变使用模式")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113478(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=2.9)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("ASIL近光功能失活前提速度冗余_车速大于3km|h，QF=0or1手动关闭近光灯")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113485(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=3.2,veh_qf=VehSpdQf.UndefindDataAccur)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)
        
    @allure.title("Crash Active mode_夜晚自动被关闭近光灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114898(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Crash Active mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113412(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Crash Convenience mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113418(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Crash Active mode_手动切自动白天近光熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_115009(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Crash Active mode_白天自动切手动近光被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113409(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("Crash Convenience mode手动点亮的近光Convenience变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113430(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Crash driving mode_手动切自动白天近光熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114734(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode手动点亮的近光Driving变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113423(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Crash driving mode_白天自动切手动近光被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_115030(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("Crash Driving mode手动点亮的近光Driving变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113423(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Crash手动开关打开Abandoned变为Active点亮近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114878(self):
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.mix.set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
    
    @allure.title("Crash手动开关打开Abandoned变为Driving点亮近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114841(self):
        self.mix.set_car_mode(car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.mix.set_usage_mode(usage_mode=UsageMode.ABANDONED)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("Factory active mode_手动切自动白天近光熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114787(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Factory active mode_夜晚自动被关闭近光灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114775(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Factory active mode_白天自动切手动近光被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114817(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode_夜晚自动被关闭近光灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114780(self):
        self.bus_comm.set_night_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Factory Driving mode_手动切自动夜晚继续被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114872(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("Factory Driving mode_手动切自动白天近光熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114743(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Normal Driving_自动近光夜晚白天未被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114986(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from Abondoned to Active")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113867(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from Abondoned to CONVENIENCE")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113866(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from Abondoned to DRIVING")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113868(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from Abondoned to INACTIVE")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113865(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from inactive to active")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113870(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from inactive to CONVENIENCE")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113869(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from inactive to DRIVING")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113871(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode changing from inactive to INACTIVE")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113872(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode is Active打开位置灯开关激活位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113878(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode is Active打开近光灯开关激活位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113879(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode is CONVENIENCE打开近光灯开关激活位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113876(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        sleep(1)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode is CONVENIENCE打开近光灯开关激活位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113877(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)

    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode is Driving打开位置灯开关激活位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113880(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)

    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode is Driving打开近光灯开关激活位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113881(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)



    @allure.title("位置灯激活|关闭的特殊要求_激活|禁用依赖使用模式_usage mode is Inactive打开近光灯开关激活位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113875(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off) 
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("前位置灯激活条件_开关处于Auto 位置_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113815(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)

    @allure.title("关闭LoBeam时RPL同步关闭_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113793(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活条件_开关处于Auto 位置_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113859(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活条件_激活LoBeam时FPL同步点亮_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113681(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Factory Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113668(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("关闭LoBeam时RPL同步关闭_Crash DRIVING mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113795(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("后位置灯激活条件_开关处于Auto 位置_Crash Driving mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113829(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关处于Auto位置_Factory Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113812(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关处于Auto 位置_Normal Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113807(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("关闭LoBeam时RPL同步关闭_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113793(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活条件_开关处于Auto 位置_Crash Driving mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113817(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_激活LoBeam时FPL同步点亮_Normal Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113675(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Active mode下激活近光灯不点亮位置灯")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113679(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭后位置灯_Crash Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113785(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("后位置灯激活过程_开关POS位置后位置灯贯穿灯故障_默认后位置灯满足激活条件")
    @pytest.mark.full
    def test_caseid_113729(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Mid,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)


    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Normal Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113664(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Normal Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113665(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113666(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        

    @allure.title("开关auto位改变使用模式关闭前位置灯_Crash Driving change to Inactive")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113850(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("开关auto位改变使用模式关闭前位置灯_Crash Active change to Inactive")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113849(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("关闭LoBeam时RPL同步关闭_Normal Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113787(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.All,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("开关Auto位改变使用模式关闭前位置灯_Normal Convenience change to Inactive")
    @pytest.mark.smoke
    def test_caseid_113842(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_car mode is factory and usagemode change to inactive from abandoned")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113667(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.FACTORY)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Factory Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113669(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Factory Driving mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113670(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Factory Driving mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113671(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.CRASH)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113672(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Crash Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113673(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关POS位开启前位置灯_Crash Driving mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113674(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_激活LoBeam时FPL同步点亮_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.position
    def test_caseid_113676(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_激活LoBeam时FPL同步点亮_Crash Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113681(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_激活LoBeam时FPL同步点亮_Crash Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113682(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_激活LoBeam时FPL同步点亮_Crash driving mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113683(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_car mode is normal and usagemode change to inactive from abandoned")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113690(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_自动近光夜晚切白天熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_111391(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_自动近光夜晚切白天熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113255(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Crash Active mode_自动近光夜晚切白天熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113301(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Convenience mode手动点亮的近光Convenience变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113309(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory active mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113329(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Convenience mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113337(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory driving mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113343(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory driving mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113344(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Active mode手动点亮的近光Active变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113351(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Convenience mode手动点亮的近光Convenience变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113354(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_手动开启近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113362(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Transport CONVENIENCE mode_手动开启近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113366(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Transport Active mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113374(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport CONVENIENCE mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113376(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113380(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode手动点亮的近光Active变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113388(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Convenience mode手动点亮的近光Convenience变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113394(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_手动开启近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113398(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.mix.set_lb_off_and_night_mode_sped0
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Crash Driving mode_手动开启近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113406(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.mix.set_lb_off_and_night_mode_sped0
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Crash driving mode_手动关闭近光")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113421(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode手动点亮的近光Active变为Inactive熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113427(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode_自动近光夜晚被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113435(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode_自动近光白天未被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113436(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode_自动近光白天切夜晚被点亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113441(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode_自动近光夜晚切白天熄灭")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113442(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("安全要求_近光单边失效_右近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113452(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("安全要求_近光单边失效_近光双侧故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113457(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Normal Driving mode近光已激活通过大屏开关打开后雾灯")
    @pytest.mark.smoke
    @pytest.mark.rearfog
    def test_caseid_113482(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extr_light_rear_fog_mode(mode=LightMode.On)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("CC#114=[2] Normal Driving mode 踩刹车触发紧急制动后解除紧急自动刹车灯不再闪烁")
    @pytest.mark.smoke
    @pytest.mark.brake
    def test_caseid_115389(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_pedal()
        self.bus_comm.set_brake_pedal()
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
        self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)

    @allure.title("normal driving远光未激活手动打闪光后失活")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113563_113543(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,ccp={629:4})
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113254(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_远光激活手动打闪光后继续亮远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113604(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=3,hbsts_prty=LowBeamClientId.Voice)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_闪光未激活手动近光开通过领航辅助ANP或自适应远光控制AHBC激活远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113638(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_手动近光和闪光开启然后请求开远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113612(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        # self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113631(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        # self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_闪光未激活自动近光开通过AVP激活远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113639(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        # self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113623(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        # self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Normal Driving mode_闪光未激活自动近光开通过ANP或AHBC激活远光")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113647(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        # self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=6,hbsts_prty=LowBeamClientId.AHBC)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)    
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=6,hbsts_prty=LowBeamClientId.AHBC)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=6,hbsts_prty=LowBeamClientId.NoFunc)
        
    @allure.title("Normal Driving mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.smoke
    @pytest.mark.highbeam
    def test_caseid_113582(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={629:4})      
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)
        

    @allure.title("Low beam激活|失活过程_手|自动近光开左近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113521(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        
    @allure.title("Low beam激活|失活过程_手|自动近光开右近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113522(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        
    @allure.title("Low beam激活|失活过程_手|自动近光开近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113523(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)
        
    @allure.title("Low beam激活|失活过程_手|自动近光开启正常")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113524(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        
    @allure.title("Low beam激活|失活过程_手|自动近光关闭")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113525(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        
    @allure.title("Low beam激活|失活过程_打开近光复用DRL左DRL故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113526(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_drl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Err)

        
    @allure.title("Low beam激活|失活过程_打开近光复用DRL左DRL故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113529(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_drl_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.On)


    @allure.title("Low beam激活|失活过程_打开近光复用DRL右DRL故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113527(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_drl_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Low beam激活|失活过程_打开近光复用DRL左右DRL故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113528(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_drl_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Err)
        
    @allure.title("CC#114=[2] Normal Driving mode 踩刹车触发紧急制动闪烁所有刹车灯")
    @pytest.mark.smoke
    def test_caseid_115404(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_pedal()
        sleep(1)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        
    @allure.title("CC#114=[2] Normal Driving mode 请求点亮刹车灯时触发紧急制动闪烁所有刹车灯")
    @pytest.mark.smoke
    def test_caseid_115392(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={114:2})
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)
        sleep(1)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.Reqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.InProgs)
        for num in range(3):
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.Off,mid_lamp_sts=isOn.Off)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.Off)
            sleep(.15)
            self.bus_comm.check_brake_light_act_sts(lamp_sts=isOn.On,mid_lamp_sts=isOn.On)
            self.bus_comm.check_brake_light_sts(sts=ExtrLtgSts.On)
        self.bus_comm.set_brake_req_light_on_sts(sts=ReqSts.NotReqd)
        self.bus_comm.set_emergency_brake_req_light_on_sts(req=EmgyBrkLiReq.NotInProgs)

    
    @allure.title("Crash Active mode_手动切自动夜晚继续被点亮")
    @pytest.mark.full
    def test_caseid_115072(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_day_mode()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title(" Normal模式，使用模式Abandoned变为Driving点亮近光")
    @pytest.mark.full
    def test_caseid_114916(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    
    @allure.title("Factory Convenience mode_手动切自动夜晚继续被点亮")
    @pytest.mark.full
    def test_caseid_114908(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_day_mode()
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    
    @allure.title("Normal Convenience mode_自动近光白天切夜晚被点亮")
    @pytest.mark.full
    def test_caseid_114901(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)


    @allure.title("Factory active mode_自动近光夜晚被点亮")
    @pytest.mark.full
    def test_caseid_114899(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_day_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode_手动切自动夜晚继续被点亮")
    @pytest.mark.full
    def test_caseid_114897(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    
    @allure.title("Transport Covenience mode_自动近光白天切夜晚被点亮")
    @pytest.mark.full
    def test_caseid_114895(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_day_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_night_mode()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
    
    @allure.title("Factory手动开关打开Inactive变为Active点亮近光")
    @pytest.mark.full
    def test_caseid_114884(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)


    @allure.title("Normal手动开关打开Inactive变为Convenience点亮近光")
    @pytest.mark.full
    def test_caseid_114882(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        # self.mix.set_and_check_low_beam(sts=isOn.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    
    @allure.title("Transport手动开关打开Abandoned变为Active点亮近光")
    @pytest.mark.full
    def test_caseid_114880(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.TRANSPORT)
        self.mix.set_and_check_low_beam(sts=isOn.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Low beam激活|失活过程_手|自动近光开左近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113521(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Low beam激活|失活过程_手|自动近光开右近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113522(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Low beam激活|失活过程_手|自动近光开近光灯故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113523(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_low_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err)

    @allure.title("Low beam激活|失活过程_手|自动近光开启正常")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113524(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Low beam激活|失活过程_手|自动近光关闭")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113525(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Low beam激活|失活过程_打开近光复用DRL左DRL故障")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113526(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.set_drl_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Err)