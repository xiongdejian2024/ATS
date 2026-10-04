#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wiper_mode_fail_case.py
@Author      : daidi.liang@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设雨刮功能
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
        try:
            self.bus_comm.set_wiper_lever_status(value=0)
        except Exception as e:
            logger.info(f"----------> after_each_func Error{str(e)}")
            pass
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 

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
    
    def set_nopresent_and_drvr_close(self,car_motion_status:int):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",car_motion_status)

    def set_present_and_drvr_close(self,car_motion_status:int):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",car_motion_status)

    def set_and_get_wiper_mode(self,mode):
        sleep(1)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,mode)
        sleep(0.7)
        self.soa.get_wiper_mode(WiperPos.Front,mode)

    def car_Vehicle_stationary_open_close_door(self,close_door_wiper_mode=None):
        #车辆静止开门关门
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        sleep(0.5)
        self.io.set_door(Drvr=Door.close)
        if close_door_wiper_mode == None:
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        else:
            self.soa.get_wiper_mode(WiperPos.Front,close_door_wiper_mode)

    def car_not_Vehicle_stationary_open_close_door(self,wiper_mode):
        #车辆静止开门关门
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,wiper_mode)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,wiper_mode)
                
    @allure.title("按键设置雨刮模式_Crash&&Drving&&车速低于7km/h_设置前雨刮单刮_禁用")
    @pytest.mark.smoke
    def test_wiper_ctrl_caseid_1985871(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.SingleWipe)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off)
        
    @allure.title("按键单刮_设置雨刮模式_Factory&&Drving&&车速高于_低于7km/h_设置前雨刮单刮_禁用") 
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987247(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)  
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off)
        
    @allure.title("按键单刮_设置雨刮模式_Normal&&Inactive &&车速高于_低于7km/h_设置前雨刮单刮_开启和禁用验证") 
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987245(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)  
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 
        
    @allure.title("按键单刮_设置雨刮模式_Transport&&Convenience&&车速高于_低于7km/h_设置前雨刮单刮_开启和禁用验证") 
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987248(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(1) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)  
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 
        
    @allure.title("按键单刮_设置雨刮模式_Transport&&Convenience&&车速高于_低于7km/h_设置前雨刮单刮_开启和禁用验证") 
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1987246(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(1) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)  
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 
        
    @allure.title("按键单刮_设置雨刮模式_Crash&&Drving&&车速高于_低于7km/h_设置前雨刮单刮_开启和禁用验证") 
    @pytest.mark.smoke
    def test_wiper_ctrl_caseid_1987249(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(1) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.SingleWipe)  
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 
        
    @allure.title("设置雨刮模式_Transport&&Driving&&车速低于7km/h_设置前雨刮为慢刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985875(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(2.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check_wiper_mode_req(WiperMode.Low)
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 
        
        
    @allure.title("设置雨刮模式_Abandoned&&Normal&&车速低于7km/h_设置前雨刮为快刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985881(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check_wiper_mode_req(WiperMode.High)
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.High)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 

    @allure.title(" 设置雨刮模式_Transport&&Convenience &&车速低于7km/h_前雨刮模式为间歇性慢刮_禁用")
    @pytest.mark.full
    def test_wiper_ctrl_caseid_1985874(self):
        self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT,
                                                    ccp={503: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.Off,
                                                    wiper_mode=WiperMode.Off)
        self.bus_comm.set_vehspd(3.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_wiper_mode_req(WiperMode.IntLow)
        sleep(1)
        self.bus_comm.set_vehspd(1.0)
        self.soa.hmi_set_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.bus_comm.check_wiper_mode_req(WiperMode.Off) 

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988759(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为1档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988758(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为2档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988757(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为3档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988756(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为4档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988755(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为自动档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988754(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为关闭档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Off)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988785(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为1档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988784(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为2档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988783(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为3档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988782(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为4档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988781(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为自动档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988780(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为关闭档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.Off)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988753(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为1档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=2)
            else:
                self.set_present_and_drvr_close(car_motion_status=2)
            self.set_nopresent_and_drvr_close(car_motion_status=2)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988752(self):
        """
       车辆静止，主驾无人，设置雨刮挡位为2档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=2)
            else:
                self.set_present_and_drvr_close(car_motion_status=2)
            self.set_nopresent_and_drvr_close(car_motion_status=2)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988751(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为3档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=2)
            else:
                self.set_present_and_drvr_close(car_motion_status=2)
            self.set_nopresent_and_drvr_close(car_motion_status=2)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988750(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为4档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=2)
            else:
                self.set_present_and_drvr_close(car_motion_status=2)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988749(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为自动档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=2)
            else:
                self.set_present_and_drvr_close(car_motion_status=2)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988748(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为关闭档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=2)
            else:
                self.set_present_and_drvr_close(car_motion_status=2)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988690(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为1档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988689(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为2档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988688(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为3档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988687(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为4档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988686(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为自动档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988685(self):
        """
        车辆静止，主驾无人，设置雨刮挡位为关闭档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=None)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988791(self):
        """
        车辆非静止，主驾占位，设置雨刮挡位为3档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=7)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.car_not_Vehicle_stationary_open_close_door(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988790(self):
        """
        车辆非静止，主驾占位，设置雨刮挡位为4档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=7)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.car_not_Vehicle_stationary_open_close_door(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988789(self):
        """
        车辆非静止，主驾占位，设置雨刮挡位为关闭档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=7)
        self.set_and_get_wiper_mode(WiperMode.Off)
        self.car_not_Vehicle_stationary_open_close_door(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988788(self):
        """
        车辆非静止，主驾占位，设置雨刮挡位为1档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=7)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.car_not_Vehicle_stationary_open_close_door(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988787(self):
        """
        车辆非静止，主驾占位，设置雨刮挡位为自动档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=7)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.car_not_Vehicle_stationary_open_close_door(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988786(self):
        """
        车辆非静止，主驾占位，设置雨刮挡位为2档，打开主驾车门，检查雨刮挡位状态
        """
        self.set_nopresent_and_drvr_close(car_motion_status=7)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.car_not_Vehicle_stationary_open_close_door(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.driver_seat_present()
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988779(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为1档，切换车辆状态为静止，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=5)
            else:
                self.set_present_and_drvr_close(car_motion_status=5)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.IntLow)
            self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",1)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988778(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为自动档，切换车辆状态为静止，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=5)
            else:
                self.set_present_and_drvr_close(car_motion_status=5)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.Auto)
            self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",1)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988777(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为3档，切换车辆状态为静止，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=5)
            else:
                self.set_present_and_drvr_close(car_motion_status=5)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.Low)
            self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",1)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988776(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为2档，切换车辆状态为静止，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=5)
            else:
                self.set_present_and_drvr_close(car_motion_status=5)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.IntHigh)
            self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",1)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988775(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为关闭档，切换车辆状态为静止，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=5)
            else:
                self.set_present_and_drvr_close(car_motion_status=5)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.Off)
            self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",1)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1988774(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为4档，切换车辆状态为静止，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=5)
            else:
                self.set_present_and_drvr_close(car_motion_status=5)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.High)
            self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",1)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988773(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为3档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=6)
            else:
                self.set_present_and_drvr_close(car_motion_status=6)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988772(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为自动档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=6)
            else:
                self.set_present_and_drvr_close(car_motion_status=6)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988771(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为4档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=6)
            else:
                self.set_present_and_drvr_close(car_motion_status=6)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988770(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为2档，开门后多次切换雨刮挡位，检查雨刮挡位状态_
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=6)
            else:
                self.set_present_and_drvr_close(car_motion_status=6)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988769(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为1档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=6)
            else:
                self.set_present_and_drvr_close(car_motion_status=6)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988768(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为关闭档，开门后多次切换雨刮挡位，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=6)
            else:
                self.set_present_and_drvr_close(car_motion_status=6)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988767(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为1档，打开主驾车门，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=4)
            else:
                self.set_present_and_drvr_close(car_motion_status=4)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988766(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为2档，打开主驾车门，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=4)
            else:
                self.set_present_and_drvr_close(car_motion_status=4)
            self.set_and_get_wiper_mode(WiperMode.IntHigh)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.IntHigh)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988765(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为3档，打开主驾车门，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=4)
            else:
                self.set_present_and_drvr_close(car_motion_status=4)
            self.set_and_get_wiper_mode(WiperMode.Low)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.Low)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988764(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为4档，打开主驾车门，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=4)
            else:
                self.set_present_and_drvr_close(car_motion_status=4)
            self.set_and_get_wiper_mode(WiperMode.High)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.High)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988763(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为自动档，打开主驾车门，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=4)
            else:
                self.set_present_and_drvr_close(car_motion_status=4)
            self.set_and_get_wiper_mode(WiperMode.Auto)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.Auto)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.full
    def test_caseid_1988762(self):
        """
        车辆非静止，主驾无人，设置雨刮挡位为关闭档，打开主驾车门，检查雨刮挡位状态
        """
        for i in ["nopresent","present"]:
            if i == "nopresent":
                self.set_nopresent_and_drvr_close(car_motion_status=4)
            else:
                self.set_present_and_drvr_close(car_motion_status=4)
            self.set_and_get_wiper_mode(WiperMode.Off)
            self.car_not_Vehicle_stationary_open_close_door(WiperMode.Off)
            self.io.set_door(Drvr=Door.open)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
            self.set_and_get_wiper_mode(WiperMode.IntLow)
            self.io.set_door(Drvr=Door.close)
            self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)


    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1991465(self):
        """
        车辆静止，主驾占位，设置雨刮挡位从1档设置为2档，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1991466(self):
        """
        车辆静止，主驾占位，设置雨刮挡位从2档设置为3档，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1991467(self):
        """
        车辆静止，主驾占位，设置雨刮挡位从3档设置为4档，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1991468(self):
        """
        车辆静止，主驾占位，设置雨刮挡位从4档设置为自动档，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1991469(self):
        """
        车辆静止，主驾占位，设置雨刮挡位从自动档设置为off档，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v210
    @pytest.mark.smoke
    def test_caseid_1991470(self):
        """
        车辆静止，主驾占位，设置雨刮挡位从off档设置为1档，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=1)
        self.set_and_get_wiper_mode(WiperMode.Off)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1991471(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为1档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.IntLow)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1991472(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为2档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.IntHigh)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.IntHigh)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1991473(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为3档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.Low)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.Low)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1991474(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为4档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.High)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.High)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1991475(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为自动档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.Auto)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.Auto)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.set_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v210
    @pytest.mark.sanity
    def test_caseid_1991476(self):
        """
        车辆静止，主驾占位，设置雨刮挡位为Off档，切换车辆状态为非静止，检查雨刮挡位状态
        """
        self.set_present_and_drvr_close(car_motion_status=2)
        self.set_and_get_wiper_mode(WiperMode.Off)
        self.car_Vehicle_stationary_open_close_door(close_door_wiper_mode=WiperMode.Off)
        self.bus_comm.set("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt",7)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.set_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v220
    @pytest.mark.smoke
    def test_caseid_1995603(self):
        """
        convience&normal 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995602(self):
        """
        convience&dyno 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.smoke
    def test_caseid_1995601(self):
        """
        Active&normal 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995600(self):
        """
        Active&dyno 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.smoke
    def test_caseid_1995599(self):
        """
        driving&normal 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995598(self):
        """
        driving&dyno 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=3)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995597(self):
        """
        convience&Transport 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995596(self):
        """
        convience&Crash 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995595(self):
        """
        convience&Factory 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995594(self):
        """
        active&Transport 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995593(self):
        """
        active&Crash 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995592(self):
        """
        active&Factory 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995591(self):
        """
        driving&Transport 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995590(self):
        """
        driving&Crash 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995589(self):
        """
        driving&Factory 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995588(self):
        """
        Inactive&Transport 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995587(self):
        """
        Inactive&Crash 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995586(self):
        """
        Inactive&Factory 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995585(self):
        """
        Inactive&normal 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995584(self):
        """
        Inactive&dyno 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995583(self):
        """
        Abandoned&Transport 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.TRANSPORT)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995582(self):
        """
        Abandoned&Crash 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.CRASH)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995581(self):
        """
        Abandoned&Factory 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.FACTORY)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995580(self):
        """
        Abandoned&normal 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995579(self):
        """
        Abandoned&dyno 雨刮拨杆短按单刮
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, car_mode=CarMode.DYNO)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)        
        self.bus_comm.set_vehspd_gear(vehspd=1.0)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=0)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995663(self):
        """
        convience&normal 拨杆短按，按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995661(self):
        """
        Active&normal 拨杆短按，按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995659(self):
        """
        driving&normal 拨杆短按，按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995662(self):
        """
        convience&dyno 拨杆短按，按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995660(self):
        """
        Active&dyno 拨杆短按，按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995658(self):
        """
        driving&dyno 拨杆短按，按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995657(self):
        """
        covience&normal 按键短按，拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995656(self):
        """
        covience&dyno 按键短按，拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995655(self):
        """
        Active&normal 按键短按，拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995654(self):
        """
        Active&dyno 按键短按，拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995653(self):
        """
        driving&normal 按键短按，拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995652(self):
        """
        driving&dyno 按键短按，拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)   
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995651(self):
        """
        convience&normal 按键长按，拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995650(self):
        """
        convience&dyno 按键长按，拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995649(self):
        """
        active&normal 按键长按，拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995648(self):
        """
        active&dyno 按键长按，拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995647(self):
        """
        driving&normal 按键长按，拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995646(self):
        """
        driving&dyno 按键长按，拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995645(self):
        """
        convience&normal 拨杆长按，按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995644(self):
        """
        convience&dyno 拨杆长按，按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995643(self):
        """
        active&normal 拨杆长按，按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995642(self):
        """
        active&dyno 拨杆长按，按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995641(self):
        """
        driving&normal 拨杆长按，按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995640(self):
        """
        driving&dyno 拨杆长按，按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995639(self):
        """
        convience&normal 拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995638(self):
        """
        convience&dyno 拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995637(self):
        """
        active&normal 拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995636(self):
        """
        active&dyno 拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995635(self):
        """
        driving&normal 拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995634(self):
        """
        driving&dyno 拨杆长按，按键短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995633(self):
        """
        convience&normal 拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995632(self):
        """
        convience&dyno 拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995631(self):
        """
        active&normal 拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995630(self):
        """
        active&dyno 拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)


    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995629(self):
        """
        driving&normal 拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        

    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995628(self):
        """
        driving&dyno 拨杆短按，按键长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995627(self):
        """
        convience&normal 按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995626(self):
        """
        convience&dyno 按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995625(self):
        """
        active&normal 按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995624(self):
        """
        active&dyno 按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        
    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995623(self):
        """
        driving&normal 按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995622(self):
        """
        driving&dyno 按键长按，拨杆短按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.LongPress) 
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=1)
        sleep(0.5)
        self.bus_comm.set_wiper_lever_status(value=0)
        self.bus_comm.check_single_wiper_status(value=1)

    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995621(self):
        """
        convience&normal 按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
       
        
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995620(self):
        """
        convience&dyno 按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)


    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995619(self):
        """
        active&normal 按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
       
        
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995618(self):
        """
        active&dyno 按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)


    @pytest.mark.v220
    @pytest.mark.sanity
    def test_caseid_1995617(self):
        """
        driving&normal 按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)
       
        
        
    @pytest.mark.v220
    @pytest.mark.full
    def test_caseid_1995616(self):
        """
        driving&dyno 按键短按，拨杆长按
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.DYNO)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.ShortPress) 
        sleep(0.5)
        self.bus_comm.set_steer_wheel_touch_switch_sts(pos=SteerWhlTouchSwtPos.Right3,sts=SteerWhlTouchSwtSts.NotAvailble) 
        self.bus_comm.check_single_wiper_status(value=1)
        self.bus_comm.set_wiper_lever_status(value=2)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(9)
        self.bus_comm.check_wiper_wash_active_status(value=2)
        sleep(3)
        self.bus_comm.check_wiper_wash_active_status(value=1)

    
    @pytest.mark.v300
    def test_caseid_1996183(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v300
    def test_caseid_1996182(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v300
    def test_caseid_1996181(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)


    @pytest.mark.v300
    def test_caseid_1996180(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v300
    def test_caseid_1996179(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v300
    def test_caseid_1996178(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.fail_001
    def test_caseid_1996177(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,最后关车门时主驾无人,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.fail_001
    def test_caseid_1996176(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,最后关车门时主驾无人,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.fail_001
    def test_caseid_1996175(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,最后关车门时主驾无人,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.fail_001
    def test_caseid_1996174(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,最后关车门时主驾无人,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.fail_001
    def test_caseid_1996173(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,最后关车门时主驾无人,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.fail_001
    def test_caseid_1996172(self):
        """
        车辆静止,车门关闭,关门前设置雨刮维修退出,主驾一直占位,最后关车门时主驾无人,雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    def test_caseid_1996171(self):
        """
        主驾占位，车门关闭，关门前未设置雨刮维修退出，关闭车门,主驾一直占位，雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
  
    @pytest.mark.v300
    def test_caseid_1996170(self):
        """
        主驾占位，车门关闭，关门前未设置雨刮维修退出，关闭车门,主驾一直占位，雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v300
    def test_caseid_1996169(self):
        """
        主驾占位，车门关闭，关门前未设置雨刮维修退出，关闭车门,主驾一直占位，雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v300
    def test_caseid_1996168(self):
        """
        主驾占位，车门关闭，关门前未设置雨刮维修退出，关闭车门,主驾一直占位，雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
  
    @pytest.mark.v300
    def test_caseid_1996167(self):
        """
        主驾占位，车门关闭，关门前未设置雨刮维修退出，关闭车门,主驾一直占位，雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v300
    def test_caseid_1996166(self):
        """
        主驾占位，车门关闭，关门前未设置雨刮维修退出，关闭车门,主驾一直占位，雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996165(self):
        """
        主驾一直占位，车门关闭，打开雨刮维修后，再次关门开门,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v300
    def test_caseid_1996164(self):
        """
        主驾一直占位，车门关闭，打开雨刮维修后，再次关门开门,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v300
    def test_caseid_1996163(self):
        """
        主驾一直占位，车门关闭，打开雨刮维修后，再次关门开门,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v300
    def test_caseid_1996162(self):
        """
        主驾一直占位，车门关闭，打开雨刮维修后，再次关门开门,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)


    @pytest.mark.v300
    def test_caseid_1996161(self):
        """
        主驾一直占位，车门关闭，打开雨刮维修后，再次关门开门,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)


    @pytest.mark.v300
    def test_caseid_1996160(self):
        """
        主驾一直占位，车门关闭，打开雨刮维修后，再次关门开门,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996160(self):
        """
        主驾一直占位，车门关闭，打开雨刮维修后，再次关门开门,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996159(self):
        """
        主驾占位，车门关闭，雨刮维修开启后主驾无人,关门前未设置雨刮维修退出,雨刮为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996158(self):
        """
        主驾占位，车门关闭，雨刮维修开启后主驾无人,关门前未设置雨刮维修退出,雨刮为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996157(self):
        """
        主驾占位，车门关闭，雨刮维修开启后主驾无人,关门前未设置雨刮维修退出,雨刮为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996156(self):
        """
        主驾占位，车门关闭，雨刮维修开启后主驾无人,关门前未设置雨刮维修退出,雨刮为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996155(self):
        """
        主驾占位，车门关闭，雨刮维修开启后主驾无人,关门前未设置雨刮维修退出,雨刮为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996154(self):
        """
        主驾占位，车门关闭，雨刮维修开启后主驾无人,关门前未设置雨刮维修退出,雨刮为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    def test_caseid_1996153(self):
        """
        主驾占位，车门打开，开门前设置雨刮维修退出，主驾一直占位，雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)   
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)   

    @pytest.mark.v300
    def test_caseid_1996152(self):
        """
        主驾占位，车门打开，开门前设置雨刮维修退出，主驾一直占位，雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)   
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh) 

    @pytest.mark.v300
    def test_caseid_1996151(self):
        """
        主驾占位，车门打开，开门前设置雨刮维修退出，主驾一直占位，雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)   
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)   

    @pytest.mark.v300
    def test_caseid_1996150(self):
        """
        主驾占位，车门打开，开门前设置雨刮维修退出，主驾一直占位，雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)   
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)   

    @pytest.mark.v300
    def test_caseid_1996149(self):
        """
        主驾占位，车门打开，开门前设置雨刮维修退出，主驾一直占位，雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)   
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)     

    @pytest.mark.v300
    def test_caseid_1996148(self):
        """
        主驾占位，车门打开，开门前设置雨刮维修退出，主驾一直占位，雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)   
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)     

    @pytest.mark.v300
    def test_caseid_1996147(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾一直占位，雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)   

    @pytest.mark.v300
    def test_caseid_1996146(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾一直占位，雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)   

    @pytest.mark.v300
    def test_caseid_1996145(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾一直占位，雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)   
         

    @pytest.mark.v300
    def test_caseid_1996144(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾一直占位，雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)  

    @pytest.mark.v300
    def test_caseid_1996143(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾一直占位，雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v300
    def test_caseid_1996142(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾一直占位，雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996141(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾无人，雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996140(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾无人，雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996139(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾无人，雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996138(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾无人，雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996137(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾无人，雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996136(self):
        """
        主驾占位，车门打开，开门前未设置雨刮维修退出,主驾无人，雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=2,seat_status="yes",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_notpresent()
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off) 
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996135(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,主驾一直无人，雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996134(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,主驾一直无人，雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996133(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,主驾一直无人，雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996132(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,主驾一直无人，雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996131(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,主驾一直无人，雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996130(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,主驾一直无人，雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996129(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,无人到最后关门时有人,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996128(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,无人到最后关门时有人,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996127(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,无人到最后关门时有人,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996126(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,无人到最后关门时有人,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996125(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,无人到最后关门时有人,雨刮挡位为auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996124(self):
        """
        主驾无人，车门关闭，关门前设置雨刮维修退出,无人到最后关门时有人,雨刮挡位为off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996123(self):
        """
        主驾无人，车门关闭，关门前未设置雨刮维修退出，主驾一直无人,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996122(self):
        """
        主驾无人，车门关闭，关门前未设置雨刮维修退出，主驾一直无人,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996121(self):
        """
        主驾无人，车门关闭，关门前未设置雨刮维修退出，主驾一直无人,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996120(self):
        """
        主驾无人，车门关闭，关门前未设置雨刮维修退出，主驾一直无人,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996119(self):
        """
        主驾无人，车门关闭，关门前未设置雨刮维修退出，主驾一直无人,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        sleep(0.5)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996118(self):
        """
        主驾无人，车门关闭，关门前未设置雨刮维修退出，主驾一直无人,雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996117(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,关闭主驾车门后,再次打开主驾车门雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996116(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,关闭主驾车门后,再次打开主驾车门雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996115(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,关闭主驾车门后,再次打开主驾车门雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996114(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,关闭主驾车门后,再次打开主驾车门雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996113(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,关闭主驾车门后,再次打开主驾车门雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996112(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,关闭主驾车门后,再次打开主驾车门雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.close)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996111(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,雨刮维修开启后主驾占位,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996110(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,雨刮维修开启后主驾占位,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996109(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,雨刮维修开启后主驾占位,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996108(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,雨刮维修开启后主驾占位,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996107(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,雨刮维修开启后主驾占位,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996106(self):
        """
        主驾无人,车门关闭,关门前未设置雨刮维修退出,雨刮维修开启后主驾占位,雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="close")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.driver_seat_present()
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.get_wiper_maintaince_pos(isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996105(self):
        """
        主驾无人，车门打开，开门前设置雨刮维修退出,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996104(self):
        """
        主驾无人，车门打开，开门前设置雨刮维修退出,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)


    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996103(self):
        """
        主驾无人，车门打开，开门前设置雨刮维修退出,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996102(self):
        """
        主驾无人，车门打开，开门前设置雨刮维修退出,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996101(self):
        """
        主驾无人，车门打开，开门前设置雨刮维修退出,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996100(self):
        """
        主驾无人，车门打开，开门前设置雨刮维修退出,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996099(self):
        """
        主驾无人，车门打开，关门前未设置雨刮维修退出,雨刮挡位为1档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntLow)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996098(self):
        """
        主驾无人，车门打开，关门前未设置雨刮维修退出,雨刮挡位为2档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.IntHigh)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996097(self):
        """
        主驾无人，车门打开，关门前未设置雨刮维修退出,雨刮挡位为3档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Low)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996096(self):
        """
        主驾无人，车门打开，关门前未设置雨刮维修退出,雨刮挡位为4档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.High)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996095(self):
        """
        主驾无人，车门打开，关门前未设置雨刮维修退出,雨刮挡位为Auto档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Auto)

    @pytest.mark.v300
    @pytest.mark.wiper002
    def test_caseid_1996094(self):
        """
        主驾无人，车门打开，关门前未设置雨刮维修退出,雨刮挡位为Off档
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.mix.set_door_and_seat_status(motion_state=1,seat_status="no",door_status="open")
        self.mix.set_wiper_mode_and_get_wiper_mode(WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_move_inhibit(WiperPos.Front,isOn.On)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
        self.mix.check_wiper_maintanance_signal("active")
        self.io.set_door(Drvr=Door.open)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
        self.mix.check_wiper_maintanance_signal("deactive")
        sleep(2)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)
        self.io.set_door(Drvr=Door.close)
        self.soa.get_wiper_mode(WiperPos.Front,WiperMode.Off)