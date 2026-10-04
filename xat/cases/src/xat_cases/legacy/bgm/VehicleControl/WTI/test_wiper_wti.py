#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_wiper_maintenance_abc.py
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


@allure.feature("车控车设")
@allure.story("后视镜功能")
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WiperService_client","WTIService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.empty_all()

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    def set_pre_condition_for_maintain_service(self, wash_func_sts: isOn, maintain_pos: isOn, wiper_mode: WiperMode,
                                               usage_mode: Union[UsageMode, None] = None,
                                               car_mode: Union[CarMode, None] = None, ccp: dict = {}):
        self.mix.set_common_precontion(usage_mode=usage_mode, car_mode=car_mode, ccp=ccp)
        self.soa.hmi_set_wiper_wash_func(WiperPos.Front, wash_func_sts)
        self.soa.hmi_set_wiper_maintaince_pos(maintain_pos)
        self.soa.hmi_set_wiper_mode(WiperPos.Front, wiper_mode)

    
    # @allure.title("退出雨刮维修位置信息提醒") 
    # @pytest.mark.sanity
    # def test_caseid_1982547(self):
    #     self.set_pre_condition_for_maintain_service(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL,
    #                                                 ccp={401: 0x2}, wash_func_sts=isOn.Off, maintain_pos=isOn.On,
    #                                                 wiper_mode=WiperMode.Off)
    #     sleep(2)
    #     self.soa.hmi_set_wiper_maintaince_pos(isOn.Off)
    #     self.soa.get_and_event_check_warning_info_list(name = "Wiper Exit Repair Position",info = "0")
    #     sleep(2)
    #     self.soa.hmi_set_wiper_maintaince_pos(isOn.On)
    #     self.soa.get_and_event_check_warning_info_list(name = "Wiper Exit Repair Position",info = "1")



    # @allure.title("RLSM故障信息")
    # @pytest.mark.sanity
    # def test_caseid_1982544(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,ccp={401: 0x2})
    #     self.mix.generate_dtc_fault(dtc_fault=DTCFault.CommunicationFail_CEM_and_RSLM,last_time=5)
    #     # self.soa.get_and_event_check_warning_info_list(name = "Wiper Sensor Failure",info = "1")
    #     self.sd_tester.dtc_read_and_check(dtc=DTCFault.CommunicationFail_CEM_and_RSLM, dtc_sts=DTCSts.CurrentFailed, fault_sts=True)

    #     self.mix.remove_dtc_fault(dtc_fault=DTCFault.CommunicationFail_CEM_and_RSLM,last_time=2)
    #     # self.soa.get_and_event_check_warning_info_list(name = "Wiper Sensor Failure",info = "0")
    #     self.sd_tester.dtc_read_and_check(dtc=DTCFault.CommunicationFail_CEM_and_RSLM, dtc_sts=DTCSts.WithHistoryWithoutCurrent, fault_sts=True)

        

