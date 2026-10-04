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

    @allure.title("Factory Driving mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113635(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
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

    @allure.title("High beam激活过程_手动远光正常关闭")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113657(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
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

    @allure.title("Factory Driving mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113272(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
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

    @allure.title("Normal Active mode_远光激活手动打闪光后继续亮远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113603(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("High beam激活过程_手动闪光正常开启")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113661(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    
    @allure.title("Normal Active mode_远光未激活手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113561(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Inactive mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113559(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
     
    @allure.title("Normal Convenience mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113542(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Convenience mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113562(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Active mode_闪光未激活自动近光开通过AHBC激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113646(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
    
    @allure.title("Normal Active mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113541(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
    
    
    @allure.title("High beam激活过程_手动闪光开右远光灯故障")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113659(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Err)

    @allure.title("Factory Inactive mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113549(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Driving mode_远光激活手动打闪光后继续亮远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113608(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
    

    @allure.title("Factory Driving mode_闪光未激活手动近光开通过AHBC激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113643(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)


    @allure.title("Factory Inactive mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113569(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Inactive mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113544(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Transport Inactive mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113564(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_闪光未激活自动近光开通过ANP激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113649(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=4)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_闪光未激活手动近光开通过ANP激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113641(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=4)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_远光未激活手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113568(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113548(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
    
    @allure.title("Transport Convenience mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113547(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Transport Active mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113546(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Inactive mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113539(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)


    @allure.title("Factory Driving mode_闪光未激活自动近光开通过ANP激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113651(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=4)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)


    @allure.title("Factory Driving mode_远光未激活手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113573(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)


    @allure.title("Factory Driving mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113553(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        
    @allure.title("Factory Driving mode_自动近光和闪光开启然后请求开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113627(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("High beam激活过程_手动闪光开左远光灯故障")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113658(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Err)

    @allure.title("High beam激活过程_手动闪光开左右远光灯故障")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113660(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Err)
    
   