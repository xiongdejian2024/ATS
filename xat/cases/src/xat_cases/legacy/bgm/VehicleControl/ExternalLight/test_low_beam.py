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
        self.soa.update(["LightService_client","CentralLockService_client"])
        self.sd_tester.set_ccp(ccp_vlaue={274:0x80})
        sleep(2)

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
        # self.mix.set_and_check_low_beam(sts=isOn.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.sd_tester.change_usage_mode(usage_mode=usage_mode_target)
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


    #--------------------------------------------->下面的是近光灯的case<-----------------------------------------------------
    
    @allure.title("Normal Convenience mode_手动切自动夜晚继续被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114814(self):
        self.auto_low_beam_keep_on_manual_to_auto_in_night(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)

    
    @allure.title("Factory Convenience mode_夜晚自动切手动近光继续被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114813(self):
        self.auto_low_beam_keep_on_auto_to_manual_in_night(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)

    
    @allure.title("Crash手动开关打开Inactive变为Driving点亮近光")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114811(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.INACTIVE,
                                                     usage_mode_target = UsageMode.DRIVING,car_mode=CarMode.CRASH)

    
    @allure.title("Crash driving mode_自动近光夜晚被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114809(self):
        self.auto_low_beam_on_by_enter_night_mode(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)

    
    @allure.title("Crash手动开关打开Inactive变为Active点亮近光")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114808(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.INACTIVE,
                                                     usage_mode_target = UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        
    
    @allure.title("Factory手动开关打开Abandoned变为Convenience点亮近光")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114800(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.ABANDONED,
                                                     usage_mode_target = UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)

    
    @allure.title("Normal手动开关打开Abandoned变为Active点亮近光")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114797(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.ABANDONED,
                                                     usage_mode_target = UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
    

    @allure.title("Transport Active mode_白天自动切手动近光被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114793(self):
        self.auto_low_beam_on_by_auto_to_manual_in_day(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)


    @allure.title("Factory Convenience mode_自动近光白天未被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114792(self):
        self.auto_low_beam_on_by_auto_to_manual_in_day(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)


    
    # @allure.title("Transport Driving mode_夜晚自动切手动近光继续被点亮")
    # @pytest.mark.full
    # @pytest.mark.new
    # def test_caseid_114782(self):
    #     self.auto_low_beam_keep_on_auto_to_manual_in_night(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)

    @allure.title("Normal手动开关打开Inactive变为Active点亮近光")
    @pytest.mark.full
    def test_caseid_114767(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.INACTIVE,
                                                     usage_mode_target = UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
    
    @allure.title("Transport手动开关打开Inactive变为Driving点亮近光")
    @pytest.mark.full
    def test_caseid_114778(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.INACTIVE,
                                                     usage_mode_target = UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)

    
    @allure.title("Crash手动开关打开Abandoned变为Convenience点亮近光")
    @pytest.mark.full
    def test_caseid_114756(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.ABANDONED,
                                                     usage_mode_target = UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)

    
    @allure.title("Crash Active mode_夜晚自动切手动近光继续被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114772(self):
        self.auto_low_beam_keep_on_auto_to_manual_in_night(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)

    
    @allure.title("Factory Convenience mode_自动近光白天未被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114792(self):
        self.auto_low_beam_on_by_auto_to_manual_in_day(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)

    
    @allure.title("Crash Convenience mode_夜晚自动切手动近光继续被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114762(self):
        self.auto_low_beam_keep_on_auto_to_manual_in_night(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)

        
    @allure.title("Normal Convenience mode_夜晚自动切手动近光继续被点亮")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114745(self):
        self.auto_low_beam_keep_on_auto_to_manual_in_night(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)

    
    @allure.title("Normal Convenience mode_手动切自动白天近光熄灭")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114741(self):
        self.auto_low_beam_off_by_enter_day_mode(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
     
    @allure.title("Transport手动开关打开Abandoned变为Active点亮近光")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114880(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.ABANDONED,
                                                     usage_mode_target = UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)

    @allure.title("Transport手动开关打开Abandoned变为Active点亮近光")
    @pytest.mark.full
    @pytest.mark.new
    def test_caseid_114880(self):
        self.auto_low_beam_on_by_transfer_usage_mode(usage_mode_start=UsageMode.ABANDONED,
                                                     usage_mode_target = UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
    
    @allure.title("Crash Convenience mode_白天自动切手动近光被点亮")
    @pytest.mark.full
    def test_caseid_115053(self):
        self.bus_comm.set_day_mode()
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Convenience mode_自动切手动近光被点亮")
    @pytest.mark.full
    def test_caseid_111351(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_day_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Convenience mode_手动切自动近光继续点亮")
    @pytest.mark.full
    def test_caseid_114879(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.mix.set_and_check_low_beam(isOn.Off)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Convenience mode_自动近光夜晚被点亮")
    @pytest.mark.full
    def test_caseid_114784(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Crash Convenience mode_自动近光被点亮")
    @pytest.mark.full
    def test_caseid_114757(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal手动开关打开Inactive变为Driving点亮近光亮")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_114752(self):
        self.mix.set_car_mode(car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Crash Convenience mode_手动切自动近光继续点亮")
    @pytest.mark.full
    def test_caseid_114744(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_night_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("ASIL近光功能失活前提速度冗余_Driving模式下近光关电源复位近光600ms内打开并保持")
    @pytest.mark.full
    @pytest.mark.lowbeam
    def test_caseid_113499(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        sleep(.6)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Low beam激活|失活过程_打开近光关闭近光同步关闭DRL")
    @pytest.mark.full
    @pytest.mark.lobeam
    def test_caseid_113530(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_drl_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode_白天模式下lin1信号超时500ms近光开")
    @pytest.mark.full
    def test_caseid_1987188(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.pause_bus_send("cem_lin1")
        sleep(.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Convenience mode_自动近光白天未被点亮")
    @pytest.mark.full
    def test_caseid_114769(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_day_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("RLSM信号OutdBri丢失500ms，打开近光")
    @pytest.mark.full
    def test_caseid_1982364(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.pause_bus_send("cem_lin1")
        sleep(.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)

    @allure.title("近光功能故障保护_driving下近光开CEM HW故障开启静态近光")
    @pytest.mark.sanity
    def test_caseid_1994275(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        for i in range(10):
            self.io.io_reset_bgm(times=0.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        # 退出limp home
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(15)

    @allure.title("近光功能故障保护_active下近光开CEM HW故障开启静态近光")
    @pytest.mark.sanity
    def test_caseid_1994276(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        for i in range(3):
            self.io.io_reset_bgm(times=0.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        # 退出limp home
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(15)

    @allure.title("近光功能故障保护_driving下近光关CEM HW故障开启静态近光")
    @pytest.mark.sanity
    def test_caseid_1994277(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        for i in range(10):
            self.io.io_reset_bgm(times=0.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        # 退出limp home
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(15)

    @allure.title("近光功能故障保护_active下近光关CEM HW故障开启静态近光")
    @pytest.mark.sanity
    def test_caseid_1994278(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        for i in range(3):
            self.io.io_reset_bgm(times=0.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        # 退出limp home
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(15)

    @allure.title("在Inactive下无法通过服务开启近光灯")
    @pytest.mark.full
    @pytest.mark.lb_new
    def test_caseid_1988814(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("在Abandoned下无法通过服务开启近光灯")
    @pytest.mark.full
    @pytest.mark.lb_new
    def test_caseid_1988815(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Dyno Driving mode下近光灯无法点亮")
    @pytest.mark.full
    @pytest.mark.lb_new
    def test_caseid_1990234(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode下CCP 274！=80 or 81点击近光灯软开关无法打开近光灯")
    @pytest.mark.full
    def test_caseid_1990235(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={274:0x82})
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.sd_tester.set_ccp(ccp_vlaue={274:0x80})

    @allure.title("近光功能故障保护_abandoned下近光关CEM HW故障保持近光关")
    @pytest.mark.full
    @pytest.mark.lb_new
    def test_caseid_1994272(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        for i in range(3):
            self.io.io_reset_bgm(times=0.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(15)

    @allure.title("近光功能故障保护_convenience下近光关CEM HW故障保持近光关")
    @pytest.mark.full
    @pytest.mark.lb_new
    def test_caseid_1994273(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        for i in range(3):
            self.io.io_reset_bgm(times=0.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(15)

    @allure.title("近光功能故障保护_inactive下近光关CEM HW故障保持近光关")
    @pytest.mark.full
    @pytest.mark.lb_new
    def test_caseid_1994274(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        for i in range(3):
            self.io.io_reset_bgm(times=0.5)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        sleep(15)