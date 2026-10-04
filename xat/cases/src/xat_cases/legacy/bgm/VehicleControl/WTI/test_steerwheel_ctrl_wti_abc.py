#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_seat_ctrl_abc.py
@Author      : liqi.yin_ext@jiduauto.com
@Time        : 2024/1/24 11:30
@Description: BGM车控车设空调
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
from xat_ecu.legacy.soa_partner.src.partner_const import *


# @allure.feature("SOA服务接口")
# @allure.story("WTI通知")
# class TestWTIServiceChargeLid(TestABCBase):
#     def before_class(self, ecu):
#         """测试用例的前处理"""
#         self.soa.update(["SteerWheelService_client", "WTIService_client"])
#         sleep(2)
#         self.sd_tester.write_ccp(ccp={186: 0x02, 13: 0x4})
#         self.bus_comm.set_Hv_sys_relay_sts(HvSysRelaySts.Close)
#     def before_each_func(self, ecu):
#             pass

#     def after_each_func(self, ecu):
#         self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)

#     def after_class(self, ecu):
#         pass


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:0")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/2519141?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1985008(self):
#         self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
#         self.soa.hmi_set_steer_wheel_heat_level(HeatLevel.High)
#         self.bus_comm.set
#         self.bus_comm.check_steerwheel_heat_req(lev_sts=HeatLevel.High, avl_sts=AvlSts.Energylimit)
#         sleep(1)
#         self.soa.get_and_event_check_warning_info_list(name="Steer Wheel Heat Warning", info='5')


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:1")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/2339557?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1981264(self):
#         self.bus_comm.set_wti_signal(func=WTI_Func.SteerWheelHeatWarning,value=5)
#         sleep(1)
#         self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteerWheelHeatWarning,sig_value=1,prom_name="Steer Wheel Heat Warning",prom_state="0")


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:2")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/2519209?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1985009(self):
#         self.bus_comm.set_wti_signal(func=WTI_Func.SteerWheelHeatWarning,value=5)
#         sleep(1)
#         self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteerWheelHeatWarning,sig_value=2,prom_name="Steer Wheel Heat Warning",prom_state="0")


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:3")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/2519211?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1985010(self):
#         self.bus_comm.set_wti_signal(func=WTI_Func.SteerWheelHeatWarning,value=5)
#         sleep(1)
#         self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteerWheelHeatWarning,sig_value=3,prom_name="Steer Wheel Heat Warning",prom_state="0")


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:4")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/2519211?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1985010(self):
#         self.bus_comm.set_wti_signal(func=WTI_Func.SteerWheelHeatWarning,value=5)
#         sleep(1)
#         self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteerWheelHeatWarning,sig_value=4,prom_name="Steer Wheel Heat Warning",prom_state="0")


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:5")
#     @allure.testcase(
#         "https://jama.jiduauto.com/perspective.req#/testCases/2339558?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1981471(self):
#         self.bus_comm.set_wti_signal(func=WTI_Func.SteerWheelHeatWarning,value=1)
#         sleep(1)
#         self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteerWheelHeatWarning,sig_value=5,prom_name="Steer Wheel Heat Warning",prom_state="5")


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:6")
#     @allure.testcase(
#         "hhttps://jama.jiduauto.com/perspective.req#/testCases/2519213?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1985012(self):
#         self.bus_comm.set_wti_signal(func=WTI_Func.SteerWheelHeatWarning,value=5)
#         sleep(1)
#         self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteerWheelHeatWarning,sig_value=6,prom_name="Steer Wheel Heat Warning",prom_state="0")


#     @allure.title("方向盘加热无故障报警SteerWhlHeatgAvlSts:7")
#     @allure.testcase(
#         "hhttps://jama.jiduauto.com/perspective.req#/testCases/2519214?projectId=46"
#     )
#     @pytest.mark.sanity
#     def test_caseid_1985013(self):
#         self.bus_comm.set_wti_signal(func=WTI_Func.SteerWheelHeatWarning,value=5)
#         sleep(1)
#         self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.SteerWheelHeatWarning,sig_value=7,prom_name="Steer Wheel Heat Warning",prom_state="0")
