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
        # self.mix.write_vehicle_model_ccp(vehicle_model=VehicleType.Mars, vehicle_mca=VehicleMca.Mca_400v)
        self.soa.update(["LightService_client","CentralLockService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.start_get_light_inhibit_sts()
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_extral_light_button_to_defaul_sts()
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        sleep(5)

    def after_each_func(self, ecu):
        self.soa.stop_get_light_inhibit_sts()
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        sleep(2)

    def after_class(self, ecu):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.change_car_mode(CarMode.NORMAL)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)


    @allure.title("Normal Driving mode_远光未激活手动打闪光")
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

    @allure.title("AVP打开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_1913465(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=5,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.On,LowBeamClientId.NoFunc)

    @allure.title("远光ANP占用开AHBC无法关闭")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_1913462(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.Off,hbid_value=6)
        sleep(2)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=4,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)

    @allure.title("远光ANP占用关AHBC无法打开")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_118862(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        sleep(2)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=4,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)

    @allure.title("High beam激活过程_手动闪光正常关闭")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113662(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.recover_extral_light_to_defaul_sts()
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("High beam激活过程_手动远光开左远光灯故障")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113653(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_闪光未激活自动近光开通过ANP或AHBC激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113652(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=4,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)

    @allure.title("Normal Driving mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113578(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Factory Active mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113588(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)
        
    @allure.title("Crash Active mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113592(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113594(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)
    
    @allure.title("方控超车时游戏模式关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_1913468(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        sleep(1)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)

    @allure.title("Transport Driving mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_111388(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_night_mode()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

     #-------------------------------------------------------------------------------------------------------------------------------------------------
     
    @allure.title("Factory Active mode_闪光未激活自动近光开通过AHBC激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113650(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=6)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=6,hbsts_prty=LowBeamClientId.NoFunc)
    
    @allure.title("ANP打开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_1913464(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        # 恢复
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=4,hbsts_prty=LowBeamClientId.NoFunc)
    
    @allure.title("Crash Active mode_自动近光和闪光开启然后请求开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113628(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113556(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Crash Active mode_远光未激活手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113576(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_远光激活手动打闪光后继续亮远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113609(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Active mode_闪光未激活手动近光开通过AHBC激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113644(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=6,hbsts_prty=LowBeamClientId.AHBC)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=6,hbsts_prty=LowBeamClientId.NoFunc)

    @allure.title("Crash Convenience mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113577(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Convenience mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113557(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        
    @allure.title("Crash Driving mode_自动近光和闪光开启然后请求开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113629(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113558(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Crash Driving mode_远光激活手动打闪光后继续亮远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113610(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode_闪光未激活手动近光开通过ANP激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113645(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=4,hbsts_prty=LowBeamClientId.NoFunc)

    @allure.title("Crash Inactive mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113574(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Inactive mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113554(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Active mode_自动近光和闪光开启然后请求开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113626(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Active mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113551(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Active mode_远光未激活手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113571(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Factory Active mode_闪光未激活手动近光开通过ANP激活远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113642(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=4,hbsts_prty=LowBeamClientId.ANP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=4,hbsts_prty=LowBeamClientId.NoFunc)

    @allure.title("Factory Convenience mode_手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113572(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Convenience mode_远光未激活手动打闪光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113552(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        sleep(0.5)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.get_high_beam_sts(HighBeamSts.Off,LowBeamClientId.NoFunc)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)

    @allure.title("Normal Active mode_自动近光和闪光开启然后请求开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113622(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode_自动近光和闪光开启然后请求开远光")
    @pytest.mark.full
    @pytest.mark.highbea
    def test_caseid_113624(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Transport Driving mode_自动近光和闪光开启然后请求开远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113625(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    @allure.title("Crash Active mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113636(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113637(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Crash Driving mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113283(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Active mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113634(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Active mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.highbeam
    def test_caseid_113277(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.bus_comm.set_night_mode()
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    def test_caseid_113579(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Transport Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    def test_caseid_113583(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Transport Convenience mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    def test_caseid_113585(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("在Inactive下无法通过服务开启远光灯")
    @pytest.mark.full
    def test_caseid_1988816(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=3)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=3,hbsts_prty=LowBeamClientId.NoFunc)

    @allure.title("在Abandoned下无法通过服务开启远光灯")
    @pytest.mark.full
    def test_caseid_1988817(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.On,hbid_value=3)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=3,hbsts_prty=LowBeamClientId.NoFunc)
    
    @allure.title("Normal Driving mode下CCP 274！=80 or 81点击远光灯按键无法打开远光灯")
    @pytest.mark.full
    def test_caseid_1990231(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL,ccp={274:0x82})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        # 恢复ccp
        self.mix.set_common_precontion(ccp={274:0x80})

    @allure.title("Dyno Driving mode下远光灯无法点亮")
    @pytest.mark.full
    def test_caseid_1990233(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={629:4})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Dyno Abandoned mode下手动闪光无法点亮")
    @pytest.mark.full
    def test_caseid_1994292(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO,ccp={629:4})
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨常亮_Transport Active mode")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995442(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨常亮_Factory Active mode")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995441(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨常亮_Crash Driving mode")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995440(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.io.hazard_light_open()
        self.io.hazard_light_close()
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨常亮_回拨关闭_Normal Driving mode")
    @pytest.mark.smoke
    @pytest.mark.pull
    def test_caseid_1995439(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨开启远光失败_Active Dyno mode")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995438(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.DYNO)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨开启远光失败_Abandoned Normal mode")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995437(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨开启远光失败_Inactive Normal mode")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995436(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_外拨开启远光失败_Convenience Normal mode")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995435(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_内拨一次_闪烁一次后关闭")
    @pytest.mark.smoke
    @pytest.mark.pull
    def test_caseid_1995434(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        sleep(1)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯关闭_内拨长拨_远光灯常亮_松手熄灭")
    @pytest.mark.smoke
    @pytest.mark.pull
    def test_caseid_1995433(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        sleep(1)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯常亮_外拨关闭远光灯")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995432(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯常亮_内拨一次_远光灯闪烁一次后常亮")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995431(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        sleep(.5)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        sleep(1)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        # 恢复
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("远光灯常亮_内拨长拨_远光灯熄灭_松手远光灯常亮")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995430(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        # 恢复
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("外拨打开远光灯_按键长按关闭远光灯")
    @pytest.mark.smoke
    @pytest.mark.pull
    def test_caseid_1995429(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("外拨打开远光灯_按键短按开闪光")
    @pytest.mark.smoke
    @pytest.mark.pull
    def test_caseid_1995428(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)   
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        # 恢复
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("外拨打开远光灯_语音关闭远光灯")
    @pytest.mark.smoke
    @pytest.mark.pull
    def test_caseid_1995427(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)   
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=3,hbsts_prty=LowBeamClientId.Voice)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("外拨打开远光灯_AVP关闭远光灯")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995426(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)   
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("外拨打开远光灯_游戏关闭远光灯")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995425(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)   
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd) 
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("内拨长拨打开远光灯_按键长按打开远光灯")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995424(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("内拨长拨打开远光灯_按键短按开闪光")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995423(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        
    @allure.title("内拨长拨打开远光灯_语音关闭远光灯")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995422(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=3,hbsts_prty=LowBeamClientId.Voice)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        
        
    @allure.title("内拨长拨打开远光灯_AVP关闭远光灯")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995421(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    
    @allure.title("内拨长拨打开远光灯_游戏关闭远光灯")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995420(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        
    @allure.title("游戏关闭远光灯_外拨开启远光灯失败")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995419(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
    
    @allure.title("游戏打开远光灯_内拨一次不闪烁")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995418(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        
    @allure.title("游戏打开远光灯_内拨长拨关闭远光灯失败")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995417(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        
    @allure.title("语音打开远光灯_外拨关闭远光灯")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995416(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=3,hbsts_prty=LowBeamClientId.Voice)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("语音关闭远光灯_内拨一次闪烁")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995415(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=3,hbsts_prty=LowBeamClientId.Voice)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("语音打开远光灯_内拨长拨_远光灯熄灭_松手远光灯常亮")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995414(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=3,hbsts_prty=LowBeamClientId.Voice)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("AVP打开远光灯_外拨关闭远光灯")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995413(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("AVP打开远光灯_内拨一次闪烁")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995412(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("AVP关闭远光灯_内拨长拨_远光灯开启_松手远光灯熄灭")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995411(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=5,hbsts_prty=LowBeamClientId.AVP)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("近光灯未开_外拨开远光失败")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995410(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("近光灯未开_内拨长拨闪光常亮")
    @pytest.mark.sanity
    @pytest.mark.pull
    def test_caseid_1995409(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd,pull_time=1)
        self.bus_comm.check_flash_lamp_always_on()
        
    @allure.title("外拨开启远光灯_左灯故障")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995408(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 2)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err,flash_light_sts=ExtrLtgSts.Off)
        # 恢复
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)
        
    @allure.title("内拨长拨开启远光灯_右灯故障_故障恢复远光灯恢复正常")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995407(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 1)
        sleep(1)
        self.bus_comm.check_flash_lamp_always_on()
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)
        sleep(1)
        self.bus_comm.check_flash_lamp_always_on()
        
    @allure.title("拨杆信号Error_外拨开启远光灯失败")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995406(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 2)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.Error)
        sleep(4)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        
    @allure.title("拨杆信号Error_内拨短拨远光灯不闪烁")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995405(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        
    @allure.title("拨杆信号Erro_外拨开启远光灯失败_拨杆信号恢复_外拨开启远光灯")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995404(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 2)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodycan.StleBodyFr01, 'LeverSwtLeLvrSwt2', 2)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off) 
        
    @allure.title("拨杆信号Error_内拨短拨远光灯不闪烁_拨杆信号恢复_内拨短拨开启闪光")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995403(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressInsd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        
    @allure.title("远光灯开_拨杆信号Error_外拨关闭远光灯失败")
    @pytest.mark.full
    @pytest.mark.pull
    def test_caseid_1995402(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        # 恢复
        self.bus_comm.set_high_beam_pull_in_out(gear=HighPressGear.PressOutd)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off) 

    @allure.title("Transport Active mode_远光未激活手动打闪光后失活")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_113566(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("Factory Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_113587(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.FACTORY)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Factory Convenience mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_113589(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Crash Inactive mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_113591(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.CRASH)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Crash Convenience mode_近光远光关手动打闪光后打远光提示不满足远光激活条件")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_113593(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.mix.set_lb_off_and_night_mode_sped0()
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.On)
        sleep(.5)
        self.bus_comm.check_hb_fail_flag_sts(hb_flag_sts=ExtrLtgSts.Off)

    @allure.title("Transport Active mode_闪光未激活手动近光远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_113632(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.TRANSPORT)
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

    @allure.title("Crash Active mode_闪光未激活自动近光开远光开手动关闭远光")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_114981(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.bus_comm.set_night_mode(wait_time=2)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
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
    
    @allure.title("游戏模式关闭远光")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1913466(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        # 游戏模式释放优先级
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)

    @allure.title("左侧远光灯故障时，右侧远光灯不受影响")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1990176(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Left,fault_sts=LampSts.On)

    @allure.title("Normal Convenice mode下远光灯无法点亮")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1990232(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("游戏模式打开远光灯")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994290(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        # 游戏模式释放优先级
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)

    @allure.title("Normal Inactive mode下远光灯无法点亮")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994291(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL,ccp={629:4})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("High beam激活过程_手动远光开左右远光灯故障")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994293(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.All,fault_sts=LampSts.On)
    
    @allure.title("High beam激活过程_手动远光开右远光灯故障")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994294(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.Error)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.Err,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_high_bean_fault_sts(pos=GeneralPos.Right,fault_sts=LampSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("按键打开远光_语音关闭远光")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994807(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        # 游戏模式释放优先级
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        
    @allure.title("游戏关闭远光_按键打开远光失败")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994808(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.soa.event_check_high_beam_switch_sts(sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Left3,sts=SteerWhlTouchSwtSts.LongPress)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        # 游戏模式释放优先级
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)

    @allure.title("游戏打开远光_释放优先级_语音关闭远光")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994809(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)        
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Off,hbid_value=3,hbsts_prty=LowBeamClientId.Voice)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)

    @allure.title("游戏打开远光_语音关闭远光失败")
    @pytest.mark.full
    @pytest.mark.hb_new1
    def test_caseid_1994810(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.On,hbid_value=1,hbsts_prty=LowBeamClientId.GameMode)        
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_high_beam_ctrl_cmd(cmd_value=HighBeamCmd.Off,hbid_value=3)
        self.bus_comm.check_high_beam_sts(hb_actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On,flash_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_and_event_check_high_beam_ctrl_sts(cmd_value=HighBeamCmd.Release,hbid_value=1,hbsts_prty=LowBeamClientId.NoFunc)