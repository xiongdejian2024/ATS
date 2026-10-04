#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_climate_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2024/2/29 15:30
@Description : BGM车控车设空调
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
@allure.story("空调")
class TestClimateCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WTIService_client", "ResetSOAConfigService_client", "ClimateControlService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        pass

    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
        
    @allure.title("PM2.5系统故障")
    @pytest.mark.full
    def test_climate_soa_caseid_1981002(self):
        self.bus_comm.set_singal("bodycan", "CcmBodyFr25", "IntPm25StsFrmClima", 3)
        self.soa.get_warning_msg_List(name="PM2.5 System Error", info="1")
        self.bus_comm.set_singal("bodycan", "CcmBodyFr25", "IntPm25StsFrmClima", 1)
        self.soa.get_warning_msg_List(name="PM2.5 System Error", info="0")
     
    # @allure.title("前排出风口调节故障_VentnActr0XBlckSts") 
    # @pytest.mark.full
    # def test_caseid_1982565(self):
    #     self.bus_comm.set_singal("bodycan", "CcmBodyFr62", "VentnActr01BlckSts", 1)
    #     self.soa.get_warning_msg_List(name="Front Vent Adjustment Error", info="1")
    #     self.bus_comm.set_singal("bodycan", "CcmBodyFr62", "VentnActr01BlckSts", 2)
    #     self.soa.get_warning_msg_List(name="Front Vent Adjustment Error", info="0") 
        
    # @allure.title("后排出风口调节故障_VentnActr0XBlckSts") 
    # @pytest.mark.full
    # def test_caseid_1982567(self):
    #     self.bus_comm.set_singal("bodycan", "CcmBodyFr66", "VentnActr09BlckSts", 1)
    #     self.soa.get_warning_msg_List(name="Rear Vent Adjustment Error", info="1")
    #     self.bus_comm.set_singal("bodycan", "CcmBodyFr66", "VentnActr10BlckSt", 1)
    #     self.soa.get_warning_msg_List(name="Rear Vent Adjustment Error", info="1")
    #     self.bus_comm.set_singal("bodycan", "CcmBodyFr66", "VentnActr10BlckSt", 2)
    #     self.soa.get_warning_msg_List(name="Rear Vent Adjustment Error", info="0")
        
    @allure.title("香氛系统故障") 
    @pytest.mark.full
    def test_caseid_1982588(self):
        self.bus_comm.set_singal("bodycan", "CcmBodyFr25", "FragStsFrmClima", 3)
        self.soa.get_warning_msg_List(name="Fragrance System Error", info="1")
        self.bus_comm.set_singal("bodycan", "CcmBodyFr25", "FragStsFrmClima", 2)
        self.soa.get_warning_msg_List(name="Fragrance System Error", info="0")
        
    # @allure.title("空气质量管理系统故障") 
    # @pytest.mark.full
    # def test_caseid_1981039(self):
    #     self.bus_comm.set_singal("bodycan", "CcmBodyFr66", "FragStsFrmClima", 3)
    #     self.soa.get_warning_msg_List(name="AQS System Error", info="1")
    #     self.bus_comm.set_singal("bodycan", "CcmBodyFr66", "FragStsFrmClima", 2)
    #     self.soa.get_warning_msg_List(name="AQS System Error", info="0")
        
    @allure.title("前排吹风模式故障") 
    @pytest.mark.full
    def test_caseid_1981035(self):
        self.bus_comm.set_singal("bodycan", "CcmBodyFr61", "HvacModFlapActrErrFrstRowLe", 1)
        self.soa.get_warning_msg_List(name="Front Mode Motor Error", info="1")
        self.bus_comm.set_singal("bodycan", "CcmBodyFr61", "HvacModFlapActrErrFrstRowRi", 1)
        self.soa.get_warning_msg_List(name="Front Mode Motor Error", info="1")
        sleep(1)
        self.bus_comm.set_singal("bodycan", "CcmBodyFr61", "HvacModFlapActrErrFrstRowLe", 2)
        self.soa.get_warning_msg_List(name="Front Mode Motor Error", info="0")
        self.bus_comm.set_singal("bodycan", "CcmBodyFr61", "HvacModFlapActrErrFrstRowRi", 2)
        self.soa.get_warning_msg_List(name="Front Mode Motor Error", info="0")
        
    @allure.title("前排出风口调节故障_VentnActr0XBlckSts") 
    @pytest.mark.full
    def test_caseid_1982565(self):
        self.bus_comm.set_singal("bodycan", "CcmBodyFr62", "VentnActr01BlckSts", 3)
        self.soa.get_warning_msg_List(name="Front Vent Adjustment Error", info="0") 
        self.bus_comm.set_singal("bodycan", "CcmBodyFr62", "VentnActr01BlckSts", 1)
        sleep(60)
        self.soa.get_warning_msg_List(name="Front Vent Adjustment Error", info="1")

    @allure.title("后排出风口调节故障_VentnActr0XBlckSts") 
    @pytest.mark.full
    def test_caseid_1982567(self):
        self.bus_comm.set_singal("bodycan", "CcmBodyFr66", "VentnActr09BlckSts", 1)
        sleep(60)
        self.soa.get_warning_msg_List(name="Rear Vent Adjustment Error", info="1")
        self.bus_comm.set_singal("bodycan", "CcmBodyFr66", "VentnActr09BlckSts", 3)
        self.soa.get_warning_msg_List(name="Rear Vent Adjustment Error", info="0")
        
    @allure.title("空气质量管理系统故障") 
    @pytest.mark.full
    def test_caseid_1981039(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_singal("bodycan", "CEMBodyFr14", "HmiHvacFanLvlFrnt", 3)
        self.bus_comm.set_singal("backbonefr", "CemBackBoneFr12", "OutdAirQlyQf", 0)
        sleep(5)
        self.soa.get_warning_msg_List(name="AQS System Error", info="1")
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.get_warning_msg_List(name="AQS System Error", info="0")