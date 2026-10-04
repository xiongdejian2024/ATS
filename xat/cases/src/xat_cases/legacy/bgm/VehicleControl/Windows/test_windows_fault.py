#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_windows_fault.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车窗相关异常用例
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


@allure.feature("BGM车控车设/车窗功能")
@allure.story("车窗故障")
@pytest.mark.run(order=1)
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","WindowService_client","KeyService_client","ResetSOAConfigService_client","WindowAppService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        
    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    
    def set_window_error_before_msg(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', 0)
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinFailrStsAtPass', 0)
        self.bus_comm.set("bodycan","RldmBodyFr01", 'WinFailrStsAtReLe', 0)
        self.bus_comm.set("bodycan","RrdmBodyFr01", 'WinFailrStsAtReRi', 0)
        self.bus_comm.set("bodycan","DdmBodyFr03", 'WinThermlStsAtDrvr', 0)
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinThermlStsAtPass', 0)
        self.bus_comm.set("bodycan","RldmBodyFr02", 'WinThermlStsAtReLe', 0)
        self.bus_comm.set("bodycan","RrdmBodyFr02", 'WinThermlStsAtReRi', 0)
        self.io.set_five_door_sts(Door.close)
        
    def single_window_error_before(self,window_postion):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        if window_postion == "right":
            self.bus_comm.set("bodycan","RrdmBodyFr01", 'WinFailrStsAtReRi', 0)
            self.bus_comm.set("bodycan","RrdmBodyFr02", 'WinThermlStsAtReRi', 0)
        elif window_postion == "left":
            self.bus_comm.set("bodycan","RldmBodyFr01", 'WinFailrStsAtReLe', 0)
            self.bus_comm.set("bodycan","RldmBodyFr02", 'WinThermlStsAtReLe', 0)
        elif window_postion == "pass":
            self.bus_comm.set("bodycan","PdmBodyFr03", 'WinFailrStsAtPass', 0)
            self.bus_comm.set("bodycan","PdmBodyFr03", 'WinThermlStsAtPass', 0)
        else:
            self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', 0)
            self.bus_comm.set("bodycan","DdmBodyFr03", 'WinThermlStsAtDrvr', 0)
            
        self.io.set_bgm_hardware_condition_to_default()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)  # 设置bodycan上五个电动门均关闭
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        
    @allure.title("如果主驾车窗位置信号没有更新，检测BGM是否会判断车窗当前位置时采用上一状态")
    @pytest.mark.full
    def test_window_caseid_1979919(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.get_four_windows_postion(pos=WinPos.percent_100)
        self.bus_comm.stop_send_pdu("bodycan", "DdmBodyFr04")
        sleep(1)
        self.bus_comm.set_windows_position(pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        sleep(2)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.bus_comm.resume_send_pdu("bodycan", "DdmBodyFr04")

    
    @allure.title("如果副驾车窗位置信号没有更新，检测BGM是否会判断车窗当前位置时采用上一状态")
    @pytest.mark.full
    def test_window_caseid_1979918(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.get_four_windows_postion(pos=WinPos.percent_100)
        self.bus_comm.stop_send_pdu("bodycan", "PdmBodyFr01")
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        sleep(2)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)
        self.bus_comm.resume_send_pdu("bodycan", "PdmBodyFr01")

    
    @allure.title("如果左后车窗位置信号没有更新，检测BGM是否会判断车窗当前位置时采用上一状态")
    @pytest.mark.full
    def test_window_caseid_1979917(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.get_four_windows_postion(pos=WinPos.percent_100)
        self.bus_comm.stop_send_pdu("bodycan", "RldmBodyFr01")
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_rire=WinPos.percent_20)
        sleep(2)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_20)
        self.bus_comm.resume_send_pdu("bodycan", "RldmBodyFr01")

    
    @allure.title("如果右后车窗位置信号没有更新，检测BGM是否会判断车窗当前位置时采用上一状态")
    @pytest.mark.full
    def test_window_caseid_1979916(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.get_four_windows_postion(pos=WinPos.percent_100)
        self.bus_comm.stop_send_pdu("bodycan", "RrdmBodyFr01")
        sleep(1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20)
        sleep(2)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_100)
        self.bus_comm.resume_send_pdu("bodycan", "RrdmBodyFr01")

    @allure.title("如果所有车窗位置信号没有更新，检测BGM是否会判断车窗当前位置时采用上一状态")
    @pytest.mark.full
    def test_window_caseid_1979915(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.get_four_windows_postion(pos=WinPos.percent_100)
        self.bus_comm.stop_send_pdu("bodycan", "DdmBodyFr04")
        self.bus_comm.stop_send_pdu("bodycan", "PdmBodyFr01")
        self.bus_comm.stop_send_pdu("bodycan", "RldmBodyFr01")
        self.bus_comm.stop_send_pdu("bodycan", "RrdmBodyFr01")
        sleep(2)
        self.soa.get_windows_postion(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.resume_send_pdu("bodycan", "DdmBodyFr04")
        self.bus_comm.resume_send_pdu("bodycan", "PdmBodyFr01")
        self.bus_comm.resume_send_pdu("bodycan", "RldmBodyFr01")
        self.bus_comm.resume_send_pdu("bodycan", "RrdmBodyFr01")

    
    # @allure.title("如果主驾车窗位置接口的位置参数“position”为0xFF，直接执行主驾关窗指令")
    # @pytest.mark.full
    # def test_window_caseid_1979914(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.soa.get_four_windows_postion(pos=WinPos.percent_100)
    #     sleep(1)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_error)
    #     self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)


    # @allure.title("如果副驾车窗位置接口的位置参数“position”为0xFF，直接执行副驾关窗指令")
    # @pytest.mark.full
    # def test_window_caseid_1979913(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.soa.get_four_windows_postion(pos=WinPos.percent_100)
    #     sleep(1)
    #     self.bus_comm.set_windows_position(pos_pass=WinPos.percent_error)
    #     self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    
    # @allure.title("如果左后车窗位置接口的位置参数“position”为0xFF，直接执行左后关窗指令")
    # @pytest.mark.full
    # def test_window_caseid_1979912(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.soa.get_four_windows_postion(pos=WinPos.percent_100)
    #     sleep(1)
    #     self.bus_comm.set_windows_position(pos_lere=WinPos.percent_error)
    #     self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)

    
    # @allure.title("如果右后车窗位置接口的位置参数“position”为0xFF，直接执行右后关窗指令")
    # @pytest.mark.full
    # def test_window_caseid_1979911(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.soa.get_four_windows_postion(pos=WinPos.percent_100)
    #     sleep(1)
    #     self.bus_comm.set_windows_position(pos_rire=WinPos.percent_error)
    #     self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    
    # @allure.title("如果所有车窗位置接口的位置参数“position”为0xFF，直接执行所有关窗指令")
    # @pytest.mark.full
    # def test_window_caseid_1979910(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.soa.get_four_windows_postion(pos=WinPos.percent_100)
    #     sleep(1)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_error,pos_pass=WinPos.percent_error,pos_lere=WinPos.percent_error,pos_rire=WinPos.percent_error)
    #     self.bus_comm.check_four_windows_position_req(pos=WinPos.close)
    
    @allure.title("验证BGM是否能正确获取所有窗户电气故障信息")
    @pytest.mark.smoke
    def test_caseid_118215(self):
        self.set_window_error_before_msg()
        self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', 1)
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinFailrStsAtPass', 1)
        self.bus_comm.set("bodycan","RldmBodyFr01", 'WinFailrStsAtReLe', 1)
        self.bus_comm.set("bodycan","RrdmBodyFr01", 'WinFailrStsAtReRi', 1)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':3,'faultMsg':'','window':0},{'fault':3,'faultMsg':'','window':1},{'fault':3,'faultMsg':'','window':2},{'fault':3,'faultMsg':'','window':3}]})
        self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', 0)
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinFailrStsAtPass', 0)
        self.bus_comm.set("bodycan","RldmBodyFr01", 'WinFailrStsAtReLe', 0)
        self.bus_comm.set("bodycan","RrdmBodyFr01", 'WinFailrStsAtReRi', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':0,'faultMsg':'','window':4}]})

   
    @allure.title("验证BGM是否能正确获取所有窗户窗户热保护故障信息")
    @pytest.mark.smoke
    def test_caseid_118214(self):
        self.set_window_error_before_msg()
        self.bus_comm.set("bodycan","DdmBodyFr03", 'WinThermlStsAtDrvr', 1)
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinThermlStsAtPass', 1)
        self.bus_comm.set("bodycan","RldmBodyFr02", 'WinThermlStsAtReLe', 1)
        self.bus_comm.set("bodycan","RrdmBodyFr02", 'WinThermlStsAtReRi', 1)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':4,'faultMsg':'','window':0},{'fault':4,'faultMsg':'','window':1},{'fault':4,'faultMsg':'','window':2},{'fault':4,'faultMsg':'','window':3}]})
        self.bus_comm.set("bodycan","DdmBodyFr03", 'WinThermlStsAtDrvr', 0)
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinThermlStsAtPass', 0)
        self.bus_comm.set("bodycan","RldmBodyFr02", 'WinThermlStsAtReLe', 0)
        self.bus_comm.set("bodycan","RrdmBodyFr02", 'WinThermlStsAtReRi', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':0,'faultMsg':'','window':4}]})
        
    @allure.title("验证BGM是否能正确上报右后窗户热保护故障信息")
    @pytest.mark.full
    def test_caseid_118216(self):
        self.single_window_error_before("right")
        self.bus_comm.set("bodycan","RrdmBodyFr02", 'WinThermlStsAtReRi', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':4,'faultMsg':'','window':3}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':4,'faultMsg':'','window':3}]})
        self.bus_comm.set("bodycan","RrdmBodyFr02", 'WinThermlStsAtReRi', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':0,'faultMsg':'','window':3}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':0,'faultMsg':'','window':3}]}]})
        
    @allure.title("验证BGM是否能正确上报右后窗户电气故障信息")
    @pytest.mark.full
    def test_caseid_118217(self):
        self.single_window_error_before("right")
        self.bus_comm.set("bodycan","RrdmBodyFr01", 'WinFailrStsAtReRi', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':3,'faultMsg':'','window':3}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {},{'out':[{'fault':3,'faultMsg':'','window':3}]})
        self.bus_comm.set("bodycan","RrdmBodyFr01", 'WinFailrStsAtReRi', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':0,'faultMsg':'','window':3}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {},{'out':[{'fault':0,'faultMsg':'','window':3}]})
        
    @allure.title("验证BGM是否能正确上报左后窗户热保护故障信息")
    @pytest.mark.full
    def test_caseid_118218(self):
        self.single_window_error_before("left")
        self.bus_comm.set("bodycan","RldmBodyFr02", 'WinThermlStsAtReLe', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':4,'faultMsg':'','window':2}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':4,'faultMsg':'','window':2}]})
        self.bus_comm.set("bodycan","RldmBodyFr02", 'WinThermlStsAtReLe', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'faults':[{'fault':0,'faultMsg':'','window':2}]}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'fault':0,'faultMsg':'','window':2}]})
        
    @allure.title("验证BGM是否能正确上报左后窗户电气故障信息")
    @pytest.mark.full
    def test_caseid_118219(self):
        self.single_window_error_before("left")
        self.bus_comm.set("bodycan","RldmBodyFr01", 'WinFailrStsAtReLe', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':3,'faultMsg':'','window':2}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':3,'faultMsg':'','window':2}]})
        self.bus_comm.set("bodycan","RldmBodyFr01", 'WinFailrStsAtReLe', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'faults':[{'fault':0,'faultMsg':'','window':2}]}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'fault':0,'faultMsg':'','window':2}]})
        
    @allure.title("验证BGM是否能正确上报副驾驶位窗户热保护故障信息")
    @pytest.mark.full
    def test_caseid_118220(self):
        self.single_window_error_before("pass")
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinThermlStsAtPass', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':4,'faultMsg':'','window':1}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':4,'faultMsg':'','window':1}]})
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinThermlStsAtPass', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'faults':[{'fault':0,'faultMsg':'','window':1}]}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'fault':0,'faultMsg':'','window':1}]})
        
    @allure.title("验证BGM是否能正确上报副驾驶位窗户电气故障信息")
    @pytest.mark.full
    def test_caseid_118221(self):
        self.single_window_error_before("pass")
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinFailrStsAtPass', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':3,'faultMsg':'','window':1}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':3,'faultMsg':'','window':1}]})
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinFailrStsAtPass', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'faults':[{'fault':0,'faultMsg':'','window':1}]}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'fault':0,'faultMsg':'','window':1}]})
        
    @allure.title("验证BGM是否能正确上报主驾驶车窗热保护故障信息")
    @pytest.mark.full
    def test_caseid_118222(self):
        self.single_window_error_before("drvr")
        self.bus_comm.set("bodycan","DdmBodyFr03", 'WinThermlStsAtDrvr', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':4,'faultMsg':'','window':0}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':4,'faultMsg':'','window':0}]})
        self.bus_comm.set("bodycan","DdmBodyFr03", 'WinThermlStsAtDrvr', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'faults':[{'fault':0,'faultMsg':'','window':0}]}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'fault':0,'faultMsg':'','window':0}]})
        
    @allure.title("验证BGM是否能正确上报主驾驶车窗电气故障信息")
    @pytest.mark.full
    def test_caseid_118223(self):
        self.single_window_error_before("drvr")
        self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', 1)
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'faults':[{'fault':3,'faultMsg':'','window':0}]}]})
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'fault':3,'faultMsg':'','window':0}]})
        self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', 0)
        self.soa.send_method_request("WindowService_client", "GetFaultInfo", {}, {'out':[{'faults':[{'fault':0,'faultMsg':'','window':0}]}]})
        self.soa.send_method_request("WindowService_client", 'WindowFault', {}, {'out':[{'fault':0,'faultMsg':'','window':0}]})
        
    