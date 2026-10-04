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
@allure.story("位置灯控制")
class TestExltlightCtrlABC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["LightService_client",'KeyService_client','CentralLockService_client'])
        self.sd_tester.set_ccp(ccp_vlaue={274:0x80})
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


    def check_postion_leam_normal(self,pos:GeneralPos):
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=pos,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=pos,extr_light_sts=ExtrLtgSts.On)

  
    @allure.title("关闭LoBeam时RPL同步关闭_Crash Active mode")
    @pytest.mark.full
    def test_caseid_113794(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("关闭LoBeam时RPL同步关闭_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113788(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("关闭LoBeam时FPL同步关闭_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113767(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("关闭LoBeam时FPL同步关闭_Crash Convenience mode")
    @pytest.mark.full
    def test_caseid_113765(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("关闭LoBeam时FPL同步关闭_Normal Driving mode")
    @pytest.mark.full
    def test_caseid_113759(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("关闭LoBeam时FPL同步关闭_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113758(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("关闭LoBeam时FPL同步关闭_Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_113757(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
    
    
    @allure.title("开关POS位改变使用模式关闭前位置灯_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113756(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Crash Active mode")
    @pytest.mark.full
    def test_caseid_113755(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Crash Convenience mode")
    @pytest.mark.full
    def test_caseid_113754(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113753(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("开关POS位改变使用模式关闭前位置灯_Factory Active mode")
    @pytest.mark.full
    def test_caseid_113752(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Factory Convenience")
    @pytest.mark.full
    def test_caseid_113751(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Normal Driving mode")
    @pytest.mark.full
    def test_caseid_113749(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113748(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关'POS'位改变使用模式关闭前位置灯_Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_113747(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭前位置灯_Crash Convenience change to Inactive")
    @pytest.mark.full
    def test_caseid_113848(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭前位置灯_Factory Driving change to Inactive")
    @pytest.mark.full
    def test_caseid_113847(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭前位置灯_Factory Active change to Inactive")
    @pytest.mark.full
    def test_caseid_113846(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭前位置灯_Factory Convenience change to Inactive")
    @pytest.mark.full
    def test_caseid_113845(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭前位置灯_Normal Driving change to Inactive")
    @pytest.mark.full
    def test_caseid_113844(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭前位置灯_Normal Active change to Inactive")
    @pytest.mark.full
    def test_caseid_113843(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活过程_开关POS位置前位置灯正常开启_默认前位置灯满足激活条件")
    @pytest.mark.full
    def test_caseid_113722(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.check_postion_leam_normal(pos=GeneralPos.Front)
   
    @allure.title("前位置灯激活条件_开关处于Auto位置_Crash Active mode")
    @pytest.mark.full
    def test_caseid_113816(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
    
    @allure.title("前位置灯激活条件_开关处于Auto位置_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113813(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关处于Auto位置_Factory Convenience mode")
    @pytest.mark.full
    def test_caseid_113811(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("前位置灯激活条件_开关处于Auto位置_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113808(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_113691(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)

    
    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113692(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)

    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113698(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)

    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Factory Active mode")
    @pytest.mark.full
    def test_caseid_113697(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)

    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Factory Convenience mode")
    @pytest.mark.full
    def test_caseid_113696(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)

    
    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Crash Convenience mode")
    @pytest.mark.full
    def test_caseid_113700(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)

    
    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Crash Active mode")
    @pytest.mark.full
    def test_caseid_113701(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)
    
    @allure.title("后位置灯激活条件_开关POS位开启后位置灯_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113702(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.check_postion_leam_normal(pos=GeneralPos.Rear)
    
    @allure.title("后位置灯激活条件_激活“LoBeam”时RPL同步点亮_Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_113703(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
    
    @allure.title("后位置灯激活条件_激活“LoBeam”时RPL同步点亮_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113704(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)



    @allure.title("后位置灯激活条件_激活“LoBeam”时RPL同步点亮_Crash Convenience mode")
    @pytest.mark.full
    def test_caseid_113710(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)


    @allure.title("后位置灯激活条件_激活“LoBeam”时RPL同步点亮_Crash Active mode")
    @pytest.mark.full
    def test_caseid_113711(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
    

    @allure.title("后位置灯激活条件_激活“LoBeam”时RPL同步点亮_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113712(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关处于Auto位置_Crash Active mode")
    @pytest.mark.full
    def test_caseid_113828(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关处于Auto 位置_Crash Convenience mode")
    @pytest.mark.full
    def test_caseid_113827(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关处于Auto位置_Factory Driving mode")
    @pytest.mark.full
    def test_caseid_113825(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关处于Auto位置_Factory Convenience mode")
    @pytest.mark.full
    def test_caseid_113823(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_开关处于Auto位置_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113820(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
    
    @allure.title("后位置灯激活条件_开关处于Auto位置_Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_113819(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Off)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("开关POS位改变使用模式关闭后位置灯_Crash Driving mode")
    @pytest.mark.full
    def test_caseid_113786(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
    
    
    @allure.title("开关POS位改变使用模式关闭后位置灯_Crash Convenience mode")
    @pytest.mark.full
    def test_caseid_113784(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭后位置灯_Normal Active mode")
    @pytest.mark.full
    def test_caseid_113777(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭后位置灯_Normal Convenience mode")
    @pytest.mark.full
    def test_caseid_113775(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("开关Auto位改变使用模式关闭后位置灯_Crash Driving change to Inactive")
    @pytest.mark.full
    def test_caseid_113857(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("开关Auto位改变使用模式关闭后位置灯_Crash Active change to Inactive")
    @pytest.mark.full
    def test_caseid_113856(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭后位置灯_Factory Driving change to Inactive")
    @pytest.mark.full
    def test_caseid_113854(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title(" 开关Auto位改变使用模式关闭后位置灯_Crash Convenience change to Inactive")
    @pytest.mark.full
    def test_caseid_113855(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.CRASH)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭后位置灯_Factory Active change to Inactive")
    @pytest.mark.full
    def test_caseid_113853(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭后位置灯_Factory Convenience change to Inactive")
    @pytest.mark.full
    def test_caseid_113852(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关Auto位改变使用模式关闭后位置灯_Normal Driving change to Inactive")
    @pytest.mark.full
    def test_caseid_113851(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("车辆能量水平EgyLvlElec对位置灯有特殊要求_低电量关闭位置灯_默认前后位置灯已激活")
    @pytest.mark.full
    def test_caseid_1986107(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.hmi_set_extilight_mode(mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
    
    @allure.title("后位置灯激活条件_开关处于Auto 位置_Normal Driving mode")
    @pytest.mark.smoke
    def test_caseid_113821(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯激活条件_激活LoBeam时RPL同步点亮_Factory Active mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113708(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.FACTORY)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_low_beam_act_sts(actn_sts=isOn.On,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("开关POS位改变使用模式关闭前位置灯_Normal Convenience mode")
    @pytest.mark.full
    @pytest.mark.position
    def test_caseid_113747(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活过程_开关POS位置前位置灯左右故障_默认前位置灯满足激活条件")
    @pytest.mark.full
    def test_caseid_113721(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Left,sts=PosnLampSts.Error)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Right,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Err)
        # 恢复
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Left,sts=PosnLampSts.On)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Right,sts=PosnLampSts.On)

    @allure.title("前位置灯激活过程_开关POS位置前位置灯左故障_默认前位置灯满足激活条件")
    @pytest.mark.full
    def test_caseid_113719(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Left,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Err)
        # 恢复
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Left,sts=PosnLampSts.On)

    @allure.title("后位置灯将请求排除安全要求_车速大于3km|h_2000ms内E2E校验和不正确_昼夜传感器变为白天")
    @pytest.mark.full
    def test_caseid_1988606_1988609(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=3.2)
        self.bus_comm.ipdu.set_no_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06')
        sleep(2)
        self.bus_comm.set_day_mode(wait_time=2)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.ipdu.restore_crc(self.bus_comm.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06')
        self.bus_comm.set_vehspd_and_qf(vehspd=0)

    @allure.title("后位置灯通讯执行器 IF 安全要求_后位置灯不被错误的关闭_连续的有效请求少于两个")
    @pytest.mark.full
    def test_caseid_1988610(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_singal("bodyexposedcanfd","BgmBodyExposedCANFr10", "SetOfPosnLampScopeReq",2)
        self.bus_comm.set_singal("bodyexposedcanfd","BgmBodyExposedCANFr10", "SetOfPosnLampScopeReq",2)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("后位置灯内部通信安全要求_one bit改变不够关闭后位置灯_SoftLiBtnSwtSetReq请求关闭位置灯")
    @pytest.mark.full
    def test_caseid_1988611(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_singal("bodyexposedcanfd","BgmBodyExposedCANFr10", "SetOfPosnLampScopeReq",3)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_singal("bodyexposedcanfd","BgmBodyExposedCANFr10", "SetOfPosnLampScopeReq",2)

    @allure.title("位置灯_位置灯开启需要UB位判别_后位置灯_Left")
    @pytest.mark.full
    def test_caseid_1988727(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedPosnLampLe1",1,ub_flag=True)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedPosnLampLe1",1,ub_flag=False)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set("bodyexposedcanfd","RcmlBodyExpoFr01","StsOfLedPosnLampLe1",1,ub_flag=True)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("位置灯_位置灯开启需要UB位判别_后位置灯_Mid")
    @pytest.mark.full
    def test_caseid_1988728(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set("bodyexposedcanfd","RcmmBodyExpoFr02","StsOfLedPosnLampMid",1,ub_flag=True)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmmBodyExpoFr02","StsOfLedPosnLampMid",1,ub_flag=False)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set("bodyexposedcanfd","RcmmBodyExpoFr02","StsOfLedPosnLampMid",1,ub_flag=True)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("位置灯_位置灯开启需要UB位判别_后位置灯_Right")
    @pytest.mark.full
    def test_caseid_1988729(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedPosnLampRi1",1,ub_flag=True)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedPosnLampRi1",1,ub_flag=False)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set("bodyexposedcanfd","RcmrBodyExpoFr01","StsOfLedPosnLampRi1",1,ub_flag=True)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("在Inactive下无法通过服务开启位置灯")
    @pytest.mark.full
    def test_caseid_1988819(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("在Abandoned下无法通过服务开启位置灯_")
    @pytest.mark.full
    def test_caseid_1988820(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.LowHeam)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("左侧位置灯故障，右侧位置灯不受影响")
    @pytest.mark.full
    def test_caseid_1990175(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Left,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Left,sts=PosnLampSts.On)
        
    @allure.title("当StsOfLedReLampLe == 0x02时，所有后部灯应置故障_后位置灯")
    @pytest.mark.full
    def test_caseid_1990194(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe', 2)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.ipdu.set(self.bus_comm.ipdu.bodyexposedcanfd.RcmlBodyExpoFr01, 'StsOfLedReLampLe', 1)

    @allure.title("在dyno下无法通过服务开启位置灯")
    @pytest.mark.full
    def test_caseid_1990215(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.DYNO,ccp={274:0x80})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("在transport下无法通过服务开启位置灯")
    @pytest.mark.full
    def test_caseid_1990216(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.TRANSPORT)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("在Abandoned下无法通过服务开启位置灯")
    @pytest.mark.full
    def test_caseid_1990217(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("NFC闭锁关闭前位置灯")
    @pytest.mark.full
    def test_caseid_1994364(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("OUTSIDE_OTHERS闭锁关闭前位置灯")
    @pytest.mark.full
    def test_caseid_1994365(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.OutsOth)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("APPROACH闭锁关闭前位置灯")
    @pytest.mark.full
    def test_caseid_1994366(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Apprch)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("TELEMATICS闭锁关闭前位置灯")
    @pytest.mark.full
    def test_caseid_1994367(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("KEYLESS_PASSIVE闭锁关闭前位置灯")
    @pytest.mark.full
    def test_caseid_1994369(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.KV_PEPS)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("Normal Driving mode下CCP 274！=80 or 81通过软开关无法开启位置灯")
    @pytest.mark.full
    def test_caseid_1990214(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.sd_tester.set_ccp(ccp_vlaue={274:0x82})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)
        self.sd_tester.set_ccp(ccp_vlaue={274:0x80})

    @allure.title("Normal Driving mode下CCP 508！=03  or 259！=04 or 02通过软开关无法开启倒车灯")
    @pytest.mark.full
    def test_caseid_1990201(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.sd_tester.set_ccp(ccp_vlaue={259:0x03})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_reverse_lamp_act_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.sd_tester.set_ccp(ccp_vlaue={259:0x02})

    @allure.title("Normal Driving mode下CCP 508！=03 or 255！=02通过软开关无法开启后雾灯")
    @pytest.mark.full
    def test_caseid_1990208(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.sd_tester.set_ccp(ccp_vlaue={508:0x02})
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_rear_fog_sts(actn_sts=isOn.Off,extr_light_sts=ExtrLtgSts.Off)
        self.sd_tester.set_ccp(ccp_vlaue={508:0x03})

    @allure.title("位置灯开启_左1右1mid故障")
    @pytest.mark.full
    def test_caseid_1994379(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.All,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.All,sts=PosnLampSts.On)

    @allure.title("位置灯开启_右1mid故障")
    @pytest.mark.full
    def test_caseid_1994380(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Right,sts=PosnLampSts.Error)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Mid,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.All,sts=PosnLampSts.On)

    @allure.title("位置灯开启_左1mid故障")
    @pytest.mark.full
    def test_caseid_1994381(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Left,sts=PosnLampSts.Error)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Mid,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.All,sts=PosnLampSts.On)

    @allure.title("位置灯开启_左1右1故障")
    @pytest.mark.full
    def test_caseid_1994382(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Left,sts=PosnLampSts.Error)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Right,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.All,sts=PosnLampSts.On)

    @allure.title("位置灯开启_右1故障")
    @pytest.mark.full
    def test_caseid_1994383(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Right,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Right,sts=PosnLampSts.On)

    @allure.title("位置灯开启_左1故障")
    @pytest.mark.full
    def test_caseid_1994384(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Left,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Err)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Rear,pos=GeneralPos.Left,sts=PosnLampSts.On)

    @allure.title("车速等于3km/h时，模式下切Inactive关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994385(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=3)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)

    @allure.title("车速大于3km/h时，不能使用模式下切Inactive关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994386(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_and_qf(vehspd=3.1)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_vehspd_and_qf(vehspd=0)

    @allure.title("灯ECU收到关闭请求信号_位置灯范围由AVP切为Normal模式")
    @pytest.mark.full
    def test_caseid_1994387(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.send_method_request("LightService_client", "LightControl", {"lights": [
            {"light": {"type": 38, "zoneId": 0}, "mode": 0, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.bus_comm.check_singal("bodyexposedcanfd","BgmBodyExposedCANFr10", 'SetOfPosnLampScopeReq',2)

    @allure.title("灯ECU收到开启请求信号_位置灯范围由Normal切为AVP模式")
    @pytest.mark.full
    def test_caseid_1994388(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.send_method_request("LightService_client", "LightControl", {"lights": [
            {"light": {"type": 38, "zoneId": 0}, "mode": 1, "brightness": 0,
             "color": {"cRed": 0, "cGreen": 0, "cBlue": 0}}]})
        self.bus_comm.check_singal("bodyexposedcanfd","BgmBodyExposedCANFr10", 'SetOfPosnLampScopeReq',1)
        
    @allure.title("开关处于Auto位开启位置灯_昼夜切换不影响前后位置灯状态")
    @pytest.mark.full
    def test_caseid_1994389(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Auto)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_day_mode(wait_time=2)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.bus_comm.set_night_mode(wait_time=2)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)

    @allure.title("NFC闭锁关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994390(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("OUTSIDE_OTHERS闭锁关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994391(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.OutsOth)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("APPROACH闭锁关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994392(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Apprch)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("TELEMATICS闭锁关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994393(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.Telm)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("KEYLESS_PASSIVE闭锁关闭后位置灯")
    @pytest.mark.full
    def test_caseid_1994394(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.mix.set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.On)
        self.mix.set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.KV_PEPS)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.Off,pos=GeneralPos.Rear,extr_light_sts=ExtrLtgSts.Off)

    @allure.title("前位置灯激活过程_开关POS位置前位置灯右故障_默认前位置灯满足激活条件")
    @pytest.mark.full
    def test_caseid_1994405(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,car_mode=CarMode.NORMAL)
        self.soa.get_and_set_extilight_mode(target_mode=ExteriorLightMode.Position)
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Right,sts=PosnLampSts.Error)
        self.bus_comm.check_pos_laom_act_sts(actn_sts=isOn.On,pos=GeneralPos.Front,extr_light_sts=ExtrLtgSts.Err)
        # 恢复
        self.bus_comm.set_pos_lamp_sts(front_rear=GeneralPos.Front,pos=GeneralPos.Right,sts=PosnLampSts.On)