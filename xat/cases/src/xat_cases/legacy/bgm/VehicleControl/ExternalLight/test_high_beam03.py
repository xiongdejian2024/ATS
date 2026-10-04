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
@allure.story("远光灯")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.mix.write_vehicle_model_ccp(vehicle_model=VehicleType.Mars, vehicle_mca=VehicleMca.Mca_400v)
        self.soa.update(["LightService_client","CentralLockService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        sleep(5)

    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        sleep(2)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)

   
    @allure.title("Factory Driving mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113590(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113580(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113584(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off) 

    @allure.title("Normal Convenience mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113581(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113586(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113262(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113630(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
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

    @allure.title("Transport Active mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_115011(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode()
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

    @allure.title("Transport Driving mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113633(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
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

    @allure.title("Transport Active mode_远光激活手动打闪光后继续亮远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113605(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode_闪光未激活手动近光开通过AHBC激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113640(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode_闪光未激活自动近光开通过AHBC激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113648(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Convenience mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_113567(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("AHBC打开远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_1913467(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("语音打开远光")
    @pytest.mark.full
    @pytest.mark.highbeam07
    def test_caseid_1913463(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=3)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
    

    # @allure.title("Factory Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    # @pytest.mark.full
    # @pytest.mark.highbeam
    # def test_caseid_113587(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
    #     sleep(.5)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    # @allure.title("Normal Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    # @pytest.mark.full
    # @pytest.mark.highbeam06
    # def test_caseid_113579(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
    #     sleep(.5)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)
    
    
   # @allure.title("Factory Convenience mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    # @pytest.mark.full
    # @pytest.mark.highbeam
    # def test_caseid_113589(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
    #     sleep(.5)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off) 

    # @allure.title("Transport Active mode_远光未激活手动打闪光后失活")
    # @pytest.mark.full
    # @pytest.mark.highbeam06
    # def test_caseid_113566(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    # @allure.title("Transport Active mode_闪光未激活手动近光远光开手动关闭远光")
    # @pytest.mark.full
    # @pytest.mark.highbeam
    # def test_caseid_113632(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
    #     self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
    #     self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
    #     sleep(1)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    # @allure.title("Transport Convenience mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    # @pytest.mark.full
    # @pytest.mark.highbeam
    # def test_caseid_113585(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
    #     sleep(.5)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off) 

    # @allure.title("Transport Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    # @pytest.mark.full
    # @pytest.mark.highbeam
    # def test_caseid_113583(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
    #     sleep(.5)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    # @allure.title("游戏模式关闭远光")
    # @pytest.mark.full
    # @pytest.mark.highbeam06
    # def test_caseid_1913466(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
    #     self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
    #     self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
    #     self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)
    #     self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)
    #     self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.Off,hbid_value=1)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    # @allure.title("Crash Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    # @pytest.mark.full
    # @pytest.mark.highbeam
    # def test_caseid_113591(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
    #     sleep(.5)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    # @allure.title("Crash Convenience mode_近光远光关手动打远光后打远光提示不满足远光激活条件")
    # @pytest.mark.full
    # @pytest.mark.highbeam
    # def test_caseid_113593(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
    #     self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
    #     self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
    #     self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
    #     sleep(.5)
    #     self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)