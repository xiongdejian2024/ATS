#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_obdfirewall.py
@time         : 2024/2/19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''


import pytest
import allure
from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *

@allure.feature('BGM BaseTech/数字安全')
class TestOBDFireWall(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        logger.info("before_class")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.sd_tester.exit_muc_boot()
        super().after_each_func(ecu)
        
    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)


    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('OBD防火墙_打开_实际状态测试')
    @pytest.mark.repeat(100)
    def test_caseid_1991554(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='01',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,'62b16501')
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4170,unlock_level=UnLock.L5,write_data='03e8',check_data='7f2e22',check_method=Check_Method.response,recover=False)

    #BGM _SOC,BGM _MCU
    @pytest.mark.full
    @allure.story('OBD防火墙')
    @allure.title('OBD防火墙_关闭_实际状态测试')
    @pytest.mark.repeat(100)
    def test_caseid_1991555(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,unlock_level=UnLock.L7,write_data='02ff',check_data='7101a04010')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.DEFAULT,'62b16502')
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4170,unlock_level=UnLock.L5,write_data='03e8',check_data='6e4170',check_method=Check_Method.response,recover=False)


#pytest BaseTech/Stress/InformationSecurity/test_obdfirewall_press.py::TestOBDFireWall::test_caseid_1985131 --disable_partner='true'
