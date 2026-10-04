#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_windows_rain.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设窗户下雨直接用例
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


@allure.feature("BGM车控车设/WTI")
@allure.story("车窗故障")
@pytest.mark.run(order=1)
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WindowService_client","WindowAppService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        sleep(0.5)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)

    def after_each_func(self, ecu):
        sleep(3)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    def set_test_before(self,signal_value,receive_value):
        self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', signal_value)
        self.soa.send_method_request("WindowService_client", 'WarningMsgList', {}, {"list": [{"name": "Driver Window Failure","info": receive_value}]})
        self.soa.send_method_request("WindowService_client", 'GetWarningMsgList', {}, {"out": [{"name": "Driver Window Failure","info": receive_value}]})
        self.bus_comm.set("bodycan","PdmBodyFr03", 'WinFailrStsAtPass', signal_value)
        self.soa.send_method_request("WindowService_client", 'WarningMsgList', {}, {"list": [{"name": "Passenger Window Failure","info": receive_value}]})
        self.soa.send_method_request("WindowService_client", 'GetWarningMsgList', {}, {"out": [{"name": "Passenger Window Failure","info":receive_value}]})
        self.bus_comm.set("bodycan","RldmBodyFr01", 'WinFailrStsAtReLe', signal_value)
        self.soa.send_method_request("WindowService_client", 'WarningMsgList', {}, {"list": [{"name": "Rear Left Window Failure","info": receive_value}]})
        self.soa.send_method_request("WindowService_client", 'GetWarningMsgList', {}, {"out": [{"name": "Rear Left Window Failure","info": receive_value}]})
        self.bus_comm.set("bodycan","RrdmBodyFr01", 'WinFailrStsAtReRi', signal_value)
        self.soa.send_method_request("WindowService_client", 'WarningMsgList', {}, {"list": [{"name": "Rear Right  Window Failure","info": receive_value}]})
        self.soa.send_method_request("WindowService_client", 'GetWarningMsgList', {}, {"out": [{"name": "Rear Right  Window Failure","info":receive_value}]})
    
    def driver_hot_test_before(self,signal_value,receive_value):
        self.bus_comm.set("bodycan","DdmBodyFr01",'WinFailrStsAtDrvr', signal_value)
        self.bus_comm.set("bodycan","DdmBodyFr03", 'WinThermlStsAtDrvr', signal_value)
        self.soa.send_method_request("WindowService_client", 'WarningMsgList', {}, {"list": [{"name": "Driver Window Motor Overheating","info":receive_value}]})
        self.soa.send_method_request("WindowService_client", 'GetWarningMsgList', {}, {"out": [{"name": "Driver Window Motor Overheating","info": receive_value}]})

    def test_caseid_1982535(self):
        """
        车窗故障信息
        """
        self.set_test_before(0,"0")
        self.set_test_before(1,"1")
        self.set_test_before(0,"0")
        
    def test_caseid_1982534(self):
        """
        主驾车窗热保护故障
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.driver_hot_test_before(0,"0")
        self.driver_hot_test_before(1,"1")
        self.driver_hot_test_before(0,"0")
        