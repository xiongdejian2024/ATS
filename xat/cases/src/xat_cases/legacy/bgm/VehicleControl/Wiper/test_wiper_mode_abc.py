#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wiper_mode_abc.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设外后视镜功能
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
from xat_ecu.api.constants.common import *


@allure.feature("BGM车控车设/雨刮功能")
@allure.story("雨刮模式")
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WiperService_client"])
        sleep(2)
        self.soa.start_get_wiper_switch_sts()
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.bus_comm.set_vehspd_gear(vehspd=0.0) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, isOn.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, WiperMode.Off)
        sleep(1)

    def after_each_func(self, ecu):
        sleep(1)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprActvFromWMM",0)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WshngCycActvFromWMM",0)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def set_pre_condition_for_maintain_service(self, wash_func_sts: isOn, maintain_pos: isOn, wiper_mode: WiperMode,
                                               usage_mode: Union[UsageMode, None] = None,
                                               car_mode: Union[CarMode, None] = None, ccp: dict = {},time_wait = 1):
        self.mix.set_common_precontion(usage_mode=usage_mode, car_mode=car_mode, ccp=ccp)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, wash_func_sts)
        self.soa.hmi_set_wiper_maintaince_pos(maintain_pos)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, wiper_mode)
        sleep(time_wait)

        
  
    @allure.title("设置雨刮模式_Crash&&Convenience&&车速低于7km/h_设置前雨刮间歇性快刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985870(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check_wiper_mode_req(WiperMode.IntHigh)
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off)  

    @allure.title("设置雨刮模式_Inactive&&Normal &&车速低于7km/h_设置前雨刮单刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985877(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 


    @allure.title("设置雨刮模式_Inactive&&Normal &&车速低于7km/h_前雨刮模式为间歇性慢刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985878(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_wiper_mode_req(WiperMode.IntLow)
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 

    @allure.title("设置雨刮模式_Normal&&Abandoned&&车速低于7km/h_设置前雨刮间歇性快刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985879(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check_wiper_mode_req(WiperMode.IntHigh)
        sleep(1) 
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 


    @allure.title("设置雨刮模式_Normal && Inactive &&车速低于7km/h_设置前雨刮为慢刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985880(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check_wiper_mode_req(WiperMode.Low)
        sleep(1) 
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off)  

    @allure.title("设置雨刮模式_间歇性慢刮到OFF_触发雨传感器灵敏度信号值变化")
    @pytest.mark.smoke
    def test_wiper_ctrl_caseid_1987075(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6) 

    @allure.title("设置雨刮模式_OFF到间歇性慢刮_触发雨传感器灵敏度信号值变化")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987073(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3) 

    @allure.title("设置雨刮模式_间歇性慢刮到慢刮_触发雨传感器灵敏度信号值变化")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987071(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6) 

    @allure.title("设置雨刮模式_间歇性慢刮到单刮_触发雨传感器灵敏度信号值变化")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987074(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6) 

    @allure.title("设置雨刮模式_间歇性慢刮到快刮_触发雨传感器灵敏度信号值变化")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987070(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6) 

    @allure.title("设置雨刮模式_OFF到自动模式_触发雨传感器灵敏度信号值变化")
    @pytest.mark.sanity
    def test_wiper_ctrl_caseid_1987069(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 5) 

    @allure.title("设置雨刮模式_间歇性慢刮到间歇性快刮_触发雨传感器灵敏度信号值变化")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987072(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 3)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.bus_comm.check_singal("cem_lin1", "CemCem_Lin1Fr01", "WiprMotIntlCmd", 6)  
        
 
       
    @allure.title("服务单刮_设置雨刮模式_Normal&&Drving_设置前雨刮单刮_开启") 
    @pytest.mark.smoke
    def test_wiper_ctrl_caseid_1987244(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe) 
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
    
    @allure.title("服务单刮_设置雨刮模式_Dynamometer&&Drving_设置前雨刮单刮_开启") 
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987243(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe) 
        
    @allure.title("服务单刮_设置雨刮模式_Active&&Normal设置前雨刮单刮_开启") 
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987242(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe) 
    
    @allure.title("服务单刮_设置雨刮模式_Convenience&&Normal设置前雨刮单刮_开启") 
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987241(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)    
    
    @pytest.mark.sanity
    def test_caseid_1991455(self):
        """
        Abandoned&normal，车速大于7km/h,检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0) 
        sleep(3)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991456(self):
        """
        Convience&normal，雨刮模式为1档，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991457(self):
        """
        Convience&normal，雨刮模式为2档，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991458(self):
        """
        Convience&normal，雨刮模式为3档，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991459(self):
        """
        Convience&normal，雨刮模式为4档，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991460(self):
        """
        Convience&normal，雨刮模式为自动档，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","RainSensActvn",1)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991461(self):
        """
        Convience&normal，雨刮洗涤周期信号激活，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WshngCycActvFromWMM",1)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WshngCycActvFromWMM",1)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991462(self):
        """
        Convience&normal，WiprActvFromWMM=on，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprActvFromWMM",1)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("cem_lin1","WmmCem_Lin1Fr01","WiprActvFromWMM",1)
        sleep(10)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)

    @pytest.mark.sanity
    def test_caseid_1991463(self):
        """
        Convience&normal，雨刮维修激活，检查WipgPwrActvnSafeWipgPwrAcsyModSafe
        """
        for i in [isOn.On,isOn.Off]:
            self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
            self.soa.hmi_set_wiper_maintaince_pos(i)
            sleep(10)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)
            self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
            self.soa.hmi_set_wiper_maintaince_pos(i)
            sleep(10)
            self.bus_comm.check("cem_lin1","CemCem_Lin1Fr01","WipgPwrActvnSafeWipgPwrAcsyModSafe",2)



    




   